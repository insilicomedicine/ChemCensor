from __future__ import annotations

import logging
import multiprocessing.queues as mpq
import os
import sys
from os import PathLike
from typing import cast

from .messages import make_scored_item
from .messages import Result
from .messages import ScoredItem
from .messages import ScoreTask


logger = logging.getLogger(__name__)

#: Exit code a scorer uses to signal a *clean* ``maxtasksperchild`` recycle
#: (as opposed to a normal end-of-stream exit, code ``0``, or a crash, any
#: other non-zero code). The orchestrator's watchdog uses this to tell a
#: recycle apart and spawn a replacement worker. Picked outside the usual
#: 0/1/130/137 range to avoid colliding with crash/signal exit codes.
_RECYCLE_EXIT_CODE = 42


def _set_thread_env(extra: dict[str, str] | None = None) -> None:
    """Pin BLAS/OMP threads to 1 — avoids oversubscription with N workers.

    Scorer workers spend their time in RDKit and Python; extra threads
    only steal CPU from other workers.

    :param extra: Additional environment overrides to apply.
    :type extra: dict[str, str] | None
    """
    # Scorer workers run RDKit / NumPy on the CPU only. Hide the GPU so
    # importing torch (pulled in transitively) does not spin up a CUDA
    # context per worker — each context reserves ~300-600 MB of VRAM and
    # adds start-up latency for no benefit. ``worker_extra_env`` (applied
    # below) can still re-enable the GPU if a caller really needs it.
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("RDKIT_NUM_THREADS", "1")
    for key, value in (extra or {}).items():
        os.environ[key] = value


def _build_worker_state(
    db_path: str | PathLike,
    max_center_type: int,
    find_exact_match: bool,
    *,
    use_fake_mapper: bool = False,
    validate_input: bool = True,
    check_skeleton_conservation: bool = True,
    check_static_stereo: bool = True,
):
    """Construct the worker's processor + scoring object pair.

    Imports happen inside the subprocess so that ``spawn`` start does
    not pay the cost of loading dependencies the worker does not need.

    :param use_fake_mapper: When ``True`` the atom mapping is precomputed
        (FakeMapper) instead of produced by rxnmapper, so the reaction-SMILES
        length check is disabled (it exists only to bound rxnmapper inputs).
    :type use_fake_mapper: bool
    :param validate_input: Forwarded to
        :class:`~chemcensor.configs.chemcensor_config.ChemCensorConfig`.
    :type validate_input: bool
    :param check_skeleton_conservation: Forwarded to
        :class:`~chemcensor.configs.chemcensor_config.ChemCensorConfig`.
    :type check_skeleton_conservation: bool
    :param check_static_stereo: Forwarded to
        :class:`~chemcensor.configs.chemcensor_config.ChemCensorConfig`.
    :type check_static_stereo: bool

    :return: ``(light_processor, censor, scoring_config)`` triple.
    """
    # Local imports — keep heavy modules out of the parent's footprint.
    from chemcensor.chemcensor import ChemCensor
    from chemcensor.configs.chemcensor_config import ChemCensorConfig
    from chemcensor.configs.scoring_configs import ScoringConfig
    from chemcensor.db.manager import DBManager

    # Lightweight pipeline — Mapper lives in a separate process. Built from the
    # shared config so validators stay identical to single-process scoring.
    config = ChemCensorConfig(
        max_center_type=max_center_type,
        find_exact_match=find_exact_match,
        use_fake_mapper=use_fake_mapper,
        mapper_in_subprocess=True,
        validate_input=validate_input,
        check_skeleton_conservation=check_skeleton_conservation,
        check_static_stereo=check_static_stereo,
    )
    light_processor = config.build_processor()
    manager = DBManager.open_readonly(db_path)
    # Both score variants are emitted per reaction, so the worker does not
    # select between them — ``evaluate_processed`` ignores this flag.
    censor = ChemCensor(
        manager=manager,
        processor=light_processor,
        config=config,
    )
    return light_processor, censor, ScoringConfig


