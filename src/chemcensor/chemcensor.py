from collections.abc import Sequence
from dataclasses import dataclass
from dataclasses import field
from dataclasses import replace
from enum import StrEnum
from operator import itemgetter
from os import PathLike
from threading import RLock
from typing import cast
from typing import Literal
from typing import overload

import numpy as np

from .basic import Reaction
from .basic import ReactionCenter
from .basic import ReactionCenterType
from .configs.chemcensor_config import ChemCensorConfig
from .configs.scoring_configs import ScoringConfig
from .db.download import resolve_database_path
from .db.manager import DBManager
from .errors import InvalidCenterTypeError
from .extraction import ReactionCenterExtractor
from .extraction.errors import ExtractionError
from .processing.errors import ProcessingError
from .processing.reaction_processor import ReactionProcessor
from .rules.functional_groups import FUNCTIONAL_GROUPS
from .trace import CenterTrace
from .trace import FunctionalGroupEvidence
from .trace import PrecedentExample
from .trace import PrecedentStatus
from .trace import TraceOutcome


_PRECEDENT_EXAMPLE_LIMIT = 3
_FG_BY_INDEX = {cast(int, group["idx"]): group for group in FUNCTIONAL_GROUPS}
_FG_UI_NAMES = {
    index: cast(str, group["ui_name"]) for index, group in _FG_BY_INDEX.items()
}


def _functional_group_names(signature: np.ndarray) -> tuple[str, ...]:
    """Return UI names for set bits in a functional-group signature."""
    return tuple(
        _FG_UI_NAMES.get(int(index), f"Functional group {index}")
        for index in np.flatnonzero(signature)
    )


def _functional_group_descriptor(index: int) -> tuple[str, str, str]:
    """Return name, UI name and SMARTS for one FG signature index."""
    group = _FG_BY_INDEX.get(index)
    if group is None:
        fallback = f"Functional group {index}"
        return fallback, fallback, ""
    return (
        cast(str, group["name"]),
        cast(str, group["ui_name"]),
        cast(str, group["smarts"]),
    )


def _precedent_examples(
    rows: list[tuple[str, str, str, bool]],
) -> tuple[PrecedentExample, ...]:
    """Convert database precedent rows into public trace models."""
    return tuple(
        PrecedentExample(
            reaction_smiles=reaction_smiles,
            document_id=document_id,
            source=source,
            is_virtual=is_virtual,
        )
        for reaction_smiles, document_id, source, is_virtual in rows
    )


def _fg_subsignature_matches(rc_fg: np.ndarray, ref_fg: np.ndarray) -> bool:
    """True if every 1-bit in *rc_fg* is also set in *ref_fg*."""
    return bool(np.sum(rc_fg - ref_fg * rc_fg) == 0)


def _fg_coverage_by_real_and_virtual(
    rc_fg: np.ndarray,
    real_fg: np.ndarray | None,
    virtual_fg: np.ndarray | None,
) -> tuple[bool, int, int]:
    """Return ``(covered, total_bits, bits_covered_by_virtual)`` for *rc_fg*.

    Bits present in *real_fg* are accepted immediately. Only bits still missing
    after the real check are required to appear in *virtual_fg*. When coverage
    succeeds via virtual fill-in, ``bits_covered_by_virtual`` equals the number
    of those missing 1-bits; otherwise it is ``0``.
    """
    total_bits = int(rc_fg.sum())
    if real_fg is None:
        real = np.zeros_like(rc_fg)
    else:
        real = real_fg
    missing = rc_fg * (1 - real)
    missing_count = int(missing.sum())
    if missing_count == 0:
        return True, total_bits, 0
    if virtual_fg is None:
        return False, total_bits, 0
    if _fg_subsignature_matches(missing, virtual_fg):
        return True, total_bits, missing_count
    return False, total_bits, 0


class FailureStage(StrEnum):
    """High-level stage where reaction scoring failed."""

    PROCESSING = "processing"
    EXTRACTION = "extraction"


@dataclass(frozen=True)
class FailureReason:
    """Structured explanation for a failed scoring result.

    :param stage: High-level scoring stage that failed.
    :type stage: FailureStage
    :param category: Stable exception-category name.
    :type category: str
    :param message: Human-readable failure description.
    :type message: str
    """

    stage: FailureStage
    category: str
    message: str


