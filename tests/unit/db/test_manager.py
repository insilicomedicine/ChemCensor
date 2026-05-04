import json
import tempfile
from pathlib import Path

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
