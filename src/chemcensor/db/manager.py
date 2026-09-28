from __future__ import annotations

import json
import sqlite3
from collections.abc import Mapping
from contextlib import closing
from os import PathLike
from pathlib import Path

import numpy as np

from ..rules.functional_groups import FG_SIGNATURE_LENGTH
from .errors import DBManagerFileNotFoundError

_SCHEMA = """\
CREATE TABLE IF NOT EXISTS reaction_centers (
    reaction_center_smiles TEXT NOT NULL,
    is_virtual             INTEGER NOT NULL DEFAULT 0,
    fg_signature           BLOB NOT NULL DEFAULT (x''),
    is_multi_component     INTEGER NOT NULL DEFAULT 0,
    components             TEXT NOT NULL DEFAULT '[]',
    PRIMARY KEY (reaction_center_smiles, is_virtual)
);
CREATE TABLE IF NOT EXISTS centers_to_reactions (
    reaction_center_smiles TEXT NOT NULL,
    is_virtual             INTEGER NOT NULL DEFAULT 0,
    reaction_smiles        TEXT NOT NULL,
    fg_signature           BLOB NOT NULL DEFAULT (x''),
    sear_signature         BLOB NOT NULL DEFAULT (x''),
    PRIMARY KEY (reaction_center_smiles, is_virtual, reaction_smiles),
    FOREIGN KEY (reaction_center_smiles, is_virtual)
        REFERENCES reaction_centers(reaction_center_smiles, is_virtual)
);
CREATE TABLE IF NOT EXISTS reactions (
    reaction_smiles TEXT NOT NULL,
    document_id     TEXT NOT NULL,
    is_virtual      INTEGER NOT NULL DEFAULT 0,
    source          TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (reaction_smiles, document_id, is_virtual)
);
CREATE TABLE IF NOT EXISTS metadata (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_ctr_reaction_smiles
    ON centers_to_reactions(reaction_smiles);
"""