def run_scorer(
    score_queue: mpq.Queue,
    result_queue: mpq.Queue,
    *,
    db_path: str | PathLike,
    max_center_type: int,
    find_exact_match: bool,
    maxtasksperchild: int | None,
    extra_env: dict[str, str] | None,
    use_fake_mapper: bool = False,
    validate_input: bool = True,
    check_skeleton_conservation: bool = True,
    check_static_stereo: bool = True,
    include_canonical_smiles: bool = False,
) -> None:
    """Entry point executed inside each scorer subprocess.

    Pulls :class:`ScoreTask` messages from ``score_queue`` until a
    ``None`` sentinel arrives, then emits one ``None`` sentinel on
    ``result_queue`` so the writer thread can count completed workers.

    A ``maxtasksperchild`` recycle is handled differently: the worker exits
    with :data:`_RECYCLE_EXIT_CODE` **without** emitting a terminal ``None``,
    and the orchestrator's watchdog spawns a replacement that resumes
    draining ``score_queue``. This keeps the terminal-``None`` count equal to
    ``n_workers`` (so the writer cannot finish early and lose the unscored
    tail).

    :param score_queue: Inbound queue with :class:`ScoreTask` items.
    :param result_queue: Outbound queue with :class:`Result` items.
    :param db_path: Path to the SQLite reaction-centers database.
    :param max_center_type: Forwarded to :class:`ChemCensor`.
    :param find_exact_match: Forwarded to :class:`ChemCensor`.
    :param maxtasksperchild: When set, the worker exits (code
        :data:`_RECYCLE_EXIT_CODE`) after this many scored batches and the
        orchestrator spawns a replacement — a guard against memory leaks in
        upstream libraries.
    :param extra_env: Additional environment overrides applied at start.
    :param use_fake_mapper: Forwarded to :func:`_build_worker_state`; when
        ``True`` the reaction-SMILES length check is disabled (mapping is
        precomputed, not produced by rxnmapper).
    :param validate_input: Forwarded to :func:`_build_worker_state`.
    :param check_skeleton_conservation: Forwarded to :func:`_build_worker_state`.
    :param check_static_stereo: Forwarded to :func:`_build_worker_state`.
    """
    _set_thread_env(extra_env)

    # Lazy construction so any import error surfaces through the worker
    # exit code rather than the parent crashing on ``Process.start``.
    processor, censor, scoring_config = _build_worker_state(
        db_path=db_path,
        max_center_type=max_center_type,
        find_exact_match=find_exact_match,
        use_fake_mapper=use_fake_mapper,
        validate_input=validate_input,
        check_skeleton_conservation=check_skeleton_conservation,
        check_static_stereo=check_static_stereo,
    )
    failed_score = scoring_config.failed_reaction_scoring.value

    from chemcensor.basic import Reaction
    from chemcensor.chemcensor import FailureReason
    from chemcensor.chemcensor import FailureStage
    from chemcensor.processing.errors import ProcessingError

    tasks_done = 0
    recycle = False
    try:
        while True:
            task = score_queue.get()
            if task is None:
                break
            assert isinstance(task, ScoreTask)

            results: list[ScoredItem] = []
            for idx, raw_smi, mapped_smi in task.items:
                if mapped_smi is None:
                    results.append(
                        make_scored_item(
                            idx,
                            raw_smi,
                            failed_score,
                            failed_score,
                            failure_reason=FailureReason(
                                stage=FailureStage.PROCESSING,
                                category="MappingFailed",
                                message=(
                                    "Atom mapping did not produce a valid reaction."
                                ),
                            ),
                            cano_rxn=raw_smi if include_canonical_smiles else None,
                        )
                    )
                    continue

                reaction = Reaction(
                    reaction_smiles=raw_smi,
                    mapped_reaction_smiles=mapped_smi,
                )
                cano_rxn = raw_smi if include_canonical_smiles else None
                all_fgs_real = True
                all_centers_real = True
                total_fgs = 0
                virtual_fgs = 0
                failure_reason: FailureReason | None = None
                try:
                    processed = processor.process(reaction)
                    result = censor.evaluate_processed(processed)
                    with_fg = result.with_functional_groups
                    without_fg = result.without_functional_groups
                    all_fgs_real = result.all_fgs_precedents_are_real
                    total_fgs = result.total_number_of_fgs
                    virtual_fgs = result.number_of_fgs_covered_by_virtual_precedents
                    all_centers_real = result.all_center_precedents_are_real
                    failure_reason = result.failure_reason
                    if include_canonical_smiles:
                        cano_rxn = processed.canonical_smiles
                except ProcessingError as error:
                    with_fg = without_fg = failed_score
                    failure_reason = FailureReason(
                        stage=FailureStage.PROCESSING,
                        category=type(error).__name__,
                        message=str(error),
                    )
                except Exception as e:  # last-ditch safety net
                    logger.exception(
                        "Unexpected error while scoring %r: %s", raw_smi, e
                    )
                    with_fg = without_fg = failed_score
                    failure_reason = FailureReason(
                        stage=FailureStage.PROCESSING,
                        category=type(e).__name__,
                        message=str(e),
                    )

                results.append(
                    make_scored_item(
                        idx,
                        raw_smi,
                        with_fg,
                        without_fg,
                        all_fgs_precedents_are_real=all_fgs_real,
                        total_number_of_fgs=total_fgs,
                        number_of_fgs_covered_by_virtual_precedents=virtual_fgs,
                        all_center_precedents_are_real=all_centers_real,
                        failure_reason=failure_reason,
                        cano_rxn=cano_rxn if include_canonical_smiles else None,
                    )
                )

            result_queue.put(Result(batch_id=task.batch_id, items=tuple(results)))

            tasks_done += 1
            if maxtasksperchild is not None and tasks_done >= maxtasksperchild:
                recycle = True
                break
    finally:
        # Announce shutdown **only** on a genuine end-of-stream exit (the
        # ``None`` sentinel). A ``maxtasksperchild`` recycle must NOT emit a
        # terminal ``None``: it has not drained a sentinel, so the writer
        # would otherwise miscount this worker as done, declare success and
        # silently drop every batch still queued for the (now-gone) worker.
        # Instead we exit with ``_RECYCLE_EXIT_CODE`` and the orchestrator
        # spawns a replacement that keeps draining ``score_queue``.
        if not recycle:
            result_queue.put(None)
        # Keep the counter alive for static analyzers.
        _ = cast(int, tasks_done)

    if recycle:
        sys.exit(_RECYCLE_EXIT_CODE)
