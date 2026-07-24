"""DOCX rendering smoke test (issue #11 / #13).

Marked slow and skipped when docxtpl is not installed, so core CI does not
require the optional Word-rendering dependency (the ``cv-poc`` extra in
``pyproject.toml``, installed via ``uv sync --extra cv-poc``).
"""
from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("docxtpl")
yaml = pytest.importorskip("yaml")

pytestmark = pytest.mark.slow

TEMPLATE_PATH = Path(__file__).parent.parent / "template" / "cv_template.docx"
DATA_PATH = Path(__file__).parent.parent / "data" / "cv_minimal.yaml"


def test_render_docx_produces_output_file(tmp_path: Path) -> None:
    from examples.cv_resume_poc.render_docx import render_docx

    data = yaml.safe_load(DATA_PATH.read_text(encoding="utf-8"))
    out = tmp_path / "cv_out.docx"

    render_docx(TEMPLATE_PATH, data, out)

    assert out.exists()
    assert out.stat().st_size > 0


def test_get_template_variables_reports_personalia_root() -> None:
    from examples.cv_resume_poc.render_docx import get_template_variables

    assert get_template_variables(TEMPLATE_PATH) == {"personalia"}
