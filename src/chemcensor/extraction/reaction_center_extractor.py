from dataclasses import replace
from typing import Sequence

from ..basic import Reaction
from ..basic import ReactionCenterType
from ..basic import SENTINEL
from ..basic.errors.fg_finder_errors import FGFinderError
from ..rules import FG_COLLECTION_GENERAL
from ..rules import FG_COLLECTION_SEAR
from ..rules import TAUTOMERIZATION_RCS
from .errors import ExtractionError
from .errors import ReactionCenterExtractorError
from .extractor import Extractor
from .fg_finder import FGFinder


class ReactionCenterExtractor:
    """Extracts reaction centers from reactions and
    annotates them with functional groups."""

    def __init__(self, max_center_type: ReactionCenterType) -> None:
        """Initialize the reaction center extractor.

        :param max_center_type: The maximum center type to extract (RC1-RC4).
        :type max_center_type: ReactionCenterType
        """
        self.max_center_type = max_center_type
        self.extractor = Extractor(max_center_type=max_center_type)
        self.fg_finder_general = FGFinder(fg_collection=FG_COLLECTION_GENERAL)
        self.fg_finder_sear = FGFinder(fg_collection=FG_COLLECTION_SEAR)
        self.tautomerization_rcs = TAUTOMERIZATION_RCS

    def _is_tautomerization_reaction(self, reaction: Reaction) -> bool:
        """Check if the reaction is a tautomerization reaction.

        :param reaction: Reaction to check.
        :type reaction: Reaction
        :return: True if the reaction is a tautomerization reaction, False otherwise.
        :rtype: bool
        """
        rc_1 = reaction.get_reaction_center_by_type(ReactionCenterType.RC1)
        return rc_1.reaction_center_smiles in self.tautomerization_rcs

    def extract_rc(self, reaction: Reaction) -> Reaction:
        """Extract reaction centers from reaction and annotate them.

        1. Extract reaction centers
        2. Check if the reaction is a tautomerization reaction
           Set is_tautomerization_reaction flag to True
           No need to find functional groups for tautomerization reactions
        3. Select functional group finder based on reaction type
        4. Annotate reaction centers with functional groups

        :param reaction: Reaction to extract reaction centers from.
        :type reaction: Reaction
        :return: Reaction with extracted reaction centers and annotated
                 functional groups.
        :rtype: Reaction
        :raises ExtractionError: If the reaction cannot be extracted.
        :raises FGFinderError: If the functional groups cannot be found.
        """

        # Extract reaction centers
        try:
            reaction = self.extractor.extract_rc(reaction)
        except ExtractionError as e:
            raise ReactionCenterExtractorError(
                f"Reaction center extraction has failed: {e}"
            ) from e

        # Check if the reaction is a tautomerization reaction
        # No need to find functional groups for tautomerization reactions
        if self._is_tautomerization_reaction(reaction):
            return replace(reaction, is_tautomerization_reaction=True)

        # Annotate reaction centers with functional groups
        try:
            reaction = self.fg_finder_general.find(reaction)
            if reaction.is_sear_reaction:
                reaction = self.fg_finder_sear.find(reaction)
        except FGFinderError as e:
            raise ReactionCenterExtractorError(e) from e

        return reaction

    def extract_rc_for_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        """Extract reaction centers for a batch of reactions.

        Dummy reactions (sentinels) are passed through unchanged.
        If ``extract_rc`` raises an ``ExtractionError``, the corresponding
        reaction is replaced with the SENTINEL.

        :param reactions: Batch of reactions to process.
        :type reactions: Sequence[Reaction]
        :return: Processed batch of reactions.
        :rtype: Sequence[Reaction]
        """
        return tuple(
            reaction if reaction.dummy else _safe_extract_rc(reaction, self)
            for reaction in reactions
        )


def _safe_extract_rc(
    reaction: Reaction, extractor: ReactionCenterExtractor
) -> Reaction:
    """Run extract_rc; on ExtractionError return SENTINEL.

    :param reaction: Reaction to extract reaction centers from.
    :type reaction: Reaction
    :param extractor: Reaction center extractor.
    :type extractor: ReactionCenterExtractor
    :return: Reaction with extracted reaction centers.
    :rtype: Reaction
    """
    try:
        return extractor.extract_rc(reaction)
    except ExtractionError:
        return SENTINEL
