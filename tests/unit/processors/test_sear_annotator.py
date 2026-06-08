from dataclasses import replace
from typing import TypedDict

import numpy as np
import pytest
from frozendict import frozendict

from chemcensor.basic import Molecule
from chemcensor.basic import Reaction
from chemcensor.basic import SENTINEL
from chemcensor.basic.functional_groups import FunctionalGroupClass
from chemcensor.basic.functional_groups import FunctionalGroups
from chemcensor.basic.reaction_transform import ReactionTransform
from chemcensor.processing.errors.sear_annotator_errors import (
    EmptyReactionTransformError,
)
from chemcensor.processing.errors.sear_annotator_errors import (
    NoReactantsReactingAtomsError,
)
from chemcensor.processing.sear_annotator import _get_mapped_reacting_ch_atoms
from chemcensor.processing.sear_annotator import SeArAnnotator
from chemcensor.rules.functional_groups import FG_COLLECTION_SEAR


def _sear_signature_from_global_indices(indices: frozenset[int]) -> np.ndarray:
    sig = np.zeros(FG_COLLECTION_SEAR.num_groups, dtype=np.uint8)
    idx_to_pos = {fg.idx: i for i, fg in enumerate(FG_COLLECTION_SEAR.known_groups)}
    for idx in indices:
        pos = idx_to_pos.get(idx)
        if pos is not None:
            sig[pos] = 1
    return sig


