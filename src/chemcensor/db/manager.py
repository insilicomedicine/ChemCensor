from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from os import PathLike
from pathlib import Path

import numpy as np

from ..rules.functional_groups import FG_SIGNATURE_LENGTH
from .errors import DBManagerFileNotFoundError

_SCHEMA = """\
CREATE TABLE IF NOT EXISTS reaction_centers (
    reaction_center_smiles TEXT PRIMARY KEY,
    fg_signature           BLOB NOT NULL DEFAULT (x''),
    is_multi_component     INTEGER NOT NULL DEFAULT 0,
    components             TEXT NOT NULL DEFAULT '[]'
);
CREATE TABLE IF NOT EXISTS centers_to_reactions (
    reaction_center_smiles TEXT NOT NULL
        REFERENCES reaction_centers(reaction_center_smiles),
    reaction_smiles TEXT NOT NULL,
    fg_signature    BLOB NOT NULL DEFAULT (x''),
    sear_signature  BLOB NOT NULL DEFAULT (x''),
    PRIMARY KEY (reaction_center_smiles, reaction_smiles)
);
CREATE TABLE IF NOT EXISTS reactions (
    reaction_smiles TEXT NOT NULL,
    document_id     TEXT NOT NULL,
    PRIMARY KEY (reaction_smiles, document_id)
);
CREATE INDEX IF NOT EXISTS idx_ctr_reaction_smiles
    ON centers_to_reactions(reaction_smiles);
"""

_SQL_SELECT_RC = (
    "SELECT fg_signature FROM reaction_centers WHERE reaction_center_smiles = ?"
)
_SQL_INSERT_RC = (
    "INSERT INTO reaction_centers"
    " (reaction_center_smiles, fg_signature, is_multi_component, components)"
    " VALUES (?, ?, ?, ?)"
)
_SQL_UPDATE_RC_FG = (
    "UPDATE reaction_centers SET fg_signature = ? WHERE reaction_center_smiles = ?"
)
_SQL_INSERT_CTR = (
    "INSERT INTO centers_to_reactions"
    " (reaction_center_smiles, reaction_smiles, fg_signature, sear_signature)"
    " VALUES (?, ?, ?, ?)"
)
_SQL_SELECT_CTR = (
    "SELECT 1 FROM centers_to_reactions"
    " WHERE reaction_center_smiles = ? AND reaction_smiles = ?"
)
_SQL_SELECT_FG_SEAR_BY_CENTER = (
    "SELECT fg_signature, sear_signature FROM centers_to_reactions"
    " WHERE reaction_center_smiles = ?"
)
_SQL_COUNT_CTR = (
    "SELECT COUNT(*) FROM centers_to_reactions WHERE reaction_center_smiles = ?"
)
_SQL_SELECT_MULTI_COMPONENT_CENTERS = (
    "SELECT rc.reaction_center_smiles, rc.fg_signature, rc.components "
    "FROM reaction_centers rc WHERE rc.is_multi_component = 1 "
    "AND (SELECT COUNT(*) FROM centers_to_reactions ctr "
    "     WHERE ctr.reaction_center_smiles = rc.reaction_center_smiles) > ?"
)
_SQL_SELECT_REACTION = "SELECT document_id FROM reactions WHERE reaction_smiles = ?"
_SQL_INSERT_REACTION = (
    "INSERT INTO reactions (reaction_smiles, document_id) VALUES (?, ?)"
)


