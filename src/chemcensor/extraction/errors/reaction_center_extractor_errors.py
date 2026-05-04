from .extraction_errors import ExtractionError


class ReactionCenterExtractorError(ExtractionError):
    """Error raised when reaction center extraction or annotation fails."""

    def __init__(self, msg_or_cause: str | BaseException) -> None:
        if isinstance(msg_or_cause, BaseException):
            super().__init__(str(msg_or_cause))
        else:
            super().__init__(msg_or_cause)
