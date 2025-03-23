# Testing Templify

This document describes how to run tests for the Templify project.

## Prerequisites

- Python 3.12 or higher
- Poetry for dependency management
- pytest for test execution

## Setup

1. Install development dependencies:
   ```bash
   poetry install
   ```

2. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Running Tests

### Run all tests

```bash
pytest
```

### Run specific test files

```bash
pytest tests/test_core.py
pytest tests/test_utils.py
```

### Run tests with coverage report

```bash
pytest --cov=templify
```

### Run tests with verbose output

```bash
pytest -v
```

## Test Structure

- `tests/test_core.py`: Tests for core functionality
- `tests/test_utils.py`: Tests for utility functions
- `tests/fixtures/`: Test data and templates

## Test Data

For PDF tests, a sample template is needed in `tests/fixtures/template.pdf`. This file needs to be added manually.

## Continuous Integration

Tests are automatically executed on GitHub Actions for every push and pull request.