@dataclass(frozen=True)
class ScoreResult:
    """Outcome of scoring a single reaction.

    Holds both scoring variants so a caller can obtain the functional-group
    aware and functional-group agnostic scores from a single evaluation, plus
    FG- and center-precedent provenance so a client can penalize virtual
    fill-in or virtual-only centers without changing ChemCensor's score logic.

    :param with_functional_groups: Score requiring each reaction center's
        functional-group sub-signature to match the DB reference.
    :type with_functional_groups: float
    :param without_functional_groups: Score based on reaction-center presence
        in the DB only, ignoring the functional-group comparison.
    :type without_functional_groups: float
    :param all_fgs_precedents_are_real: ``True`` when no center in the with-FG
        consecutive-prefix needed a virtual signature fill-in (AND over the
        whole passing prefix). Vacuously ``True`` for early exits (failed /
        SIS / exact match / tautomerization) where no FG check ran.
        Virtual-only center *presence* does not flip this flag; only FG bits
        accepted via the virtual signature do.
    :type all_fgs_precedents_are_real: bool
    :param total_number_of_fgs: Number of set functional groups (signature 1s)
        on the decisive center for the with-FG score — the outermost center
        that passed the consecutive-prefix rule, or the first center that
        failed the FG check when none passed. ``0`` when no FG check ran.
    :type total_number_of_fgs: int
    :param number_of_fgs_covered_by_virtual_precedents: Of those groups on the
        decisive center, how many were missing from the real signature and
        accepted via the virtual signature. ``0`` when the decisive center
        failed the FG check or needed no virtual fill-in. Unlike the bool,
        this is *not* aggregated over the prefix.
    :type number_of_fgs_covered_by_virtual_precedents: int
    :param all_center_precedents_are_real: ``True`` when every center that
        contributed to the without-FG consecutive prefix was found as a real
        row (AND over that prefix). ``False`` when at least one of those
        centers existed only as a virtual row. Vacuously ``True`` for early
        exits where no center lookup ran (failed / SIS / exact match /
        tautomerization). A center with both real and virtual rows counts as
        real.
    :type all_center_precedents_are_real: bool
    :param failure_reason: Structured processing or extraction failure
        information. ``None`` for successful results. This field is excluded
        from dataclass equality, so two otherwise equal scores may carry
        different diagnostic details.
    :type failure_reason: FailureReason | None
    """

    with_functional_groups: float
    without_functional_groups: float
    all_fgs_precedents_are_real: bool = True
    total_number_of_fgs: int = 0
    number_of_fgs_covered_by_virtual_precedents: int = 0
    all_center_precedents_are_real: bool = True
    failure_reason: FailureReason | None = field(default=None, compare=False)

    @classmethod
    def uniform(
        cls,
        value: float,
        *,
        all_fgs_precedents_are_real: bool = True,
        total_number_of_fgs: int = 0,
        number_of_fgs_covered_by_virtual_precedents: int = 0,
        all_center_precedents_are_real: bool = True,
        failure_reason: FailureReason | None = None,
    ) -> "ScoreResult":
        """Build a result where both variants share the same ``value``.

        Used for outcomes decided before the per-center loop (failed, SIS,
        exact match, tautomerization), which do not depend on functional groups.

        :param value: Score assigned to both variants.
        :type value: float
        :param all_fgs_precedents_are_real: FG-precedent flag (defaults to
            ``True`` — no FG check ran on early-exit paths).
        :type all_fgs_precedents_are_real: bool
        :param total_number_of_fgs: FG count on the decisive center (``0`` for
            early-exit outcomes).
        :type total_number_of_fgs: int
        :param number_of_fgs_covered_by_virtual_precedents: FGs on that center
            covered by virtual signatures (``0`` for early-exit outcomes).
        :type number_of_fgs_covered_by_virtual_precedents: int
        :param all_center_precedents_are_real: Center-precedent flag (defaults
            to ``True`` — no center lookup ran on early-exit paths).
        :type all_center_precedents_are_real: bool
        :param failure_reason: Structured failure information, or ``None`` for
            a successful early-exit outcome.
        :type failure_reason: FailureReason | None
        :return: A :class:`ScoreResult` with identical variants.
        :rtype: ScoreResult
        """
        return cls(
            with_functional_groups=value,
            without_functional_groups=value,
            all_fgs_precedents_are_real=all_fgs_precedents_are_real,
            total_number_of_fgs=total_number_of_fgs,
            number_of_fgs_covered_by_virtual_precedents=(
                number_of_fgs_covered_by_virtual_precedents
            ),
            all_center_precedents_are_real=all_center_precedents_are_real,
            failure_reason=failure_reason,
        )

    def select(self, check_functional_groups: bool) -> float:
        """Return the score for the requested functional-group mode.

        :param check_functional_groups: When ``True`` return the FG-aware score,
            otherwise the FG-agnostic one.
        :type check_functional_groups: bool
        :return: The selected score.
        :rtype: float
        """
        return (
            self.with_functional_groups
            if check_functional_groups
            else self.without_functional_groups
        )


