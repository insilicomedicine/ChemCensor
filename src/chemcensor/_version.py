from importlib.metadata import PackageNotFoundError
from importlib.metadata import version


def installed_version(fallback: str = "0+unknown") -> str:
    """Return the installed ChemCensor distribution version."""
    try:
        return version("chemcensor")
    except PackageNotFoundError:
        return fallback
