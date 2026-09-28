from __future__ import annotations

import os
import queue as queue_mod
from pathlib import Path
from typing import Any

from chemcensor.parallel.io import read_mapped_dump
from chemcensor.parallel.mapper_proc import _build_fake_processor
from chemcensor.parallel.mapper_proc import _set_thread_env
from chemcensor.parallel.mapper_proc import run_mapper
from chemcensor.parallel.messages import MapTask
from chemcensor.processing.utils import strip_atom_map_labels


def test_fake_processor_rebuilds_mapping_from_precomputed_input() -> None:
    """A precomputed mapped reaction is stripped to raw and re-mapped."""
    proc = _build_fake_processor()
    mapped_in = "[CH3:1][CH3:2]>>[CH3:1][CH3:2]"

    out = proc(((0, mapped_in),))

    idx, raw, mapped = out[0]
    assert idx == 0
    # raw is the atom-map-stripped input (order preserved, no ``:N``).
    assert raw == strip_atom_map_labels(mapped_in)
    assert ":" not in raw
    # FakeMapper rebuilds a canonical atom-mapped reaction.
    assert mapped is not None
    assert ">>" in mapped and ":1]" in mapped and ":2]" in mapped


def test_strip_atom_map_labels_preserves_atom_order() -> None:
    mapped = "[NH3+:12][C@@H:3]>>[NH2:12][C@@H:3]"

    assert strip_atom_map_labels(mapped) == "[NH3+][C@@H]>>[NH2][C@@H]"


def test_fake_processor_forwards_none_for_garbage() -> None:
    """Inputs FakeMapper cannot map are forwarded with ``mapped=None``."""
    proc = _build_fake_processor()

    out = proc(((0, ">>"), (1, "not-a-reaction")))

    assert out[0] == (0, ">>", None)
    assert out[1][0] == 1 and out[1][2] is None


def test_fake_processor_preserves_order_and_indices() -> None:
    proc = _build_fake_processor()
    items = ((5, "[CH3:1][CH3:2]>>[CH3:1][CH3:2]"), (9, ">>"))

    out = proc(items)

    assert [row[0] for row in out] == [5, 9]


def test_run_mapper_dumps_mapped_smiles(tmp_path: Path) -> None:
    """With a dump path set, every mapped reaction is persisted by ``idx``."""
    # ``run_mapper`` only uses the ``get``/``put`` protocol, so a plain
    # thread queue stands in for the multiprocessing one.
    map_queue: Any = queue_mod.Queue()
    map_queue.put(
        MapTask(
            batch_id=0,
            items=((3, "[CH3:1][CH3:2]>>[CH3:1][CH3:2]"), (4, "not-a-reaction")),
        )
    )
    map_queue.put(None)
    score_queue: Any = queue_mod.Queue()
    dump_path = tmp_path / "mapped-0.csv"

    run_mapper(
        map_queue,
        score_queue,
        threads=1,
        rxnmapper_batch_size=1,
        use_fake_mapper=True,
        mapped_dump_path=dump_path,
    )

    dumped = read_mapped_dump([dump_path])
    # idx 4 could not be mapped, so it is absent rather than empty.
    assert list(dumped) == [3]
    assert ":1]" in dumped[3] and ":2]" in dumped[3]


def test_set_thread_env_use_cpu_hides_cuda(monkeypatch) -> None:
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "0")
    _set_thread_env(1, use_cpu=True)
    assert os.environ["CUDA_VISIBLE_DEVICES"] == ""
