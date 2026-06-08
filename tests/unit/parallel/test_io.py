from __future__ import annotations

import csv
from pathlib import Path

import pytest

from chemcensor.parallel.io import CsvSink
from chemcensor.parallel.io import iter_csv_smiles
from chemcensor.parallel.io import ListSink


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def test_iter_csv_smiles_basic(tmp_path: Path) -> None:
    path = tmp_path / "in.csv"
    _write_csv(
        path,
        [
            {"reaction_smiles": "A>>B"},
            {"reaction_smiles": "C>>D"},
            {"reaction_smiles": "E>>F"},
        ],
    )
    rows = list(iter_csv_smiles(path, smiles_column="reaction_smiles"))
    assert rows == [(0, "A>>B"), (1, "C>>D"), (2, "E>>F")]


def test_iter_csv_smiles_skip_empty_rows(tmp_path: Path) -> None:
    path = tmp_path / "in.csv"
    _write_csv(
        path,
        [
            {"reaction_smiles": "A>>B"},
            {"reaction_smiles": ""},
            {"reaction_smiles": "  "},
            {"reaction_smiles": "E>>F"},
        ],
    )
    rows = list(iter_csv_smiles(path, smiles_column="reaction_smiles"))
    # idx 0 and 3 survive; 1 and 2 are skipped silently.
    assert rows == [(0, "A>>B"), (3, "E>>F")]


def test_iter_csv_smiles_skip_until(tmp_path: Path) -> None:
    path = tmp_path / "in.csv"
    _write_csv(
        path,
        [{"reaction_smiles": f"R{i}>>P{i}"} for i in range(5)],
    )
    rows = list(
        iter_csv_smiles(path, smiles_column="reaction_smiles", skip_until_idx=2)
    )
    assert rows == [(3, "R3>>P3"), (4, "R4>>P4")]


def test_iter_csv_smiles_skip_indices(tmp_path: Path) -> None:
    """Individual out-of-order indices are skipped on resume."""
    path = tmp_path / "in.csv"
    _write_csv(
        path,
        [{"reaction_smiles": f"R{i}>>P{i}"} for i in range(6)],
    )
    rows = list(
        iter_csv_smiles(
            path,
            smiles_column="reaction_smiles",
            skip_until_idx=2,
            skip_indices={4, 5},
        )
    )
    # 0..2 below the frontier, 4 and 5 already done out-of-order → only 3 left.
    assert rows == [(3, "R3>>P3")]


def test_iter_csv_smiles_missing_column_raises(tmp_path: Path) -> None:
    path = tmp_path / "in.csv"
    _write_csv(path, [{"other": "X"}])
    with pytest.raises(KeyError):
        list(iter_csv_smiles(path, smiles_column="reaction_smiles"))


def test_list_sink_collects() -> None:
    sink = ListSink()
    sink.write([(0, "A>>B", 1.0), (1, "C>>D", 2.0)])
    sink.write([(2, "E>>F", 3.0)])
    sink.close()
    assert sink.items == [
        (0, "A>>B", 1.0),
        (1, "C>>D", 2.0),
        (2, "E>>F", 3.0),
    ]


def test_csv_sink_writes_header_and_rows(tmp_path: Path) -> None:
    out = tmp_path / "out.csv"
    with CsvSink(out) as sink:
        sink.write([(0, "A>>B", 1.0)])
        sink.write([(1, "C>>D", 2.0)])

    with open(out, encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    assert rows[0] == ["idx", "smiles", "score"]
    assert rows[1:] == [["0", "A>>B", "1.0"], ["1", "C>>D", "2.0"]]


def test_csv_sink_append_does_not_duplicate_header(tmp_path: Path) -> None:
    out = tmp_path / "out.csv"
    with CsvSink(out) as sink:
        sink.write([(0, "A>>B", 1.0)])
    with CsvSink(out, append=True) as sink:
        sink.write([(1, "C>>D", 2.0)])

    with open(out, encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    assert rows == [
        ["idx", "smiles", "score"],
        ["0", "A>>B", "1.0"],
        ["1", "C>>D", "2.0"],
    ]


def test_csv_sink_append_to_empty_file_writes_header(tmp_path: Path) -> None:
    out = tmp_path / "out.csv"
    out.touch()  # empty file
    with CsvSink(out, append=True) as sink:
        sink.write([(0, "A>>B", 1.0)])
    with open(out, encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    assert rows[0] == ["idx", "smiles", "score"]
