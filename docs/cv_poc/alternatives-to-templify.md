# Alternatives to Templify for “template + data → document”

Epic: https://github.com/pkuppens/templify/issues/7 · Issue: https://github.com/pkuppens/templify/issues/9

This note compares **templating stacks** for structured documents—not Word engine choice (`python-docx` vs `docxtpl` is a separate implementation detail for `.docx`).

## Templify (this repo)

**Relevant APIs:** `render_data`, `render_text`, `render_jinja2`, `MissingKeyHandling` in [`src/templify/core.py`](../../src/templify/core.py).

| Strength | Notes |
|----------|--------|
| Recursive dict/list templates | `render_data` walks structures and replaces `{placeholders}` and Jinja/JMESPath segments in strings. |
| Missing-key policy | `KEEP`, `DEFAULT`, `RAISE` shared across text/data/Jinja paths (behaviour differs slightly for Jinja vs plain placeholders). |
| JMESPath in strings | Useful for summaries over arrays without custom code. |
| Jinja2 bridge | `render_jinja2` wraps `Environment` with loaders, custom filters, undefined classes per policy. |

**Gaps / caveats (re-validated against current tree):**

| Area | Detail |
|------|--------|
| **CLI** | [`src/templify/cli.py`](../../src/templify/cli.py) exposes `render` / `validate` but does **not** implement them (stub). |
| **DOCX** | No first-class `.docx` pipeline; CV PoC will add integration (python-docx / docxtpl / etc.) **alongside** templify for merge logic. |
| **PDF** | `render_pdf` expects XML-ish structure after `render_data`, then only `<text>` tags become ReportLab `Paragraph`s—**narrow** layout model, not a general Word replacement. |
| **“Single `render` router”** | [`docs/development/architecture.md`](../../docs/development/architecture.md) describes a unified `render()`; the **exported** API remains separate functions (`render_data`, `render_jinja2`, …). |

## Jinja2-only

Use **`jinja2.Environment`** directly: loaders, globals, filters, **StrictUndefined** / **undefined** choices, templates on disk.

| vs Templify | |
|-------------|--|
| **Pros** | Mature ecosystem, IDE support, inheritance/includes, large community. |
| **Cons** | No built-in **recursive `render_data`** over JSON payloads; you combine Jinja with custom glue. Templify adds that glue plus JMESPath-in-string patterns. |

**When to prefer Jinja2-only:** mostly free-form text/HTML documents with file templates and no need for recursive JSON template trees.

## Mako

Fast, Python-centric. Heavier security/process story for untrusted templates. Less common for document pipelines than Jinja2 in Python—reasonable for code generation, not the default for CV PoC.

## docxtpl

**Role:** embed **Jinja2** inside Word documents—not an alternative to Templify’s *entire* model, but a **delivery** option when placeholders live in `.docx`. Often used as **Templify + docxtpl**: build context dict in Python (optionally via `render_data`-style preprocessing), then `docxtpl` renders the Word file.

## PDF paths

| Option | When |
|--------|------|
| Existing **`render_pdf`** | PoC spike for “same XML template → PDF” only; limited tag subset. |
| HTML → PDF (weasyprint, etc.) | Not in repo today; add only if layout requirements justify new deps. |
| Duplicate PDF from Word | Export from Word/LibreOffice manually—out of scope for automation in minimal PoC. |

## “What’s new” (lightweight scan, 2024–2026)

Template engines in Python are still dominated by **Jinja2**; **StrictUndefined** and environment config remain the main control levers. Niche “document merge” tools exist per vendor (Office, Google); nothing broadly replaces a small library + `python-docx` for on-prem CV generation without evaluating licence and format lock-in.

## Recommendation for this CV PoC

- **Keep Templify** for **data-side** templating (recursive structures, missing-key policy, optional JMESPath) and for **report generation** strings.
- **Add** a dedicated **Word** integration (e.g. docxtpl or python-docx) for `.docx` output; treat it as **transport**, not a replacement for Templify’s `render_data`.
- **Revisit** if the PoC only needs **flat** Jinja files + HTML—then Jinja2-only plus a static site generator could be simpler, but that is **not** the Word + JSON5/YAML epic scope.
