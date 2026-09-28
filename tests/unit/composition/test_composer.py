import csv
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import numpy as np
import pytest

from chemcensor.basic import Reaction
from chemcensor.composition.composer import ReactionCenterDBComposer
from chemcensor.configs import CompositionConfig
from chemcensor.db import DBManager
from chemcensor.db.errors import InvalidDBVersionError
from chemcensor.rules.functional_groups import FG_COLLECTION_SEAR
from chemcensor.rules.functional_groups import FG_SIGNATURE_LENGTH


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_csv(path: Path, smiles: list[str], column: str = "reaction_smiles"):
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([column])
        for s in smiles:
            writer.writerow([s])


def _make_reaction(
    smiles: str = "A>>B",
    dummy: bool = False,
    is_sis_reaction: bool = False,
    reaction_centers: dict | None = None,
    *,
    is_virtual: bool = False,
    source: str = "",
):
    rxn = MagicMock()
    rxn.reaction_smiles = smiles
    rxn.dummy = dummy
    rxn.is_sis_reaction = is_sis_reaction
    rxn.reaction_centers = reaction_centers or {}
    rxn.canonical_smiles = smiles
    rxn.document_id = "test"
    rxn.source = source
    rxn.is_virtual = is_virtual
    rxn.sear_signature = np.zeros(FG_COLLECTION_SEAR.num_groups, dtype=np.uint8)

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


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_processor():
    return MagicMock()


@pytest.fixture
def mock_extractor():
    return MagicMock()


@pytest.fixture
def manager():
    return DBManager()


@pytest.fixture
def composer(mock_processor, mock_extractor):
    return ReactionCenterDBComposer(
        processor=mock_processor,
        reaction_center_extractor=mock_extractor,
        batch_size=5,
    )


# ---------------------------------------------------------------------------
# Tests – _add_centers
# ---------------------------------------------------------------------------


class TestAddCenters:
    def test_inserts_new_centers(self, composer):
        sig = np.array([1, 0, 1], dtype=np.uint8)
        rxn = _make_reaction(reaction_centers={"RC1": _make_rc("rc1", sig)})

        composer._add_centers([rxn])

        result = composer._manager.find_center("rc1")
        assert result is not None
        assert np.array_equal(result, sig)

    def test_inserts_component_metadata(self, composer):
        sig = np.array([1, 0, 1], dtype=np.uint8)
        rc = _make_rc(
            "rc1",
            sig,
            is_composite=True,
            components=("A>>B", "C>>D"),
        )
        rxn = _make_reaction(reaction_centers={"RC1": rc})

        composer._add_centers([rxn])

        row = composer._manager._conn.execute(
            "SELECT is_multi_component, components FROM reaction_centers"
            " WHERE reaction_center_smiles = ?",
            ("rc1",),
        ).fetchone()
        assert row is not None
        assert row[0] == 1
        assert json.loads(row[1]) == ["A>>B", "C>>D"]

    def test_updates_existing_center_with_bitwise_or(self, composer):
        existing_sig = np.array([1, 0, 0], dtype=np.uint8)
        new_sig = np.array([0, 1, 0], dtype=np.uint8)
        expected = np.array([1, 1, 0], dtype=np.uint8)

        rxn1 = _make_reaction(
            smiles="rxn1", reaction_centers={"RC1": _make_rc("rc_x", existing_sig)}
        )
        composer._add_centers([rxn1])
        rxn2 = _make_reaction(
            smiles="rxn2", reaction_centers={"RC1": _make_rc("rc_x", new_sig)}
        )
        composer._add_centers([rxn2])

        result = composer._manager.find_center("rc_x")
        assert result is not None
        assert np.array_equal(result, expected)

    def test_multiple_centers_per_reaction(self, composer):
        sig1 = np.array([1, 0], dtype=np.uint8)
        sig2 = np.array([0, 1], dtype=np.uint8)
        rxn = _make_reaction(
            reaction_centers={
                "RC1": _make_rc("rc_a", sig1),
                "RC2": _make_rc("rc_b", sig2),
            },
        )

        composer._add_centers([rxn])

        assert composer._manager.find_center("rc_a") is not None
        assert composer._manager.find_center("rc_b") is not None

    def test_virtual_composer_does_not_or_with_real(
        self, mock_processor, mock_extractor
    ):
        real_sig = np.array([1, 0, 0], dtype=np.uint8)
        virt_sig = np.array([0, 1, 0], dtype=np.uint8)

        composer = ReactionCenterDBComposer(
            mock_processor, mock_extractor, batch_size=5
        )
        composer._add_centers(
            [
                _make_reaction(
                    reaction_centers={"RC1": _make_rc("rc_x", real_sig)},
                    is_virtual=False,
                )
            ]
        )
        composer._add_centers(
            [
                _make_reaction(
                    reaction_centers={"RC1": _make_rc("rc_x", virt_sig)},
                    is_virtual=True,
                )
            ]
        )

        assert np.array_equal(
            composer._manager.find_center("rc_x", is_virtual=False), real_sig
        )
        assert np.array_equal(
            composer._manager.find_center("rc_x", is_virtual=True), virt_sig
        )


