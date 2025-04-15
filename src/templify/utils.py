"""
Utility functions for Templify
"""
from typing import Any


def get_value_from_path(obj: dict[str, Any], path: str) -> Any:
    """
    Get a value from a nested dictionary using a dot-notation path.

    Args:
        obj: The dictionary to traverse
        path: The dot-notation path to the value

    Returns:
        The value at the specified path, or the original path if not found
    """
    current = obj
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
