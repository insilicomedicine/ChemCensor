from __future__ import annotations

import logging
import multiprocessing.queues as mpq
import os
import re
from typing import Any
from typing import Callable

from .messages import MapTask
from .messages import ScoreTask


logger = logging.getLogger(__name__)

# Matches the ``:N`` atom-map label inside a bracket atom (``[CH3:1]``).
# Used to derive an unmapped reaction SMILES from a precomputed mapped one
# without re-canonicalising (RDKit would reorder atoms and break the
# index alignment FakeMapper relies on).
_ATOM_MAP_RE = re.compile(r":\d+(?=[\]])")

# A per-batch processor: maps ``(idx, smiles)`` items to scorer items
# ``(idx, raw_smiles, mapped_smiles_or_None)``.
_BatchProcessor = Callable[
    [tuple[tuple[int, str], ...]], tuple[tuple[int, str, str | None], ...]
]


def _set_thread_env(threads: int) -> None:
    """Pin BLAS/OMP threads for this process before any heavy import.

    Must be called *before* importing ``torch`` / ``transformers`` /
    ``rxnmapper`` because those libraries cache the thread setting on
    first import.

    :param threads: Number of CPU threads the mapper may use.
    :type threads: int
    """
    threads_str = str(max(1, threads))
    os.environ.setdefault("OMP_NUM_THREADS", threads_str)
    os.environ.setdefault("MKL_NUM_THREADS", threads_str)
    os.environ.setdefault("OPENBLAS_NUM_THREADS", threads_str)
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")


def _map_with_retry(mapper: Any, smiles_list: list[str]) -> list[str]:
    """Map a batch and fall back to per-reaction mapping on chunk failure.

    ``rxnmapper.BatchedMapper`` chunks the input internally; when one
    chunk raises, the whole chunk is normally lost.  We catch the
    exception and re-run each reaction one by one so the failure is
    isolated to the offending SMILES.

    :param mapper: A :class:`rxnmapper.BatchedMapper` instance.
    :type mapper: Any
    :param smiles_list: Raw reaction SMILES to map.
    :type smiles_list: list[str]
    :return: One mapped SMILES per input; ``">>"`` for failures.
    :rtype: list[str]
    """
    try:
        return list(mapper.map_reactions(smiles_list))
    except Exception as e:
        logger.warning(
            "rxnmapper failed on a batch of %d reactions; retrying one by one: %s",
            len(smiles_list),
            e,
        )

    mapped: list[str] = []
    for smiles in smiles_list:
        try:
            mapped.append(next(mapper.map_reactions([smiles])))
        except Exception:
            mapped.append(">>")
    return mapped


def _build_rxnmapper_processor(rxnmapper_batch_size: int) -> _BatchProcessor:
    """Build the rxnmapper-backed per-batch processor.

    Validates the raw SMILES first (cheap, mapping-independent) so the
    GPU-bound mapper never wastes a forward pass — or trips the slow
    per-reaction fallback in :func:`_map_with_retry` — on doomed input.

    :param rxnmapper_batch_size: ``batch_size`` for the
        :class:`rxnmapper.BatchedMapper`.
    :return: A callable turning ``MapTask`` items into ``ScoreTask`` items.
    :rtype: _BatchProcessor
    """
    from rxnmapper import BatchedMapper

    from chemcensor.basic import Reaction
    from chemcensor.processing.errors import ProcessingError
    from chemcensor.processing.validator import Validator

    mapper = BatchedMapper(canonicalize=True, batch_size=rxnmapper_batch_size)
    validator = Validator()

    def _is_valid(smiles: str) -> bool:
        try:
            validator.process(Reaction(reaction_smiles=smiles))
            return True
        except ProcessingError:
            return False

    def _process(
        items: tuple[tuple[int, str], ...],
    ) -> tuple[tuple[int, str, str | None], ...]:
        indices = [idx for idx, _ in items]
        raw = [smi for _, smi in items]

        valid_flags = [_is_valid(smi) for smi in raw]
        to_map = [smi for smi, ok in zip(raw, valid_flags) if ok]
        mapped_iter = iter(_map_with_retry(mapper, to_map))

        mapped: list[str | None] = []
        for ok in valid_flags:
            if not ok:
                mapped.append(None)
                continue
            mapped_smi = next(mapped_iter)
            mapped.append(mapped_smi if mapped_smi and mapped_smi != ">>" else None)

        return tuple(
            (idx, raw_smi, mapped_smi)
            for idx, raw_smi, mapped_smi in zip(indices, raw, mapped)
        )

    return _process


