from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock
from unittest.mock import patch

import chemcensor.parallel as parallel
from chemcensor import ScoreResult
from chemcensor.basic import Reaction
from chemcensor.parallel import ParallelConfig


class _StubCensor:
    def __init__(self, result: ScoreResult) -> None:
        self.result = result
        self.calls: list[str] = []
        self.batch_calls = 0

    def evaluate_batch(self, reactions: list[Reaction]) -> list[ScoreResult]:
        self.batch_calls += 1
        self.calls.extend(reaction.reaction_smiles for reaction in reactions)
        return [self.result] * len(reactions)


def test_small_batch_uses_in_process_scorer_without_pipeline(tmp_path: Path) -> None:
    expected = ScoreResult.uniform(2.0)
    censor = _StubCensor(expected)
    db_path = tmp_path / "db.sqlite"
    db_path.touch()

    with (
        patch.object(parallel, "_get_in_process_censor", return_value=censor),
        patch.object(
            parallel,
            "_run_pipeline",
            side_effect=AssertionError("small batch spawned the pipeline"),
        ),
    ):
        result = parallel.score_batch(
            ["A>>B", "C>>D"],
            db_path=db_path,
            config=ParallelConfig(in_process_batch_threshold=2),
        )

    assert result == [expected, expected]
    assert censor.calls == ["A>>B", "C>>D"]
    assert censor.batch_calls == 1


def test_score_batch_downloads_default_database_when_omitted(
    tmp_path: Path,
) -> None:
    expected = ScoreResult.uniform(2.0)
    censor = _StubCensor(expected)
    db_path = tmp_path / "db.sqlite"
    db_path.touch()

    with (
        patch.object(
            parallel, "resolve_database_path", return_value=db_path
        ) as resolve,
        patch.object(parallel, "_get_in_process_censor", return_value=censor),
    ):
        result = parallel.score_batch(
            ["A>>B"],
            config=ParallelConfig(in_process_batch_threshold=1),
        )

    resolve.assert_called_once_with(None)
    assert result == [expected]


def test_batch_above_threshold_retains_multiprocessing_path(tmp_path: Path) -> None:
    db_path = tmp_path / "db.sqlite"
    db_path.touch()

    with (
        patch.object(parallel, "_run_pipeline") as pipeline,
        patch.object(
            parallel,
            "_get_in_process_censor",
            side_effect=AssertionError("large batch used in-process scorer"),
        ),
        patch.object(parallel, "_IN_PROCESS_CENSOR", Mock()),
        patch.object(parallel, "_IN_PROCESS_KEY", ("cached",)),
    ):
        parallel.score_batch(
            ["A>>B", "C>>D"],
            db_path=db_path,
            config=ParallelConfig(in_process_batch_threshold=1),
        )
        assert parallel._IN_PROCESS_CENSOR is None
        assert parallel._IN_PROCESS_KEY is None

    pipeline.assert_called_once()


def test_in_process_censor_is_reused_for_same_database_and_config(
    tmp_path: Path,
    monkeypatch,
) -> None:
    db_path = tmp_path / "db.sqlite"
    db_path.touch()
    censor = Mock()
    monkeypatch.setattr(parallel, "_IN_PROCESS_CENSOR", None)
    monkeypatch.setattr(parallel, "_IN_PROCESS_KEY", None)

    with patch("chemcensor.ChemCensor.open", return_value=censor) as open_censor:
        config = ParallelConfig(mapper_threads=3).resolved()
        first = parallel._get_in_process_censor(db_path, config)
        second = parallel._get_in_process_censor(db_path, config)

    assert first is censor
    assert second is censor
    open_censor.assert_called_once()
    assert open_censor.call_args.kwargs["config"].mapper_n_jobs == 3


def test_release_in_process_scorer_clears_initialized_cuda(monkeypatch) -> None:
    cuda = Mock()
    cuda.is_initialized.return_value = True
    torch_module = ModuleType("torch")
    setattr(torch_module, "cuda", cuda)
    monkeypatch.setitem(
        parallel.sys.modules,
        "torch",
        torch_module,
    )
    monkeypatch.setattr(parallel, "_IN_PROCESS_CENSOR", Mock())
    monkeypatch.setattr(parallel, "_IN_PROCESS_KEY", ("cached",))

    parallel.release_in_process_scorer()

    assert parallel._IN_PROCESS_CENSOR is None
    assert parallel._IN_PROCESS_KEY is None
    cuda.empty_cache.assert_called_once_with()


def test_concurrent_small_batches_are_guarded(tmp_path: Path) -> None:
    db_path = tmp_path / "db.sqlite"
    db_path.touch()
    state_lock = threading.Lock()
    active = 0
    max_active = 0

    class BlockingCensor:
        def evaluate_batch(self, reactions: list[Reaction]) -> list[ScoreResult]:
            nonlocal active, max_active
            with state_lock:
                active += 1
                max_active = max(max_active, active)
            time.sleep(0.02)
            with state_lock:
                active -= 1
            return [ScoreResult.uniform(1.0)] * len(reactions)

    with patch.object(
        parallel,
        "_get_in_process_censor",
        return_value=BlockingCensor(),
    ):
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(
                    parallel.score_batch,
                    [reaction],
                    db_path=db_path,
                    config=ParallelConfig(in_process_batch_threshold=1),
                )
                for reaction in ("A>>B", "C>>D")
            ]
            for future in futures:
                future.result()

    assert max_active == 1