class TestComposeCsvVirtual:
    def test_compose_reads_per_row_is_virtual_and_source(
        self, mock_processor, mock_extractor, tmp_path
    ):
        csv_path = tmp_path / "mixed.csv"
        out_path = tmp_path / "out.sqlite"
        with csv_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "library_id",
                    "cleaned_rxn",
                    "document_id",
                    "is_virtual",
                    "source_id",
                ]
            )
            writer.writerow(["lib1", "A>>B", "pat1", "0", ""])
            writer.writerow(["lib1", "C>>D", "pat2", "1", "21"])

        def _process_with_doc(batch):
            processed = []
            for r in batch:
                rxn = _make_reaction(
                    r.reaction_smiles,
                    is_virtual=r.is_virtual,
                    source=r.source,
                )
                rxn.document_id = r.document_id
                processed.append(rxn)
            return processed

        mock_processor.process_batch.side_effect = _process_with_doc

        def _extract(batch):
            out = []
            for r in batch:
                rxn = _make_reaction(
                    r.canonical_smiles,
                    reaction_centers={
                        "RC1": _make_rc(
                            f"rc_{r.canonical_smiles}",
                            np.array(
                                [1, 0] if not r.is_virtual else [0, 1],
                                dtype=np.uint8,
                            ),
                        )
                    },
                    is_virtual=r.is_virtual,
                    source=r.source,
                )
                rxn.document_id = r.document_id
                out.append(rxn)
            return out

        mock_extractor.extract_rc_for_batch.side_effect = _extract

        composer = ReactionCenterDBComposer(
            mock_processor,
            mock_extractor,
            batch_size=5,
        )
        composer.compose(csv_path, out_path, db_version="U9-TEST")

        loaded = DBManager.load(out_path)
        assert loaded.find_center("rc_A>>B", is_virtual=False) is not None
        assert loaded.find_center("rc_C>>D", is_virtual=True) is not None
        real_row = loaded._conn.execute(
            "SELECT is_virtual, source FROM reactions WHERE reaction_smiles = ?",
            ("A>>B",),
        ).fetchone()
        virt_row = loaded._conn.execute(
            "SELECT is_virtual, source FROM reactions WHERE reaction_smiles = ?",
            ("C>>D",),
        ).fetchone()
        assert real_row == (0, "")
        assert virt_row == (1, "21")


# ---------------------------------------------------------------------------
# Tests – _compose_batch
# ---------------------------------------------------------------------------


