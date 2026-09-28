import json
from unittest.mock import MagicMock

import numpy as np
import pytest

from chemcensor.composition.records import apply_center
from chemcensor.composition.records import apply_reaction
from chemcensor.composition.records import apply_reaction_record
from chemcensor.composition.records import CenterRecord
from chemcensor.composition.records import ReactionRecord
from chemcensor.composition.records import record_from_reaction
from chemcensor.composition.records import run_distributivity_postprocessing
from chemcensor.configs import CompositionConfig
from chemcensor.db import DBManager
from chemcensor.extraction.errors import ExtractionError
from chemcensor.rules.functional_groups import FG_COLLECTION_SEAR
from chemcensor.rules.functional_groups import FG_SIGNATURE_LENGTH


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sear() -> np.ndarray:
    return np.zeros(FG_COLLECTION_SEAR.num_groups, dtype=np.uint8)


def _make_reaction(
    *,
    canonical_smiles: str = "A>>B",
    is_sis_reaction: bool = False,
    reaction_centers: dict | None = None,
    source: str = "",
    is_virtual: bool = False,
):
    rxn = MagicMock()
    rxn.canonical_smiles = canonical_smiles
    rxn.is_sis_reaction = is_sis_reaction
    rxn.sear_signature = _sear()
    rxn.reaction_centers = reaction_centers or {}
    rxn.source = source
    rxn.is_virtual = is_virtual
    return rxn


def _make_rc(
    smiles: str,
    sig: np.ndarray,
    *,
    is_composite: bool = False,
    components: tuple[str, ...] | None = None,
):
    rc = MagicMock()
    rc.reaction_center_smiles = smiles
    rc.fg_signature = sig
    rc.is_reaction_center_composite = is_composite
    rc.reaction_center_components = components if components is not None else (smiles,)
    return rc


@pytest.fixture
def manager():
    return DBManager()


# ---------------------------------------------------------------------------
# apply_reaction
# ---------------------------------------------------------------------------


class TestApplyReaction:
    def test_inserts_new_reaction(self, manager):
        apply_reaction(manager, "A>>B", "doc1")
        assert manager.find_reaction("A>>B") == ["doc1"]

    def test_duplicate_pair_not_inserted_twice(self, manager):
        apply_reaction(manager, "A>>B", "doc1")
        apply_reaction(manager, "A>>B", "doc1")
        row = manager._conn.execute(
            "SELECT COUNT(*) FROM reactions WHERE reaction_smiles = ?", ("A>>B",)
        ).fetchone()
        assert row[0] == 1

    def test_same_reaction_different_doc_inserts_both(self, manager):
        apply_reaction(manager, "A>>B", "doc1")
        apply_reaction(manager, "A>>B", "doc2")
        assert sorted(manager.find_reaction("A>>B")) == ["doc1", "doc2"]


# ---------------------------------------------------------------------------
# apply_center
# ---------------------------------------------------------------------------


class TestApplyCenter:
    def test_inserts_new_center(self, manager):
        sig = np.array([1, 0, 1], dtype=np.uint8)
        apply_center(
            manager,
            reaction_center_smiles="rc1",
            fg_signature=sig,
            is_multi_component=False,
            components=["rc1"],
            reaction_canonical_smiles="A>>B",
            sear_signature=_sear(),
        )
        result = manager.find_center("rc1")
        assert result is not None
        assert np.array_equal(result, sig)

    def test_updates_existing_center_with_bitwise_or(self, manager):
        first = np.array([1, 0, 0], dtype=np.uint8)
        second = np.array([0, 1, 0], dtype=np.uint8)
        for sig, rxn in ((first, "r1>>p"), (second, "r2>>p")):
            apply_center(
                manager,
                reaction_center_smiles="rc_x",
                fg_signature=sig,
                is_multi_component=False,
                components=["rc_x"],
                reaction_canonical_smiles=rxn,
                sear_signature=_sear(),
            )
        assert np.array_equal(
            manager.find_center("rc_x"), np.array([1, 1, 0], dtype=np.uint8)
        )

    def test_stores_component_metadata(self, manager):
        sig = np.array([1, 0, 1], dtype=np.uint8)
        apply_center(
            manager,
            reaction_center_smiles="rc1",
            fg_signature=sig,
            is_multi_component=True,
            components=["A>>B", "C>>D"],
            reaction_canonical_smiles="A.C>>B.D",
            sear_signature=_sear(),
        )
        row = manager._conn.execute(
            "SELECT is_multi_component, components FROM reaction_centers"
            " WHERE reaction_center_smiles = ?",
            ("rc1",),
        ).fetchone()
        assert row[0] == 1
        assert json.loads(row[1]) == ["A>>B", "C>>D"]


# ---------------------------------------------------------------------------
# record_from_reaction
# ---------------------------------------------------------------------------


class TestRecordFromReaction:
    def test_sis_reaction_has_no_centers(self):
        extractor = MagicMock()
        rxn = _make_reaction(canonical_smiles="SIS>>RXN", is_sis_reaction=True)

        record = record_from_reaction(rxn, extractor)

        assert isinstance(record, ReactionRecord)
        assert record.is_sis is True
        assert record.canonical_smiles == "SIS>>RXN"
        assert record.centers == ()
        extractor.extract_rc.assert_not_called()

    def test_normal_reaction_collects_centers(self):
        sig = np.array([1, 0, 1], dtype=np.uint8)
        extracted = _make_reaction(
            canonical_smiles="A>>B",
            reaction_centers={"RC1": _make_rc("rc1", sig)},
        )
        extractor = MagicMock()
        extractor.extract_rc.return_value = extracted

        record = record_from_reaction(
            _make_reaction(canonical_smiles="A>>B"), extractor
        )

        assert record.is_sis is False
        assert len(record.centers) == 1
        center = record.centers[0]
        assert isinstance(center, CenterRecord)
        assert center.reaction_center_smiles == "rc1"
        assert np.array_equal(center.fg_signature, sig)

    def test_extraction_error_yields_no_centers(self):
        extractor = MagicMock()
        extractor.extract_rc.side_effect = ExtractionError("boom")

        record = record_from_reaction(
            _make_reaction(canonical_smiles="A>>B"), extractor
        )

        assert record.is_sis is False
        assert record.centers == ()


