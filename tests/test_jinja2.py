"""
Tests for Jinja2 template rendering functionality.
"""
from datetime import datetime

import pytest

from templify import render_jinja2


class TestJinja2Templating:
    """Test suite for Jinja2 template rendering functionality."""

    def test_basic_variable_replacement(self):
        """Test basic variable replacement in Jinja2 templates."""
        template = "Hello, {{ name }}!"
        context = {"name": "Alice"}

        result = render_jinja2(template, context)
        assert result == "Hello, Alice!"

    def test_control_structures(self):
        """Test if/else control structures in Jinja2 templates."""
        template = """
        {% if user.is_admin %}
            Welcome, Administrator {{ user.name }}!
        {% else %}
            Welcome, {{ user.name }}!
        {% endif %}
        """
        context = {
            "user": {
                "name": "Alice",
                "is_admin": True
            }
        }

        result = render_jinja2(template, context)
        assert "Welcome, Administrator Alice!" in result

    def test_loops(self):
        """Test for loops in Jinja2 templates."""
        template = """
        Your recent activity:
        {% for activity in user.recent_activities %}
            - {{ activity.type }}: {{ activity.description }}
        {% endfor %}
        """
        context = {
            "user": {
                "recent_activities": [
                    {"type": "login", "description": "Logged in from Chrome"},
                    {"type": "edit", "description": "Updated profile"}
                ]
            }
        }

        result = render_jinja2(template, context)
        assert "- login: Logged in from Chrome" in result
        assert "- edit: Updated profile" in result

    def test_macros(self):
        """Test macro definitions and usage in Jinja2 templates."""
        template = """
        {% macro format_date(date) %}
            {{ date.strftime('%Y-%m-%d') }}
        {% endmacro %}

        Last login: {{ format_date(user.last_login) }}
        """
        context = {
            "user": {
                "last_login": datetime(2025, 3, 21)
            }
        }

        result = render_jinja2(template, context)
        assert "Last login: 2025-03-21" in result

    def test_template_inheritance(self):
        """Test template inheritance in Jinja2 templates."""
        base_template = """
        {% block content %}
        Default content
        {% endblock %}
        """
        child_template = """
        {% extends "base.html" %}
        {% block content %}
        Custom content: {{ message }}
        {% endblock %}
        """
        context = {"message": "Hello, World!"}

        result = render_jinja2(child_template, context, templates={
            "base.html": base_template
        })
        assert "Custom content: Hello, World!" in result

    def test_filters(self):
        """Test built-in and custom filters in Jinja2 templates."""
        template = """
        {{ text | upper }}
        {{ number | round(2) }}
        {{ items | length }}
        """
        context = {
            "text": "hello",
            "number": 3.14159,
            "items": [1, 2, 3, 4, 5]
        }

        result = render_jinja2(template, context)
        assert "HELLO" in result
        assert "3.14" in result
        assert "5" in result

    def test_complex_template(self):
        """Test a complex template combining multiple Jinja2 features."""
        template = """
        {% if user.is_admin %}
            <div class="admin-panel">
                <h1>Admin Dashboard</h1>
                <p>Welcome back, {{ user.name }}!</p>

                <h2>Recent Activity</h2>
                <ul>
                {% for activity in user.recent_activities %}
                    <li class="{{ activity.type }}">
                        {{ activity.type | title }}: {{ activity.description }}
                        <span class="timestamp">{{ activity.timestamp | datetime }}</span>
                    </li>
                {% endfor %}
                </ul>

                <h2>System Status</h2>
                <table>
                    <tr>
                        <th>Metric</th>
                        <th>Value</th>
                    </tr>
                    {% for metric, value in system_metrics.items() %}
                    <tr>
                        <td>{{ metric | replace('_', ' ') | title }}</td>
                        <td>{{ value }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
        {% else %}
            <div class="user-panel">
                <h1>Welcome, {{ user.name }}!</h1>
                <p>You have {{ user.notifications | default(0) }} new notifications.</p>
            </div>
        {% endif %}
        """
        context = {
            "user": {
                "name": "Alice",
                "is_admin": True,
                "recent_activities": [
                    {
                        "type": "login",
                        "description": "Logged in from Chrome",
                        "timestamp": datetime(2025, 3, 21, 10, 30)
                    },
                    {
                        "type": "edit",
                        "description": "Updated profile",
                        "timestamp": datetime(2025, 3, 21, 11, 15)
                    }
                ],
                "notifications": 5
            },
            "system_metrics": {
                "cpu_usage": "45%",
                "memory_usage": "2.3GB",
                "disk_space": "156GB"
            }
        }

        result = render_jinja2(template, context)
        assert "Admin Dashboard" in result
        assert "Alice" in result
        assert "Login" in result
        assert "Edit" in result
        assert "Cpu Usage" in result
        assert "45%" in result

    def test_error_handling(self):
        """Test error handling in Jinja2 templates."""
        template = "{{ undefined_variable }}"
        context = {}

        with pytest.raises(ValueError):
            render_jinja2(template, context)

    def test_custom_filters(self):
        """Test custom filter registration and usage."""
        def reverse_string(s: str) -> str:
            return s[::-1]

        template = "{{ text | reverse }}"
        context = {"text": "hello"}
        filters = {"reverse": reverse_string}

        result = render_jinja2(template, context, filters=filters)
        assert result == "olleh"
