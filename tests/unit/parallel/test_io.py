from __future__ import annotations

import csv
from pathlib import Path

import pytest

from chemcensor.parallel.errors import MalformedCsvError
from chemcensor.parallel.errors import OutputSchemaMismatchError
from chemcensor.parallel.io import CsvSink
from chemcensor.parallel.io import existing_mapped_dump_shards
from chemcensor.parallel.io import iter_csv_smiles
from chemcensor.parallel.io import ListSink
from chemcensor.parallel.io import mapped_dump_shards
from chemcensor.parallel.io import MappedRxnDump
from chemcensor.parallel.io import read_mapped_dump
from chemcensor.parallel.io import write_csv_with_extra_column
from chemcensor.parallel.messages import make_scored_item

_HEADER = [
    "idx",
    "smiles",
    "score_with_fg",
    "score_without_fg",
    "all_fgs_precedents_are_real",
    "total_number_of_fgs",
    "number_of_fgs_covered_by_virtual_precedents",
    "all_center_precedents_are_real",
    "failure_stage",
    "failure_category",
    "failure_message",
]


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
    sink.write(
        [
            make_scored_item(0, "A>>B", 1.0, 1.0),
            make_scored_item(1, "C>>D", 2.0, 3.0, total_number_of_fgs=2),
        ]
    )
    sink.write(
        [
            make_scored_item(
                2,
                "E>>F",
                3.0,
                4.0,
                all_fgs_precedents_are_real=False,
                all_center_precedents_are_real=False,
            )
        ]
    )
    sink.close()
    assert sink.items == [
        (0, "A>>B", 1.0, 1.0, True, 0, 0, True, "", "", ""),
        (1, "C>>D", 2.0, 3.0, True, 2, 0, True, "", "", ""),
        (2, "E>>F", 3.0, 4.0, False, 0, 0, False, "", "", ""),
    ]


