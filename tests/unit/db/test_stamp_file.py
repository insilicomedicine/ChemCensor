from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

from chemcensor.db.errors import DatabaseAlreadyStampedError
from chemcensor.db.errors import DBManagerFileNotFoundError
from chemcensor.db.errors import InvalidDBVersionError
from chemcensor.db.manager import DBManager
from chemcensor.db.stamp import stamp_database_file
from chemcensor.rules.functional_groups import FG_SIGNATURE_LENGTH

FG_A = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)


@pytest.fixture
def unstamped_db(tmp_path: Path) -> Path:
    """An on-disk database with data but no build stamp."""
    db = DBManager()
    db.add_reaction_center("C>>CC", FG_A)
    db.add_reaction("R>>P", "doc1")
    db_path = tmp_path / "unstamped.sqlite"
    db.dump(db_path)
    return db_path


_COUNT_QUERIES = (
    "SELECT COUNT(*) FROM reaction_centers",
    "SELECT COUNT(*) FROM centers_to_reactions",
    "SELECT COUNT(*) FROM reactions",
)


def _data_snapshot(db_path: Path) -> tuple:
    manager = DBManager.open_readonly(db_path)
    counts = tuple(
        manager._conn.execute(query).fetchone()[0] for query in _COUNT_QUERIES
    )
    manager._conn.close()
    return counts


class TestStampDatabaseFile:
    def test_stamps_an_existing_database_in_place(self, unstamped_db: Path):
        assert DBManager.read_metadata(unstamped_db) == {}

        stamp_database_file(unstamped_db, "U3-1")

        metadata = DBManager.read_metadata(unstamped_db)
        assert metadata["db_version"] == "U3-1"
        assert metadata["built_at"]
        assert metadata["chemcensor_version"]

    def test_returns_the_written_stamp(self, unstamped_db: Path):
        stamp = stamp_database_file(unstamped_db, "U3-1")

        assert stamp == DBManager.read_metadata(unstamped_db)

    def test_leaves_the_data_tables_untouched(self, unstamped_db: Path):
        before = _data_snapshot(unstamped_db)

        stamp_database_file(unstamped_db, "U3-1")

        assert _data_snapshot(unstamped_db) == before

    def test_restamping_the_same_version_is_an_idempotent_no_op(
        self, unstamped_db: Path
    ):
        first = stamp_database_file(
            unstamped_db, "U3-1", built_at="2026-01-01T00:00:00Z"
        )

        # A second stamp of the same label must not rewrite built_at /
        # chemcensor_version, even from a newer install.
        second = stamp_database_file(unstamped_db, "U3-1")

        assert second == first
        assert DBManager.read_metadata(unstamped_db) == first

    def test_force_refreshes_the_same_version(self, unstamped_db: Path):
        stamp_database_file(unstamped_db, "U3-1", built_at="2026-01-01T00:00:00Z")

        refreshed = stamp_database_file(
            unstamped_db, "U3-1", built_at="2026-02-02T00:00:00Z", force=True
        )

        assert refreshed["built_at"] == "2026-02-02T00:00:00Z"
        assert DBManager.read_metadata(unstamped_db) == refreshed

    def test_refuses_to_change_the_version_without_force(self, unstamped_db: Path):
        stamp_database_file(unstamped_db, "U3-1")

        with pytest.raises(DatabaseAlreadyStampedError, match="already stamped"):
            stamp_database_file(unstamped_db, "U3-2")

        assert DBManager.read_metadata(unstamped_db)["db_version"] == "U3-1"

    def test_force_overwrites_a_different_version(self, unstamped_db: Path):
        stamp_database_file(unstamped_db, "U3-1")

        stamp_database_file(unstamped_db, "U3-2", force=True)

        assert DBManager.read_metadata(unstamped_db)["db_version"] == "U3-2"

    def test_built_at_can_be_supplied(self, unstamped_db: Path):
        stamp_database_file(unstamped_db, "U3-1", built_at="2026-08-20T09:14:02Z")

        assert (
            DBManager.read_metadata(unstamped_db)["built_at"] == "2026-08-20T09:14:02Z"
        )

    def test_rejects_a_blank_version_label(self, unstamped_db: Path):
        with pytest.raises(InvalidDBVersionError, match="db_version"):
            stamp_database_file(unstamped_db, "  ")

    def test_missing_file(self, tmp_path: Path):
        with pytest.raises(DBManagerFileNotFoundError):
            stamp_database_file(tmp_path / "nope.sqlite", "U3-1")

    def test_does_not_copy_the_database_into_memory(self, unstamped_db: Path):
        """The reference DB is ~6GB; ``load``/``dump`` would rewrite the whole file."""
        with patch.object(DBManager, "load", side_effect=AssertionError("used load")):
            with patch.object(
                DBManager, "dump", side_effect=AssertionError("used dump")
            ):
                stamp_database_file(unstamped_db, "U3-1")

        assert DBManager.read_metadata(unstamped_db)["db_version"] == "U3-1"
