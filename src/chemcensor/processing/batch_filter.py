from typing import Sequence

from ..basic import Reaction


class BatchFilter:
    """Filters out invalid (sentinel/dummy) reactions from a batch.

    Intended to be placed at the end of the processing pipeline
    to strip sentinel placeholders and return only valid reactions
    ready for reaction center extraction.
    """

    def process(self, reaction: Reaction) -> Reaction:
        """Pass-through for single reactions.

        :param reaction: Reaction to process
        :type reaction: Reaction

        :return: The same reaction, unchanged
        :rtype: Reaction
        """
        return reaction

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        """Remove all dummy (sentinel) reactions from the batch.

        :param reactions: Batch of reactions, potentially containing sentinels
        :type reactions: Sequence[Reaction]

        :return: Only the valid (non-dummy) reactions
        :rtype: Sequence[Reaction]
        """
        return tuple(reaction for reaction in reactions if not reaction.dummy)
