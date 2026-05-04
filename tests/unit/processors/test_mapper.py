import re
from unittest.mock import patch

import pytest

from chemcensor.basic import Reaction
from chemcensor.basic import SENTINEL
from chemcensor.processing.errors.mapper_errors import MapperError
from chemcensor.processing.mapper import Mapper


@pytest.fixture
def mapper():
    return Mapper()


@pytest.fixture
def reaction1():
    return Reaction(
        reaction_smiles="O=C(c1ccccc1)O.NCC2COC2>>O=C(c3ccccc3)NCC4COC4",
    )


@pytest.fixture
def reaction2():
    return Reaction(
        reaction_smiles="C[C@@H]1OCCN(C(OC(C)(C)C)=O)C1.Cl>>C[C@@H]2OCCNC2",
    )


@pytest.fixture
def mapped_reaction1():
    return Reaction(
        reaction_smiles="O=C(c1ccccc1)O.NCC2COC2>>O=C(c3ccccc3)NCC4COC4",
        mapped_reaction_smiles=(
            "[NH2:3][CH2:4][CH:5]1[CH2:6][O:7][CH2:8]1."
            "O[C:2](=[O:1])[c:9]1[cH:10][cH:11][cH:12][cH:13][cH:14]1>>"
            "[O:1]=[C:2]([NH:3][CH2:4][CH:5]1[CH2:6][O:7][CH2:8]1)"
            "[c:9]1[cH:10][cH:11][cH:12][cH:13][cH:14]1"
        ),
    )


@pytest.fixture
def mapped_reaction2():
    return Reaction(
        reaction_smiles="C[C@@H]1OCCN(C(OC(C)(C)C)=O)C1.Cl>>C[C@@H]2OCCNC2",
        mapped_reaction_smiles=(
            "CC(C)(C)OC(=O)[N:4]1[CH2:3][C@H:2]([CH3:1])[O:7][CH2:6][CH2:5]1."
            "Cl>>[CH3:1][C@H:2]1[CH2:3][NH:4][CH2:5][CH2:6][O:7]1"
        ),
    )


@pytest.fixture
def failed_reaction_from_validator():
    return SENTINEL


@pytest.fixture
def reaction_will_fail_in_mapper():
    return Reaction(
        reaction_smiles="NNN>CCC",
    )


@pytest.fixture
def batch(
    reaction1, reaction2, failed_reaction_from_validator, reaction_will_fail_in_mapper
):
    return [
        reaction1,
        reaction2,
        failed_reaction_from_validator,
        reaction_will_fail_in_mapper,
    ]


# --- process() ---


def test_process_returns_reaction_with_mapped_smiles(mapper, reaction1):
    """process() returns a Reaction with non-empty mapped_reaction_smiles."""
    result = mapper.process(reaction1)
    assert isinstance(result, Reaction)
    assert result.mapped_reaction_smiles
    assert ">>" in result.mapped_reaction_smiles


def test_process_preserves_reaction_fields(mapper, reaction1):
    """process() only updates mapped_reaction_smiles; other fields unchanged."""
    result = mapper.process(reaction1)
    assert result.reaction_smiles == reaction1.reaction_smiles
    assert result.processed_reaction_smiles == reaction1.processed_reaction_smiles
    assert result.reaction_centers == reaction1.reaction_centers
    assert result.mapped_reaction_smiles != reaction1.mapped_reaction_smiles


def test_process_mapped_smiles_contains_atom_mapping(mapper, reaction1):
    """Mapped SMILES contains atom map numbers (e.g. [C:1], [2:])."""
    result = mapper.process(reaction1)
    # RXNMapper produces atom maps like [CH2:4] or [1:]
    assert re.search(r":\d+]|:\d+\)|:\d+\[", result.mapped_reaction_smiles)


def test_process_first_reaction(mapper, reaction1, mapped_reaction1):
    """process() works for first reaction SMILES."""
    result = mapper.process(reaction1)
    assert result.mapped_reaction_smiles == mapped_reaction1.mapped_reaction_smiles
    assert result.reaction_smiles == mapped_reaction1.reaction_smiles


def test_process_second_reaction(mapper, reaction2, mapped_reaction2):
    """process() works for another reaction SMILES."""
    result = mapper.process(reaction2)
    assert result.mapped_reaction_smiles == mapped_reaction2.mapped_reaction_smiles
    assert result.reaction_smiles == mapped_reaction2.reaction_smiles


# --- Error handling ---


def test_map_reaction_smiles_raises_mapper_error_on_empty_result(mapper):
    """_map_reaction_smiles raises MapperError when RXNMapper returns '>>'."""
    with patch.object(mapper._mapper, "map_reactions", return_value=iter([">>"])):
        with pytest.raises(MapperError) as exc_info:
            mapper._map_reaction_smiles(">>CC")
    assert exc_info.value.reaction_smiles == ">>CC"
    assert "empty" in exc_info.value.msg.lower()


def test_process_batch(mapper, batch):
    """process_batch() passes sentinels through and processes valid reactions."""
    results = mapper.process_batch(batch)
    assert len(results) == len(batch)
    assert not results[0].dummy
    assert not results[1].dummy
    assert results[2].dummy
    assert results[2] is SENTINEL
    assert results[3].dummy
