from dataclasses import replace

import pytest

from chemcensor.basic import Reaction
from chemcensor.basic.reaction_center import ReactionCenterType
from chemcensor.basic.reaction_transform import ReactionTransform
from chemcensor.configs.reaction_center_extraction_configs import ExtractionConfig
from chemcensor.configs.reaction_center_extraction_configs import LINEAR_CONFIGS
from chemcensor.configs.reaction_center_extraction_configs import RING_CONFIGS
from chemcensor.extraction.errors.extractor_errors import MissingReactingAtomsError
from chemcensor.extraction.errors.extractor_errors import MissingReactionTransformError
from chemcensor.extraction.extractor import Extractor


# ============================================================================
# Reaction SMILES fixtures
# ============================================================================


# Ring reaction: Li metalation on a pyridine ring (from sear_annotator tests)
RING_REACTION_SMILES = (
    "C.[F:8][C:5]([F:6])([F:7])[c:4]1[cH:3][cH:2][c:11]([Cl:12])"
    "[cH:10][n:9]1.[Li+:1]>>[Li:1][c:2]1[cH:3][c:4]([C:5]([F:6])"
    "([F:7])[F:8])[n:9][cH:10][c:11]1[Cl:12]"
)

# Linear reaction: acyl chloride + amine → amide (no ring atoms in RC)
LINEAR_REACTION_SMILES = (
    "[CH3:1][C:2](=[O:3])[Cl:4].[NH2:5][CH3:6]" ">>" "[CH3:1][C:2](=[O:3])[NH:5][CH3:6]"
)


@pytest.fixture
def ring_reaction() -> Reaction:
    T = ReactionTransform.from_reaction_smiles(RING_REACTION_SMILES)
    return Reaction(reaction_smiles=RING_REACTION_SMILES, reaction_transform=T)


@pytest.fixture
def linear_reaction() -> Reaction:
    T = ReactionTransform.from_reaction_smiles(LINEAR_REACTION_SMILES)
    return Reaction(reaction_smiles=LINEAR_REACTION_SMILES, reaction_transform=T)


@pytest.fixture
def reaction_no_transform() -> Reaction:
    return Reaction(reaction_smiles="A>>B", reaction_transform=None)


@pytest.fixture
def reaction_no_reacting_atoms() -> Reaction:
    T = ReactionTransform.from_reaction_smiles(LINEAR_REACTION_SMILES)
    T_no_atoms = replace(T, p_reacting_atoms=None, R_reacting_atoms=None)
    return Reaction(
        reaction_smiles=LINEAR_REACTION_SMILES, reaction_transform=T_no_atoms
    )


# ============================================================================
# Initialization
# ============================================================================


class TestExtractorInit:
    def test_valid_max_center_type(self) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC2)
        assert ext.max_center_type == ReactionCenterType.RC2

    def test_default_max_center_type(self) -> None:
        ext = Extractor()
        assert ext.max_center_type == ReactionCenterType.RC4


# ============================================================================
# Error cases
# ============================================================================


class TestExtractorErrors:
    def test_no_transform_raises(self, reaction_no_transform: Reaction) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC1)
        with pytest.raises(MissingReactionTransformError):
            ext.extract_rc(reaction_no_transform)

    def test_no_reacting_atoms_raises(
        self, reaction_no_reacting_atoms: Reaction
    ) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC1)
        with pytest.raises(MissingReactingAtomsError):
            ext.extract_rc(reaction_no_reacting_atoms)


# ============================================================================
# extract_rc — basic contract
# ============================================================================


