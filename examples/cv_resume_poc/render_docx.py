"""
Render the CV PoC Word template from a data context (issue #11).

Templify's ``render_data`` preprocesses the context dict (JMESPath
expressions, ``{placeholder}`` substitution, missing-key policy) before the
result is handed to docxtpl's own Jinja2 rendering of the ``.docx``
template. PDF output is out of scope for this round (see
``docs/cv_poc/alternatives-to-templify.md``).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from docxtpl import DocxTemplate

from templify.core import MissingKeyHandling, render_data


def get_template_variables(template_path: Path) -> set[str]:
    """Root variable names the ``.docx`` template references (docxtpl introspection)."""
    return DocxTemplate(str(template_path)).get_undeclared_template_variables()


def render_docx(
    template_path: Path,
    data: dict[str, Any],
    output_path: Path,
    handle_missing: MissingKeyHandling = MissingKeyHandling.KEEP,
) -> None:
    """Render ``template_path`` with ``data`` (preprocessed via ``render_data``) to ``output_path``."""
    context = render_data(data, data, handle_missing)
    tpl = DocxTemplate(str(template_path))
    tpl.render(context)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tpl.save(str(output_path))
