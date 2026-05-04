from collections.abc import Sequence

from ..basic import MoleculeStereoSpecification
from ..basic import Reaction
from ..basic.errors.molecule_stereo_specification_errors import (
    MoleculeStereoSpecificationRuntimeError,
)
from ..basic.molecule_stereo_specification import collect_pseudoasymmetric_centers
from .base import process_batch as _process_batch
from .errors.static_stereo_validator_errors import (
    StaticStereoValidatorEmptyStereoSpecificationError,
)
from .errors.static_stereo_validator_errors import (
    StaticStereoValidatorEmptyTransformError,
)
from .errors.static_stereo_validator_errors import (
    StaticStereoValidatorInconsistentStaticAtomStereoError,
)
from .errors.static_stereo_validator_errors import (
    StaticStereoValidatorInconsistentStaticBondStereoError,
)
from .errors.static_stereo_validator_errors import StaticStereoValidatorRuntimeError
from .stereo_utils import confirm_bond_stereo_consistency_in_static_part
from .stereo_utils import confirm_center_consistency_in_static_part
from .stereo_utils import get_static_assigned_atom_centers
from .stereo_utils import get_static_assigned_bond_centers


class StaticStereoValidator:
    """Validate that static stereochemistry is preserved across a reaction.

    The validator runs after reaction mapping and reaction-center detection.
    It ignores dynamic stereo around the reaction center and checks only atom
    and bond stereocenters that should remain unchanged between reactant and
    product.
    """

    def process(self, reaction: Reaction) -> Reaction:
        """Validate static stereo and return the original reaction on success.

        The method performs four steps in order:

        1. Skip cases that cannot or should not be validated here.
        2. Extract stereo specifications for product and reactants.
        3. Collect assigned static atom and bond stereocenters outside the
           reaction center.
        4. Check atom stereo first and bond stereo second.

        :param reaction: Reaction to validate.
        :type reaction: Reaction
        :return: The same reaction instance if validation succeeds.
        :rtype: Reaction

        :raises StaticStereoValidatorEmptyTransformError: If
            ``reaction.reaction_transform`` is missing.
        :raises StaticStereoValidatorEmptyStereoSpecificationError: If stereo
            extraction unexpectedly returns ``None`` for product or reactants.
        :raises StaticStereoValidatorInconsistentStaticAtomStereoError: If a
            static atom stereocenter is not preserved.
        :raises StaticStereoValidatorInconsistentStaticBondStereoError: If a
            static bond stereocenter is not preserved.
        """
        if reaction.reaction_transform is None:
            raise StaticStereoValidatorEmptyTransformError()

        # SIS reactions are already validated by the SisAnnotator.
        if reaction.is_sis_reaction:
            return reaction

        transform = reaction.reaction_transform
        reaction_smiles = reaction.processed_reaction_smiles or reaction.reaction_smiles

        # Extract stereo specs for the product and every mapped reactant.
        try:
            product_stereo_spec = MoleculeStereoSpecification.extract_from_molecule(
                m=transform.product.canonical_rdmol
            )
        except MoleculeStereoSpecificationRuntimeError as e:
            raise StaticStereoValidatorRuntimeError(
                msg=e.msg,
                smiles=e.molecule_smiles,
            ) from e
        if product_stereo_spec is None:
            raise StaticStereoValidatorEmptyStereoSpecificationError()

        reactants_stereo_specs: list[MoleculeStereoSpecification] = []
        for reactant in transform.reactants:
            try:
                reactant_stereo_spec = (
                    MoleculeStereoSpecification.extract_from_molecule(
                        m=reactant.canonical_rdmol
                    )
                )
            except MoleculeStereoSpecificationRuntimeError as e:
                raise StaticStereoValidatorRuntimeError(
                    msg=e.msg,
                    smiles=e.molecule_smiles,
                ) from e
            if reactant_stereo_spec is None:
                raise StaticStereoValidatorEmptyStereoSpecificationError()
            reactants_stereo_specs.append(reactant_stereo_spec)

        reactants_reacting_atoms = transform.R_reacting_atoms or tuple(
            tuple() for _ in reactants_stereo_specs
        )

        # Derive the static assigned atom and bond centers that must be preserved.
        product_static_assigned_atom_centers = get_static_assigned_atom_centers(
            stereo_spec=product_stereo_spec,
            reacting_atoms=transform.p_reacting_atoms,
        )
        product_static_assigned_bond_centers = get_static_assigned_bond_centers(
            stereo_spec=product_stereo_spec,
            reacting_atoms=transform.p_reacting_atoms,
        )
        reactants_static_assigned_atom_centers = tuple(
            get_static_assigned_atom_centers(
                stereo_spec=reactant_stereo_spec,
                reacting_atoms=reacting_atoms,
            )
            for reactant_stereo_spec, reacting_atoms in zip(
                reactants_stereo_specs,
                reactants_reacting_atoms,
            )
        )
        reactants_static_assigned_bond_centers = tuple(
            get_static_assigned_bond_centers(
                stereo_spec=reactant_stereo_spec,
                reacting_atoms=reacting_atoms,
            )
            for reactant_stereo_spec, reacting_atoms in zip(
                reactants_stereo_specs,
                reactants_reacting_atoms,
            )
        )
        reactants_pseudoasymmetric_atom_centers = tuple(
            frozenset(collect_pseudoasymmetric_centers(reactant_stereo_spec))
            for reactant_stereo_spec in reactants_stereo_specs
        )

        # Nothing to validate if there are no assigned static centers anywhere.
        if (
            not product_static_assigned_atom_centers
            and not product_static_assigned_bond_centers
            and not any(reactants_static_assigned_atom_centers)
            and not any(reactants_static_assigned_bond_centers)
        ):
            return reaction

        if not confirm_center_consistency_in_static_part(
            transform=transform,
            product_static_assigned_atom_centers=product_static_assigned_atom_centers,
            reactants_static_assigned_atom_centers=(
                reactants_static_assigned_atom_centers
            ),
            reactants_pseudoasymmetric_atom_centers=(
                reactants_pseudoasymmetric_atom_centers
            ),
        ):
            raise StaticStereoValidatorInconsistentStaticAtomStereoError(
                reaction_smiles=reaction_smiles
            )

        if not confirm_bond_stereo_consistency_in_static_part(
            transform=transform,
            product_static_assigned_bond_centers=product_static_assigned_bond_centers,
            reactants_static_assigned_bond_centers=(
                reactants_static_assigned_bond_centers
            ),
        ):
            raise StaticStereoValidatorInconsistentStaticBondStereoError(
                reaction_smiles=reaction_smiles
            )

        return reaction

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        """Validate a batch of reactions.

        :param reactions: Batch of reactions to validate.
        :type reactions: Sequence[Reaction]
        :return: Validated reactions in the original order.
        :rtype: Sequence[Reaction]
        """
        return _process_batch(reactions=reactions, processor=self)
