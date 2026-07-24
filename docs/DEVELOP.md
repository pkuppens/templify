# Development Guide

This guide will help you set up your development environment for Templify.

## Prerequisites

### Python 3.13+

Templify supports Python 3.11-3.14; 3.13 and 3.14 are the primary, fully-tested
versions. Use the newest of those for local development.

#### Windows
1. Download Python 3.13 from the [official Python website](https://www.python.org/downloads/)
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
sudo apt install python3.13 python3.13-venv
```

#### macOS
```bash
brew install python@3.13
```

### uv

Templify uses [uv](https://docs.astral.sh/uv/) for package management — never `poetry` or bare `pip install`.

#### Windows
```bash
winget install astral-sh.uv
```

#### Ubuntu/Debian and macOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Verify Installation

```bash
python --version  # Should show Python 3.13.x (or 3.14.x)
uv --version       # Should show a recent uv version
```

## Project Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/pkuppens/templify.git
   cd templify
   ```

2. Install dependencies:
   ```bash
   uv sync --group dev
   ```

3. Run commands inside the environment with `uv run <command>` (e.g. `uv run pytest`), or activate
   the `.venv` uv creates in-project.

## Development Workflow

### Running Tests

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=templify

# Run specific test file
uv run pytest tests/test_core.py
```

### Code Quality

The project uses several tools to maintain code quality:
- Ruff for linting and code formatting - replaces black, flake8, and isort
- MyPy for type checking

Run all checks:
```bash
# Run linter and formatter
uv run ruff check .

# Type checking
uv run mypy
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

1. If `uv` command is not found after installation:
   - Add uv to PATH: `%USERPROFILE%\.local\bin`
   - Restart your terminal

2. If Python 3.13 is not found:
   - Verify Python installation in System Settings > Apps
   - Check PATH environment variable

### Unix/macOS-specific

1. If the uv installer fails:
   ```bash
   # Try installing with pip
   pip install uv
   ```

2. If Python 3.13 is not found:
   ```bash
   # On Ubuntu/Debian
   sudo apt install python3.13-venv

   # On macOS
   brew link python@3.13
   ```

## Getting Help

- Check the [GitHub Issues](https://github.com/pkuppens/templify/issues)
- Join our [Issues](https://github.com/pkuppens/templify/issues)
- Contact the maintainers

## Additional Information

See the [Home](index.md) for more information about the project.

- [INSTALL.md](INSTALL.md)
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)
