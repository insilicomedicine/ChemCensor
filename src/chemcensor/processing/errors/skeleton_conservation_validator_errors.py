from .processing_errors import ProcessingError


class SkeletonConservationValidatorError(ProcessingError):
    """Exception raised when skeleton-conservation validation fails."""

    pass


class SkeletonConservationValidatorEmptyTransformError(
    SkeletonConservationValidatorError
):
    """Raised when skeleton-conservation validation cannot start without a
    transform."""

    def __init__(self) -> None:
        super().__init__(
            "Reaction transform is empty. "
            "Skeleton-conservation validation is not possible."
        )


class SkeletonConservationValidatorTruncatedCarbonChainError(
    SkeletonConservationValidatorError
):
    """Raised when a pure-hydrocarbon fragment is deleted from (or added to) a
    retained molecule across a broken carbon-carbon bond.

    This flags chemically implausible "homolog drift" artifacts such as an
    ethyl ether silently becoming a methyl ether: the carbon-heteroatom bond is
    preserved, but the carbon chain loses (or gains) carbons with no
    corresponding leaving group or reagent to account for it.
    """

    def __init__(self, reaction_smiles: str, side: str) -> None:
        self.reaction_smiles = reaction_smiles
        self.side = side
        super().__init__(
            "A pure-hydrocarbon fragment is "
            f"{'deleted from' if side == 'reactant' else 'added to'} the "
            f"{side} skeleton across a broken carbon-carbon bond, with no "
            "leaving group or reagent to account for it: "
            f"{reaction_smiles}"
        )
