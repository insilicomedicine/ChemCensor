from dataclasses import replace
from typing import Sequence

import pytest

from chemcensor import ChemCensor
from chemcensor import FailureStage
from chemcensor import ScoreResult
from chemcensor import ScoringConfig
from chemcensor import TraceOutcome
from chemcensor.basic import Reaction
from chemcensor.db import DBManager
from chemcensor.extraction.errors import ReactionCenterExtractorError
from chemcensor.processing.errors.validator_errors import RxnSmilesSyntaxError
from chemcensor.processing.reaction_processor import ReactionProcessor


class _FailingProcessor:
    def process(self, reaction: Reaction) -> Reaction:
        raise RxnSmilesSyntaxError("invalid reaction syntax", reaction.reaction_smiles)

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        return tuple(self.process(reaction) for reaction in reactions)


class _CanonicalizingProcessor:
    def process(self, reaction: Reaction) -> Reaction:
        return replace(reaction, canonical_smiles=reaction.reaction_smiles)

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        return tuple(self.process(reaction) for reaction in reactions)


def test_processing_failure_returns_structured_reason_without_raising() -> None:
    censor = ChemCensor(
        manager=DBManager(),
        processor=ReactionProcessor(processors=(_FailingProcessor(),)),
    )

    trace = censor.trace("not-a-reaction")
    result = trace.result

    assert trace.outcome is TraceOutcome.FAILED
    assert trace.centers == ()
    failed_score = ScoringConfig.failed_reaction_scoring.value
    assert result.with_functional_groups == failed_score
    assert result.without_functional_groups == failed_score
    assert result.failure_reason is not None
    assert result.failure_reason.stage is FailureStage.PROCESSING
    assert result.failure_reason.category == "RxnSmilesSyntaxError"
    assert result.failure_reason.message == "invalid reaction syntax"


def test_extraction_failure_returns_structured_reason(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    censor = ChemCensor(
        manager=DBManager(),
        processor=ReactionProcessor(processors=(_CanonicalizingProcessor(),)),
    )

    def fail_extraction(_reaction: Reaction) -> Reaction:
        raise ReactionCenterExtractorError("cannot extract reaction center")

    monkeypatch.setattr(censor._rc_extractor, "extract_rc", fail_extraction)

    result = censor.evaluate("CCO>>CC=O")

    failed_score = ScoringConfig.failed_reaction_scoring.value
    assert result.with_functional_groups == failed_score
    assert result.without_functional_groups == failed_score
    assert result.failure_reason is not None
    assert result.failure_reason.stage is FailureStage.EXTRACTION
    assert result.failure_reason.category == "ReactionCenterExtractorError"
    assert result.failure_reason.message == "cannot extract reaction center"


def test_successful_result_has_no_failure_reason() -> None:
    result = ScoreResult.uniform(1.0)

    assert result.failure_reason is None
