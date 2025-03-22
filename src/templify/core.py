"""
Core functionality for Templify.

This module provides the main templating functionality including:
- Text template rendering
- Recursive data structure templating
- JMESPath query support
- PDF document templating
"""
import re
from pathlib import Path
from typing import Any


def get_value_from_path(obj: dict[str, Any], path: str) -> Any:
    """
    Get a value from a nested dictionary using a dot-notation path.

    Args:
        obj: The dictionary to traverse
        path: The dot-notation path to the value

    Returns:
        The value at the specified path, or the original path if not found

    Examples:
        >>> data = {"user": {"name": "Alice", "notifications": 5}}
        >>> get_value_from_path(data, "user.name")
        'Alice'
        >>> get_value_from_path(data, "user.notifications")
        5
        >>> get_value_from_path(data, "nonexistent")
        'nonexistent'
    """
    current = obj
    for key in path.split('.'):
        if not isinstance(current, dict):
            return path
        current = current.get(key, path)
    return current


def render_text(template: str, context: dict[str, Any]) -> str:
    """
    Render a text template with placeholders.

    Args:
        template: The template string containing placeholders in {placeholder} format
        context: Dictionary containing values for placeholders

    Returns:
        Rendered string with placeholders replaced

    Examples:
        >>> template = (
        ...     "Welcome, {user.name}! "
        ...     "You have {user.notifications} new messages."
        ... )
        >>> context = {"user": {"name": "Alice", "notifications": 5}}
        >>> render_text(template, context)
        'Welcome, Alice! You have 5 new messages.'

        >>> template = "Hello {name}, your balance is {balance}"
        >>> context = {"name": "John"}
        >>> render_text(template, context)
        'Hello John, your balance is {balance}'
    """
    def replace_placeholder(match: re.Match) -> str:
        placeholder = match.group(1)
        value = get_value_from_path(context, placeholder)
        return str(value) if value != placeholder else f"{{{placeholder}}}"

    pattern = r'\{([^}]+)\}'
    return re.sub(pattern, replace_placeholder, template)


def render_data(
    data: dict[str, Any] | list,
    context: dict[str, Any]
) -> dict[str, Any] | list:
    """
    Recursively render placeholders in a data structure.

    Args:
        data: Dictionary or list containing placeholders
        context: Dictionary containing values for placeholders

    Returns:
        Data structure with placeholders replaced

    Examples:
        >>> data = {
        ...     "report": {
        ...         "title": "Sales for {month}",
        ...         "summary": "Total units sold: {sales.total}",
        ...     },
        ...     "generated_on": "{date}",
        ... }
        >>> context = {
        ...     "month": "March",
        ...     "sales": {"total": 1500},
        ...     "date": "2025-04-01"
        ... }
        >>> result = render_data(data, context)
        >>> result == {
        ...     "report": {
        ...         "title": "Sales for March",
        ...         "summary": "Total units sold: 1500"
        ...     },
        ...     "generated_on": "2025-04-01"
        ... }
        True

        >>> data = {
        ...     "items": [
        ...         {"name": "{product.name}", "price": "{product.price}"},
        ...         {"name": "{product.name}", "price": "{product.price}"}
        ...     ]
        ... }
        >>> context = {
        ...     "product": {"name": "Test Product", "price": "100"}
        ... }
        >>> result = render_data(data, context)
        >>> result == {
        ...     "items": [
        ...         {"name": "Test Product", "price": "100"},
        ...         {"name": "Test Product", "price": "100"}
        ...     ]
        ... }
        True
    """
    if isinstance(data, dict):
        return {k: render_data(v, context) for k, v in data.items()}
    elif isinstance(data, list):
        return [render_data(item, context) for item in data]
    elif isinstance(data, str):
        return render_text(data, context)
    return data


def render_pdf_file(
    template_path: str | Path,
    output_path: str | Path,
    context: dict[str, Any]
) -> None:
    """
    Render a PDF template with placeholders.

    Args:
        template_path: Path to the PDF template
        output_path: Path where the rendered PDF should be saved
        context: Dictionary containing values for placeholders

    Raises:
        FileNotFoundError: If template file doesn't exist
        ValueError: If required placeholders are missing
    """
    # TODO: Implement PDF template rendering
    template_path = Path(template_path)
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    output_path = Path(output_path)
    output_path.touch()  # Create empty file for now
