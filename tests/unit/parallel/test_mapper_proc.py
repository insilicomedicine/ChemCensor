from __future__ import annotations

from chemcensor.parallel.mapper_proc import _ATOM_MAP_RE
from chemcensor.parallel.mapper_proc import _build_fake_processor


def test_fake_processor_rebuilds_mapping_from_precomputed_input() -> None:
    """A precomputed mapped reaction is stripped to raw and re-mapped."""
    proc = _build_fake_processor()
    mapped_in = "[CH3:1][CH3:2]>>[CH3:1][CH3:2]"

    out = proc(((0, mapped_in),))

    idx, raw, mapped = out[0]
    assert idx == 0
    # raw is the atom-map-stripped input (order preserved, no ``:N``).
    assert raw == _ATOM_MAP_RE.sub("", mapped_in)
    assert ":" not in raw
    # FakeMapper rebuilds a canonical atom-mapped reaction.
    assert mapped is not None
    assert ">>" in mapped and ":1]" in mapped and ":2]" in mapped


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