class TestExtractRC:
    def test_returns_reaction_with_centers(self, ring_reaction: Reaction) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC1)
        result = ext.extract_rc(ring_reaction)
        assert isinstance(result, Reaction)
        assert len(result.reaction_centers) >= 1

    def test_preserves_reaction_smiles(self, ring_reaction: Reaction) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC1)
        result = ext.extract_rc(ring_reaction)
        assert result.reaction_smiles == ring_reaction.reaction_smiles

    def test_preserves_reaction_transform(self, ring_reaction: Reaction) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC1)
        result = ext.extract_rc(ring_reaction)
        assert result.reaction_transform == ring_reaction.reaction_transform

    def test_base_center_has_type_1(self, ring_reaction: Reaction) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC1)
        result = ext.extract_rc(ring_reaction)
        assert (
            result.get_reaction_center_by_type(ReactionCenterType.RC1).center_type
            == ReactionCenterType.RC1
        )

    def test_base_center_has_smiles(self, ring_reaction: Reaction) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC1)
        result = ext.extract_rc(ring_reaction)
        rc = result.get_reaction_center_by_type(ReactionCenterType.RC1)
        assert ">>" in rc.reaction_center_smiles
        assert len(rc.reaction_center_smiles) > 2

    def test_base_center_has_product_indices(self, ring_reaction: Reaction) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC1)
        result = ext.extract_rc(ring_reaction)
        rc = result.get_reaction_center_by_type(ReactionCenterType.RC1)
        assert isinstance(rc.product_indices, frozenset)
        assert len(rc.product_indices) > 0

    def test_base_center_has_reactant_indices(self, ring_reaction: Reaction) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC1)
        result = ext.extract_rc(ring_reaction)
        rc = result.get_reaction_center_by_type(ReactionCenterType.RC1)
        assert isinstance(rc.reactant_indices, tuple)
        assert len(rc.reactant_indices) > 0
        for r_indices in rc.reactant_indices:
            assert isinstance(r_indices, frozenset)


# ============================================================================
# extract_rc — max_center_type=1 (only base)
# ============================================================================


class TestExtractRCType1Only:
    def test_exactly_one_center(self, ring_reaction: Reaction) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC1)
        result = ext.extract_rc(ring_reaction)
        assert len(result.reaction_centers) == 1

    def test_exactly_one_center_linear(self, linear_reaction: Reaction) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC1)
        result = ext.extract_rc(linear_reaction)
        assert len(result.reaction_centers) == 1


# ============================================================================
# extract_rc — multiple center types
# ============================================================================


class TestExtractRCMultipleTypes:
    def test_max_type_4_at_least_one_center(self, ring_reaction: Reaction) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC4)
        result = ext.extract_rc(ring_reaction)
        assert len(result.reaction_centers) >= 1

    def test_max_type_4_linear_at_least_one_center(
        self, linear_reaction: Reaction
    ) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC4)
        result = ext.extract_rc(linear_reaction)
        assert len(result.reaction_centers) >= 1

    def test_no_duplicate_centers(self, ring_reaction: Reaction) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC4)
        result = ext.extract_rc(ring_reaction)
        smiles_list = [
            rc.reaction_center_smiles for rc in result.reaction_centers.values()
        ]
        assert len(smiles_list) == len(set(smiles_list))


# ============================================================================
# _has_ring_atoms_in_rc
# ============================================================================


class TestHasRingAtomsInRC:
    def test_ring_reaction_detected(self, ring_reaction: Reaction) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC1)
        T = ring_reaction.reaction_transform
        assert T is not None
        rc = ext._extract_single_rc(
            config=ExtractionConfig(center_type=ReactionCenterType.RC1), T=T
        )
        assert ext._has_ring_atoms_in_rc(T, rc) is True

    def test_linear_reaction_not_detected(self, linear_reaction: Reaction) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC1)
        T = linear_reaction.reaction_transform
        assert T is not None
        rc = ext._extract_single_rc(
            config=ExtractionConfig(center_type=ReactionCenterType.RC1), T=T
        )
        assert ext._has_ring_atoms_in_rc(T, rc) is False


# ============================================================================
# _select_additional_configs
# ============================================================================


class TestSelectAdditionalConfigs:
    def test_ring_configs_when_has_rings(self) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC4)
        configs = ext._select_additional_configs(has_ring_atoms=True)
        assert configs == RING_CONFIGS

    def test_linear_configs_when_no_rings(self) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC4)
        configs = ext._select_additional_configs(has_ring_atoms=False)
        assert configs == LINEAR_CONFIGS

    def test_respects_max_center_type(self) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC2)
        configs = ext._select_additional_configs(has_ring_atoms=True)
        assert all(c.center_type <= ReactionCenterType.RC2 for c in configs)
        assert len(configs) == 1  # only type 2

    def test_empty_when_max_is_1(self) -> None:
        ext = Extractor(max_center_type=ReactionCenterType.RC1)
        configs = ext._select_additional_configs(has_ring_atoms=True)
        assert len(configs) == 0
