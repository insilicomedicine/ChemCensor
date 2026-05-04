class FunctionalGroupError(Exception):
    """Base class for functional group errors."""

    pass


class InvalidSMARTSStringError(FunctionalGroupError):
    """Raised when an invalid SMARTS string is provided."""

    def __init__(self, smarts: str):
        self.smarts = smarts
        super().__init__(f"Invalid SMARTS string: {smarts}")


class MissingRequiredKeysError(FunctionalGroupError):
    """Raised when required keys are missing from the functional group data."""

    def __init__(self, missing_keys: set[str]):
        self.missing_keys = missing_keys
        keys_str = ", ".join(sorted(missing_keys))
        super().__init__(f"Missing required keys in functional group data: {keys_str}")


class InvalidDataTypesError(FunctionalGroupError):
    """Raised when invalid data types are provided for the functional group data."""

    def __init__(self, invalid_data_type: type, key: str, expected_type: type):
        self.key = key
        self.invalid_data_type = invalid_data_type
        self.expected_type = expected_type
        super().__init__(
            f"Invalid data types in functional group data: "
            f"{self.invalid_data_type} for key: {self.key}. "
            f"Expected type: {expected_type}"
        )


class FunctionalGroupsInitializationError(FunctionalGroupError):
    """Raised when the functional groups initialization fails."""

    def __init__(self):
        super().__init__("Functional groups initialization failed")
