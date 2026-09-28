class DatabaseError(Exception):
    """Base class for database errors."""

    pass


class DBManagerFileNotFoundError(DatabaseError):
    """Raised when the database file is not found."""

    def __init__(self, msg_or_cause: str | BaseException) -> None:
        super().__init__(msg_or_cause)


class InvalidDBVersionError(DatabaseError):
    """Raised when a build-stamp ``db_version`` label is missing or blank."""


class DatabaseAlreadyStampedError(DatabaseError):
    """Raised when stamping would overwrite a different existing ``db_version``."""
