# CV resume PoC (synthetic fixtures)

Epic: https://github.com/pkuppens/templify/issues/7

This folder holds **minimal, synthetic** sample data for the Dutch CV proof of concept. Replace or extend with anonymized real templates from your environment when available.

## Layout

| Path | Purpose |
|------|---------|
| `data/cv_minimal.yaml` | Same logical content as JSON5 (YAML) |
| `data/cv_minimal.json5` | Same content with JSON5 comments and trailing comma |
| `template/` | Word `.docx` template with placeholders (add under implementation issues) |

Data files use UTF-8 and Dutch field names under `personalia`.
