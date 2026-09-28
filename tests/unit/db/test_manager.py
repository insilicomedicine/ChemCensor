import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import numpy as np
from pytest import fixture
from pytest import raises

from chemcensor.db.errors import DBManagerFileNotFoundError
from chemcensor.db.manager import DBManager
from chemcensor.rules.functional_groups import FG_COLLECTION_SEAR

FG_A = np.array([1, 0, 0, 0, 0], dtype=np.uint8)
FG_B = np.array([0, 0, 1, 0, 1], dtype=np.uint8)
FG_C = np.array([0, 1, 0, 0, 0], dtype=np.uint8)
SEAR_ZERO = np.zeros(FG_COLLECTION_SEAR.num_groups, dtype=np.uint8)


@fixture
def db() -> DBManager:
    return DBManager()


class TestAddReactionCenter:
    def test_add_single(self, db: DBManager):
        db.add_reaction_center("C>>CC", FG_A)
        assert db.find_center("C>>CC") is not None

    def test_add_stores_fg_signature(self, db: DBManager):
        db.add_reaction_center("cOC>>cO", FG_B)
        result = db.find_center("cOC>>cO")
        assert result is not None
        assert np.array_equal(result, FG_B)

    def test_add_different_smiles(self, db: DBManager):
        db.add_reaction_center("cOC>>cO", FG_A)
        db.add_reaction_center("cN>>c", FG_C)
        assert db.find_center("cOC>>cO") is not None
        assert db.find_center("cN>>c") is not None

    def test_add_multi_component(self, db: DBManager):
        components = ["C>>CC", "N>>NN"]
        db.add_reaction_center(
            "C.N>>CC.NN", FG_A, is_multi_component=True, components=components
        )
        row = db._conn.execute(
            "SELECT is_multi_component, components"
            " FROM reaction_centers WHERE reaction_center_smiles = ?",
            ("C.N>>CC.NN",),
        ).fetchone()
        assert row is not None
        assert row[0] == 1
        assert json.loads(row[1]) == components


class TestAddReaction:
    def test_add_single(self, db: DBManager):
        db.add_reaction("CC(O)C.Br>>CC(Br)C")
        assert db.find_reaction("CC(O)C.Br>>CC(Br)C") is not None

    def test_add_stores_document_id(self, db: DBManager):
        db.add_reaction("CC(O)C.Br>>CC(Br)C", "document_id")
        result = db.find_reaction("CC(O)C.Br>>CC(Br)C")
        assert result is not None
        assert "document_id" in result

    def test_find_reaction_precedents_returns_document_metadata(self, db: DBManager):
        reaction = "CC(O)C.Br>>CC(Br)C"
        for index in range(5):
            db.add_reaction(
                reaction,
                f"doc-{index}",
                is_virtual=True,
                source=f"source-{index}",
            )

        precedents = db.find_reaction_precedents(
            reaction,
            is_virtual=True,
            limit=3,
        )

        assert len(precedents) == 3
        assert precedents[0] == (reaction, "doc-0", "source-0", True)
        assert db.find_reaction_precedents(reaction, limit=0) == []


class TestFind:
    def test_find_empty_db(self, db: DBManager):
        assert db.find_center("C>>CC") is None

    def test_find_existing(self, db: DBManager):
        db.add_reaction_center("cOC>>cO", FG_B)
        result = db.find_center("cOC>>cO")
        assert result is not None
        assert np.array_equal(result, FG_B)

    def test_find_smiles_mismatch(self, db: DBManager):
        db.add_reaction_center("cOC>>cO", FG_A)
        assert db.find_center("cN>>c") is None


class TestCountCenter:
    def test_count_no_links(self, db: DBManager):
        db.add_reaction_center("C>>CC", FG_A)
        assert db.count_center("C>>CC") == 0

    def test_count_multiple_links(self, db: DBManager):
        db.add_reaction_center("C>>CC", FG_A)
        db.add_reaction("R1>>P1")
        db.add_reaction("R2>>P2")
        db.add_center_to_reaction("C>>CC", "R1>>P1", FG_B, SEAR_ZERO)
        db.add_center_to_reaction("C>>CC", "R2>>P2", FG_C, SEAR_ZERO)
        assert db.count_center("C>>CC") == 2


