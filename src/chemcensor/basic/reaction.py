from dataclasses import dataclass
from dataclasses import field
from functools import partial

import numpy as np
from frozendict import frozendict

from ..rules.functional_groups import FG_COLLECTION_SEAR
from .errors import ReactionCenterNotFoundError
from .reaction_center import ReactionCenter
from .reaction_center import ReactionCenterType
from .reaction_transform import ReactionTransform


@dataclass(frozen=True)
class Reaction:
    """Represents a chemical reaction with its processing stages."""

    reaction_smiles: str
    mapped_reaction_smiles: str = ""
    processed_reaction_smiles: str = ""
    reaction_transform: ReactionTransform | None = None
    is_sear_reaction: bool = False
    sear_signature: np.ndarray = field(
        default_factory=partial(np.zeros, FG_COLLECTION_SEAR.num_groups, dtype=np.uint8)
    )
    reaction_centers: frozendict[ReactionCenterType, ReactionCenter] = frozendict()
    canonical_smiles: str = ""
    is_sis_reaction: bool = False
    is_tautomerization_reaction: bool = False
    dummy: bool = False
    document_id: str = ""

    def get_reaction_center_by_type(
        self, center_type: ReactionCenterType
    ) -> ReactionCenter:
        """Get the reaction center by type.

        :param center_type: The type of reaction center to get.
        :type center_type: ReactionCenterType
        :return: The reaction center.
        :rtype: ReactionCenter
        """
        try:
            return self.reaction_centers[center_type]
        except KeyError:
            raise ReactionCenterNotFoundError(center_type)