_SQL_SELECT_RC = (
    "SELECT fg_signature FROM reaction_centers"
    " WHERE reaction_center_smiles = ? AND is_virtual = ?"
)
_SQL_INSERT_RC = (
    "INSERT INTO reaction_centers"
    " (reaction_center_smiles, is_virtual, fg_signature,"
    "  is_multi_component, components)"
    " VALUES (?, ?, ?, ?, ?)"
)
_SQL_UPDATE_RC_FG = (
    "UPDATE reaction_centers SET fg_signature = ?"
    " WHERE reaction_center_smiles = ? AND is_virtual = ?"
)
_SQL_INSERT_CTR = (
    "INSERT INTO centers_to_reactions"
    " (reaction_center_smiles, is_virtual, reaction_smiles,"
    "  fg_signature, sear_signature)"
    " VALUES (?, ?, ?, ?, ?)"
)
_SQL_SELECT_CTR = (
    "SELECT 1 FROM centers_to_reactions"
    " WHERE reaction_center_smiles = ? AND is_virtual = ?"
    " AND reaction_smiles = ?"
)
_SQL_SELECT_FG_SEAR_BY_CENTER = (
    "SELECT fg_signature, sear_signature FROM centers_to_reactions"
    " WHERE reaction_center_smiles = ? AND is_virtual = ?"
)
_SQL_COUNT_CTR = (
    "SELECT COUNT(*) FROM centers_to_reactions"
    " WHERE reaction_center_smiles = ? AND is_virtual = ?"
)
_SQL_COUNT_CTR_SEAR = (
    "SELECT COUNT(*) FROM centers_to_reactions"
    " WHERE reaction_center_smiles = ? AND is_virtual = ? AND sear_signature = ?"
)
_SQL_CENTER_PRECEDENTS_PREFIX = (
    "WITH precedent_reactions AS MATERIALIZED ("
    " SELECT ctr.reaction_smiles, ctr.is_virtual"
    " FROM centers_to_reactions AS ctr"
    " WHERE ctr.reaction_center_smiles = ? AND ctr.is_virtual = ?"
)
_SQL_CENTER_PRECEDENTS_SUFFIX = (
    " ORDER BY ctr.reaction_smiles LIMIT ?"
    ")"
    " SELECT precedent.reaction_smiles, r.document_id, r.source, r.is_virtual"
    " FROM precedent_reactions AS precedent"
    " JOIN reactions AS r"
    " ON r.reaction_smiles = precedent.reaction_smiles"
    " AND r.is_virtual = precedent.is_virtual"
    " AND r.document_id = ("
    "  SELECT MIN(first_document.document_id)"
    "  FROM reactions AS first_document"
    "  WHERE first_document.reaction_smiles = precedent.reaction_smiles"
    "  AND first_document.is_virtual = precedent.is_virtual"
    " )"
    " ORDER BY precedent.reaction_smiles, r.document_id, r.source"
)
_SQL_SELECT_CENTER_PRECEDENTS = (
    _SQL_CENTER_PRECEDENTS_PREFIX + _SQL_CENTER_PRECEDENTS_SUFFIX
)
_SQL_SELECT_CENTER_SEAR_PRECEDENTS = (
    _SQL_CENTER_PRECEDENTS_PREFIX
    + " AND ctr.sear_signature = ?"
    + _SQL_CENTER_PRECEDENTS_SUFFIX
)
_SQL_SELECT_CENTER_FG_PRECEDENTS = (
    _SQL_CENTER_PRECEDENTS_PREFIX
    + " AND hex(substr(ctr.fg_signature, ?, 1)) = '01'"
    + _SQL_CENTER_PRECEDENTS_SUFFIX
)
_SQL_SELECT_CENTER_SEAR_FG_PRECEDENTS = (
    _SQL_CENTER_PRECEDENTS_PREFIX + " AND ctr.sear_signature = ?"
    " AND hex(substr(ctr.fg_signature, ?, 1)) = '01'" + _SQL_CENTER_PRECEDENTS_SUFFIX
)
_SQL_SELECT_MULTI_COMPONENT_CENTERS = (
    "SELECT rc.reaction_center_smiles, rc.is_virtual, rc.fg_signature,"
    " rc.components "
    "FROM reaction_centers rc WHERE rc.is_multi_component = 1 "
    "AND (SELECT COUNT(*) FROM centers_to_reactions ctr "
    "     WHERE ctr.reaction_center_smiles = rc.reaction_center_smiles"
    "       AND ctr.is_virtual = rc.is_virtual) > ?"
)
_SQL_SELECT_REACTION_WITH_VIRTUALITY = (
    "SELECT document_id, is_virtual FROM reactions WHERE reaction_smiles = ?"
)
_SQL_SELECT_REACTION_DOCS = (
    "SELECT document_id FROM reactions" " WHERE reaction_smiles = ? AND is_virtual = ?"
)
_SQL_SELECT_REACTION_PRECEDENTS = (
    "SELECT reaction_smiles, document_id, source, is_virtual "
    "FROM reactions WHERE reaction_smiles = ? AND is_virtual = ? "
    "ORDER BY document_id, source LIMIT ?"
)
_SQL_INSERT_REACTION = (
    "INSERT INTO reactions"
    " (reaction_smiles, document_id, is_virtual, source)"
    " VALUES (?, ?, ?, ?)"
)
_SQL_UPSERT_METADATA = "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)"
_SQL_CREATE_METADATA = (
    "CREATE TABLE IF NOT EXISTS metadata ("
    " key   TEXT PRIMARY KEY,"
    " value TEXT NOT NULL"
    ")"
)
_SQL_SELECT_METADATA = "SELECT key, value FROM metadata"


def _write_metadata_rows(conn: sqlite3.Connection, values: Mapping[str, str]) -> None:
    """Create the metadata table if needed and upsert *values* into it.

    Shared by the in-memory (:meth:`DBManager.write_metadata`) and file-level
    (:meth:`DBManager.stamp_file`) write paths so both stamp identically.

    :param conn: An open SQLite connection to write into.
    :type conn: sqlite3.Connection
    :param values: Key/value pairs to store.
    :type values: Mapping[str, str]
    """
    conn.execute(_SQL_CREATE_METADATA)
    conn.executemany(
        _SQL_UPSERT_METADATA,
        [(key, str(value)) for key, value in values.items()],
    )


def _readonly_database_uri(path: Path) -> str:
    """Return an escaped absolute SQLite URI for an immutable database."""
    return f"{path.resolve().as_uri()}?mode=ro&immutable=1"


