from typing import cast
from typing import Sequence

from ..basic import Reaction
from ..rules.functional_groups import FG_COLLECTION_SEAR
from .base import Processor
from .cano_rxn_annotator import CanoRxnAnnotator
from .mapper import Mapper
from .orphan_remover import OrphanRemover
from .sear_annotator import SeArAnnotator
from .sis_annotator import SisAnnotator
from .static_stereo_validator import StaticStereoValidator
from .transform_creator import TransformCreator
from .validator import Validator

DEFAULT_PROCESSORS: Sequence[Processor] = cast(
    Sequence[Processor],
    (
        Validator(),
        Mapper(),
        OrphanRemover(),
        TransformCreator(),
        CanoRxnAnnotator(),
        SisAnnotator(),
        StaticStereoValidator(),
        SeArAnnotator(FG_COLLECTION_SEAR),
    ),
)


class ReactionProcessor:
    """
    ReactionProcessor that processes reactions through
    a sequence of processors.
    """

    processors: Sequence[Processor]

    def __init__(
        self,
        processors: Sequence[Processor] = (),
    ) -> None:
        """
        Initialize ReactionProcessor with processors.

        :param processors: Sequence of Processors to use.
        :type processors: Sequence[Processor]
        """
        self.processors = processors or DEFAULT_PROCESSORS

    def process(self, reaction: Reaction) -> Reaction:
        """
        Process reaction through all registered processors sequentially.

        :param reaction: Reaction to process
        :type reaction: Reaction

        :return: Processed reaction after applying all processors
        :rtype: Reaction
        """
        for processor in self.processors:
            reaction = processor.process(reaction)
        return reaction

    def process_batch(self, reactions: Sequence[Reaction]) -> Sequence[Reaction]:
        """
        Process a batch of reactions through all registered processors sequentially.

        Dummy reactions (sentinels) are passed through by each processor,
        keeping the batch size constant.

        :param reactions: Batch of reactions to process
        :type reactions: Sequence[Reaction]

        :return: Processed batch of reactions after applying all processors
        :rtype: Sequence[Reaction]
        """
        for processor in self.processors:
            reactions = processor.process_batch(reactions)
        return reactions
