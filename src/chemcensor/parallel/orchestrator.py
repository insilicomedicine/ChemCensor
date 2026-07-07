from __future__ import annotations

import logging
import multiprocessing as mp
import os
import queue as queue_mod
import threading
import time
from collections.abc import Iterable
from collections.abc import Iterator
from contextlib import contextmanager
from os import PathLike
from typing import Any

from . import checkpoint as ckpt_mod
from .config import ParallelConfig
from .errors import MapperCrashedError
from .errors import ScorerCrashedError
from .io import ResultSink
from .mapper_proc import run_mapper
from .messages import MapTask
from .messages import Result
from .scorer_proc import _RECYCLE_EXIT_CODE
from .scorer_proc import run_scorer


logger = logging.getLogger(__name__)


_DEFAULT_JOIN_TIMEOUT = 30.0
_DEFAULT_WATCHDOG_INTERVAL = 2.0


_CUDA_ENV_VAR = "CUDA_VISIBLE_DEVICES"


@contextmanager
def _scorers_gpu_hidden(worker_extra_env: dict[str, str] | None) -> Iterator[None]:
    """Temporarily set ``CUDA_VISIBLE_DEVICES`` for spawning scorer workers.

    ``spawn`` children inherit a snapshot of the parent's ``os.environ`` at
    ``Process.start()``, so hiding the GPU here keeps the (already-started)
    mapper on the GPU while ensuring scorer workers never create a CUDA
    context. Restores the previous value on exit. If the caller pinned the
    GPU explicitly via ``worker_extra_env[CUDA_VISIBLE_DEVICES]`` that value
    is honoured instead of hiding the device.

    :param worker_extra_env: Per-worker environment overrides from the config.
    :type worker_extra_env: dict[str, str] | None
    """
    desired = (worker_extra_env or {}).get(_CUDA_ENV_VAR, "")
    previous = os.environ.get(_CUDA_ENV_VAR)
    os.environ[_CUDA_ENV_VAR] = desired
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop(_CUDA_ENV_VAR, None)
        else:
            os.environ[_CUDA_ENV_VAR] = previous


def _batched(
    source: Iterable[tuple[int, str]],
    batch_size: int,
) -> Iterator[list[tuple[int, str]]]:
    """Group ``(idx, smiles)`` pairs into batches of ``batch_size``.

    :param source: Iterable of ``(idx, smiles)`` records.
    :param batch_size: Number of records per emitted batch.
    :return: Iterator of lists; the final list may be shorter.
    """
    batch: list[tuple[int, str]] = []
    for item in source:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def _reader_thread(
    source: Iterable[tuple[int, str]],
    map_queue: Any,
    *,
    batch_size: int,
    n_mappers: int,
    stop_event: threading.Event,
    error_event: threading.Event,
) -> None:
    """Read input batches and put :class:`MapTask` messages on the queue.

    Honours ``stop_event`` and ``error_event`` so a downstream crash can
    abort the read cleanly.  Emits one ``None`` sentinel per mapper after
    the source is exhausted (each mapper consumes exactly one and the last
    one fans out further sentinels to the scorers). Sentinels are enqueued
    last, so the FIFO queue guarantees all real batches are picked up
    before any mapper stops.
    """
    try:
        for batch_id, batch in enumerate(_batched(source, batch_size)):
            if stop_event.is_set() or error_event.is_set():
                break
            map_queue.put(MapTask(batch_id=batch_id, items=tuple(batch)))
    except Exception as e:
        logger.exception("Reader thread failed: %s", e)
        error_event.set()
    finally:
        for _ in range(n_mappers):
            try:
                map_queue.put(None)
            except Exception:
                logger.debug(
                    "Reader: enqueue of end-of-stream sentinel failed", exc_info=True
                )


