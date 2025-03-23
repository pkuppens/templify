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

## Quick Start

```python
from templify import render_text

template = "Hello, {name}! You have {count} new messages."
context = {"name": "Alice", "count": 5}
result = render_text(template, context)
# Result: "Hello, Alice! You have 5 new messages."
```

## Installation

```bash
pip install templify
```

## Documentation Sections

- [Getting Started](guides/quickstart.md) - Quick start guide and basic usage
- [Installation](guides/installation.md) - Detailed installation instructions
- [Templates](guides/templates.md) - Template formats and syntax
- [Advanced Usage](guides/advanced.md) - Advanced features and patterns
- [API Reference](api/core.md) - Complete API documentation
- [Development](development/contributing.md) - Contributing guidelines
- [Architecture](development/architecture.md) - System design and components
- [Requirements](reference/requirements.md) - Project requirements
- [Changelog](reference/changelog.md) - Version history and changes

## Examples

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
"""

context = {
    "user": {
        "name": "Alice",
        "is_admin": True,
        "recent_activities": [
            {"type": "login", "description": "Logged in from Chrome"},
            {"type": "edit", "description": "Updated profile"}
        ]
    }
}
result = render_jinja2(template, context)
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](development/contributing.md) for details.

## License

MIT License - see [LICENSE](LICENSE) for details.
