from __future__ import annotations

from enum import Enum
from enum import StrEnum

from ..basic import ReactionCenterType
from ..trace import TraceOutcome


class ScoringOutcome(StrEnum):
    """Stable identifiers for non-center scoring outcomes."""

    FAILED = "failed"
    DEFAULT = "default"
    TAUTOMERIZATION = "tautomerization"
    SIS = "sis"
    EXACT_MATCH = "exact_match"


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

    @classmethod
    def center_type_scoring(cls, center_type: ReactionCenterType) -> float:
        """Return the score associated with a reaction-center type.

        :param center_type: Reaction-center context level to resolve.
        :type center_type: ReactionCenterType
        :return: Numeric score for the center type.
        :rtype: float
        """
        return float(cls[f"lc_{center_type.value}_scoring"].value)

    @classmethod
    def outcome_scoring(cls, outcome: ScoringOutcome) -> float:
        """Return the score associated with a non-center outcome.

        :param outcome: Stable identifier of the scoring outcome.
        :type outcome: ScoringOutcome
        :return: Numeric score for the outcome.
        :rtype: float
        """
        return float(_OUTCOME_SCORES[outcome])

    @classmethod
    def outcome_meaning(cls, outcome: ScoringOutcome | TraceOutcome) -> str:
        """Return the human-readable meaning of a scoring or trace outcome.

        Unlike :meth:`score_meaning`, this method distinguishes outcomes that
        share a numeric value, such as SIS and tautomerization. Trace outcomes
        are accepted directly, so callers can resolve
        ``ScoringConfig.outcome_meaning(trace.outcome)`` without translating
        between public enums.

        :param outcome: Stable identifier of the scoring outcome.
        :type outcome: ScoringOutcome | TraceOutcome
        :return: Human-readable interpretation of the outcome.
        :rtype: str
        """
        return _OUTCOME_MEANINGS[outcome]

    @classmethod
    def score_meaning(cls, score: float) -> str:
        """Return the stable human-readable meaning of a score.

        A score of ``1.0`` is shared by an RC1 match, SIS classification and
        tautomerization. These outcomes cannot be distinguished from the
        numeric score alone, so its interpretation names all three.

        :param score: A numeric value returned by ChemCensor.
        :type score: float
        :return: Human-readable interpretation of the score.
        :rtype: str
        :raises KeyError: If the value is not part of the scoring scale.
        """
        return _SCORE_MEANINGS[float(score)]

    @classmethod
    def score_meanings(cls) -> dict[float, str]:
        """Return the complete score-to-meaning mapping.

        A new dictionary is returned so callers can adapt labels for their UI
        without mutating the library's definitions.

        :return: All supported numeric scores and their stable meanings.
        :rtype: dict[float, str]
        """
        return dict(_SCORE_MEANINGS)


_OUTCOME_SCORES = {
    ScoringOutcome.FAILED: ScoringConfig.failed_reaction_scoring.value,
    ScoringOutcome.DEFAULT: ScoringConfig.default_reaction_scoring.value,
    ScoringOutcome.TAUTOMERIZATION: (
        ScoringConfig.tautomerization_reaction_scoring.value
    ),
    ScoringOutcome.SIS: ScoringConfig.sis_reaction_scoring.value,
    ScoringOutcome.EXACT_MATCH: ScoringConfig.exact_match_scoring.value,
}

_OUTCOME_MEANINGS: dict[ScoringOutcome | TraceOutcome, str] = {
    ScoringOutcome.FAILED: (
        "Reaction processing or reaction-center extraction failed."
    ),
    ScoringOutcome.DEFAULT: "No known reaction center matched the reaction.",
    ScoringOutcome.TAUTOMERIZATION: ("The reaction was classified as tautomerization."),
    ScoringOutcome.SIS: "The reaction was classified as SIS.",
    ScoringOutcome.EXACT_MATCH: (
        "Exact canonical reaction match found in the database."
    ),
    TraceOutcome.CENTER_COVERAGE: (
        "One or more known reaction centers matched the reaction."
    ),
    TraceOutcome.NO_COVERAGE: "No known reaction center matched the reaction.",
}

_SCORE_MEANINGS = {
    ScoringConfig.failed_reaction_scoring.value: _OUTCOME_MEANINGS[
        ScoringOutcome.FAILED
    ],
    ScoringConfig.default_reaction_scoring.value: _OUTCOME_MEANINGS[
        ScoringOutcome.DEFAULT
    ],
    ScoringConfig.lc_1_scoring.value: (
        "RC1 matched, or the reaction was classified as SIS or tautomerization."
    ),
    ScoringConfig.lc_2_scoring.value: "Reaction center RC2 matched.",
    ScoringConfig.lc_3_scoring.value: "Reaction center RC3 matched.",
    ScoringConfig.lc_4_scoring.value: "Reaction center RC4 matched.",
    ScoringConfig.exact_match_scoring.value: _OUTCOME_MEANINGS[
        ScoringOutcome.EXACT_MATCH
    ],
}
