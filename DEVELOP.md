# Development Guide

This guide will help you set up your development environment for Templify.

## Prerequisites

### Python 3.12+

#### Windows
1. Download Python 3.12 from the [official Python website](https://www.python.org/downloads/)
2. Run the installer
3. Make sure to check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   ```

#### Ubuntu/Debian
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv
```

#### macOS
```bash
brew install python@3.12
```

### Poetry

#### Windows
```bash
winget install poetry
```

#### Ubuntu/Debian
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### macOS
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Verify Installation

```bash
python --version  # Should show Python 3.12.x
poetry --version  # Should show Poetry version 1.8.3 or higher
```

## Project Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/pkuppens/templify.git
   cd templify
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=templify

# Run specific test file
pytest tests/test_core.py
```

### Code Quality

The project uses several tools to maintain code quality:

- `ruff` for linting - replaces flake8, isort, and black
- `mypy` for type checking

Run all checks:
```bash
# Format code
black .

# Run linter
ruff check .

# Type checking
mypy .
```

### Project Structure

```
templify/
├── src/
│   └── templify/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
│   ├── test_core.py
│   ├── test_utils.py
│   └── fixtures/
├── docs/
├── pyproject.toml
└── README.md
```

## Common Issues

### Windows-specific

1. If `poetry` command is not found after installation:
   - Add Poetry to PATH: `%APPDATA%\Python\Scripts`
   - Restart your terminal

2. If Python 3.12 is not found:
   - Verify Python installation in System Settings > Apps
   - Check PATH environment variable

### Unix/macOS-specific

1. If Poetry installation fails:
   ```bash
   # Try installing with pip
   pip install poetry
   ```

2. If Python 3.12 is not found:
   ```bash
   # On Ubuntu/Debian
   sudo apt install python3.12-venv

   # On macOS
   brew link python@3.12
   ```

## Getting Help

- Check the [GitHub Issues](https://github.com/pkuppens/templify/issues)
- Join our [Discussions](https://github.com/pkuppens/templify/discussions)
- Contact the maintainers

## Additional Information

- [README.md](README.md)
- [INSTALL.md](INSTALL.md)
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)
