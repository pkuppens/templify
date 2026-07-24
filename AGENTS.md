## Agent skills

### Code intelligence (CodeGraph)

This repo is indexed by [CodeGraph](https://github.com/colbymchenry/codegraph) — a local
SQLite knowledge graph of every symbol, edge, and file, kept under `.codegraph/`. Reach for it
BEFORE grep/find or reading files to understand or locate code:

- **MCP tool** (when available): `codegraph_explore` — give it symbol names or a natural-language
  question and it returns the relevant symbols' verbatim source plus the call paths between them
  (including dynamic-dispatch hops grep can't follow), in one call.
- **Shell** (always works): `codegraph explore "<symbol names or question>"` prints the same
  output. Other useful subcommands: `codegraph status` (index health), `codegraph query <search>`,
  `codegraph callers|callees|impact <symbol>`, `codegraph affected [files...]`.

**Maintenance**: `.codegraph/` is machine-local and gitignored (via its own nested
`.codegraph/.gitignore` — never remove that file or add exceptions for the database/log/pid
files it excludes). A background daemon keeps the index in sync with file changes (~1s lag); if
`codegraph status` reports the index as stale or missing, run `codegraph sync` to catch up or
`codegraph index` to rebuild from scratch. Each contributor/agent environment needs its own
index — there's nothing to share or commit.

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
