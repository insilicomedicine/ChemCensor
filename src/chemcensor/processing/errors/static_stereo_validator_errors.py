from .processing_errors import ProcessingError


class StaticStereoValidatorError(ProcessingError):
    """Exception raised when static stereo validation fails."""

    pass


class StaticStereoValidatorEmptyTransformError(StaticStereoValidatorError):
    """Raised when static stereo validation cannot start without a transform."""

    def __init__(self):
        super().__init__(
            "Reaction transform is empty. Static stereo validation is not possible."
        )


class StaticStereoValidatorRuntimeError(StaticStereoValidatorError):
    """Raised when stereo specification extraction fails during validation."""

    def __init__(self, msg: str, smiles: str):
        self.msg = msg
        self.smiles = smiles
        super().__init__(self.msg)

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"StaticStereoValidatorRuntimeError: {self.msg} for {self.smiles}"


class StaticStereoValidatorInconsistentStaticAtomStereoError(
    StaticStereoValidatorError
):
    """Raised when static atom stereochemistry differs between product
    and reactant(s)."""

    def __init__(self, reaction_smiles: str):
        self.reaction_smiles = reaction_smiles
        super().__init__(
            "Assigned atom stereocenters in the static part of the molecule "
            "are inconsistent between the product and the reactant(s): "
            f"{reaction_smiles}"
        )


class StaticStereoValidatorEmptyStereoSpecificationError(StaticStereoValidatorError):
    """Raised when static stereo validation cannot start without a stereo
    specification for the product or the reactant(s)."""

    def __init__(self):
        super().__init__(
            "Stereo specification is empty. Static stereo validation is not possible."
        )


class StaticStereoValidatorInconsistentStaticBondStereoError(
    StaticStereoValidatorError
):
    """Raised when static bond stereochemistry differs between product
    and reactant(s)."""

    def __init__(self, reaction_smiles: str):
        self.reaction_smiles = reaction_smiles
        super().__init__(
            "Assigned bond stereo centers in the static part of the molecule "
            "are inconsistent between the product and the reactant(s): "
            f"{reaction_smiles}"
        )


class StaticStereoValidatorInvalidStaticCenterError(StaticStereoValidatorError):
    """Raised when a supposedly static atom stereocenter is not fully mappable."""

    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(self.msg)


class StaticStereoValidatorInvalidStaticBondError(StaticStereoValidatorError):
    """Raised when a supposedly static bond stereocenter is not fully mappable."""

    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(self.msg)
