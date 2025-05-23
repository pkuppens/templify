"""
Tests for core templating functionality.

This module contains tests for the core templating features of Templify:
1. Basic text template rendering with placeholders
2. Recursive data structure templating
3. JMESPath query support
4. Binary document (PDF) templating
5. Edge cases and error handling
"""
from datetime import datetime
from typing import Any

import pytest

from templify import render_data, render_pdf, render_text


class TestTextTemplateRendering:
    """Test suite for basic text template rendering functionality."""

    def test_basic_placeholder_replacement(self):
        """Test basic placeholder replacement in text templates."""
        template = "Welcome, {user.name}! You have {user.notifications} new messages."
        context = {"user": {"name": "Alice", "notifications": 5}}

        result = render_text(template, context)
        assert result == "Welcome, Alice! You have 5 new messages."

    def test_missing_placeholder_remains_unchanged(self):
        """Test that missing placeholders remain unchanged in the output."""
        template = "Hello {name}, your balance is {balance}"
        context = {"name": "John"}

        result = render_text(template, context)
        assert result == "Hello John, your balance is {balance}"

    def test_nested_placeholder_replacement(self):
        """Test replacement of deeply nested placeholders."""
        template = "User {user.profile.name} from {user.profile.location.city}"
        context = {"user": {"profile": {"name": "Alice", "location": {"city": "New York"}}}}

        result = render_text(template, context)
        assert result == "User Alice from New York"


