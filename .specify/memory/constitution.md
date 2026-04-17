<!--
SYNC IMPACT REPORT
==================
Version change: (none) → 1.0.0 (initial ratification — all content was placeholder)
Modified principles: N/A (first version)
Added sections:
  - I. Pipeline Purity
  - II. Library-First
  - III. Schema Contract
  - IV. Security by Default
  - V. Test Discipline
  - VI. Backwards Compatibility
  - Technology Constraints
  - Development Workflow
  - Governance
Removed sections: N/A
Templates requiring updates:
  ✅ .specify/templates/plan-template.md — Constitution Check section aligns with all six principles
  ✅ .specify/templates/spec-template.md — Requirements section aligns with schema/security/compat principles
  ✅ .specify/templates/tasks-template.md — Task structure aligns with test-first discipline and story independence
Deferred items: None. All placeholders resolved.
-->

# graphify Constitution

## Core Principles

### I. Pipeline Purity (NON-NEGOTIABLE)

Each pipeline stage MUST be a single, pure function in its own module.
Stages communicate only through plain Python dicts and `nx.Graph` objects —
no shared module-level state, no database connections held across stages,
no side effects outside `graphify-out/`.

- Stage functions: `collect_files`, `extract`, `build_graph`, `cluster`,
  `analyze`, `render_report`, `export` — one function per module, one
  responsibility per function.
- New pipeline stages MUST fit this pattern; multi-responsibility modules
  are a constitution violation requiring explicit justification.
- Functions that produce side effects (file writes, network calls) MUST be
  isolated in dedicated helpers (`cache.py`, `security.py`, `ingest.py`)
  and MUST NOT be embedded in pipeline stage functions.

### II. Library-First

Every capability MUST be importable as a Python function before it is
exposed via CLI or skill orchestration.

- `graphify/__init__.py` uses lazy imports (`__getattr__` + `_map`) so
  `graphify install` works before heavy dependencies (tree-sitter, scipy,
  graspologic) are installed. New public functions MUST be added to `_map`.
- CLI (`__main__.py`) and `skill.md` MUST call library functions — they
  MUST NOT re-implement logic already in the library.
- New features MUST be testable via direct Python import without invoking
  the CLI or the skill.

### III. Schema Contract (NON-NEGOTIABLE)

All data entering `build_graph()` MUST pass `validate_extraction()` first.
No exceptions.

- Every extractor MUST return exactly:
  ```
  {"nodes": [{id, label, source_file, source_location}],
   "edges": [{source, target, relation, confidence}]}
  ```
- Confidence labels are the controlled vocabulary: `EXTRACTED`, `INFERRED`,
  `AMBIGUOUS`. No other values are valid.
- New extractors MUST validate their output against this schema in tests
  before the extractor is wired into `extract()`.
- Cross-repo edge dicts (meta-graph) MUST include `discovery` and
  `confidence_score` fields in addition to the base schema fields.

### IV. Security by Default (NON-NEGOTIABLE)

All external input MUST pass through `graphify/security.py` before use.

- URLs → `validate_url()` (http/https only; blocks `file://` redirects).
- File paths from external callers → `validate_graph_path()` (must resolve
  inside `graphify-out/`).
- Node labels before HTML rendering → `sanitize_label()` (strips control
  chars, HTML-escapes, caps at 256 chars).
- New input surfaces (CLI flags, API params, config files) MUST add
  corresponding validation in `security.py` before shipping.
- Security checks MUST NOT be skipped via optional flags or fallback paths.

### V. Test Discipline

One test file per module, under `tests/`. Tests MUST be pure unit tests:
no network calls, no file-system side effects outside `pytest`'s `tmp_path`.

- New modules MUST ship with a corresponding `tests/test_<module>.py`.
- New language extractors MUST include a fixture file in `tests/fixtures/`
  and language-specific tests in `tests/test_languages.py`.
- Tests for schema-producing code (extractors, cross-repo edge discovery)
  MUST assert the output passes `validate_extraction()` or the relevant
  schema check.
- `pytest tests/ -q` MUST pass with zero failures before any PR is merged.
  CI enforces Python 3.10 and 3.12.

### VI. Backwards Compatibility

Public API and output formats MUST not break existing callers without a
major version bump and explicit migration guidance.

- Functions in `graphify/__init__.py`'s `_map` are public API. Parameters
  MUST be added with defaults; existing parameter semantics MUST NOT change.
- `detect_incremental(root: Path)` callers (single path) MUST continue to
  work unchanged after any signature extension (e.g., `Path | list[Path]`).
- `graph.json` node-link format, `manifest.json` mtime format, and
  `GRAPH_REPORT.md` section headings are stable output contracts. Changes
  require explicit versioning in the file or a migration note in CHANGELOG.
- The `--update` CLI flag MUST continue to work as an explicit override
  even after auto-detect is introduced.

## Technology Constraints

- **Python**: 3.10+ (`requires-python = ">=3.10"`). No 3.11+ exclusive
  syntax (no `ExceptionGroup`, no `tomllib` stdlib usage without compat shim).
  Use `from __future__ import annotations` for forward references.
- **Graph library**: NetworkX. `nx.Graph` (undirected) is the default;
  `nx.DiGraph` only when edge direction must be preserved for export/analysis.
- **AST extraction**: tree-sitter. Adding a language means adding its
  tree-sitter package to `pyproject.toml` — no custom parsers.
- **Clustering**: graspologic Leiden preferred; python-louvain as fallback.
  Do not add a third clustering backend without removing one.
- **Config files**: `repos.yaml` uses PyYAML. No additional config file
  formats (TOML, INI) without deprecating the YAML path.
- **No database**: All state is files on disk under `graphify-out/`.
  No SQLite, no Redis, no external stores.

## Development Workflow

- All new modules follow the pipeline purity pattern: single function,
  plain dict/graph I/O, no shared state.
- New public API functions MUST be added to `graphify/__init__.py`'s `_map`
  before the PR is merged.
- CHANGELOG entries are required for every user-visible change.
- Skill files (`skill.md` and platform variants) MUST be kept in sync when
  the Python library API changes. The skill is the primary user-facing
  interface for Claude Code users.
- Multi-repo features MUST remain opt-in: absence of `repos.yaml` MUST
  result in unchanged single-repo behaviour.

## Governance

This constitution supersedes all other project practices where they conflict.

- **Amendments**: Any change to a principle (including additions, removals,
  or rewordings) MUST increment the version (`MINOR` for additions/expansions,
  `MAJOR` for removals or principle redefinitions, `PATCH` for wording fixes).
- **Compliance**: Every PR that introduces a new module, new extractor, or new
  public API function MUST explicitly pass the Constitution Check in its
  `plan.md` before implementation begins.
- **Violations**: If a principle MUST be violated, the violation MUST be
  documented in the `Complexity Tracking` table of `plan.md` with rationale
  and the simpler alternative that was rejected.
- **Runtime guidance**: `CLAUDE.md` (project root) is the runtime development
  guide for AI assistants. It MUST stay consistent with this constitution.
  When the constitution is amended, `CLAUDE.md` MUST be reviewed for drift.

**Version**: 1.0.0 | **Ratified**: 2026-04-16 | **Last Amended**: 2026-04-16
