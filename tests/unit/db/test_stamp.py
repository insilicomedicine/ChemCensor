from importlib.metadata import version

import pytest

from chemcensor.db.errors import InvalidDBVersionError
from chemcensor.db.stamp import build_stamp
from chemcensor.db.stamp import validate_db_version


class TestBuildStamp:
    def test_includes_requested_version_label(self):
        assert build_stamp("U3-1")["db_version"] == "U3-1"

    def test_includes_installed_chemcensor_version(self):
        assert build_stamp("U3-1")["chemcensor_version"] == version("chemcensor")

    def test_built_at_defaults_to_utc_now(self):
        built_at = build_stamp("U3-1")["built_at"]

        assert built_at.endswith("Z")
        # ISO-8601 with second precision, e.g. 2026-08-20T09:14:02Z
        assert len(built_at) == 20

    def test_built_at_can_be_supplied(self):
        stamp = build_stamp("U3-1", built_at="2026-08-20T09:14:02Z")

        assert stamp["built_at"] == "2026-08-20T09:14:02Z"

    def test_values_are_all_strings(self):
        assert all(isinstance(value, str) for value in build_stamp("U3-1").values())

    @pytest.mark.parametrize("label", ["", "   "])
    def test_rejects_blank_version_label(self, label):
        with pytest.raises(InvalidDBVersionError, match="db_version"):
            build_stamp(label)

    def test_strips_surrounding_whitespace_from_label(self):
        assert build_stamp("  U3-1  ")["db_version"] == "U3-1"


class TestValidateDbVersion:
    def test_returns_stripped_label(self):
        assert validate_db_version("  U3-1 ") == "U3-1"

    @pytest.mark.parametrize("label", ["", "   "])
    def test_rejects_blank_label(self, label):
        with pytest.raises(InvalidDBVersionError, match="db_version"):
            validate_db_version(label)
