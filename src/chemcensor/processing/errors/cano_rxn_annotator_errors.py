from .processing_errors import ProcessingError


class CanoRxnAnnotatorError(ProcessingError):
    """Exception raised when canonical reaction annotation fails."""

    pass


class CanoRxnAnnotatorEmptyTransformError(CanoRxnAnnotatorError):
    """Exception raised when the reaction transform is missing."""

    def __init__(self):
        super().__init__(
            "Reaction transform is empty. "
            "Canonical reaction SMILES annotation is not possible."
        )
