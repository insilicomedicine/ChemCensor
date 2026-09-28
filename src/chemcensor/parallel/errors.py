from __future__ import annotations


class ParallelError(Exception):
    """Base class for parallel-pipeline errors."""


class MapperCrashedError(ParallelError):
    """The mapper subprocess died unexpectedly. The run is unrecoverable."""


class ScorerCrashedError(ParallelError):
    """A scorer worker died and could not be restarted within the budget."""


class CheckpointCorruptedError(ParallelError):
    """The checkpoint file exists but its contents could not be parsed."""


class MalformedCsvError(ParallelError):
    """A CSV cannot be rewritten without losing data."""


class OutputSchemaMismatchError(ParallelError):
    """The output CSV header does not match the schema this version writes.

    Raised on resume/append when an existing result file was produced by an
    older (or differently configured) ChemCensor and cannot safely receive
    new rows.
    """
