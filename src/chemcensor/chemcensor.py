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

    def score(self, reaction_smiles: str) -> float:
        """Score a reaction by checking if its reaction centers are in the database.

        1. Process reaction (validate, map, orphans, transform, canonicalize,
           SIS / SeAr annotation).
        2. Extract reaction centers and annotate FGs.
        3. Look up each extracted center in the DB; return the maximum score
           among those found.

        :param reaction_smiles: Reaction SMILES string to score.
        :type reaction_smiles: str
        :return: Score from config (exact_match / lc_N / default / failed).
        :rtype: float
        """

        reaction = Reaction(reaction_smiles=reaction_smiles)

        try:
            reaction = self._processor.process(reaction)
        except ProcessingError:
            return ScoringConfig.failed_reaction_scoring.value

        return self.score_processed(reaction)

    def score_processed(self, reaction: Reaction) -> float:
        """Score a reaction that already went through processing.

        Use this when the processing pipeline has been split across
        processes — for example in the parallel scorer worker, where atom
        mapping happens in a dedicated mapper process and the lightweight
        processor in the worker continues from
        :class:`~chemcensor.processing.OrphanRemover` onwards.

        Performs steps 2 and 3 of :meth:`score`: optional exact-match
        lookup, reaction-center extraction and DB-based scoring.

        :param reaction: Reaction that has already been processed by a
            :class:`~chemcensor.processing.reaction_processor.ReactionProcessor`
            (i.e. it has ``canonical_smiles`` populated, SIS / tautomer
            flags set, etc.).
        :type reaction: Reaction
        :return: Score from config (exact_match / lc_N / default / failed).
        :rtype: float
        """
        if reaction.dummy:
            return ScoringConfig.failed_reaction_scoring.value

        if reaction.is_sis_reaction:
            return ScoringConfig.sis_reaction_scoring.value

        if (
            self._find_exact_match
            and self._manager.find_reaction(reaction.canonical_smiles) is not None
        ):
            return ScoringConfig.exact_match_scoring.value

        try:
            reaction = self._rc_extractor.extract_rc(reaction)
        except ExtractionError:
            return ScoringConfig.failed_reaction_scoring.value

        if reaction.is_tautomerization_reaction:
            return ScoringConfig.tautomerization_reaction_scoring.value

        score: float = ScoringConfig.default_reaction_scoring.value
        for center_type, rc in sorted(
            reaction.reaction_centers.items(), key=itemgetter(0)
        ):
            ref_fg = self._reference_fg_for_center_scoring(reaction, rc)
            if ref_fg is None or not _fg_subsignature_matches(rc.fg_signature, ref_fg):
                break

            current_score = ScoringConfig[f"lc_{center_type}_scoring"].value
            score = current_score if current_score > score else score

        return score