def _writer_thread(
    result_queue: Any,
    sink: ResultSink,
    *,
    n_workers: int,
    total_hint: int | None,
    progress: bool,
    checkpoint_path: str | PathLike | None,
    checkpoint_interval: int,
    initial_state: ckpt_mod.CheckpointState,
    stop_event: threading.Event,
    error_event: threading.Event,
) -> None:
    """Consume :class:`Result` messages until every scorer has signalled.

    Maintains the contiguous-completion index in
    :class:`~.checkpoint.CheckpointState` for efficient resume.  Writes
    are flushed batch-by-batch through ``sink``.
    """
    workers_done = 0
    completed_total = initial_state.completed_count
    # Number of completed records at the last checkpoint flush. Used to
    # decide *when* to checkpoint via a running delta — a modulo test on
    # ``completed_total`` would almost never fire, since the counter jumps
    # by ``batch_size`` and rarely lands exactly on a multiple of the
    # interval.
    last_ckpt_at = initial_state.completed_count
    last_contiguous = initial_state.last_contiguous_idx
    # Seed with the out-of-order rows completed by a previous run so the
    # contiguous frontier can advance over them (they are *not* re-fed by
    # the reader, so we must remember they are already done).
    pending_above: set[int] = set(initial_state.completed_above)

    pbar = None
    if progress:
        try:
            from tqdm import tqdm

            pbar = tqdm(total=total_hint, initial=completed_total, unit="rxn")
        except ImportError:
            logger.info("tqdm not installed; progress bar disabled")
            pbar = None

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
            assert isinstance(msg, Result)

            sink.write(msg.items)
            completed_total += len(msg.items)

            # Advance ``last_contiguous`` over any indices that fill the gap.
            for idx, *_rest in msg.items:
                if idx == last_contiguous + 1:
                    last_contiguous += 1
                    while last_contiguous + 1 in pending_above:
                        pending_above.discard(last_contiguous + 1)
                        last_contiguous += 1
                elif idx > last_contiguous + 1:
                    pending_above.add(idx)
                # idx <= last_contiguous: already accounted for; no-op.

            if pbar is not None:
                pbar.update(len(msg.items))

            if (
                checkpoint_path is not None
                and checkpoint_interval > 0
                and completed_total - last_ckpt_at >= checkpoint_interval
            ):
                ckpt_mod.save(
                    checkpoint_path,
                    ckpt_mod.CheckpointState(
                        last_contiguous_idx=last_contiguous,
                        completed_count=completed_total,
                        completed_above=frozenset(pending_above),
                    ),
                )
                last_ckpt_at = completed_total
    except Exception as e:
        logger.exception("Writer thread failed: %s", e)
        error_event.set()
    finally:
        if pbar is not None:
            pbar.close()
        if checkpoint_path is not None:
            try:
                ckpt_mod.save(
                    checkpoint_path,
                    ckpt_mod.CheckpointState(
                        last_contiguous_idx=last_contiguous,
                        completed_count=completed_total,
                        completed_above=frozenset(pending_above),
                    ),
                )
            except Exception as e:
                logger.warning("Final checkpoint flush failed: %s", e)
        stop_event.set()


def _watchdog(
    mapper_procs: list[Any],
    scorer_procs: list[Any],
    *,
    respawn_scorer: Any,
    stop_event: threading.Event,
    error_event: threading.Event,
) -> None:
    """Detect dead subprocesses; respawn recycled scorers, abort on crash.

    A scorer that hits ``maxtasksperchild`` exits cleanly with
    :data:`_RECYCLE_EXIT_CODE` *without* draining its end-of-stream
    sentinel, so the watchdog spawns a replacement (``respawn_scorer``)
    into the same slot. This keeps the number of live scorers — and hence
    the count of terminal ``None`` sentinels the writer expects — equal to
    ``n_workers`` and prevents the unscored tail from being silently
    dropped while the writer reports success.

    Any *other* non-zero exit code is treated as a crash: the watchdog
    sets ``error_event`` and the run fails fast. Unscored indices remain
    in the input and will be retried on resume.

    :param respawn_scorer: ``callable(slot_index) -> started Process`` used
        to replace a recycled scorer.
    """
    while not stop_event.is_set():
        for mp_proc in mapper_procs:
            if not mp_proc.is_alive() and mp_proc.exitcode not in (0, None):
                logger.error(
                    "Mapper subprocess %s died (exitcode=%s)",
                    mp_proc.name,
                    mp_proc.exitcode,
                )
                error_event.set()
                return
        for i, sp in enumerate(scorer_procs):
            if sp.is_alive():
                continue
            code = sp.exitcode
            if code == _RECYCLE_EXIT_CODE:
                # Clean maxtasksperchild recycle. Only respawn while the run
                # is still live; once stop/error is set the pipeline is
                # winding down and a replacement would just block on an empty
                # queue.
                if not (stop_event.is_set() or error_event.is_set()):
                    logger.debug(
                        "Scorer %s recycled (maxtasksperchild); respawning slot %d",
                        sp.name,
                        i,
                    )
                    scorer_procs[i] = respawn_scorer(i)
            elif code not in (0, None):
                logger.error(
                    "Scorer subprocess %s died (exitcode=%s)",
                    sp.name,
                    code,
                )
                error_event.set()
                return
        time.sleep(_DEFAULT_WATCHDOG_INTERVAL)


