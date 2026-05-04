class ChemCensorError(Exception):
    """Base class for ChemCensor errors."""


class InvalidCenterTypeError(ChemCensorError):
    """Raised when an invalid reaction center type is provided."""

    def __init__(self, value: object) -> None:
        self.value = value
        super().__init__(
            f"Invalid max_center_type={value!r}; "
            f"expected int 1–4 or ReactionCenterType"
        )
