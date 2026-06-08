from __future__ import annotations

from collections.abc import Iterable
from os import PathLike
from pathlib import Path
from typing import Literal
from typing import overload

from . import checkpoint as ckpt_mod
from .config import ParallelConfig
from .errors import CheckpointCorruptedError
from .errors import MapperCrashedError
from .errors import ParallelError
from .errors import ScorerCrashedError
from .io import CsvSink
from .io import iter_csv_smiles
from .io import ListSink
from .orchestrator import run as _run_pipeline


__all__ = [
    "ParallelConfig",
    "ParallelError",
    "MapperCrashedError",
    "ScorerCrashedError",
    "CheckpointCorruptedError",
    "score_batch",
    "score_file",
]


@overload
def score_batch(
    smiles: Iterable[str],
    *,
    db_path: str | PathLike,
    config: ParallelConfig | None = ...,
    return_dict: Literal[False] = False,
) -> list[float]: ...


@overload
def score_batch(
    smiles: Iterable[str],
    *,
    db_path: str | PathLike,
    config: ParallelConfig | None = ...,
    return_dict: Literal[True],
) -> dict[int, float]: ...


def score_batch(
    smiles: Iterable[str],
    *,
    db_path: str | PathLike,
    config: ParallelConfig | None = None,
    return_dict: bool = False,
) -> list[float] | dict[int, float]:
    """Score an in-memory iterable of reaction SMILES.

    Materialises the iterable to fix indices, then runs the pipeline
    and re-orders the results so the returned list aligns with the
    input.  For very large inputs prefer :func:`score_file`.

    :param smiles: Iterable of raw reaction SMILES strings.
    :type smiles: Iterable[str]
    :param db_path: Path to the SQLite reaction-centers database.
    :type db_path: str | PathLike
    :param config: Pipeline configuration. ``None`` uses defaults
        (auto-scaling on CPU count).
    :type config: ParallelConfig | None
    :param return_dict: When ``True``, return ``dict[int, float]``
        keyed by the input position; when ``False`` (default) return
        ``list[float]`` in the original input order.
    :type return_dict: bool
    :return: Per-input scores either as a list (input order) or as a
        dict keyed by input index.
    :rtype: list[float] | dict[int, float]
    """
    cfg = (config or ParallelConfig()).resolved()
    smiles_list = list(smiles)
    source = list(enumerate(smiles_list))
    sink = ListSink()

    _run_pipeline(
        source=iter(source),
        sink=sink,
        db_path=db_path,
        config=cfg,
        total_hint=len(smiles_list),
    )

    if return_dict:
        return {idx: score for idx, _smi, score in sink.items}

    failed_default = _failed_score()
    out: list[float] = [failed_default] * len(smiles_list)
    for idx, _smi, score in sink.items:
        if 0 <= idx < len(out):
            out[idx] = score
    return out


def score_file(
    input_path: str | PathLike,
    output_path: str | PathLike,
    *,
    db_path: str | PathLike,
    smiles_column: str = "reaction_smiles",
    config: ParallelConfig | None = None,
    checkpoint_path: str | PathLike | None = None,
    total_hint: int | None = None,
) -> None:
    """Score a CSV file of reactions and stream results to another CSV.

    The output file gains three columns: ``idx`` (the 0-based input
    row index), ``smiles`` (the raw input SMILES) and ``score``.  Rows
    are written in the order workers complete them — *not* input
    order; sort by ``idx`` post-hoc if you need it.

    When ``checkpoint_path`` is provided the writer periodically
    flushes a small JSON file with the highest contiguously-completed
    input index *and* the set of already-completed out-of-order indices
    above it.  On resume, the reader skips every already-completed row
    (contiguous prefix + the out-of-order set) and the writer appends to
    the existing output CSV, so no ``idx`` is scored or written twice.

    :param input_path: Source CSV (must contain ``smiles_column``).
    :type input_path: str | PathLike
    :param output_path: Destination CSV (created or appended to).
    :type output_path: str | PathLike
    :param db_path: Path to the SQLite reaction-centers database.
    :type db_path: str | PathLike
    :param smiles_column: Name of the column holding reaction SMILES.
    :type smiles_column: str
    :param config: Pipeline configuration. ``None`` uses defaults.
    :type config: ParallelConfig | None
    :param checkpoint_path: Optional ``.ckpt`` path for resumable runs.
    :type checkpoint_path: str | PathLike | None
    :param total_hint: Override the row count used for the progress
        bar; pass when the count is known upfront and you want to
        avoid scanning the input file.
    :type total_hint: int | None
    """
    cfg = (config or ParallelConfig()).resolved()

    state = (
        ckpt_mod.load(checkpoint_path)
        if checkpoint_path is not None
        else ckpt_mod.CheckpointState()
    )

    source = iter_csv_smiles(
        input_path,
        smiles_column=smiles_column,
        skip_until_idx=state.last_contiguous_idx,
        skip_indices=state.completed_above,
    )

    if total_hint is None:
        total_hint = _count_rows(input_path)

    append_mode = state.last_contiguous_idx >= 0 and Path(output_path).exists()
    with CsvSink(output_path, append=append_mode) as sink:
        _run_pipeline(
            source=source,
            sink=sink,
            db_path=db_path,
            config=cfg,
            total_hint=total_hint,
            checkpoint_path=checkpoint_path,
            initial_state=state,
        )


def _count_rows(path: str | PathLike) -> int | None:
    """Best-effort fast count of data rows in a CSV file.

    Used only to populate the progress bar; returns ``None`` on any
    error so the writer thread can fall back to an unbounded bar.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            # Subtract header row.
            return max(0, sum(1 for _ in fh) - 1)
    except OSError:
        return None


def _failed_score() -> float:
    """Return ``ScoringConfig.failed_reaction_scoring.value`` lazily.

    Lazy import keeps the parallel package's import surface small for
    callers that only need the public symbols.
    """
    from chemcensor.configs.scoring_configs import ScoringConfig

    return float(ScoringConfig.failed_reaction_scoring.value)
