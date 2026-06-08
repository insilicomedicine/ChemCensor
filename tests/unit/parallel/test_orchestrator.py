from __future__ import annotations

import queue as queue_mod
import threading
from pathlib import Path

import pytest

from chemcensor.parallel import checkpoint as ckpt_mod
from chemcensor.parallel import orchestrator
from chemcensor.parallel.io import ListSink
from chemcensor.parallel.messages import Result


def _run_writer(
    messages: list[Result],
    *,
    checkpoint_path: Path,
    checkpoint_interval: int,
    initial_state: ckpt_mod.CheckpointState | None = None,
) -> ListSink:
    """Drive ``_writer_thread`` synchronously with a prefilled queue."""
    q: queue_mod.Queue = queue_mod.Queue()
    for msg in messages:
        q.put(msg)
    q.put(None)  # single-worker end-of-stream sentinel

    sink = ListSink()
    orchestrator._writer_thread(
        q,
        sink,
        n_workers=1,
        total_hint=None,
        progress=False,
        checkpoint_path=checkpoint_path,
        checkpoint_interval=checkpoint_interval,
        initial_state=initial_state or ckpt_mod.CheckpointState(),
        stop_event=threading.Event(),
        error_event=threading.Event(),
    )
    return sink


def test_periodic_checkpoint_fires_when_batch_size_does_not_divide_interval(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Regression: checkpoints must be written mid-run, not only at the end.

    The old condition (``completed_total % checkpoint_interval == 0``) never
    fired when the per-batch step did not divide the interval — here batches
    of 3 with interval 5 (3, 6, 9, 12 are never multiples of 5), so every bit
    of progress was lost on an early termination. The delta-based condition
    must save part-way through.
    """
    saved: list[ckpt_mod.CheckpointState] = []
    monkeypatch.setattr(
        orchestrator.ckpt_mod,
        "save",
        lambda _path, state: saved.append(state),
    )

    # Four batches of 3 contiguous indices each → completed_total 3, 6, 9, 12.
    messages = [
        Result(
            batch_id=b,
            items=tuple((b * 3 + j, f"R{b * 3 + j}>>P", 1.0) for j in range(3)),
        )
        for b in range(4)
    ]

    _run_writer(
        messages,
        checkpoint_path=tmp_path / "state.ckpt",
        checkpoint_interval=5,
    )

    # At least one mid-run checkpoint (before the final flush) must reflect
    # partial progress; the old modulo logic would only ever save 12.
    mid_run = [s for s in saved if 0 < s.completed_count < 12]
    assert mid_run, f"no mid-run checkpoint was written: {saved}"
    assert saved[-1].completed_count == 12


def test_checkpoint_delta_counts_from_resumed_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The delta is measured from the resumed ``completed_count``.

    A run resumed at 100 with interval 5 must not checkpoint on the very
    first tiny batch just because ``100 % 5 == 0`` — it should wait until
    ``checkpoint_interval`` *new* records have been processed.
    """
    saved: list[ckpt_mod.CheckpointState] = []
    monkeypatch.setattr(
        orchestrator.ckpt_mod,
        "save",
        lambda _path, state: saved.append(state),
    )

    # Resume at 100; first batch adds 2 (→102, delta 2 < 5: no save),
    # second batch adds 2 (→104, delta 4 < 5: no save) until the threshold.
    messages = [
        Result(batch_id=0, items=((100, "a>>b", 1.0), (101, "c>>d", 1.0))),
        Result(batch_id=1, items=((102, "e>>f", 1.0), (103, "g>>h", 1.0))),
        Result(batch_id=2, items=((104, "i>>j", 1.0), (105, "k>>l", 1.0))),
    ]

    _run_writer(
        messages,
        checkpoint_path=tmp_path / "state.ckpt",
        checkpoint_interval=5,
        initial_state=ckpt_mod.CheckpointState(
            last_contiguous_idx=99, completed_count=100
        ),
    )

    # If ``last_ckpt_at`` were (wrongly) seeded to 0, the first batch would
    # already satisfy ``102 - 0 >= 5`` and save prematurely. Correct seeding
    # from the resumed count delays the first save until 106 (6 new ≥ 5).
    assert all(
        s.completed_count != 102 for s in saved
    ), f"checkpoint fired too early: {saved}"
    assert any(
        s.completed_count == 106 for s in saved
    ), f"expected a periodic save at 106: {saved}"
