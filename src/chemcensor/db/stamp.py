from __future__ import annotations

from datetime import datetime
from datetime import timezone
from os import PathLike

from .._version import installed_version
from .errors import DatabaseAlreadyStampedError
from .errors import InvalidDBVersionError
from .manager import DBManager

DB_VERSION_KEY = "db_version"
BUILT_AT_KEY = "built_at"
CHEMCENSOR_VERSION_KEY = "chemcensor_version"


def build_stamp(db_version: str, built_at: str | None = None) -> dict[str, str]:
    """Return the key/value build stamp for a freshly composed database.

    :param db_version: Catalog version label for this build (e.g. ``U3-1``).
    :type db_version: str
    :param built_at: Build timestamp as an ISO-8601 UTC string. Defaults to now.
    :type built_at: str | None
    :return: Stamp values to pass to
        :meth:`~chemcensor.db.manager.DBManager.write_metadata`.
    :rtype: dict[str, str]
    :raises InvalidDBVersionError: If *db_version* is empty or blank.
    """
    return {
        DB_VERSION_KEY: validate_db_version(db_version),
        BUILT_AT_KEY: built_at or _utc_now(),
        CHEMCENSOR_VERSION_KEY: _chemcensor_version(),
    }


def validate_db_version(db_version: str) -> str:
    """Return *db_version* stripped, raising if it is missing or blank.

    :param db_version: Catalog version label (e.g. ``U3-1``).
    :type db_version: str
    :return: The stripped label.
    :rtype: str
    :raises InvalidDBVersionError: If *db_version* is empty or blank.
    """
    label = str(db_version).strip()
    if not label:
        raise InvalidDBVersionError(
            "db_version must be a non-empty version label (e.g. 'U3-1')"
        )

    return label


def _utc_now() -> str:
    """Return the current UTC time as ``YYYY-MM-DDTHH:MM:SSZ``."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _chemcensor_version() -> str:
    """Return the installed chemcensor version, or ``unknown`` if unavailable."""
    return installed_version("unknown")


def stamp_database_file(
    db_path: str | PathLike,
    db_version: str,
    *,
    built_at: str | None = None,
    force: bool = False,
) -> dict[str, str]:
    """Stamp an existing database file in place, without rebuilding it.

    :param db_path: The path to the SQLite database file.
    :type db_path: str | PathLike
    :param db_version: Catalog version label (e.g. ``U3-1``).
    :type db_version: str
    :param built_at: Build timestamp as an ISO-8601 UTC string. Defaults to now.
    :type built_at: str | None
    :param force: Refresh the stamp even when the file already carries a
        ``db_version``. Required to replace a *different* label.
    :type force: bool
    :return: The stamp stored in the file. When the file already carries the
        same label and *force* is not set, the existing stamp is returned
        unchanged.
    :rtype: dict[str, str]
    :raises InvalidDBVersionError: If *db_version* is blank.
    :raises DatabaseAlreadyStampedError: If the file already carries a
        different label and *force* is not set.
    :raises DBManagerFileNotFoundError: If the database file is missing.
    """
    stamp = build_stamp(db_version, built_at=built_at)
    existing = DBManager.read_metadata(db_path)
    existing_version = existing.get(DB_VERSION_KEY)
    if existing_version and not force:
        if existing_version != stamp[DB_VERSION_KEY]:
            raise DatabaseAlreadyStampedError(
                f"Database is already stamped as {existing_version!r}; "
                f"pass force=True to restamp it as {stamp[DB_VERSION_KEY]!r}"
            )
        # Same label without force: idempotent no-op. Leave built_at and
        # chemcensor_version untouched so a re-run from a newer install does
        # not silently rewrite the provenance of an unchanged database.
        return existing

    DBManager.stamp_file(db_path, stamp)
    return stamp
