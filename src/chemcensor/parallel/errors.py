from __future__ import annotations


class ParallelError(Exception):
    """Base class for parallel-pipeline errors."""


class MapperCrashedError(ParallelError):
    """The mapper subprocess died unexpectedly. The run is unrecoverable."""


class ScorerCrashedError(ParallelError):
    """A scorer worker died and could not be restarted within the budget."""


class CheckpointCorruptedError(ParallelError):
    """The checkpoint file exists but its contents could not be parsed."""
