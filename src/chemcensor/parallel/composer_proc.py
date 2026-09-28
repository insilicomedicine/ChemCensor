from __future__ import annotations

import logging
import multiprocessing.queues as mpq
import sys
from typing import cast
from typing import TYPE_CHECKING

from .messages import CompositionResult
from .messages import ScoreTask
from .scorer_proc import _RECYCLE_EXIT_CODE
from .scorer_proc import _set_thread_env


if TYPE_CHECKING:
    from chemcensor.composition.records import ReactionRecord


logger = logging.getLogger(__name__)


def _build_worker_state(
    max_center_type: int,
    *,
    use_fake_mapper: bool = False,
    validate_input: bool = True,
    check_skeleton_conservation: bool = True,
    check_static_stereo: bool = True,
):
    """Construct the worker's processor + extractor pair.

    Imports happen inside the subprocess so that ``spawn`` start does not pay
    the cost of loading dependencies the worker does not need. The processing
    pipeline mirrors the serial ``scripts/compose_database.py`` set, minus the
    stages handled elsewhere: :class:`Mapper` runs in the mapper subprocess and
    :class:`BatchFilter` is unnecessary because dummies are dropped explicitly
    while preserving the input ``idx``.

    :param max_center_type: Maximum reaction-center type to extract (1–4).
    :type max_center_type: int
    :param use_fake_mapper: When ``True`` the atom mapping is precomputed
        upstream (FakeMapper), so the reaction-SMILES length check is disabled
        (it exists only to bound rxnmapper inputs).
    :type use_fake_mapper: bool
    :param validate_input: Forwarded to
        :class:`~chemcensor.configs.composition_configs.CompositionPipelineConfig`.
    :type validate_input: bool
    :param check_skeleton_conservation: Forwarded to
        :class:`~chemcensor.configs.composition_configs.CompositionPipelineConfig`.
    :type check_skeleton_conservation: bool
    :param check_static_stereo: Forwarded to
        :class:`~chemcensor.configs.composition_configs.CompositionPipelineConfig`.
    :type check_static_stereo: bool
    :return: ``(processor, extractor)`` pair.
    """
    # Local imports — keep heavy modules out of the parent's footprint.
    from chemcensor.basic import ReactionCenterType
    from chemcensor.configs import CompositionPipelineConfig
    from chemcensor.extraction import ReactionCenterExtractor

    # The mapper runs in a dedicated subprocess and BatchFilter is unnecessary
    # (dummies are dropped explicitly while preserving the input ``idx``), so
    # both stages are excluded here; all validators stay identical to scoring
    # and serial composition via the shared factory.
    processor = CompositionPipelineConfig(
        use_fake_mapper=use_fake_mapper,
        mapper_in_subprocess=True,
        validate_input=validate_input,
        check_skeleton_conservation=check_skeleton_conservation,
        check_static_stereo=check_static_stereo,
    ).build_processor()
    extractor = ReactionCenterExtractor(
        max_center_type=ReactionCenterType(max_center_type)
    )
    return processor, extractor


def run_composer_worker(
    score_queue: mpq.Queue,
    result_queue: mpq.Queue,
    *,
    max_center_type: int,
    maxtasksperchild: int | None,
    extra_env: dict[str, str] | None,
    use_fake_mapper: bool = False,
    validate_input: bool = True,
    check_skeleton_conservation: bool = True,
    check_static_stereo: bool = True,
) -> None:
    """Entry point executed inside each composer worker subprocess.

    Pulls :class:`ScoreTask` messages from ``score_queue`` until a ``None``
    sentinel arrives, then emits one ``None`` sentinel on ``result_queue`` so
    the writer thread can count completed workers. Each task is processed
    through the (mapping-free) pipeline; every non-dummy result is turned into
    a picklable :class:`~chemcensor.composition.records.ReactionRecord` and
    forwarded — index-aligned — inside a :class:`CompositionResult`.

    A ``maxtasksperchild`` recycle is handled exactly as in
    :func:`~chemcensor.parallel.scorer_proc.run_scorer`: the worker exits with
    :data:`_RECYCLE_EXIT_CODE` **without** emitting a terminal ``None``, and the
    orchestrator's watchdog spawns a replacement that resumes draining
    ``score_queue``.

    :param score_queue: Inbound queue with :class:`ScoreTask` items.
    :param result_queue: Outbound queue with :class:`CompositionResult` items.
    :param max_center_type: Maximum reaction-center type to extract (1–4).
    :param maxtasksperchild: When set, the worker exits (code
        :data:`_RECYCLE_EXIT_CODE`) after this many processed batches and the
        orchestrator spawns a replacement — a guard against memory leaks in
        upstream libraries.
    :param extra_env: Additional environment overrides applied at start.
    :param use_fake_mapper: Forwarded to :func:`_build_worker_state`; when
        ``True`` the reaction-SMILES length check is disabled.
    :param validate_input: Forwarded to :func:`_build_worker_state`.
    :param check_skeleton_conservation: Forwarded to :func:`_build_worker_state`.
    :param check_static_stereo: Forwarded to :func:`_build_worker_state`.
    """
    _set_thread_env(extra_env)

    # Lazy construction so any import error surfaces through the worker exit
    # code rather than the parent crashing on ``Process.start``.
    processor, extractor = _build_worker_state(
        max_center_type=max_center_type,
        use_fake_mapper=use_fake_mapper,
        validate_input=validate_input,
        check_skeleton_conservation=check_skeleton_conservation,
        check_static_stereo=check_static_stereo,
    )

    from chemcensor.basic import Reaction
    from chemcensor.composition.records import record_from_reaction

    tasks_done = 0
    recycle = False
    try:
        while True:
            task = score_queue.get()
            if task is None:
                break
            assert isinstance(task, ScoreTask)

            indices = [idx for idx, _raw, _mapped in task.items]
            reactions = [
                (
                    Reaction(reaction_smiles=raw_smi, mapped_reaction_smiles=mapped_smi)
                    if mapped_smi is not None
                    else None
                )
                for _idx, raw_smi, mapped_smi in task.items
            ]
            # Feed only the mappable reactions through the pipeline; keep a
            # placeholder ``None`` for the rest so the input ``idx`` stays
            # aligned with the processed output.
            to_process = [r for r in reactions if r is not None]
            processed = list(processor.process_batch(to_process)) if to_process else []

            processed_iter = iter(processed)
            items: list[tuple[int, "ReactionRecord"]] = []
            for idx, reaction in zip(indices, reactions):
                if reaction is None:
                    continue
                result = next(processed_iter)
                if result.dummy:
                    continue
                try:
                    record = record_from_reaction(result, extractor)
                except Exception as e:  # last-ditch safety net
                    logger.exception(
                        "Unexpected error while building record for idx %d: %s",
                        idx,
                        e,
                    )
                    continue
                items.append((idx, record))

            result_queue.put(
                CompositionResult(batch_id=task.batch_id, items=tuple(items))
            )

            tasks_done += 1
            if maxtasksperchild is not None and tasks_done >= maxtasksperchild:
                recycle = True
                break
    finally:
        # Announce shutdown **only** on a genuine end-of-stream exit. A
        # ``maxtasksperchild`` recycle must NOT emit a terminal ``None``: the
        # writer would otherwise miscount this worker as done, declare success
        # and silently drop every batch still queued for the (now-gone) worker.
        if not recycle:
            result_queue.put(None)
        _ = cast(int, tasks_done)

    if recycle:
        sys.exit(_RECYCLE_EXIT_CODE)