def test_csv_sink_writes_header_and_rows(tmp_path: Path) -> None:
    out = tmp_path / "out.csv"
    with CsvSink(out) as sink:
        sink.write([make_scored_item(0, "A>>B", 1.0, 1.0)])
        sink.write(
            [
                make_scored_item(
                    1,
                    "C>>D",
                    2.0,
                    3.0,
                    all_fgs_precedents_are_real=False,
                    total_number_of_fgs=2,
                    number_of_fgs_covered_by_virtual_precedents=1,
                    all_center_precedents_are_real=False,
                )
            ]
        )

    with open(out, encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    assert rows[0] == _HEADER
    assert rows[1:] == [
        ["0", "A>>B", "1.0", "1.0", "True", "0", "0", "True", "", "", ""],
        ["1", "C>>D", "2.0", "3.0", "False", "2", "1", "False", "", "", ""],
    ]


def test_csv_sink_append_does_not_duplicate_header(tmp_path: Path) -> None:
    out = tmp_path / "out.csv"
    with CsvSink(out) as sink:
        sink.write([make_scored_item(0, "A>>B", 1.0, 1.0)])
    with CsvSink(out, append=True) as sink:
        sink.write([make_scored_item(1, "C>>D", 2.0, 3.0)])

    with open(out, encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    assert rows == [
        _HEADER,
        ["0", "A>>B", "1.0", "1.0", "True", "0", "0", "True", "", "", ""],
        ["1", "C>>D", "2.0", "3.0", "True", "0", "0", "True", "", "", ""],
    ]


def test_csv_sink_append_to_empty_file_writes_header(tmp_path: Path) -> None:
    out = tmp_path / "out.csv"
    out.touch()  # empty file
    with CsvSink(out, append=True) as sink:
        sink.write([make_scored_item(0, "A>>B", 1.0, 1.0)])
    with open(out, encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    assert rows[0] == _HEADER


def test_csv_sink_writes_cano_rxn_column(tmp_path: Path) -> None:
    out = tmp_path / "out.csv"
    with CsvSink(out, include_canonical_smiles=True) as sink:
        sink.write([make_scored_item(0, "A>>B", 1.0, 2.0, cano_rxn="canon>>rxn")])

    with open(out, encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    assert rows[0] == _HEADER + ["cano_rxn"]
    assert rows[1] == [
        "0",
        "A>>B",
        "1.0",
        "2.0",
        "True",
        "0",
        "0",
        "True",
        "",
        "",
        "",
        "canon>>rxn",
    ]


def test_csv_sink_append_rejects_legacy_header(tmp_path: Path) -> None:
    """Resume must not append under a pre-CM-3565 7-column header."""
    out = tmp_path / "out.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "idx",
                "smiles",
                "score_with_fg",
                "score_without_fg",
                "all_fgs_precedents_are_real",
                "total_number_of_fgs",
                "number_of_fgs_covered_by_virtual_precedents",
            ]
        )
        writer.writerow([0, "A>>B", 1.0, 1.0, True, 0, 0])

    with pytest.raises(OutputSchemaMismatchError, match="Refusing to append"):
        CsvSink(out, append=True)


def test_csv_sink_append_rejects_cano_flag_mismatch(tmp_path: Path) -> None:
    out = tmp_path / "out.csv"
    with CsvSink(out) as sink:
        sink.write([make_scored_item(0, "A>>B", 1.0, 1.0)])

    with pytest.raises(OutputSchemaMismatchError):
        CsvSink(out, append=True, include_canonical_smiles=True)


def test_mapped_dump_roundtrip(tmp_path: Path) -> None:
    """Shards written by the mappers are read back as ``idx -> mapped``."""
    shards = mapped_dump_shards(tmp_path, 2)
    with MappedRxnDump(shards[0]) as dump:
        dump.write([(0, "A>>B", "[A:1]>>[B:1]"), (2, "E>>F", None)])
    with MappedRxnDump(shards[1]) as dump:
        dump.write([(1, "C>>D", "[C:1]>>[D:1]")])

    # Unmapped rows (``None``) are dropped, so only usable maps come back.
    assert read_mapped_dump(shards) == {0: "[A:1]>>[B:1]", 1: "[C:1]>>[D:1]"}


def test_read_mapped_dump_tolerates_missing_shards(tmp_path: Path) -> None:
    shards = mapped_dump_shards(tmp_path, 3)
    with MappedRxnDump(shards[1]) as dump:
        dump.write([(7, "A>>B", "[A:1]>>[B:1]")])

    assert read_mapped_dump(shards) == {7: "[A:1]>>[B:1]"}


def test_existing_mapped_dump_shards_discovers_written_shards(tmp_path: Path) -> None:
    """The merge step finds the shards without being told the mapper count."""
    for shard in mapped_dump_shards(tmp_path, 12):
        MappedRxnDump(shard).close()
    (tmp_path / "unrelated.csv").write_text("", encoding="utf-8")

    found = existing_mapped_dump_shards(tmp_path)

    assert found == sorted(mapped_dump_shards(tmp_path, 12))


def test_write_csv_with_extra_column_appends_column(tmp_path: Path) -> None:
    path = tmp_path / "in.csv"
    out = tmp_path / "out.csv"
    _write_csv(
        path,
        [
            {"cleaned_rxn": "A>>B", "PatentNumber": "US1"},
            {"cleaned_rxn": "C>>D", "PatentNumber": "US2"},
        ],
    )

    filled = write_csv_with_extra_column(
        path, out, column="mapped_rxn", values={1: "[C:1]>>[D:1]"}
    )

    assert filled == 1
    with open(out, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert rows[0] == {
        "cleaned_rxn": "A>>B",
        "PatentNumber": "US1",
        "mapped_rxn": "",
    }
    assert rows[1]["mapped_rxn"] == "[C:1]>>[D:1]"


def test_write_csv_with_extra_column_updates_in_place(tmp_path: Path) -> None:
    """Passing the input as the output rewrites it, overwriting the column."""
    path = tmp_path / "in.csv"
    _write_csv(
        path,
        [
            {"cleaned_rxn": "A>>B", "mapped_rxn": "stale"},
            {"cleaned_rxn": "C>>D", "mapped_rxn": ""},
        ],
    )

    filled = write_csv_with_extra_column(
        path, path, column="mapped_rxn", values={0: "[A:1]>>[B:1]"}
    )

    assert filled == 1
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        assert reader.fieldnames == ["cleaned_rxn", "mapped_rxn"]
        rows = list(reader)
    assert rows[0]["mapped_rxn"] == "[A:1]>>[B:1]"
    assert rows[1]["mapped_rxn"] == ""
    assert not list(tmp_path.glob("*.tmp"))


def test_write_csv_with_extra_column_rejects_ragged_row(tmp_path: Path) -> None:
    """A row with more fields than the header would lose data when copied."""
    path = tmp_path / "in.csv"
    path.write_text("cleaned_rxn\nA>>B,extra\n", encoding="utf-8")

    with pytest.raises(MalformedCsvError):
        write_csv_with_extra_column(
            path, tmp_path / "out.csv", column="mapped_rxn", values={}
        )


def test_write_csv_with_extra_column_rejects_headerless_csv(tmp_path: Path) -> None:
    path = tmp_path / "in.csv"
    path.write_text("", encoding="utf-8")

    with pytest.raises(MalformedCsvError):
        write_csv_with_extra_column(
            path, tmp_path / "out.csv", column="mapped_rxn", values={}
        )
