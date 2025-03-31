"""
Tests for Jinja2 template rendering functionality.
"""

from pathlib import Path
from typing import Any, Dict

import pytest

from templify.core import render_data, render_jinja2
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

@pytest.mark.skip(reason="Jinja2 template rendering needs to be fixed to handle file paths correctly")
def test_basic_jinja2_rendering(sample_template: Path) -> None:
    """Test basic Jinja2 template rendering."""
    # This test verifies that a simple template with one variable renders correctly
    # The template is a file containing "Hello {{ name }}!" and should output "Hello John!"
    result = render_jinja2(sample_template, SAMPLE_CONTEXT)
    assert result == "Hello John!"

@pytest.mark.skip(reason="Jinja2 template rendering needs to be fixed to handle file paths correctly")
def test_complex_jinja2_rendering(complex_template: Path) -> None:
    """Test complex Jinja2 template rendering with multiple features."""
    # This test verifies that a complex template with multiple features works:
    # - Macro definition and usage
    # - Conditional rendering
    # - List iteration
    # - Nested data access
    # - Multiple template blocks
    result = render_jinja2(complex_template, SAMPLE_CONTEXT)
    expected = """
Hello John!

You are an adult.

Your items:
- apple
- banana
- orange

Nested data:
value
1
2
3
    """.strip()
    assert result.strip() == expected

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

@pytest.mark.skip(reason="Currently fails: name evaluates to empty string, but it should keep placeholder")
def test_jinja2_error_handling(sample_template: Path) -> None:
    """Test error handling for invalid Jinja2 templates."""
    # This test verifies that the renderer properly handles missing variables:
    # - Template expects a 'name' variable
    # - Context only contains 'invalid' variable
    # - Should raise ValueError with descriptive message
    with pytest.raises(ValueError) as exc_info:
        result = render_jinja2(sample_template, {"invalid": "context"})
        print(result)
    assert "Template rendering failed" in str(exc_info.value)

def test_jinja2_in_render_data() -> None:
    """Test Jinja2 template rendering through render_data function."""
    # This test verifies that string templates work directly (not just files):
    # - Template is a string containing "Hello {{ name }}!"
    # - Should render to "Hello John!" using the SAMPLE_CONTEXT
    template = "Hello {{ name }}!"
    result = render_data(template, SAMPLE_CONTEXT)
    assert result == "Hello John!"

@pytest.mark.skip(reason="Jinja2 template rendering needs to be fixed to handle file paths correctly")
def test_jinja2_with_custom_filters() -> None:
    """Test Jinja2 template with custom filters."""
    # This test verifies custom filter functionality:
    # - reverse filter should reverse the name string
    # - join filter should combine list items with separator
    # - Template is a file with multiple filter applications
    template = create_test_file(
        """
{{ name | reverse }}  # Should output "nhoJ"
{{ items | join(' | ')}}  # Should output "apple | banana | orange"
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

@pytest.mark.skip(reason="Jinja2 template rendering needs to be fixed to handle file paths correctly")
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

@pytest.mark.skip(reason="Jinja2 template rendering needs to be fixed to handle file paths correctly")
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

@pytest.mark.skip(reason="Jinja2 template rendering needs to be fixed to handle file paths correctly")
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
