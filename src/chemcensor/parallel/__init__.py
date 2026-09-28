from __future__ import annotations

import csv
import gc
import logging
import shutil
import sys
import tempfile
from collections.abc import Iterable
from collections.abc import Iterator
from contextlib import contextmanager
from os import PathLike
from pathlib import Path
from threading import RLock
from typing import Literal
from typing import overload
from typing import TYPE_CHECKING

from . import checkpoint as ckpt_mod
from ..db.download import resolve_database_path
from .config import ParallelConfig
from .errors import CheckpointCorruptedError
from .errors import MalformedCsvError
from .errors import MapperCrashedError
from .errors import OutputSchemaMismatchError
from .errors import ParallelError
from .errors import ScorerCrashedError
from .io import CsvSink
from .io import existing_mapped_dump_shards
from .io import iter_csv_smiles
from .io import ListSink
from .io import read_mapped_dump
from .io import write_csv_with_extra_column
from .messages import ScoredItem
from .orchestrator import run as _run_pipeline


if TYPE_CHECKING:
    from chemcensor.chemcensor import ChemCensor
    from chemcensor.chemcensor import ScoreResult


logger = logging.getLogger(__name__)

_IN_PROCESS_LOCK = RLock()
_IN_PROCESS_CENSOR: ChemCensor | None = None
_IN_PROCESS_KEY: tuple[object, ...] | None = None


__all__ = [
    "ParallelConfig",
    "ParallelError",
    "MapperCrashedError",
    "ScorerCrashedError",
    "CheckpointCorruptedError",
    "MalformedCsvError",
    "OutputSchemaMismatchError",
    "score_batch",
    "score_file",
    "compose_file",
    "release_in_process_scorer",
]


@overload
def score_batch(
    smiles: Iterable[str],
    *,
    db_path: str | PathLike | None = None,
    config: ParallelConfig | None = ...,
    return_dict: Literal[False] = False,
) -> list["ScoreResult"]: ...


@overload
def score_batch(
    smiles: Iterable[str],
    *,
    db_path: str | PathLike | None = None,
    config: ParallelConfig | None = ...,
    return_dict: Literal[True],
) -> dict[int, "ScoreResult"]: ...