class DBManager:
    """Manages the reaction centers database backed by an in-memory SQLite store.

    The default connection is an in-memory database created via
    :meth:`__init__` or copied from a file via :meth:`load`.  For massively
    parallel read-only access (e.g. the parallel scoring pipeline) prefer
    :meth:`open_readonly`, which attaches an immutable file-backed connection
    so that all worker processes share the same OS page cache and the
    database is not duplicated in RAM.
    """

    def __init__(
        self,
        init_db: bool = True,
    ) -> None:
        """Initialize the database manager.

        :param init_db: Whether to initialise the database with the schema.
        :type init_db: bool
        """
        self._conn: sqlite3.Connection = sqlite3.connect(":memory:")
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._readonly: bool = False

        if init_db:
            self._conn.executescript(_SCHEMA)

    @classmethod
    def load(cls, db_path: str | PathLike) -> DBManager:
        """Load a database from a file.

        :param db_path: The path to the SQLite database file.
        :type db_path: str | PathLike
        :return: The loaded database manager.
        :rtype: DBManager
        """
        manager = cls(init_db=False)
        path = Path(db_path)
        if not path.exists():
            raise DBManagerFileNotFoundError(f"Database file not found: {path}")

        with closing(sqlite3.connect(str(path))) as file_conn:
            file_conn.backup(manager._conn)

        return manager

    @classmethod
    def open_readonly(cls, db_path: str | PathLike) -> DBManager:
        """Open a database file in shared read-only mode (no in-memory copy).

        The connection is opened with ``mode=ro&immutable=1`` so SQLite knows
        the file will not change and skips locking; multiple processes can
        attach to the same file and share its pages via the OS page cache.
        Useful for parallel scoring where the database would otherwise be
        duplicated per worker.

        Write methods raise :class:`RuntimeError` for managers opened this
        way.

        :param db_path: The path to the SQLite database file.
        :type db_path: str | PathLike
        :return: A read-only DBManager backed by the file on disk.
        :rtype: DBManager
        :raises DBManagerFileNotFoundError: If the database file is missing.
        """
        path = Path(db_path)
        if not path.exists():
            raise DBManagerFileNotFoundError(f"Database file not found: {path}")

        # Bypass the default :memory: connection to avoid wasting RAM.
        manager = cls.__new__(cls)
        manager._conn = sqlite3.connect(
            f"file:{path}?mode=ro&immutable=1",
            uri=True,
            check_same_thread=False,
        )
        manager._readonly = True
        return manager

    def _ensure_writable(self) -> None:
        """Raise if this manager was opened in read-only mode.

        :raises RuntimeError: If the manager is read-only.
        """
        if self._readonly:
            raise RuntimeError(
                "DBManager is opened in read-only mode; "
                "write operations are not allowed."
            )

    def dump(self, db_path: str | PathLike) -> None:
        """Write the in-memory database to an SQLite file on disk.

        If the target file already exists it is overwritten.

        :param db_path: Destination path for the SQLite database.
        :type db_path: str | PathLike
        """
        self._ensure_writable()
        path = Path(db_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            path.unlink()

        with closing(sqlite3.connect(str(path))) as file_conn:
            self._conn.backup(file_conn)

    def find_center(self, reaction_center_smiles: str) -> np.ndarray | None:
        """Return the FG-signature of the reaction center from the database.

        :param reaction_center_smiles: the reaction center smiles to search for.
        :type reaction_center_smiles: str
        :return: The FG-signature of the reaction center from the database.
            The returned object is read-only.
        :rtype: np.ndarray | None
        """
        row = self._conn.execute(
            _SQL_SELECT_RC,
            (reaction_center_smiles,),
        ).fetchone()
        if row is None:
            return None
        return np.frombuffer(row[0], dtype=np.uint8)

    def update(self, reaction_center_smiles: str, fg_signature: np.ndarray) -> None:
        """Update a reaction center in the database. It's needed
        when ReactionCenrerDBComposer finds the existing reaction center
        in the database and needs to update the reaction center's FG-signature.

        :param reaction_center_smiles: The reaction center smiles to update.
        :type reaction_center_smiles: str
        :param fg_signature: The FG-signature of the reaction center.
        :type fg_signature: np.ndarray
        """
        self._ensure_writable()
        self._conn.execute(
            _SQL_UPDATE_RC_FG,
            (fg_signature.astype(np.uint8).tobytes(), reaction_center_smiles),
        )
        self._conn.commit()

    def add_reaction_center(
        self,
        reaction_center_smiles: str,
        fg_signature: np.ndarray,
        is_multi_component: bool = False,
        components: list[str] | None = None,
    ) -> None:
        """Insert a reaction center into the database.

        :param reaction_center_smiles: The reaction center smiles to add.
        :type reaction_center_smiles: str
        :param fg_signature: The FG-signature of the reaction center.
        :type fg_signature: np.ndarray
        :param is_multi_component: Whether the center has multiple components.
        :type is_multi_component: bool
        :param components: SMILES of individual components (for multi-component
            centers).
        :type components: list[str] | None
        """
        self._ensure_writable()
        self._conn.execute(
            _SQL_INSERT_RC,
            (
                reaction_center_smiles,
                fg_signature.astype(np.uint8).tobytes(),
                int(is_multi_component),
                json.dumps(components or []),
            ),
        )
        self._conn.commit()

    def add_center_to_reaction(
        self,
        reaction_center_smiles: str,
        reaction_smiles: str,
        fg_signature: np.ndarray,
        sear_signature: np.ndarray,
    ) -> None:
        """Link a reaction center to a reaction in the bridge table.

        :param reaction_center_smiles: The reaction center SMILES.
        :type reaction_center_smiles: str
        :param reaction_smiles: The reaction SMILES.
        :type reaction_smiles: str
        :param fg_signature: The FG-signature for this specific
            center-reaction pair.
        :type fg_signature: np.ndarray
        :param sear_signature: SEAr context signature for this pair.
        :type sear_signature: np.ndarray
        """
        self._ensure_writable()
        self._conn.execute(
            _SQL_INSERT_CTR,
            (
                reaction_center_smiles,
                reaction_smiles,
                fg_signature.astype(np.uint8).tobytes(),
                sear_signature.astype(np.uint8).tobytes(),
            ),
        )
        self._conn.commit()

    def find_center_to_reaction(
        self, reaction_center_smiles: str, reaction_smiles: str
    ) -> bool:
        """Check whether a (center, reaction) pair exists in the bridge table.

        :param reaction_center_smiles: The reaction center SMILES.
        :type reaction_center_smiles: str
        :param reaction_smiles: The reaction SMILES.
        :type reaction_smiles: str
        :return: ``True`` if the pair already exists, ``False`` otherwise.
        :rtype: bool
        """
        row = self._conn.execute(
            _SQL_SELECT_CTR,
            (reaction_center_smiles, reaction_smiles),
        ).fetchone()
        return row is not None

    def has_center_sear_in_bridge(
        self,
        reaction_center_smiles: str,
        sear_signature: np.ndarray,
    ) -> bool:
        """Return whether any bridge row exists for this center and SEAr signature.

        Rows are loaded by reaction center only; ``sear_signature`` is compared
        in Python so SQLite does not need a BLOB index on ``sear_signature``.

        :param reaction_center_smiles: The reaction center SMILES.
        :type reaction_center_smiles: str
        :param sear_signature: SEAr signature to match.
        :type sear_signature: np.ndarray
        :rtype: bool
        """
        sear_bytes = sear_signature.astype(np.uint8).tobytes()
        rows = self._conn.execute(
            _SQL_SELECT_FG_SEAR_BY_CENTER,
            (reaction_center_smiles,),
        ).fetchall()
        return any(sear_blob == sear_bytes for _, sear_blob in rows)

    def aggregate_fg_signature_for_center_sear(
        self,
        reaction_center_smiles: str,
        sear_signature: np.ndarray,
    ) -> np.ndarray:
        """Bitwise-OR of ``fg_signature`` over bridge rows for center + SEAr context.

        Rows are loaded by reaction center only; ``sear_signature`` is matched
        in Python (see :meth:`has_center_sear_in_bridge`).

        :param reaction_center_smiles: The reaction center SMILES.
        :type reaction_center_smiles: str
        :param sear_signature: SEAr signature to filter rows.
        :type sear_signature: np.ndarray
        :return: Combined signature.
        :rtype: np.ndarray
        """
        sear_bytes = sear_signature.astype(np.uint8).tobytes()
        rows = self._conn.execute(
            _SQL_SELECT_FG_SEAR_BY_CENTER,
            (reaction_center_smiles,),
        ).fetchall()
        combined = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
        for fg_blob, sear_blob in rows:
            if sear_blob != sear_bytes:
                continue
            combined = np.bitwise_or(combined, np.frombuffer(fg_blob, dtype=np.uint8))
        return combined

    def count_center(self, reaction_center_smiles: str) -> int:
        """Return the number of reactions linked to a center.

        :param reaction_center_smiles: The reaction center SMILES.
        :type reaction_center_smiles: str
        :return: Number of rows in ``centers_to_reactions`` for this center.
        :rtype: int
        """
        row = self._conn.execute(
            _SQL_COUNT_CTR,
            (reaction_center_smiles,),
        ).fetchone()
        return row[0]

    def list_multi_component_for_dist(
        self, reaction_count: int
    ) -> list[tuple[str, np.ndarray, list[str]]]:
        """Return multi-component centers with more than specified number of
        rows in ``centers_to_reactions`` for distributivity.

        :param reaction_count: The reaction count threshold for distributivity
        :type reaction_count: int
        :return: List of tuples of (composite center SMILES, FG-signature,
            component list).
        """
        rows = self._conn.execute(
            _SQL_SELECT_MULTI_COMPONENT_CENTERS,
            (reaction_count,),
        ).fetchall()
        return [
            (smiles, np.frombuffer(fg_signature, dtype=np.uint8), json.loads(comps))
            for smiles, fg_signature, comps in rows
        ]

    def find_reaction(self, reaction_smiles: str) -> list[str] | None:
        """Return the document IDs for a reaction, or None if not found.

        :param reaction_smiles: The reaction SMILES to search for.
        :type reaction_smiles: str
        :return: The document IDs associated with the reaction, or None.
        :rtype: list[str] | None
        """
        row = self._conn.execute(
            _SQL_SELECT_REACTION,
            (reaction_smiles,),
        ).fetchall()
        if not row:
            return None
        return [tupl[0] for tupl in row]

    def add_reaction(self, reaction_smiles: str, document_id: str = "") -> None:
        """Insert a reaction into the database.

        :param reaction_smiles: The reaction SMILES to add.
        :type reaction_smiles: str
        :param document_id: The document ID where the reaction originates.
        :type document_id: str
        """
        self._ensure_writable()
        self._conn.execute(
            _SQL_INSERT_REACTION,
            (reaction_smiles, document_id),
        )
        self._conn.commit()

    def __enter__(self) -> DBManager:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._conn.close()
