# CV PoC — validation runbook

Epic: https://github.com/pkuppens/templify/issues/7 · Issue: https://github.com/pkuppens/templify/issues/14

Use this checklist when the PoC entrypoint and report generator exist. Until then, steps marked *future* are placeholders.

## Preconditions

- [ ] Repository synced; optional CV dependencies installed per `README` / `pyproject` group.
- [ ] Sample data: `examples/cv_resume_poc/data/cv_minimal.yaml` and `cv_minimal.json5`.

## Run (future)

1. Run the documented one-liner (e.g. `run_poc.py` or CLI) with:
   - `--data` pointing to YAML **and** once to JSON5 (same logical content).
   - A Word template path when available.
2. Confirm exit code **0** for happy path.
3. Open output `.docx` in Word or LibreOffice (no repair dialog).

## Outputs to verify

- [ ] **Filled document** matches expected placeholders for the sample.
- [ ] **Markdown report** contains sections: Summary; Missing in data; Superfluous in data; Optional blocks; Multiplicity; Warnings.

## Edge-case matrix

| Scenario | Input | Expected report section / behaviour |
|----------|-------|-------------------------------------|
| All keys present | Full sample data + matching template | Summary counts zero missing; Optional blocks show “provided” where applicable |
| Missing optional field | Data without `personalia.linkedin` | Missing or Optional (per design); not fatal if optional |
| Missing required field | Data without `personalia.naam` | **Missing in data**; exit non-zero if `--strict` |
| Empty list | `telefoon: []` | **Multiplicity** or Warnings; document policy |
| Extra key in data | Unknown top-level key | **Superfluous in data** |
| Duplicate placeholder in template | Same token twice | No crash; count in Summary if implemented |
| UTF-8 Dutch | Names with **é**, **IJ**, etc. | Correct in `.docx` and report |
| JSON5 comments | `cv_minimal.json5` with `//` comments | Parsed same as YAML; **Warnings** may note comments stripped post-parse |

## Sign-off

- [ ] Reviewer name / date
- [ ] Notes