def run(
    source: Iterable[tuple[int, str]],
    sink: ResultSink,
    *,
    db_path: str | PathLike,
    config: ParallelConfig,
    total_hint: int | None = None,
    checkpoint_path: str | PathLike | None = None,
    initial_state: ckpt_mod.CheckpointState | None = None,
) -> None:
    """Run the parallel scoring pipeline end-to-end.

    The caller owns ``source`` (an iterable of ``(idx, raw_smiles)``)
    and ``sink`` (a :class:`ResultSink` instance).  This function
    blocks until the input is exhausted or an error occurs.

    :param source: Iterable yielding ``(idx, smiles)`` records.
    :type source: Iterable[tuple[int, str]]
    :param sink: Sink that receives
        ``(idx, smiles, score_with_fg, score_without_fg)`` results.
    :type sink: ResultSink
    :param db_path: Path to the SQLite reaction-centers database.
    :type db_path: str | PathLike
    :param config: Resolved (or raw — will be auto-scaled here)
        configuration.
    :type config: ParallelConfig
    :param total_hint: Total number of records, if known. Used only for
        the progress bar.
    :type total_hint: int | None
    :param checkpoint_path: When provided, periodic checkpoint writes
        record the highest contiguously-completed input index.
    :type checkpoint_path: str | PathLike | None
    :param initial_state: Existing checkpoint state from a previous run
        (skipping of input happens in the caller via
        :func:`~chemcensor.parallel.io.iter_csv_smiles`).
    :type initial_state: ckpt_mod.CheckpointState | None
    :raises MapperCrashedError: The mapper subprocess died.
    :raises ScorerCrashedError: A scorer subprocess crashed (a clean
        ``maxtasksperchild`` recycle is respawned and is not an error).
    """
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
    state = initial_state or ckpt_mod.CheckpointState()

    # Shared counter so the last mapper to finish emits the scorer
    # sentinels exactly once (see ``run_mapper``).
    mappers_remaining: Any = ctx.Value("i", cfg.n_mappers)

    mapper_procs = [
        ctx.Process(
            target=run_mapper,
            name=f"chemcensor-mapper-{i}",
            kwargs=dict(
                map_queue=map_queue,
                score_queue=score_queue,
                threads=cfg.mapper_threads,
                rxnmapper_batch_size=cfg.mapper_internal_batch_size,
                n_scorers=cfg.n_workers,
                mappers_remaining=mappers_remaining,
                use_fake_mapper=cfg.use_fake_mapper,
            ),
            daemon=True,
        )
        for i in range(cfg.n_mappers)
    ]

    def _new_scorer(i: int) -> Any:
        """Build (but do not start) a scorer process for slot ``i``."""
        return ctx.Process(
            target=run_scorer,
            name=f"chemcensor-scorer-{i}",
            kwargs=dict(
                score_queue=score_queue,
                result_queue=result_queue,
                db_path=str(db_path),
                max_center_type=cfg.max_center_type,
                find_exact_match=cfg.find_exact_match,
                maxtasksperchild=cfg.maxtasksperchild,
                extra_env=cfg.worker_extra_env or None,
                use_fake_mapper=cfg.use_fake_mapper,
            ),
            daemon=True,
        )

    def _spawn_scorer(i: int) -> Any:
        """Build + start a replacement scorer for slot ``i`` (GPU hidden).

        Used by the watchdog to recycle a worker that hit
        ``maxtasksperchild``. Scorers are always CPU-only, so we keep the
        GPU hidden regardless of the mapper mode.
        """
        proc = _new_scorer(i)
        with _scorers_gpu_hidden(cfg.worker_extra_env):
            proc.start()
        return proc

    scorer_procs = [_new_scorer(i) for i in range(cfg.n_workers)]

    # Start the mappers first so they inherit the real ``CUDA_VISIBLE_DEVICES``
    # and keep the GPU. Scorers are CPU-only (RDKit / NumPy); spawn them
    # with the GPU hidden so importing chemcensor → rxnmapper → torch does
    # not create a CUDA context per worker (each reserves hundreds of MB of
    # VRAM and adds start-up latency). ``spawn`` children snapshot the
    # parent's ``os.environ`` at ``start()``, so toggling it here is enough.
    # With the fake mapper there is no rxnmapper at all, so mappers are
    # CPU-only too and start with the GPU hidden as well.
    if cfg.use_fake_mapper:
        with _scorers_gpu_hidden(cfg.worker_extra_env):
            for mp_proc in mapper_procs:
                mp_proc.start()
            for sp in scorer_procs:
                sp.start()
    else:
        for mp_proc in mapper_procs:
            mp_proc.start()
        with _scorers_gpu_hidden(cfg.worker_extra_env):
            for sp in scorer_procs:
                sp.start()

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
        target=_writer_thread,
        name="chemcensor-writer",
        kwargs=dict(
            result_queue=result_queue,
            sink=sink,
            n_workers=cfg.n_workers,
            total_hint=total_hint,
            progress=cfg.progress,
            checkpoint_path=checkpoint_path,
            checkpoint_interval=cfg.checkpoint_interval,
            initial_state=state,
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
            scorer_procs=scorer_procs,
            respawn_scorer=_spawn_scorer,
            stop_event=stop_event,
            error_event=error_event,
        ),
        daemon=True,
    )

    reader.start()
    writer.start()
    watchdog.start()

    try:
        writer.join()
        reader.join(timeout=_DEFAULT_JOIN_TIMEOUT)
        # Drain in case error_event fired and reader still has sentinels queued.
        for mp_proc in mapper_procs:
            mp_proc.join(timeout=_DEFAULT_JOIN_TIMEOUT)
        for sp in scorer_procs:
            sp.join(timeout=_DEFAULT_JOIN_TIMEOUT)
    finally:
        stop_event.set()
        _shutdown_processes([*mapper_procs, *scorer_procs])
        _drain_queue(map_queue)
        _drain_queue(score_queue)
        _drain_queue(result_queue)

    if error_event.is_set():
        # Distinguish mapper vs scorer crashes for callers.
        dead_mappers = [
            mp_proc for mp_proc in mapper_procs if mp_proc.exitcode not in (0, None)
        ]
        if dead_mappers:
            raise MapperCrashedError(
                "Mapper subprocesses died: "
                + ", ".join(f"{p.name}={p.exitcode}" for p in dead_mappers)
            )
        dead = [
            sp
            for sp in scorer_procs
            if sp.exitcode not in (0, None, _RECYCLE_EXIT_CODE)
        ]
        if dead:
            raise ScorerCrashedError(
                "Scorer subprocesses died: "
                + ", ".join(f"{sp.name}={sp.exitcode}" for sp in dead)
            )
        # Generic fallback if the error came from a thread.
        raise ScorerCrashedError("Parallel pipeline aborted due to an error")


def _shutdown_processes(procs: list[Any]) -> None:
    """Best-effort shutdown of subprocesses without hanging the parent."""
    for proc in procs:
        if proc.is_alive():
            try:
                proc.terminate()
            except Exception:
                logger.debug("terminate() failed for %s", proc.name, exc_info=True)
    for proc in procs:
        try:
            proc.join(timeout=5.0)
        except Exception:
            logger.debug("join() failed for %s", proc.name, exc_info=True)
        if proc.is_alive():
            try:
                proc.kill()
            except Exception:
                logger.debug("kill() failed for %s", proc.name, exc_info=True)


def _drain_queue(q: Any) -> None:
    """Discard any items still sitting on ``q`` to allow GC of the file desc."""
    try:
        while True:
            q.get_nowait()
    except Exception:
        # ``Empty`` for the normal drain, OSError when the queue is closed —
        # both are expected at shutdown.
        logger.debug("Queue drain stopped", exc_info=True)
    try:
        q.close()
        q.join_thread()
    except Exception:
        logger.debug("Queue close/join_thread failed", exc_info=True)
