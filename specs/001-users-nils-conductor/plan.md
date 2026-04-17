# Implementation Plan: Graphify Fork — Multi-Repo + Doc Pipeline Integration

**Branch**: `001-users-nils-conductor` | **Date**: 2026-04-16 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/001-users-nils-conductor/spec.md`

## Summary

Add multi-repo federated graph support to graphify: auto-detect incremental mode (no `--update` flag needed), ghost-node pruning on incremental runs, a new `graphify/multi.py` module for multi-repo orchestration, and corresponding SKILL.md orchestration updates. Each repo keeps its own `graphify-out/graph.json`; a workspace-level `meta-graph.json` stores only cross-repo edges discovered via four heuristics (import patterns, shared types, Helm/K8s refs, ArgoCD app-of-apps).

## Technical Context

**Language/Version**: Python 3.10+ (matches `requires-python = ">=3.10"` in pyproject.toml)  
**Primary Dependencies**: networkx, PyYAML (for `repos.yaml` parsing), tree-sitter (existing), graspologic/python-louvain (existing clustering)  
**Storage**: JSON files on disk (`graph.json`, `meta-graph.json`, `manifest.json`); no database  
**Testing**: pytest (existing `tests/` suite with one file per module pattern)  
**Target Platform**: macOS/Linux/Windows; CLI tool + importable library  
**Project Type**: Python library + CLI  
**Performance Goals**: Incremental runs should skip unchanged files; multi-repo runs should process repos independently (no re-extraction of unchanged repos)  
**Constraints**: Must maintain backwards compatibility — single-root `detect_incremental(Path)` callers must not break; no Python 3.11+ syntax  
**Scale/Scope**: Target workspaces: 2–10 repos; typical repo graph: 500–3000 nodes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Pipeline Purity | ✅ Pass | `multi.py`, `prune_deleted`, `merge_graphs` are pure functions; plain dict/nx.Graph I/O; no shared state |
| II. Library-First | ✅ Pass | All 4 new functions added to `__init__.py` `_map`; CLI/skill call library only |
| III. Schema Contract | ✅ Pass | Cross-repo edges extend base schema; `prune_deleted` operates on already-validated graphs |
| IV. Security by Default | ✅ Pass | No new unvalidated input surfaces; repo paths checked for existence before use |
| V. Test Discipline | ✅ Pass | `tests/test_multi.py` (new), `test_build.py` and `test_detect.py` extended; fixtures in `tests/fixtures/` |
| VI. Backwards Compatibility | ✅ Pass | `detect_incremental(Path)` callers unchanged; `--update` flag preserved; `graph.json` format unchanged |

**Post-design re-check**: All principles pass. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/001-users-nils-conductor/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit-tasks)
```

### Source Code (repository root)

```text
graphify/
├── multi.py             # NEW: multi_repo_detect, discover_cross_repo_edges, save/load_meta_graph
├── build.py             # MODIFIED: add prune_deleted(), merge_graphs()
├── detect.py            # MODIFIED: detect_incremental() accepts Path | list[Path]
├── __init__.py          # MODIFIED: expose 4 new public functions in _map
└── skill.md             # MODIFIED: auto-detect step, multi-repo pipeline, prune step

tests/
├── test_multi.py        # NEW: unit tests for graphify/multi.py
├── test_build.py        # MODIFIED: add tests for prune_deleted, merge_graphs
└── test_detect.py       # MODIFIED: add tests for list[Path] support in detect_incremental
```

**Structure Decision**: Single project, extending existing `graphify/` package. No new top-level directories. Follows the one-test-file-per-module pattern already established in `tests/`.

## Complexity Tracking

No constitution violations to justify.
