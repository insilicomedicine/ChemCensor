import numpy as np
import pytest
from frozendict import frozendict
from rdkit import Chem

from chemcensor.basic.errors.fg_finder_errors import FGFinderNoReactionCentersError
from chemcensor.basic.errors.fg_finder_errors import FGFinderNoTransformError
from chemcensor.basic.functional_groups import FunctionalGroupClass
from chemcensor.basic.functional_groups import FunctionalGroups
from chemcensor.basic.reaction import Reaction
from chemcensor.basic.reaction_center import ReactionCenter
from chemcensor.basic.reaction_center import ReactionCenterType
from chemcensor.basic.reaction_center_fragment import ReactionCenterFragment
from chemcensor.basic.reaction_transform import ReactionTransform
from chemcensor.extraction.fg_finder import FGFinder


# ============================================================================
# Helpers
# ============================================================================


def _empty_fragment() -> ReactionCenterFragment:
    """Create a dummy empty ReactionCenterFragment for testing."""
    return ReactionCenterFragment(fr_mol=Chem.RWMol())


def _build_reaction(
    rxn_smiles: str,
    center_type: ReactionCenterType = ReactionCenterType.RC1,
    is_sear_reaction: bool = False,
) -> Reaction:
    """Build a Reaction with a ReactionTransform and one ReactionCenter
    whose skip-indices are derived from the transform's reacting atoms."""
    transform = ReactionTransform.from_reaction_smiles(rxn_smiles)
    n_reactants = len(transform.reactants)
    rc = ReactionCenter(
        center_type=center_type,
        product_fragment=_empty_fragment(),
        reactant_fragments=tuple(_empty_fragment() for _ in range(n_reactants)),
        product_indices=frozenset(transform.p_reacting_atoms or ()),
        reactant_indices=tuple(
            frozenset(ra) for ra in (transform.R_reacting_atoms or ())
        ),
        fg_signature=np.zeros(len(FUNCTIONAL_GROUPS_TEST), dtype=np.uint8),
    )
    return Reaction(
        reaction_smiles=rxn_smiles,
        reaction_transform=transform,
        reaction_centers=frozendict({rc.center_type: rc}),
        is_sear_reaction=is_sear_reaction,
    )


# ============================================================================
# Fixtures — functional-group collections
# ============================================================================

KETONE_FG: frozendict[str, int | str | FunctionalGroupClass] = frozendict(
    {
        "idx": 0,
        "name": "a-[Ch] ketone",
        "ui_name": "a-[Ch] ketone",
        "smarts": "[CX4&h][C](=[O])[#6]",
        "fg_class": FunctionalGroupClass.GENERAL,
    }
)
PHENOL_FG: frozendict[str, int | str | FunctionalGroupClass] = frozendict(
    {
        "idx": 1,
        "name": "phenol c-[Oh]",
        "ui_name": "phenol c-[Oh]",
        "smarts": "[c;!$(*n)&!$(*:1:a:a:n:a:a:1)][Oh]",
        "fg_class": FunctionalGroupClass.GENERAL,
    }
)
SEAR1_FG: frozendict[str, int | str | FunctionalGroupClass] = frozendict(
    {
        "idx": 2,
        "name": "Arenes [ch] (ortho-EWG) Type II",
        "ui_name": "Arenes [ch] (ortho-EWG) Type II",
        "smarts": "[cr6h]:[c$(*[C]=[O,S,N])]",
        "fg_class": FunctionalGroupClass.SEAR,
    }
)
SEAR2_FG: frozendict[str, int | str | FunctionalGroupClass] = frozendict(
    {
        "idx": 3,
        "name": "Arenes [ch] (ortho-EDG) Type VI",
        "ui_name": "Arenes [ch] (ortho-EDG) Type VI",
        "smarts": "[cr6h]:[c$(*[NX3!$(*=O),SX2])]",
        "fg_class": FunctionalGroupClass.SEAR,
    }
)
METHYL_ESTER_FG: frozendict[str, int | str | FunctionalGroupClass] = frozendict(
    {
        "idx": 4,
        "name": "Carboxylic ester (methyl) COOCH3",
        "ui_name": "Carboxylic ester (methyl) COOCH3",
        "smarts": "[C;X3&z2](=[O])[O][CH3]",
        "fg_class": FunctionalGroupClass.GENERAL,
    }
)
PYRIDINE_FG: frozendict[str, int | str | FunctionalGroupClass] = frozendict(
    {
        "idx": 5,
        "name": "Pyridine",
        "ui_name": "Pyridine",
        "smarts": "[c,n]:1:[n,c]:[c,n]:[n]:[c,n]:[c,n]:1",
        "fg_class": FunctionalGroupClass.SKIP,
    }
)
SEAR3_FG: frozendict[str, int | str | FunctionalGroupClass] = frozendict(
    {
        "idx": 6,
        "name": "Arenes [ch] (ortho-EDG) Type III",
        "ui_name": "Arenes [ch] (ortho-EDG) Type III",
        "smarts": "[cr6h]:[c;$(*[O;+0H1,-1H0])]",
        "fg_class": FunctionalGroupClass.SEAR,
    }
)

