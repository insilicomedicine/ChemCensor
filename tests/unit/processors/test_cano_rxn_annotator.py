import pytest

from chemcensor.basic import Reaction
from chemcensor.basic import ReactionTransform
from chemcensor.basic import SENTINEL
from chemcensor.processing.cano_rxn_annotator import CanoRxnAnnotator
from chemcensor.processing.errors.cano_rxn_annotator_errors import (
    CanoRxnAnnotatorEmptyTransformError,
)


@pytest.fixture
def annotator() -> CanoRxnAnnotator:
    return CanoRxnAnnotator()


@pytest.fixture
def single_reactant_reaction() -> Reaction:
    """Reaction with a single reactant (methanol deprotonation)."""
    return Reaction(
        reaction_smiles="[CH3:1][OH:2]>>[CH3:1][O-:2]",
        reaction_transform=ReactionTransform.from_reaction_smiles(
            "[CH3:1][OH:2]>>[CH3:1][O-:2]"
        ),
    )


@pytest.fixture
def multi_reactant_reaction() -> Reaction:
    """Reaction with two reactants."""
    return Reaction(
        reaction_smiles="[C:1].[N:2]>>[C:1][N:2]",
        reaction_transform=ReactionTransform.from_reaction_smiles(
            "[C:1].[N:2]>>[C:1][N:2]"
        ),
    )


@pytest.fixture
def multi_reactant_reaction_reverted_order() -> Reaction:
    """Reaction with two reactants."""
    return Reaction(
        reaction_smiles="[N:2].[C:1]>>[C:1][N:2]",
        reaction_transform=ReactionTransform.from_reaction_smiles(
            "[N:2].[C:1]>>[C:1][N:2]"
        ),
    )


@pytest.fixture
def no_transform_reaction() -> Reaction:
    """Reaction without a reaction transform."""
    return Reaction(reaction_smiles="CO>>CO")


@pytest.fixture
def batch(single_reactant_reaction, no_transform_reaction, multi_reactant_reaction):
    return [
        single_reactant_reaction,
        no_transform_reaction,
        multi_reactant_reaction,
    ]


# ============================================================================
# process() tests
# ============================================================================


def test_process_single_reactant(
    annotator: CanoRxnAnnotator, single_reactant_reaction: Reaction
) -> None:
    """process() should populate canonical_smiles for a single-reactant reaction."""
    result = annotator.process(single_reactant_reaction)
    assert result.canonical_smiles != ""
    assert ">>" in result.canonical_smiles
    assert result.canonical_smiles == "CO>>C[O-]"


def test_process_multi_reactant(
    annotator: CanoRxnAnnotator, multi_reactant_reaction: Reaction
) -> None:
    """process() should join multiple reactant canonical SMILES with '.'."""
    result = annotator.process(multi_reactant_reaction)
    assert result.canonical_smiles != ""
    reactants_part, product_part = result.canonical_smiles.split(">>")
    assert multi_reactant_reaction.reaction_transform is not None
    assert (
        product_part
        == multi_reactant_reaction.reaction_transform.product.canonical_smiles
    )
    reactant_smiles_set = set(reactants_part.split("."))
    expected_set = {
        r.canonical_smiles for r in multi_reactant_reaction.reaction_transform.reactants
    }
    assert reactant_smiles_set == expected_set


def test_process_reverted_order_smiles(
    annotator: CanoRxnAnnotator,
    multi_reactant_reaction: Reaction,
    multi_reactant_reaction_reverted_order: Reaction,
) -> None:
    """Changing the order of the reactants should yield the same canonical SMILES."""
    result1 = annotator.process(multi_reactant_reaction)
    result2 = annotator.process(multi_reactant_reaction_reverted_order)
    assert result1.canonical_smiles == result2.canonical_smiles


def test_process_empty_transform_raises(
    annotator: CanoRxnAnnotator, no_transform_reaction: Reaction
) -> None:
    """process() should raise the error when transform is None."""
    with pytest.raises(CanoRxnAnnotatorEmptyTransformError):
        annotator.process(no_transform_reaction)


def test_process_batch(annotator: CanoRxnAnnotator, batch) -> None:
    """process_batch() should handle failures gracefully and pass sentinels through."""
    results = annotator.process_batch(batch)
    assert len(results) == len(batch)
    assert results[0].canonical_smiles != ""
    assert not results[0].dummy
    assert results[1].dummy
    assert results[1] is SENTINEL
    assert results[2].canonical_smiles != ""
    assert not results[2].dummy
