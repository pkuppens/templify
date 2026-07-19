`cv_template.docx` is the minimal Word template for the CV PoC (issue #11). It uses docxtpl/Jinja2 placeholders under the `personalia` block, aligned with `docs/cv_poc/data_model.md` and the sample data in `../data/`:

- `{{ personalia.naam }}`, `{{ personalia.adres }}`, `{{ personalia.linkedin }}`
- `{% for t in personalia.telefoon %}...{% endfor %}` and the equivalent loop over `personalia.email` (both 0..n lists)

Regenerate it with `python-docx` if it needs to change; there is no separate generator script checked in since it is a one-off fixture.
