from __future__ import annotations

import pytest

from chemcensor.parallel.config import autoscale
from chemcensor.parallel.config import ParallelConfig


@pytest.mark.parametrize(
    "cpu_count, expected_workers, expected_mappers",
    [
        # Tiny host: one mapper, one worker.
        (1, 1, 1),
        (2, 1, 1),
        # Small server: a fair split, mappers take ~a quarter (>=1).
        (4, 2, 1),
        (8, 5, 2),
        # Mid: mappers take ~quarter of CPUs.
        (16, 11, 4),
        # Mapper count saturates at 8 from cpu_count=32 onwards.
        (32, 23, 8),
        (64, 55, 8),
        (128, 119, 8),
    ],
)
def test_autoscale_defaults(cpu_count, expected_workers, expected_mappers) -> None:
    n_workers, mapper_threads, n_mappers = autoscale(cpu_count=cpu_count)
    assert n_workers == expected_workers
    assert n_mappers == expected_mappers
    # Threads per mapper default to 1 (scaling happens via processes).
    assert mapper_threads == 1


def test_autoscale_user_override_workers() -> None:
    n_workers, mapper_threads, n_mappers = autoscale(n_workers=10, cpu_count=16)
    assert n_workers == 10
    assert n_mappers == 4  # still autoscaled
    assert mapper_threads == 1


def test_autoscale_user_override_mappers() -> None:
    n_workers, mapper_threads, n_mappers = autoscale(n_mappers=2, cpu_count=16)
    assert n_mappers == 2
    assert mapper_threads == 1
    assert n_workers == 16 - 2 * 1 - 1  # leaves room for main


def test_autoscale_user_override_mapper_threads() -> None:
    n_workers, mapper_threads, n_mappers = autoscale(mapper_threads=2, cpu_count=16)
    assert mapper_threads == 2
    assert n_mappers == 4
    assert n_workers == 16 - 4 * 2 - 1  # mappers * threads reserved


def test_autoscale_user_override_all() -> None:
    n_workers, mapper_threads, n_mappers = autoscale(
        n_workers=4, mapper_threads=4, n_mappers=1, cpu_count=8
    )
    assert n_workers == 4
    assert mapper_threads == 4
    assert n_mappers == 1


def test_autoscale_floors_at_one() -> None:
    n_workers, mapper_threads, n_mappers = autoscale(
        n_workers=0, mapper_threads=0, n_mappers=0, cpu_count=1
    )
    assert n_workers == 1
    assert mapper_threads == 1
    assert n_mappers == 1


def test_parallel_config_resolved_idempotent() -> None:
    cfg = ParallelConfig(n_workers=3, mapper_threads=2)
    resolved = cfg.resolved()
    assert resolved.n_workers == 3
    assert resolved.mapper_threads == 2
    # All other fields preserved verbatim.
    assert resolved.batch_size == cfg.batch_size
    assert resolved.find_exact_match == cfg.find_exact_match


def test_parallel_config_resolved_preserves_use_fake_mapper() -> None:
    assert ParallelConfig().resolved().use_fake_mapper is False
    assert ParallelConfig(use_fake_mapper=True).resolved().use_fake_mapper is True


def test_parallel_config_resolved_autoscales_none(monkeypatch) -> None:
    monkeypatch.setattr("os.cpu_count", lambda: 16)
    cfg = ParallelConfig()
    resolved = cfg.resolved()
    assert resolved.n_workers is not None and resolved.n_workers >= 1
    assert resolved.mapper_threads is not None and resolved.mapper_threads >= 1
    assert resolved.n_mappers is not None and resolved.n_mappers >= 1
