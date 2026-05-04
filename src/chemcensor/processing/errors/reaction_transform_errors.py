from .processing_errors import ProcessingError


class ReactionTransformError(ProcessingError):
    """Exception raised when reaction transform creation fails."""

    pass


class ReactionTransformEmptyReactionSMILESError(ReactionTransformError):
    """Exception raised when reaction transform creation fails
    because the processed reaction SMILES is empty."""

    def __init__(self):
        super().__init__(
            "Cannot create reaction transform. processed_reaction_smiles is empty. "
        )


class ReactionTransformCreationError(ReactionTransformError):
    """Exception raised when reaction transform creation fails."""

    def __init__(self, error: Exception):
        super().__init__(f"Cannot create reaction transform. {error}")
