from concurrent.futures import ThreadPoolExecutor
from threading import Event
from threading import Lock
from typing import Sequence

from chemcensor.basic import Reaction
from chemcensor.basic import SENTINEL
from chemcensor.chemcensor import ChemCensor
from chemcensor.chemcensor import ScoreResult
from chemcensor.configs.scoring_configs import ScoringConfig
from chemcensor.db.manager import DBManager
from chemcensor.processing.reaction_processor import ReactionProcessor


class _OverlapDetectingProcessor:
    """Block the first call and record any concurrent processor entry."""

    def __init__(self) -> None:
        self.first_entered = Event()
        self.release_first = Event()
        self.overlap_detected = Event()
        self._state_lock = Lock()
        self._active = False
        self._call_count = 0

    @property
    def call_count(self) -> int:
        with self._state_lock:
            return self._call_count

    def process(self, reaction: Reaction) -> Reaction:
        with self._state_lock:
            if self._active:
                self.overlap_detected.set()
            self._active = True
            self._call_count += 1
            call_number = self._call_count

        if call_number == 1:
            self.first_entered.set()
            if not self.release_first.wait(timeout=5):
                raise TimeoutError("test did not release the first scoring call")

        with self._state_lock:
            self._active = False
        return SENTINEL

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        return tuple(self.process(reaction) for reaction in reactions)


def test_concurrent_calls_to_one_censor_are_serialized() -> None:
    detector = _OverlapDetectingProcessor()
    second_started = Event()
    censor = ChemCensor(
        manager=DBManager(),
        processor=ReactionProcessor(processors=(detector,)),
    )

    def evaluate_second_reaction() -> ScoreResult:
        second_started.set()
        return censor.evaluate("CCN>>CC=N")

    with ThreadPoolExecutor(max_workers=2) as executor:
        first = executor.submit(censor.evaluate, "CCO>>CC=O")
        assert detector.first_entered.wait(timeout=5)

        second = executor.submit(evaluate_second_reaction)
        assert second_started.wait(timeout=5)
        assert not detector.overlap_detected.wait(timeout=0.1)

        detector.release_first.set()
        first_result = first.result(timeout=5)
        second_result = second.result(timeout=5)

    failed_score = ScoringConfig.failed_reaction_scoring.value
    assert first_result.with_functional_groups == failed_score
    assert second_result.with_functional_groups == failed_score
    assert detector.call_count == 2
    assert not detector.overlap_detected.is_set()
