from __future__ import annotations

from os import PathLike
from pathlib import Path


DEFAULT_DATABASE_REPO_ID = "insilicomedicine/chemcensor"
DEFAULT_DATABASE_FILENAME = "ChemCensor-DB-U3.sqlite"
DEFAULT_DATABASE_MIN_VERSION = "1.3.0"


def download_default_database(
    *,
    cache_dir: str | PathLike | None = None,
    force_download: bool = False,
    token: str | bool | None = None,
    local_files_only: bool = False,
) -> Path:
    """Download the default ChemCensor database into the Hugging Face cache.

    Subsequent calls reuse the cached file. Hugging Face handles concurrent
    downloads, resumable transfers and integrity checks.

    :param cache_dir: Optional Hugging Face cache directory.
    :param force_download: Download again even when a cached file exists.
    :param token: Hugging Face token or ``True`` to use the configured token.
    :param local_files_only: Resolve only from the local cache without network.
    :return: Local path to the SQLite database.
    """
    from huggingface_hub import hf_hub_download

    normalized_cache_dir = Path(cache_dir) if cache_dir is not None else None
    path = hf_hub_download(
        repo_id=DEFAULT_DATABASE_REPO_ID,
        filename=DEFAULT_DATABASE_FILENAME,
        repo_type="dataset",
        cache_dir=normalized_cache_dir,
        force_download=force_download,
        token=token,
        local_files_only=local_files_only,
    )
    return Path(path)


def resolve_database_path(
    db_path: str | PathLike | None,
    *,
    cache_dir: str | PathLike | None = None,
) -> Path:
    """Return an explicit database path or download the default database."""
    if db_path is not None:
        return Path(db_path)
    return download_default_database(cache_dir=cache_dir)
