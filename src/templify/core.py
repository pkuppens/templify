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
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Optional, Union

import jmespath
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate


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

        # Handle simple variable references (e.g., {{ name }})
        if '|' not in expr:
            return str(get_value_from_path(context, expr))

        # Handle JMESPath expressions
        parts = expr.split('|')
        if len(parts) != 2 or not parts[1].strip().startswith('jmespath('):
            raise ValueError(f"Invalid JMESPath expression: {expr}")

        # Extract the data path and JMESPath expression
        data_path = parts[0].strip()
        jmespath_expr = parts[1].strip()[9:-2]  # Remove 'jmespath("' and '")'

        # Get the data to query
        data = get_value_from_path(context, data_path)
        if data == data_path:
            raise ValueError(f"Data not found: {data_path}")

        # Execute the query
        result = execute_jmespath_query(jmespath_expr, data)
        return str(result)

    pattern = r'\{\{([^}]+)\}\}'
    return re.sub(pattern, replace_jmespath, template)


def render_jinja2(
    template: Union[str, Path],
    context: dict[str, Any],
    templates: dict[str, str] | None = None,
    filters: dict[str, Any] | None = None
) -> str:
    """
    Render a Jinja2 template.

    Args:
        template: The Jinja2 template string or path to template file
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
        for _, content in templates.items():
            env.get_template = lambda n: Template(content) if n in templates else None

    # Create and render the template
    try:
        # If template is a Path, read its contents
        if isinstance(template, Path):
            with open(template, 'r') as f:
                template = f.read()

        template_obj = env.from_string(template)
        return template_obj.render(**context)
    except Exception as e:
        raise ValueError(f"Error rendering Jinja2 template: {e!s}") from e


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
    if isinstance(data, list):
        return [render_data(item, context) for item in data]
    if isinstance(data, str):
        # First try JMESPath template
        if '{{' in data and '}}' in data:
            return render_jmespath_template(data, context)
        # Then try regular placeholder
        return render_text(data, context)
    return data


def render_pdf(
    template: str,
    context: dict[str, Any],
    output_path: Optional[Union[str, Path]] = None,
    content: Optional[list[dict[str, Any]]] = None,
) -> Union[bytes, Path]:
    """Render a PDF document from a template.

    Args:
        template: The template string or file path
        context: The context data for template rendering
        output_path: Optional path to save the PDF (if not provided, returns bytes)
        content: Optional list of content items for the PDF

    Returns:
        The rendered PDF as bytes or the path to the saved file

    Example:
        >>> template = '''
        ... <document>
        ...     <page>
        ...         <text>Hello, {{name}}!</text>
        ...     </page>
        ... </document>
        ... '''
        >>> context = {"name": "World"}
        >>> pdf_bytes = render_pdf(template, context)
        >>> with open("output.pdf", "wb") as f:
        ...     f.write(pdf_bytes)
    """
    # First render the template
    rendered = render_data(template, context)

    # Parse the XML template
    root = ET.fromstring(rendered)

    # Create PDF document
    doc = SimpleDocTemplate(
        str(output_path) if output_path else None,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
    )

    # Process content if provided
    if content:
        # Convert content to PDF elements
        elements = [
            Paragraph(
                str(content_item.get("text", "")),
                getSampleStyleSheet()["Normal"],
            )
            for content_item in content
        ]
        doc.build(elements)
    else:
        # Build document from template
        doc.build([])

    return doc.filename if output_path else doc.getpdfdata()
