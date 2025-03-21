"""
Tests for core functionality
"""
from templify import render_data, render_pdf_file, render_text


def test_render_text():
    """Test basic text template rendering"""
    template = "Welcome, {user.name}! You have {user.notifications} new messages."
    context = {"user": {"name": "Alice", "notifications": 5}}

    result = render_text(template, context)
    assert result == "Welcome, Alice! You have 5 new messages."


def test_render_data():
    """Test recursive data structure rendering"""
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


def test_render_data_with_jmespath():
    """Test data rendering with JMESPath expressions"""
    data = {
        "summary": 'Top-selling product: '
                   '{{ products | jmespath("max_by(@, &sales).name") }}',
        "details": 'Total revenue: '
        '{{ products | jmespath("sum(@[].revenue)") }}',
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


def test_render_pdf_file(tmp_path):
    """Test PDF template rendering"""
    template_path = "tests/fixtures/template.pdf"
    output_path = tmp_path / "output.pdf"

    context = {
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

    render_pdf_file(template_path, str(output_path), context)
    assert output_path.exists()