def score_batch(
    smiles: Iterable[str],
    *,
    db_path: str | PathLike | None = None,
    config: ParallelConfig | None = None,
    return_dict: bool = False,
) -> list["ScoreResult"] | dict[int, "ScoreResult"]:
    """Score an in-memory iterable of reaction SMILES.

    Materialises the iterable to fix indices. Batches at or below
    :attr:`ParallelConfig.in_process_batch_threshold` reuse one guarded,
    file-backed :class:`~chemcensor.chemcensor.ChemCensor`; larger batches run
    the multiprocessing pipeline. The small-batch path loads rxnmapper in the
    caller process and retains it for reuse; call
    :func:`release_in_process_scorer` to release it deliberately. For very
    large inputs prefer :func:`score_file`, which always uses multiprocessing.

    Each entry is a :class:`~chemcensor.chemcensor.ScoreResult` holding both
    scoring variants and FG-precedent provenance, produced in a single pass.

    :param smiles: Iterable of raw reaction SMILES strings.
    :type smiles: Iterable[str]
    :param db_path: Path to the SQLite reaction-centers database. When omitted,
        download and reuse the current default database from Hugging Face.
    :type db_path: str | PathLike | None
    :param config: Pipeline configuration. ``None`` uses defaults
        (auto-scaling on CPU count).
    :type config: ParallelConfig | None
    :param return_dict: When ``True``, return ``dict[int, ScoreResult]``
        keyed by the input position; when ``False`` (default) return
        ``list[ScoreResult]`` in the original input order.
    :type return_dict: bool
    :return: Per-input results either as a list (input order) or as a
        dict keyed by input index.
    :rtype: list[ScoreResult] | dict[int, ScoreResult]
    """
    from chemcensor.chemcensor import FailureReason
    from chemcensor.chemcensor import FailureStage
    from chemcensor.chemcensor import ScoreResult

    cfg = (config or ParallelConfig()).resolved()
    smiles_list = list(smiles)
    if not smiles_list:
        return {} if return_dict else []
    resolved_db_path = resolve_database_path(db_path)

    use_in_process = (
        cfg.in_process_batch_threshold > 0
        and len(smiles_list) <= cfg.in_process_batch_threshold
        and not cfg.worker_extra_env
    )
    if use_in_process:
        results = _score_batch_in_process(
            smiles_list,
            db_path=resolved_db_path,
            config=cfg,
        )
        if return_dict:
            return dict(enumerate(results))
        return results

    source = list(enumerate(smiles_list))
    sink = ListSink()

    with _multiprocessing_guard():
        _run_pipeline(
            source=iter(source),
            sink=sink,
            db_path=resolved_db_path,
            config=cfg,
            total_hint=len(smiles_list),
        )

    def _to_score_result(item: ScoredItem) -> "ScoreResult":
        failure_reason = (
            FailureReason(
                stage=FailureStage(item[8]),
                category=item[9],
                message=item[10],
            )
            if item[8]
            else None
        )
        return ScoreResult(
            with_functional_groups=item[2],
            without_functional_groups=item[3],
            all_fgs_precedents_are_real=item[4],
            total_number_of_fgs=item[5],
            number_of_fgs_covered_by_virtual_precedents=item[6],
            all_center_precedents_are_real=item[7],
            failure_reason=failure_reason,
        )

    if return_dict:
        return {item[0]: _to_score_result(item) for item in sink.items}

    failed_default = _failed_score()
    out: list[ScoreResult] = [
        ScoreResult.uniform(
            failed_default,
            failure_reason=FailureReason(
                stage=FailureStage.PROCESSING,
                category="MissingParallelResult",
                message="Parallel scoring did not return a result.",
            ),
        )
        for _ in range(len(smiles_list))
    ]
    for item in sink.items:
        idx = item[0]
        if 0 <= idx < len(out):
            out[idx] = _to_score_result(item)
    return out


def _score_batch_in_process(
    smiles: list[str],
    *,
    db_path: str | PathLike,
    config: ParallelConfig,
) -> list["ScoreResult"]:
    """Score a small batch through the guarded process-local ChemCensor."""
    with _IN_PROCESS_LOCK:
        censor = _get_in_process_censor(db_path, config)
        from chemcensor.basic import Reaction

        if not config.use_fake_mapper:
            return censor.evaluate_batch(
                [
                    Reaction(reaction_smiles=reaction_smiles)
                    for reaction_smiles in smiles
                ]
            )

        from chemcensor.basic import SENTINEL
        from chemcensor.processing.errors import ProcessingError
        from chemcensor.processing.utils import (
            reaction_from_precomputed_mapping,
        )

        reactions: list[Reaction] = []
        for mapped_smiles in smiles:
            try:
                reactions.append(reaction_from_precomputed_mapping(mapped_smiles))
            except ProcessingError:
                reactions.append(SENTINEL)
        return censor.evaluate_batch(reactions)


def _release_in_process_censor() -> None:
    """Drop the cached scorer and release cached CUDA allocations when loaded."""
    global _IN_PROCESS_CENSOR
    global _IN_PROCESS_KEY

    cached_censor = _IN_PROCESS_CENSOR
    _IN_PROCESS_CENSOR = None
    _IN_PROCESS_KEY = None
    del cached_censor
    gc.collect()

    torch = sys.modules.get("torch")
    cuda = getattr(torch, "cuda", None) if torch is not None else None
    if cuda is not None and cuda.is_initialized():
        cuda.empty_cache()


def release_in_process_scorer() -> None:
    """Release the process-local scorer cached by small ``score_batch`` calls.

    The call waits for any active in-process scoring or multiprocessing
    transition using the same cache, then drops the cached
    :class:`~chemcensor.chemcensor.ChemCensor` and releases initialized CUDA
    cache allocations. A later small ``score_batch`` call creates a new scorer.
    """
    with _IN_PROCESS_LOCK:
        _release_in_process_censor()


