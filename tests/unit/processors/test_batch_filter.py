import pytest

from chemcensor.basic import Reaction
from chemcensor.basic import SENTINEL
from chemcensor.processing import BatchFilter


@pytest.fixture
def batch_filter() -> BatchFilter:
    return BatchFilter()


@pytest.fixture
def valid_reaction1() -> Reaction:
    return Reaction(reaction_smiles="CO>>C[O-]")


@pytest.fixture
def valid_reaction2() -> Reaction:
    return Reaction(reaction_smiles="CC(O)C.Br>>CC(Br)C")


@pytest.fixture
def invalid_reaction() -> Reaction:
    return SENTINEL


@pytest.fixture
def reaction_batch(
    valid_reaction1: Reaction, valid_reaction2: Reaction, invalid_reaction: Reaction
) -> list[Reaction]:
    return [valid_reaction1, valid_reaction2, invalid_reaction]


def test_process_batch_removes_sentinels(
    batch_filter: BatchFilter, reaction_batch: list[Reaction]
) -> None:
    """process_batch() should remove sentinels from the batch."""
    result = batch_filter.process_batch(reaction_batch)
    assert len(result) == 2
