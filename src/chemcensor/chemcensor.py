from dataclasses import dataclass
from operator import itemgetter
from os import PathLike

import numpy as np

from .basic import Reaction
from .basic import ReactionCenter
from .basic import ReactionCenterType
from .configs.scoring_configs import ScoringConfig
from .db.manager import DBManager
from .errors import InvalidCenterTypeError
from .extraction import ReactionCenterExtractor
from .extraction.errors import ExtractionError
from .processing.errors import ProcessingError
from .processing.reaction_processor import ReactionProcessor


def _fg_subsignature_matches(rc_fg: np.ndarray, ref_fg: np.ndarray) -> bool:
    """True if every 1-bit in *rc_fg* is also set in *ref_fg*."""
    return bool(np.sum(rc_fg - ref_fg * rc_fg) == 0)


@dataclass(frozen=True)
class ScoreResult:
    """Outcome of scoring a single reaction.

    Holds both scoring variants so a caller can obtain the functional-group
    aware and functional-group agnostic scores from a single evaluation.

    :param with_functional_groups: Score requiring each reaction center's
        functional-group sub-signature to match the DB reference.
    :type with_functional_groups: float
    :param without_functional_groups: Score based on reaction-center presence
        in the DB only, ignoring the functional-group comparison.
    :type without_functional_groups: float
    """

    with_functional_groups: float
    without_functional_groups: float

    @classmethod
    def uniform(cls, value: float) -> "ScoreResult":
        """Build a result where both variants share the same ``value``.

        Used for outcomes decided before the per-center loop (failed, SIS,
        exact match, tautomerization), which do not depend on functional groups.

        :param value: Score assigned to both variants.
        :type value: float
        :return: A :class:`ScoreResult` with identical variants.
        :rtype: ScoreResult
        """
        return cls(with_functional_groups=value, without_functional_groups=value)

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


