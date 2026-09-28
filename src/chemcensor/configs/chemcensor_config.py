from __future__ import annotations

from dataclasses import dataclass

from ..processing.reaction_processor import build_processors
from ..processing.reaction_processor import ReactionProcessor


@dataclass(frozen=True, slots=True)
class ChemCensorConfig:
    """Configuration for :class:`~chemcensor.chemcensor.ChemCensor`.

    Bundles scoring knobs and the processing pipeline variant so an external
    caller can construct ChemCensor in one place — for example switching to
    the alpha pipeline that uses :class:`~chemcensor.processing.fake_mapper.FakeMapper`
    instead of :class:`~chemcensor.processing.mapper.Mapper`, or disabling
    individual validators that are on by default.

    :ivar max_center_type: Maximum reaction-center type to extract (1–4).
    :ivar find_exact_match: When ``True``, a canonical-SMILES hit in the DB
        returns ``exact_match_scoring`` before reaction-center lookup.
    :ivar check_functional_groups: When ``True``,
        :meth:`~chemcensor.chemcensor.ChemCensor.score` returns the
        functional-group-aware variant from
        :class:`~chemcensor.chemcensor.ScoreResult`.
    :ivar use_fake_mapper: When ``True``, build a pipeline with
        :class:`~chemcensor.processing.fake_mapper.FakeMapper` (precomputed
        atom maps in ``Reaction.meta``) instead of rxnmapper-backed
        :class:`~chemcensor.processing.mapper.Mapper`. The reaction-SMILES
        length check is disabled, matching the parallel alpha path.
    :ivar mapper_in_subprocess: When ``True``, omit the mapper stage from the
        built pipeline because atom mapping runs in a dedicated subprocess (the
        parallel scoring worker). All validators stay identical to the
        single-process pipeline.
    :ivar use_cpu: When ``True``, hide CUDA before constructing the
        rxnmapper-backed mapper so atom mapping runs on CPU. No effect when
        ``use_fake_mapper`` or ``mapper_in_subprocess`` is ``True``.
    :ivar mapper_batch_size: Optional internal rxnmapper batch size. ``None``
        uses the mapper default.
    :ivar mapper_n_jobs: OMP thread default passed to the mapper. Existing
        host ``OMP_NUM_THREADS`` values remain unchanged.
    :ivar validate_input: When ``True`` (default), run the preliminary
        :class:`~chemcensor.processing.validator.Validator` (syntax / RDKit /
        carbon / optional length).
    :ivar check_skeleton_conservation: When ``True`` (default), run
        :class:`~chemcensor.processing.skeleton_conservation_validator.SkeletonConservationValidator`.
    :ivar check_static_stereo: When ``True`` (default), run
        :class:`~chemcensor.processing.static_stereo_validator.StaticStereoValidator`.
    """

    max_center_type: int = 4
    find_exact_match: bool = True
    check_functional_groups: bool = True
    use_fake_mapper: bool = False
    mapper_in_subprocess: bool = False
    use_cpu: bool = False
    mapper_batch_size: int | None = None
    mapper_n_jobs: int = 1
    validate_input: bool = True
    check_skeleton_conservation: bool = True
    check_static_stereo: bool = True

    def build_processor(self) -> ReactionProcessor:
        """Return a :class:`~chemcensor.processing.reaction_processor.ReactionProcessor`
        for this configuration.

        :return: Processor pipeline (default, FakeMapper-backed, or without the
            mapper stage for the parallel scoring worker).
        :rtype: ReactionProcessor
        """
        return ReactionProcessor(
            processors=build_processors(
                use_fake_mapper=self.use_fake_mapper,
                include_mapper=not self.mapper_in_subprocess,
                use_cpu=self.use_cpu,
                mapper_batch_size=self.mapper_batch_size,
                mapper_n_jobs=self.mapper_n_jobs,
                validate_input=self.validate_input,
                check_skeleton_conservation=self.check_skeleton_conservation,
                check_static_stereo=self.check_static_stereo,
            )
        )
