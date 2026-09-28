from importlib.metadata import PackageNotFoundError
from unittest.mock import patch

from chemcensor._version import installed_version


def test_installed_version_reads_public_distribution() -> None:
    with patch("chemcensor._version.version", return_value="1.4.0") as lookup:
        assert installed_version() == "1.4.0"
    lookup.assert_called_once_with("chemcensor")


def test_installed_version_returns_requested_fallback() -> None:
    with patch(
        "chemcensor._version.version",
        side_effect=PackageNotFoundError,
    ):
        assert installed_version("unknown") == "unknown"
