from __future__ import annotations

import json
from pathlib import Path

import pytest

from chemcensor.parallel.checkpoint import CheckpointState
from chemcensor.parallel.checkpoint import load
from chemcensor.parallel.checkpoint import save
from chemcensor.parallel.errors import CheckpointCorruptedError


def test_load_missing_returns_default(tmp_path: Path) -> None:
    state = load(tmp_path / "absent.ckpt")
    assert state == CheckpointState()
    assert state.last_contiguous_idx == -1
    assert state.completed_count == 0


def test_save_then_load_roundtrip(tmp_path: Path) -> None:
    target = tmp_path / "state.ckpt"
    save(target, CheckpointState(last_contiguous_idx=42, completed_count=43))
    loaded = load(target)
    assert loaded == CheckpointState(last_contiguous_idx=42, completed_count=43)


def test_save_is_atomic(tmp_path: Path) -> None:
    target = tmp_path / "state.ckpt"
    # Pre-populate the destination so we can confirm it's overwritten.
    target.write_text(
        json.dumps({"version": 1, "last_contiguous_idx": 0, "completed_count": 0})
    )
    save(target, CheckpointState(last_contiguous_idx=10, completed_count=11))
    assert load(target).last_contiguous_idx == 10
    # The temp file should be cleaned up after rename.
    assert not target.with_suffix(target.suffix + ".tmp").exists()


def test_roundtrip_preserves_completed_above(tmp_path: Path) -> None:
    target = tmp_path / "state.ckpt"
    state = CheckpointState(
        last_contiguous_idx=2,
        completed_count=5,
        completed_above=frozenset({4, 5}),
    )
    save(target, state)
    assert load(target) == state


def test_v1_checkpoint_loads_with_empty_completed_above(tmp_path: Path) -> None:
    """Old (v1) checkpoints have no ``completed_above`` — default to empty."""
    target = tmp_path / "v1.ckpt"
    target.write_text(
        json.dumps({"version": 1, "last_contiguous_idx": 7, "completed_count": 8})
    )
    loaded = load(target)
    assert loaded.last_contiguous_idx == 7
    assert loaded.completed_count == 8
    assert loaded.completed_above == frozenset()


def test_completed_above_serialized_sorted(tmp_path: Path) -> None:
    target = tmp_path / "state.ckpt"
    save(
        target,
        CheckpointState(
            last_contiguous_idx=0,
            completed_count=3,
            completed_above=frozenset({9, 3, 5}),
        ),
    )
    payload = json.loads(target.read_text(encoding="utf-8"))
    assert payload["version"] == 2
    assert payload["completed_above"] == [3, 5, 9]


def test_load_unknown_version_raises(tmp_path: Path) -> None:
    target = tmp_path / "bad.ckpt"
    target.write_text(
        json.dumps({"version": 99, "last_contiguous_idx": 0, "completed_count": 0})
    )
    with pytest.raises(CheckpointCorruptedError):
        load(target)


def test_load_malformed_raises(tmp_path: Path) -> None:
    target = tmp_path / "bad.ckpt"
    target.write_text("not json")
    with pytest.raises(CheckpointCorruptedError):
        load(target)


def test_load_missing_keys_raises(tmp_path: Path) -> None:
    target = tmp_path / "bad.ckpt"
    target.write_text(json.dumps({"version": 1}))
    with pytest.raises(CheckpointCorruptedError):
        load(target)
