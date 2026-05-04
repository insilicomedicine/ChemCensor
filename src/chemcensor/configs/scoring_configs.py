from enum import Enum


class ScoringConfig(Enum):
    """Configuration for scoring reactions.

    Reaction-center scores follow the naming convention ``lc_{N}_scoring``
    where *N* is the integer value of the corresponding
    :class:`~chemcensor.basic.ReactionCenterType` (1–4).
    Use :meth:`center_type_scoring` to look up the score for a given
    center type instead of hard-coding the attribute names.
    """

    failed_reaction_scoring = -1.0
    default_reaction_scoring = 0.0
    tautomerization_reaction_scoring = 1.0
    sis_reaction_scoring = 1.0
    lc_1_scoring = 1.0
    lc_2_scoring = 2.0
    lc_3_scoring = 3.0
    lc_4_scoring = 4.0
    exact_match_scoring = 5.0
