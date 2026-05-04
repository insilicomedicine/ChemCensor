from .extraction_errors import ExtractionError


class FragmentExtractorError(ExtractionError):
    """Error raised when molecular fragment extraction fails."""

    pass


class MoleculeNotSetError(FragmentExtractorError):
    """Error raised when extraction is attempted without a molecule."""

    def __init__(self) -> None:
        super().__init__(
            "Molecule is not set. "
            "Call extract_fragment() before using internal methods."
        )
