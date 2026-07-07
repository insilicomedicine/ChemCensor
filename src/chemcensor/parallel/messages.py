from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MapTask:
    """A batch of raw reaction SMILES queued for atom mapping.

    :param batch_id: Monotonically increasing id assigned by the reader,
        used for ordering and crash-recovery bookkeeping.
    :type batch_id: int
    :param items: Tuple of ``(idx, raw_smiles)`` pairs. ``idx`` is the
        input position (row number for files, list index for in-memory
        inputs).
    :type items: tuple[tuple[int, str], ...]
    """

    batch_id: int
    items: tuple[tuple[int, str], ...]


@dataclass(frozen=True)
class ScoreTask:
    """A batch of (raw, mapped) reaction SMILES ready for scoring.

    ``mapped`` is ``None`` when the mapper failed for that record; the
    scorer will short-circuit to ``failed_reaction_scoring`` without
    spending CPU on the rest of the pipeline.

    :param batch_id: Id propagated from the originating :class:`MapTask`.
    :type batch_id: int
    :param items: Tuple of ``(idx, raw_smiles, mapped_smiles_or_None)``.
    :type items: tuple[tuple[int, str, str | None], ...]
    """

    batch_id: int
    items: tuple[tuple[int, str, str | None], ...]


@dataclass(frozen=True)
class Result:
    """Scored records emitted by a scorer process.

    Each record carries both scoring variants produced in a single
    evaluation: the functional-group aware score and the functional-group
    agnostic score (see :class:`~chemcensor.chemcensor.ScoreResult`).

    :param batch_id: Id propagated from the originating :class:`ScoreTask`.
    :type batch_id: int
    :param items: Tuple of
        ``(idx, raw_smiles, score_with_fg, score_without_fg)``.
    :type items: tuple[tuple[int, str, float, float], ...]
    """

    batch_id: int
    items: tuple[tuple[int, str, float, float], ...]
