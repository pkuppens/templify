# Testing Templify

This document describes how to run tests for the Templify project.

## Prerequisites

- Python 3.11-3.14 (3.13/3.14 fully tested)
- uv for dependency management (never `poetry` or bare `pip install`)
- pytest for test execution

## Setup

1. Install development dependencies:
   ```bash
   uv sync --group dev
   ```

2. Run commands inside the environment with `uv run <command>`.

## Running Tests

### Run all tests

```bash
uv run pytest
```

### Run specific test files

```bash
uv run pytest tests/test_core.py
uv run pytest tests/test_utils.py
```

### Run tests with coverage report

```bash
uv run pytest --cov=templify
```

### Run tests with verbose output

```bash
uv run pytest -v
```

## Test Structure

- `tests/test_core.py`: Tests for core functionality
- `tests/test_utils.py`: Tests for utility functions
- `tests/fixtures/`: Test data and templates

## Test Data

For PDF tests, a sample template is needed in `tests/fixtures/template.pdf`. This file needs to be added manually.

## Continuous Integration

Tests are automatically executed on GitHub Actions for every push and pull request.