# ---------------------------------------------------------------------------
# apply_reaction_record
# ---------------------------------------------------------------------------


class TestApplyReactionRecord:
    def test_applies_reaction_and_centers(self, manager):
        sig = np.array([1, 1, 0], dtype=np.uint8)
        record = ReactionRecord(
            canonical_smiles="A>>B",
            is_sis=False,
            sear_signature=_sear(),
            centers=(
                CenterRecord(
                    reaction_center_smiles="rc1",
                    fg_signature=sig,
                    is_multi_component=False,
                    components=("rc1",),
                ),
            ),
        )

        apply_reaction_record(manager, record, "doc1")

        assert manager.find_reaction("A>>B") == ["doc1"]
        assert np.array_equal(manager.find_center("rc1"), sig)
        assert manager.find_center_to_reaction("rc1", "A>>B")

    def test_sis_record_adds_reaction_only(self, manager):
        record = ReactionRecord(
            canonical_smiles="SIS>>RXN",
            is_sis=True,
            sear_signature=_sear(),
            centers=(),
        )

        apply_reaction_record(manager, record, "doc1")

        assert manager.find_reaction("SIS>>RXN") == ["doc1"]
        row = manager._conn.execute("SELECT COUNT(*) FROM reaction_centers").fetchone()
        assert row[0] == 0


# ---------------------------------------------------------------------------
# run_distributivity_postprocessing
# ---------------------------------------------------------------------------


class TestRunDistributivityPostprocessing:
    def test_merges_multi_with_and_of_components(self, manager):
        sig_multi = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
        sig_multi[4] = 1
        sig_a = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
        sig_a[0] = 1
        sig_a[1] = 1
        sig_b = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
        sig_b[0] = 1
        sig_b[2] = 1
        sear = _sear()

        manager.add_reaction_center("comp_a>>y", sig_a)
        manager.add_reaction_center("comp_b>>y", sig_b)
        manager.add_reaction_center(
            "multi>>y",
            sig_multi,
            is_multi_component=True,
            components=["comp_a>>y", "comp_b>>y"],
        )
        for rs in ("r1>>q", "r2>>q", "r3>>q"):
            manager.add_reaction(rs, "doc")
            manager.add_center_to_reaction("multi>>y", rs, sig_multi, sear)

        assert (
            manager.count_center("multi>>y")
            > CompositionConfig.distributivity_threshold
        )

        run_distributivity_postprocessing(manager)

        out = manager.find_center("multi>>y")
        assert out[0] == 1  # AND(sig_a, sig_b): bit shared by both components
        assert out[1] == 0
        assert out[2] == 0
        assert out[4] == 1  # original composite-row bit preserved (OR with AND)


class TestVirtualApply:
    def test_or_does_not_cross_virtual_groups(self, manager):
        real_sig = np.array([1, 0, 0], dtype=np.uint8)
        virt_sig = np.array([0, 1, 0], dtype=np.uint8)
        apply_center(
            manager,
            reaction_center_smiles="rc_shared",
            fg_signature=real_sig,
            is_multi_component=False,
            components=["rc_shared"],
            reaction_canonical_smiles="r1>>p",
            sear_signature=_sear(),
            is_virtual=False,
        )
        apply_center(
            manager,
            reaction_center_smiles="rc_shared",
            fg_signature=virt_sig,
            is_multi_component=False,
            components=["rc_shared"],
            reaction_canonical_smiles="r2>>p",
            sear_signature=_sear(),
            is_virtual=True,
        )
        assert np.array_equal(
            manager.find_center("rc_shared", is_virtual=False), real_sig
        )
        assert np.array_equal(
            manager.find_center("rc_shared", is_virtual=True), virt_sig
        )

    def test_apply_reaction_stores_source_for_virtual(self, manager):
        apply_reaction(manager, "A>>B", "doc1", is_virtual=True, source="42")
        row = manager._conn.execute(
            "SELECT is_virtual, source FROM reactions WHERE reaction_smiles = ?",
            ("A>>B",),
        ).fetchone()
        assert row == (1, "42")

    def test_distributivity_stays_within_virtual_group(self, manager):
        sig_multi = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
        sig_multi[4] = 1
        sig_a = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
        sig_a[0] = 1
        sig_a[1] = 1
        sig_b = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
        sig_b[0] = 1
        sig_b[2] = 1
        sear = _sear()

        # Real components would AND to bit 0; virtual multi should ignore them.
        manager.add_reaction_center("comp_a>>y", sig_a, is_virtual=False)
        manager.add_reaction_center("comp_b>>y", sig_b, is_virtual=False)
        manager.add_reaction_center(
            "multi>>y",
            sig_multi,
            is_multi_component=True,
            components=["comp_a>>y", "comp_b>>y"],
            is_virtual=True,
        )
        for rs in ("r1>>q", "r2>>q", "r3>>q"):
            manager.add_reaction(rs, "doc", is_virtual=True)
            manager.add_center_to_reaction(
                "multi>>y", rs, sig_multi, sear, is_virtual=True
            )

        run_distributivity_postprocessing(manager)

        out = manager.find_center("multi>>y", is_virtual=True)
        assert out is not None
        assert out[0] == 0  # real components must not affect virtual multi
        assert out[4] == 1
