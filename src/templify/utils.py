"""
Utility functions for Templify
"""


def is_placeholder(value: str) -> bool:
    """
    Check if a string is a placeholder.

    Args:
        value: String to check

    Returns:
        True if the string is a placeholder, False otherwise
    """
    return isinstance(value, str) and (
        (value.startswith("{")
        and value.endswith("}"))
        or (value.startswith("{{")
        and value.endswith("}}"))
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
