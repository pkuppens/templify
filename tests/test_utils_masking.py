"""
Tests for mask_value_for_keys (log-safe JSON/object snapshots).
"""

import json

from templify import mask_value_for_keys
from templify.utils import mask_value_for_keys as mask_value_for_keys_direct


class TestMaskValueForKeys:
    """Regression and behaviour tests for sensitive-field masking."""

    def test_does_not_mutate_original_nested_dict(self) -> None:
        """The live dict used at runtime must keep secrets after masking."""
        inner = {"password": "secret", "x": 1}
        original: dict = {"user": {"Patient_Name": "Jane"}, "nested": inner}
        original_id = id(original)
        inner_id = id(inner)

        masked = mask_value_for_keys(original)

        assert original["user"]["Patient_Name"] == "Jane"
        assert original["nested"]["password"] == "secret"
        assert id(original) == original_id
        assert id(original["nested"]) == inner_id
        assert masked["user"]["Patient_Name"] == "*****"
        assert masked["nested"]["password"] == "*****"

    def test_nested_dict_default_keys(self) -> None:
        """Default keys password and patient_name are masked case-insensitively."""
        data = {"password": "p", "Patient_Name": "Pat", "ok": "visible"}
        assert mask_value_for_keys(data) == {
            "password": "*****",
            "Patient_Name": "*****",
            "ok": "visible",
        }

    def test_list_of_dicts(self) -> None:
        """Lists are traversed; each dict is masked."""
        data = [{"password": "a"}, {"password": "b", "other": 1}]
        assert mask_value_for_keys(data) == [{"password": "*****"}, {"password": "*****", "other": 1}]

    def test_json_string_valid_masks(self) -> None:
        """JSON text is parsed, masked, and re-serialized."""
        raw = '{"password": "x", "n": 1}'
        out = mask_value_for_keys(raw)
        assert json.loads(out) == {"password": "*****", "n": 1}

    def test_json_string_invalid_unchanged(self) -> None:
        """Non-JSON strings are returned as-is."""
        raw = "not json {"
        assert mask_value_for_keys(raw) is raw

    def test_custom_mask_keys_and_mask(self) -> None:
        """Callers can override key set and placeholder."""
        data = {"token": "t", "password": "p"}
        result = mask_value_for_keys(data, mask_keys={"token"}, mask="[REDACTED]")
        assert result == {"token": "[REDACTED]", "password": "p"}

    def test_empty_containers(self) -> None:
        """Empty dict and list round-trip."""
        assert mask_value_for_keys({}) == {}
        assert mask_value_for_keys([]) == []

    def test_non_string_sensitive_value_masked(self) -> None:
        """Values for sensitive keys are replaced entirely (any type)."""
        data = {"password": 12345, "patient_name": True}
        assert mask_value_for_keys(data) == {"password": "*****", "patient_name": "*****"}

    def test_export_and_direct_import_equivalent(self) -> None:
        """Package export matches utils module."""
        d = {"password": "s"}
        assert mask_value_for_keys(d) == mask_value_for_keys_direct(d)