@contextmanager
def _multiprocessing_guard() -> Iterator[None]:
    """Prevent rebuilding the cached mapper while subprocess mappers run."""
    with _IN_PROCESS_LOCK:
        _release_in_process_censor()
        yield


def _get_in_process_censor(
    db_path: str | PathLike,
    config: ParallelConfig,
) -> "ChemCensor":
    """Return the single cached scorer, rebuilding it when identity changes."""
    from chemcensor import ChemCensor
    from chemcensor import ChemCensorConfig

    global _IN_PROCESS_CENSOR
    global _IN_PROCESS_KEY

    path = Path(db_path).resolve()
    try:
        stat = path.stat()
        database_identity: tuple[object, ...] = (
            str(path),
            stat.st_dev,
            stat.st_ino,
            stat.st_size,
            stat.st_mtime_ns,
        )
    except OSError:
        database_identity = (str(path),)

    key = (
        *database_identity,
        config.max_center_type,
        config.find_exact_match,
        config.mapper_internal_batch_size,
        config.mapper_threads,
        config.use_fake_mapper,
        config.use_cpu,
        config.validate_input,
        config.check_skeleton_conservation,
        config.check_static_stereo,
    )
    if _IN_PROCESS_CENSOR is None or _IN_PROCESS_KEY != key:
        censor_config = ChemCensorConfig(
            max_center_type=config.max_center_type,
            find_exact_match=config.find_exact_match,
            use_fake_mapper=config.use_fake_mapper,
            use_cpu=config.use_cpu,
            mapper_batch_size=config.mapper_internal_batch_size,
            mapper_n_jobs=config.mapper_threads or 1,
            validate_input=config.validate_input,
            check_skeleton_conservation=config.check_skeleton_conservation,
            check_static_stereo=config.check_static_stereo,
        )
        _IN_PROCESS_CENSOR = ChemCensor.open(path, config=censor_config)
        _IN_PROCESS_KEY = key
    return _IN_PROCESS_CENSOR


