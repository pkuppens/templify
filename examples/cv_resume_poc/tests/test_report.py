"""Unit tests for the CV PoC mismatch/report logic (issue #10)."""
from __future__ import annotations

from examples.cv_resume_poc.report import build_report
from examples.cv_resume_poc.schema import CV_SCHEMA

FULL_DATA = {
    "schema_version": "0.1",
    "personalia": {
        "naam": "Jan de Vries",
        "adres": "1234 AB Utrecht",
        "telefoon": ["+31 6 12345678"],
        "email": ["jan.devries@voorbeeld.nl"],
        "linkedin": "https://linkedin.com/in/example",
    },
}


class TestBuildReportHappyPath:
    def test_full_data_no_missing_required(self) -> None:
        report = build_report(FULL_DATA)
        assert report.missing_required == []
        assert report.is_valid

    def test_full_data_all_optional_provided(self) -> None:
        report = build_report(FULL_DATA)
        assert set(report.provided_optional) == {
            "schema_version",
            "personalia.adres",
            "personalia.telefoon",
            "personalia.email",
            "personalia.linkedin",
        }
        assert report.missing_optional == []

    def test_full_data_no_superfluous(self) -> None:
        assert build_report(FULL_DATA).superfluous == []

    def test_multiplicity_counts(self) -> None:
        report = build_report(FULL_DATA)
        assert report.multiplicity == {"personalia.telefoon": 1, "personalia.email": 1}


class TestBuildReportMissingRequired:
    def test_missing_naam_is_flagged_and_invalid(self) -> None:
        data = {"personalia": {"adres": "x"}}
        report = build_report(data)
        assert report.missing_required == ["personalia.naam"]
        assert not report.is_valid

    def test_missing_naam_when_personalia_absent(self) -> None:
        report = build_report({})
        assert "personalia.naam" in report.missing_required


class TestBuildReportOptionalAndMultiplicity:
    def test_missing_optional_field_not_fatal(self) -> None:
        data = {"personalia": {"naam": "Jan"}}
        report = build_report(data)
        assert report.is_valid
        assert "personalia.linkedin" in report.missing_optional

    def test_empty_list_recorded_as_zero_count(self) -> None:
        data = {"personalia": {"naam": "Jan", "telefoon": []}}
        report = build_report(data)
        assert report.multiplicity["personalia.telefoon"] == 0

    def test_non_list_value_for_list_field_warns(self) -> None:
        data = {"personalia": {"naam": "Jan", "telefoon": "not-a-list"}}
        report = build_report(data)
        assert any("personalia.telefoon" in w for w in report.warnings)
        assert "personalia.telefoon" not in report.multiplicity


class TestBuildReportSuperfluous:
    def test_extra_top_level_key_flagged(self) -> None:
        data = {"personalia": {"naam": "Jan"}, "extra_top": 1}
        report = build_report(data)
        assert "extra_top" in report.superfluous

    def test_extra_nested_personalia_key_flagged(self) -> None:
        data = {"personalia": {"naam": "Jan", "extra_nested": "x"}}
        report = build_report(data)
        assert "personalia.extra_nested" in report.superfluous

    def test_schema_version_ignored_by_default(self) -> None:
        data = {"schema_version": "0.1", "personalia": {"naam": "Jan"}}
        report = build_report(data)
        assert "schema_version" not in report.superfluous


class TestBuildReportTemplateReference:
    def test_unreferenced_root_warns(self) -> None:
        report = build_report(FULL_DATA, template_vars=set())
        assert any("personalia" in w for w in report.warnings)

    def test_referenced_root_no_warning(self) -> None:
        report = build_report(FULL_DATA, template_vars={"personalia", "schema_version"})
        assert not any("does not reference" in w for w in report.warnings)


class TestValidationReportMarkdown:
    def test_to_markdown_contains_expected_sections(self) -> None:
        report = build_report(FULL_DATA)
        md = report.to_markdown()
        for heading in ("Summary", "Missing in data", "Superfluous in data", "Optional blocks", "Multiplicity", "Warnings"):
            assert f"## {heading}" in md

    def test_schema_constant_matches_data_model_field_count(self) -> None:
        assert len(CV_SCHEMA) == 6
