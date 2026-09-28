from __future__ import annotations

import logging
import multiprocessing as mp
import queue as queue_mod
import threading
from collections.abc import Iterable
from collections.abc import Mapping
from os import PathLike
from typing import Any

from ..db.stamp import validate_db_version
from .composer_proc import run_composer_worker
from .config import ParallelConfig
from .errors import MapperCrashedError
from .errors import ScorerCrashedError
from .io import mapped_dump_shards
from .mapper_proc import run_mapper
from .messages import CompositionResult
from .orchestrator import _DEFAULT_JOIN_TIMEOUT
from .orchestrator import _drain_queue
from .orchestrator import _hide_gpu_from_mappers
from .orchestrator import _reader_thread
from .orchestrator import _scorers_gpu_hidden
from .orchestrator import _shutdown_processes
from .orchestrator import _signal_workers_after_mappers
from .orchestrator import _watchdog
from .scorer_proc import _RECYCLE_EXIT_CODE


logger = logging.getLogger(__name__)


def _db_writer_thread(
    result_queue: Any,
    *,
    output_path: str | PathLike,
    db_version: str,
    idx_to_doc: Mapping[int, str],
    idx_to_source: Mapping[int, str],
    idx_to_virtual: Mapping[int, bool],
    n_workers: int,
    total_hint: int | None,
    progress: bool,
    stop_event: threading.Event,
    error_event: threading.Event,
) -> None:
    """Aggregate worker records into one database, then post-process and dump.

    Owns the single writable in-memory :class:`~chemcensor.db.manager.DBManager`
    (SQLite is not safe to share across processes, and the aggregation is the
    cheap, inherently serial step). Consumes :class:`CompositionResult` messages
    until every worker has emitted its terminal ``None`` sentinel, applying each
    record via the shared aggregation helpers; the reaction's ``document_id``,
    ``source``, and ``is_virtual`` are looked up by ``idx``. On a clean finish
    it runs the distributivity post-processing, writes the ``db_version`` build
    stamp, and dumps the database to ``output_path``. If ``error_event`` fired,
    the partial database is *not* written and therefore never stamped.
    """
    # Imported here (not at module load) so the parent process pays the
    # ``chemcensor`` import cost only when actually composing.
    from dataclasses import replace

    from chemcensor.composition.records import apply_reaction_record
    from chemcensor.composition.records import run_distributivity_postprocessing
    from chemcensor.db import DBManager
    from chemcensor.db.stamp import build_stamp

    manager = DBManager()

    pbar = None
    if progress:
        try:
            from tqdm import tqdm

            pbar = tqdm(total=total_hint, unit="rxn")
        except ImportError:
            logger.info("tqdm not installed; progress bar disabled")
            pbar = None

    workers_done = 0
    try:
        while workers_done < n_workers:
            if error_event.is_set():
                break
            try:
                msg = result_queue.get(timeout=1.0)
            except queue_mod.Empty:
                continue

            if msg is None:
                workers_done += 1
                continue
            assert isinstance(msg, CompositionResult)

            for idx, record in msg.items:
                record_with_meta = replace(
                    record,
                    source=idx_to_source.get(idx, record.source),
                    is_virtual=idx_to_virtual.get(idx, record.is_virtual),
                )
                apply_reaction_record(
                    manager,
                    record_with_meta,
                    idx_to_doc.get(idx, ""),
                )

            if pbar is not None:
                pbar.update(len(msg.items))

        if not error_event.is_set():
            run_distributivity_postprocessing(manager)
            stamp = build_stamp(db_version)
            manager.write_metadata(stamp)
            manager.dump(output_path)
            logger.info(
                "Database saved to %s (db_version=%s)",
                output_path,
                stamp["db_version"],
            )
    except Exception as e:
        logger.exception("DB writer thread failed: %s", e)
        error_event.set()
    finally:
        if pbar is not None:
            pbar.close()
        stop_event.set()


