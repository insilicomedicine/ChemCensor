from .processing_errors import ProcessingError


class OrphanRemoverError(ProcessingError):
    """Error raised when orphan remover fails."""

    pass


class ReactionNotSplitError(OrphanRemoverError):
    """Error raised when reaction is not split into reactants and product."""

    def __init__(self, reaction_smiles: str):
        self.reaction_smiles = reaction_smiles
        super().__init__(
            f"Reaction {reaction_smiles} is not split into"
            "reactants and product by >> separator."
        )


class NoMappedReactantsError(OrphanRemoverError):
    """Error raised when no mapped reactants are found in reaction."""

    def __init__(self, reaction_smiles: str):
        self.reaction_smiles = reaction_smiles
        super().__init__(f"No mapped reactants found in reaction {reaction_smiles}.")


class NoMappedProductError(OrphanRemoverError):
    """Error raised when no mapped product are found in reaction."""

    def __init__(self, reaction_smiles: str):
        self.reaction_smiles = reaction_smiles
        super().__init__(f"No mapped product found in reaction {reaction_smiles}.")


class MultipleMappedProductsError(OrphanRemoverError):
    """Error raised when multiple mapped products are found in reaction."""

    def __init__(self, reaction_smiles: str):
        self.reaction_smiles = reaction_smiles
        super().__init__(
            f"Multiple mapped products found in reaction {reaction_smiles}."
        )