class TestFindCenterPrecedents:
    def test_separates_virtuality_and_respects_limit(self, db: DBManager):
        center = "C>>CC"
        db.add_reaction_center(center, FG_A, is_virtual=False)
        db.add_reaction_center(center, FG_B, is_virtual=True)
        for is_virtual in (False, True):
            for index in range(5):
                reaction = f"R{index}{int(is_virtual)}>>P{index}"
                source = f"source-{index}" if is_virtual else ""
                db.add_reaction(
                    reaction,
                    f"doc-{index}",
                    is_virtual=is_virtual,
                    source=source,
                )
                db.add_center_to_reaction(
                    center,
                    reaction,
                    FG_A,
                    SEAR_ZERO,
                    is_virtual=is_virtual,
                )

        real = db.find_center_precedents(center, is_virtual=False, limit=3)
        virtual = db.find_center_precedents(center, is_virtual=True, limit=3)

        assert len(real) == 3
        assert len(virtual) == 3
        assert all(not row[3] for row in real)
        assert all(row[3] for row in virtual)
        assert all(row[2] == "" for row in real)
        assert all(row[2].startswith("source-") for row in virtual)
        assert db.find_center_precedents(center, limit=0) == []

    def test_limits_distinct_reactions_and_selects_first_document(self, db: DBManager):
        center = "C>>CC"
        db.add_reaction_center(center, FG_A)
        for reaction_index in range(4):
            reaction = f"R{reaction_index}>>P{reaction_index}"
            for document_index in range(3):
                db.add_reaction(
                    reaction,
                    f"doc-{document_index}",
                    source=f"source-{document_index}",
                )
            db.add_center_to_reaction(center, reaction, FG_A, SEAR_ZERO)

        queries = (
            db.find_center_precedents(center, limit=3),
            db.find_center_precedents(
                center,
                limit=3,
                sear_signature=SEAR_ZERO,
            ),
            db.find_center_fg_precedents(center, 0, limit=3),
            db.find_center_fg_precedents(
                center,
                0,
                limit=3,
                sear_signature=SEAR_ZERO,
            ),
        )

        for precedents in queries:
            assert len(precedents) == 3
            assert len({row[0] for row in precedents}) == 3
            assert all(row[1:3] == ("doc-0", "source-0") for row in precedents)

    def test_fg_precedents_require_bridge_bit_and_remain_separate(self, db: DBManager):
        center = "C>>CC"
        db.add_reaction_center(center, FG_A, is_virtual=False)
        db.add_reaction_center(center, FG_A, is_virtual=True)
        for is_virtual in (False, True):
            for index in range(5):
                reaction = f"FG{index}{int(is_virtual)}>>P{index}"
                signature = (
                    np.array([1, 0, 0, 0, 0], dtype=np.uint8)
                    if index % 2 == 0
                    else np.array([0, 1, 0, 0, 0], dtype=np.uint8)
                )
                db.add_reaction(
                    reaction,
                    f"doc-{index}",
                    is_virtual=is_virtual,
                    source="virtual-source" if is_virtual else "",
                )
                db.add_center_to_reaction(
                    center,
                    reaction,
                    signature,
                    SEAR_ZERO,
                    is_virtual=is_virtual,
                )

        real_fg_0 = db.find_center_fg_precedents(
            center,
            0,
            is_virtual=False,
            limit=3,
        )
        virtual_fg_0 = db.find_center_fg_precedents(
            center,
            0,
            is_virtual=True,
            limit=3,
        )
        real_fg_1 = db.find_center_fg_precedents(center, 1, is_virtual=False)

        assert len(real_fg_0) == 3
        assert len(virtual_fg_0) == 3
        assert all(not row[3] and "FG" in row[0] for row in real_fg_0)
        assert all(row[3] and row[2] == "virtual-source" for row in virtual_fg_0)
        assert len(real_fg_1) == 2
        assert db.find_center_fg_precedents(center, -1) == []

    def test_filters_sear_precedents_and_count_by_context(self, db: DBManager):
        center = "C>>CC"
        other_sear = SEAR_ZERO.copy()
        other_sear[0] = 1
        db.add_reaction_center(center, FG_A)
        for reaction, sear_signature in (
            ("matching>>reaction", SEAR_ZERO),
            ("other>>reaction", other_sear),
        ):
            db.add_reaction(reaction, f"doc-{reaction}")
            db.add_center_to_reaction(
                center,
                reaction,
                FG_A,
                sear_signature,
            )

        rows = db.find_center_precedents(
            center,
            sear_signature=SEAR_ZERO,
        )

        assert rows == [("matching>>reaction", "doc-matching>>reaction", "", False)]
        assert db.count_center(center, sear_signature=SEAR_ZERO) == 1
        assert db.find_center_fg_precedents(
            center,
            0,
            sear_signature=SEAR_ZERO,
        ) == [("matching>>reaction", "doc-matching>>reaction", "", False)]
        assert (
            db.find_center_fg_precedents(
                center,
                1,
                sear_signature=SEAR_ZERO,
            )
            == []
        )


