from typing import cast
from typing import Sequence

from ..basic import Reaction
from ..rules.functional_groups import FG_COLLECTION_SEAR
from .base import Processor
from .batch_filter import BatchFilter
from .cano_rxn_annotator import CanoRxnAnnotator
from .fake_mapper import FakeMapper
from .mapper import Mapper
from .orphan_remover import OrphanRemover
from .sear_annotator import SeArAnnotator
from .sis_annotator import SisAnnotator
from .skeleton_conservation_validator import SkeletonConservationValidator
from .static_stereo_validator import StaticStereoValidator
from .transform_creator import TransformCreator
from .validator import Validator


def build_processors(
    *,
    use_fake_mapper: bool = False,
    include_mapper: bool = True,
    include_batch_filter: bool = False,
    mapper_batch_size: int | None = None,
    mapper_n_jobs: int = 1,
    use_cpu: bool = False,
    validate_input: bool = True,
    check_skeleton_conservation: bool = True,
    check_static_stereo: bool = True,
) -> Sequence[Processor]:
    """Build a reaction-processing pipeline.

    This is the single source of truth for the ordered processor list shared by
    the scoring path and every DB-composition path. The stages that legitimately
    differ between those paths are expressed as flags rather than by
    hand-rolling separate tuples, so the set of *validators* (and their order)
    stays identical everywhere.

    .. note::
        This is the low-level factory. Application code should not call it
        directly — use
        :class:`~chemcensor.configs.chemcensor_config.ChemCensorConfig` (scoring)
        or
        :class:`~chemcensor.configs.composition_configs.CompositionPipelineConfig`
        (DB composition), which fix the correct flag combination for each use
        case and route through this factory.

    :param use_fake_mapper: When ``True``, use
        :class:`~chemcensor.processing.fake_mapper.FakeMapper` (precomputed atom
        maps in ``Reaction.meta``) instead of the rxnmapper-backed
        :class:`~chemcensor.processing.mapper.Mapper`, and disable the
        reaction-SMILES length check (it only bounds rxnmapper inputs). Has no
        effect on the mapper stage when ``include_mapper`` is ``False``, but
        still governs the length check when ``validate_input`` is ``True``.
    :type use_fake_mapper: bool
    :param include_mapper: When ``True`` (default), insert the mapper stage.
        Set ``False`` for the parallel composition worker, where mapping runs in
        a separate subprocess.
    :type include_mapper: bool
    :param include_batch_filter: When ``True``, append
        :class:`~chemcensor.processing.batch_filter.BatchFilter` at the end.
        Used by DB composition; off for scoring.
    :type include_batch_filter: bool
    :param mapper_batch_size: Optional batch size for the rxnmapper-backed
        :class:`~chemcensor.processing.mapper.Mapper`. Ignored when
        ``use_fake_mapper`` is ``True`` or ``include_mapper`` is ``False``.
        ``None`` uses the ``Mapper`` default.
    :type mapper_batch_size: int | None
    :param mapper_n_jobs: OMP thread default passed to the rxnmapper-backed
        mapper.
    :type mapper_n_jobs: int
    :param use_cpu: When ``True``, construct the rxnmapper-backed
        :class:`~chemcensor.processing.mapper.Mapper` with CUDA hidden so
        mapping runs on CPU. Ignored when ``use_fake_mapper`` is ``True``
        or ``include_mapper`` is ``False``.
    :type use_cpu: bool
    :param validate_input: When ``True`` (default), prepend
        :class:`~chemcensor.processing.validator.Validator` (syntax, RDKit,
        carbon, and optionally length).
    :type validate_input: bool
    :param check_skeleton_conservation: When ``True`` (default), include
        :class:`~chemcensor.processing.skeleton_conservation_validator.SkeletonConservationValidator`.
    :type check_skeleton_conservation: bool
    :param check_static_stereo: When ``True`` (default), include
        :class:`~chemcensor.processing.static_stereo_validator.StaticStereoValidator`.
    :type check_static_stereo: bool
    :return: Ordered processor sequence.
    :rtype: Sequence[Processor]
    """
    processors: list[Processor] = []

    if validate_input:
        processors.append(Validator(check_length=not use_fake_mapper))

    if include_mapper:
        if use_fake_mapper:
            processors.append(FakeMapper())
        elif mapper_batch_size is not None:
            processors.append(
                Mapper(
                    batch_size=mapper_batch_size,
                    n_jobs=mapper_n_jobs,
                    use_cpu=use_cpu,
                )
            )
        else:
            processors.append(Mapper(n_jobs=mapper_n_jobs, use_cpu=use_cpu))

    processors.extend(
        (
            OrphanRemover(),
            TransformCreator(),
        )
    )

    if check_skeleton_conservation:
        processors.append(SkeletonConservationValidator())

    processors.append(CanoRxnAnnotator())
    processors.append(SisAnnotator())

    if check_static_stereo:
        processors.append(StaticStereoValidator())

    processors.append(SeArAnnotator(FG_COLLECTION_SEAR))

    if include_batch_filter:
        processors.append(BatchFilter())

    return cast(Sequence[Processor], tuple(processors))


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

        When ``processors`` is empty, the default rxnmapper-backed pipeline
        from :func:`build_processors` is used. Prefer
        :meth:`~chemcensor.configs.chemcensor_config.ChemCensorConfig.build_processor`
        when configuring ChemCensor (including FakeMapper).

        :param processors: Sequence of Processors to use.
        :type processors: Sequence[Processor]
        """
        self.processors = processors or build_processors()

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
