"""
Utility functions for Templify.

Includes :func:`mask_value_for_keys` for log-safe snapshots of nested data (see that
function's docstring). It does not replace encryption or access control.
"""
from __future__ import annotations

import json
from collections.abc import Collection
from typing import Any

DEFAULT_MASK_KEYS: frozenset[str] = frozenset({"password", "patient_name"})


def get_value_from_path(obj: dict[str, Any], path: str) -> Any:
    """
    Get a value from a nested dictionary using a dot-notation path.

    Args:
        obj: The dictionary to traverse
        path: The dot-notation path to the value

    Returns:
        The value at the specified path, or the original path if not found
    """
    current: Any = obj
    for key in path.split("."):
        if not isinstance(current, dict):
            return path
        current = current.get(key, path)
    return current


def is_placeholder(value: str) -> bool:
    """
    Check if a string is a placeholder.

    Args:
        value: String to check

    Returns:
        True if the string is a placeholder, False otherwise
    """
    return isinstance(value, str) and (
        (value.startswith("{") and value.endswith("}")) or (value.startswith("{{") and value.endswith("}}"))
    )


def extract_placeholder_value(placeholder: str) -> str:
    """
    Extract the value from a placeholder string.

    Args:
        placeholder: Placeholder string
            (e.g. "{user.name}" or "{{ products | jmespath(...) }}")

    Returns:
        The value inside the placeholder
    """
    if not is_placeholder(placeholder):
        return placeholder

    # Remove the outer braces
    value = placeholder.strip("{}")

    # If it's a JMESPath expression, return the full expression, stripped of whitespace
    if "| jmespath" in value:
        return value.strip()

    # Otherwise, return the path
    return value.strip()


def mask_value_for_keys(
    data: Any,
    mask_keys: Collection[str] | None = None,
    mask: str = "*****",
) -> Any:
    """
    Return a deep-shaped copy of nested dicts/lists with selected keys redacted.

    Intended for safe logging, debugging, and support output so secrets and
    identifiers (for example passwords or patient names) are not printed in plain
    text. This is not encryption, secure storage, or a substitute for a secrets
    manager or centralized log redaction in your application.

    The function does **not** mutate ``data``. You may pass the same dict or list
    your code uses at runtime; only the returned value contains masks. For a
    string that parses as JSON, a new JSON string is returned on success; if the
    string is not valid JSON, it is returned unchanged.

    Redaction at emit time can be centralized (for example ``logging`` filters or
    structured logging processors) or done at the call site by passing the return
    value into ``logger`` calls or ``print``.

    Args:
        data: A nested ``dict``/``list`` structure, or a ``str`` containing JSON.
        mask_keys: Key names to redact, compared case-insensitively. Each entry
            should be lowercase (values are normalized to lowercase). If omitted,
            ``password`` and ``patient_name`` are used.
        mask: Placeholder string written in place of sensitive values.

    Returns:
        A new structure of the same shape as the input, with matching values
        replaced by ``mask``, or for JSON strings a new JSON string, or the
        original string if it is not valid JSON.
    """

    normalized_keys: frozenset[str] = (
        frozenset(k.lower() for k in mask_keys) if mask_keys is not None else DEFAULT_MASK_KEYS
    )

    def _mask(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: (mask if k.lower() in normalized_keys else _mask(v)) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_mask(item) for item in obj]
        return obj

    if isinstance(data, str):
        try:
            parsed: Any = json.loads(data)
        except json.JSONDecodeError:
            return data
        return json.dumps(_mask(parsed))

    return _mask(data)
