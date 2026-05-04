from .processing_errors import ProcessingError


class MapperError(ProcessingError):
    """Exception raised when reaction atom-mapping fails."""

    def __init__(self, reaction_smiles=None, msg=None):
        self.reaction_smiles = reaction_smiles
        self.msg = msg or "Mapping error"
        super().__init__(self.msg)

    def __str__(self):
        return self.msg

    def __repr__(self):
        rxn = repr(self.reaction_smiles) if self.reaction_smiles is not None else "None"
        return f"MapperError(reaction_smiles={rxn}, msg={self.msg!r})"


class JobSpecificationError(ProcessingError):
    """Exception raised when job number specification is invalid."""

    def __init__(self, msg=None):
        self.msg = msg or "Job specification error"
        super().__init__(self.msg)

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"JobSpecificationError(msg={self.msg!r})"


class ValidationError(ProcessingError):
    """Exception raised when validation fails."""

    def __init__(self, msg: str, reaction_smiles: str):
        """Initialize validation error.

        :param msg: Human-readable error message.
        :type msg: str
        :param reaction_smiles: Reaction SMILES string that failed validation.
        :type reaction_smiles: str
        """
        self.msg = msg
        self.reaction_smiles = reaction_smiles
        super().__init__(self.msg)

    def __str__(self):
        return self.msg

    def __repr__(self):
        return (
            f"{type(self).__name__}(msg={self.msg!r}, "
            f"reaction_smiles={self.reaction_smiles!r})"
        )


class RxnSmilesLengthError(ValidationError):
    """Exception raised when reaction smiles length is invalid."""

    pass


class RxnSmilesSyntaxError(ValidationError):
    """Exception raised when reaction smiles syntax is invalid."""

    pass


class RxnSmilesArrowsError(ValidationError):
    """Exception raised when reaction smiles
    contains coordinate bond arrows.
    """

    pass


class RxnSmilesNoCarbonError(ValidationError):
    """Exception raised when reaction smiles does not contain any carbon."""

    pass


class RxnSmilesRDKitError(ValidationError):
    """Exception raised when reaction smiles is invalid."""

    pass
