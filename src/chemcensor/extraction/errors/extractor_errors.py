from .extraction_errors import ExtractionError


class ExtractorError(ExtractionError):
    """Error raised when reaction center extraction fails."""

    pass


class MissingReactionTransformError(ExtractorError):
    """Error raised when reaction transform is not available on the reaction."""

    def __init__(self) -> None:
        super().__init__(
            "Reaction transform is not available. " "Cannot extract reaction centers."
        )


class MissingReactingAtomsError(ExtractorError):
    """Error raised when reacting atoms are not set on the transform."""

    def __init__(self) -> None:
        super().__init__(
            "Reacting atoms are not set on the transform. "
            "Cannot extract reaction center."
        )


class EmptySMARTSError(ExtractorError):
    """Error raised when a fragment produces an empty SMARTS string."""

    def __init__(self, fragment_label: str) -> None:
        self.fragment_label = fragment_label
        super().__init__(f"{fragment_label} produced an empty SMARTS string.")

    def __repr__(self) -> str:
        return f"EmptySMARTSError(fragment_label={self.fragment_label!r})"
