import pytest

from chemcensor.basic import Reaction
from chemcensor.basic import SENTINEL
from chemcensor.processing.errors.validator_errors import ValidationError
from chemcensor.processing.validator import Validator


@pytest.fixture
def valid_reaction1() -> Reaction:
    return Reaction(
        reaction_smiles="C[C@@H]1OCCN(C(OC(C)(C)C)=O)C1.Cl>>C[C@@H]2OCCNC2",
    )


@pytest.fixture
def valid_reaction2() -> Reaction:
    return Reaction(
        reaction_smiles="CCC=O.NCCOC.[C-]#[N+]C1CCCCC1.OC2=C([N+]([O-])=O)C=CC=C2>>O=C("
        "C(CC)N(CCOC)C3=C([N+]([O-])=O)C=CC=C3)NC4CCCCC4",
    )


@pytest.fixture
def invalid_syntax() -> Reaction:
    return Reaction(
        reaction_smiles=">>C1=CC=CC=C1",
    )


@pytest.fixture
def invalid_length() -> Reaction:
    return Reaction(
        reaction_smiles="",
    )


@pytest.fixture
def invalid_smiles() -> Reaction:
    return Reaction(
        reaction_smiles="C1=NC=CC=C>>CC2=NC=CC=C2",
    )


@pytest.fixture
def validator() -> Validator:
    return Validator()


@pytest.fixture
def reaction_batch(
    valid_reaction1, valid_reaction2, invalid_syntax, invalid_length, invalid_smiles
) -> list[Reaction]:
    return [
        valid_reaction1,
        valid_reaction2,
        invalid_syntax,
        invalid_length,
        invalid_smiles,
    ]


def test_valid_reaction1_passes(
    validator: Validator, valid_reaction1: Reaction
) -> None:
    """Valid reaction 1 passes all validators without raising."""
    result = validator.process(valid_reaction1)
    assert result.reaction_smiles == valid_reaction1.reaction_smiles


def test_valid_reaction2_passes(
    validator: Validator, valid_reaction2: Reaction
) -> None:
    """Valid reaction 2 passes all validators without raising."""
    result = validator.process(valid_reaction2)
    assert result.reaction_smiles == valid_reaction2.reaction_smiles


def test_invalid_syntax_raises_rxn_smiles_syntax_error(
    validator: Validator,
    invalid_syntax: Reaction,
) -> None:
    """Reaction with missing left part (>>only products) raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        validator.process(invalid_syntax)
    assert exc_info.value.msg == (
        "Reaction smiles must contain exactly two " "parts separated by '>>'."
    )


def test_invalid_length_raises_rxn_smiles_length_error(
    validator: Validator,
    invalid_length: Reaction,
) -> None:
    """Empty reaction_smiles raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        validator.process(invalid_length)
    assert exc_info.value.msg == "Reaction smiles must be 1-512 characters."


def test_invalid_smiles_raises_rxn_smiles_rdkit_error(
    validator: Validator,
    invalid_smiles: Reaction,
) -> None:
    """Reaction with invalid SMILES (unclosed ring) raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        validator.process(invalid_smiles)
    assert exc_info.value.msg == (
        f"Invalid smiles: " f"{invalid_smiles.reaction_smiles.split('>>')[0]}"
    )


def test_reaction_batch_passes(
    validator: Validator, reaction_batch: list[Reaction]
) -> None:
    """Reaction batch passes all validators without raising."""
    results = validator.process_batch(reaction_batch)
    assert len(results) == len(reaction_batch)
    assert not results[0].dummy
    assert not results[1].dummy
    assert results[2].dummy
    assert results[3].dummy
    assert results[4].dummy
    assert results[2] is SENTINEL
    assert results[3] is SENTINEL
    assert results[4] is SENTINEL
