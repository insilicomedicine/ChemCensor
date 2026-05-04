class ReactionTransformError(Exception):
    """Base class for reaction transform errors."""

    pass


class ProductMissingAtomMapError(ReactionTransformError):
    """Error raised when a reaction transform initialization fails."""

    def __init__(self, reaction_smiles: str):
        self.reaction_smiles = reaction_smiles
        super().__init__(
            f"Product in reaction SMILES lacks atom map: {reaction_smiles}"
        )


class ReactantsMissingAtomMapError(ReactionTransformError):
    """Error raised when a reaction transform initialization fails."""

    def __init__(self, reaction_smiles: str):
        self.reaction_smiles = reaction_smiles
        super().__init__(
            f"Reactants in reaction SMILES lack atom map: {reaction_smiles}"
        )
