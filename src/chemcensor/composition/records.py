"""Picklable composition records and shared DB-aggregation helpers.

The serial :class:`~chemcensor.composition.composer.ReactionCenterDBComposer`
and the parallel pipeline (:mod:`chemcensor.parallel.composition_orchestrator`)
must store reaction centers identically. They cannot share :class:`Reaction`
objects, however: those carry an RDKit ``ChemicalReaction`` (via
``reaction_transform``) which is not picklable, so they cannot cross a
process boundary. This module therefore defines:

* lightweight, picklable records (:class:`ReactionRecord`,
  :class:`CenterRecord`) that a worker process can extract from a processed
  :class:`Reaction` and send to the writer, and
* the aggregation primitives (:func:`apply_reaction`, :func:`apply_center`,
  :func:`run_distributivity_postprocessing`) that mutate a
  :class:`~chemcensor.db.manager.DBManager`.

Both the serial composer and the parallel writer route through the same
primitives, so the two paths produce byte-for-byte equivalent databases.
Every primitive is order-independent (bitwise-OR of FG signatures, dedup of
reactions/centers), which is what makes the parallel build correct.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..basic import Reaction
from ..configs import CompositionConfig
from ..db import DBManager
from ..extraction import ReactionCenterExtractor
from ..extraction.errors import ExtractionError


@dataclass(frozen=True)
class CenterRecord:
    """A single reaction center ready to be stored in the database.

    :param reaction_center_smiles: Canonical reaction-center SMILES (PK).
    :type reaction_center_smiles: str
    :param fg_signature: Functional-group signature for this center.
    :type fg_signature: np.ndarray
    :param is_multi_component: Whether the center is composite (>1 component).
    :type is_multi_component: bool
    :param components: Simple-component SMILES of a composite center.
    :type components: tuple[str, ...]
    """

    reaction_center_smiles: str
    fg_signature: np.ndarray
    is_multi_component: bool
    components: tuple[str, ...]


@dataclass(frozen=True)
class ReactionRecord:
    """Everything the writer needs to store one processed reaction.

    ``centers`` is empty for SIS reactions (which are still inserted into the
    ``reactions`` table but contribute no centers) and for reactions whose
    center extraction failed — matching the serial composer, which adds every
    processed reaction but only extracts centers for the non-SIS ones.

    :param canonical_smiles: Canonical reaction SMILES.
    :type canonical_smiles: str
    :param is_sis: Whether the reaction is a stereo-isomerism-selection one.
    :type is_sis: bool
    :param sear_signature: SEAr context signature for the reaction.
    :type sear_signature: np.ndarray
    :param centers: Extracted reaction centers (empty if SIS / extraction
        failed).
    :type centers: tuple[CenterRecord, ...]
    :param source: Provenance string (e.g. CSV ``source_id`` for virtual).
    :type source: str
    :param is_virtual: Whether the reaction belongs to the virtual group.
    :type is_virtual: bool
    """

    canonical_smiles: str
    is_sis: bool
    sear_signature: np.ndarray
    centers: tuple[CenterRecord, ...]
    source: str = ""
    is_virtual: bool = False


def record_from_reaction(
    reaction: Reaction,
    extractor: ReactionCenterExtractor,
) -> ReactionRecord:
    """Build a picklable :class:`ReactionRecord` from a processed reaction.

    Mirrors the per-reaction half of
    :meth:`ReactionCenterDBComposer._compose_batch`: SIS reactions carry no
    centers, and a non-SIS reaction whose extraction raises
    :class:`ExtractionError` is stored with no centers (the reaction itself is
    still recorded by the caller).

    :param reaction: A reaction that has already been through the processing
        pipeline (must not be a dummy/sentinel).
    :type reaction: Reaction
    :param extractor: Extractor used to derive reaction centers.
    :type extractor: ReactionCenterExtractor
    :return: A picklable record describing the reaction and its centers.
    :rtype: ReactionRecord
    """
    if reaction.is_sis_reaction:
        return ReactionRecord(
            canonical_smiles=reaction.canonical_smiles,
            is_sis=True,
            sear_signature=np.asarray(reaction.sear_signature, dtype=np.uint8),
            centers=(),
            source=reaction.source,
            is_virtual=reaction.is_virtual,
        )

    try:
        extracted = extractor.extract_rc(reaction)
    except ExtractionError:
        extracted = None

    centers: tuple[CenterRecord, ...] = ()
    if extracted is not None:
        centers = tuple(
            CenterRecord(
                reaction_center_smiles=rc.reaction_center_smiles,
                fg_signature=np.asarray(rc.fg_signature, dtype=np.uint8),
                is_multi_component=rc.is_reaction_center_composite,
                components=tuple(rc.reaction_center_components),
            )
            for rc in extracted.reaction_centers.values()
        )

    return ReactionRecord(
        canonical_smiles=reaction.canonical_smiles,
        is_sis=False,
        sear_signature=np.asarray(reaction.sear_signature, dtype=np.uint8),
        centers=centers,
        source=reaction.source,
        is_virtual=reaction.is_virtual,
    )


def apply_reaction(
    manager: DBManager,
    canonical_smiles: str,
    document_id: str,
    *,
    is_virtual: bool = False,
    source: str = "",
) -> None:
    """Insert a reaction unless the ``(smiles, document_id, is_virtual)``
    triple already exists.

    This is the per-reaction body of
    :meth:`ReactionCenterDBComposer._add_reactions`.

    :param manager: Writable database manager.
    :type manager: DBManager
    :param canonical_smiles: Canonical reaction SMILES.
    :type canonical_smiles: str
    :param document_id: Document ID the reaction originates from.
    :type document_id: str
    :param is_virtual: Whether the reaction is virtual.
    :type is_virtual: bool
    :param source: Provenance string for virtual reactions.
    :type source: str
    """
    document_ids = manager.find_reaction_document_ids(
        canonical_smiles, is_virtual=is_virtual
    )
    if document_ids is not None and document_id in document_ids:
        return
    manager.add_reaction(
        canonical_smiles,
        document_id,
        is_virtual=is_virtual,
        source=source,
    )


def apply_center(
    manager: DBManager,
    *,
    reaction_center_smiles: str,
    fg_signature: np.ndarray,
    is_multi_component: bool,
    components: list[str],
    reaction_canonical_smiles: str,
    sear_signature: np.ndarray,
    is_virtual: bool = False,
) -> None:
    """Insert or update one reaction center and its bridge row.

    This is the per-center body of
    :meth:`ReactionCenterDBComposer._add_centers`: if the center already
    exists (within the same virtuality group) its FG-signature is OR-ed with
    the new one, otherwise a new row is created; the bridge row is added only
    when the ``(center, is_virtual, reaction)`` triple is new.

    :param manager: Writable database manager.
    :type manager: DBManager
    :param reaction_center_smiles: Canonical reaction-center SMILES.
    :type reaction_center_smiles: str
    :param fg_signature: FG-signature for this center.
    :type fg_signature: np.ndarray
    :param is_multi_component: Whether the center is composite.
    :type is_multi_component: bool
    :param components: Simple-component SMILES (for composite centers).
    :type components: list[str]
    :param reaction_canonical_smiles: Canonical SMILES of the owning reaction.
    :type reaction_canonical_smiles: str
    :param sear_signature: SEAr signature of the owning reaction.
    :type sear_signature: np.ndarray
    :param is_virtual: Whether the center belongs to the virtual group.
    :type is_virtual: bool
    """
    existing = manager.find_center(reaction_center_smiles, is_virtual=is_virtual)
    if existing is not None:
        combined = np.bitwise_or(existing, fg_signature)
        manager.update(reaction_center_smiles, combined, is_virtual=is_virtual)
    else:
        manager.add_reaction_center(
            reaction_center_smiles,
            fg_signature,
            is_multi_component=is_multi_component,
            components=components,
            is_virtual=is_virtual,
        )
    if not manager.find_center_to_reaction(
        reaction_center_smiles,
        reaction_canonical_smiles,
        is_virtual=is_virtual,
    ):
        manager.add_center_to_reaction(
            reaction_center_smiles,
            reaction_canonical_smiles,
            fg_signature,
            sear_signature,
            is_virtual=is_virtual,
        )


def apply_reaction_record(
    manager: DBManager,
    record: ReactionRecord,
    document_id: str,
) -> None:
    """Apply a full :class:`ReactionRecord` to the database.

    Adds the reaction itself, then every center it carries. Mirrors a single
    reaction's contribution in :meth:`ReactionCenterDBComposer._compose_batch`.

    :param manager: Writable database manager.
    :type manager: DBManager
    :param record: The record to store.
    :type record: ReactionRecord
    :param document_id: Document ID the reaction originates from.
    :type document_id: str
    """
    apply_reaction(
        manager,
        record.canonical_smiles,
        document_id,
        is_virtual=record.is_virtual,
        source=record.source,
    )
    for center in record.centers:
        apply_center(
            manager,
            reaction_center_smiles=center.reaction_center_smiles,
            fg_signature=center.fg_signature,
            is_multi_component=center.is_multi_component,
            components=list(center.components),
            reaction_canonical_smiles=record.canonical_smiles,
            sear_signature=record.sear_signature,
            is_virtual=record.is_virtual,
        )


def run_distributivity_postprocessing(manager: DBManager) -> None:
    """Apply FG-signature distributivity for frequent multi-component centers.

    For each multi-component center appearing in more than
    ``CompositionConfig.distributivity_threshold`` reactions, fold the bitwise
    AND of its existing components' signatures into the composite center's
    FG-signature (kept via OR). Component lookup and update stay within the
    same virtuality group. Identical to
    :meth:`ReactionCenterDBComposer._run_postprocessing`.

    :param manager: Writable database manager.
    :type manager: DBManager
    """
    for (
        center_smiles,
        is_virtual,
        current_fg_sig,
        components,
    ) in manager.list_multi_component_for_dist(
        CompositionConfig.distributivity_threshold
    ):
        comp_sigs = [
            manager.find_center(comp_smiles, is_virtual=is_virtual)
            for comp_smiles in set(components)
        ]
        comp_sigs_no_none = [x for x in comp_sigs if x is not None]
        if comp_sigs_no_none:
            combined = np.bitwise_and.reduce(comp_sigs_no_none)
            merged = np.bitwise_or(current_fg_sig, combined)
            manager.update(center_smiles, merged, is_virtual=is_virtual)