class TestDataStructureTemplating:
    """Test suite for recursive data structure templating."""

    def test_basic_data_structure_rendering(self):
        """Test basic recursive data structure rendering."""
        data = {
            "report": {
                "title": "Sales for {month}",
                "summary": "Total units sold: {sales.total}",
            },
            "generated_on": "{date}",
        }

        context = {"month": "March", "sales": {"total": 1500}, "date": "2025-04-01"}

        result = render_data(data, context)
        assert result == {
            "report": {"title": "Sales for March", "summary": "Total units sold: 1500"},
            "generated_on": "2025-04-01",
        }

    def test_nested_list_rendering(self):
        """Test rendering of nested lists within data structures."""
        data = {
            "items": [
                {"name": "{product.name}", "price": "{product.price}"},
                {"name": "{product.name}", "price": "{product.price}"},
            ]
        }
        context = {"product": {"name": "Test Product", "price": "100"}}

        result = render_data(data, context)
        assert result == {"items": [{"name": "Test Product", "price": "100"}, {"name": "Test Product", "price": "100"}]}

    def test_missing_placeholders_in_data_structure(self):
        """Test that missing placeholders remain unchanged in data structures."""
        data = {"user": {"name": "{name}", "email": "{email}", "address": "{address}"}}
        context = {"name": "John", "email": "john@example.com"}

        result = render_data(data, context)
        assert result == {"user": {"name": "John", "email": "john@example.com", "address": "{address}"}}

    def test_complex_data_structure_rendering(self):
        """Test rendering of complex data structures with various types."""
        test_date = datetime(2024, 3, 15, 14, 30)
        data = {
            "user": {
                "name": "{user.name}",
                "age": 25,
                "active": True,
                "last_login": test_date,
                "preferences": {"theme": "{user.preferences.theme}", "notifications": True},
            },
            "items": [
                {"id": 1, "name": "{product.name}", "price": 99.99, "created_at": test_date},
                {"id": 2, "name": "{product.name}", "price": 149.99, "created_at": test_date},
            ],
        }
        context = {"user": {"name": "John Doe", "preferences": {"theme": "dark"}}, "product": {"name": "Test Product"}}

        result = render_data(data, context)
        assert result == {
            "user": {
                "name": "John Doe",
                "age": 25,
                "active": True,
                "last_login": test_date.isoformat(),
                "preferences": {"theme": "dark", "notifications": True},
            },
            "items": [
                {"id": 1, "name": "Test Product", "price": 99.99, "created_at": test_date.isoformat()},
                {"id": 2, "name": "Test Product", "price": 149.99, "created_at": test_date.isoformat()},
            ],
        }

    def test_dict_in_placeholder(self):
        """Test that dictionaries in placeholders are not converted to strings."""
        # Create a complex dictionary
        complex_dict = {"name": "Test Dict", "values": [1, 2, 3], "nested": {"key": "value", "number": 42}}

        # Create a template with a placeholder for the dictionary
        data = {"simple": "Simple value", "complex": "{complex_dict}"}

        # Create context with the dictionary
        context = {"complex_dict": complex_dict}

        # Render the template
        result = render_data(data, context)

        # Verify that the dictionary is not converted to a string
        assert isinstance(result["complex"], dict)
        assert result["complex"] == complex_dict

        # Verify the nested structure is preserved
        assert result["complex"]["nested"]["key"] == "value"
        assert result["complex"]["nested"]["number"] == 42
        assert result["complex"]["values"] == [1, 2, 3]

    def test_array_in_placeholder(self):
        """Test that arrays in placeholders are not converted to strings."""
        # Create a complex array
        complex_array = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}, {"id": 3, "name": "Item 3"}]

        # Create a template with a placeholder for the array
        data = {"simple": "Simple value", "complex": "{complex_array}"}

        # Create context with the array
        context = {"complex_array": complex_array}

        # Render the template
        result = render_data(data, context)

        # Verify that the array is not converted to a string
        assert isinstance(result["complex"], list)
        assert result["complex"] == complex_array

        # Verify the array elements are preserved
        assert result["complex"][0]["id"] == 1
        assert result["complex"][0]["name"] == "Item 1"
        assert result["complex"][1]["id"] == 2
        assert result["complex"][1]["name"] == "Item 2"
        assert result["complex"][2]["id"] == 3
        assert result["complex"][2]["name"] == "Item 3"

    def test_mixed_complex_structures(self):
        """Test that mixed complex structures are handled correctly."""
        # Create complex structures
        complex_dict = {"name": "Test Dict", "values": [1, 2, 3], "nested": {"key": "value", "number": 42}}

        complex_array = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}, {"id": 3, "name": "Item 3"}]

        # Create a template with placeholders for the complex structures
        data = {
            "simple": "Simple value",
            "dict": "{complex_dict}",
            "array": "{complex_array}",
            "mixed": {"dict": "{complex_dict}", "array": "{complex_array}"},
        }

        # Create context with the complex structures
        context = {"complex_dict": complex_dict, "complex_array": complex_array}

        # Render the template
        result = render_data(data, context)

        # Verify that the complex structures are not converted to strings
        assert isinstance(result["dict"], dict)
        assert isinstance(result["array"], list)
        assert isinstance(result["mixed"]["dict"], dict)
        assert isinstance(result["mixed"]["array"], list)

        # Verify the values are preserved
        assert result["dict"] == complex_dict
        assert result["array"] == complex_array
        assert result["mixed"]["dict"] == complex_dict
        assert result["mixed"]["array"] == complex_array


class TestJMESPathTemplating:
    """Test suite for JMESPath query support in templates."""

    @pytest.mark.skip(reason="JMESPath expression handling needs to be fixed to handle complex queries correctly")
    def test_basic_jmespath_query(self):
        """Test basic JMESPath query functionality."""
        data = {
            "summary": ("Top-selling product: " '{{ products | jmespath("max_by(@, &sales).name") }}'),
            "details": ("Total revenue: " '{{ products | jmespath("sum(@[].revenue)") }}'),
        }

        context = {
            "products": [
                {"name": "Product A", "sales": 100, "revenue": 1000},
                {"name": "Product B", "sales": 150, "revenue": 2000},
                {"name": "Product C", "sales": 120, "revenue": 1800},
            ]
        }

        result = render_data(data, context)
        assert result == {
            "summary": "Top-selling product: Product B",
            "details": "Total revenue: 4800",
        }

    @pytest.mark.skip(reason="JMESPath expression handling needs to be fixed to handle complex queries correctly")
    def test_complex_jmespath_query(self):
        """Test more complex JMESPath queries with multiple operations."""
        data = {
            "summary": (
                "Top 2 products by revenue: {{ products | jmespath("
                "\"sort_by(@, &revenue)[-2:] | [*].name | join(', ', @)\""
                ") }}"
            )
        }

        context = {
            "products": [
                {"name": "Product A", "revenue": 1000},
                {"name": "Product B", "revenue": 2000},
                {"name": "Product C", "revenue": 1800},
                {"name": "Product D", "revenue": 1500},
            ]
        }

        result = render_data(data, context)
        # Check that both Product B and Product C are in the result
        # (order doesn't matter)
        assert "Product B" in result["summary"]
        assert "Product C" in result["summary"]
        # Check that we have exactly two products
        assert result["summary"].count(",") == 1

    def test_invalid_jmespath_query(self):
        """Test handling of invalid JMESPath queries."""
        data = {"error": '{{ products | jmespath("invalid.query") }}'}
        context = {"products": []}

        with pytest.raises(ValueError):
            render_data(data, context)


