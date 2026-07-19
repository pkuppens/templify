"""
Standalone CLI entrypoint for the CV PoC (issue #12).

Deliberately not a subcommand of ``src/templify/cli.py`` — see the epic
decision record on issue #7 (all PoC code lives under
``examples/cv_resume_poc/``; templify's own CLI stays untouched).

Usage::

    python -m examples.cv_resume_poc.run_poc \\
        --template examples/cv_resume_poc/template/cv_template.docx \\
        --data examples/cv_resume_poc/data/cv_minimal.yaml \\
        --out-docx /tmp/cv_out.docx \\
        --report-md /tmp/report.md \\
        --strict
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from examples.cv_resume_poc.render_docx import get_template_variables, render_docx
from examples.cv_resume_poc.report import ValidationReport, build_report


def load_data(data_path: Path) -> dict[str, Any]:
    """Load YAML or JSON5 data based on file extension.

    Raises ``ValueError`` on an unrecognized extension or unparseable content
    — this is always fatal, regardless of ``--strict``, since nothing else
    can proceed without valid data.
    """
    text = data_path.read_text(encoding="utf-8")
    suffix = data_path.suffix.lower()

    try:
        if suffix in (".yaml", ".yml"):
            import yaml

            loaded: dict[str, Any] = yaml.safe_load(text) or {}
            return loaded
        if suffix in (".json5", ".json"):
            import json5

            parsed: dict[str, Any] = json5.loads(text)
            return parsed
    except Exception as exc:
        raise ValueError(f"Could not parse {data_path} as {suffix}: {exc}") from exc

    raise ValueError(f"Unrecognized data file extension: {suffix} (expected .yaml, .yml, .json5, or .json)")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render the CV PoC Word document and/or validation report.")
    parser.add_argument("--template", type=Path, required=True, help="Path to the .docx template.")
    parser.add_argument("--data", type=Path, required=True, help="Path to YAML or JSON5 data.")
    parser.add_argument("--out-docx", type=Path, default=None, help="Where to write the rendered .docx (optional).")
    parser.add_argument("--report-md", type=Path, default=None, help="Where to write the markdown report (default: stdout).")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if required fields are missing from data (in addition to unparseable data, always fatal).",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    try:
        data = load_data(args.data)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    template_vars = get_template_variables(args.template)
    report: ValidationReport = build_report(data, template_vars=template_vars)

    if args.out_docx is not None:
        render_docx(args.template, data, args.out_docx)

    report_text = report.to_markdown()
    if args.report_md is not None:
        args.report_md.parent.mkdir(parents=True, exist_ok=True)
        args.report_md.write_text(report_text, encoding="utf-8")
    else:
        print(report_text)

    if args.strict and not report.is_valid:
        print(f"error: missing required field(s): {', '.join(report.missing_required)}", file=sys.stderr)
        return 1

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
