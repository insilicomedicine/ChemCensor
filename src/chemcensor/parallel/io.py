from __future__ import annotations

import csv
import os
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Mapping
from os import PathLike
from pathlib import Path
from typing import Protocol

from .errors import MalformedCsvError
from .errors import OutputSchemaMismatchError
from .messages import ScoredItem

_RESULT_HEADER = (
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
)
_RESULT_HEADER_WITH_CANO = (*_RESULT_HEADER, "cano_rxn")


def _expected_result_header(*, include_canonical_smiles: bool) -> tuple[str, ...]:
    return _RESULT_HEADER_WITH_CANO if include_canonical_smiles else _RESULT_HEADER


def _read_csv_header(path: Path) -> tuple[str, ...] | None:
    """Return the first CSV row as a header tuple, or ``None`` if empty."""
    with open(path, newline="", encoding="utf-8") as fh:
        row = next(csv.reader(fh), None)
    if row is None:
        return None
    return tuple(row)


_MAPPED_DUMP_HEADER = ("idx", "mapped_rxn")
_MAPPED_SHARD_STEM = "mapped"


def iter_csv_smiles(
    path: str | PathLike,
    *,
    smiles_column: str,
    skip_until_idx: int = -1,
    skip_indices: Iterable[int] | None = None,
) -> Iterator[tuple[int, str]]:
    """Yield ``(idx, smiles)`` pairs from a CSV file.

    ``idx`` is the 0-based row number (header excluded). Rows whose
    ``smiles_column`` value is empty are skipped silently.

    :param path: Path to the input CSV file.
    :type path: str | PathLike
    :param smiles_column: Name of the column that contains reaction SMILES.
    :type smiles_column: str
    :param skip_until_idx: When ``>= 0``, rows with ``idx <=
        skip_until_idx`` are skipped. Used for fast resume.
    :type skip_until_idx: int
    :param skip_indices: Additional individual indices to skip — the
        out-of-order rows already written in a previous run (above the
        contiguous frontier). Skipping them on resume avoids re-scoring
        and, crucially, avoids appending duplicate ``idx`` rows to the
        output.
    :type skip_indices: Iterable[int] | None
    :return: Iterator of ``(idx, smiles)`` pairs.
    :rtype: Iterator[tuple[int, str]]
    :raises KeyError: If ``smiles_column`` is missing from the CSV header.
    """
    skip_set = frozenset(skip_indices) if skip_indices is not None else frozenset()
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None or smiles_column not in reader.fieldnames:
            raise KeyError(
                f"Column {smiles_column!r} not found in {path} "
                f"(have: {reader.fieldnames})"
            )
        for idx, row in enumerate(reader):
            if idx <= skip_until_idx or idx in skip_set:
                continue
            smiles = (row.get(smiles_column) or "").strip()
            if not smiles:
                continue
            yield idx, smiles


class ResultSink(Protocol):
    """Protocol consumed by the writer thread.

    Implementations buffer per-batch results and flush them to their
    underlying storage (a file, a Python list, ...).
    """

    def write(self, items: Iterable[ScoredItem]) -> None:
        """Append a batch of scored result tuples.

        Each item is either
        ``(idx, smiles, score_with_fg, score_without_fg,
        all_fgs_precedents_are_real, total_number_of_fgs,
        number_of_fgs_covered_by_virtual_precedents,
        all_center_precedents_are_real, failure_stage, failure_category,
        failure_message)`` or, when canonical SMILES are requested, the same
        plus ``cano_rxn``.

        :param items: Iterable of result rows.
        :type items: Iterable[ScoredItem]
        """
        ...

    def close(self) -> None:
        """Flush buffers and release any external resources."""
        ...


class ListSink:
    """In-memory sink that collects results into a list.

    Order of insertion mirrors the order in which the writer thread sees
    results — which is *not* guaranteed to be the input order.  Callers
    that need input order should sort by ``idx`` post-hoc or use the
    helpers in :mod:`chemcensor.parallel`.
    """

    def __init__(self) -> None:
        self._items: list[ScoredItem] = []

    def write(self, items: Iterable[ScoredItem]) -> None:
        self._items.extend(items)

    def close(self) -> None:
        # Nothing to release; list lives on the caller side.
        return None

    @property
    def items(self) -> list[ScoredItem]:
        """Return collected scored result tuples."""
        return self._items


class CsvSink:
    """Stream scored result rows to CSV.

    Supports append mode for resume: when ``append=True`` and the file
    already exists with a matching header, the header is not rewritten.
    A schema mismatch against an earlier ChemCensor version raises
    :class:`OutputSchemaMismatchError` instead of silently corrupting the file.

    :raises OutputSchemaMismatchError: On append when the existing header
        differs from the schema this version writes.
    """

    def __init__(
        self,
        path: str | PathLike,
        *,
        append: bool = False,
        include_canonical_smiles: bool = False,
    ) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        expected = _expected_result_header(
            include_canonical_smiles=include_canonical_smiles
        )
        mode = "w"
        if append and path.exists() and path.stat().st_size > 0:
            existing = _read_csv_header(path)
            if existing is None:
                mode = "w"
            elif existing != expected:
                raise OutputSchemaMismatchError(
                    f"Output CSV {path} has header {list(existing)!r}, but this "
                    f"version writes {list(expected)!r}. Refusing to append — "
                    "start a fresh output file (or delete the checkpoint) after "
                    "upgrading ChemCensor."
                )
            else:
                mode = "a"
        self._include_canonical_smiles = include_canonical_smiles
        # newline="" is required on Windows to avoid extra \r in the output
        # produced by csv; harmless on POSIX.
        self._fh = open(path, mode, newline="", encoding="utf-8")
        self._writer = csv.writer(self._fh)
        if mode == "w":
            self._writer.writerow(expected)
            self._fh.flush()

    def write(self, items: Iterable[ScoredItem]) -> None:
        if self._include_canonical_smiles:
            rows = [item if len(item) == 12 else (*item[:11], "") for item in items]
            self._writer.writerows(rows)
        else:
            self._writer.writerows(item[:11] for item in items)
        self._fh.flush()

    def close(self) -> None:
        if not self._fh.closed:
            self._fh.close()

    def __enter__(self) -> "CsvSink":
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()