class DBManager:
    """Manages the reaction centers database backed by an in-memory SQLite store.

    The default connection is an in-memory database created via
    :meth:`__init__` or copied from a file via :meth:`load`.  For massively
    parallel read-only access (e.g. the parallel scoring pipeline) prefer
    :meth:`open_readonly`, which attaches an immutable file-backed connection
    so that all worker processes share the same OS page cache and the
    database is not duplicated in RAM.

    Connections may be created in one thread and used sequentially in another,
    which supports dispatching blocking scoring calls to a worker thread.
    Concurrent calls sharing one manager are not supported; callers must
    serialize them with a lock or semaphore. Read-only managers remain
    immutable regardless of which thread uses them.
    """

    def __init__(
        self,
        init_db: bool = True,
    ) -> None:
        """Initialize the database manager.

        :param init_db: Whether to initialise the database with the schema.
        :type init_db: bool
        """
        self._conn: sqlite3.Connection = sqlite3.connect(
            ":memory:",
            check_same_thread=False,
        )
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._readonly: bool = False

        if init_db:
            self._conn.executescript(_SCHEMA)

    @classmethod
    def load(cls, db_path: str | PathLike) -> DBManager:
        """Load a database from a file into a thread-transferable connection.

        The returned manager may be created in one thread and used
        sequentially in another. Concurrent access to the same manager must be
        serialized by the caller.

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

        The returned manager may be created in one thread and used
        sequentially in another. Concurrent access to the same manager must be
        serialized by the caller.

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
            _readonly_database_uri(path),
            uri=True,
            check_same_thread=False,
        )
        manager._readonly = True
        return manager

    @classmethod
    def read_metadata(cls, db_path: str | PathLike) -> dict[str, str]:
        """Read the build stamp from a database file without loading it into RAM.

        :param db_path: The path to the SQLite database file.
        :type db_path: str | PathLike
        :return: The stored key/value pairs, empty for databases built before
            stamping was introduced.
        :rtype: dict[str, str]
        :raises DBManagerFileNotFoundError: If the database file is missing.
        """
        path = Path(db_path)
        if not path.exists():
            raise DBManagerFileNotFoundError(f"Database file not found: {path}")

        with closing(sqlite3.connect(_readonly_database_uri(path), uri=True)) as conn:
            try:
                rows = conn.execute(_SQL_SELECT_METADATA).fetchall()
            except sqlite3.OperationalError as exc:
                if "no such table" not in str(exc).lower():
                    raise
                # No metadata table: the database predates build stamping.
                return {}

        return {key: value for key, value in rows}

    @classmethod
    def stamp_file(cls, db_path: str | PathLike, values: Mapping[str, str]) -> None:
        """Write metadata into an existing database file, in place.

        :param db_path: The path to the SQLite database file.
        :type db_path: str | PathLike
        :param values: Key/value pairs to store.
        :type values: Mapping[str, str]
        :raises DBManagerFileNotFoundError: If the database file is missing.
        """
        path = Path(db_path)
        if not path.exists():
            raise DBManagerFileNotFoundError(f"Database file not found: {path}")

        with closing(sqlite3.connect(str(path))) as conn:
            with conn:
                _write_metadata_rows(conn, values)

    def _ensure_writable(self) -> None:
        """Raise if this manager was opened in read-only mode.

        :raises RuntimeError: If the manager is read-only.
        """
        if self._readonly:
            raise RuntimeError(
                "DBManager is opened in read-only mode; "
                "write operations are not allowed."
            )

    def write_metadata(self, values: Mapping[str, str]) -> None:
        """Store build-stamp key/value pairs in the database.

        Note: Existing keys are replaced.

        :param values: Key/value pairs to store, e.g. ``db_version``,
            ``built_at``, ``chemcensor_version``.
        :type values: Mapping[str, str]
        """
        self._ensure_writable()
        with self._conn:
            _write_metadata_rows(self._conn, values)

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

    def find_center(
        self,
        reaction_center_smiles: str,
        *,
        is_virtual: bool = False,
    ) -> np.ndarray | None:
        """Return the FG-signature of the reaction center from the database.

        :param reaction_center_smiles: the reaction center smiles to search for.
        :type reaction_center_smiles: str
        :param is_virtual: Whether to look up the virtual (``True``) or real
            (``False``) row for this center.
        :type is_virtual: bool
        :return: The FG-signature of the reaction center from the database.
            The returned object is read-only.
        :rtype: np.ndarray | None
        """
        row = self._conn.execute(
            _SQL_SELECT_RC,
            (reaction_center_smiles, int(is_virtual)),
        ).fetchone()
        if row is None:
            return None
        return np.frombuffer(row[0], dtype=np.uint8)

    def lookup_center_fg_pair(
        self, reaction_center_smiles: str
    ) -> tuple[np.ndarray | None, np.ndarray | None]:
        """Return ``(real_fg, virtual_fg)`` for a center SMILES.

        Either element is ``None`` when the corresponding row is absent.

        :param reaction_center_smiles: The reaction center SMILES.
        :type reaction_center_smiles: str
        :return: Pair of optional FG signatures for real and virtual rows.
        :rtype: tuple[np.ndarray | None, np.ndarray | None]
        """
        return (
            self.find_center(reaction_center_smiles, is_virtual=False),
            self.find_center(reaction_center_smiles, is_virtual=True),
        )

    def update(
        self,
        reaction_center_smiles: str,
        fg_signature: np.ndarray,
        *,
        is_virtual: bool = False,
    ) -> None:
        """Update a reaction center in the database. It's needed
        when ReactionCenrerDBComposer finds the existing reaction center
        in the database and needs to update the reaction center's FG-signature.

        :param reaction_center_smiles: The reaction center smiles to update.
        :type reaction_center_smiles: str
        :param fg_signature: The FG-signature of the reaction center.
        :type fg_signature: np.ndarray
        :param is_virtual: Whether to update the virtual or real row.
        :type is_virtual: bool
        """
        self._ensure_writable()
        self._conn.execute(
            _SQL_UPDATE_RC_FG,
            (
                fg_signature.astype(np.uint8).tobytes(),
                reaction_center_smiles,
                int(is_virtual),
            ),
        )
        self._conn.commit()

    def add_reaction_center(
        self,
        reaction_center_smiles: str,
        fg_signature: np.ndarray,
        is_multi_component: bool = False,
        components: list[str] | None = None,
        *,
        is_virtual: bool = False,
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
        :param is_virtual: Whether this center comes from virtual reactions.
        :type is_virtual: bool
        """
        self._ensure_writable()
        self._conn.execute(
            _SQL_INSERT_RC,
            (
                reaction_center_smiles,
                int(is_virtual),
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
        *,
        is_virtual: bool = False,
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
        :param is_virtual: Whether the linked center is virtual.
        :type is_virtual: bool
        """
        self._ensure_writable()
        self._conn.execute(
            _SQL_INSERT_CTR,
            (
                reaction_center_smiles,
                int(is_virtual),
                reaction_smiles,
                fg_signature.astype(np.uint8).tobytes(),
                sear_signature.astype(np.uint8).tobytes(),
            ),
        )
        self._conn.commit()

    def find_center_to_reaction(
        self,
        reaction_center_smiles: str,
        reaction_smiles: str,
        *,
        is_virtual: bool = False,
    ) -> bool:
        """Check whether a (center, reaction) pair exists in the bridge table.

        :param reaction_center_smiles: The reaction center SMILES.
        :type reaction_center_smiles: str
        :param reaction_smiles: The reaction SMILES.
        :type reaction_smiles: str
        :param is_virtual: Whether to look up the virtual or real bridge row.
        :type is_virtual: bool
        :return: ``True`` if the pair already exists, ``False`` otherwise.
        :rtype: bool
        """
        row = self._conn.execute(
            _SQL_SELECT_CTR,
            (reaction_center_smiles, int(is_virtual), reaction_smiles),
        ).fetchone()
        return row is not None

    def has_center_sear_in_bridge(
        self,
        reaction_center_smiles: str,
        sear_signature: np.ndarray,
        *,
        is_virtual: bool = False,
    ) -> bool:
        """Return whether any bridge row exists for this center and SEAr signature.

        Rows are loaded by reaction center and virtuality; ``sear_signature`` is
        compared in Python so SQLite does not need a BLOB index on
        ``sear_signature``.

        :param reaction_center_smiles: The reaction center SMILES.
        :type reaction_center_smiles: str
        :param sear_signature: SEAr signature to match.
        :type sear_signature: np.ndarray
        :param is_virtual: Whether to search virtual or real bridge rows.
        :type is_virtual: bool
        :rtype: bool
        """
        sear_bytes = sear_signature.astype(np.uint8).tobytes()
        rows = self._conn.execute(
            _SQL_SELECT_FG_SEAR_BY_CENTER,
            (reaction_center_smiles, int(is_virtual)),
        ).fetchall()
        return any(sear_blob == sear_bytes for _, sear_blob in rows)

    def aggregate_fg_signature_for_center_sear(
        self,
        reaction_center_smiles: str,
        sear_signature: np.ndarray,
        *,
        is_virtual: bool = False,
    ) -> np.ndarray:
        """Bitwise-OR of ``fg_signature`` over bridge rows for center + SEAr context.

        Rows are loaded by reaction center and virtuality; ``sear_signature`` is
        matched in Python (see :meth:`has_center_sear_in_bridge`).

        :param reaction_center_smiles: The reaction center SMILES.
        :type reaction_center_smiles: str
        :param sear_signature: SEAr signature to filter rows.
        :type sear_signature: np.ndarray
        :param is_virtual: Whether to aggregate virtual or real bridge rows.
        :type is_virtual: bool
        :return: Combined signature.
        :rtype: np.ndarray
        """
        sear_bytes = sear_signature.astype(np.uint8).tobytes()
        rows = self._conn.execute(
            _SQL_SELECT_FG_SEAR_BY_CENTER,
            (reaction_center_smiles, int(is_virtual)),
        ).fetchall()
        combined = np.zeros(FG_SIGNATURE_LENGTH, dtype=np.uint8)
        for fg_blob, sear_blob in rows:
            if sear_blob != sear_bytes:
                continue
            combined = np.bitwise_or(combined, np.frombuffer(fg_blob, dtype=np.uint8))
        return combined

    def lookup_center_sear_fg_pair(
        self,
        reaction_center_smiles: str,
        sear_signature: np.ndarray,
    ) -> tuple[np.ndarray | None, np.ndarray | None]:
        """Return ``(real_fg, virtual_fg)`` from SEAr bridge rows for a center.

        An element is ``None`` when no bridge row matches that virtuality and
        ``sear_signature``.

        :param reaction_center_smiles: The reaction center SMILES.
        :type reaction_center_smiles: str
        :param sear_signature: SEAr signature to match.
        :type sear_signature: np.ndarray
        :return: Pair of optional aggregated FG signatures.
        :rtype: tuple[np.ndarray | None, np.ndarray | None]
        """
        real_fg: np.ndarray | None = None
        if self.has_center_sear_in_bridge(
            reaction_center_smiles, sear_signature, is_virtual=False
        ):
            real_fg = self.aggregate_fg_signature_for_center_sear(
                reaction_center_smiles, sear_signature, is_virtual=False
            )
        virtual_fg: np.ndarray | None = None
        if self.has_center_sear_in_bridge(
            reaction_center_smiles, sear_signature, is_virtual=True
        ):
            virtual_fg = self.aggregate_fg_signature_for_center_sear(
                reaction_center_smiles, sear_signature, is_virtual=True
            )
        return real_fg, virtual_fg

    def count_center(
        self,
        reaction_center_smiles: str,
        *,
        is_virtual: bool = False,
        sear_signature: np.ndarray | None = None,
    ) -> int:
        """Return the number of reactions linked to a center.

        :param reaction_center_smiles: The reaction center SMILES.
        :type reaction_center_smiles: str
        :param is_virtual: Whether to count virtual or real bridge rows.
        :type is_virtual: bool
        :param sear_signature: Optional exact SEAr context signature.
        :type sear_signature: np.ndarray | None
        :return: Number of rows in ``centers_to_reactions`` for this center.
        :rtype: int
        """
        if sear_signature is None:
            row = self._conn.execute(
                _SQL_COUNT_CTR,
                (reaction_center_smiles, int(is_virtual)),
            ).fetchone()
        else:
            row = self._conn.execute(
                _SQL_COUNT_CTR_SEAR,
                (
                    reaction_center_smiles,
                    int(is_virtual),
                    sear_signature.astype(np.uint8).tobytes(),
                ),
            ).fetchone()
        return row[0]

    def find_center_precedents(
        self,
        reaction_center_smiles: str,
        *,
        is_virtual: bool = False,
        limit: int = 3,
        sear_signature: np.ndarray | None = None,
    ) -> list[tuple[str, str, str, bool]]:
        """Return distinct reaction examples linked to one reaction center.

        Real and virtual rows are queried independently. For SEAr reactions,
        supplying ``sear_signature`` restricts examples to the context used by
        center scoring. When one reaction has multiple document rows, the
        lexicographically first document ID is returned as its representative.

        :param reaction_center_smiles: Reaction-center database key.
        :type reaction_center_smiles: str
        :param is_virtual: Whether to return virtual rather than real rows.
        :type is_virtual: bool
        :param limit: Maximum number of distinct reactions to return.
        :type limit: int
        :param sear_signature: Optional exact SEAr context signature.
        :type sear_signature: np.ndarray | None
        :return: Reaction SMILES, document ID, source and virtuality tuples.
        :rtype: list[tuple[str, str, str, bool]]
        """
        if limit <= 0:
            return []

        if sear_signature is None:
            rows = self._conn.execute(
                _SQL_SELECT_CENTER_PRECEDENTS,
                (reaction_center_smiles, int(is_virtual), limit),
            ).fetchall()
        else:
            rows = self._conn.execute(
                _SQL_SELECT_CENTER_SEAR_PRECEDENTS,
                (
                    reaction_center_smiles,
                    int(is_virtual),
                    sear_signature.astype(np.uint8).tobytes(),
                    limit,
                ),
            ).fetchall()
        return [
            (reaction_smiles, document_id, source, bool(row_is_virtual))
            for reaction_smiles, document_id, source, row_is_virtual in rows
        ]

    def find_center_fg_precedents(
        self,
        reaction_center_smiles: str,
        functional_group_index: int,
        *,
        is_virtual: bool = False,
        limit: int = 3,
        sear_signature: np.ndarray | None = None,
    ) -> list[tuple[str, str, str, bool]]:
        """Return distinct examples containing one FG around a reaction center.

        The FG bit is checked on each ``centers_to_reactions`` bridge row, so
        every returned reaction is direct evidence that the functional group
        occurred with this center. SQLite BLOB positions are one-based, hence
        the ``functional_group_index + 1`` query parameter. When one reaction
        has multiple document rows, the lexicographically first document ID is
        returned as its representative.

        :param reaction_center_smiles: Reaction-center database key.
        :type reaction_center_smiles: str
        :param functional_group_index: Zero-based FG signature position.
        :type functional_group_index: int
        :param is_virtual: Whether to return virtual rather than real rows.
        :type is_virtual: bool
        :param limit: Maximum number of distinct reactions to return.
        :type limit: int
        :param sear_signature: Optional exact SEAr context signature.
        :type sear_signature: np.ndarray | None
        :return: Reaction SMILES, document ID, source and virtuality tuples.
        :rtype: list[tuple[str, str, str, bool]]
        """
        if functional_group_index < 0 or limit <= 0:
            return []

        signature_position = functional_group_index + 1
        if sear_signature is None:
            rows = self._conn.execute(
                _SQL_SELECT_CENTER_FG_PRECEDENTS,
                (
                    reaction_center_smiles,
                    int(is_virtual),
                    signature_position,
                    limit,
                ),
            ).fetchall()
        else:
            rows = self._conn.execute(
                _SQL_SELECT_CENTER_SEAR_FG_PRECEDENTS,
                (
                    reaction_center_smiles,
                    int(is_virtual),
                    sear_signature.astype(np.uint8).tobytes(),
                    signature_position,
                    limit,
                ),
            ).fetchall()
        return [
            (reaction_smiles, document_id, source, bool(row_is_virtual))
            for reaction_smiles, document_id, source, row_is_virtual in rows
        ]

    def list_multi_component_for_dist(
        self, reaction_count: int
    ) -> list[tuple[str, bool, np.ndarray, list[str]]]:
        """Return multi-component centers with more than specified number of
        rows in ``centers_to_reactions`` for distributivity.

        :param reaction_count: The reaction count threshold for distributivity
        :type reaction_count: int
        :return: List of tuples of (composite center SMILES, is_virtual,
            FG-signature, component list).
        """
        rows = self._conn.execute(
            _SQL_SELECT_MULTI_COMPONENT_CENTERS,
            (reaction_count,),
        ).fetchall()
        return [
            (
                smiles,
                bool(is_virtual),
                np.frombuffer(fg_signature, dtype=np.uint8),
                json.loads(comps),
            )
            for smiles, is_virtual, fg_signature, comps in rows
        ]

    def find_reaction_matches(
        self, reaction_smiles: str
    ) -> list[tuple[str, bool]] | None:
        """Return ``(document_id, is_virtual)`` rows for a reaction SMILES.

        Single index scan on ``reaction_smiles``. Callers that only need
        presence should prefer :meth:`find_reaction`.

        :param reaction_smiles: The reaction SMILES to search for.
        :type reaction_smiles: str
        :return: Matching rows as ``(document_id, is_virtual)``, or ``None``
            if the reaction is absent.
        :rtype: list[tuple[str, bool]] | None
        """
        rows = self._conn.execute(
            _SQL_SELECT_REACTION_WITH_VIRTUALITY,
            (reaction_smiles,),
        ).fetchall()
        if not rows:
            return None
        return [(doc_id, bool(is_virtual)) for doc_id, is_virtual in rows]

    def find_reaction(self, reaction_smiles: str) -> list[str] | None:
        """Return the document IDs for a reaction, or None if not found.

        Matches both real and virtual rows. Thin wrapper over
        :meth:`find_reaction_matches` so presence lookups share one SQL path.

        :param reaction_smiles: The reaction SMILES to search for.
        :type reaction_smiles: str
        :return: The document IDs associated with the reaction, or None.
        :rtype: list[str] | None
        """
        matches = self.find_reaction_matches(reaction_smiles)
        if matches is None:
            return None
        return [doc_id for doc_id, _ in matches]

    def find_reaction_document_ids(
        self,
        reaction_smiles: str,
        *,
        is_virtual: bool = False,
    ) -> list[str] | None:
        """Return document IDs for a reaction within one virtuality group.

        :param reaction_smiles: The reaction SMILES to search for.
        :type reaction_smiles: str
        :param is_virtual: Whether to look up virtual or real rows.
        :type is_virtual: bool
        :return: Document IDs, or ``None`` if no matching row exists.
        :rtype: list[str] | None
        """
        rows = self._conn.execute(
            _SQL_SELECT_REACTION_DOCS,
            (reaction_smiles, int(is_virtual)),
        ).fetchall()
        if not rows:
            return None
        return [tupl[0] for tupl in rows]

    def find_reaction_precedents(
        self,
        reaction_smiles: str,
        *,
        is_virtual: bool = False,
        limit: int = 3,
    ) -> list[tuple[str, str, str, bool]]:
        """Return limited document-bearing examples for an exact reaction.

        :param reaction_smiles: Exact canonical reaction SMILES.
        :type reaction_smiles: str
        :param is_virtual: Whether to return virtual rather than real rows.
        :type is_virtual: bool
        :param limit: Maximum number of reaction/document rows to return.
        :type limit: int
        :return: Reaction SMILES, document ID, source and virtuality tuples.
        :rtype: list[tuple[str, str, str, bool]]
        """
        if limit <= 0:
            return []
        rows = self._conn.execute(
            _SQL_SELECT_REACTION_PRECEDENTS,
            (reaction_smiles, int(is_virtual), limit),
        ).fetchall()
        return [
            (matched_smiles, document_id, source, bool(row_is_virtual))
            for matched_smiles, document_id, source, row_is_virtual in rows
        ]

    def add_reaction(
        self,
        reaction_smiles: str,
        document_id: str = "",
        *,
        is_virtual: bool = False,
        source: str = "",
    ) -> None:
        """Insert a reaction into the database.

        :param reaction_smiles: The reaction SMILES to add.
        :type reaction_smiles: str
        :param document_id: The document ID where the reaction originates.
        :type document_id: str
        :param is_virtual: Whether this reaction is virtual.
        :type is_virtual: bool
        :param source: Provenance string (e.g. CSV ``rxn_idx`` for virtual).
        :type source: str
        """
        self._ensure_writable()
        self._conn.execute(
            _SQL_INSERT_REACTION,
            (reaction_smiles, document_id, int(is_virtual), source),
        )
        self._conn.commit()

    def __enter__(self) -> DBManager:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._conn.close()