class TestComposeBatch:
    def test_inserts_reactions(self, mock_processor, mock_extractor):
        rxn = _make_reaction("A>>B", reaction_centers={})
        mock_processor.process_batch.return_value = [rxn]
        mock_extractor.extract_rc_for_batch.side_effect = lambda b: b

        composer = ReactionCenterDBComposer(
            mock_processor,
            mock_extractor,
            batch_size=5,
        )
        composer._compose_batch([Reaction(reaction_smiles="A>>B")])

        assert composer._manager.find_reaction("A>>B") is not None

    def test_sis_reactions_excluded_from_extraction(
        self, mock_processor, mock_extractor
    ):
        sis_rxn = _make_reaction("SIS>>RXN", is_sis_reaction=True)
        normal_rxn = _make_reaction("A>>B")
        mock_processor.process_batch.return_value = [sis_rxn, normal_rxn]
        mock_extractor.extract_rc_for_batch.side_effect = lambda b: b

        composer = ReactionCenterDBComposer(
            mock_processor,
            mock_extractor,
            batch_size=5,
        )
        composer._compose_batch(
            [Reaction(reaction_smiles="SIS>>RXN"), Reaction(reaction_smiles="A>>B")]
        )

        call_args = mock_extractor.extract_rc_for_batch.call_args[0][0]
        assert len(call_args) == 1
        assert call_args[0].reaction_smiles == "A>>B"

    def test_sis_reactions_still_inserted(self, mock_processor, mock_extractor):
        sis_rxn = _make_reaction("SIS>>RXN", is_sis_reaction=True)
        mock_processor.process_batch.return_value = [sis_rxn]
        mock_extractor.extract_rc_for_batch.side_effect = lambda b: b

        composer = ReactionCenterDBComposer(
            mock_processor,
            mock_extractor,
            batch_size=5,
        )
        composer._compose_batch([Reaction(reaction_smiles="SIS>>RXN")])

        assert composer._manager.find_reaction("SIS>>RXN") is not None


class TestAddReactions:
    def test_duplicate_reaction_and_document_id_does_not_raise(
        self, mock_processor, mock_extractor
    ):
        rxn_a = _make_reaction("A>>B")
        rxn_a.document_id = "same_doc_id1"
        rxn_b = _make_reaction("A>>B")
        rxn_b.document_id = "same_doc_id1"
        mock_processor.process_batch.return_value = [rxn_a, rxn_b]
        mock_extractor.extract_rc_for_batch.side_effect = lambda b: b

        composer = ReactionCenterDBComposer(
            mock_processor,
            mock_extractor,
            batch_size=5,
        )
        composer._compose_batch(
            [Reaction(reaction_smiles="A>>B"), Reaction(reaction_smiles="A>>B")]
        )

        assert "same_doc_id1" in composer._manager.find_reaction("A>>B")
        row = composer._manager._conn.execute(
            "SELECT COUNT(*) FROM reactions WHERE reaction_smiles = ?", ("A>>B",)
        ).fetchone()
        assert row[0] == 1

    def test_same_reaction_different_document_id_inserts_both(
        self, mock_processor, mock_extractor
    ):
        rxn_a = _make_reaction("A>>B")
        rxn_a.document_id = "doc1"
        rxn_b = _make_reaction("A>>B")
        rxn_b.document_id = "doc2"
        mock_processor.process_batch.return_value = [rxn_a, rxn_b]
        mock_extractor.extract_rc_for_batch.side_effect = lambda b: b

        composer = ReactionCenterDBComposer(
            mock_processor,
            mock_extractor,
            batch_size=5,
        )
        composer._compose_batch(
            [Reaction(reaction_smiles="A>>B"), Reaction(reaction_smiles="A>>B")]
        )

        row = composer._manager._conn.execute(
            "SELECT COUNT(*) FROM reactions WHERE reaction_smiles = ?", ("A>>B",)
        ).fetchone()
        assert row[0] == 2

    def test_duplicate_pair_among_multiple_document_ids_does_not_raise(
        self, mock_processor, mock_extractor
    ):
        """Reproduces the case where a reaction has several document IDs and a
        duplicate (smiles, document_id) pair appears later in the batch."""
        smiles = "C[Si](C)(C)Cl>>Cl"
        doc_ids = [
            "US20090247591A1",
            "US20070015784A1",
            "US20070281954A1",
            "US20070129347A1",
            "US20070129347A1",
        ]
        reactions = []
        for doc_id in doc_ids:
            rxn = _make_reaction(smiles)
            rxn.document_id = doc_id
            reactions.append(rxn)

        mock_processor.process_batch.return_value = reactions
        mock_extractor.extract_rc_for_batch.side_effect = lambda b: b

        composer = ReactionCenterDBComposer(
            mock_processor,
            mock_extractor,
            batch_size=10,
        )
        composer._compose_batch([Reaction(reaction_smiles=smiles)] * len(doc_ids))

        row = composer._manager._conn.execute(
            "SELECT COUNT(*) FROM reactions WHERE reaction_smiles = ?",
            (smiles,),
        ).fetchone()
        assert row[0] == 4


