from __future__ import annotations

import json
import os
from dataclasses import dataclass
from os import PathLike
from pathlib import Path

from .errors import CheckpointCorruptedError


_CKPT_VERSION = 2


@dataclass(frozen=True)
class CheckpointState:
    """In-memory representation of a checkpoint file.

    :param last_contiguous_idx: Largest input index ``i`` such that every
        record in ``[0, i]`` has been scored and flushed to the sink.
        ``-1`` means no records have been completed yet.
    :type last_contiguous_idx: int
    :param completed_count: Total number of records flushed so far. May
        be greater than ``last_contiguous_idx + 1`` because of
        out-of-order completion (see ``completed_above``).
    :type completed_count: int
    :param completed_above: Input indices that have been scored and
        flushed but sit *above* the contiguous frontier (i.e. ``idx >
        last_contiguous_idx``) because their lower neighbours were not
        finished yet. Persisting them lets resume skip already-written
        rows instead of re-scoring them and appending duplicate ``idx``
        rows to the output. Older (v1) checkpoints have none.
    :type completed_above: frozenset[int]
    """

    last_contiguous_idx: int = -1
    completed_count: int = 0
    completed_above: frozenset[int] = frozenset()


def load(path: str | PathLike) -> CheckpointState:
    """Load a checkpoint file. Returns a fresh state if the file is missing.

    :param path: Path to the ``.ckpt`` file.
    :type path: str | PathLike
    :return: Parsed checkpoint state.
    :rtype: CheckpointState
    :raises CheckpointCorruptedError: If the file exists but cannot be
        parsed or has an unexpected version.
    """
    path = Path(path)
    if not path.exists():
        return CheckpointState()

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise CheckpointCorruptedError(f"Cannot read checkpoint {path}: {e}") from e

    # v1 and v2 are read-compatible: v1 simply has no ``completed_above``.
    if not isinstance(payload, dict) or payload.get("version") not in (
        1,
        _CKPT_VERSION,
    ):
        raise CheckpointCorruptedError(
            f"Unexpected checkpoint payload at {path}: {payload!r}"
        )

    try:
        completed_above = frozenset(int(i) for i in payload.get("completed_above", ()))
        return CheckpointState(
            last_contiguous_idx=int(payload["last_contiguous_idx"]),
            completed_count=int(payload["completed_count"]),
            completed_above=completed_above,
        )
    except (KeyError, TypeError, ValueError) as e:
        raise CheckpointCorruptedError(f"Malformed checkpoint at {path}: {e}") from e


def save(path: str | PathLike, state: CheckpointState) -> None:
    """Atomically write ``state`` to ``path``.

    The write goes to a sibling ``.tmp`` file which is then renamed via
    :func:`os.replace` — this is atomic on POSIX and on modern Windows.

    :param path: Destination ``.ckpt`` path.
    :type path: str | PathLike
    :param state: Checkpoint state to persist.
    :type state: CheckpointState
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")

    payload = {
        "version": _CKPT_VERSION,
        "last_contiguous_idx": state.last_contiguous_idx,
        "completed_count": state.completed_count,
        # Sorted for stable, diff-friendly output.
        "completed_above": sorted(state.completed_above),
    }
    tmp.write_text(json.dumps(payload), encoding="utf-8")
    os.replace(tmp, path)
