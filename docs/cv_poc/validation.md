# CV PoC — validation runbook

Epic: https://github.com/pkuppens/templify/issues/7 · Issue: https://github.com/pkuppens/templify/issues/14

The PoC entrypoint and report generator now exist (`examples/cv_resume_poc/run_poc.py`,
`report.py`, `schema.py`, `render_docx.py`); this runbook reflects the real command and report
sections.

## Preconditions

- [ ] Repository synced; optional CV dependencies installed:
      `uv sync --extra cv-poc`.
- [ ] Sample data: `examples/cv_resume_poc/data/cv_minimal.yaml` and `cv_minimal.json5`.
- [ ] Template: `examples/cv_resume_poc/template/cv_template.docx`.

## Run

1. Run the one-liner, once per data format (same logical content):

   ```bash
   python -m examples.cv_resume_poc.run_poc \
     --template examples/cv_resume_poc/template/cv_template.docx \
     --data examples/cv_resume_poc/data/cv_minimal.yaml \
     --out-docx /tmp/cv_out.docx \
     --report-md /tmp/report.md \
     --strict

   python -m examples.cv_resume_poc.run_poc \
     --template examples/cv_resume_poc/template/cv_template.docx \
     --data examples/cv_resume_poc/data/cv_minimal.json5 \
     --out-docx /tmp/cv_out.docx \
     --report-md /tmp/report.md \
     --strict
   ```

2. Confirm exit code **0** for happy path. `--strict` fails (exit 1) only on missing **required**
   fields per `docs/cv_poc/data_model.md`; unparseable data is always fatal (exit 2) regardless of
   `--strict`.
3. Open output `.docx` in Word or LibreOffice (no repair dialog).

## Outputs to verify

- [ ] **Filled document** matches expected placeholders for the sample (`personalia.naam`,
      `adres`, `linkedin`, and the `telefoon`/`email` loops).
- [ ] **Markdown report** contains sections: Summary; Missing in data; Superfluous in data;
      Optional blocks; Multiplicity; Warnings.

## Edge-case matrix

| Scenario | Input | Expected report section / behaviour |
|----------|-------|-------------------------------------|
| All keys present | Full sample data + matching template | Summary counts zero missing; Optional blocks show "provided" for every optional field |
| Missing optional field | Data without `personalia.linkedin` | **Optional blocks** lists it "not provided"; not fatal, exit 0 even under `--strict` |
| Missing required field | Data without `personalia.naam` | **Missing in data**; exit 1 under `--strict`, exit 0 otherwise |
| Empty list | `telefoon: []` | **Multiplicity** records `personalia.telefoon: 0 entries`; no separate warning |
| Non-list value for a list field | `telefoon: "not-a-list"` | **Warnings** notes the type mismatch; excluded from Multiplicity |
| Extra key in data | Unknown top-level or nested `personalia.*` key | **Superfluous in data** (default ignore list: `schema_version` only) |
| Template doesn't reference a schema root | Template omits `{{ personalia... }}` entirely | **Warnings** notes the unreferenced root (coarse: root-name only, not per field — see `render_docx.py`) |
| UTF-8 Dutch | Names with **é**, **IJ**, etc. | Correct in `.docx` and report (verified manually; no automated fixture assertion yet) |
| JSON5 comments | `cv_minimal.json5` with `//` comments and trailing commas | Parsed to the same structure as the YAML fixture (asserted in `tests/test_run_poc.py::TestLoadData::test_yaml_and_json5_load_to_same_structure`) |

## Sign-off

- [ ] Reviewer name / date
- [ ] Notes
