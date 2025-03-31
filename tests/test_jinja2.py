"""
Tests for Jinja2 template rendering functionality.
"""

from pathlib import Path
from typing import Any, Dict

import pytest

from templify.core import MissingKeyHandling, render_data, render_jinja2, render_text
from tests.utils import create_test_file, get_project_tmp_dir

# Test data used across multiple tests
# Contains a mix of simple values, lists, and nested dictionaries
SAMPLE_CONTEXT = {
    "name": "John",
    "age": 30,
    "items": ["apple", "banana", "orange"],
    "nested": {
        "key": "value",
        "list": [1, 2, 3],
    },
}

@pytest.fixture
def sample_greet_template_single() -> Path:
    """Create a sample Jinja2 template string single curly braces."""
    return "Hello {name}!"  # Simple template with one variable


@pytest.fixture
def sample_greet_template_double() -> Path:
    """Create a sample Jinja2 template string double curly braces escaped."""
    return "Hello {{ name }}!"  # Simple template with one variable


@pytest.fixture
def sample_template() -> Path:
    """Create a sample Jinja2 template file."""
    return create_test_file(
        "Hello {{ name }}!",  # Simple template with one variable
        prefix="jinja2_sample_",
        suffix=".j2"
    )

@pytest.fixture
def complex_template() -> Path:
    """Create a complex Jinja2 template file with multiple features."""
    return create_test_file(
        """
{% macro greet(name) %}
Hello {{ name }}!
{% endmacro %}
{{ greet(name) }}
{% if age >= 18 %}
You are an adult.
{% else %}
You are a minor.
{% endif %}

Your items:
{% for item in items %}
- {{ item }}
{% endfor %}

Nested data:
{{ nested.key }}
{% for num in nested.list %}
{{ num }}
{% endfor %}
        """,
        prefix="jinja2_complex_",
        suffix=".j2"
    )


@pytest.fixture
def template_with_filters() -> Path:
    """Create a template using Jinja2 filters."""
    return create_test_file(
        """
{{ name | upper }}
{{ items | length }}
{{ nested.list | sum }}
        """,
        prefix="jinja2_filters_",
        suffix=".j2"
    )


def test_basic_jinja2_rendering(sample_template: Path) -> None:
    """Test basic Jinja2 template rendering."""
    # This test verifies that a simple template with one variable
    # renders correctly. The template is a file containing
    # "Hello {{ name }}!" and should output "Hello John!"
    result = render_jinja2(sample_template, SAMPLE_CONTEXT)
    assert result == "Hello John!"


def test_complex_jinja2_rendering(complex_template: Path) -> None:
    """Test complex Jinja2 template rendering with multiple features."""
    # This test verifies that a complex template with multiple features works:
    # - Macro definition and usage
    # - Conditional rendering
    # - List iteration
    # - Nested data access
    # - Multiple template blocks
    # Note that an exact string match is complicated due to the
    # newlines and spacing
    result = render_jinja2(complex_template, SAMPLE_CONTEXT)
    assert "Hello John!" in result
    assert "You are an adult." in result
    assert "Your items:" in result
    assert "- banana" in result
    assert "3" in result


def test_jinja2_filters(template_with_filters: Path) -> None:
    """Test Jinja2 filter usage."""
    # This test verifies that Jinja2 filters work correctly:
    # - upper filter converts text to uppercase
    # - length filter gets list length
    # - sum filter adds numbers in a list
    result = render_jinja2(template_with_filters, SAMPLE_CONTEXT)
    expected = """
JOHN
3
6
    """.strip()
    assert result.strip() == expected


def test_jinja2_simple_key_handling() -> None:
    """Test error handling for handling missing keys in Jinja2 templates."""
    # This test verifies that the renderer properly handles missing variables:
    # - Template expects a 'name' variable
    # - Context only contains 'invalid' variable
    # Templify should keep the placeholder {{ name }} in the output
    # Note that Jinja2 will raise an error if the variable is not found
    result = render_text("Hello {name}!", {"name": "John"})
    assert result == "Hello John!"


def test_jinja2_simple_double_key_handling() -> None:
    """Test error handling for handling missing keys in Jinja2 templates."""
    # This test verifies that the renderer properly handles missing variables:
    # - Template expects a 'name' variable
    # - Context only contains 'invalid' variable
    # Templify should keep the placeholder {{ name }} in the output
    # Note that Jinja2 will raise an error if the variable is not found
    result = render_text("Hello {{ name }}!", {"name": "John"})
    assert result == "Hello John!"


def test_jinja2_missing_simple_key_handling(sample_template: Path) -> None:
    """Test error handling for handling missing keys in Jinja2 templates."""
    # This test verifies that the renderer properly handles missing variables:
    # - Template expects a 'name' variable
    # - Context only contains 'invalid' variable
    # Templify should keep the placeholder {{ name }} in the output
    # Note that Jinja2 will raise an error if the variable is not found
    result = render_text("Hello {name}!", {"invalid": "context"})
    print(result)
    assert result == "Hello {name}!"


