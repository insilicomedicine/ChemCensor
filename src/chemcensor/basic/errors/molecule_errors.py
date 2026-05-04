class MoleculeError(Exception):
    """Base class for molecule errors."""

    pass


class InvalidSMILESError(MoleculeError):
    """Raised when an invalid SMILES string is provided."""

    def __init__(self, smiles: str):
        self.smiles = smiles
        super().__init__(f"Invalid SMILES string: {smiles}")
