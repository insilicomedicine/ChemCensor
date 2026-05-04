import pytest

from chemcensor.basic import Molecule
from chemcensor.basic import Reaction
from chemcensor.basic import ReactionTransform
from chemcensor.basic import SENTINEL
from chemcensor.processing.errors.reaction_transform_errors import (
    ReactionTransformCreationError,
)
from chemcensor.processing.errors.reaction_transform_errors import (
    ReactionTransformEmptyReactionSMILESError,
)
from chemcensor.processing.transform_creator import TransformCreator


@pytest.fixture
def creator() -> TransformCreator:
    return TransformCreator()


@pytest.fixture
def valid_mapped_reaction() -> Reaction:
    """Reaction with valid atom-mapped processed_reaction_smiles."""
    return Reaction(
        reaction_smiles="[CH3:1][OH:2]>>[CH3:1][O-:2]",
        processed_reaction_smiles="[CH3:1][OH:2]>>[CH3:1][O-:2]",
    )


@pytest.fixture
def valid_multi_reactant_reaction() -> Reaction:
    """Reaction with multiple reactants."""
    return Reaction(
        reaction_smiles="[C:1].[N:2]>>[C:1][N:2]",
        processed_reaction_smiles="[C:1].[N:2]>>[C:1][N:2]",
    )


@pytest.fixture
def empty_processed_smiles_reaction() -> Reaction:
    """Reaction whose processed_reaction_smiles is empty."""
    return Reaction(
        reaction_smiles="CO>>CO",
        processed_reaction_smiles="",
    )


@pytest.fixture
def invalid_smiles_reaction() -> Reaction:
    """Reaction with invalid SMILES in processed_reaction_smiles."""
    return Reaction(
        reaction_smiles="invalid>>invalid",
        processed_reaction_smiles="invalid>>invalid",
    )


@pytest.fixture
def failed_reaction_from_downstream_processor():
    return SENTINEL


@pytest.fixture
def batch(
    valid_mapped_reaction,
    valid_multi_reactant_reaction,
    empty_processed_smiles_reaction,
    failed_reaction_from_downstream_processor,
):
    return [
        valid_mapped_reaction,
        valid_multi_reactant_reaction,
        empty_processed_smiles_reaction,
        failed_reaction_from_downstream_processor,
    ]


@pytest.fixture
def missing_product_atom_map_reaction() -> Reaction:
    """Reaction where product has no atom map."""
    return Reaction(
        reaction_smiles="[CH3:1][OH:2]>>CO",
        processed_reaction_smiles="[CH3:1][OH:2]>>CO",
    )


@pytest.fixture
def missing_reactants_atom_map_reaction() -> Reaction:
    """Reaction where reactants have no atom map."""
    return Reaction(
        reaction_smiles="CO>>[CH3:1][OH:2]",
        processed_reaction_smiles="CO>>[CH3:1][OH:2]",
    )


def test_process_returns_reaction_with_transform(
    creator: TransformCreator, valid_mapped_reaction: Reaction
) -> None:
    """process() should populate reaction_transform on the returned Reaction."""
    result = creator.process(valid_mapped_reaction)
    assert result.reaction_transform is not None
    assert isinstance(result.reaction_transform, ReactionTransform)
    assert result.reaction_transform.reactants[0] == (
        Molecule.from_atom_mapped_smiles("[CH3:1][OH:2]")
    )
    assert result.reaction_transform.product == Molecule.from_atom_mapped_smiles(
        "[CH3:1][O-:2]"
    )
    assert result.reaction_transform.pR_map == {0: (0, 0), 1: (0, 1)}
    assert result.reaction_transform.Rp_map == ({0: 0, 1: 1},)
    assert result.reaction_transform.p_reacting_atoms == (1,)
    assert result.reaction_transform.R_reacting_atoms == ((1,),)


def test_process_preserves_original_fields(
    creator: TransformCreator, valid_mapped_reaction: Reaction
) -> None:
    """process() should not alter other Reaction fields."""
    result = creator.process(valid_mapped_reaction)
    assert result.reaction_smiles == valid_mapped_reaction.reaction_smiles
    assert (
        result.processed_reaction_smiles
        == valid_mapped_reaction.processed_reaction_smiles
    )


def test_process_multi_reactant_reaction(
    creator: TransformCreator, valid_multi_reactant_reaction: Reaction
) -> None:
    """process() should handle reactions with multiple reactants."""
    result = creator.process(valid_multi_reactant_reaction)
    assert result.reaction_transform is not None
    assert len(result.reaction_transform.reactants) == 2
    assert result.reaction_transform.reactants[0] == (
        Molecule.from_atom_mapped_smiles("[C:1]")
    )
    assert result.reaction_transform.reactants[1] == (
        Molecule.from_atom_mapped_smiles("[N:2]")
    )
    assert result.reaction_transform.product == (
        Molecule.from_atom_mapped_smiles("[C:1][N:2]")
    )
    assert result.reaction_transform.pR_map == {0: (0, 0), 1: (1, 0)}
    assert result.reaction_transform.Rp_map == ({0: 0}, {0: 1})
    assert result.reaction_transform.p_reacting_atoms == (0, 1)
    assert result.reaction_transform.R_reacting_atoms == ((0,), (0,))


# ============================================================================
# Error tests
# ============================================================================


def test_process_empty_smiles_raises_empty_error(
    creator: TransformCreator, empty_processed_smiles_reaction: Reaction
) -> None:
    """process() should raise ReactionTransformEmptyReactionSMILESError
    when processed_reaction_smiles is empty."""
    with pytest.raises(ReactionTransformEmptyReactionSMILESError):
        creator.process(empty_processed_smiles_reaction)


def test_process_invalid_smiles_raises_creation_error(
    creator: TransformCreator, invalid_smiles_reaction: Reaction
) -> None:
    """process() should wrap MoleculeError into ReactionTransformCreationError."""
    with pytest.raises(ReactionTransformCreationError):
        creator.process(invalid_smiles_reaction)


def test_process_missing_product_atom_map_raises_creation_error(
    creator: TransformCreator, missing_product_atom_map_reaction: Reaction
) -> None:
    """process() should wrap ProductMissingAtomMapError into
    ReactionTransformCreationError."""
    with pytest.raises(ReactionTransformCreationError):
        creator.process(missing_product_atom_map_reaction)


def test_process_missing_reactants_atom_map_raises_creation_error(
    creator: TransformCreator, missing_reactants_atom_map_reaction: Reaction
) -> None:
    """process() should wrap ReactantsMissingAtomMapError into
    ReactionTransformCreationError."""
    with pytest.raises(ReactionTransformCreationError):
        creator.process(missing_reactants_atom_map_reaction)


def test_process_creation_error_chains_original_exception(
    creator: TransformCreator, invalid_smiles_reaction: Reaction
) -> None:
    """ReactionTransformCreationError should chain the original exception."""
    with pytest.raises(ReactionTransformCreationError) as exc_info:
        creator.process(invalid_smiles_reaction)
    assert exc_info.value.__cause__ is not None
