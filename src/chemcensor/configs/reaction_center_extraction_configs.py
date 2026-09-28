from __future__ import annotations

from dataclasses import dataclass

from ..basic.reaction_center import ReactionCenterType

DEFAULT_NEIGHBOR_DEPTH = 1


@dataclass(frozen=True)
class ExtractionConfig:
    """Configuration for a single reaction center extraction level.

    :param center_type: Reaction center type (RC1 = base, RC2–RC4 = extended).
    :type center_type: ReactionCenterType
    :param neighbor_depth: How many layers of neighbors to include.
    :type neighbor_depth: int
    :param include_rings: Whether to include complete rings.
    :type include_rings: bool
    :param include_fused: Whether to include fused ring systems.
    :type include_fused: bool
    :param include_substituents: Whether to include aryl substituents.
    :type include_substituents: bool
    :param include_chiral: Whether to expand the fragment around chiral centers,
        pulling in their rings and neighbors.
    :type include_chiral: bool
    :param include_stereo_tags: Whether to carry stereo tags over to the extracted
        fragment. Independent of ``include_chiral``: a level can keep the tags of
        the atoms it already covers without growing the fragment.
    :type include_stereo_tags: bool
    """

    center_type: ReactionCenterType
    neighbor_depth: int = DEFAULT_NEIGHBOR_DEPTH
    include_rings: bool = False
    include_fused: bool = False
    include_substituents: bool = False
    include_chiral: bool = False
    include_stereo_tags: bool = True


BASE_CONFIG = ExtractionConfig(center_type=ReactionCenterType.RC1)

RING_CONFIGS: tuple[ExtractionConfig, ...] = (
    ExtractionConfig(
        center_type=ReactionCenterType.RC2,
        include_rings=True,
        include_chiral=True,
    ),
    ExtractionConfig(
        center_type=ReactionCenterType.RC3,
        include_rings=True,
        include_fused=True,
        include_chiral=True,
    ),
    ExtractionConfig(
        center_type=ReactionCenterType.RC4,
        include_rings=True,
        include_fused=True,
        include_substituents=True,
        include_chiral=True,
    ),
)

LINEAR_CONFIGS: tuple[ExtractionConfig, ...] = (
    ExtractionConfig(
        center_type=ReactionCenterType.RC2,
        neighbor_depth=DEFAULT_NEIGHBOR_DEPTH + 1,
        include_chiral=True,
    ),
    ExtractionConfig(
        center_type=ReactionCenterType.RC3,
        neighbor_depth=DEFAULT_NEIGHBOR_DEPTH + 2,
        include_chiral=True,
    ),
    ExtractionConfig(
        center_type=ReactionCenterType.RC4,
        neighbor_depth=DEFAULT_NEIGHBOR_DEPTH + 3,
        include_chiral=True,
    ),
)
