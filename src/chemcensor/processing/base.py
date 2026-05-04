from typing import Protocol
from typing import Sequence

from ..basic import Reaction
from ..basic import SENTINEL
from .errors.processing_errors import ProcessingError


class Processor(Protocol):
    """Protocol for reaction processors."""

    def process(self, reaction: Reaction) -> Reaction:
        """Process reaction.

        :param reaction: Reaction to process
        :type reaction: Reaction

        :return: Processed reaction
        :rtype: Reaction
        """
        ...

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        """Process batch of reactions. Mainly for DB composition.

        Dummy reactions (sentinels) are passed through unchanged.
        If ``process`` raises a ``ProcessingError``, the corresponding
        reaction is replaced with the SENTINEL.

        :param reactions: Batch of reactions to process
        :type reactions: Sequence[Reaction]

        :return: Processed batch of reactions
        :rtype: Sequence[Reaction]
        """
        ...


def process_batch(reactions: Sequence[Reaction], processor) -> Sequence[Reaction]:
    """Process a batch of reactions through a sequence of processors.
    Repeated in all processors except for the mapper.

    :param reactions: Batch of reactions to process
    :type reactions: Sequence[Reaction]

    :return: Processed batch of reactions
    :rtype: Sequence[Reaction]
    """
    return tuple[Reaction, ...](
        reaction if reaction.dummy else _safe_process(reaction, processor)
        for reaction in reactions
    )


def _safe_process(reaction: Reaction, processor: Processor) -> Reaction:
    """Process reaction safely.

    :param reaction: Reaction to process
    :type reaction: Reaction
    :param processor: Processor to use
    :type processor: Processor

    :return: Processed reaction or SENTINEL if processing fails
    :rtype: Reaction
    """
    try:
        return processor.process(reaction)
    except ProcessingError:
        return SENTINEL
