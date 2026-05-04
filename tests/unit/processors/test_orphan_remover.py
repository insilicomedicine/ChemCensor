import pytest
from frozendict import frozendict

from chemcensor.basic import Reaction
from chemcensor.basic import SENTINEL
from chemcensor.processing.errors.orphan_remover_errors import (
    MultipleMappedProductsError,
)
from chemcensor.processing.errors.orphan_remover_errors import NoMappedProductError
from chemcensor.processing.errors.orphan_remover_errors import NoMappedReactantsError
from chemcensor.processing.errors.orphan_remover_errors import ReactionNotSplitError
from chemcensor.processing.orphan_remover import _has_atom_mapping
from chemcensor.processing.orphan_remover import OrphanRemover


@pytest.fixture
def remover() -> OrphanRemover:
    return OrphanRemover()


def _make_reaction(mapped_smiles: str) -> Reaction:
    """Helper to create a Reaction with only mapped_reaction_smiles set."""
    return Reaction(
        reaction_smiles="",
        mapped_reaction_smiles=mapped_smiles,
        processed_reaction_smiles="",
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
def batch(mapped_reaction1, mapped_reaction2, failed_reaction_from_validator):
    return [
        mapped_reaction1,
        mapped_reaction2,
        failed_reaction_from_validator,
    ]


# ============================================================================
# _has_atom_mapping tests
# ============================================================================


def test_has_atom_mapping_with_mapping():
    """Fragment with atom mapping returns True."""
    assert _has_atom_mapping("[CH3:1][OH:2]") is True


def test_has_atom_mapping_without_mapping():
    """Fragment without atom mapping returns False."""
    assert _has_atom_mapping("CC(=O)O") is False


def test_has_atom_mapping_partial():
    """Fragment with only some atoms mapped returns True."""
    assert _has_atom_mapping("[CH3:1]CC") is True


def test_has_atom_mapping_empty():
    """Empty string returns False."""
    assert _has_atom_mapping("") is False


# ============================================================================
# Basic orphan removal
# ============================================================================


def test_removes_unmapped_reactants(remover: OrphanRemover):
    """Unmapped reactant fragments are removed."""
    rxn = _make_reaction("[CH3:1][OH:2].CC(=O)O>>[CH3:1][O-:2]")
    result = remover.process(rxn)
    assert result.processed_reaction_smiles == "[CH3:1][OH:2]>>[CH3:1][O-:2]"


def test_removes_unmapped_products(remover: OrphanRemover):
    """Unmapped product fragments are removed."""
    rxn = _make_reaction("[CH3:1][OH:2]>>[CH3:1][O-:2].O")
    result = remover.process(rxn)
    assert result.processed_reaction_smiles == "[CH3:1][OH:2]>>[CH3:1][O-:2]"


def test_removes_multiple_unmapped_reactants(remover: OrphanRemover):
    """Multiple unmapped reactant fragments are all removed."""
    rxn = _make_reaction("[CH3:1][OH:2].CC.O.NaCl>>[CH3:1][O-:2]")
    result = remover.process(rxn)
    assert result.processed_reaction_smiles == "[CH3:1][OH:2]>>[CH3:1][O-:2]"


def test_keeps_all_mapped_reactants(remover: OrphanRemover):
    """All mapped reactant fragments are preserved."""
    rxn = _make_reaction("[CH3:1][Br:2].[Na:3][OH:4]>>[CH3:1][OH:4]")
    result = remover.process(rxn)
    assert "[CH3:1][Br:2]" in result.processed_reaction_smiles
    assert "[Na:3][OH:4]" in result.processed_reaction_smiles


# ============================================================================
# Spectator removal
# ============================================================================


def test_removes_spectators_from_both_sides(remover: OrphanRemover):
    """Mapped fragments identical on both sides (spectators) are removed."""
    rxn = _make_reaction("[CH3:1][OH:2].[Na+:3]>>[CH3:1][O-:2].[Na+:3]")
    result = remover.process(rxn)
    assert result.processed_reaction_smiles == "[CH3:1][OH:2]>>[CH3:1][O-:2]"
    assert "[Na+:3]" not in result.processed_reaction_smiles


def test_removes_multiple_spectators(remover: OrphanRemover):
    """Multiple spectator fragments are all removed."""
    rxn = _make_reaction("[CH3:1][OH:2].[Na+:3].[Cl-:4]>>[CH3:1][O-:2].[Na+:3].[Cl-:4]")
    result = remover.process(rxn)
    assert result.processed_reaction_smiles == "[CH3:1][OH:2]>>[CH3:1][O-:2]"


def test_removes_orphans_and_spectators_together(remover: OrphanRemover):
    """Both orphans and spectators are removed in a single pass."""
    rxn = _make_reaction("[CH3:1][OH:2].CC.[Na+:3]>>[CH3:1][O-:2].O.[Na+:3]")
    result = remover.process(rxn)
    assert result.processed_reaction_smiles == "[CH3:1][OH:2]>>[CH3:1][O-:2]"


# ============================================================================
# Clean reaction (nothing to remove)
# ============================================================================


def test_clean_reaction_unchanged(remover: OrphanRemover):
    """Reaction without orphans or spectators passes through."""
    rxn = _make_reaction("[CH3:1][OH:2]>>[CH3:1][O-:2]")
    result = remover.process(rxn)
    assert result.processed_reaction_smiles == "[CH3:1][OH:2]>>[CH3:1][O-:2]"


def test_preserves_other_reaction_fields(remover: OrphanRemover):
    """process() only sets processed_reaction_smiles, other fields unchanged."""
    rxn = Reaction(
        reaction_smiles="original",
        mapped_reaction_smiles="[CH3:1][OH:2]>>[CH3:1][O-:2]",
        processed_reaction_smiles="old",
    )
    result = remover.process(rxn)
    assert result.reaction_smiles == "original"
    assert result.mapped_reaction_smiles == "[CH3:1][OH:2]>>[CH3:1][O-:2]"
    assert result.reaction_centers == frozendict()


# ============================================================================
# Error cases
# ============================================================================


def test_raises_reaction_not_split(remover: OrphanRemover):
    """Raises ReactionNotSplitError when >> separator is missing."""
    rxn = _make_reaction("[CH3:1][OH:2]")
    with pytest.raises(ReactionNotSplitError):
        remover.process(rxn)


def test_raises_no_mapped_product(remover: OrphanRemover):
    """Raises NoMappedProductError when product has no mapped fragments."""
    rxn = _make_reaction("[CH3:1][OH:2]>>CC")
    with pytest.raises(NoMappedProductError):
        remover.process(rxn)


def test_raises_no_mapped_reactants(remover: OrphanRemover):
    """Raises NoMappedReactantsError when no reactants have mapping."""
    rxn = _make_reaction("CC.O>>[CH3:1][O-:2]")
    with pytest.raises(NoMappedReactantsError):
        remover.process(rxn)


def test_raises_multiple_mapped_products(remover: OrphanRemover):
    """Raises MultipleMappedProductsError when >1 product has mapping."""
    rxn = _make_reaction("[CH3:1][Br:2].[Na:3][OH:4]>>[CH3:1][OH:4].[Na:3][Br:2]")
    with pytest.raises(MultipleMappedProductsError):
        remover.process(rxn)


def test_raises_when_all_products_are_spectators(remover: OrphanRemover):
    """Raises NoMappedProductError when all mapped products are spectators."""
    # Identity reaction — product == reactant → spectator → nothing left
    rxn = _make_reaction("[CH3:1][OH:2]>>[CH3:1][OH:2]")
    with pytest.raises(NoMappedProductError):
        remover.process(rxn)


def test_raises_when_all_reactants_are_spectators(remover: OrphanRemover):
    """Raises NoMappedReactantsError when all mapped reactants are
    spectators after product filtering."""
    # Only the reactant is a spectator, product has additional fragment
    rxn = _make_reaction("[Na+:3]>>[CH3:1][O-:2].[Na+:3]")
    with pytest.raises(NoMappedReactantsError):
        remover.process(rxn)


# ============================================================================
# Edge cases
# ============================================================================


def test_split_with_triple_arrow(remover: OrphanRemover):
    """>>> in SMILES is split as >>+remainder, no unpacking crash."""
    rxn = _make_reaction("[CH3:1][OH:2]>>>[CH3:1][O-:2]")
    # maxsplit=1 prevents ValueError; product becomes ">[CH3:1][O-:2]"
    # which still has atom mapping, so no error — but SMILES is malformed.
    # OrphanRemover's job is not to validate SMILES syntax.
    result = remover.process(rxn)
    assert ">>" in result.processed_reaction_smiles


def test_complex_reaction_with_orphans(remover: OrphanRemover):
    """Real-world-like reaction with mapped reactants, orphans, and product."""
    rxn = _make_reaction(
        "[NH2:3][CH2:4][CH:5]1[CH2:6][O:7][CH2:8]1."
        "O[C:2](=[O:1])[c:9]1[cH:10][cH:11][cH:12][cH:13][cH:14]1."
        "CCO>>"
        "[O:1]=[C:2]([NH:3][CH2:4][CH:5]1[CH2:6][O:7][CH2:8]1)"
        "[c:9]1[cH:10][cH:11][cH:12][cH:13][cH:14]1.O"
    )
    result = remover.process(rxn)
    # Orphan "CCO" removed from reactants, "O" removed from products
    assert "CCO" not in result.processed_reaction_smiles.split(">>")[0]
    assert result.processed_reaction_smiles.split(">>")[1].count(".") == 0


def test_empty_product_side(remover: OrphanRemover):
    """Empty product side raises NoMappedProductError."""
    rxn = _make_reaction("[CH3:1][OH:2]>>")
    with pytest.raises(NoMappedProductError):
        remover.process(rxn)


def test_empty_reactant_side(remover: OrphanRemover):
    """Empty reactant side raises NoMappedReactantsError."""
    rxn = _make_reaction(">>[CH3:1][O-:2]")
    with pytest.raises(NoMappedReactantsError):
        remover.process(rxn)


def test_process_batch(remover: OrphanRemover, batch):
    """process_batch() passes sentinels through and processes valid reactions."""
    results = remover.process_batch(batch)
    assert len(results) == len(batch)
    assert not results[0].dummy
    assert not results[1].dummy
    assert results[2].dummy
    assert results[2] is SENTINEL
