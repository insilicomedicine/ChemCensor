from dataclasses import replace
from typing import Sequence

import numpy as np
from frozendict import frozendict

from ..basic import FunctionalGroups
from ..basic import Reaction
from ..basic import ReactionCenter
from ..basic import ReactionTransform
from ..basic.errors.fg_finder_errors import FGFinderNoReactionCentersError
from ..basic.errors.fg_finder_errors import FGFinderNoTransformError
from ..basic.molecule import Molecule


class FGFinder:
    """Finds functional groups in reactions.

    For each :class:`ReactionCenter` attached to a :class:`Reaction`, computes a
    binary ``fg_signature`` indicating which functional groups from the
    :class:`FunctionalGroups` collection are present in the reaction environment
    (product **and** reactants), *excluding* matches that overlap with the
    reacting-fragment atom indices stored on the center
    (``product_indices`` / ``reactant_indices``).

    :param fg_collection: The collection of functional groups to search for.
    :type fg_collection: FunctionalGroups
    """

    def __init__(self, fg_collection: FunctionalGroups) -> None:
        self.fg_collection = fg_collection

    def find(self, reaction: Reaction) -> Reaction:
        """Compute functional-group signatures for every reaction center.

        :param reaction: A reaction that already carries an annotated
            :class:`ReactionTransform` and at least one :class:`ReactionCenter`.
        :type reaction: Reaction
        :return: A copy of *reaction* whose reaction centers have their
            ``fg_signature`` fields populated.
        :rtype: Reaction
        :raises FGFinderNoTransformError: If *reaction* has no annotated
            :class:`ReactionTransform`.
        """
        if not reaction.reaction_transform:
            raise FGFinderNoTransformError(reaction)

        if not reaction.reaction_centers:
            raise FGFinderNoReactionCentersError(reaction)

        updated_centers = {
            ct: replace(
                rc,
                fg_signature=self._compute_signature(
                    reaction.reaction_transform,
                    rc,
                ),
            )
            for ct, rc in reaction.reaction_centers.items()
        }

        return replace(reaction, reaction_centers=frozendict(updated_centers))

    def _compute_signature(
        self,
        transform: ReactionTransform,
        rc: ReactionCenter,
    ) -> np.ndarray:
        """Compute the combined FG signature for a reaction center.

        The product signature and every reactant signature are united with
        logical OR, mirroring the legacy ``compute_fingeprint_for_transform``.
        :param transform: ReactionTransform object
        :type transform: ReactionTransform
        :param rc: ReactionCenter object
        :type rc: ReactionCenter
        :return: Binary vector indicating which functional groups are present
        :rtype: np.ndarray
        """
        # Product contribution
        signature = self._compute_mol_signature(
            transform.product, rc.product_indices, rc.fg_signature
        )

        # Reactant contributions
        for i, reactant in enumerate(transform.reactants):
            skip_indices = (
                rc.reactant_indices[i] if i < len(rc.reactant_indices) else frozenset()
            )
            reactant_sig = self._compute_mol_signature(
                reactant, skip_indices, rc.fg_signature
            )
            signature = np.logical_or(signature, reactant_sig).astype(np.uint8)

        return signature

    def _compute_mol_signature(
        self,
        mol: Molecule,
        skip_indices: frozenset[int],
        fg_signature: np.ndarray,
    ) -> np.ndarray:
        """Build a binary vector for a single molecule.

        A bit is set to 1 if the corresponding functional group has **at least
        one** substructure match whose atom indices do **not** intersect with
        *skip_indices* (the reacting fragment).
        :param mol: Molecule object
        :type mol: Molecule
        :param skip_indices: Atom indices to skip
        :type skip_indices: frozenset[int]
        :return: Binary vector indicating which functional groups are present
        :rtype: np.ndarray
        """
        signature = fg_signature.copy()

        matched_groups = self.fg_collection.identify_functional_groups(mol)
        for matched_group in matched_groups:
            pos = matched_group.functional_group.idx
            for match_set in matched_group.matching_sets:
                if skip_indices.isdisjoint(match_set):
                    signature[pos] = 1
                    break

        return signature

    def find_for_batch_and_annotate(
        self, reactions: Sequence[Reaction], patents: Sequence[str]
    ) -> Sequence[Reaction]:
        """Will be used in DB composition.
        Find functional groups for a batch of reactions and
        annotate them with patent IDs.
        """
        raise NotImplementedError("Not implemented")