class TestUpdate:
    def test_update_fg_signature(self, db: DBManager):
        db.add_reaction_center("cOC>>cO", FG_C)
        result = db.find_center("cOC>>cO")
        assert result is not None
        assert np.array_equal(result, FG_C)

        db.update("cOC>>cO", FG_B)

        result = db.find_center("cOC>>cO")
        assert result is not None
        assert np.array_equal(result, FG_B)


class TestDumpLoad:
    def test_round_trip(self, db: DBManager):
        db.add_reaction_center("cOC>>cO", FG_A)
        db.add_reaction_center("cN>>c", FG_B)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.db"
            db.dump(path)
            assert path.exists()

            db2 = DBManager.load(path)

            result = db2.find_center("cOC>>cO")
            assert result is not None
            assert np.array_equal(result, FG_A)

            assert db2.find_center("cN>>c") is not None
            assert db2.find_center("unknown>>x") is None

    def test_load_nonexistent_raises(self):
        with raises(DBManagerFileNotFoundError):
            DBManager.load("/nonexistent/path/db.sqlite")

    def test_dump_creates_parent_dirs(self, db: DBManager):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sub" / "dir" / "test.db"
            db.dump(path)
            assert path.exists()

    def test_dump_overwrites_existing(self, db: DBManager):
        db.add_reaction_center("cOC>>cO", FG_A)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.db"
            db.dump(path)
            db.add_reaction_center("cN>>c", FG_B)
            db.dump(path)

            db2 = DBManager.load(path)
            assert db2.find_center("cOC>>cO") is not None
            assert db2.find_center("cN>>c") is not None


class TestVirtualCenters:
    def test_real_and_virtual_are_independent(self, db: DBManager):
        db.add_reaction_center("C>>CC", FG_A, is_virtual=False)
        db.add_reaction_center("C>>CC", FG_B, is_virtual=True)

        real = db.find_center("C>>CC", is_virtual=False)
        virt = db.find_center("C>>CC", is_virtual=True)
        assert real is not None and np.array_equal(real, FG_A)
        assert virt is not None and np.array_equal(virt, FG_B)

    def test_update_does_not_cross_groups(self, db: DBManager):
        db.add_reaction_center("C>>CC", FG_A, is_virtual=False)
        db.add_reaction_center("C>>CC", FG_B, is_virtual=True)
        db.update("C>>CC", FG_C, is_virtual=False)

        real = db.find_center("C>>CC", is_virtual=False)
        virt = db.find_center("C>>CC", is_virtual=True)
        assert real is not None and np.array_equal(real, FG_C)
        assert virt is not None and np.array_equal(virt, FG_B)

    def test_lookup_center_fg_pair(self, db: DBManager):
        db.add_reaction_center("C>>CC", FG_A, is_virtual=False)
        db.add_reaction_center("C>>CC", FG_B, is_virtual=True)
        real, virt = db.lookup_center_fg_pair("C>>CC")
        assert real is not None and np.array_equal(real, FG_A)
        assert virt is not None and np.array_equal(virt, FG_B)

        alone_real, alone_virt = db.lookup_center_fg_pair("missing>>x")
        assert alone_real is None and alone_virt is None

    def test_virtual_reaction_stores_source(self, db: DBManager):
        db.add_reaction("A>>B", "pat1", is_virtual=True, source="21")
        assert db.find_reaction("A>>B") == ["pat1"]
        row = db._conn.execute(
            "SELECT is_virtual, source FROM reactions WHERE reaction_smiles = ?",
            ("A>>B",),
        ).fetchone()
        assert row == (1, "21")

    def test_find_reaction_matches_virtual_for_exact_match(self, db: DBManager):
        db.add_reaction("virt>>rxn", "doc", is_virtual=True, source="99")
        assert db.find_reaction("virt>>rxn") == ["doc"]

    def test_find_reaction_matches_reports_virtuality(self, db: DBManager):
        assert db.find_reaction_matches("missing>>x") is None

        db.add_reaction("real>>rxn", "d1", is_virtual=False)
        assert db.find_reaction_matches("real>>rxn") == [("d1", False)]

        db.add_reaction("virt>>rxn", "d2", is_virtual=True, source="7")
        assert db.find_reaction_matches("virt>>rxn") == [("d2", True)]

        db.add_reaction("both>>rxn", "d3", is_virtual=False)
        db.add_reaction("both>>rxn", "d3", is_virtual=True, source="8")
        both = db.find_reaction_matches("both>>rxn")
        assert both is not None
        assert sorted(both) == [
            ("d3", False),
            ("d3", True),
        ]

    def test_bridge_scoped_by_virtual(self, db: DBManager):
        db.add_reaction_center("C>>CC", FG_A, is_virtual=False)
        db.add_reaction_center("C>>CC", FG_B, is_virtual=True)
        db.add_reaction("R>>P", "d1", is_virtual=False)
        db.add_center_to_reaction("C>>CC", "R>>P", FG_A, SEAR_ZERO, is_virtual=False)
        assert db.find_center_to_reaction("C>>CC", "R>>P", is_virtual=False)
        assert not db.find_center_to_reaction("C>>CC", "R>>P", is_virtual=True)
        assert db.count_center("C>>CC", is_virtual=False) == 1
        assert db.count_center("C>>CC", is_virtual=True) == 0