class MappedRxnDump:
    """Stream ``(idx, mapped_rxn)`` pairs produced by one mapper process.

    Every mapper owns its own shard file, so no cross-process locking is
    needed; ``idx`` values never repeat across shards because each input row
    is handled by exactly one mapper. Rows the mapper could not map are
    written with an empty ``mapped_rxn``. Each batch is flushed so an aborted
    run still leaves a readable shard.
    """

    def __init__(self, path: str | PathLike) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = open(path, "w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._fh)
        self._writer.writerow(_MAPPED_DUMP_HEADER)

    def write(self, items: Iterable[tuple[int, str, str | None]]) -> None:
        """Append one mapper batch, given as ``(idx, raw, mapped)`` triples.

        :param items: The mapper's per-batch output.
        :type items: Iterable[tuple[int, str, str | None]]
        """
        self._writer.writerows((idx, mapped or "") for idx, _raw, mapped in items)
        self._fh.flush()

    def close(self) -> None:
        if not self._fh.closed:
            self._fh.close()

    def __enter__(self) -> "MappedRxnDump":
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()


def mapped_dump_shards(directory: str | PathLike, n_mappers: int) -> list[Path]:
    """Return the shard paths to hand out to ``n_mappers`` mapper processes.

    :param directory: Directory holding the shards.
    :type directory: str | PathLike
    :param n_mappers: Number of mapper processes.
    :type n_mappers: int
    :return: One path per mapper.
    :rtype: list[Path]
    """
    return [Path(directory) / f"{_MAPPED_SHARD_STEM}-{i}.csv" for i in range(n_mappers)]


def existing_mapped_dump_shards(directory: str | PathLike) -> list[Path]:
    """Return the shards actually present in *directory*.

    The merge step runs after the mappers are gone and does not need to know
    how many of them there were, so it discovers the shards instead of
    reconstructing their names.

    :param directory: Directory holding the shards.
    :type directory: str | PathLike
    :return: Existing shard paths, in mapper order.
    :rtype: list[Path]
    """
    return sorted(Path(directory).glob(f"{_MAPPED_SHARD_STEM}-*.csv"))


def read_mapped_dump(paths: Iterable[str | PathLike]) -> dict[int, str]:
    """Load ``idx -> mapped_rxn`` from mapper dump shards.

    Missing shards and rows with an empty ``mapped_rxn`` (mapping failed) are
    skipped, so the returned mapping only holds usable atom-mapped SMILES.

    :param paths: Shard paths, e.g. from :func:`mapped_dump_shards`.
    :type paths: Iterable[str | PathLike]
    :return: Mapping from input row index to atom-mapped reaction SMILES.
    :rtype: dict[int, str]
    """
    out: dict[int, str] = {}
    for path in paths:
        if not Path(path).exists():
            continue
        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            next(reader, None)  # header
            for row in reader:
                if len(row) < 2 or not row[1]:
                    continue
                try:
                    idx = int(row[0])
                except ValueError:
                    continue
                out[idx] = row[1]
    return out


def write_csv_with_extra_column(
    input_path: str | PathLike,
    output_path: str | PathLike,
    *,
    column: str,
    values: Mapping[int, str],
) -> int:
    """Copy a CSV, filling ``column`` from ``values`` keyed by row index.

    Row indices are 0-based with the header excluded, matching
    :func:`iter_csv_smiles`. Rows without an entry in ``values`` get an empty
    value. An existing ``column`` keeps its position and is overwritten. The
    result is written to a temporary file and then renamed, so ``output_path``
    may equal ``input_path`` for an in-place update without the risk of
    leaving a truncated CSV behind.

    :param input_path: Source CSV.
    :type input_path: str | PathLike
    :param output_path: Destination CSV; may be ``input_path``.
    :type output_path: str | PathLike
    :param column: Name of the column to add or overwrite.
    :type column: str
    :param values: Mapping from row index to cell value.
    :type values: Mapping[int, str]
    :return: Number of rows that received a non-empty value.
    :rtype: int
    :raises MalformedCsvError: If the source CSV has no header, or if a row has
        more fields than the header (copying it would silently drop data).
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = output_path.with_name(output_path.name + ".tmp")

    filled = 0
    with (
        open(input_path, newline="", encoding="utf-8") as src,
        open(tmp_path, "w", newline="", encoding="utf-8") as dst,
    ):
        reader = csv.DictReader(src)
        fieldnames: list[str] = list(reader.fieldnames or [])
        if not fieldnames:
            raise MalformedCsvError(f"{input_path} has no header row")
        if column not in fieldnames:
            fieldnames.append(column)
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()
        for idx, row in enumerate(reader):
            if None in row:
                raise MalformedCsvError(
                    f"{input_path}: row {idx} has more fields than the header; "
                    "refusing to rewrite the file"
                )
            value = values.get(idx, "")
            row[column] = value
            if value:
                filled += 1
            writer.writerow({key: row.get(key) or "" for key in fieldnames})
    os.replace(tmp_path, output_path)
    return filled
