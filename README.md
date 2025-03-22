# Templify

A powerful templating library that supports multiple template formats and data structures.

## Features

- Text template rendering with placeholders
- Recursive data structure templating
- JMESPath query support for complex data transformations
- Full Jinja2 template support including:
  - Control structures (if/else, for loops)
  - Template inheritance and includes
  - Filters and macros
  - Custom filters and extensions
- PDF document templating (coming soon)

## Installation

```bash
pip install templify
```

## Usage

### Basic Text Templates

```python
from templify import render_text

template = "Hello, {name}! You have {count} new messages."
context = {"name": "Alice", "count": 5}
result = render_text(template, context)
# Result: "Hello, Alice! You have 5 new messages."
```

### Data Structure Templates

```python
from templify import render_data

template = {
    "user": {
        "name": "{name}",
        "email": "{email}"
    },
    "settings": {
        "theme": "{theme}",
        "notifications": "{notifications}"
    }
}
context = {
    "name": "Alice",
    "email": "alice@example.com",
    "theme": "dark",
    "notifications": True
}
result = render_data(template, context)
```

### JMESPath Queries

```python
from templify import render_data

template = {
    "summary": 'Top product: {{ products | jmespath("max_by(@, &sales).name") }}',
    "total": 'Revenue: {{ products | jmespath("sum(@[].revenue)") }}'
}
context = {
    "products": [
        {"name": "Product A", "sales": 100, "revenue": 1000},
        {"name": "Product B", "sales": 150, "revenue": 2000}
    ]
}
result = render_data(template, context)
```

### Jinja2 Templates

```python
from templify import render_jinja2

template = """
{% if user.is_admin %}
    Welcome, Administrator {{ user.name }}!
{% else %}
    Welcome, {{ user.name }}!
{% endif %}

Your recent activity:
{% for activity in user.recent_activities %}
    - {{ activity.type }}: {{ activity.description }}
{% endfor %}

{% macro format_date(date) %}
    {{ date.strftime('%Y-%m-%d') }}
{% endmacro %}

Last login: {{ format_date(user.last_login) }}
"""

context = {
    "user": {
        "name": "Alice",
        "is_admin": True,
        "recent_activities": [
            {"type": "login", "description": "Logged in from Chrome"},
            {"type": "edit", "description": "Updated profile"}
        ],
        "last_login": datetime.now()
    }
}
result = render_jinja2(template, context)
```

## Development

### Setup

1. Clone the repository
2. Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
3. Install dependencies: `poetry install`
4. Activate the virtual environment: `poetry shell`

### Running Tests

```bash
pytest
```

### Code Style

This project uses:
- Black for code formatting
- Ruff for linting
- MyPy for type checking

Run pre-commit hooks to ensure code quality:
```bash
pre-commit run --all-files
```

## License

MIT License
