from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..reaction_center import ReactionCenterType


class ReactionError(Exception):
    """Base class for reaction errors."""

    pass


class ReactionCenterNotFoundError(ReactionError):
    """Raised when a reaction center is not found."""

    def __init__(self, center_type: ReactionCenterType):
        self.center_type = center_type
        super().__init__(f"Reaction center {center_type.name} not found.")