FUNCTIONAL_GROUPS_TEST = (
    KETONE_FG,
    PHENOL_FG,
    SEAR1_FG,
    SEAR2_FG,
    METHYL_ESTER_FG,
    PYRIDINE_FG,
    SEAR3_FG,
)


@pytest.fixture
def fg_collection_general() -> FunctionalGroups:
    """FunctionalGroups with general functional groups."""
    return FunctionalGroups.from_tuple(
        (
            tuple(
                fg
                for fg in FUNCTIONAL_GROUPS_TEST
                if fg["fg_class"] == FunctionalGroupClass.GENERAL
            )
        )
    )


@pytest.fixture
def fg_collection_sear() -> FunctionalGroups:
    """FunctionalGroups with SEAR functional groups."""
    return FunctionalGroups.from_tuple(
        (
            tuple(
                fg
                for fg in FUNCTIONAL_GROUPS_TEST
                if fg["fg_class"] == FunctionalGroupClass.SEAR
            )
        )
    )


@pytest.fixture
def fg_collection_skip() -> FunctionalGroups:
    """FunctionalGroups with skip functional groups."""
    return FunctionalGroups.from_tuple(
        (
            tuple(
                fg
                for fg in FUNCTIONAL_GROUPS_TEST
                if fg["fg_class"] == FunctionalGroupClass.SKIP
            )
        )
    )


@pytest.fixture
def fg_finder_general(fg_collection_general) -> FGFinder:
    """FGFinder with hydroxyl + primary amine collection."""
    return FGFinder(fg_collection_general)


@pytest.fixture
def fg_finder_sear(fg_collection_sear) -> FGFinder:
    """FGFinder with SEAR collection."""
    return FGFinder(fg_collection_sear)


# ============================================================================
# Fixtures — reactions
# ============================================================================


@pytest.fixture
def suzuki_rxn_smiles() -> str:
    """Suzuki coupling of benzyl chloride and pyridine."""
    return (
        "OB(O)[c:5]1[cH:6][cH:7][c:8]([OH:9])[cH:10][cH:11]1."
        "[CH3:1][n:2]1[cH:3][c:4](I)[cH:12][n:13]1"
        ">>[CH3:1][n:2]1[cH:3][c:4](-[c:5]2[cH:6][cH:7][c:8]([OH:9])[cH:10]"
        "[cH:11]2)[cH:12][n:13]1"
    )


@pytest.fixture
def suzuki_reaction(suzuki_rxn_smiles) -> Reaction:
    """Fully built Reaction for the Suzuki coupling."""
    return _build_reaction(suzuki_rxn_smiles)


@pytest.fixture
def suzuki_signature() -> np.ndarray:
    """Signature for the Suzuki coupling."""
    return np.array([0, 1, 0, 0, 0, 0, 0])


@pytest.fixture
def bromination_smiles() -> str:
    """Bromination SEAR."""
    return (
        "[CH3:1][O:2][C:3](=[O:4])[c:5]1[cH:6][cH:7][c:8]([O:9][CH3:10])"
        "[cH:11][cH:13]1.Br[Br:12]>>[CH3:1][O:2][C:3](=[O:4])"
        "[c:5]1[cH:6][cH:7][c:8]([O:9][CH3:10])[c:11]([Br:12])[cH:13]1"
    )


@pytest.fixture
def sear_reaction(bromination_smiles) -> Reaction:
    """Reaction for bromination SEAR."""
    return _build_reaction(bromination_smiles, is_sear_reaction=True)


@pytest.fixture
def bromination_signature_sear_collection() -> np.ndarray:
    """Signature for the bromination SEAR."""
    return np.array([0, 0, 1, 0, 0, 0, 0])


@pytest.fixture
def bromination_signature_general_collection() -> np.ndarray:
    """Signature for the bromination SEAR."""
    return np.array([0, 0, 0, 0, 1, 0, 0])


@pytest.fixture
def boc_deprotection_smiles() -> str:
    """Boc deprotection"""
    return (
        "CC(C)(C)OC(=O)[N:5]1[CH2:4][CH2:3][C:2](=[O:1])[c:11]2[cH:10]"
        "[cH:9][n:8][cH:7][c:6]21>>[O:1]=[C:2]1[CH2:3][CH2:4][NH:5]"
        "[c:6]2[cH:7][n:8][cH:9][cH:10][c:11]21"
    )


@pytest.fixture
def boc_deprotection_reaction(boc_deprotection_smiles) -> Reaction:
    """Reaction for Boc deprotection."""
    return _build_reaction(boc_deprotection_smiles)