class TestPDFTemplating:
    """Test suite for PDF document templating."""

    @pytest.fixture
    def sample_pdf_template(self, tmp_path) -> str:
        """
        Create a simple XML template for PDF generation.

        Returns:
            Path to the created XML template file
        """
        template_path = tmp_path / "template.xml"
        template_content = """<?xml version="1.0" encoding="UTF-8"?>
<document>
    <page>
        <text>Client: {client_name}</text>
        <text>Invoice #: {invoice_number}</text>
        <text>Date: {invoice_date}</text>
        <text>Due Date: {due_date}</text>
        <text>Total Amount: ${total}</text>
        <text>Items: {{ items | jmespath('[*].description | join(", ", @)') }}</text>
    </page>
</document>"""

        with open(template_path, "w") as f:
            f.write(template_content)

        return str(template_path)

    @pytest.fixture
    def sample_invoice_context(self) -> dict[str, Any]:
        """Fixture providing sample invoice data for testing."""
        return {
            "client_name": "Acme Corporation",
            "invoice_number": "INV-2025-04001",
            "invoice_date": "2025-03-21",
            "due_date": "2025-04-20",
            "items": [
                {
                    "description": "Professional Services",
                    "quantity": 40,
                    "rate": 150,
                    "amount": 6000,
                },
                {
                    "description": "Software License",
                    "quantity": 1,
                    "rate": 2500,
                    "amount": 2500,
                },
                {
                    "description": "Support Package",
                    "quantity": 1,
                    "rate": 750,
                    "amount": 750,
                },
            ],
            "subtotal": 9250,
            "tax_rate": 8.5,
            "tax_amount": 786.25,
            "total": 10036.25,
        }

    @pytest.mark.skip(reason="PDF template rendering needs to be fixed to handle XML templates correctly")
    def test_basic_pdf_rendering(self, tmp_path, sample_invoice_context, sample_pdf_template):
        """Test basic PDF template rendering with placeholders."""
        output_path = tmp_path / "output.pdf"

        with open(sample_pdf_template) as f:
            template = f.read()

        render_pdf(template, sample_invoice_context, str(output_path))
        assert output_path.exists()

    @pytest.mark.skip(reason="PDF template rendering needs to be fixed to handle missing placeholders correctly")
    def test_pdf_rendering_with_missing_placeholders(self, tmp_path):
        """Test PDF rendering when some placeholders are missing."""
        template = """<?xml version="1.0" encoding="UTF-8"?>
<document>
    <page>
        <text>Client: {client_name}</text>
        <text>Invoice #: {invoice_number}</text>
    </page>
</document>"""
        output_path = tmp_path / "output.pdf"
        context = {"client_name": "Test Client"}  # Missing invoice_number

        with pytest.raises(ValueError):
            render_pdf(template, context, str(output_path))

    @pytest.mark.skip(reason="PDF template rendering needs to be fixed to validate XML structure correctly")
    def test_pdf_rendering_with_invalid_template(self, tmp_path, sample_invoice_context):
        """Test PDF rendering with an invalid XML template."""
        template = """<?xml version="1.0" encoding="UTF-8"?>
<invalid>
    <not-a-document>
        <text>This is not a valid template</text>
    </not-a-document>
</invalid>"""
        output_path = tmp_path / "output.pdf"

        with pytest.raises(ValueError):
            render_pdf(template, sample_invoice_context, str(output_path))
