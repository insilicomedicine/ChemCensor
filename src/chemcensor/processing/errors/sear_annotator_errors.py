from .processing_errors import ProcessingError


class SeArAnnotatorError(ProcessingError):
    """Error raised when SEAr annotator fails."""

    pass


class EmptyReactionTransformError(SeArAnnotatorError):
    """Error raised when reaction transform is empty."""

    def __init__(self):
        super().__init__(
            "Reaction transform is empty. SEAr annotator cannot be applied."
        )


class NoReactantsReactingAtomsError(SeArAnnotatorError):
    """Error raised when no reacting atoms are found in reactants."""

    def __init__(self):
        super().__init__(
            "No reacting atoms found in reactants. SEAr annotator cannot be applied."
        )
