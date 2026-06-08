from __future__ import annotations

import os
from dataclasses import dataclass
from dataclasses import field


# Cap the number of mapper processes. The mapper is the pipeline
# bottleneck (single-threaded Python post-processing of rxnmapper's
# attention output), so it is parallelised across processes rather than
# threads. Beyond ~8 concurrent mappers the shared GPU and IPC overhead
# start to dominate on commodity hardware.
_MAX_MAPPERS = 8
# Default OMP threads per mapper process. Extra threads do not help —
# the bottleneck is GIL-bound Python, not BLAS — so each mapper gets a
# single thread and we scale with processes instead.
_DEFAULT_MAPPER_THREADS = 1
# Reserve one CPU for the main process (reader + writer threads do I/O
# and progress reporting, but Python GC and the orchestrator itself
# need breathing room).
_MAIN_PROCESS_RESERVE = 1


@dataclass(frozen=True)
class ParallelConfig:
    """Knobs for the parallel scoring pipeline.

    :param n_workers: Number of scorer worker processes. ``None`` →
        autoscale based on CPU count.
    :type n_workers: int | None
    :param n_mappers: Number of rxnmapper (mapper) processes. ``None`` →
        autoscale based on CPU count. The mapper stage is the throughput
        bottleneck, so it is parallelised across processes.
    :type n_mappers: int | None
    :param mapper_threads: Number of CPU threads given to *each* rxnmapper
        process via ``OMP_NUM_THREADS``. ``None`` → autoscale (1). Extra
        threads do not improve throughput; scale ``n_mappers`` instead.
    :type mapper_threads: int | None
    :param batch_size: Number of SMILES grouped into a single
        :class:`~chemcensor.parallel.messages.MapTask`. Larger batches
        amortise pickle/IPC overhead but raise peak memory and the
        granularity of checkpoints.
    :type batch_size: int
    :param map_queue_size: Maximum number of batches buffered on the
        reader → mapper queue (back-pressure).
    :type map_queue_size: int
    :param score_queue_size: Maximum number of batches buffered on the
        mapper → scorers queue.
    :type score_queue_size: int
    :param result_queue_size: Maximum number of batches buffered on the
        scorers → writer queue.
    :type result_queue_size: int
    :param max_center_type: Maximum reaction-center type to extract (1–4).
    :type max_center_type: int
    :param find_exact_match: Whether scorers should short-circuit to
        ``exact_match_scoring`` on a canonical-SMILES hit in the DB.
    :type find_exact_match: bool
    :param progress: Whether to display a tqdm progress bar in the writer
        thread.
    :type progress: bool
    :param checkpoint_interval: Number of scored reactions between
        atomic ``.ckpt`` flushes. ``0`` disables checkpointing.
    :type checkpoint_interval: int
    :param maxtasksperchild: When set, each scorer worker exits after this
        many scored batches and the orchestrator's watchdog spawns a fresh
        replacement into the same slot (a guard against memory leaks in
        upstream libraries). The replacement keeps draining the queue, so
        no input is dropped regardless of how it relates to the batch
        count. ``None`` (default) keeps every worker alive for the whole
        run.
    :type maxtasksperchild: int | None
    :param mapper_internal_batch_size: ``batch_size`` passed to
        :class:`rxnmapper.BatchedMapper`. Independent from
        :attr:`batch_size`.
    :type mapper_internal_batch_size: int
    :param use_fake_mapper: When ``True`` the input column is expected to
        hold *precomputed* atom-mapped reaction SMILES; the mapper stage
        reuses them via :class:`~chemcensor.processing.fake_mapper.FakeMapper`
        instead of running ``rxnmapper``. No GPU is used and the
        reaction-SMILES length check is disabled.
    :type use_fake_mapper: bool
    :param worker_extra_env: Optional environment overrides applied in
        every scorer process before any heavy import.
    :type worker_extra_env: dict[str, str]
    """

    n_workers: int | None = None
    n_mappers: int | None = None
    mapper_threads: int | None = None
    batch_size: int = 64
    map_queue_size: int = 8
    score_queue_size: int = 16
    result_queue_size: int = 32
    max_center_type: int = 4
    find_exact_match: bool = True
    progress: bool = True
    checkpoint_interval: int = 1000
    maxtasksperchild: int | None = None
    mapper_internal_batch_size: int = 32
    use_fake_mapper: bool = False
    worker_extra_env: dict[str, str] = field(default_factory=dict)

    def resolved(self) -> "ParallelConfig":
        """Return a copy with auto-scaled ``n_workers`` / ``n_mappers`` /
        ``mapper_threads``.

        :return: A new :class:`ParallelConfig` with concrete values.
        :rtype: ParallelConfig
        """
        n_workers, mapper_threads, n_mappers = autoscale(
            n_workers=self.n_workers,
            mapper_threads=self.mapper_threads,
            n_mappers=self.n_mappers,
        )
        # ``dataclasses.replace`` would re-validate the dict default;
        # construct explicitly for clarity.
        return ParallelConfig(
            n_workers=n_workers,
            n_mappers=n_mappers,
            mapper_threads=mapper_threads,
            batch_size=self.batch_size,
            map_queue_size=self.map_queue_size,
            score_queue_size=self.score_queue_size,
            result_queue_size=self.result_queue_size,
            max_center_type=self.max_center_type,
            find_exact_match=self.find_exact_match,
            progress=self.progress,
            checkpoint_interval=self.checkpoint_interval,
            maxtasksperchild=self.maxtasksperchild,
            mapper_internal_batch_size=self.mapper_internal_batch_size,
            use_fake_mapper=self.use_fake_mapper,
            worker_extra_env=dict(self.worker_extra_env),
        )


