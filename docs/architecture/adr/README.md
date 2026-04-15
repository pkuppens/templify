# Architecture Decision Records (ADR)

Design decisions for Templify are recorded here so rationales stay traceable as the codebase evolves.

## Authoring guidelines

- **When to add an ADR**: Use an ADR when a choice affects structure, behaviour, or maintenance of the library (API contracts, security or privacy patterns, performance trade-offs). Skip an ADR for trivial refactors with no lasting decision.
- **Location and naming**: One file per decision under this directory: `NNN-short-kebab-title.md` (sequential number, three digits, check the index below for the next free number).
- **Structure**: Follow the template used in existing ADRs—at minimum: title, **Status**, **Date**, **Deciders**, **Related** links, **Context and problem statement**, **Decision drivers**, **Considered options**, **Decision outcome**, **Consequences**, and **Pros and cons of the options** where helpful.
- **Status values**: Use **Proposed**, **Accepted**, **Deprecated**, or **Superseded** (and point to the replacing ADR when superseded).
- **Immutability**: Do not rewrite the narrative of an **Accepted** ADR to change the decision; add a new ADR that **supersedes** it and update this index.
- **Index**: Add a row to the table below for every new ADR file.

## Index

| ADR | Title |
|-----|--------|
| [ADR-001](001-json-masking-non-mutating.md) | Non-mutating JSON/object masking for safe logging |
