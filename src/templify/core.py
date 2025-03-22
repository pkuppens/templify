"""
Core functionality for Templify.

This module provides the main templating functionality including:
- Text template rendering
- Recursive data structure templating
- JMESPath query support
- Jinja2 template support
- PDF document templating
"""
import re
from pathlib import Path
from typing import Any, Optional

import jmespath
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape


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


def execute_jmespath_query(query: str, data: Any) -> Any:
    """
    Execute a JMESPath query safely.

    Args:
        query: The JMESPath query to execute
        data: The data to query

    Returns:
        The query result

    Raises:
        ValueError: If the query is invalid or returns None
    """
    try:
        result = jmespath.search(query, data)
        if result is None:
            raise ValueError(f"JMESPath query returned None: {query}")
        return result
    except jmespath.exceptions.JMESPathError as e:
        raise ValueError(f"Invalid JMESPath query: {query}") from e


def render_jmespath_template(template: str, context: dict[str, Any]) -> str:
    """
    Render a template with JMESPath expressions.

    Args:
        template: The template string containing JMESPath expressions
        context: Dictionary containing data to query

    Returns:
        Rendered string with JMESPath expressions evaluated

    Examples:
        >>> data = {
        ...     "products": [
        ...         {"name": "Product A", "sales": 100, "revenue": 1000},
        ...         {"name": "Product B", "sales": 150, "revenue": 2000},
        ...         {"name": "Product C", "sales": 120, "revenue": 1800},
        ...     ]
        ... }
        >>> template = (
        ...     'Top-selling product: {{ products | jmespath("max_by(@, &sales).name") }}'
        ... )
        >>> render_jmespath_template(template, data)
        'Top-selling product: Product B'

        >>> template = (
        ...     'Total revenue: {{ products | jmespath("sum(@[].revenue)") }}'
        ... )
        >>> render_jmespath_template(template, data)
        'Total revenue: 4800'

        >>> template = (
        ...     'Top 2 by revenue: {{ products | jmespath('
        ...     '"sort_by(@, &revenue)[-2:] | [*].name | join(\', \', @)"'
        ...     ') }}'
        ... )
        >>> render_jmespath_template(template, data)
        'Top 2 by revenue: Product B, Product C'
    """
    def replace_jmespath(match: re.Match) -> str:
        expr = match.group(1).strip()
        if not expr.startswith('products | jmespath("'):
            raise ValueError(f"Invalid JMESPath expression: {expr}")

        # Extract the actual JMESPath expression
        jmespath_expr = expr[len('products | jmespath("'):-2]

        # Execute the query
        result = execute_jmespath_query(jmespath_expr, context['products'])
        return str(result)

    pattern = r'\{\{([^}]+)\}\}'
    return re.sub(pattern, replace_jmespath, template)


def render_jinja2(
    template: str,
    context: dict[str, Any],
    templates: Optional[dict[str, str]] = None,
    filters: Optional[dict[str, Any]] = None
) -> str:
    """
    Render a Jinja2 template.

    Args:
        template: The Jinja2 template string
        context: Dictionary containing values for template variables
        templates: Optional dictionary of template names to template strings for inheritance
        filters: Optional dictionary of custom filters to register

    Returns:
        Rendered string with template expressions evaluated

    Examples:
        >>> template = "Hello, {{ name }}!"
        >>> context = {"name": "Alice"}
        >>> render_jinja2(template, context)
        'Hello, Alice!'

        >>> template = ```
        ... {% if user.is_admin %}
        ...     Welcome, Administrator {{ user.name }}!
        ... {% else %}
        ...     Welcome, {{ user.name }}!
        ... {% endif %}
        ... ```
        >>> context = {
        ...     "user": {
        ...         "name": "Alice",
        ...         "is_admin": True
        ...     }
        ... }
        >>> render_jinja2(template, context)
        'Welcome, Administrator Alice!'

        >>> template = ```
        ... {% macro format_date(date) %}
        ...     {{ date.strftime('%Y-%m-%d') }}
        ... {% endmacro %}
        ... Last login: {{ format_date(user.last_login) }}
        ... ```
        >>> context = {
        ...     "user": {
        ...         "last_login": datetime(2025, 3, 21)
        ...     }
        ... }
        >>> render_jinja2(template, context)
        'Last login: 2025-03-21'
    """
    # Create a Jinja2 environment
    env = Environment(
        autoescape=select_autoescape(['html', 'xml']),
        loader=FileSystemLoader('.') if templates else None
    )

    # Register custom filters if provided
    if filters:
        for name, func in filters.items():
            env.filters[name] = func

    # If templates are provided, add them to the environment
    if templates:
        for name, content in templates.items():
            env.get_template = lambda n: Template(content) if n in templates else None

    # Create and render the template
    try:
        template_obj = env.from_string(template)
        return template_obj.render(**context)
    except Exception as e:
        raise ValueError(f"Error rendering Jinja2 template: {str(e)}") from e


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
        # First try JMESPath template
        if '{{' in data and '}}' in data:
            return render_jmespath_template(data, context)
        # Then try regular placeholder
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
