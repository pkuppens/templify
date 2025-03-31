"""
Core templating functionality for Templify.

This module provides the main templating functionality including:
- Text template rendering
- Recursive data structure templating
- JMESPath query support
- Jinja2 template support
- PDF document templating
"""

from enum import Enum
from pathlib import Path
from typing import Any, Union, Optional
import re
import xml.etree.ElementTree as ET

import jmespath
from jinja2 import (
    Environment, 
    FileSystemLoader, 
    StrictUndefined, 
    UndefinedError, 
    select_autoescape,
    DebugUndefined
)
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from .utils import get_value_from_path


class MissingKeyHandling(Enum):
    """Enum for handling missing keys in templates."""
    KEEP = "keep"  # Keep the placeholder as is
    DEFAULT = "default"  # Use default value based on type
    RAISE = "raise"  # Raise ValueError (default Jinja2 behavior)


class DefaultUndefined(StrictUndefined):
    """Custom Undefined class that returns default values based on type."""
    def __str__(self):
        name = str(self._undefined_name)
        if '_num' in name or '_number' in name:
            return "0"
        elif '_list' in name or '_array' in name:
            return "[]"
        elif '_bool' in name or '_boolean' in name:
            return "False"
        return ""
    
    def __int__(self):
        return 0
    
    def __float__(self):
        return 0.0
    
    def __list__(self):
        return []
    
    def __bool__(self):
        return False


def render_text(
    template: str, 
    context: dict[str, Any],
    handle_missing: MissingKeyHandling = MissingKeyHandling.KEEP
) -> str:
    """
    Render a text template with placeholders.

    Args:
        template: The template string containing placeholders in {placeholder} format
        context: Dictionary containing values for placeholders
        handle_missing: How to handle missing keys (KEEP, DEFAULT, or RAISE)

    Returns:
        Rendered string with placeholders replaced
    """
    # First try jmespath template {{ key }}
    if '{{' in template and '}}' in template:
        return render_jinja2(template, context, handle_missing=handle_missing)

    # Otherwise, {key} format
    def replace_placeholder(match: re.Match) -> str:
        placeholder = match.group(1)
        value = get_value_from_path(context, placeholder)
        
        if value == placeholder:  # Key not found
            if handle_missing == MissingKeyHandling.KEEP:
                return f"{{{placeholder}}}"
            elif handle_missing == MissingKeyHandling.DEFAULT:
                # Try to infer type from placeholder name
                if '_num' in placeholder or '_number' in placeholder:
                    return "0"
                elif '_list' in placeholder or '_array' in placeholder:
                    return "[]"
                elif '_bool' in placeholder or '_boolean' in placeholder:
                    return "False"
                else:
                    return ""
            else:  # RAISE
                raise ValueError(
                    f"Missing required template variable: {placeholder}"
                )
        return str(value)

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


def render_jmespath_template(
    template: str, 
    context: dict[str, Any],
    handle_missing: MissingKeyHandling = MissingKeyHandling.KEEP
) -> str:
    """
    Render a template with JMESPath expressions.

    Args:
        template: The template string containing JMESPath expressions
        context: Dictionary containing data to query
        handle_missing: How to handle missing keys (KEEP, DEFAULT, or RAISE)

    Returns:
        Rendered string with JMESPath expressions evaluated
    """
    def replace_jmespath(match: re.Match) -> str:
        expr = match.group(1).strip()

        # Handle simple variable references (e.g., {{ name }})
        if '|' not in expr:
            value = get_value_from_path(context, expr)
            if value == expr:  # Key not found
                if handle_missing == MissingKeyHandling.KEEP:
                    return f"{{{{ {expr} }}}}"
                elif handle_missing == MissingKeyHandling.DEFAULT:
                    return ""
                else:  # RAISE
                    raise ValueError(
                        f"Missing required template variable: {expr}"
                    )
            return str(value)

        # Handle JMESPath expressions
        parts = expr.split('|')
        if len(parts) != 2 or not parts[1].strip().startswith('jmespath('):
            raise ValueError(f"Invalid JMESPath expression: {expr}")

        # Extract the data path and JMESPath expression
        data_path = parts[0].strip()
        jmespath_expr = parts[1].strip()[9:-2]  # Remove 'jmespath("' and '")'

        # Get the data to query
        data = get_value_from_path(context, data_path)
        if data == data_path:  # Key not found
            if handle_missing == MissingKeyHandling.KEEP:
                return f"{{{{ {expr} }}}}"
            elif handle_missing == MissingKeyHandling.DEFAULT:
                return ""
            else:  # RAISE
                raise ValueError(
                    f"Missing required template variable: {data_path}"
                )

        # Execute the query
        result = execute_jmespath_query(jmespath_expr, data)
        return str(result)

    pattern = r'\{\{([^}]+)\}\}'
    return re.sub(pattern, replace_jmespath, template)


