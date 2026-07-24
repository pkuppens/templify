## Agent skills

### Package management

Use **uv** for all dependency management, virtualenvs, builds, and running project commands
(`uv sync`, `uv run <command>`, `uv build`, `uv lock`). Never use `poetry` or bare `pip install` —
poetry support was removed in favor of uv. Supported Python versions are 3.11-3.14; 3.13 and 3.14
are the primary, fully-tested versions (see `pyproject.toml`'s `requires-python` and the CI matrix
in `.github/workflows/ci.yml`).

### Issue tracker

Issues live in GitHub Issues (pkuppens/templify). See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context layout — `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
