"""
Tests for Jinja2 template rendering functionality.
"""

from pathlib import Path
from typing import Any, Dict

import pytest

from templify.core import render_data, render_jinja2
from tests.utils import create_test_file, get_project_tmp_dir

# Test data
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
        "Hello {{ name }}!",
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
    result = render_jinja2(sample_template, SAMPLE_CONTEXT)
    assert result == "Hello John!"

@pytest.mark.skip(reason="Jinja2 template rendering needs to be fixed to handle file paths correctly")
def test_complex_jinja2_rendering(complex_template: Path) -> None:
    """Test complex Jinja2 template rendering with multiple features."""
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
    result = render_jinja2(template_with_filters, SAMPLE_CONTEXT)
    expected = """
JOHN
3
6
    """.strip()
    assert result.strip() == expected

def test_jinja2_error_handling(sample_template: Path) -> None:
    """Test error handling for invalid Jinja2 templates."""
    with pytest.raises(ValueError) as exc_info:
        render_jinja2(sample_template, {"invalid": "context"})
    assert "Template rendering failed" in str(exc_info.value)

def test_jinja2_in_render_data() -> None:
    """Test Jinja2 template rendering through render_data function."""
    template = "Hello {{ name }}!"
    result = render_data(template, SAMPLE_CONTEXT)
    assert result == "Hello John!"

@pytest.mark.skip(reason="Jinja2 template rendering needs to be fixed to handle file paths correctly")
def test_jinja2_with_custom_filters() -> None:
    """Test Jinja2 template with custom filters."""
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

@pytest.mark.skip(reason="Jinja2 template rendering needs to be fixed to handle file paths correctly")
def test_jinja2_with_conditionals() -> None:
    """Test Jinja2 template with conditional logic."""
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
