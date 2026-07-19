"""
Mismatch/validation report for the CV PoC (issue #10).

Compares a data dict against ``CV_SCHEMA`` (required/optional, multiplicity)
and, informationally, against the set of root variable names a Word template
references (``docxtpl.DocxTemplate.get_undeclared_template_variables()``).

Known limitation: Jinja/docxtpl variable discovery only reports **root**
names for attribute access (``personalia.naam`` shows up as just
``personalia``), so template-reference checks in this report operate at the
root-field granularity, not per leaf field. Required/optional and
multiplicity checks do not have this limitation since they read the data
directly.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from examples.cv_resume_poc.schema import CV_SCHEMA, DEFAULT_SUPERFLUOUS_IGNORE, FieldSpec


def _get_by_path(data: dict[str, Any], path: str) -> tuple[bool, Any]:
    """Return (present, value) for a dotted path into nested dicts."""
    current: Any = data
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return False, None
        current = current[key]
    return True, current


def _root_name(path: str) -> str:
    return path.split(".", 1)[0]


def _allowed_children(schema: tuple[FieldSpec, ...]) -> dict[str, set[str]]:
    """Map each parent path (``""`` for the root) to its allowed child keys."""
    allowed: dict[str, set[str]] = {}
    for spec in schema:
        parts = spec.path.split(".")
        for i in range(len(parts)):
            parent = ".".join(parts[:i])
            allowed.setdefault(parent, set()).add(parts[i])
    return allowed


def _find_superfluous(data: dict[str, Any], schema: tuple[FieldSpec, ...], ignore: frozenset[str]) -> list[str]:
    allowed = _allowed_children(schema)
    superfluous: list[str] = []

    def _walk(node: Any, path: str) -> None:
        if not isinstance(node, dict):
            return
        known = allowed.get(path)
        if known is None:
            return
        for key in node:
            if key in ignore or key in known:
                child_path = f"{path}.{key}" if path else key
                if key in known:
                    _walk(node[key], child_path)
                continue
            child_path = f"{path}.{key}" if path else key
            superfluous.append(child_path)

    _walk(data, "")
    return superfluous


@dataclass
class ValidationReport:
    """Structured result of checking data (and optionally a template) against ``CV_SCHEMA``."""

    missing_required: list[str] = field(default_factory=list)
    missing_optional: list[str] = field(default_factory=list)
    provided_optional: list[str] = field(default_factory=list)
    superfluous: list[str] = field(default_factory=list)
    multiplicity: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """True when there are no missing required fields (the ``--strict`` gate)."""
        return not self.missing_required

    def to_markdown(self) -> str:
        lines: list[str] = ["# CV PoC validation report", ""]

        lines.append("## Summary")
        lines.append(f"- Missing required: {len(self.missing_required)}")
        lines.append(f"- Superfluous in data: {len(self.superfluous)}")
        lines.append(f"- Optional fields provided: {len(self.provided_optional)}")
        lines.append(f"- Optional fields missing: {len(self.missing_optional)}")
        lines.append("")

        lines.append("## Missing in data")
        if self.missing_required:
            lines.extend(f"- `{p}` (required)" for p in self.missing_required)
        else:
            lines.append("- None")
        lines.append("")

        lines.append("## Superfluous in data")
        if self.superfluous:
            lines.extend(f"- `{p}`" for p in self.superfluous)
        else:
            lines.append("- None")
        lines.append("")

        lines.append("## Optional blocks")
        if self.provided_optional or self.missing_optional:
            lines.extend(f"- `{p}`: provided" for p in self.provided_optional)
            lines.extend(f"- `{p}`: not provided" for p in self.missing_optional)
        else:
            lines.append("- None")
        lines.append("")

        lines.append("## Multiplicity")
        if self.multiplicity:
            lines.extend(f"- `{p}`: {count} entries" for p, count in self.multiplicity.items())
        else:
            lines.append("- None")
        lines.append("")

        lines.append("## Warnings")
        if self.warnings:
            lines.extend(f"- {w}" for w in self.warnings)
        else:
            lines.append("- None")
        lines.append("")

        return "\n".join(lines)


def build_report(
    data: dict[str, Any],
    template_vars: set[str] | None = None,
    schema: tuple[FieldSpec, ...] = CV_SCHEMA,
    ignore_superfluous: frozenset[str] = DEFAULT_SUPERFLUOUS_IGNORE,
) -> ValidationReport:
    """Check ``data`` against ``schema``, optionally cross-referencing a template's root variables."""
    report = ValidationReport()

    for spec in schema:
        present, value = _get_by_path(data, spec.path)
        if not present:
            if spec.required:
                report.missing_required.append(spec.path)
            else:
                report.missing_optional.append(spec.path)
            continue

        if not spec.required:
            report.provided_optional.append(spec.path)

        if spec.multiplicity == "list":
            if isinstance(value, list):
                report.multiplicity[spec.path] = len(value)
            else:
                report.warnings.append(f"`{spec.path}` expected a list, got {type(value).__name__}")

    report.superfluous = _find_superfluous(data, schema, ignore_superfluous)

    if template_vars is not None:
        referenced_roots = template_vars
        schema_roots = {_root_name(spec.path) for spec in schema}
        unreferenced = sorted(schema_roots - referenced_roots)
        if unreferenced:
            report.warnings.append(
                "Template does not reference root(s): " + ", ".join(f"`{r}`" for r in unreferenced) +
                " (note: template-reference checks only see root variable names, not individual fields)"
            )

    return report
