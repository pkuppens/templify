"""
Test fixtures for Jinja2 templates.
"""
from datetime import datetime
from typing import Any

# Basic template with variable replacement
BASIC_TEMPLATE = """
Hello, {{ name }}!
Your account balance is ${{ balance }}.
"""

# Template with control structures
CONTROL_TEMPLATE = """
{% if user.is_admin %}
    Welcome, Administrator {{ user.name }}!
{% else %}
    Welcome, {{ user.name }}!
{% endif %}

{% if user.notifications > 0 %}
    You have {{ user.notifications }} new notifications.
{% endif %}
"""

# Template with loops
LOOP_TEMPLATE = """
Your recent activity:
{% for activity in user.recent_activities %}
    - {{ activity.type }}: {{ activity.description }}
    {% if activity.timestamp %}
        ({{ activity.timestamp | datetime }})
    {% endif %}
{% endfor %}

{% if user.tasks %}
    Pending tasks:
    {% for task in user.tasks %}
        * {{ task.title }} (Due: {{ task.due_date | datetime }})
    {% endfor %}
{% endif %}
"""

# Template with macros
MACRO_TEMPLATE = """
{% macro format_date(date) %}
    {{ date.strftime('%Y-%m-%d') }}
{% endmacro %}

{% macro format_currency(amount) %}
    ${{ "%.2f"|format(amount) }}
{% endmacro %}

Invoice Details:
Date: {{ format_date(invoice.date) }}
Amount: {{ format_currency(invoice.amount) }}
"""

# Template with inheritance
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Default Title{% endblock %}</title>
    <style>
        {% block style %}{% endblock %}
    </style>
</head>
<body>
    <header>
        {% block header %}
        <h1>{{ site_title }}</h1>
        {% endblock %}
    </header>
    <main>
        {% block content %}
        Default content
        {% endblock %}
    </main>
    <footer>
        {% block footer %}
        <p>&copy; {{ year }} {{ site_title }}</p>
        {% endblock %}
    </footer>
</body>
</html>
"""

CHILD_TEMPLATE = """
{% extends "base.html" %}

{% block title %}User Dashboard{% endblock %}

{% block style %}
    .dashboard { padding: 20px; }
    .metric { margin: 10px 0; }
{% endblock %}

{% block content %}
    <div class="dashboard">
        <h2>Welcome, {{ user.name }}!</h2>
        <div class="metrics">
            {% for metric, value in metrics.items() %}
            <div class="metric">
                <strong>{{ metric | replace('_', ' ') | title }}:</strong>
                {{ value }}
            </div>
            {% endfor %}
        </div>
    </div>
{% endblock %}
"""

# Complex template combining multiple features
COMPLEX_TEMPLATE = """
{% macro format_date(date) %}
    {{ date.strftime('%Y-%m-%d %H:%M') }}
{% endmacro %}

{% macro format_currency(amount) %}
    ${{ "%.2f"|format(amount) }}
{% endmacro %}

<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Admin Dashboard{% endblock %}</title>
    <style>
        .admin-panel { padding: 20px; }
        .metric { margin: 10px 0; }
        .activity-list { list-style: none; padding: 0; }
        .activity-item { margin: 10px 0; padding: 10px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    {% if user.is_admin %}
    <div class="admin-panel">
        <h1>Admin Dashboard</h1>
        <p>Welcome back, {{ user.name }}!</p>

        <h2>Recent Activity</h2>
        <ul class="activity-list">
        {% for activity in user.recent_activities %}
            <li class="activity-item">
                <strong>{{ activity.type | title }}:</strong>
                {{ activity.description }}
                <span class="timestamp">{{ format_date(activity.timestamp) }}</span>
            </li>
        {% endfor %}
        </ul>

        <h2>System Status</h2>
        <div class="metrics">
            {% for metric, value in system_metrics.items() %}
            <div class="metric">
                <strong>{{ metric | replace('_', ' ') | title }}:</strong>
                {{ value }}
            </div>
            {% endfor %}
        </div>

        <h2>Financial Summary</h2>
        <table>
            <tr>
                <th>Period</th>
                <th>Revenue</th>
                <th>Expenses</th>
                <th>Net</th>
            </tr>
            {% for period in financial_data %}
            <tr>
                <td>{{ period.name }}</td>
                <td>{{ format_currency(period.revenue) }}</td>
                <td>{{ format_currency(period.expenses) }}</td>
                <td>{{ format_currency(period.revenue - period.expenses) }}</td>
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
</body>
</html>
"""

# Sample context data for testing
SAMPLE_CONTEXT: dict[str, Any] = {
    "name": "Alice",
    "balance": 1234.56,
    "user": {
        "name": "Alice",
        "is_admin": True,
        "notifications": 5,
        "recent_activities": [
            {"type": "login", "description": "Logged in from Chrome", "timestamp": datetime(2025, 3, 21, 10, 30)},
            {"type": "edit", "description": "Updated profile", "timestamp": datetime(2025, 3, 21, 11, 15)},
        ],
        "tasks": [
            {"title": "Review monthly report", "due_date": datetime(2025, 3, 25)},
            {"title": "Update documentation", "due_date": datetime(2025, 3, 28)},
        ],
    },
    "invoice": {"date": datetime(2025, 3, 21), "amount": 1234.56},
    "site_title": "My Dashboard",
    "year": 2025,
    "metrics": {"cpu_usage": "45%", "memory_usage": "2.3GB", "disk_space": "156GB"},
    "system_metrics": {"cpu_usage": "45%", "memory_usage": "2.3GB", "disk_space": "156GB"},
    "financial_data": [
        {"name": "Q1 2025", "revenue": 50000.00, "expenses": 35000.00},
        {"name": "Q2 2025", "revenue": 75000.00, "expenses": 40000.00},
    ],
}