def _build_fake_processor() -> _BatchProcessor:
    """Build the FakeMapper-backed per-batch processor.

    Each input SMILES is a *precomputed* atom-mapped reaction SMILES (e.g.
    CREED's ``*_mapped`` fields). The unmapped reaction SMILES is recovered
    by textually stripping atom-map labels — this preserves atom order so
    :class:`~chemcensor.processing.fake_mapper.FakeMapper` re-attaches the
    maps to the right atoms — and the canonical mapped SMILES is rebuilt
    from the parsed maps. No GPU and no ``rxnmapper`` involved.

    :return: A callable turning ``MapTask`` items into ``ScoreTask`` items.
    :rtype: _BatchProcessor
    """
    from frozendict import frozendict

    from chemcensor.basic import Reaction
    from chemcensor.processing.errors import ProcessingError
    from chemcensor.processing.fake_mapper import FakeMapper
    from chemcensor.processing.utils import (
        prepare_fake_mapper_meta_from_mapped_rxn as _prepare_meta,
    )

    fake = FakeMapper()

    def _process(
        items: tuple[tuple[int, str], ...],
    ) -> tuple[tuple[int, str, str | None], ...]:
        out: list[tuple[int, str, str | None]] = []
        for idx, mapped_input in items:
            raw = _ATOM_MAP_RE.sub("", mapped_input)
            try:
                meta = _prepare_meta(mapped_input)
                reaction = fake.process(
                    Reaction(reaction_smiles=raw, meta=frozendict(meta))
                )
                out.append((idx, raw, reaction.mapped_reaction_smiles))
            except ProcessingError:
                out.append((idx, raw, None))
            except Exception as e:  # last-ditch safety net
                logger.warning("FakeMapper failed on %r: %s", mapped_input, e)
                out.append((idx, raw, None))
        return tuple(out)

    return _process


def run_mapper(
    map_queue: mpq.Queue,
    score_queue: mpq.Queue,
    *,
    threads: int,
    rxnmapper_batch_size: int,
    n_scorers: int,
    mappers_remaining: Any = None,
    use_fake_mapper: bool = False,
) -> None:
    """Entry point executed inside the mapper subprocess.

    Reads :class:`MapTask` messages from ``map_queue``, validates the raw
    SMILES (cheap, mapping-independent), runs the valid ones through
    :func:`_map_with_retry`, and forwards :class:`ScoreTask` messages to
    ``score_queue``.  Reactions that fail validation skip rxnmapper and are
    forwarded with ``mapped=None``.  A ``None`` sentinel on ``map_queue``
    triggers shutdown; the mapper then enqueues ``n_scorers`` sentinels
    on ``score_queue`` so each scorer worker can drain and exit.

    :param map_queue: Inbound queue with :class:`MapTask` items.
    :type map_queue: multiprocessing.Queue
    :param score_queue: Outbound queue with :class:`ScoreTask` items.
    :type score_queue: multiprocessing.Queue
    :param threads: Maximum CPU threads to allocate to torch/OMP.
    :type threads: int
    :param rxnmapper_batch_size: ``batch_size`` for the
        :class:`rxnmapper.BatchedMapper`.
    :type rxnmapper_batch_size: int
    :param n_scorers: Number of sentinels to emit on shutdown.
    :type n_scorers: int
    :param mappers_remaining: Optional shared counter (``multiprocessing``
        ``Value``) used to coordinate sentinel emission when several mapper
        processes share ``score_queue``. Each mapper decrements it on exit;
        the last one to finish emits the ``n_scorers`` sentinels so every
        scorer drains exactly once. ``None`` means this is the only mapper.
    :type mappers_remaining: multiprocessing.Value | None
    :param use_fake_mapper: When ``True`` the input SMILES are precomputed
        atom-mapped reactions and :class:`FakeMapper` is used instead of
        ``rxnmapper`` (no GPU, no model import).
    :type use_fake_mapper: bool
    """
    _set_thread_env(threads)

    # Build the per-batch processor inside the subprocess so the parent
    # never imports rxnmapper/torch (and, for the fake path, never even
    # touches the GPU).
    if use_fake_mapper:
        process_batch = _build_fake_processor()
    else:
        process_batch = _build_rxnmapper_processor(rxnmapper_batch_size)

    try:
        while True:
            task = map_queue.get()
            if task is None:
                break
            assert isinstance(task, MapTask)
            score_items = process_batch(task.items)
            score_queue.put(ScoreTask(batch_id=task.batch_id, items=score_items))
    finally:
        # With several mappers sharing ``score_queue``, only the last one
        # to finish may emit scorer sentinels — otherwise scorers would see
        # ``n_mappers * n_scorers`` of them. The shared counter serialises
        # this decision; a lone mapper (``None``) always emits.
        if mappers_remaining is None:
            is_last = True
        else:
            with mappers_remaining.get_lock():
                mappers_remaining.value -= 1
                is_last = mappers_remaining.value <= 0
        if is_last:
            for _ in range(n_scorers):
                score_queue.put(None)
