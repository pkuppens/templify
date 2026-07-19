"""
Canonical CV PoC schema constant.

A small hand-written source of truth for required/optional and multiplicity,
manually kept in sync with ``docs/cv_poc/data_model.md``. Deliberately not a
JSON Schema file or Pydantic model — see issue #10 and the epic decision
record on issue #7 for why.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Multiplicity = Literal["single", "list"]


@dataclass(frozen=True)
class FieldSpec:
    """One row of the canonical schema: a dotted data path and its rules."""

    path: str
    required: bool
    multiplicity: Multiplicity


CV_SCHEMA: tuple[FieldSpec, ...] = (
    FieldSpec("schema_version", required=False, multiplicity="single"),
    FieldSpec("personalia.naam", required=True, multiplicity="single"),
    FieldSpec("personalia.adres", required=False, multiplicity="single"),
    FieldSpec("personalia.telefoon", required=False, multiplicity="list"),
    FieldSpec("personalia.email", required=False, multiplicity="list"),
    FieldSpec("personalia.linkedin", required=False, multiplicity="single"),
)

# Keys ignored when scanning data for superfluous (unknown) entries.
DEFAULT_SUPERFLUOUS_IGNORE: frozenset[str] = frozenset({"schema_version"})
