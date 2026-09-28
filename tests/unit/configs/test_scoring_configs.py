import pytest

from chemcensor import ReactionCenterType
from chemcensor import ScoringConfig
from chemcensor import ScoringOutcome
from chemcensor import TraceOutcome


@pytest.mark.parametrize("center_type", list(ReactionCenterType))
def test_center_type_scoring_resolves_every_center_type(
    center_type: ReactionCenterType,
) -> None:
    expected = ScoringConfig[f"lc_{center_type.value}_scoring"].value

    assert ScoringConfig.center_type_scoring(center_type) == expected


@pytest.mark.parametrize(
    ("outcome", "meaning_fragment"),
    [
        (ScoringOutcome.FAILED, "failed"),
        (ScoringOutcome.DEFAULT, "No known reaction center"),
        (ScoringOutcome.TAUTOMERIZATION, "tautomerization"),
        (ScoringOutcome.SIS, "SIS"),
        (ScoringOutcome.EXACT_MATCH, "Exact canonical reaction match"),
    ],
)
def test_every_special_outcome_has_a_stable_score_and_meaning(
    outcome: ScoringOutcome,
    meaning_fragment: str,
) -> None:
    score = ScoringConfig.outcome_scoring(outcome)

    assert score in ScoringConfig.score_meanings()
    assert meaning_fragment in ScoringConfig.outcome_meaning(outcome)


def test_sis_and_tautomerization_are_distinct_outcomes_with_the_same_score() -> None:
    assert ScoringOutcome.SIS is not ScoringOutcome.TAUTOMERIZATION
    assert str(ScoringOutcome.SIS) == "sis"
    assert ScoringConfig.outcome_scoring(
        ScoringOutcome.SIS
    ) == ScoringConfig.outcome_scoring(ScoringOutcome.TAUTOMERIZATION)
    assert ScoringConfig.outcome_meaning(
        ScoringOutcome.SIS
    ) != ScoringConfig.outcome_meaning(ScoringOutcome.TAUTOMERIZATION)


@pytest.mark.parametrize("outcome", list(TraceOutcome))
def test_trace_outcome_meanings_are_resolved_directly(outcome: TraceOutcome) -> None:
    assert ScoringConfig.outcome_meaning(outcome)


def test_no_coverage_and_default_have_the_same_meaning() -> None:
    assert ScoringConfig.outcome_meaning(
        TraceOutcome.NO_COVERAGE
    ) == ScoringConfig.outcome_meaning(ScoringOutcome.DEFAULT)


def test_score_meanings_returns_an_independent_complete_mapping() -> None:
    meanings = ScoringConfig.score_meanings()

    assert set(meanings) == {float(member.value) for member in ScoringConfig}
    meanings[ScoringConfig.exact_match_scoring.value] = "client label"
    assert (
        ScoringConfig.score_meaning(ScoringConfig.exact_match_scoring.value)
        != "client label"
    )


def test_score_meaning_rejects_unknown_score() -> None:
    with pytest.raises(KeyError):
        ScoringConfig.score_meaning(999.0)
