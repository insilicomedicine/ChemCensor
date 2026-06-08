from __future__ import annotations

import csv
from collections.abc import Iterable
from collections.abc import Iterator
from os import PathLike
from pathlib import Path
from typing import Protocol


_RESULT_HEADER = ("idx", "smiles", "score")


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

    def write(self, items: Iterable[tuple[int, str, float]]) -> None:
        """Append a batch of ``(idx, smiles, score)`` tuples.

        :param items: Iterable of result rows.
        :type items: Iterable[tuple[int, str, float]]
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
        self._items: list[tuple[int, str, float]] = []

    def write(self, items: Iterable[tuple[int, str, float]]) -> None:
        self._items.extend(items)

    def close(self) -> None:
        # Nothing to release; list lives on the caller side.
        return None

    @property
    def items(self) -> list[tuple[int, str, float]]:
        """Return collected ``(idx, smiles, score)`` tuples."""
        return self._items


class CsvSink:
    """File-backed sink that streams ``(idx, smiles, score)`` rows to CSV.

    Supports append mode for resume: when ``append=True`` and the file
    already exists, the header is not rewritten.
    """

    def __init__(self, path: str | PathLike, *, append: bool = False) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if append and path.exists() and path.stat().st_size > 0 else "w"
        # newline="" is required on Windows to avoid extra \r in the output
        # produced by csv; harmless on POSIX.
        self._fh = open(path, mode, newline="", encoding="utf-8")
        self._writer = csv.writer(self._fh)
        if mode == "w":
            self._writer.writerow(_RESULT_HEADER)
            self._fh.flush()

    def write(self, items: Iterable[tuple[int, str, float]]) -> None:
        self._writer.writerows(items)
        self._fh.flush()

    def close(self) -> None:
        if not self._fh.closed:
            self._fh.close()

    def __enter__(self) -> "CsvSink":
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()
