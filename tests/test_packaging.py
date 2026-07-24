"""Guards for the uv package-management migration (poetry -> uv).

Asserts the repo's packaging metadata stays uv/hatchling-based and doesn't
regress back to poetry, and that the supported Python range matches the
CI matrix.
"""
from __future__ import annotations

import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_pyproject() -> dict:
    with (REPO_ROOT / "pyproject.toml").open("rb") as f:
        return tomllib.load(f)


def test_no_poetry_table():
    pyproject = _load_pyproject()
    assert "poetry" not in pyproject.get("tool", {})


def test_build_backend_is_hatchling():
    pyproject = _load_pyproject()
    build_system = pyproject["build-system"]
    assert build_system["build-backend"] == "hatchling.build"
    assert any(req.startswith("hatchling") for req in build_system["requires"])


def test_requires_python_matches_supported_range():
    pyproject = _load_pyproject()
    assert pyproject["project"]["requires-python"] == ">=3.11,<4.0"


def test_cv_poc_extra_defined():
    pyproject = _load_pyproject()
    extras = pyproject["project"]["optional-dependencies"]
    assert "cv-poc" in extras
    assert any(dep.startswith("docxtpl") for dep in extras["cv-poc"])


def test_no_poetry_lock_files():
    assert not (REPO_ROOT / "poetry.lock").exists()
    assert not (REPO_ROOT / "poetry.toml").exists()


def test_uv_lock_present():
    assert (REPO_ROOT / "uv.lock").exists()


def test_no_requirements_extra_txt():
    assert not (REPO_ROOT / "examples" / "cv_resume_poc" / "requirements-extra.txt").exists()