def autoscale(
    *,
    n_workers: int | None = None,
    mapper_threads: int | None = None,
    n_mappers: int | None = None,
    cpu_count: int | None = None,
) -> tuple[int, int, int]:
    """Pick concrete ``(n_workers, mapper_threads, n_mappers)`` values.

    The mapper stage is the pipeline bottleneck, so it is scaled across
    *processes* (``n_mappers``), each pinned to a single CPU thread; the
    remaining CPUs go to the scorer pool. ``n_mappers`` takes ~a quarter
    of the host (capped), mirroring the previous single-process mapper
    heuristic, and every value floors at 1 on tiny hosts.

    :param n_workers: Explicit override for scorer process count.
    :type n_workers: int | None
    :param mapper_threads: Explicit override for OMP threads per mapper.
    :type mapper_threads: int | None
    :param n_mappers: Explicit override for mapper process count.
    :type n_mappers: int | None
    :param cpu_count: Override for ``os.cpu_count()`` (used in tests).
    :type cpu_count: int | None
    :return: Resolved ``(n_workers, mapper_threads, n_mappers)`` tuple.
    :rtype: tuple[int, int, int]
    """
    total = cpu_count if cpu_count is not None else (os.cpu_count() or 1)
    total = max(1, total)

    # Heuristic: mappers take ~quarter of CPUs, capped, and at least 1.
    auto_mappers = min(_MAX_MAPPERS, max(1, total // 4))
    resolved_mappers = n_mappers if n_mappers is not None else auto_mappers
    resolved_mappers = max(1, resolved_mappers)

    resolved_threads = (
        mapper_threads if mapper_threads is not None else _DEFAULT_MAPPER_THREADS
    )
    resolved_threads = max(1, resolved_threads)

    auto_workers = max(
        1, total - resolved_mappers * resolved_threads - _MAIN_PROCESS_RESERVE
    )
    resolved_workers = n_workers if n_workers is not None else auto_workers
    resolved_workers = max(1, resolved_workers)

    return resolved_workers, resolved_threads, resolved_mappers