SEAR_TEST_FGS: tuple[frozendict[str, int | str | FunctionalGroupClass], ...] = (
    frozendict(
        {
            "idx": 159,
            "name": "Arenes [ch] (meta-EWG)",
            "ui_name": "Arenes [ch] (meta-EWG)",
            "smarts": "[ch]:1:[c]:[c$(*[N$(*=O),C$(*=[O,S,N]),S$(*=[O]),"
            "C$(*#N)]),c$(*[C]([F,Cl,B,I])([F,Cl,B,I])[F,Cl,B,I]),n]"
            ":[c]:[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict(
        {
            "idx": 161,
            "name": "Arenes [ch] (ortho-EDG) Type II",
            "ui_name": "Arenes [ch] (ortho-EDG) Type II",
            "smarts": "[cr6h]:[c$(*[F,Cl,Br,I])]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict(
        {
            "idx": 166,
            "name": "Arenes [ch] (ortho-EWG)",
            "ui_name": "Arenes [ch] (ortho-EWG)",
            "smarts": "[cr6h]:[c$(*[N$(*=O),S$(*=[O]),C$(*#N)]),"
            "c$(*[C]([F,Cl,B,I])([F,Cl,B,I])[F,Cl,B,I]),n]",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
    frozendict(
        {
            "idx": 173,
            "name": "Arenes [ch] (para-EWG)",
            "ui_name": "Arenes [ch] (para-EWG)",
            "smarts": "[ch]:1:[c]:[c]:[c$(*[N$(*=O),C$(*=[O,S,N]),S$(*=[O]),"
            "C$(*#N)]),c$(*[C]([F,Cl,B,I])([F,Cl,B,I])[F,Cl,B,I]),n]"
            ":[c]:[c]:1",
            "fg_class": FunctionalGroupClass.SEAR,
        }
    ),
)


class SeArCase(TypedDict):
    id: str
    reaction_smiles: str
    expected_is_sear_reaction: bool
    expected_group_indices: frozenset[int]


SEAR_CASES: list[SeArCase] = [
    {
        "id": "sear",
        "reaction_smiles": (
            "C.[F:8][C:5]([F:6])([F:7])[c:4]1[cH:3][cH:2][c:11]([Cl:12])"
            "[cH:10][n:9]1.[Li+:1]>>[Li:1][c:2]1[cH:3][c:4]([C:5]([F:6])"
            "([F:7])[F:8])[n:9][cH:10][c:11]1[Cl:12]"
        ),
        "expected_is_sear_reaction": True,
        "expected_group_indices": frozenset({161, 173}),
    },
    {
        "id": "non_sear",
        "reaction_smiles": (
            "[CH3:1][C:2]([CH3:3])([OH:4])[c:5]1[cH:6][c:7]([C:8]([F:9])"
            "([F:10])[F:11])[n:12][cH:13][c:14]1-[c:15]1[cH:16][cH:17]"
            "[c:18]([C:19]2([C:20]#N)[CH2:23][O:24][CH2:25]2)[cH:26]"
            "[cH:27]1.[OH-:21].[OH2:22]>>[CH3:1][C:2]([CH3:3])([OH:4])"
            "[c:5]1[cH:6][c:7]([C:8]([F:9])([F:10])[F:11])[n:12][cH:13]"
            "[c:14]1-[c:15]1[cH:16][cH:17][c:18]([C:19]2([C:20](=[O:21])"
            "[OH:22])[CH2:23][O:24][CH2:25]2)[cH:26][cH:27]1"
        ),
        "expected_is_sear_reaction": False,
        "expected_group_indices": frozenset(),
    },
    {
        "id": "non_sear_oxidation",
        "reaction_smiles": (
            "[CH3:1][N:2]([CH2:3][C:4]1([c:5]2[cH:6][cH:7][c:8]([CH:9]=[CH2:10])[cH:12]"
            "[cH:13]2)[CH2:14][CH2:15][CH2:16][CH2:17]1)[C:18](=[O:19])[O:20][C:21]"
            "([CH3:22])([CH3:23])[CH3:24].O=C(O[OH:11])c1cccc(Cl)c1>>[CH3:1][N:2]"
            "([CH2:3][C:4]1([c:5]2[cH:6][cH:7][c:8]([CH:9]3[CH2:10][O:11]3)[cH:12]"
            "[cH:13]2)[CH2:14][CH2:15][CH2:16][CH2:17]1)[C:18](=[O:19])[O:20][C:21]"
            "([CH3:22])([CH3:23])[CH3:24]"
        ),
        "expected_is_sear_reaction": False,
        "expected_group_indices": frozenset(),
    },
    {
        "id": "non_sear_urea_formation",
        "reaction_smiles": (
            "[CH3:1][O:2][CH2:3][CH2:4][c:5]1[cH:6][cH:7][c:8]([NH2:9])[cH:38]"
            "[n:39]1.[NH2:12][c:13]1[cH:14][cH:15][c:16]([C:17]([F:18])([F:19])"
            "[F:20])[cH:21][c:22]1-[c:23]1[cH:24][n:25][c:26]([N:27]2[CH2:28]"
            "[CH2:29][C:30]([CH3:31])([OH:32])[CH2:33][CH2:34]2)[n:35][c:36]1"
            "[CH3:37].c1cn([C:10](n2ccnc2)=[O:11])cn1>>[CH3:1][O:2][CH2:3][CH2:4]"
            "[c:5]1[cH:6][cH:7][c:8]([NH:9][C:10](=[O:11])[NH:12][c:13]2[cH:14]"
            "[cH:15][c:16]([C:17]([F:18])([F:19])[F:20])[cH:21][c:22]2-[c:23]2"
            "[cH:24][n:25][c:26]([N:27]3[CH2:28][CH2:29][C:30]([CH3:31])([OH:32])"
            "[CH2:33][CH2:34]3)[n:35][c:36]2[CH3:37])[cH:38][n:39]1"
        ),
        "expected_is_sear_reaction": False,
        "expected_group_indices": frozenset(),
    },
]


@pytest.fixture
def annotator() -> SeArAnnotator:
    return SeArAnnotator(FunctionalGroups.from_tuple(SEAR_TEST_FGS))


@pytest.fixture
def annotator_integration() -> SeArAnnotator:
    return SeArAnnotator(FG_COLLECTION_SEAR)


def _make_reaction(reaction_smiles: str) -> Reaction:
    """Create a Reaction with a ready ReactionTransform."""
    transform = ReactionTransform.from_reaction_smiles(reaction_smiles)
    return Reaction(
        reaction_smiles=reaction_smiles,
        reaction_transform=transform,
    )


@pytest.fixture
def batch() -> list[Reaction]:
    return [
        _make_reaction(SEAR_CASES[0]["reaction_smiles"]),
        _make_reaction(SEAR_CASES[1]["reaction_smiles"]),
        SENTINEL,
    ]


# ============================================================================
# SEAr detection
# ============================================================================


@pytest.mark.parametrize(
    "case",
    SEAR_CASES,
    ids=[case["id"] for case in SEAR_CASES],
)
def test_process_sets_expected_sear_annotation(
    annotator: SeArAnnotator,
    case: SeArCase,
) -> None:
    """Each case gets the expected SeAr classification."""
    reaction = _make_reaction(case["reaction_smiles"])
    result = annotator.process(reaction)
    assert result.is_sear_reaction is case["expected_is_sear_reaction"]
    expected_sig = _sear_signature_from_global_indices(case["expected_group_indices"])
    assert np.array_equal(result.sear_signature, expected_sig)


# ============================================================================
# Field preservation
# ============================================================================


@pytest.mark.parametrize(
    "case",
    SEAR_CASES,
    ids=[case["id"] for case in SEAR_CASES],
)
def test_preserves_reaction_smiles(
    annotator: SeArAnnotator,
    case: SeArCase,
) -> None:
    """process() preserves the original reaction_smiles."""
    reaction = _make_reaction(case["reaction_smiles"])
    result = annotator.process(reaction)
    assert result.reaction_smiles == reaction.reaction_smiles


@pytest.mark.parametrize(
    "case",
    SEAR_CASES,
    ids=[case["id"] for case in SEAR_CASES],
)
def test_preserves_reaction_transform(
    annotator: SeArAnnotator,
    case: SeArCase,
) -> None:
    """process() preserves the reaction_transform."""
    reaction = _make_reaction(case["reaction_smiles"])
    result = annotator.process(reaction)
    assert result.reaction_transform == reaction.reaction_transform


# ============================================================================
# Error cases
# ============================================================================


def test_raises_on_empty_transform(annotator: SeArAnnotator) -> None:
    """Raises EmptyReactionTransformError when reaction_transform is None."""
    reaction = Reaction(reaction_smiles="A>>B", reaction_transform=None)
    with pytest.raises(EmptyReactionTransformError):
        annotator.process(reaction)


def test_raises_on_no_reacting_atoms(annotator: SeArAnnotator) -> None:
    """Raises NoReactantsReactingAtomsError when R_reacting_atoms is None."""
    transform = ReactionTransform.from_reaction_smiles(SEAR_CASES[0]["reaction_smiles"])
    transform_no_atoms = replace(transform, R_reacting_atoms=None)
    reaction = Reaction(
        reaction_smiles=SEAR_CASES[0]["reaction_smiles"],
        reaction_transform=transform_no_atoms,
    )
    with pytest.raises(NoReactantsReactingAtomsError):
        annotator.process(reaction)


# ============================================================================
# _get_mapped_reacting_ch_atoms
# ============================================================================


@pytest.fixture
def molecule() -> Molecule:
    return Molecule.from_atom_mapped_smiles(
        "[F:8][C:5]([F:6])([F:7])[c:4]1[cH:3][cH:2][c:11]([Cl:12])[cH:10][n:9]1"
    )


def test_get_mapped_reacting_ch_atoms_returns_expected_indices(
    molecule: Molecule,
) -> None:
    reacting_atoms_1 = (5,)
    reacting_atoms_2 = (6,)
    reacting_atoms_3 = (9,)
    reacting_atoms_4 = (5, 6, 9)
    reacting_atoms_5 = (1, 2)
    reacting_atoms_6 = (4, 7)
    assert _get_mapped_reacting_ch_atoms(molecule, reacting_atoms_1) == frozenset({5})
    assert _get_mapped_reacting_ch_atoms(molecule, reacting_atoms_2) == frozenset({6})
    assert _get_mapped_reacting_ch_atoms(molecule, reacting_atoms_3) == frozenset({9})
    assert _get_mapped_reacting_ch_atoms(molecule, reacting_atoms_4) == frozenset(
        {5, 6, 9}
    )
    assert _get_mapped_reacting_ch_atoms(molecule, reacting_atoms_5) == frozenset()
    assert _get_mapped_reacting_ch_atoms(molecule, reacting_atoms_6) == frozenset()


def test_get_mapped_reacting_ch_atoms_ignores_unmapped_aromatic_ch() -> None:
    molecule = Molecule.from_atom_mapped_smiles("c1cccc([OH:1])c1")
    assert _get_mapped_reacting_ch_atoms(molecule, (0, 1, 2, 3, 5, 6)) == frozenset()


# ============================================================================
# integration sear tests
# ============================================================================

SEAR_CASES_INTEGRATION: list[SeArCase] = [
    {
        "id": "sear_integration",
        "reaction_smiles": (
            "Br[Br:9].[CH3:1][CH:2]1[CH2:3][N:4]([c:5]2[cH:6][cH:7][cH:8][c:10]3[cH:11]"
            "[n:12][cH:13][n:14]23)[CH2:15][CH:16]1[NH:17][C:18](=[O:19])[O:20][C:21]"
            "([CH3:22])([CH3:23])[CH3:24]>>[CH3:1][CH:2]1[CH2:3][N:4]([c:5]2[cH:6][cH:"
            "7][c:8]([Br:9])[c:10]3[cH:11][n:12][cH:13][n:14]23)[CH2:15][CH:16]1[NH:17]"
            "[C:18](=[O:19])[O:20][C:21]([CH3:22])([CH3:23])[CH3:24]"
        ),
        "expected_is_sear_reaction": True,
        "expected_group_indices": frozenset({159, 163, 515}),
    },
]


@pytest.mark.parametrize(
    "case",
    SEAR_CASES_INTEGRATION,
    ids=[case["id"] for case in SEAR_CASES_INTEGRATION],
)
def test_integration_sear_tests(
    annotator_integration: SeArAnnotator,
    case: SeArCase,
) -> None:
    """Each case gets the expected SeAr classification."""
    reaction = _make_reaction(case["reaction_smiles"])
    result = annotator_integration.process(reaction)
    assert result.is_sear_reaction is case["expected_is_sear_reaction"]
    expected_sig = _sear_signature_from_global_indices(case["expected_group_indices"])
    assert np.array_equal(result.sear_signature, expected_sig)


# ============================================================================
# process_batch
# ============================================================================


def test_process_batch(annotator: SeArAnnotator, batch):
    """process_batch() passes sentinels through and processes valid reactions."""
    results = annotator.process_batch(batch)
    assert len(results) == len(batch)
    assert not results[0].dummy
    assert not results[1].dummy
    assert results[2].dummy
    assert results[2] is SENTINEL
