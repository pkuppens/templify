"""Tests for the run_poc.py CLI entrypoint (issue #12 / #13)."""
from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("docxtpl")
pytest.importorskip("yaml")
pytest.importorskip("json5")

from examples.cv_resume_poc.run_poc import build_arg_parser, load_data, run

TEMPLATE_PATH = Path(__file__).parent.parent / "template" / "cv_template.docx"
YAML_DATA_PATH = Path(__file__).parent.parent / "data" / "cv_minimal.yaml"
JSON5_DATA_PATH = Path(__file__).parent.parent / "data" / "cv_minimal.json5"


class TestLoadData:
    def test_loads_yaml(self) -> None:
        data = load_data(YAML_DATA_PATH)
        assert data["personalia"]["naam"] == "Jan de Vries"

    def test_loads_json5(self) -> None:
        data = load_data(JSON5_DATA_PATH)
        assert data["personalia"]["naam"] == "Jan de Vries"

    def test_yaml_and_json5_load_to_same_structure(self) -> None:
        assert load_data(YAML_DATA_PATH) == load_data(JSON5_DATA_PATH)

    def test_unparseable_yaml_raises(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.yaml"
        bad.write_text("key: [unclosed", encoding="utf-8")
        with pytest.raises(ValueError, match="Could not parse"):
            load_data(bad)

    def test_unrecognized_extension_raises(self, tmp_path: Path) -> None:
        bad = tmp_path / "data.txt"
        bad.write_text("naam: Jan", encoding="utf-8")
        with pytest.raises(ValueError, match="Unrecognized data file extension"):
            load_data(bad)


class TestRunHappyPath:
    def test_full_data_strict_exits_zero(self, tmp_path: Path) -> None:
        parser = build_arg_parser()
        out_docx = tmp_path / "out.docx"
        report_md = tmp_path / "report.md"
        args = parser.parse_args(
            [
                "--template",
                str(TEMPLATE_PATH),
                "--data",
                str(YAML_DATA_PATH),
                "--out-docx",
                str(out_docx),
                "--report-md",
                str(report_md),
                "--strict",
            ]
        )

        exit_code = run(args)

        assert exit_code == 0
        assert out_docx.exists()
        assert "Missing required: 0" in report_md.read_text(encoding="utf-8")


class TestRunStrictGate:
    def test_missing_required_field_exits_nonzero_under_strict(self, tmp_path: Path) -> None:
        data_path = tmp_path / "bad.yaml"
        data_path.write_text('personalia:\n  adres: "x"\n', encoding="utf-8")
        parser = build_arg_parser()
        args = parser.parse_args(["--template", str(TEMPLATE_PATH), "--data", str(data_path), "--strict"])

        assert run(args) == 1

    def test_missing_required_field_exits_zero_without_strict(self, tmp_path: Path) -> None:
        data_path = tmp_path / "bad.yaml"
        data_path.write_text('personalia:\n  adres: "x"\n', encoding="utf-8")
        parser = build_arg_parser()
        args = parser.parse_args(["--template", str(TEMPLATE_PATH), "--data", str(data_path)])

        assert run(args) == 0

    def test_superfluous_key_stays_informational_under_strict(self, tmp_path: Path) -> None:
        data_path = tmp_path / "extra.yaml"
        data_path.write_text('personalia:\n  naam: "Jan"\nextra_top: 1\n', encoding="utf-8")
        parser = build_arg_parser()
        args = parser.parse_args(["--template", str(TEMPLATE_PATH), "--data", str(data_path), "--strict"])

        assert run(args) == 0

    def test_unparseable_data_exits_nonzero_without_strict(self, tmp_path: Path) -> None:
        data_path = tmp_path / "bad.yaml"
        data_path.write_text("key: [unclosed", encoding="utf-8")
        parser = build_arg_parser()
        args = parser.parse_args(["--template", str(TEMPLATE_PATH), "--data", str(data_path)])

        assert run(args) == 2
