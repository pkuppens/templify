# Templify

Templify simplifies advanced templating features.
- templating within complex data structures
- more advanced placeholders (JMESPath)
- various output types, including binary formats like PDF.

## Problem Description

Common templating tools like Jinja2 don't support:

- Recursive placeholder replacement in data structures, including nested dictionaries and arrays.
- Advanced data queries, such as those provided by JMESPath.
- Direct binary output generation, e.g., PDF documents.

Templify addresses these gaps with a clean and easy-to-use library interface.

## Business Value

- **Easy PDF Generation**: Quickly create complex documents without manual formatting.
- **Data Object Templating**: Automate filling placeholders deeply nested within data structures.
- **Advanced Query Support**: Seamlessly integrate powerful queries to fetch and fill data.

## Technical Examples

### Example: Render Text Templates

    template = 'Welcome, {user.name}! You have {user.notifications} new messages.'
    context = {
        'user': {'name': 'Alice', 'notifications': 5}
    }

    message = templify.render_text(template, context)

**Output:**

    Welcome, Alice! You have 5 new messages.

### Example: Render Recursive Data Structures

    data = {
        'report': {
            'title': 'Sales for {month}',
            'summary': 'Total units sold: {sales.total}'
        },
        'generated_on': '{date}'
    }

    context = {
        'month': 'March',
        'sales': {'total': 1500},
        'date': '2025-04-01'
    }

    output = templify.render_data(data, context)

**Output:**

    {
        'report': {
            'title': 'Sales for March',
            'summary': 'Total units sold: 1500'
        },
        'generated_on': '2025-04-01'
    }

### Example: Advanced Query with JMESPath

    data = {
        'summary': 'Top-selling product: {{ products | jmespath("max_by(@, &sales).name") }}',
        'details': 'Total revenue: {{ products | jmespath("sum(@[].revenue)") }}'
    }

    context = {
        'products': [
            {'name': 'Product A', 'sales': 100, 'revenue': 1000},
            {'name': 'Product B', 'sales': 150, 'revenue': 2000},
            {'name': 'Product C', 'sales': 120, 'revenue': 1800}
        ]
    }

    output = templify.render_data(data, context)

**Output:**

    {
        'summary': 'Top-selling product: Product B',
        'details': 'Total revenue: 4800'
    }

### Example: Render Binary Documents (PDF)

    import templify

    # Define your data context with values to insert into the template
    context = {
        'client_name': 'Acme Corporation',
        'invoice_number': 'INV-2025-04001',
        'invoice_date': '2025-03-21',
        'due_date': '2025-04-20',
        'items': [
            {'description': 'Professional Services', 'quantity': 40, 'rate': 150, 'amount': 6000},
            {'description': 'Software License', 'quantity': 1, 'rate': 2500, 'amount': 2500},
            {'description': 'Support Package', 'quantity': 1, 'rate': 750, 'amount': 750}
        ],
        'subtotal': 9250,
        'tax_rate': 8.5,
        'tax_amount': 786.25,
        'total': 10036.25
    }

    # Load the PDF template and fill in the placeholders
    templify.render_pdf_file(
        template_path='template_with_placeholders.pdf',  # Path to source PDF with placeholders
        output_path='filled_document.pdf',               # Path where the filled PDF will be saved
        context=context,                                 # Data context containing values for placeholders
        overwrite=True                                   # Optional: overwrite existing output file if it exists
    )

    print("PDF document successfully generated at 'filled_document.pdf'")

**Output:**

Binary PDF file was save in the specified output_path.

## Project Design

Templify uses modern Python development best practices and tooling:

- **Python Version**: Python 3.12+
- **Package Management**: `poetry`
- **Testing**: `pytest`
- **Code Quality**:
    - Formatting: `black`
    - Linting: `ruff`, `flake8`
    - Typing: `mypy`
- **CI/CD & Deployment**:
    - GitHub Actions (CI/CD, automated testing, releases)
    - Automated deployment to PyPI on release tags
- **Documentation**:
    - Hosted via GitHub Pages
- **Directory Structure**:

      templify/
      ├── src/
      │   └── templify/
      │       ├── __init__.py
      │       ├── core.py
      │       └── utils.py
      ├── tests/
      ├── docs/
      ├── pyproject.toml
      └── README.md

## Licensing

Templify is released under the **MIT License**, allowing free use, including commercial projects.

## Sponsorship

You can sponsor ongoing Templify development via [GitHub Sponsors](https://github.com/sponsors/) or
contact the author directly for consultancy and tailored support.

## Contributing

Please see our [Contribution Guidelines](CONTRIBUTING.md) to get involved.