class ChemCensor:
    """Public API for reaction scoring.

    User only supplies the reaction centers database (path or manager).
    Processing pipeline and extraction are created internally.
    """

    def __init__(
        self,
        *,
        db_path: str | PathLike | None = None,
        manager: DBManager | None = None,
        max_center_type: int | ReactionCenterType = 4,
        find_exact_match: bool = True,
        check_functional_groups: bool = True,
        processor: ReactionProcessor | None = None,
    ) -> None:
        """Initialize ChemCensor from a database path or an existing DBManager.

        Exactly one of ``db_path`` or ``manager`` must be provided.

        :param db_path: Path to the SQLite reaction-centers database (loaded on init).
        :type db_path: str | PathLike | None
        :param manager: Pre-built DBManager instance (e.g. for tests or custom load).
        :type manager: DBManager | None
        :param max_center_type: Maximum reaction-center type to extract (1–4).
        :type max_center_type: int | ReactionCenterType
        :param find_exact_match: If ``True`` (default), look up the reaction's
            canonical SMILES in the DB first and return ``exact_match_scoring``
            on hit. Set to ``False`` to skip this check and always score via
            reaction centers.
        :type find_exact_match: bool
        :param check_functional_groups: If ``True`` (default), a reaction center
            only counts as a match when its functional-group sub-signature is
            contained in the reference signature from the DB. Set to ``False``
            to score purely on reaction-center presence in the DB, ignoring the
            functional-group comparison.
        :type check_functional_groups: bool
        :param processor: Optional pre-built :class:`ReactionProcessor`. When
            omitted, a default pipeline including
            :class:`~chemcensor.processing.Mapper` is created. Pass a custom
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
            raise ValueError("Provide db_path or manager")

        try:
            max_center_type = ReactionCenterType(max_center_type)
        except ValueError:
            raise InvalidCenterTypeError(max_center_type) from None

        self._processor = processor if processor is not None else ReactionProcessor()
        self._rc_extractor = ReactionCenterExtractor(max_center_type=max_center_type)
        self._find_exact_match = find_exact_match
        self._check_functional_groups = check_functional_groups

    def _reference_fg_for_center_scoring(
        self, reaction: Reaction, rc: ReactionCenter
    ) -> np.ndarray | None:
        """FG signature from the DB used to validate *rc* for scoring.

        Non-SEAr: global signature from ``reaction_centers``. SEAr: rows in
        ``centers_to_reactions`` matching ``reaction.sear_signature`` (after
        confirming at least one such row exists).
        """
        if reaction.is_sear_reaction:
            if not self._manager.has_center_sear_in_bridge(
                rc.reaction_center_smiles,
                reaction.sear_signature,
            ):
                return None
            return self._manager.aggregate_fg_signature_for_center_sear(
                rc.reaction_center_smiles,
                reaction.sear_signature,
            )
        return self._manager.find_center(rc.reaction_center_smiles)

    def evaluate(self, reaction_smiles: str) -> ScoreResult:
        """Evaluate a reaction, returning both functional-group score variants.

        1. Process reaction (validate, map, orphans, transform, canonicalize,
           SIS / SeAr annotation).
        2. Extract reaction centers and annotate FGs.
        3. Look up each extracted center in the DB and score it.

        The (expensive) pipeline runs once; the with- and without-functional
        -groups scores are derived together (see :class:`ScoreResult`).

        :param reaction_smiles: Reaction SMILES string to score.
        :type reaction_smiles: str
        :return: Both scoring variants for the reaction.
        :rtype: ScoreResult
        """
        reaction = Reaction(reaction_smiles=reaction_smiles)

        try:
            reaction = self._processor.process(reaction)
        except ProcessingError:
            return ScoreResult.uniform(ScoringConfig.failed_reaction_scoring.value)

        return self.evaluate_processed(reaction)

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
        if reaction.dummy:
            return ScoreResult.uniform(ScoringConfig.failed_reaction_scoring.value)

        if reaction.is_sis_reaction:
            return ScoreResult.uniform(ScoringConfig.sis_reaction_scoring.value)

        if (
            self._find_exact_match
            and self._manager.find_reaction(reaction.canonical_smiles) is not None
        ):
            return ScoreResult.uniform(ScoringConfig.exact_match_scoring.value)

        try:
            reaction = self._rc_extractor.extract_rc(reaction)
        except ExtractionError:
            return ScoreResult.uniform(ScoringConfig.failed_reaction_scoring.value)

        if reaction.is_tautomerization_reaction:
            return ScoreResult.uniform(
                ScoringConfig.tautomerization_reaction_scoring.value
            )

        return self._score_centers(reaction)

    def _score_centers(self, reaction: Reaction) -> ScoreResult:
        """Score the extracted reaction centers against the DB.

        Walks the centers in ascending type order, accumulating the with- and
        without-functional-groups scores in a single pass. A center counts for
        either variant only while the preceding centers also counted (the
        consecutive-prefix rule). Center presence in the DB is required by both
        variants; only the with-FG variant additionally requires the FG
        sub-signature to match.

        :param reaction: Reaction with extracted, FG-annotated centers.
        :type reaction: Reaction
        :return: Both scoring variants.
        :rtype: ScoreResult
        """
        default = ScoringConfig.default_reaction_scoring.value
        score_with_fg = default
        score_without_fg = default
        fg_chain_alive = True

        for center_type, rc in sorted(
            reaction.reaction_centers.items(), key=itemgetter(0)
        ):
            ref_fg = self._reference_fg_for_center_scoring(reaction, rc)
            if ref_fg is None:
                break

            current_score = ScoringConfig[f"lc_{center_type}_scoring"].value
            score_without_fg = max(score_without_fg, current_score)

            if fg_chain_alive and _fg_subsignature_matches(rc.fg_signature, ref_fg):
                score_with_fg = max(score_with_fg, current_score)
            else:
                fg_chain_alive = False

        return ScoreResult(
            with_functional_groups=score_with_fg,
            without_functional_groups=score_without_fg,
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
