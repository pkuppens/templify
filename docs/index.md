# Templify Documentation

Welcome to the Templify documentation! This guide will help you understand and use the Templify library effectively.

## Overview

Templify is a powerful templating library that supports multiple template formats and data structures. It provides a unified API for handling various template types, from simple text templates to complex data structures.

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

For installation and basic usage, see the [Installation Guide](INSTALL.md).

## Documentation Sections

- [Development Guide](DEVELOP.md) - Development setup and guidelines
- [Contributing](development/contributing.md) - Contributing guidelines
- [Architecture](development/architecture.md) - System design and components
- [Requirements](reference/requirements.md) - Project requirements
- [Implementation Plan](IMPLEMENTATION_PLAN.md) - Project roadmap and implementation details

## Examples

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
    "summary": '{% raw %}Top product: {{ products | jmespath("max_by(@, &sales).name") }}{% endraw %}',
    "total": '{% raw %}Revenue: {{ products | jmespath("sum(@[].revenue)") }}{% endraw %}'
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
{% raw %}
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
{% endraw %}
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

## Contributing

We welcome contributions! Please see our [Contributing Guide](development/contributing.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
