from collections.abc import Sequence
from dataclasses import replace

from ..basic import MoleculeStereoSpecification
from ..basic import Reaction
from ..basic import ReactionTransform
from ..basic.errors.molecule_stereo_specification_errors import (
    MoleculeStereoSpecificationRuntimeError,
)
from ..basic.molecule_stereo_specification import collect_pseudoasymmetric_centers
from ..basic.molecule_stereo_specification import collect_stereo_centers
from ..configs.sis_config import sis_config
from .base import process_batch as _process_batch
from .errors.sis_annotator_errors import SisAnnotatorEmptyTransformError
from .errors.sis_annotator_errors import (
    SisAnnotatorInconsistentStaticCentersError,
)
from .errors.sis_annotator_errors import SisAnnotatorRuntimeError
from .stereo_utils import bond_key


class SisAnnotator:
    """Annotate reactions with the SIS flag."""

    def is_sis_reaction(
        self,
        transform: ReactionTransform,
        stereo_spec_product: MoleculeStereoSpecification | None,
        stereo_specs_reactants: list[MoleculeStereoSpecification | None],
        reaction_smiles: str,
    ) -> bool:
        """Confirm if the reaction is a single-step stereoisomer separation (SIS):
        racemic/unassigned → single diastereomer at an atom (R/S or pseudo r/s) and/or
        alkene (E/Z).

        Delegates to :meth:`_has_sis_atom_stereo` (tetrahedral CIP) or
        :meth:`_has_sis_alkene_stereo` (E/Z).

        :param transform: ReactionTransform to check
        :type transform: ReactionTransform
        :param stereo_spec_product: pre-computed product stereo specification
        :type stereo_spec_product: MoleculeStereoSpecification | None
        :param stereo_specs_reactants: pre-computed reactant stereo specifications
        :type stereo_specs_reactants: list[MoleculeStereoSpecification | None]
        :return: True if the reaction is SIS, False otherwise
        :rtype: bool
        """
        if transform.has_reacting_atoms:
            return False
        if len(transform.reactants) > 1:
            return False
        if stereo_spec_product is None:
            return False

        stereo_spec_reactant = stereo_specs_reactants[0]
        if stereo_spec_reactant is None:
            return False

        if self._has_sis_atom_stereo(
            transform=transform,
            stereo_spec_product=stereo_spec_product,
            stereo_spec_reactant=stereo_spec_reactant,
            reaction_smiles=reaction_smiles,
        ):
            return True
        return self._has_sis_alkene_stereo(
            transform=transform,
            stereo_spec_product=stereo_spec_product,
            stereo_spec_reactant=stereo_spec_reactant,
            reaction_smiles=reaction_smiles,
        )

    def _has_sis_atom_stereo(
        self,
        transform: ReactionTransform,
        stereo_spec_product: MoleculeStereoSpecification,
        stereo_spec_reactant: MoleculeStereoSpecification,
        reaction_smiles: str,
    ) -> bool:
        """Whether the transform matches **atom** SIS (R/S or pseudo r/s): one reactant,
        no bond edits.

        Uses **CIP labels** (``atom_center_labels`` from FindMolChiralCenters), not
        raw RDKit ``GetChiralTag`` (CW/CCW): after canonicalization the same
        configuration can appear as different tetrahedral tags while R/S stays the
        same.

        **SIS** here: at least one stereocenter is **assigned** in the product
        (ordinary ``R``/``S`` or pseudo ``r``/``s``) and **unassigned** (``?``) on
        the mapped reactant atom; every other stereocenter that is **assigned** on
        both sides must keep the **same** CIP label (same diastereomer). Excludes
        racemization where product ``?`` maps to reactant R/S. The number of
        simultaneous ``?`` → ``R/S`` / ``r``/``s`` resolutions is capped by
        :attr:`SisConfig.max_simultaneous_atom_stereo_resolutions` on
        :data:`~chemcensor.configs.sis_config.sis_config`.

        :param transform: reaction transform with edit detection
        :param stereo_spec_product: product stereo specification
        :param stereo_spec_reactant: reactant stereo specification
        :return: ``True`` if this is atom-level SIS, else ``False``
        """
        p_assigned, atom_centers_unassigned_product = collect_stereo_centers(
            stereo_spec=stereo_spec_product,
        )
        p_pseudo_product = collect_pseudoasymmetric_centers(stereo_spec_product)
        product_stereo_centers = p_assigned | p_pseudo_product

        if not product_stereo_centers:
            return False

        # exclude racemization: product ``?`` at p_idx pairs with reactant R/S
        for pu in atom_centers_unassigned_product:
            mapping = transform.pR_map.get(pu)
            if mapping is None:
                continue
            _, r_atom_idx = mapping
            r_assigned, _ = collect_stereo_centers(stereo_spec=stereo_spec_reactant)
            if r_atom_idx in r_assigned:
                return False

        r_assigned, r_unassigned = collect_stereo_centers(
            stereo_spec=stereo_spec_reactant,
        )
        r_stereo_atoms = r_assigned | r_unassigned
        r_pseudoasymmetric = collect_pseudoasymmetric_centers(stereo_spec_reactant)

        has_resolved_from_unassigned = False
        atom_stereo_resolution_count = 0

        for p_center in product_stereo_centers:
            mapping = transform.pR_map.get(p_center)
            if mapping is None:
                return False
            r_idx, r_atom_idx = mapping
            if r_idx != 0:
                return False

            p_label = stereo_spec_product.atom_center_labels.get(p_center)
            r_label = stereo_spec_reactant.atom_center_labels.get(r_atom_idx)

            if r_atom_idx not in r_stereo_atoms:
                if r_atom_idx in r_pseudoasymmetric:
                    continue
                return False

            if r_atom_idx in r_unassigned:
                if p_label is not None and p_label != "?":
                    has_resolved_from_unassigned = True
                    atom_stereo_resolution_count += 1
                continue

            # assigned on both sides: must be same R/S (no net inversion)
            if r_atom_idx in r_assigned:
                if (
                    p_label is None
                    or r_label is None
                    or p_label == "?"
                    or r_label == "?"
                ):
                    raise SisAnnotatorInconsistentStaticCentersError(reaction_smiles)
                if p_label != r_label:
                    raise SisAnnotatorInconsistentStaticCentersError(reaction_smiles)

        if not has_resolved_from_unassigned:
            return False
        if (
            atom_stereo_resolution_count
            > sis_config.max_simultaneous_atom_stereo_resolutions
        ):
            return False
        return True

    def _has_sis_alkene_stereo(
        self,
        transform: ReactionTransform,
        stereo_spec_product: MoleculeStereoSpecification,
        stereo_spec_reactant: MoleculeStereoSpecification,
        reaction_smiles: str,
    ) -> bool:
        """Whether the transform matches **alkene** SIS (E/Z): one reactant,
        no bond edits.

        The product must have at least one **assigned** double-bond stereo center
        whose RDKit stereo differs from the reactant on the same bond (via ``pR_map``);
        that bond must be **unassigned** (enumerable) on the reactant. Rejects cases
        where the product still has unassigned alkene classes overlapping an assigned
        alkene on the reactant. The number of simultaneous enumerable-bond stereo
        changes is capped by `SisConfig.max_simultaneous_alkene_stereo_resolutions`
        on ~chemcensor.configs.sis_config.sis_config`.

        :param transform: reaction transform with edit detection
        :param stereo_spec_product: product stereo specification
        :param stereo_spec_reactant: reactant stereo specification
        :return: ``True`` if this is alkene E/Z SIS, else ``False``
        """
        p_assigned = {bond_key(*b) for b in stereo_spec_product.assigned_bond_centers}
        r_assigned = {bond_key(*b) for b in stereo_spec_reactant.assigned_bond_centers}
        r_unassigned = {
            bond_key(*b) for b in stereo_spec_reactant.unassigned_bond_centers
        }

        # Product bond keys in reactant index space (for overlap with r_assigned)
        mapped_p_unassigned: set[tuple[int, int]] = set()
        for pa, pb in stereo_spec_product.unassigned_bond_centers:
            ma = transform.pR_map.get(pa)
            mb = transform.pR_map.get(pb)
            if ma is None or mb is None:
                continue
            if ma[0] != mb[0]:
                continue
            mapped_p_unassigned.add(bond_key(ma[1], mb[1]))

        if mapped_p_unassigned & r_assigned:
            raise SisAnnotatorInconsistentStaticCentersError(reaction_smiles)

        product_mol = transform.product.canonical_rdmol
        reactant_mol = transform.reactants[0].canonical_rdmol

        for ra, rb in r_assigned:
            p_atom_idx_a = transform.Rp_map[0][ra]
            p_atom_idx_b = transform.Rp_map[0][rb]
            if p_atom_idx_a is None or p_atom_idx_b is None:
                raise SisAnnotatorInconsistentStaticCentersError(reaction_smiles)

            p_bk = bond_key(p_atom_idx_a, p_atom_idx_b)
            if p_bk not in p_assigned:
                raise SisAnnotatorInconsistentStaticCentersError(reaction_smiles)

            if product_mol.GetBondBetweenAtoms(
                p_atom_idx_a, p_atom_idx_b
            ).GetStereo() != (reactant_mol.GetBondBetweenAtoms(ra, rb).GetStereo()):
                raise SisAnnotatorInconsistentStaticCentersError(reaction_smiles)

        if not p_assigned:
            return False

        alkene_stereo_resolution_count = 0
        for a, b in p_assigned:
            ma = transform.pR_map.get(a)
            mb = transform.pR_map.get(b)
            if ma is None or mb is None:
                continue
            r_idx_a, ra = ma
            r_idx_b, rb = mb
            if r_idx_a != r_idx_b:
                return False
            r_mol = transform.reactants[r_idx_a].canonical_rdmol
            if (
                product_mol.GetBondBetweenAtoms(a, b).GetStereo()
                != r_mol.GetBondBetweenAtoms(ra, rb).GetStereo()
            ):
                if bond_key(ra, rb) not in r_unassigned:
                    return False
                alkene_stereo_resolution_count += 1

        if alkene_stereo_resolution_count == 0:
            return False
        if (
            alkene_stereo_resolution_count
            > sis_config.max_simultaneous_alkene_stereo_resolutions
        ):
            return False
        return True

    def process(self, reaction: Reaction) -> Reaction:
        """
        Process a Reaction object and return a new Reaction
        object with the is_sis_reaction field.

        :param reaction: Reaction to process
        :type reaction: Reaction

        :return: Processed reaction
        :rtype: Reaction

        :raises SisAnnotatorEmptyTransformError: if reaction_transform is None
        """
        if reaction.reaction_transform is None:
            raise SisAnnotatorEmptyTransformError()

        T = reaction.reaction_transform
        try:
            stereo_spec_product = MoleculeStereoSpecification.extract_from_molecule(
                m=T.product.canonical_rdmol
            )
            stereo_specs_reactants = [
                MoleculeStereoSpecification.extract_from_molecule(m=r.canonical_rdmol)
                for r in T.reactants
            ]
        except MoleculeStereoSpecificationRuntimeError as e:
            raise SisAnnotatorRuntimeError(msg=e.msg, smiles=e.molecule_smiles) from e

        if self.is_sis_reaction(
            transform=T,
            stereo_spec_product=stereo_spec_product,
            stereo_specs_reactants=stereo_specs_reactants,
            reaction_smiles=(
                reaction.processed_reaction_smiles or reaction.reaction_smiles
            ),
        ):
            return replace(reaction, is_sis_reaction=True)

        return reaction

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        """Annotate a batch of reactions with SIS information.

        :param reactions: Batch of reactions to process
        :type reactions: Sequence[Reaction]

        :return: Batch of annotated reactions
        :rtype: Sequence[Reaction]
        """
        return _process_batch(reactions=reactions, processor=self)
