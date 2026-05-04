from dataclasses import replace
from typing import Sequence

import numpy as np
from frozendict import frozendict
from rdkit import Chem

from ..basic import Molecule
from ..basic import Reaction
from ..basic.functional_groups import FunctionalGroups
from ..rules.functional_groups import FG_COLLECTION_SEAR
from .base import process_batch as _process_batch
from .errors.sear_annotator_errors import EmptyReactionTransformError
from .errors.sear_annotator_errors import NoReactantsReactingAtomsError


CH_SMARTS = Chem.MolFromSmarts("[cH]")

_SEAR_FG_IDX_TO_POS: frozendict[int, int] = frozendict(
    {fg.idx: pos for pos, fg in enumerate(FG_COLLECTION_SEAR.known_groups)}
)


def _get_mapped_reacting_ch_atoms(
    molecule: Molecule,
    reacting_atoms: tuple[int, ...],
) -> frozenset[int]:
    """Get mapped aromatic ``cH`` atoms that belong to the reacting site.

    :param molecule: Molecule to check
    :type molecule: Molecule
    :param reacting_atoms: Reacting atoms indices
    :type reacting_atoms: tuple[int, ...]
    :return: Reacting aromatic ``cH`` atom indices that are mapped to product.
    :rtype: frozenset[int]
    """
    atom_mapped_rdmol = molecule.atom_mapped_canonical_rdmol

    # get all aromatic ``cH`` atoms in the molecule
    matches = atom_mapped_rdmol.GetSubstructMatches(CH_SMARTS)
    if not matches:
        return frozenset()

    reacting_atoms_set = set(reacting_atoms)
    matched_atoms = {idx for match in matches for idx in match}

    # filter aromatic ``cH`` atoms that belong to the reacting site
    # and are mapped to product
    return frozenset(
        idx
        for idx in matched_atoms & reacting_atoms_set
        if atom_mapped_rdmol.GetAtomWithIdx(idx).GetAtomMapNum() > 0
    )


class SeArAnnotator:
    """Annotates reaction with SEAr information."""

    functional_groups: FunctionalGroups

    def __init__(self, functional_groups: FunctionalGroups) -> None:
        """Initialize SeArAnnotator with functional groups.

        :param functional_groups: Pre-filtered functional groups for SEAr detection
        :type functional_groups: FunctionalGroups
        """
        self.functional_groups = functional_groups

    def process(self, reaction: Reaction) -> Reaction:
        """Annotate reaction with SEAr information. The reaction is considered SEAr
        if it contains at least one SEAr functional group that includes mapped
        aromatic ``cH`` atoms that belong to the reacting site. If such a functional
        group is found, the reaction is considered SEAr and the corresponding
        bits in ``sear_signature`` (aligned with :data:`FG_COLLECTION_SEAR`) are set.

        :param reaction: Reaction to annotate
        :type reaction: Reaction
        :return: Annotated reaction with ``is_sear_reaction`` and
                ``sear_signature`` attributes set
        :rtype: Reaction
        """
        transform = reaction.reaction_transform

        if transform is None:
            raise EmptyReactionTransformError()

        if transform.R_reacting_atoms is None:
            raise NoReactantsReactingAtomsError()

        is_sear = False
        sear_hit_indices: set[int] = set()

        # Identify functional groups in each reactant
        for reactant, r_reacting_atoms in zip(
            transform.reactants, transform.R_reacting_atoms
        ):
            # check if reactant has reacting atoms
            if not r_reacting_atoms:
                continue

            # get mapped aromatic ``cH`` atoms that belong to the reacting site
            reacting_ch_atoms = _get_mapped_reacting_ch_atoms(
                molecule=reactant,
                reacting_atoms=r_reacting_atoms,
            )
            if not reacting_ch_atoms:
                continue

            # identify sear functional groups in reactant
            matched_sear_groups = self.functional_groups.identify_functional_groups(
                reactant
            )
            # filter sear functional groups that include mapped aromatic ``cH``
            # atoms that belong to the reacting site by checking the first index of
            # matched pattern (corresponds to cH atom in pattern)
            reacting_sear_groups = tuple(
                matched_group
                for matched_group in matched_sear_groups
                if any(
                    matching_set[0] in reacting_ch_atoms
                    for matching_set in matched_group.matching_sets
                )
            )

            # if there are sear functional groups that include mapped aromatic ``cH``
            # atoms that belong to the reacting site, set is_sear_reaction to True
            # and record SEAr functional-group indices for the signature vector
            if reacting_sear_groups:
                is_sear = True
                sear_hit_indices |= {
                    matched_group.functional_group.idx
                    for matched_group in reacting_sear_groups
                }

        sear_signature = np.zeros(FG_COLLECTION_SEAR.num_groups, dtype=np.uint8)
        for fg_idx in sear_hit_indices:
            pos = _SEAR_FG_IDX_TO_POS.get(fg_idx)
            if pos is not None:
                sear_signature[pos] = 1

        return replace(
            reaction,
            is_sear_reaction=is_sear,
            sear_signature=sear_signature,
        )

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        """Annotate a batch of reactions with SEAr information.

        :param reactions: Batch of reactions to process
        :type reactions: Sequence[Reaction]

        :return: Batch of annotated reactions
        :rtype: Sequence[Reaction]
        """
        return _process_batch(reactions=reactions, processor=self)
