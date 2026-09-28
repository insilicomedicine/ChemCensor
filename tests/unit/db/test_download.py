from pathlib import Path
from unittest.mock import patch

from chemcensor.db.download import DEFAULT_DATABASE_FILENAME
from chemcensor.db.download import DEFAULT_DATABASE_REPO_ID
from chemcensor.db.download import download_default_database
from chemcensor.db.download import resolve_database_path


def test_download_default_database_uses_hugging_face_cache(tmp_path: Path) -> None:
    downloaded = tmp_path / DEFAULT_DATABASE_FILENAME

    with patch(
        "huggingface_hub.hf_hub_download",
        return_value=str(downloaded),
    ) as download:
        result = download_default_database(cache_dir=tmp_path)

    assert result == downloaded
    download.assert_called_once_with(
        repo_id=DEFAULT_DATABASE_REPO_ID,
        filename=DEFAULT_DATABASE_FILENAME,
        repo_type="dataset",
        cache_dir=tmp_path,
        force_download=False,
        token=None,
        local_files_only=False,
    )


def test_resolve_database_path_preserves_explicit_path(tmp_path: Path) -> None:
    explicit = tmp_path / "custom.sqlite"

    with patch(
        "chemcensor.db.download.download_default_database",
        side_effect=AssertionError("explicit paths must not trigger downloads"),
    ):
        assert resolve_database_path(explicit) == explicit


def test_resolve_database_path_downloads_when_omitted(tmp_path: Path) -> None:
    downloaded = tmp_path / DEFAULT_DATABASE_FILENAME

    with patch(
        "chemcensor.db.download.download_default_database",
        return_value=downloaded,
    ) as download:
        assert resolve_database_path(None) == downloaded

    download.assert_called_once_with(cache_dir=None)