# ---------------------------------------------------------------------------
# Smoke test – real pipeline with test CSV
# ---------------------------------------------------------------------------


@pytest.mark.heavy_test
class TestComposeSmokeTest:
    """Run the full pipeline against the test CSV.

    Requires RDKit and rxnmapper, so marked as heavy.
    """

    REFERENCE_CSV = Path(__file__).parent / "reaction_database_test.csv"

    def test_compose_with_real_pipeline(self):
        from chemcensor.basic import ReactionCenterType
        from chemcensor.configs import CompositionPipelineConfig
        from chemcensor.extraction import ReactionCenterExtractor

        if not self.REFERENCE_CSV.exists():
            pytest.skip(f"Test CSV not found: {self.REFERENCE_CSV}")

        processor = CompositionPipelineConfig(mapper_batch_size=20).build_processor()
        extractor = ReactionCenterExtractor(max_center_type=ReactionCenterType.RC4)

        composer = ReactionCenterDBComposer(
            processor=processor,
            reaction_center_extractor=extractor,
            batch_size=20,
            reaction_smiles_column="reaction_smiles",
            document_id_column="document_id",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test_output.sqlite"
            composer.compose(self.REFERENCE_CSV, db_path, db_version="U9-TEST")

            assert db_path.exists()

            loaded = DBManager.load(db_path)

            row = loaded._conn.execute(
                "SELECT COUNT(*) FROM reaction_centers"
            ).fetchone()
            assert row[0] == 102, "Database should contain 102 reaction centers"
            assert (
                loaded.find_reaction(
                    "CC1=NN(c2ccccc2)C(=O)C1C(=O)CC=O.CNN"
                    ">>Cc1cc(-c2c(C)nn(-c3ccccc3)c2O)n(C)n1"
                )
                is not None
            )
            result = loaded.find_center("CC(O)=O.CN>>CNC(C)=O")
            assert result is not None
            assert 76 in result.nonzero()[0]  # Alcohol from reaction #20
            assert 321 in result.nonzero()[0]  # Ketone from reaction #19
            assert loaded.find_reaction("O.O.O.[Zn++]>>[Zn++]") is None  # sentinel

            check_multi_comp = loaded._conn.execute(
                "SELECT is_multi_component FROM reaction_centers"
                " WHERE reaction_center_smiles = ?",
                ("CN(C)C(=O)OC(C)(C)C.CN(C)C(=O)OC(C)(C)C>>CNC.CNC",),
            ).fetchone()
            assert check_multi_comp[0] == 1

            check_components = loaded._conn.execute(
                "SELECT components FROM reaction_centers"
                " WHERE reaction_center_smiles = ?",
                ("CO[Si](C)(C)C.CO[Si](C)(C)C.CO[Si](C)(C)C>>CO.CO.CO",),
            ).fetchone()
            assert json.loads(check_components[0]) == [
                "CO[Si](C)(C)C>>CO",
                "CO[Si](C)(C)C>>CO",
                "CO[Si](C)(C)C>>CO",
            ]
            # check distributivity
            combined = loaded.find_center(
                "CN(C)C(=O)OC(C)(C)C.CN(C)C(=O)OC(C)(C)C" ">>CNC.CNC"
            )
            assert 361 in combined.nonzero()[0]  # Phenol from single de-Boc(test45)


class TestRunPostprocessing:
    def test_no_distributivity_when_reaction_count_not_above_threshold(self, composer):
        """``count_center`` must be *strictly greater* than the threshold for
        distributivity.
        """
        m = composer._manager
        sig_multi = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
        sig_multi[0] = 1
        sig_a = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
        sig_a[1] = 1
        sig_b = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
        sig_b[2] = 1
        sear = np.zeros(FG_COLLECTION_SEAR.num_groups, dtype=np.uint8)

        m.add_reaction_center("comp_a>>x", sig_a)
        m.add_reaction_center("comp_b>>x", sig_b)
        m.add_reaction_center(
            "multi>>x",
            sig_multi,
            is_multi_component=True,
            components=["comp_a>>x", "comp_b>>x"],
        )
        for rs in ("r1>>p", "r2>>p"):
            m.add_reaction(rs, "doc")
            m.add_center_to_reaction("multi>>x", rs, sig_multi, sear)

        composer._run_postprocessing()

        out = m.find_center("multi>>x")
        assert out is not None
        assert out[0] == 1
        assert out[1] == 0
        assert out[2] == 0

    def test_distributivity_merges_multi_with_and_of_components(self, composer):
        """Frequent multi-component centers get ``fg |= (AND of component sigs)``.

        The stored multi-center signature is not replaced wholesale: bits already
        set on the composite row are kept via OR, while bits present in *every*
        component row (bitwise AND) are folded in. Component SMILES are de-duplicated
        with ``set`` when aggregating.
        """
        m = composer._manager
        sig_multi = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
        sig_multi[4] = 1
        sig_a = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
        sig_a[0] = 1
        sig_a[1] = 1
        sig_b = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
        sig_b[0] = 1
        sig_b[2] = 1
        sear = np.zeros(FG_COLLECTION_SEAR.num_groups, dtype=np.uint8)

        m.add_reaction_center("comp_a>>y", sig_a)
        m.add_reaction_center("comp_b>>y", sig_b)
        m.add_reaction_center(
            "multi>>y",
            sig_multi,
            is_multi_component=True,
            components=["comp_a>>y", "comp_b>>y"],
        )
        for rs in ("r1>>q", "r2>>q", "r3>>q"):
            m.add_reaction(rs, "doc")
            m.add_center_to_reaction("multi>>y", rs, sig_multi, sear)

        assert m.count_center("multi>>y") > CompositionConfig.distributivity_threshold

        composer._run_postprocessing()

        out = m.find_center("multi>>y")
        assert out is not None
        assert out[0] == 1  # AND(sig_a, sig_b): bit shared by both components
        assert out[1] == 0
        assert out[2] == 0
        assert out[4] == 1  # original composite-row bit preserved (OR with AND)


def _write_stamp_csv(path: Path) -> None:
    """Write a CSV using the composer's default column names."""
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["cleaned_rxn", "document_id"])
        writer.writerow(["A>>B", "doc1"])


class TestComposeStampsDatabase:
    def test_compose_writes_build_stamp(
        self, composer, mock_processor, mock_extractor, tmp_path: Path
    ):
        csv_path = tmp_path / "in.csv"
        out_path = tmp_path / "out.sqlite"
        _write_stamp_csv(csv_path)
        mock_processor.process_batch.return_value = []
        mock_extractor.extract_rc_for_batch.side_effect = lambda batch: []

        composer.compose(csv_path, out_path, db_version="U9-TEST")

        metadata = DBManager.read_metadata(out_path)
        assert metadata["db_version"] == "U9-TEST"
        assert metadata["built_at"]
        assert metadata["chemcensor_version"]

    def test_compose_requires_a_version_label(
        self, composer, mock_processor, mock_extractor, tmp_path: Path
    ):
        csv_path = tmp_path / "in.csv"
        _write_stamp_csv(csv_path)
        mock_processor.process_batch.return_value = []
        mock_extractor.extract_rc_for_batch.side_effect = lambda batch: []

        with pytest.raises(InvalidDBVersionError, match="db_version"):
            composer.compose(csv_path, tmp_path / "out.sqlite", db_version="")
