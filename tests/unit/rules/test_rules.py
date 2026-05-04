import pytest

from chemcensor.basic.functional_groups import FunctionalGroups
from chemcensor.rules.expandable_functional_groups import EXPANDABLE_FUNCTIONAL_GROUPS
from chemcensor.rules.functional_groups import FUNCTIONAL_GROUPS


@pytest.mark.parametrize("functional_group", FUNCTIONAL_GROUPS)
def test_functional_group_idx(functional_group):
    fgs = FunctionalGroups.from_tuple(FUNCTIONAL_GROUPS)
    assert len(fgs.known_groups) == len(FUNCTIONAL_GROUPS)


@pytest.mark.parametrize("functional_group", EXPANDABLE_FUNCTIONAL_GROUPS)
def test_expandable_functional_groups(functional_group):
    exondable_fgs = FunctionalGroups.from_tuple(EXPANDABLE_FUNCTIONAL_GROUPS)
    assert len(exondable_fgs.known_groups) == len(EXPANDABLE_FUNCTIONAL_GROUPS)
