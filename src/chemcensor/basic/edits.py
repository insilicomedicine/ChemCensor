from enum import Enum


class AtomEditType(Enum):
    NONE = 0
    ATOM_ADDED = 1
    FRAGMENT_ATTACH = 2
    FRAGMENT_DETACH = 3
    PROPERTY_CHANGE = 4

    def __bool__(self) -> bool:
        return self != AtomEditType.NONE