@dataclass(frozen=True)
class ScoreTrace:
    """Explainable result of processing, extraction and center scoring.

    :param result: Final aggregate score, identical to :meth:`ChemCensor.evaluate`.
    :type result: ScoreResult
    :param outcome: High-level scoring path.
    :type outcome: TraceOutcome
    :param centers: RC1–RC4 center traversal in ascending type order.
    :type centers: tuple[CenterTrace, ...]
    :param chain_failed_at: First center that stopped the functional-group-aware
        consecutive chain.
    :type chain_failed_at: ReactionCenterType | None
    :param center_chain_failed_at: First absent center that stopped the
        center-presence consecutive chain.
    :type center_chain_failed_at: ReactionCenterType | None
    :param canonical_smiles: Canonical full-reaction SMILES when processing
        completed, otherwise the best available reaction string.
    :type canonical_smiles: str
    :param exact_real_precedents: Up to three real document records for an
        exact reaction match.
    :type exact_real_precedents: tuple[PrecedentExample, ...]
    :param exact_virtual_precedents: Up to three virtual document records for
        an exact reaction match.
    :type exact_virtual_precedents: tuple[PrecedentExample, ...]
    """

    result: ScoreResult
    outcome: TraceOutcome
    centers: tuple[CenterTrace, ...] = ()
    chain_failed_at: ReactionCenterType | None = None
    center_chain_failed_at: ReactionCenterType | None = None
    canonical_smiles: str = ""
    exact_real_precedents: tuple[PrecedentExample, ...] = ()
    exact_virtual_precedents: tuple[PrecedentExample, ...] = ()


def _failed_result(
    stage: FailureStage,
    error: ProcessingError | ExtractionError,
) -> ScoreResult:
    """Return the configured failed score with structured error information."""
    return ScoreResult.uniform(
        ScoringConfig.failed_reaction_scoring.value,
        failure_reason=FailureReason(
            stage=stage,
            category=type(error).__name__,
            message=str(error),
        ),
    )


