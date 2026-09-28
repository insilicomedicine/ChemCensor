from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

from ..processing.reaction_processor import build_processors
from ..processing.reaction_processor import ReactionProcessor


class CompositionConfig(IntEnum):
    """Configuration for database composition.

    Specifies two parameters: batch_size and distributivity
    threshold. The latter one determines how many reaction examples
    the multi-component center should have for applying
    distributivity of its FG bits based on bits from individual
    components
    """

    default_batch_size = 32
    distributivity_threshold = 2


@dataclass(frozen=True, slots=True)
class CompositionPipelineConfig:
    """Configuration for the DB-composition processing pipeline.

    Composition variant counterpart of
    :class:`~chemcensor.configs.chemcensor_config.ChemCensorConfig`: it fixes the
    flag combination passed to
    :func:`~chemcensor.processing.reaction_processor.build_processors` so that
    every composition entry point (serial script, parallel worker, tests) is
    derived from the same factory and shares an identical validator set.

    :ivar use_fake_mapper: When ``True``, use
        :class:`~chemcensor.processing.fake_mapper.FakeMapper` (precomputed atom
        maps) instead of the rxnmapper-backed
        :class:`~chemcensor.processing.mapper.Mapper`, and disable the
        reaction-SMILES length check.
    :ivar mapper_in_subprocess: When ``True`` (parallel worker), omit the mapper
        stage (mapping runs in a dedicated subprocess) and the ``BatchFilter``
        stage (dummies are dropped explicitly while preserving the input
        ``idx``). When ``False`` (serial composition), both stages are included.
    :ivar mapper_batch_size: Batch size for the rxnmapper-backed ``Mapper``;
        ignored when ``mapper_in_subprocess`` or ``use_fake_mapper`` is ``True``.
    :ivar use_cpu: When ``True``, hide CUDA before constructing the
        rxnmapper-backed mapper so atom mapping runs on CPU. Ignored when
        ``mapper_in_subprocess`` or ``use_fake_mapper`` is ``True``.
    :ivar validate_input: When ``True`` (default), run the preliminary
        :class:`~chemcensor.processing.validator.Validator`.
    :ivar check_skeleton_conservation: When ``True`` (default), run
        :class:`~chemcensor.processing.skeleton_conservation_validator.SkeletonConservationValidator`.
    :ivar check_static_stereo: When ``True`` (default), run
        :class:`~chemcensor.processing.static_stereo_validator.StaticStereoValidator`.
    """

    use_fake_mapper: bool = False
    mapper_in_subprocess: bool = False
    mapper_batch_size: int = int(CompositionConfig.default_batch_size)
    use_cpu: bool = False
    validate_input: bool = True
    check_skeleton_conservation: bool = True
    check_static_stereo: bool = True

    def build_processor(self) -> ReactionProcessor:
        """Return the composition
        :class:`~chemcensor.processing.reaction_processor.ReactionProcessor`.

        :return: Processor pipeline for serial or parallel-worker composition.
        :rtype: ReactionProcessor
        """
        in_process = not self.mapper_in_subprocess
        return ReactionProcessor(
            processors=build_processors(
                use_fake_mapper=self.use_fake_mapper,
                include_mapper=in_process,
                include_batch_filter=in_process,
                mapper_batch_size=self.mapper_batch_size,
                use_cpu=self.use_cpu,
                validate_input=self.validate_input,
                check_skeleton_conservation=self.check_skeleton_conservation,
                check_static_stereo=self.check_static_stereo,
            )
        )