def test_jinja2_missing_key_handling_keep():
    """Test keeping missing keys in templates."""
    result = render_text(
        "Hello {name}!",
        {"invalid": "context"},
        handle_missing=MissingKeyHandling.KEEP
    )
    assert result == "Hello {name}!"

    result = render_text(
        "Hello {{ name }}!",
        {"invalid": "context"},
        handle_missing=MissingKeyHandling.KEEP
    )
    assert result == "Hello {{ name }}!"


def test_jinja2_missing_key_handling_default():
    """Test default values for missing keys."""
    context = {"valid": "value"}
    template = """
    String: {{ missing_str }}
    Number: {{ missing_num }}
    List: {{ missing_list }}
    Boolean: {{ missing_bool }}
    """
    result = render_text(
        template,
        context,
        handle_missing=MissingKeyHandling.DEFAULT
    )
    assert "String: " in result
    assert "Number: 0" in result
    assert "List: []" in result
    assert "Boolean: False" in result


def test_jinja2_missing_key_handling_raise():
    """Test raising error for missing keys."""
    with pytest.raises(ValueError):
        render_text(
            "Hello {{ name }}!",
            {"invalid": "context"},
            handle_missing=MissingKeyHandling.RAISE
        )

    with pytest.raises(ValueError):
        render_text(
            "Hello {name}!",
            {"invalid": "context"},
            handle_missing=MissingKeyHandling.RAISE
        )


def test_jinja2_mixed_template_handling():
    """Test templates with both existing and missing keys."""
    template = "Hello {{ name }}, Age: {{ age }}!"
    context = {"name": "John"}

    # Test KEEP behavior
    result = render_text(
        template,
        context,
        handle_missing=MissingKeyHandling.KEEP
    )
    assert result == "Hello John, Age: {{ age }}!"

    # Test DEFAULT behavior
    result = render_text(
        template,
        context,
        handle_missing=MissingKeyHandling.DEFAULT
    )
    assert result == "Hello John, Age: !"


def test_jinja2_in_render_data() -> None:
    """Test Jinja2 template rendering through render_data function."""
    # This test verifies that string templates work directly (not just files):
    # - Template is a string containing "Hello {{ name }}!"
    # - Should render to "Hello John!" using the SAMPLE_CONTEXT
    template = "Hello {{ name }}!"
    result = render_data(template, SAMPLE_CONTEXT)
    assert result == "Hello John!"


def test_jinja2_with_custom_filters() -> None:
    """Test Jinja2 template with custom filters."""
    # This test verifies custom filter functionality:
    # - reverse filter should reverse the name string
    # - join filter should combine list items with separator
    # - Template is a file with multiple filter applications
    template = create_test_file(
        """
{{ name | reverse }}
{{ items | join(' | ')}}
        """,
        prefix="jinja2_custom_filters_",
        suffix=".j2"
    )
    result = render_jinja2(template, SAMPLE_CONTEXT)
    expected = """
nhoJ
apple | banana | orange
    """.strip()
    assert result.strip() == expected


def test_jinja2_with_conditionals() -> None:
    """Test Jinja2 template with conditional logic."""
    # This test verifies conditional rendering:
    # - Template checks age against 25
    # - Uses if/elif/else structure
    # - Should output "You are over 25" since age is 30
    template = create_test_file(
        """
{% if age > 25 %}
You are over 25
{% elif age == 25 %}
You are exactly 25
{% else %}
You are under 25
{% endif %}
        """,
        prefix="jinja2_conditionals_",
        suffix=".j2"
    )
    result = render_jinja2(template, SAMPLE_CONTEXT)
    assert "You are over 25" in result


def test_jinja2_with_loops() -> None:
    """Test Jinja2 template with loop constructs."""
    # This test verifies loop functionality:
    # - Iterates over items list
    # - Uses loop.index for counter
    # - Should output numbered list of items
    template = create_test_file(
        """
{% for item in items %}
Item {{ loop.index }}: {{ item }}
{% endfor %}
        """,
        prefix="jinja2_loops_",
        suffix=".j2"
    )
    result = render_jinja2(template, SAMPLE_CONTEXT)
    expected = """
Item 1: apple

Item 2: banana

Item 3: orange
    """.strip()
    assert result.strip() == expected


def test_jinja2_with_nested_data() -> None:
    """Test Jinja2 template with nested data structures."""
    # This test verifies nested data access:
    # - Accesses nested.key directly
    # - Iterates over nested.list
    # - Should output value and numbered list
    template = create_test_file(
        """
{{ nested.key }}
{% for num in nested.list %}
Number: {{ num }}
{% endfor %}
        """,
        prefix="jinja2_nested_",
        suffix=".j2"
    )
    result = render_jinja2(template, SAMPLE_CONTEXT)
    expected = """
value

Number: 1

Number: 2

Number: 3
    """.strip()
    assert result.strip() == expected