def run_composition(
    source: Iterable[tuple[int, str]],
    *,
    output_path: str | PathLike,
    idx_to_doc: Mapping[int, str],
    config: ParallelConfig,
    db_version: str,
    total_hint: int | None = None,
    idx_to_source: Mapping[int, str] | None = None,
    idx_to_virtual: Mapping[int, bool] | None = None,
    mapped_dump_dir: str | PathLike | None = None,
) -> None:
    """Run the parallel composition pipeline end-to-end.

    Mirrors :func:`chemcensor.parallel.orchestrator.run` but replaces the
    scorer workers with composer workers and the result-sink writer with a
    database writer that owns the single in-memory store. Blocks until the
    input is exhausted (and the database dumped) or an error occurs.

    :param source: Iterable yielding ``(idx, raw_smiles)`` records. For the
        fake-mapper path ``raw_smiles`` is the precomputed atom-mapped SMILES.
    :type source: Iterable[tuple[int, str]]
    :param output_path: Destination path for the composed SQLite database.
    :type output_path: str | PathLike
    :param idx_to_doc: Mapping from input ``idx`` to ``document_id``; populated
        by the CSV source before each row is enqueued, so the writer reads it
        race-free.
    :type idx_to_doc: Mapping[int, str]
    :param config: Resolved (or raw — auto-scaled here) configuration. The
        scoring-only fields (``find_exact_match``, ``checkpoint_interval``) are
        ignored.
    :type config: ParallelConfig
    :param db_version: Catalog version label stored in the composed database.
    :type db_version: str
    :param total_hint: Total number of records, if known (progress bar only).
    :type total_hint: int | None
    :param idx_to_source: Optional mapping from ``idx`` to provenance ``source``
        (e.g. CSV ``source_id`` for virtual reactions).
    :type idx_to_source: Mapping[int, str] | None
    :param idx_to_virtual: Optional mapping from ``idx`` to per-row
        ``is_virtual``.
    :type idx_to_virtual: Mapping[int, bool] | None
    :param mapped_dump_dir: When set, each mapper streams its atom-mapped
        reaction SMILES to a shard in this directory (see
        :func:`~chemcensor.parallel.io.mapped_dump_shards`). The caller merges
        the shards once the run has finished successfully.
    :type mapped_dump_dir: str | PathLike | None
    :raises MapperCrashedError: A mapper subprocess died.
    :raises ScorerCrashedError: A composer worker crashed (a clean
        ``maxtasksperchild`` recycle is respawned and is not an error).
    """
    # Validated before any process is spawned: the writer thread stamps the
    # database at the very end, and a bad label there would surface as a dead
    # writer rather than a clear error.
    validate_db_version(db_version)

    if idx_to_source is None:
        idx_to_source = {}
    if idx_to_virtual is None:
        idx_to_virtual = {}
    cfg = config.resolved()
    assert (
        cfg.n_workers is not None
        and cfg.mapper_threads is not None
        and cfg.n_mappers is not None
    )

    ctx = mp.get_context("spawn")
    map_queue: Any = ctx.Queue(maxsize=cfg.map_queue_size)
    score_queue: Any = ctx.Queue(maxsize=cfg.score_queue_size)
    result_queue: Any = ctx.Queue(maxsize=cfg.result_queue_size)

    stop_event = threading.Event()
    error_event = threading.Event()

    dump_shards = (
        mapped_dump_shards(mapped_dump_dir, cfg.n_mappers)
        if mapped_dump_dir is not None
        else None
    )

    mapper_procs = [
        ctx.Process(
            target=run_mapper,
            name=f"chemcensor-mapper-{i}",
            kwargs=dict(
                map_queue=map_queue,
                score_queue=score_queue,
                threads=cfg.mapper_threads,
                rxnmapper_batch_size=cfg.mapper_internal_batch_size,
                use_fake_mapper=cfg.use_fake_mapper,
                use_cpu=cfg.use_cpu,
                validate_input=cfg.validate_input,
                mapped_dump_path=dump_shards[i] if dump_shards is not None else None,
            ),
            daemon=True,
        )
        for i in range(cfg.n_mappers)
    ]

    def _new_worker(i: int) -> Any:
        """Build (but do not start) a composer worker process for slot ``i``."""
        return ctx.Process(
            target=run_composer_worker,
            name=f"chemcensor-composer-{i}",
            kwargs=dict(
                score_queue=score_queue,
                result_queue=result_queue,
                max_center_type=cfg.max_center_type,
                maxtasksperchild=cfg.maxtasksperchild,
                extra_env=cfg.worker_extra_env or None,
                use_fake_mapper=cfg.use_fake_mapper,
                validate_input=cfg.validate_input,
                check_skeleton_conservation=cfg.check_skeleton_conservation,
                check_static_stereo=cfg.check_static_stereo,
            ),
            daemon=True,
        )

    def _spawn_worker(i: int) -> Any:
        """Build + start a replacement composer worker for slot ``i``.

        Used by the watchdog to recycle a worker that hit
        ``maxtasksperchild``. Workers are always CPU-only, so the GPU stays
        hidden regardless of the mapper mode.
        """
        proc = _new_worker(i)
        with _scorers_gpu_hidden(cfg.worker_extra_env):
            proc.start()
        return proc

    worker_procs = [_new_worker(i) for i in range(cfg.n_workers)]

    # Start the mappers first so they inherit the real ``CUDA_VISIBLE_DEVICES``
    # and keep the GPU; composer workers are CPU-only (RDKit / NumPy) and are
    # started with the GPU hidden. Fake-mapper and ``use_cpu`` mappers never
    # need the GPU, so they start with it hidden as well.
    if _hide_gpu_from_mappers(cfg):
        with _scorers_gpu_hidden(cfg.worker_extra_env):
            for mp_proc in mapper_procs:
                mp_proc.start()
            for wp in worker_procs:
                wp.start()
    else:
        for mp_proc in mapper_procs:
            mp_proc.start()
        with _scorers_gpu_hidden(cfg.worker_extra_env):
            for wp in worker_procs:
                wp.start()

    reader = threading.Thread(
        target=_reader_thread,
        name="chemcensor-reader",
        kwargs=dict(
            source=source,
            map_queue=map_queue,
            batch_size=cfg.batch_size,
            n_mappers=cfg.n_mappers,
            stop_event=stop_event,
            error_event=error_event,
        ),
        daemon=True,
    )
    writer = threading.Thread(
        target=_db_writer_thread,
        name="chemcensor-db-writer",
        kwargs=dict(
            result_queue=result_queue,
            output_path=output_path,
            db_version=db_version,
            idx_to_doc=idx_to_doc,
            idx_to_source=idx_to_source,
            idx_to_virtual=idx_to_virtual,
            n_workers=cfg.n_workers,
            total_hint=total_hint,
            progress=cfg.progress,
            stop_event=stop_event,
            error_event=error_event,
        ),
        daemon=True,
    )
    watchdog = threading.Thread(
        target=_watchdog,
        name="chemcensor-watchdog",
        kwargs=dict(
            mapper_procs=mapper_procs,
            scorer_procs=worker_procs,
            respawn_scorer=_spawn_worker,
            stop_event=stop_event,
            error_event=error_event,
        ),
        daemon=True,
    )
    mapper_completion = threading.Thread(
        target=_signal_workers_after_mappers,
        name="chemcensor-mapper-completion",
        kwargs=dict(
            mapper_procs=mapper_procs,
            score_queue=score_queue,
            n_workers=cfg.n_workers,
            stop_event=stop_event,
            error_event=error_event,
        ),
        daemon=True,
    )

    reader.start()
    writer.start()
    watchdog.start()
    mapper_completion.start()

    try:
        writer.join()
        reader.join(timeout=_DEFAULT_JOIN_TIMEOUT)
        mapper_completion.join(timeout=_DEFAULT_JOIN_TIMEOUT)
        for mp_proc in mapper_procs:
            mp_proc.join(timeout=_DEFAULT_JOIN_TIMEOUT)
        for wp in worker_procs:
            wp.join(timeout=_DEFAULT_JOIN_TIMEOUT)
    finally:
        stop_event.set()
        _shutdown_processes([*mapper_procs, *worker_procs])
        _drain_queue(map_queue)
        _drain_queue(score_queue)
        _drain_queue(result_queue)

    if error_event.is_set():
        dead_mappers = [
            mp_proc for mp_proc in mapper_procs if mp_proc.exitcode not in (0, None)
        ]
        if dead_mappers:
            raise MapperCrashedError(
                "Mapper subprocesses died: "
                + ", ".join(f"{p.name}={p.exitcode}" for p in dead_mappers)
            )
        dead = [
            wp
            for wp in worker_procs
            if wp.exitcode not in (0, None, _RECYCLE_EXIT_CODE)
        ]
        if dead:
            raise ScorerCrashedError(
                "Composer worker subprocesses died: "
                + ", ".join(f"{wp.name}={wp.exitcode}" for wp in dead)
            )
        # Generic fallback if the error came from a thread (e.g. the writer).
        raise ScorerCrashedError("Parallel composition aborted due to an error")
