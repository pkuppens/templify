# CV PoC — canonical data model (NL)

This document defines the **logical** resume data used by the CV proof of concept. **YAML** and **JSON5** files must load to the same nested structure (see `examples/cv_resume_poc/data/`).

Epic: https://github.com/pkuppens/templify/issues/7 · Issue: https://github.com/pkuppens/templify/issues/8

## Versioning

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | string | Document format version (e.g. `0.1`). Optional for early PoC; recommend setting once CLI validates. |

## Personalia (`personalia`)

Contact and identity block. Field names are **Dutch** to match typical CV conventions.

| Field | Type | Optionality | Multiplicity |
|-------|------|-------------|--------------|
| `naam` | string | required | single |
| `adres` | string | optional | single |
| `telefoon` | list of string | optional | 0..n |
| `email` | list of string | optional | 0..n |
| `linkedin` | string (URI) | optional | single |

Nested lists allow multiple phone numbers or emails without repeating field names.

## Optional sections (future)

The PoC may add `ervaring`, `opleiding`, etc. Add rows here when templates reference them.

## Example shape (YAML)

See `examples/cv_resume_poc/data/cv_minimal.yaml`.

## Example shape (JSON5)

See `examples/cv_resume_poc/data/cv_minimal.json5` (comments allowed; parsed object must match YAML).

## Template vs data

- **Data file**: this structure (JSON5 or YAML).
- **Word template**: placeholders agreed with implementation (e.g. Jinja-style `{{ personalia.naam }}` or project-specific tokens). The mismatch report (issue #10) will compare **template keys** to **data paths**.
