from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .basic import ReactionCenterType


class PrecedentStatus(StrEnum):
    """Database precedent status for one reaction center."""

    REAL = "real"
    VIRTUAL = "virtual"
    ABSENT = "absent"


class TraceOutcome(StrEnum):
    """High-level path that produced the final score."""

    FAILED = "failed"
    SIS = "sis"
    EXACT_MATCH = "exact_match"
    TAUTOMERIZATION = "tautomerization"
    CENTER_COVERAGE = "center_coverage"
    NO_COVERAGE = "no_coverage"


@dataclass(frozen=True)
class PrecedentExample:
    """One reaction/document example supporting a reaction center."""

    reaction_smiles: str
    document_id: str
    source: str
    is_virtual: bool


@dataclass(frozen=True)
class FunctionalGroupEvidence:
    """Static FG description and its reaction-center precedents.

    :param name: Internal descriptive functional-group name.
    :type name: str
    :param ui_name: Stable human-readable display name.
    :type ui_name: str
    :param smarts: SMARTS pattern used to identify the functional group.
    :type smarts: str
    """

    name: str
    ui_name: str
    smarts: str
    real_precedents: tuple[PrecedentExample, ...] = ()
    virtual_precedents: tuple[PrecedentExample, ...] = ()


@dataclass(frozen=True)
class CenterTrace:
    """Trace of one extracted reaction center's database coverage.

    :param center_type: RC context level.
    :type center_type: ReactionCenterType
    :param reaction_center_smiles: Canonical reaction-center SMILES used as
        the database key.
    :type reaction_center_smiles: str
    :param precedent_status: Preferred precedent status. Real rows take
        precedence over virtual rows when both exist.
    :type precedent_status: PrecedentStatus
    :param precedent_count: Number of reactions linked to the preferred
        precedent status.
    :type precedent_count: int
    :param required_functional_groups: Human-readable names of functional
        groups required by this center.
    :type required_functional_groups: tuple[str, ...]
    :param missing_functional_groups: Required groups covered by neither real
        nor virtual precedent signatures.
    :type missing_functional_groups: tuple[str, ...]
    :param virtual_functional_groups: Required groups supplied by the virtual
        signature because the real signature did not cover them.
    :type virtual_functional_groups: tuple[str, ...]
    :param included_without_functional_groups: Whether this center extended
        the consecutive center-presence score.
    :type included_without_functional_groups: bool
    :param included_with_functional_groups: Whether this center extended the
        consecutive functional-group-aware score.
    :type included_with_functional_groups: bool
    :param real_precedents: Up to three real reaction examples.
    :type real_precedents: tuple[PrecedentExample, ...]
    :param virtual_precedents: Up to three virtual reaction examples.
    :type virtual_precedents: tuple[PrecedentExample, ...]
    :param functional_group_evidence: Per-required-FG precedent examples whose
        bridge-row signatures contain that functional group.
    :type functional_group_evidence: tuple[FunctionalGroupEvidence, ...]
    """

    center_type: ReactionCenterType
    reaction_center_smiles: str
    precedent_status: PrecedentStatus
    precedent_count: int
    required_functional_groups: tuple[str, ...]
    missing_functional_groups: tuple[str, ...]
    virtual_functional_groups: tuple[str, ...]
    included_without_functional_groups: bool
    included_with_functional_groups: bool
    real_precedents: tuple[PrecedentExample, ...] = ()
    virtual_precedents: tuple[PrecedentExample, ...] = ()
    functional_group_evidence: tuple[FunctionalGroupEvidence, ...] = ()
