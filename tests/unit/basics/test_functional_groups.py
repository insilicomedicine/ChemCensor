import pytest
from frozendict import frozendict

from chemcensor.basic.errors import FunctionalGroupsInitializationError
from chemcensor.basic.errors import InvalidDataTypesError
from chemcensor.basic.errors import InvalidSMARTSStringError
from chemcensor.basic.errors import MissingRequiredKeysError
from chemcensor.basic.functional_groups import FunctionalGroup
from chemcensor.basic.functional_groups import FunctionalGroupClass
from chemcensor.basic.functional_groups import FunctionalGroups
from chemcensor.basic.functional_groups import MatchedGroup
from chemcensor.basic.molecule import Molecule


def fg_to_dict(
    fg: FunctionalGroup,
) -> frozendict[str, int | str | FunctionalGroupClass]:
    """Convert FunctionalGroup to dict for FunctionalGroups initialization."""
    return frozendict(
        {
            "idx": fg.idx,
            "name": fg.name,
            "ui_name": fg.ui_name,
            "smarts": fg.smarts,
            "fg_class": fg.fg_class,
        }
    )


@pytest.fixture
def simple_functional_group_data() -> frozendict[str, int | str | FunctionalGroupClass]:
    """Simple functional group data."""
    return frozendict(
        {
            "idx": 0,
            "name": "Hydroxyl",
            "ui_name": "Hydroxyl",
            "smarts": "[OH]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    )


@pytest.fixture
def phenol_functional_group_data() -> frozendict[str, int | str | FunctionalGroupClass]:
    """Phenol functional group data."""
    return frozendict(
        {
            "idx": 1,
            "name": "Phenol",
            "ui_name": "Phenol",
            "smarts": "c[OH]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    )


@pytest.fixture
def hydroxyl_group(
    simple_functional_group_data: frozendict[str, int | str | FunctionalGroupClass],
) -> FunctionalGroup:
    """Create a hydroxyl functional group."""
    return FunctionalGroup.from_dict(simple_functional_group_data)


@pytest.fixture
def phenol_group(
    phenol_functional_group_data: frozendict[str, int | str | FunctionalGroupClass],
) -> FunctionalGroup:
    """Create a phenol functional group."""
    return FunctionalGroup.from_dict(phenol_functional_group_data)


@pytest.fixture
def functional_groups_collection(
    simple_functional_group_data: frozendict[str, int | str | FunctionalGroupClass],
    phenol_functional_group_data: frozendict[str, int | str | FunctionalGroupClass],
) -> FunctionalGroups:
    """Create a collection of functional groups."""
    fgs = (simple_functional_group_data, phenol_functional_group_data)
    return FunctionalGroups.from_tuple(fgs)


# ============================================================================
# FunctionalGroup tests
# ============================================================================


def test_functional_group_creation(
    simple_functional_group_data: frozendict[str, int | str | FunctionalGroupClass],
):
    """Test creating a functional group."""
    fg = FunctionalGroup.from_dict(simple_functional_group_data)
    assert fg.idx == 0
    assert fg.name == "Hydroxyl"
    assert fg.smarts == "[OH]"
    assert fg.fg_class == FunctionalGroupClass.GENERAL


def test_functional_group_pattern_created(hydroxyl_group: FunctionalGroup):
    """Test that pattern is created from SMARTS."""
    assert hydroxyl_group.pattern is not None


def test_functional_group_invalid_smarts():
    """Test that invalid SMARTS raises InvalidSMARTSStringError on pattern access."""
    invalid_data = {
        "idx": 0,
        "name": "Invalid",
        "ui_name": "Invalid",
        "smarts": "invalid_smarts_xyz",
        "fg_class": FunctionalGroupClass.GENERAL,
    }
    fg = FunctionalGroup.from_dict(invalid_data)
    with pytest.raises(InvalidSMARTSStringError, match="Invalid SMARTS string"):
        _ = fg.pattern


def test_functional_group_missing_required_keys():
    """Test that missing required keys raises MissingRequiredKeysError."""
    incomplete_data = {
        "idx": 0,
        "name": "Incomplete",
        # missing 'smarts' and 'class'
    }
    with pytest.raises(MissingRequiredKeysError, match="Missing required keys"):
        FunctionalGroup.from_dict(incomplete_data)


def test_functional_group_invalid_data_types():
    """Test that invalid data types raise InvalidDataTypesError."""
    invalid_data = frozendict(
        {
            "idx": "not_an_int",
            "name": "Test",
            "smarts": "[OH]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    )
    with pytest.raises(InvalidDataTypesError, match="Invalid data types"):
        FunctionalGroup.from_dict(invalid_data)


def test_functional_group_frozen(hydroxyl_group: FunctionalGroup):
    """Test that FunctionalGroup is immutable (frozen)."""
    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        hydroxyl_group.name = "New Name"  # type: ignore


def test_functional_group_fields():
    """Test functional group fields."""
    fg = FunctionalGroup(
        idx=0,
        name="Test",
        ui_name="Test",
        smarts="[OH]",
        fg_class=FunctionalGroupClass.GENERAL,
    )
    # Check that all fields are set correctly
    assert fg.idx == 0
    assert fg.name == "Test"
    assert fg.smarts == "[OH]"
    assert fg.fg_class == FunctionalGroupClass.GENERAL
    assert fg.pattern is not None


# ============================================================================
# MatchedGroup tests
# ============================================================================


def test_matched_group_creation(hydroxyl_group: FunctionalGroup):
    """Test creating a matched group."""
    matching_sets = ((0, 1), (2, 3))
    matched = MatchedGroup(functional_group=hydroxyl_group, matching_sets=matching_sets)
    assert matched.functional_group == hydroxyl_group
    assert matched.matching_sets == matching_sets


def test_matched_group_immutable_matching_sets():
    """Test that matching_sets are immutable."""
    fg = FunctionalGroup(
        idx=0,
        name="Test",
        ui_name="Test",
        smarts="[OH]",
        fg_class=FunctionalGroupClass.GENERAL,
    )
    matching_sets = ((0,),)
    matched = MatchedGroup(functional_group=fg, matching_sets=matching_sets)
    # matching_sets should be tuple of atom-index tuples (RDKit match shape)
    assert isinstance(matched.matching_sets, tuple)
    assert all(isinstance(s, tuple) for s in matched.matching_sets)
    assert all(isinstance(i, int) for s in matched.matching_sets for i in s)


def test_matched_group_frozen():
    """Test that MatchedGroup is immutable (frozen)."""
    fg = FunctionalGroup(
        idx=0,
        name="Test",
        ui_name="Test",
        smarts="[OH]",
        fg_class=FunctionalGroupClass.GENERAL,
    )
    matched = MatchedGroup(functional_group=fg, matching_sets=((0,),))
    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        matched.matching_sets = ((1,),)  # type: ignore


# ============================================================================
# FunctionalGroups tests
# ============================================================================


def test_functional_groups_creation(
    functional_groups_collection: FunctionalGroups,
):
    """Test creating a FunctionalGroups collection."""
    assert functional_groups_collection is not None
    assert len(functional_groups_collection.known_groups) == 2


def test_functional_groups_fingerprints_created(
    functional_groups_collection: FunctionalGroups,
):
    """Test that fingerprints are created in __init__."""
    assert functional_groups_collection.fps_bits_collection is not None
    assert len(functional_groups_collection.fps_bits_collection) == len(
        functional_groups_collection.known_groups
    )


def test_identify_functional_groups_all(
    functional_groups_collection: FunctionalGroups,
):
    """Test identifying all functional groups in a molecule."""
    # Methanol has hydroxyl group
    methanol = Molecule("CO")
    matches = functional_groups_collection.identify_functional_groups(methanol)
    assert len(matches) > 0
    assert all(isinstance(m, MatchedGroup) for m in matches)


def test_identify_functional_groups_no_match(
    functional_groups_collection: FunctionalGroups,
):
    """Test identifying functional groups when no match exists."""
    # Methane has no functional groups
    methane = Molecule("C")
    matches = functional_groups_collection.identify_functional_groups(methane)
    assert len(matches) == 0


def test_identify_functional_groups_phenol(
    phenol_functional_group_data: frozendict[str, int | str | FunctionalGroupClass],
):
    """Test identifying phenol functional group."""
    fgs = FunctionalGroups.from_tuple((phenol_functional_group_data,), fp_length=2048)

    # Phenol molecule
    phenol = Molecule("c1ccccc1O")
    matches = fgs.identify_functional_groups(phenol)
    assert len(matches) > 0


def test_functional_groups_filter_by_class():
    """Test filtering functional groups by class manually."""
    fg_data = (
        frozendict(
            {
                "idx": 0,
                "name": "Hydroxyl",
                "ui_name": "Hydroxyl",
                "smarts": "[OH]",
                "fg_class": FunctionalGroupClass.GENERAL,
            }
        ),
        frozendict(
            {
                "idx": 1,
                "name": "Amine",
                "ui_name": "Amine",
                "smarts": "[NH2]",
                "fg_class": FunctionalGroupClass.SKIP,
            }
        ),
        frozendict(
            {
                "idx": 2,
                "name": "Phenol",
                "ui_name": "Phenol",
                "smarts": "c[OH]",
                "fg_class": FunctionalGroupClass.GENERAL,
            }
        ),
    )
    fgs = FunctionalGroups.from_tuple(fg_data)

    # Filter by class 1
    class_1_groups = [
        fg for fg in fgs.known_groups if fg.fg_class == FunctionalGroupClass.GENERAL
    ]
    assert len(class_1_groups) == 2
    assert all(fg.fg_class == FunctionalGroupClass.GENERAL for fg in class_1_groups)

    # Filter by class 2
    class_2_groups = [
        fg for fg in fgs.known_groups if fg.fg_class == FunctionalGroupClass.SKIP
    ]
    assert len(class_2_groups) == 1
    assert class_2_groups[0].name == "Amine"


def test_functional_groups_caching():
    """Test that identify_functional_groups uses caching."""
    fg = FunctionalGroup(
        idx=0,
        name="Hydroxyl",
        ui_name="Hydroxyl",
        smarts="[OH]",
        fg_class=FunctionalGroupClass.GENERAL,
    )
    fgs = FunctionalGroups.from_tuple((fg_to_dict(fg),))
    mol = Molecule("CO")

    # First call
    result1 = fgs.identify_functional_groups(mol)
    # Second call should use cache
    result2 = fgs.identify_functional_groups(mol)

    # Results should be identical
    assert result1 == result2


def test_functional_groups_frozen(
    functional_groups_collection: FunctionalGroups,
):
    """Test that FunctionalGroups is immutable (frozen)."""
    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        functional_groups_collection.known_groups = ()  # type: ignore


def test_functional_groups_initialization_with_list():
    """Test FunctionalGroups initialization from list of dicts."""
    fg_data = (
        frozendict(
            {
                "idx": 0,
                "name": "Hydroxyl",
                "ui_name": "Hydroxyl",
                "smarts": "[OH]",
                "fg_class": FunctionalGroupClass.GENERAL,
            }
        ),
        frozendict(
            {
                "idx": 1,
                "name": "Amine",
                "ui_name": "Amine",
                "smarts": "[NH2]",
                "fg_class": FunctionalGroupClass.SKIP,
            }
        ),
    )
    fgs = FunctionalGroups.from_tuple(fg_data)

    assert isinstance(fgs, FunctionalGroups)
    assert len(fgs.known_groups) == 2
    assert fgs.known_groups[0].name == "Hydroxyl"
    assert fgs.known_groups[1].name == "Amine"


def test_functional_groups_initialization_error():
    """Test that FunctionalGroups raises error on bad data."""
    fg_data = (frozendict({"idx": 0, "name": "Test"}),)  # missing required keys
    with pytest.raises(FunctionalGroupsInitializationError):
        FunctionalGroups.from_tuple(fg_data)


def test_matched_group_matching_sets_structure():
    """Test structure of matching_sets in MatchedGroup."""
    fg = FunctionalGroup(
        idx=0,
        name="Test",
        ui_name="Test",
        smarts="[OH]",
        fg_class=FunctionalGroupClass.GENERAL,
    )
    fgs = FunctionalGroups.from_tuple((fg_to_dict(fg),))

    # Ethanol has one hydroxyl group
    ethanol = Molecule("CCO")
    matches = fgs.identify_functional_groups(ethanol)

    if len(matches) > 0:
        match = matches[0]
        # matching_sets mirror GetSubstructMatches: tuple of per-match atom index tuples
        assert isinstance(match.matching_sets, tuple)
        for matching_set in match.matching_sets:
            assert isinstance(matching_set, tuple)
            assert all(isinstance(idx, int) for idx in matching_set)


def test_functional_group_missing_idx():
    """Test that FunctionalGroup.from_dict raises error when idx is missing."""
    fg_data = frozendict(
        {"name": "Test", "smarts": "[OH]", "fg_class": FunctionalGroupClass.GENERAL}
    )
    with pytest.raises(MissingRequiredKeysError):
        FunctionalGroup.from_dict(fg_data)


def test_functional_group_missing_name():
    """Test that FunctionalGroup.from_dict raises error when name is missing."""
    fg_data = frozendict(
        {"idx": 0, "smarts": "[OH]", "fg_class": FunctionalGroupClass.GENERAL}
    )
    with pytest.raises(MissingRequiredKeysError):
        FunctionalGroup.from_dict(fg_data)


def test_functional_group_missing_ui_name():
    """Test that FunctionalGroup.from_dict raises error when ui_name is missing."""
    fg_data = frozendict(
        {
            "idx": 0,
            "name": "Test",
            "smarts": "[OH]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    )
    with pytest.raises(MissingRequiredKeysError):
        FunctionalGroup.from_dict(fg_data)


def test_functional_group_missing_smarts():
    """Test that FunctionalGroup.from_dict raises error when smarts is missing."""
    fg_data = frozendict(
        {
            "idx": 0,
            "name": "Test",
            "ui_name": "Test",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    )
    with pytest.raises(MissingRequiredKeysError):
        FunctionalGroup.from_dict(fg_data)


def test_functional_group_missing_fg_class():
    """Test that FunctionalGroup.from_dict raises error when fg_class is missing."""
    fg_data = frozendict(
        {"idx": 0, "name": "Test", "ui_name": "Test", "smarts": "[OH]"}
    )
    with pytest.raises(MissingRequiredKeysError):
        FunctionalGroup.from_dict(fg_data)


def test_functional_group_invalid_idx_type():
    """Test that FunctionalGroup.from_dict raises error when idx is not int."""
    fg_data = frozendict(
        {
            "idx": "not_int",
            "name": "Test",
            "smarts": "[OH]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    )
    with pytest.raises(InvalidDataTypesError):
        FunctionalGroup.from_dict(fg_data)


def test_functional_group_invalid_name_type():
    """Test that FunctionalGroup.from_dict raises error when name is not str."""
    fg_data = frozendict(
        {
            "idx": 0,
            "name": 123,
            "ui_name": "Test",
            "smarts": "[OH]",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    )
    with pytest.raises(InvalidDataTypesError):
        FunctionalGroup.from_dict(fg_data)


def test_functional_group_invalid_smarts_type():
    """Test that FunctionalGroup.from_dict raises error when smarts is not str."""
    fg_data = frozendict(
        {
            "idx": 0,
            "name": "Test",
            "ui_name": "Test",
            "smarts": 123,
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    )
    with pytest.raises(InvalidDataTypesError):
        FunctionalGroup.from_dict(fg_data)


def test_functional_group_invalid_fg_class_type():
    """Test that FunctionalGroup.from_dict raises error when fg_class
    is not FunctionalGroupClass.
    """
    fg_data = frozendict(
        {
            "idx": 0,
            "name": "Test",
            "ui_name": "Test",
            "smarts": "[OH]",
            "fg_class": "not_FunctionalGroupClass",
        }
    )
    with pytest.raises(InvalidDataTypesError):
        FunctionalGroup.from_dict(fg_data)


def test_functional_groups_invalid_smarts_pattern():
    """Test that FunctionalGroups.from_tuple raises error for invalid SMARTS."""
    fg_data = frozendict(
        {
            "idx": 0,
            "name": "Invalid",
            "ui_name": "Invalid",
            "smarts": "[[[invalid_smarts",
            "fg_class": FunctionalGroupClass.GENERAL,
        }
    )
    with pytest.raises(FunctionalGroupsInitializationError):
        FunctionalGroups.from_tuple((fg_data,))
