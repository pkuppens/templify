# ADR-001: Non-mutating JSON/object masking for safe logging

**Status**: Accepted
**Date**: 2026-04-14
**Deciders**: Project maintainers
**Related**: [`src/templify/utils.py`](https://github.com/pkuppens/templify/blob/main/src/templify/utils.py) (`mask_value_for_keys`), [issue #6](https://github.com/pkuppens/templify/issues/6)

## Context and problem statement

Templify needs a small helper to produce **log-safe** snapshots of nested `dict`/`list` data (and JSON text) so that secrets and identifiers such as passwords or patient names are not written in plain text to logs, debug output, or support bundles.

Callers often pass the **same** objects they use for real work (request bodies, template context). If masking **mutated** those objects in place, the running process could lose secrets for later steps, or shared mutable structures could be corrupted in hard-to-reproduce ways. The library must make a clear contract: callers can pass live objects without side effects.

An earlier sketch used mutable holder objects; that made it easy to alter shared state by accident. The chosen API is a **pure function** on plain `dict` / `list` / JSON text instead.

## Behavior for nested dict and list values

The helper walks only **`dict` and `list`** (plus a top-level **`str`** that is valid JSON, handled via parse → walk → serialize):

- **`dict`**: Builds a **new** dict with the same keys. For each key, if its lowercased name is in the configured mask set, the value is replaced by the mask string; otherwise the value is processed recursively. Nested dicts inside lists are masked the same way when the walk reaches them.
- **`list`**: Builds a **new** list. Each element is processed recursively. List positions are not named, so redaction applies only to **values of keys** in nested dicts, not to “which list index” something sits at.
- **Other values** (including **`tuple`**, numbers, string values nested inside dicts/lists, and arbitrary objects): returned **unchanged** by reference—there is no deep walk through tuples or custom types. Only a **top-level** string is parsed as JSON when it is valid JSON; string leaves in nested structures are not re-parsed.

So typical nested payloads (`dict` of `dict`s, `list` of `dict`s) are fully covered; tuples and non-JSON structures are not recursively traversed.

## Decision drivers

- **Correctness**: No accidental removal of secrets from live application state.
- **Predictability** and **testability**: Pure function behaviour; easy to assert “original unchanged, masked copy returned.”
- **Alignment** with common “sanitize for display” patterns (not encryption).
- **Privacy / safe logging expectations**: Support teams and developers who copy-paste structured data without leaking sensitive fields.

## Considered options

1. **Non-mutating (return new nested structures)** — Recursively build new `dict`/`list` containers and substitute mask values for matching keys; for JSON strings, `json.loads` → mask → `json.dumps`.
2. **In-place mutation** — Walk the same objects and overwrite values for keys that match.
3. **`copy.deepcopy` then in-place mask** — Deep copy first, then mutate the copy only (still avoids mutating the caller’s input, but allocates a full copy up front).

## Decision outcome

**Chosen option: (1)** — recursive **non-mutating** construction with fresh containers along the walk. JSON string input: on successful parse, return a **new** string; on parse failure, return the original string unchanged.

**Rationale**: Option (1) avoids mutating the input without paying for a full `deepcopy` of every leaf when only building new containers along the path. Option (2) is rejected because it violates the requirement to keep live objects intact. Option (3) is a valid alternative but adds extra memory and cost for typical logging volumes; the recursive fresh-build in (1) is sufficient.

## Consequences

### Positive consequences

- **Safe to call with live request/context objects**; originals remain unchanged.
- **Tests** can assert identity and values on the input after masking.
- **Clear API** for use at call sites or from a future logging filter that calls the same helper.

### Negative consequences

- **Extra allocations** compared to in-place mutation (mitigation: intended for logging/debug, not hot paths; callers should not mask in tight loops on huge trees without profiling).

### Neutral / follow-up

- **Centralized redaction** (e.g. `logging` filters, structured logging processors) remains an **application** responsibility; this library supplies the **primitive** (`mask_value_for_keys`). Teams may combine both: central pipeline for consistency, explicit calls where needed.

## Pros and cons of the options

### Option 1 (chosen)

- Preserves caller input; predictable; test-friendly.
- No full-tree `deepcopy` unless needed later for other reasons.
- Cost: allocates new dict/list nodes along the path.

### Option 2

- Fewer allocations.
- **Rejected**: breaks live objects and shared mutable state.

### Option 3

- Preserves caller input.
- **Rejected for default**: heavier than necessary; can be revisited if profiling shows a need.