@pytest.fixture
def boc_deprotection_signature() -> np.ndarray:
    """Signature for the Boc deprotection."""
    return np.array([1, 0, 0, 0, 0, 0, 0])


@pytest.fixture
def reaction_without_transform() -> Reaction:
    """Reaction that has no ReactionTransform."""
    return Reaction(
        reaction_smiles=(
            "[CH3:1][CH2:2][CH:3]([CH3:4])[OH:5]"
            ">>[CH3:1][CH2:2][C@@H:3]([CH3:4])[OH:5]"
        )
    )


# ============================================================================
# FGFinder.find — error handling
# ============================================================================


def test_raises_without_reaction_transform(
    fg_finder_general, reaction_without_transform
):
    """find() raises FGFinderNoTransformError when no transform."""

    with pytest.raises(FGFinderNoTransformError):
        fg_finder_general.find(reaction_without_transform)


# ============================================================================
# FGFinder.find — signature shape and FG classes
# ============================================================================


def test_signature_length_matches_default_signature_size(
    fg_finder_general, suzuki_reaction
):
    """Signature length equals the number of known functional groups."""
    result = fg_finder_general.find(suzuki_reaction)
    sig = result.get_reaction_center_by_type(ReactionCenterType.RC1).fg_signature
    assert sig.shape == (len(FUNCTIONAL_GROUPS_TEST),)


def test_sear_groups(fg_collection_sear):
    sear_groups_indices = [
        fg.idx
        for fg in fg_collection_sear.known_groups
        if fg.fg_class == FunctionalGroupClass.SEAR
    ]
    assert sear_groups_indices == [2, 3, 6]


def test_skip_groups(fg_collection_skip):
    skip_groups = [
        fg.idx
        for fg in fg_collection_skip.known_groups
        if fg.fg_class == FunctionalGroupClass.SKIP
    ]
    assert skip_groups == [5]


# ============================================================================
# FGFinder.find — test signatures
# ============================================================================


def test_phenol_is_detected(fg_finder_general, suzuki_reaction, fg_collection_sear):
    """Phenol should be detected, but SEAR3 should not.
    SEAr is skipped but can be found by simple matching.
    """
    result = fg_finder_general.find(suzuki_reaction)
    sig = result.get_reaction_center_by_type(ReactionCenterType.RC1).fg_signature
    assert sig[1] == 1
    assert sig[6] == 0

    matches = fg_collection_sear.identify_functional_groups(
        suzuki_reaction.reaction_transform.reactants[0]
    )
    # The first match is SEAR3.
    assert matches[0].functional_group.idx == 6


def test_empty_reaction_centers(fg_finder_general, suzuki_reaction, suzuki_rxn_smiles):
    """find() with no reaction centers returns the reaction unchanged."""
    transform = ReactionTransform.from_reaction_smiles(suzuki_rxn_smiles)
    reaction = Reaction(
        reaction_smiles=suzuki_rxn_smiles,
        reaction_transform=transform,
        reaction_centers=frozendict(),
    )
    with pytest.raises(FGFinderNoReactionCentersError):
        fg_finder_general.find(reaction)


def test_suzuki_signature(fg_finder_general, suzuki_reaction, suzuki_signature):
    """Suzuki signature should match the expected signature."""
    result = fg_finder_general.find(suzuki_reaction)
    sig = result.get_reaction_center_by_type(ReactionCenterType.RC1).fg_signature
    assert all(sig == suzuki_signature)


def test_bromination_signature_sear(
    fg_finder_sear, sear_reaction, bromination_signature_sear_collection
):
    """Bromination signature should match the expected signature."""
    result = fg_finder_sear.find(sear_reaction)
    sig = result.get_reaction_center_by_type(ReactionCenterType.RC1).fg_signature
    assert all(sig == bromination_signature_sear_collection)


def test_bromination_signature(
    fg_finder_general, sear_reaction, bromination_signature_general_collection
):
    """Bromination signature should match the expected signature."""
    result = fg_finder_general.find(sear_reaction)
    sig = result.get_reaction_center_by_type(ReactionCenterType.RC1).fg_signature
    assert all(sig == bromination_signature_general_collection)


def test_boc_deprotection_signature(
    fg_finder_general,
    boc_deprotection_reaction,
    boc_deprotection_signature,
    fg_collection_skip,
):
    """Boc deprotection signature should match the expected signature."""
    result = fg_finder_general.find(boc_deprotection_reaction)
    sig = result.get_reaction_center_by_type(ReactionCenterType.RC1).fg_signature
    assert all(sig == boc_deprotection_signature)

    matches = fg_collection_skip.identify_functional_groups(
        boc_deprotection_reaction.reaction_transform.reactants[0]
    )
    # skipped pyridine can be found by simple matching
    assert matches[-1].functional_group.idx == 5
