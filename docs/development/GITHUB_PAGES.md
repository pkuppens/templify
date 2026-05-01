# GitHub Pages documentation

## Overview

Published documentation is **built with [MkDocs](https://www.mkdocs.org/)** from Markdown under [`docs/`](../index.md) and [`mkdocs.yml`](https://github.com/pkuppens/templify/blob/main/mkdocs.yml). GitHub Actions uploads the generated static site (`site/` after a build) to GitHub Pages using **`actions/deploy-pages`** — not Jekyll rendering repo Markdown on its own.

## Published site

For this repository the usual Pages URL is:

**https://pkuppens.github.io/templify/**

Confirm in GitHub: **Repository → Settings → Pages** (custom domain overrides this). After each deployment, the **Documentation** workflow log prints `Deployment URL: …`.

## When CI builds and deploys

Workflow file: [`.github/workflows/docs.yml`](https://github.com/pkuppens/templify/blob/main/.github/workflows/docs.yml).

- **Automatic:** push to **`main`** that changes `docs/**`, `mkdocs.yml`, `pyproject.toml`, `poetry.lock`, or `.github/workflows/docs.yml`.
- **Manual:** **Actions → Documentation → Run workflow** (`workflow_dispatch`). Choose the branch to build from when you run it.

Production deploy uses the **`github-pages`** Pages environment.

## Local preview

Install development dependencies (see [`pyproject.toml`](https://github.com/pkuppens/templify/blob/main/pyproject.toml)), then:

- **Serve:** `mkdocs serve` — live reload while editing.
- **Build:** `mkdocs build --strict` — writes static files to **`site/`** (same layout CI deploys).

CI currently uses Poetry (`poetry install --with dev` and `poetry run mkdocs build --strict`). Locally you can use the same or your usual tool (for example `uv`) as long as MkDocs and plugins from `pyproject.toml` are installed.

## Source vs generated output

| Location | Role |
|----------|------|
| `docs/`, `mkdocs.yml` | **Source** — edit here only. |
| `site/` | **Build output** — local only; ignored by Git. |
| GitHub Pages | **Hosted** snapshot from the latest successful **Documentation** workflow deploy. |

## Legacy `gh-pages` branch

Some repositories still have a **`gh-pages` branch** with old “deploy commits” from earlier tooling (for example workflows that pushed the `site/` tree to that branch).

This project’s active workflow deploys via **artifacts and `deploy-pages`**, which does **not** require that branch. If **`origin/gh-pages`** still exists, treat it as **historical**:

- Do **not** merge `gh-pages` into `main`.
- Prefer **repository Settings → Pages** to see what source is configured (typically **GitHub Actions**).

## Optional git safeguards

[`scripts/setup-git-config.sh`](https://github.com/pkuppens/templify/blob/main/scripts/setup-git-config.sh) sets local preferences (for example `--no-ff` on `main`, `--ff-only` on `gh-pages`) so accidental merges involving a legacy Pages branch are less likely.

If your copy of that script sets `branch.main.mergeFilter` to `git-merge-filter-gh-pages`, remove that line unless you install matching helper tooling — **that executable is not part of this repository** and breaks merges if missing.

You can extend protection with branch rules on GitHub or a **`pre-merge-commit`** hook; those are optional and not required for MkDocs deployments.

## Best practices

1. Edit documentation under `docs/` on feature branches; merge to `main` to trigger CI when touched paths match the workflow filters (or run the workflow manually from your branch).
2. Use relative links inside docs where possible; run **`mkdocs build --strict`** locally before pushing.
3. Keep docs changes in Git with application code releases when it matters for readers.

## Further reading

- [GitHub Pages](https://docs.github.com/en/pages)
- [Deploying MkDocs-built sites via GitHub Actions](https://docs.github.com/en/actions/guides/publishing-docs-with-github-pages)
- [MkDocs documentation](https://www.mkdocs.org/)
