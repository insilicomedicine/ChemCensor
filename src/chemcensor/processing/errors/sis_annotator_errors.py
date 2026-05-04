from .processing_errors import ProcessingError


class SisAnnotatorError(ProcessingError):
    """Exception raised when SIS annotator fails."""

    pass


class SisAnnotatorEmptyTransformError(SisAnnotatorError):
    """Exception raised when SIS annotator runtime error occurs."""

    def __init__(selfr):
        super().__init__("Reaction transform is empty. SIS annotation is not possible.")


class SisAnnotatorRuntimeError(SisAnnotatorError):
    """Exception raised when SIS annotator runtime error occurs."""

    def __init__(self, msg: str, smiles: str):
        self.msg = msg
        self.smiles = smiles
        super().__init__(self.msg)

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"SisAnnotatorRuntimeError: {self.msg} for {self.smiles}"


class SisAnnotatorInconsistentStaticCentersError(SisAnnotatorError):
    """Raised when assigned stereo centers outside the reaction center
    are not preserved between the product and the reactant(s)."""

    def __init__(self, reaction_smiles: str):
        self.reaction_smiles = reaction_smiles
        super().__init__(
            f"Assigned stereo centers in the static part of the molecule "
            f"are inconsistent between the product and the reactant(s): "
            f"{reaction_smiles}"
        )