class ChemCensor:
    """Public API for reaction scoring.

    User only supplies the reaction centers database (path or manager).
    Processing pipeline and extraction are created internally.

    For server applications, use :meth:`open` to attach to the database file
    in read-only mode without copying it into memory. The ``db_path`` argument
    to :meth:`__init__` retains the original in-memory loading behavior.

    Scoring calls on one instance are thread-safe but serialized: the mapper,
    extractor and database manager are never entered concurrently. Multiple
    instances may execute independently. Use the parallel scoring API for
    throughput rather than concurrent calls to one instance. Construction with
    ``ChemCensorConfig(use_cpu=True)`` is not thread-safe because mapper setup
    temporarily changes ``CUDA_VISIBLE_DEVICES``; server applications must
    construct instances before starting request-serving threads.
    """

    def __init__(
        self,
        *,
        db_path: str | PathLike | None = None,
        manager: DBManager | None = None,
        config: ChemCensorConfig = ChemCensorConfig(),
        processor: ReactionProcessor | None = None,
    ) -> None:
        """Initialize ChemCensor from a database path or an existing DBManager.

        Provide at most one of ``db_path`` or ``manager``. When neither is
        provided, the current default database is downloaded from Hugging Face
        on first use and opened directly in read-only mode.

        Scoring and pipeline options are taken from ``config``. Pass
        ``ChemCensorConfig(use_fake_mapper=True)`` for the alpha FakeMapper
        pipeline, or ``ChemCensorConfig(use_cpu=True)`` to run rxnmapper on
        CPU. Set ``validate_input`` / ``check_skeleton_conservation`` /
        ``check_static_stereo`` to ``False`` to skip those default-on
        validators.

        :param db_path: Path to the SQLite reaction-centers database (loaded on init).
        :type db_path: str | PathLike | None
        :param manager: Pre-built DBManager instance (e.g. for tests or custom load).
        :type manager: DBManager | None
        :param config: Bundled scoring and pipeline configuration.
        :type config: ChemCensorConfig
        :param processor: Optional pre-built :class:`ReactionProcessor`. When
            omitted, the pipeline is built from ``config``. Pass a custom
            lightweight processor (e.g. without ``Mapper``) when reactions
            are pre-mapped upstream — used by the parallel scoring pipeline.
        :type processor: ReactionProcessor | None
        """
        if db_path is not None and manager is not None:
            raise ValueError(
                "Provide db_path or manager instance using DBManager.load() method. "
                "Both items are not permitted"
            )
        if db_path is not None:
            self._manager = DBManager.load(db_path)
        elif manager is not None:
            self._manager = manager
        else:
            self._manager = DBManager.open_readonly(resolve_database_path(None))

        try:
            max_center_type = ReactionCenterType(config.max_center_type)
        except ValueError:
            raise InvalidCenterTypeError(config.max_center_type) from None

        self._processor = (
            processor if processor is not None else config.build_processor()
        )
        self._rc_extractor = ReactionCenterExtractor(max_center_type=max_center_type)
        self._find_exact_match = config.find_exact_match
        self._check_functional_groups = config.check_functional_groups
        self._scoring_lock = RLock()

    @classmethod
    def open(
        cls,
        db_path: str | PathLike | None = None,
        *,
        readonly: bool = True,
        config: ChemCensorConfig = ChemCensorConfig(),
        processor: ReactionProcessor | None = None,
    ) -> "ChemCensor":
        """Open ChemCensor from a database file or the default database.

        By default, the SQLite file remains on disk and is opened in immutable
        read-only mode. This avoids the full in-memory copy performed by
        ``ChemCensor(db_path=...)`` and is the recommended constructor for
        long-lived servers and other memory-sensitive applications.

        When ``db_path`` is omitted, the current compatible database is
        downloaded from Hugging Face and reused from its local cache.

        Set ``readonly=False`` to retain the traditional behavior of loading a
        writable database copy into memory. Changes to that copy are not
        written back to ``db_path`` unless its manager is explicitly dumped.

        :param db_path: Optional path to the SQLite reaction-centers database.
        :type db_path: str | PathLike | None
        :param readonly: Open the file directly in immutable read-only mode.
        :type readonly: bool
        :param config: Bundled scoring and pipeline configuration.
        :type config: ChemCensorConfig
        :param processor: Optional pre-built :class:`ReactionProcessor`.
        :type processor: ReactionProcessor | None
        :return: A ChemCensor backed by the selected database access mode.
        :rtype: ChemCensor
        """
        resolved_path = resolve_database_path(db_path)
        manager = (
            DBManager.open_readonly(resolved_path)
            if readonly
            else DBManager.load(resolved_path)
        )
        return cls(manager=manager, config=config, processor=processor)

    def _reference_fg_pair_for_center_scoring(
        self, reaction: Reaction, rc: ReactionCenter
    ) -> tuple[np.ndarray | None, np.ndarray | None]:
        """Return ``(real_fg, virtual_fg)`` used to validate *rc* for scoring.

        Non-SEAr: global signatures from ``reaction_centers``. SEAr: aggregated
        bridge rows matching ``reaction.sear_signature`` per virtuality group.
        """
        if reaction.is_sear_reaction:
            return self._manager.lookup_center_sear_fg_pair(
                rc.reaction_center_smiles,
                reaction.sear_signature,
            )
        return self._manager.lookup_center_fg_pair(rc.reaction_center_smiles)

    def trace(self, reaction_smiles: str) -> ScoreTrace:
        """Process and score a reaction with an explainable center traversal.

        The returned :attr:`ScoreTrace.result` is produced by the same code
        path as :meth:`evaluate`; tracing does not reimplement scoring logic.

        :param reaction_smiles: Reaction SMILES string to process and score.
        :type reaction_smiles: str
        :return: Structured processing outcome and RC1–RC4 traversal.
        :rtype: ScoreTrace
        """
        with self._scoring_lock:
            reaction = Reaction(reaction_smiles=reaction_smiles)
            return self._trace_reaction(reaction, include_precedents=True)

    def trace_batch(self, reaction_smiles: Sequence[str]) -> list[ScoreTrace]:
        """Trace a batch while mapping all reactions in one mapper call.

        Failed processing items follow the batch contract and are returned as
        ``ProcessingSentinel`` traces.

        :param reaction_smiles: Reaction SMILES strings in route order.
        :type reaction_smiles: Sequence[str]
        :return: One evidence-bearing trace per input, in the same order.
        :rtype: list[ScoreTrace]
        """
        with self._scoring_lock:
            processed = self._processor.process_batch(
                [
                    Reaction(reaction_smiles=reaction_smiles_item)
                    for reaction_smiles_item in reaction_smiles
                ]
            )
            return [
                self._trace_processed(
                    reaction,
                    include_precedents=True,
                )
                for reaction in processed
            ]

    def _trace_reaction(
        self,
        reaction: Reaction,
        *,
        include_precedents: bool,
    ) -> ScoreTrace:
        """Process *reaction* and return its complete scoring trace."""
        try:
            processed = self._processor.process(reaction)
        except ProcessingError as error:
            return ScoreTrace(
                result=_failed_result(FailureStage.PROCESSING, error),
                outcome=TraceOutcome.FAILED,
                canonical_smiles=reaction.reaction_smiles,
            )
        return self._trace_processed(
            processed,
            include_precedents=include_precedents,
        )

    @overload
    def evaluate(
        self, reaction_smiles: str, return_canonical_smiles: Literal[False] = ...
    ) -> ScoreResult: ...

    @overload
    def evaluate(
        self, reaction_smiles: str, return_canonical_smiles: Literal[True]
    ) -> tuple[ScoreResult, str]: ...

    def evaluate(
        self, reaction_smiles: str, return_canonical_smiles: bool = False
    ) -> ScoreResult | tuple[ScoreResult, str]:
        """Evaluate a reaction, returning both functional-group score variants.

        1. Process reaction (validate, map, orphans, transform, canonicalize,
           SIS / SeAr annotation).
        2. Extract reaction centers and annotate FGs.
        3. Look up each extracted center in the DB and score it.

        The (expensive) pipeline runs once; the with- and without-functional
        -groups scores are derived together (see :class:`ScoreResult`).

        For the FakeMapper alpha pipeline, use :meth:`evaluate_reaction` so
        ``Reaction.meta`` (precomputed atom maps) is preserved.

        :param reaction_smiles: Reaction SMILES string to score.
        :type reaction_smiles: str
        :param return_canonical_smiles: When ``True``, return
            ``(ScoreResult, canonical_smiles)`` instead of a
            :class:`ScoreResult` alone.
        :type return_canonical_smiles: bool
        :return: Both scoring variants for the reaction, optionally paired
            with the canonical SMILES string.
        :rtype: ScoreResult | tuple[ScoreResult, str]
        """
        with self._scoring_lock:
            trace = self._trace_reaction(
                Reaction(reaction_smiles=reaction_smiles),
                include_precedents=False,
            )

            if return_canonical_smiles:
                return (trace.result, trace.canonical_smiles)
            return trace.result

    def evaluate_reaction(self, reaction: Reaction) -> ScoreResult:
        """Evaluate a :class:`~chemcensor.basic.Reaction`, preserving its ``meta``.

        Same pipeline as :meth:`evaluate`, but accepts a fully constructed
        :class:`~chemcensor.basic.Reaction` — required when using
        :attr:`~chemcensor.configs.chemcensor_config.ChemCensorConfig.use_fake_mapper`
        and supplying atom maps via ``Reaction.meta``.

        :param reaction: Reaction to process and score.
        :type reaction: Reaction
        :return: Both scoring variants for the reaction.
        :rtype: ScoreResult
        """
        with self._scoring_lock:
            return self._trace_reaction(
                reaction,
                include_precedents=False,
            ).result

    def evaluate_batch(self, reactions: Sequence[Reaction]) -> list[ScoreResult]:
        """Process and score a batch with one call per pipeline stage.

        This allows the mapper to map the reactions together. As with other
        processor batch APIs, an item that fails any processing stage becomes
        a sentinel and receives a ``ProcessingSentinel`` failure reason.

        :param reactions: Reactions to process and score in input order.
        :type reactions: Sequence[Reaction]
        :return: One score result per input reaction, in the same order.
        :rtype: list[ScoreResult]
        """
        with self._scoring_lock:
            processed = self._processor.process_batch(reactions)
            return [
                self._trace_processed(
                    reaction,
                    include_precedents=False,
                ).result
                for reaction in processed
            ]

    def evaluate_processed(self, reaction: Reaction) -> ScoreResult:
        """Evaluate an already-processed reaction, returning both score variants.

        Use this when the processing pipeline has been split across
        processes — for example in the parallel scorer worker, where atom
        mapping happens in a dedicated mapper process and the lightweight
        processor in the worker continues from
        :class:`~chemcensor.processing.OrphanRemover` onwards.

        Performs steps 2 and 3 of :meth:`evaluate`: optional exact-match
        lookup, reaction-center extraction and DB-based scoring.

        :param reaction: Reaction that has already been processed by a
            :class:`~chemcensor.processing.reaction_processor.ReactionProcessor`
            (i.e. it has ``canonical_smiles`` populated, SIS / tautomer
            flags set, etc.).
        :type reaction: Reaction
        :return: Both scoring variants for the reaction.
        :rtype: ScoreResult
        """
        with self._scoring_lock:
            return self._trace_processed(
                reaction,
                include_precedents=False,
            ).result

    def _trace_processed(
        self,
        reaction: Reaction,
        *,
        include_precedents: bool,
    ) -> ScoreTrace:
        """Extract and score an already-processed reaction with a trace."""
        canonical_smiles = reaction.canonical_smiles or reaction.reaction_smiles
        if reaction.dummy:
            result = ScoreResult.uniform(
                ScoringConfig.failed_reaction_scoring.value,
                failure_reason=FailureReason(
                    stage=FailureStage.PROCESSING,
                    category="ProcessingSentinel",
                    message="Reaction was marked as failed by upstream processing.",
                ),
            )
            return ScoreTrace(
                result=result,
                outcome=TraceOutcome.FAILED,
                canonical_smiles=canonical_smiles,
            )

        if reaction.is_sis_reaction:
            return ScoreTrace(
                result=ScoreResult.uniform(ScoringConfig.sis_reaction_scoring.value),
                outcome=TraceOutcome.SIS,
                canonical_smiles=canonical_smiles,
            )

        exact_real_precedents: tuple[PrecedentExample, ...] = ()
        exact_virtual_precedents: tuple[PrecedentExample, ...] = ()
        if self._find_exact_match and include_precedents:
            exact_real_precedents = _precedent_examples(
                self._manager.find_reaction_precedents(
                    reaction.canonical_smiles,
                    is_virtual=False,
                    limit=_PRECEDENT_EXAMPLE_LIMIT,
                )
            )
            exact_virtual_precedents = _precedent_examples(
                self._manager.find_reaction_precedents(
                    reaction.canonical_smiles,
                    is_virtual=True,
                    limit=_PRECEDENT_EXAMPLE_LIMIT,
                )
            )
            exact_match = bool(exact_real_precedents or exact_virtual_precedents)
        else:
            exact_match = bool(
                self._find_exact_match
                and self._manager.find_reaction(reaction.canonical_smiles)
            )
        exact_result = (
            ScoreResult.uniform(ScoringConfig.exact_match_scoring.value)
            if exact_match
            else None
        )
        if exact_result is not None and not include_precedents:
            return ScoreTrace(
                result=exact_result,
                outcome=TraceOutcome.EXACT_MATCH,
                canonical_smiles=canonical_smiles,
            )

        try:
            extracted = self._rc_extractor.extract_rc(reaction)
        except ExtractionError as error:
            if exact_result is not None:
                return ScoreTrace(
                    result=exact_result,
                    outcome=TraceOutcome.EXACT_MATCH,
                    canonical_smiles=canonical_smiles,
                    exact_real_precedents=exact_real_precedents,
                    exact_virtual_precedents=exact_virtual_precedents,
                )
            return ScoreTrace(
                result=_failed_result(FailureStage.EXTRACTION, error),
                outcome=TraceOutcome.FAILED,
                canonical_smiles=canonical_smiles,
            )

        if exact_result is not None:
            center_trace = self._trace_centers(
                extracted,
                canonical_smiles=canonical_smiles,
                include_precedents=True,
            )
            return replace(
                center_trace,
                result=exact_result,
                outcome=TraceOutcome.EXACT_MATCH,
                exact_real_precedents=exact_real_precedents,
                exact_virtual_precedents=exact_virtual_precedents,
            )

        if extracted.is_tautomerization_reaction:
            return ScoreTrace(
                result=ScoreResult.uniform(
                    ScoringConfig.tautomerization_reaction_scoring.value
                ),
                outcome=TraceOutcome.TAUTOMERIZATION,
                canonical_smiles=canonical_smiles,
            )

        return self._trace_centers(
            extracted,
            canonical_smiles=canonical_smiles,
            include_precedents=include_precedents,
        )

    def _score_centers(self, reaction: Reaction) -> ScoreResult:
        """Score the extracted reaction centers against the DB.

        Walks the centers in ascending type order, accumulating the with- and
        without-functional-groups scores in a single pass. A center counts for
        either variant only while the preceding centers also counted (the
        consecutive-prefix rule). Center presence prefers real rows, then
        virtual; the with-FG variant accepts bits covered by real and requires
        any remaining bits to appear in the virtual signature.

        FG counters refer to a single decisive center (outermost pass, or the
        first failure when none passed). ``all_fgs_precedents_are_real`` is an
        AND over the whole with-FG consecutive prefix: if any earlier center
        needed virtual fill-in to unlock a higher ``score_with_fg``, the flag
        stays ``False`` even when the outermost center is fully real.
        ``all_center_precedents_are_real`` is the analogous AND over the
        without-FG prefix: any virtual-only center in that chain flips it.

        :param reaction: Reaction with extracted, FG-annotated centers.
        :type reaction: Reaction
        :return: Both scoring variants plus FG- and center-precedent provenance.
        :rtype: ScoreResult
        """
        return self._trace_centers(
            reaction,
            canonical_smiles=reaction.canonical_smiles or reaction.reaction_smiles,
            include_precedents=False,
        ).result

    def _trace_centers(
        self,
        reaction: Reaction,
        *,
        canonical_smiles: str,
        include_precedents: bool,
    ) -> ScoreTrace:
        """Score extracted centers once while retaining traversal details."""
        default = ScoringConfig.default_reaction_scoring.value
        score_with_fg = default
        score_without_fg = default
        center_chain_alive = True
        fg_chain_alive = True
        total_fgs = 0
        fgs_from_virtual = 0
        fg_passed_any = False
        prefix_used_virtual_fg = False
        prefix_used_virtual_center = False
        chain_failed_at: ReactionCenterType | None = None
        center_chain_failed_at: ReactionCenterType | None = None
        center_traces: list[CenterTrace] = []
        precedent_sear_signature = (
            reaction.sear_signature if reaction.is_sear_reaction else None
        )

        for center_type, rc in sorted(
            reaction.reaction_centers.items(), key=itemgetter(0)
        ):
            resolved_center_type = ReactionCenterType(center_type)
            real_fg, virtual_fg = self._reference_fg_pair_for_center_scoring(
                reaction, rc
            )
            if real_fg is not None:
                precedent_status = PrecedentStatus.REAL
            elif virtual_fg is not None:
                precedent_status = PrecedentStatus.VIRTUAL
            else:
                precedent_status = PrecedentStatus.ABSENT

            center_present = precedent_status is not PrecedentStatus.ABSENT
            included_without_fg = center_chain_alive and center_present
            if included_without_fg:
                current_score = ScoringConfig.center_type_scoring(resolved_center_type)
                score_without_fg = max(score_without_fg, current_score)
                prefix_used_virtual_center = (
                    prefix_used_virtual_center
                    or precedent_status is PrecedentStatus.VIRTUAL
                )
            elif center_chain_alive:
                center_chain_alive = False
                center_chain_failed_at = resolved_center_type

            included_with_fg = False
            if fg_chain_alive and included_without_fg:
                covered, n_fgs, n_virtual_fgs = _fg_coverage_by_real_and_virtual(
                    rc.fg_signature,
                    real_fg,
                    virtual_fg,
                )
                if covered:
                    current_score = ScoringConfig.center_type_scoring(
                        resolved_center_type
                    )
                    score_with_fg = max(score_with_fg, current_score)
                    total_fgs = n_fgs
                    fgs_from_virtual = n_virtual_fgs
                    fg_passed_any = True
                    prefix_used_virtual_fg = prefix_used_virtual_fg or n_virtual_fgs > 0
                    included_with_fg = True
                else:
                    if not fg_passed_any:
                        total_fgs = n_fgs
                        fgs_from_virtual = 0
                    fg_chain_alive = False
                    chain_failed_at = resolved_center_type
            elif fg_chain_alive:
                fg_chain_alive = False
                chain_failed_at = resolved_center_type

            if include_precedents:
                if precedent_status is PrecedentStatus.ABSENT:
                    precedent_count = 0
                else:
                    precedent_count = self._manager.count_center(
                        rc.reaction_center_smiles,
                        is_virtual=precedent_status is PrecedentStatus.VIRTUAL,
                        sear_signature=precedent_sear_signature,
                    )

                real_signature = (
                    real_fg if real_fg is not None else np.zeros_like(rc.fg_signature)
                )
                virtual_signature = (
                    virtual_fg
                    if virtual_fg is not None
                    else np.zeros_like(rc.fg_signature)
                )
                combined_signature = np.maximum(real_signature, virtual_signature)
                missing_signature = rc.fg_signature * (1 - combined_signature)
                virtual_required_signature = (
                    rc.fg_signature * (1 - real_signature) * virtual_signature
                )

                real_precedents: tuple[PrecedentExample, ...] = ()
                virtual_precedents: tuple[PrecedentExample, ...] = ()
                if real_fg is not None:
                    real_precedents = _precedent_examples(
                        self._manager.find_center_precedents(
                            rc.reaction_center_smiles,
                            is_virtual=False,
                            limit=_PRECEDENT_EXAMPLE_LIMIT,
                            sear_signature=precedent_sear_signature,
                        )
                    )
                if virtual_fg is not None:
                    virtual_precedents = _precedent_examples(
                        self._manager.find_center_precedents(
                            rc.reaction_center_smiles,
                            is_virtual=True,
                            limit=_PRECEDENT_EXAMPLE_LIMIT,
                            sear_signature=precedent_sear_signature,
                        )
                    )
                evidence_items: list[FunctionalGroupEvidence] = []
                for fg_index in np.flatnonzero(rc.fg_signature):
                    resolved_fg_index = int(fg_index)
                    real_fg_precedents: tuple[PrecedentExample, ...] = ()
                    virtual_fg_precedents: tuple[PrecedentExample, ...] = ()
                    if real_signature[resolved_fg_index]:
                        real_fg_precedents = _precedent_examples(
                            self._manager.find_center_fg_precedents(
                                rc.reaction_center_smiles,
                                resolved_fg_index,
                                is_virtual=False,
                                limit=_PRECEDENT_EXAMPLE_LIMIT,
                                sear_signature=precedent_sear_signature,
                            )
                        )
                    if virtual_signature[resolved_fg_index]:
                        virtual_fg_precedents = _precedent_examples(
                            self._manager.find_center_fg_precedents(
                                rc.reaction_center_smiles,
                                resolved_fg_index,
                                is_virtual=True,
                                limit=_PRECEDENT_EXAMPLE_LIMIT,
                                sear_signature=precedent_sear_signature,
                            )
                        )
                    fg_name, fg_ui_name, fg_smarts = _functional_group_descriptor(
                        resolved_fg_index
                    )
                    evidence_items.append(
                        FunctionalGroupEvidence(
                            name=fg_name,
                            ui_name=fg_ui_name,
                            smarts=fg_smarts,
                            real_precedents=real_fg_precedents,
                            virtual_precedents=virtual_fg_precedents,
                        )
                    )

                center_traces.append(
                    CenterTrace(
                        center_type=resolved_center_type,
                        reaction_center_smiles=rc.reaction_center_smiles,
                        precedent_status=precedent_status,
                        precedent_count=precedent_count,
                        required_functional_groups=_functional_group_names(
                            rc.fg_signature
                        ),
                        missing_functional_groups=_functional_group_names(
                            missing_signature
                        ),
                        virtual_functional_groups=_functional_group_names(
                            virtual_required_signature
                        ),
                        included_without_functional_groups=included_without_fg,
                        included_with_functional_groups=included_with_fg,
                        real_precedents=real_precedents,
                        virtual_precedents=virtual_precedents,
                        functional_group_evidence=tuple(evidence_items),
                    )
                )

            if not include_precedents and not center_chain_alive and not fg_chain_alive:
                break

        result = ScoreResult(
            with_functional_groups=score_with_fg,
            without_functional_groups=score_without_fg,
            all_fgs_precedents_are_real=not prefix_used_virtual_fg,
            total_number_of_fgs=total_fgs,
            number_of_fgs_covered_by_virtual_precedents=fgs_from_virtual,
            all_center_precedents_are_real=not prefix_used_virtual_center,
        )
        if score_without_fg > default:
            outcome = TraceOutcome.CENTER_COVERAGE
        else:
            outcome = TraceOutcome.NO_COVERAGE
        return ScoreTrace(
            result=result,
            outcome=outcome,
            centers=tuple(center_traces),
            chain_failed_at=chain_failed_at,
            center_chain_failed_at=center_chain_failed_at,
            canonical_smiles=canonical_smiles,
        )

    def score(self, reaction_smiles: str) -> float:
        """Score a reaction, honoring this instance's ``check_functional_groups``.

        Thin wrapper over :meth:`evaluate` for callers that want a single score.

        :param reaction_smiles: Reaction SMILES string to score.
        :type reaction_smiles: str
        :return: Score from config (exact_match / lc_N / default / failed).
        :rtype: float
        """
        return self.evaluate(reaction_smiles).select(self._check_functional_groups)

    def score_reaction(self, reaction: Reaction) -> float:
        """Score a :class:`~chemcensor.basic.Reaction`, honoring
        ``check_functional_groups``.

        Use with the FakeMapper alpha pipeline when atom maps are attached via
        ``Reaction.meta``.

        :param reaction: Reaction to process and score.
        :type reaction: Reaction
        :return: Score from config (exact_match / lc_N / default / failed).
        :rtype: float
        """
        return self.evaluate_reaction(reaction).select(self._check_functional_groups)

    def score_processed(self, reaction: Reaction) -> float:
        """Score an already-processed reaction, honoring ``check_functional_groups``.

        Thin wrapper over :meth:`evaluate_processed`.

        :param reaction: Reaction already processed by a
            :class:`~chemcensor.processing.reaction_processor.ReactionProcessor`.
        :type reaction: Reaction
        :return: Score from config (exact_match / lc_N / default / failed).
        :rtype: float
        """
        return self.evaluate_processed(reaction).select(self._check_functional_groups)