def score_file(
    input_path: str | PathLike,
    output_path: str | PathLike,
    *,
    db_path: str | PathLike | None = None,
    smiles_column: str = "reaction_smiles",
    config: ParallelConfig | None = None,
    checkpoint_path: str | PathLike | None = None,
    total_hint: int | None = None,
) -> None:
    """Score a CSV file of reactions and stream results to another CSV.

    The output file gains columns: ``idx`` (the 0-based input row
    index), ``smiles`` (the raw input SMILES), ``score_with_fg`` (score
    requiring the functional-group sub-signature to match),
    ``score_without_fg`` (score on reaction-center presence only), plus
    FG- and center-precedent provenance
    (``all_fgs_precedents_are_real``, ``total_number_of_fgs``,
    ``number_of_fgs_covered_by_virtual_precedents``,
    ``all_center_precedents_are_real``, ``failure_stage``,
    ``failure_category``, ``failure_message``). Rows are written in the order
    workers complete them — *not* input order; sort by ``idx`` post-hoc
    if you need it.

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
    :param db_path: Path to the SQLite reaction-centers database. When omitted,
        download and reuse the current default database from Hugging Face.
    :type db_path: str | PathLike | None
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
    resolved_db_path = resolve_database_path(db_path)

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
    with _multiprocessing_guard():
        with CsvSink(
            output_path,
            append=append_mode,
            include_canonical_smiles=cfg.include_canonical_smiles,
        ) as sink:
            _run_pipeline(
                source=source,
                sink=sink,
                db_path=resolved_db_path,
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


def _iter_compose_csv(
    path: str | PathLike,
    *,
    smiles_column: str,
    document_id_column: str,
    idx_to_doc: dict[int, str],
    source_column: str = "source_id",
    idx_to_source: dict[int, str] | None = None,
    is_virtual_column: str = "is_virtual",
    idx_to_virtual: dict[int, bool] | None = None,
) -> Iterator[tuple[int, str]]:
    """Yield ``(idx, smiles)`` pairs and record each row's metadata.

    ``idx`` is the 0-based row number (header excluded), matching
    :func:`~chemcensor.parallel.io.iter_csv_smiles`. The ``document_id``,
    ``source``, and ``is_virtual`` values are written into the corresponding
    maps *before* the row is yielded — and therefore before it is enqueued —
    so the DB-writer thread can read them back by ``idx`` without a race.
    Rows whose ``smiles_column`` value is empty are skipped silently.

    :param path: Path to the input CSV file.
    :type path: str | PathLike
    :param smiles_column: Column holding reaction SMILES (precomputed
        atom-mapped SMILES when the fake mapper is used).
    :type smiles_column: str
    :param document_id_column: Column holding the document ID.
    :type document_id_column: str
    :param idx_to_doc: Mapping populated with ``idx -> document_id`` as a side
        effect.
    :type idx_to_doc: dict[int, str]
    :param source_column: CSV column for provenance (e.g. ``source_id``).
    :type source_column: str
    :param idx_to_source: Mapping populated with ``idx -> source``.
    :type idx_to_source: dict[int, str] | None
    :param is_virtual_column: CSV column for the per-row virtual flag.
    :type is_virtual_column: str
    :param idx_to_virtual: Mapping populated with ``idx -> is_virtual``.
    :type idx_to_virtual: dict[int, bool] | None
    :return: Iterator of ``(idx, smiles)`` pairs.
    :rtype: Iterator[tuple[int, str]]
    :raises KeyError: If a required column is missing from the CSV header.
    """
    from chemcensor.composition.composer import parse_csv_bool

    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames
        if fieldnames is None or smiles_column not in fieldnames:
            raise KeyError(
                f"Column {smiles_column!r} not found in {path} (have: {fieldnames})"
            )
        if document_id_column not in fieldnames:
            raise KeyError(
                f"Column {document_id_column!r} not found in {path} "
                f"(have: {fieldnames})"
            )
        has_source = source_column in fieldnames
        has_virtual = is_virtual_column in fieldnames
        for idx, row in enumerate(reader):
            smiles = (row.get(smiles_column) or "").strip()
            if not smiles:
                continue
            idx_to_doc[idx] = (row.get(document_id_column) or "").strip()
            if idx_to_source is not None:
                idx_to_source[idx] = (
                    (row.get(source_column) or "").strip() if has_source else ""
                )
            if idx_to_virtual is not None:
                idx_to_virtual[idx] = (
                    parse_csv_bool(row.get(is_virtual_column)) if has_virtual else False
                )
            yield idx, smiles


def compose_file(
    input_path: str | PathLike,
    output_path: str | PathLike,
    *,
    db_version: str,
    reaction_smiles_column: str = "cleaned_rxn",
    document_id_column: str = "document_id",
    config: ParallelConfig | None = None,
    total_hint: int | None = None,
    source_column: str = "source_id",
    is_virtual_column: str = "is_virtual",
    save_mapped_path: str | PathLike | None = None,
    mapped_column: str = "mapped_rxn",
) -> None:
    """Compose a reaction-center SQLite database from a CSV, in parallel.

    The parallel analogue of
    :meth:`chemcensor.composition.composer.ReactionCenterDBComposer.compose`:
    reactions are mapped and processed across several subprocesses, while a
    single writer thread aggregates every extracted center into one in-memory
    database and dumps it to ``output_path``. Because all aggregation steps are
    order-independent, the result is equivalent to a serial build.

    Set ``config.use_fake_mapper = True`` when ``reaction_smiles_column`` holds
    *precomputed* atom-mapped reaction SMILES; rxnmapper (and the GPU) are then
    bypassed entirely.

    Only a subset of :class:`ParallelConfig` applies to composition. The
    scoring-only fields ``find_exact_match``, ``checkpoint_interval`` and
    ``in_process_batch_threshold`` are ignored (composition has no resume or
    in-memory batch-scoring path).

    :param input_path: Source CSV (must contain ``reaction_smiles_column``,
        ``document_id_column``, ``is_virtual_column``, and ``source_column``).
    :type input_path: str | PathLike
    :param output_path: Destination path for the SQLite database.
    :type output_path: str | PathLike
    :param db_version: Catalog version label for this build (e.g. ``U3-1``),
        stored inside the database so consumers can identify the build.
    :type db_version: str
    :param reaction_smiles_column: Column holding reaction SMILES.
    :type reaction_smiles_column: str
    :param document_id_column: Column holding the document ID.
    :type document_id_column: str
    :param config: Pipeline configuration. ``None`` uses defaults (auto-scaling
        on CPU count).
    :type config: ParallelConfig | None
    :param total_hint: Override the row count used for the progress bar.
    :type total_hint: int | None
    :param source_column: CSV column copied into ``reactions.source``.
    :type source_column: str
    :param is_virtual_column: CSV column with the per-row virtual flag.
    :type is_virtual_column: str
    :param save_mapped_path: When set, the atom maps computed during this run
        are written to this CSV as ``mapped_column`` — every other column of
        ``input_path`` is copied over unchanged. Pass ``input_path`` to update
        the input in place. A later run can then read that column with
        ``config.use_fake_mapper = True`` and skip rxnmapper entirely. The CSV
        is only written after a successful composition.
    :type save_mapped_path: str | PathLike | None
    :param mapped_column: Column name used by ``save_mapped_path``.
    :type mapped_column: str
    """
    from ..db.stamp import validate_db_version
    from .composition_orchestrator import run_composition

    # Checked before any row is read or worker spawned, so a missing label fails
    # in milliseconds rather than after a full composition.
    validate_db_version(db_version)

    cfg = (config or ParallelConfig()).resolved()

    if total_hint is None:
        total_hint = _count_rows(input_path)

    idx_to_doc: dict[int, str] = {}
    idx_to_source: dict[int, str] = {}
    idx_to_virtual: dict[int, bool] = {}
    source = _iter_compose_csv(
        input_path,
        smiles_column=reaction_smiles_column,
        document_id_column=document_id_column,
        idx_to_doc=idx_to_doc,
        source_column=source_column,
        idx_to_source=idx_to_source,
        is_virtual_column=is_virtual_column,
        idx_to_virtual=idx_to_virtual,
    )

    # The mappers stream their atom maps to per-process shards next to the
    # target CSV; they are merged into it only once the whole run succeeded,
    # so a partially mapped column can never be mistaken for a complete one.
    dump_dir: Path | None = None
    if save_mapped_path is not None:
        dump_dir = Path(
            tempfile.mkdtemp(
                prefix=".chemcensor-mapped-",
                dir=Path(save_mapped_path).parent,
            )
        )

    try:
        with _multiprocessing_guard():
            run_composition(
                source=source,
                output_path=output_path,
                idx_to_doc=idx_to_doc,
                config=cfg,
                db_version=db_version,
                total_hint=total_hint,
                idx_to_source=idx_to_source,
                idx_to_virtual=idx_to_virtual,
                mapped_dump_dir=dump_dir,
            )
    except BaseException:
        if dump_dir is not None:
            logger.warning(
                "Composition failed; atom maps collected so far are kept in %s",
                dump_dir,
            )
        raise

    if dump_dir is None or save_mapped_path is None:
        return

    # The database is already on disk at this point, so a failure here must not
    # read as a failed composition — say so, and leave the shards for a manual
    # merge.
    try:
        mapped = read_mapped_dump(existing_mapped_dump_shards(dump_dir))
        filled = write_csv_with_extra_column(
            input_path,
            save_mapped_path,
            column=mapped_column,
            values=mapped,
        )
    except BaseException:
        logger.error(
            "Composition succeeded and %s is complete, but the atom maps could "
            "not be written to %s; the raw shards are kept in %s",
            output_path,
            save_mapped_path,
            dump_dir,
        )
        raise

    logger.info(
        "Wrote %d atom-mapped reactions to column %r of %s",
        filled,
        mapped_column,
        save_mapped_path,
    )
    shutil.rmtree(dump_dir, ignore_errors=True)