def render_data(
    data: dict[str, Any] | list,
    context: dict[str, Any],
    handle_missing: MissingKeyHandling = MissingKeyHandling.KEEP
) -> dict[str, Any] | list:
    """
    Recursively render placeholders in a data structure.

    Args:
        data: Dictionary or list containing placeholders
        context: Dictionary containing values for placeholders
        handle_missing: How to handle missing keys (KEEP, DEFAULT, or RAISE)

    Returns:
        Data structure with placeholders replaced
    """
    if isinstance(data, dict):
        return {
            k: render_data(v, context, handle_missing) 
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [
            render_data(item, context, handle_missing) 
            for item in data
        ]
    if isinstance(data, str):
        # First try JMESPath template
        if '{{' in data and '}}' in data:
            return render_jmespath_template(data, context, handle_missing)
        # Then try regular placeholder
        return render_text(data, context, handle_missing)
    return data


def render_jinja2(
    template: Union[str, Path],
    context: dict[str, Any],
    templates: dict[str, str] | None = None,
    filters: dict[str, Any] | None = None,
    handle_missing: MissingKeyHandling = MissingKeyHandling.KEEP
) -> str:
    """
    Render a Jinja2 template.

    Args:
        template: The Jinja2 template string or path to template file
        context: Dictionary containing values for template variables
        templates: Optional dictionary of template names to template strings
        filters: Optional dictionary of custom filters to register
        handle_missing: How to handle missing keys (KEEP, DEFAULT, or RAISE)

    Returns:
        Rendered string with template expressions evaluated
    """
    # Create a Jinja2 environment
    if isinstance(template, Path):
        template_dir = str(template.parent)
        template_name = template.name
    else:
        template_dir = '.'
        template_name = None

    if handle_missing == MissingKeyHandling.KEEP:
        env = Environment(
            autoescape=select_autoescape(['html', 'xml']),
            loader=FileSystemLoader(template_dir),
            undefined=DebugUndefined
        )
    elif handle_missing == MissingKeyHandling.DEFAULT:
        env = Environment(
            autoescape=select_autoescape(['html', 'xml']),
            loader=FileSystemLoader(template_dir),
            undefined=DefaultUndefined
        )
    else:  # RAISE
        env = Environment(
            autoescape=select_autoescape(['html', 'xml']),
            loader=FileSystemLoader(template_dir),
            undefined=StrictUndefined
        )

    # Register custom filters if provided
    if filters:
        for name, func in filters.items():
            env.filters[name] = func

    # Load template
    if template_name:
        template_obj = env.get_template(template_name)
    else:
        template_obj = env.from_string(template)

    try:
        return template_obj.render(**context)
    except UndefinedError as e:
        if handle_missing == MissingKeyHandling.RAISE:
            raise ValueError(f"Missing required template variable: {str(e)}")
        return str(template)


def render_pdf(
    template: str,
    context: dict[str, Any],
    output_path: Optional[Union[str, Path]] = None,
    content: Optional[list[dict[str, Any]]] = None,
    handle_missing: MissingKeyHandling = MissingKeyHandling.KEEP,
) -> Union[bytes, Path]:
    """Render a PDF document from a template.

    Args:
        template: The template string or file path
        context: The context data for template rendering
        output_path: Optional path to save the PDF (if not provided, returns bytes)
        content: Optional list of content items for the PDF
        handle_missing: How to handle missing keys (KEEP, DEFAULT, or RAISE)

    Returns:
        The rendered PDF as bytes or the path to the saved file
    """
    # First render the template
    rendered = render_data(template, context, handle_missing)

    # Parse the XML template and create elements
    elements = []
    for elem in ET.fromstring(rendered).iter():
        if elem.tag == 'text':
            elements.append(
                Paragraph(
                    elem.text or "",
                    getSampleStyleSheet()["Normal"]
                )
            )

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
        elements.extend([
            Paragraph(
                str(content_item.get("text", "")),
                getSampleStyleSheet()["Normal"],
            )
            for content_item in content
        ])

    # Build document from elements
    doc.build(elements)

    return doc.filename if output_path else doc.getpdfdata()