class TestMetadata:
    def test_read_metadata_returns_empty_dict_for_unstamped_db(
        self, db: DBManager, tmp_path: Path
    ):
        db_path = tmp_path / "unstamped.sqlite"
        db.dump(db_path)

        assert DBManager.read_metadata(db_path) == {}

    def test_write_metadata_survives_dump_and_read(self, db: DBManager, tmp_path: Path):
        db.write_metadata(
            {
                "db_version": "U3-1",
                "built_at": "2026-08-20T09:14:02Z",
                "chemcensor_version": "1.4.0",
            }
        )
        db_path = tmp_path / "stamped.sqlite"
        db.dump(db_path)

        assert DBManager.read_metadata(db_path) == {
            "db_version": "U3-1",
            "built_at": "2026-08-20T09:14:02Z",
            "chemcensor_version": "1.4.0",
        }

    def test_write_metadata_on_loaded_db_without_metadata_table(self, tmp_path: Path):
        """A legacy unstamped file has no ``metadata`` table; ``load`` then
        ``write_metadata`` must create it rather than raise."""
        import sqlite3
        from contextlib import closing

        legacy_path = tmp_path / "legacy.sqlite"
        with closing(sqlite3.connect(str(legacy_path))) as conn:
            conn.execute("CREATE TABLE reactions (reaction_smiles TEXT)")
            conn.commit()

        manager = DBManager.load(legacy_path)
        manager.write_metadata({"db_version": "U3-1"})

        rows = manager._conn.execute("SELECT key, value FROM metadata").fetchall()
        assert rows == [("db_version", "U3-1")]

    def test_write_metadata_overwrites_existing_key(self, db: DBManager):
        db.write_metadata({"db_version": "U3-1"})
        db.write_metadata({"db_version": "U3-2"})

        rows = db._conn.execute("SELECT key, value FROM metadata").fetchall()
        assert rows == [("db_version", "U3-2")]

    def test_write_metadata_rejects_readonly_manager(
        self, db: DBManager, tmp_path: Path
    ):
        db_path = tmp_path / "readonly.sqlite"
        db.dump(db_path)
        readonly = DBManager.open_readonly(db_path)

        with raises(RuntimeError, match="read-only"):
            readonly.write_metadata({"db_version": "U3-1"})

    def test_add_reaction_rejects_readonly_manager(self, db: DBManager, tmp_path: Path):
        db_path = tmp_path / "readonly.sqlite"
        db.dump(db_path)
        readonly = DBManager.open_readonly(db_path)

        with raises(RuntimeError, match="read-only"):
            readonly.add_reaction("CCO>>CC=O")

    def test_read_metadata_missing_file(self, tmp_path: Path):
        with raises(DBManagerFileNotFoundError):
            DBManager.read_metadata(tmp_path / "nope.sqlite")

    def test_read_metadata_does_not_copy_the_database_into_memory(
        self, db: DBManager, tmp_path: Path
    ):
        """The reference DB is ~6GB; ``load`` would back it up into ``:memory:``."""
        db.write_metadata({"db_version": "U3-1"})
        db_path = tmp_path / "stamped.sqlite"
        db.dump(db_path)

        with patch.object(DBManager, "load", side_effect=AssertionError("used load")):
            assert DBManager.read_metadata(db_path) == {"db_version": "U3-1"}
