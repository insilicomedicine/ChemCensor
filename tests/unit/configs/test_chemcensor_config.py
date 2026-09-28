import os

from chemcensor.configs.chemcensor_config import ChemCensorConfig
from chemcensor.configs.composition_configs import CompositionPipelineConfig
from chemcensor.processing.fake_mapper import FakeMapper
from chemcensor.processing.mapper import Mapper
from chemcensor.processing.skeleton_conservation_validator import (
    SkeletonConservationValidator,
)
from chemcensor.processing.static_stereo_validator import StaticStereoValidator
from chemcensor.processing.utils import length_check
from chemcensor.processing.validator import Validator


def _processor_types(
    config: ChemCensorConfig | CompositionPipelineConfig,
) -> list[type]:
    return [type(p) for p in config.build_processor().processors]


def test_default_config_uses_mapper() -> None:
    processors = ChemCensorConfig().build_processor().processors
    assert isinstance(processors[0], Validator)
    assert length_check in processors[0].validators
    assert isinstance(processors[1], Mapper)


def test_fake_mapper_config_uses_fake_mapper() -> None:
    processors = ChemCensorConfig(use_fake_mapper=True).build_processor().processors
    assert isinstance(processors[1], FakeMapper)
    assert isinstance(processors[0], Validator)
    assert length_check not in processors[0].validators


def test_default_pipeline_includes_optional_validators() -> None:
    types = _processor_types(ChemCensorConfig())
    assert Validator in types
    assert SkeletonConservationValidator in types
    assert StaticStereoValidator in types


def test_optional_validators_can_be_disabled() -> None:
    types = _processor_types(
        ChemCensorConfig(
            validate_input=False,
            check_skeleton_conservation=False,
            check_static_stereo=False,
        )
    )
    assert Validator not in types
    assert SkeletonConservationValidator not in types
    assert StaticStereoValidator not in types
    assert Mapper in types


def test_use_cpu_is_forwarded_to_mapper(monkeypatch) -> None:
    monkeypatch.setattr(
        "chemcensor.processing.mapper._create_batched_mapper",
        lambda _batch_size, *, use_cpu: None,
    )
    processors = ChemCensorConfig(use_cpu=True).build_processor().processors
    mapper = next(p for p in processors if isinstance(p, Mapper))
    assert mapper.use_cpu is True


def test_mapper_batch_size_and_threads_are_forwarded(monkeypatch) -> None:
    created_batch_sizes: list[int] = []
    monkeypatch.delenv("OMP_NUM_THREADS", raising=False)
    monkeypatch.setattr(
        "chemcensor.processing.mapper._create_batched_mapper",
        lambda batch_size, *, use_cpu: created_batch_sizes.append(batch_size),
    )

    ChemCensorConfig(mapper_batch_size=7, mapper_n_jobs=3).build_processor()

    assert created_batch_sizes == [7]
    assert os.environ["OMP_NUM_THREADS"] == "3"


def test_disabled_validators_keep_pipeline_order() -> None:
    """Disabling optional stages must not reorder the remaining ones."""
    default_names = [t.__name__ for t in _processor_types(ChemCensorConfig())]
    trimmed_names = [
        t.__name__
        for t in _processor_types(
            ChemCensorConfig(
                check_skeleton_conservation=False,
                check_static_stereo=False,
            )
        )
    ]
    assert trimmed_names == [
        name
        for name in default_names
        if name
        not in (
            "SkeletonConservationValidator",
            "StaticStereoValidator",
        )
    ]


def test_composition_default_pipeline_includes_optional_validators() -> None:
    types = _processor_types(CompositionPipelineConfig())
    assert Validator in types
    assert SkeletonConservationValidator in types
    assert StaticStereoValidator in types


def test_composition_pipeline_honours_validator_flags() -> None:
    types = _processor_types(
        CompositionPipelineConfig(
            validate_input=False,
            check_skeleton_conservation=False,
            check_static_stereo=False,
        )
    )
    assert Validator not in types
    assert SkeletonConservationValidator not in types
    assert StaticStereoValidator not in types
