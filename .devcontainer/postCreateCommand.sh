#! /usr/bin/env bash

# Install Dependencies
uv sync --group dev

# Install pre-commit hooks
uv run pre-commit install --install-hooks
