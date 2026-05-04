from frozendict import frozendict

from ..basic.functional_groups import FunctionalGroupClass
from ..basic.functional_groups import FunctionalGroups

EXPANDABLE_FUNCTIONAL_GROUPS: tuple[
    frozendict[str, int | str | FunctionalGroupClass], ...
] = (
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 0,
            "name": "Carbonyl",
            "smarts": "C=O",
            "fg_class": FunctionalGroupClass.EXPANDABLE,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 1,
            "name": "Amidine",
            "smarts": "C=[Nh1+0]",
            "fg_class": FunctionalGroupClass.EXPANDABLE,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 2,
            "name": "Sulfone",
            "smarts": "O=S=O",
            "fg_class": FunctionalGroupClass.EXPANDABLE,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 3,
            "name": "Nitrile",
            "smarts": "C#N",
            "fg_class": FunctionalGroupClass.EXPANDABLE,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 4,
            "name": "Aryl ketone",
            "smarts": "c=O",
            "fg_class": FunctionalGroupClass.EXPANDABLE,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 5,
            "name": "Phosphoryl",
            "smarts": "P=O",
            "fg_class": FunctionalGroupClass.EXPANDABLE,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 6,
            "name": "CF3",
            "smarts": "[C$(Cc)](F)(F)F",
            "fg_class": FunctionalGroupClass.EXPANDABLE,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 7,
            "name": "Azide and azide anion",
            "smarts": "[#7]=[#7+]=[#7-]",
            "fg_class": FunctionalGroupClass.EXPANDABLE,
        }
    ),
    frozendict[str, int | str | FunctionalGroupClass](
        {
            "idx": 8,
            "name": "Nitro group",
            "smarts": "[N+](=[O])[O-]",
            "fg_class": FunctionalGroupClass.EXPANDABLE,
        }
    ),
)

EXPANDABLE_FUNCTIONAL_GROUPS_COLLECTION = FunctionalGroups.from_tuple(
    EXPANDABLE_FUNCTIONAL_GROUPS
)
