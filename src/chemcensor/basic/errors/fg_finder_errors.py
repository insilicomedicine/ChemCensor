from chemcensor.basic import Reaction


class FGFinderError(Exception):
    """Base class for FGFinder errors."""

    pass


class FGFinderNoTransformError(FGFinderError):
    """Raised when a reaction has no ReactionTransform."""

    def __init__(self, reaction: Reaction):
        self.reaction = reaction
        super().__init__(
            f"Reaction {reaction.reaction_smiles} has no "
            "annotated ReactionTransform."
        )


class FGFinderNoReactionCentersError(FGFinderError):
    """Raised when a reaction has no ReactionCenters."""

    def __init__(self, reaction: Reaction):
        self.reaction = reaction
        super().__init__(
            f"Reaction {reaction.reaction_smiles} has no " "annotated ReactionCenters."
        )
