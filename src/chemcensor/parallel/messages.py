from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from chemcensor.chemcensor import FailureReason
    from chemcensor.composition.records import ReactionRecord

# ``(idx, smiles, with_fg, without_fg, all_fgs_real, total_fgs, virtual_fgs,
# all_centers_real, failure_stage, failure_category, failure_message)`` or,
# when canonical SMILES are requested, the same plus ``cano_rxn``.
ScoredItem = (
    tuple[int, str, float, float, bool, int, int, bool, str, str, str]
    | tuple[int, str, float, float, bool, int, int, bool, str, str, str, str]
)


def make_scored_item(
    idx: int,
    smiles: str,
    with_fg: float,
    without_fg: float,
    *,
    all_fgs_precedents_are_real: bool = True,
    total_number_of_fgs: int = 0,
    number_of_fgs_covered_by_virtual_precedents: int = 0,
    all_center_precedents_are_real: bool = True,
    failure_reason: FailureReason | None = None,
    cano_rxn: str | None = None,
) -> ScoredItem:
    """Build a :data:`ScoredItem` row, optionally with canonical SMILES."""
    base = (
        idx,
        smiles,
        float(with_fg),
        float(without_fg),
        all_fgs_precedents_are_real,
        total_number_of_fgs,
        number_of_fgs_covered_by_virtual_precedents,
        all_center_precedents_are_real,
        str(failure_reason.stage) if failure_reason is not None else "",
        failure_reason.category if failure_reason is not None else "",
        failure_reason.message if failure_reason is not None else "",
    )
    if cano_rxn is not None:
        return (*base, cano_rxn)
    return base


@dataclass(frozen=True)
class MapTask:
    """A batch of raw reaction SMILES queued for atom mapping.

    :param batch_id: Monotonically increasing id assigned by the reader,
        used for ordering and crash-recovery bookkeeping.
    :type batch_id: int
    :param items: Tuple of ``(idx, raw_smiles)`` pairs. ``idx`` is the
        input position (row number for files, list index for in-memory
        inputs).
    :type items: tuple[tuple[int, str], ...]
    """

    batch_id: int
    items: tuple[tuple[int, str], ...]


@dataclass(frozen=True)
class ScoreTask:
    """A batch of (raw, mapped) reaction SMILES ready for scoring.

    ``mapped`` is ``None`` when the mapper failed for that record; the
    scorer will short-circuit to ``failed_reaction_scoring`` without
    spending CPU on the rest of the pipeline.

    :param batch_id: Id propagated from the originating :class:`MapTask`.
    :type batch_id: int
    :param items: Tuple of ``(idx, raw_smiles, mapped_smiles_or_None)``.
    :type items: tuple[tuple[int, str, str | None], ...]
    """

    batch_id: int
    items: tuple[tuple[int, str, str | None], ...]


@dataclass(frozen=True)
class Result:
    """Scored records emitted by a scorer process.

    Each record carries both scoring variants plus FG- and center-precedent
    provenance produced in a single evaluation (see
    :class:`~chemcensor.chemcensor.ScoreResult`).

    :param batch_id: Id propagated from the originating :class:`ScoreTask`.
    :type batch_id: int
    :param items: Tuple of
        ``(idx, raw_smiles, score_with_fg, score_without_fg,
        all_fgs_precedents_are_real, total_number_of_fgs,
        number_of_fgs_covered_by_virtual_precedents,
        all_center_precedents_are_real, failure_stage, failure_category,
        failure_message)`` or, when canonical SMILES are requested, the same
        plus ``cano_rxn``.
    :type items: tuple[ScoredItem, ...]
    """

    batch_id: int
    items: tuple[ScoredItem, ...]


@dataclass(frozen=True)
class CompositionResult:
    """Reaction records emitted by a composer worker process.

    Each item pairs the input ``idx`` with a picklable
    :class:`~chemcensor.composition.records.ReactionRecord`. The writer thread
    looks the reaction's ``document_id`` up by ``idx`` (it is not carried
    through the mapper) and applies the record to the shared database.

    :param batch_id: Id propagated from the originating :class:`ScoreTask`.
    :type batch_id: int
    :param items: Tuple of ``(idx, reaction_record)`` pairs.
    :type items: tuple[tuple[int, "ReactionRecord"], ...]
    """

    batch_id: int
    items: tuple[tuple[int, "ReactionRecord"], ...]
