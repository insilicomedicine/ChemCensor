class DatabaseError(Exception):
    """Base class for database errors."""

    pass


class DBManagerFileNotFoundError(DatabaseError):
    """Raised when the database file is not found."""

    def __init__(self, msg_or_cause: str | BaseException) -> None:
        super().__init__(msg_or_cause)
