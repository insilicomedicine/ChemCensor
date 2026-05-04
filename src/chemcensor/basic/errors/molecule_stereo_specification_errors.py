class MoleculeStereoSpecificationError(Exception):
    """Exception raised when molecule stereo specification fails."""

    pass


class MoleculeStereoSpecificationRuntimeError(MoleculeStereoSpecificationError):
    """Exception raised when molecule stereo specification runtime error occurs."""

    def __init__(self, msg: str, molecule_smiles: str):
        self.msg = msg
        self.molecule_smiles = molecule_smiles
        super().__init__(self.msg)

    def __str__(self):
        return self.msg

    def __repr__(self):
        return (
            f"MoleculeStereoSpecificationRuntimeError for molecule "
            f"{self.molecule_smiles!r}: {self.msg!r}"
        )
