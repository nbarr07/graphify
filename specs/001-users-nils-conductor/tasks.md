---
description: "Task list for Graphify Fork — Multi-Repo + Doc Pipeline Integration"
---

# Tasks: Graphify Fork — Multi-Repo + Doc Pipeline Integration

**Input**: Design documents from `/specs/001-users-nils-conductor/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US4)
- Exact file paths included in every task

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add the one missing dependency and confirm test harness baseline.

- [x] T001 Add `pyyaml` to `dependencies` in `pyproject.toml` (required for repos.yaml parsing per research.md Decision 1)
- [x] T002 [P] Verify `pytest tests/ -q` passes clean on current branch before any changes (baseline gate)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core building blocks that all user stories depend on — must complete before any story work begins.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T003 Add `prune_deleted(G, deleted_files)` to `graphify/build.py` — filters nodes by `source_file` attr, calls `G.remove_nodes_from()`, returns `(G, removed_ids)` (~15 lines)
- [x] T004 [P] Add `merge_graphs(graphs, cross_edges=None)` to `graphify/build.py` — prefixes node IDs with `{repo_name}::`, copies attributes, adds cross_edges as nx edges (~30 lines)
- [x] T005 Modify `detect_incremental(root, manifest_path)` in `graphify/detect.py` to accept `Path | list[Path]` — when list: iterate, call `detect()` per path, merge `files` dicts by category, union `deleted_files`; single `Path` behaviour unchanged (~15 lines changed)
- [x] T006 Create `graphify/multi.py` with stub module: `multi_repo_detect`, `discover_cross_repo_edges`, `save_meta_graph`, `load_meta_graph` function signatures, docstrings, and imports only (no implementation yet — establishes the module for parallel story work)
- [x] T007 Expose 4 new symbols in `graphify/__init__.py` `_map`: `multi_repo_detect`, `discover_cross_repo_edges`, `merge_graphs`, `prune_deleted`

**Checkpoint**: Foundation ready — T003–T007 complete, unit tests for these functions can now begin in parallel with story implementation.

---

## Phase 3: User Story 1 — Incremental Single-Repo Rebuild (Priority: P1) 🎯 MVP

**Goal**: `graphify .` auto-detects existing `graph.json` and uses incremental mode without `--update` flag; deleted-file ghost nodes are pruned automatically.

**Independent Test**: Run `graphify .` in a repo with existing `graphify-out/graph.json`. Confirm `detect_incremental()` was called (check output/logs), only changed files re-extracted, and nodes from any deleted files are absent from the output graph.

### Implementation for User Story 1

- [x] T008 [US1] Implement ghost-node pruning in the incremental update flow: in `graphify/skill.md` Step 3 (update flow), add call to `prune_deleted(G, detection["deleted_files"])` after loading existing graph and before merging new extractions
- [x] T009 [US1] Add auto-detect Step 1.5 to `graphify/skill.md`: check for `graphify-out/graph.json` existence → set `UPDATE_MODE` (use `detect_incremental()`) or `FRESH_MODE` (use `detect()`); remove requirement for explicit `--update` flag in normal flow (flag remains as override)

### Tests for User Story 1

- [x] T010 [P] [US1] Add `test_prune_deleted` to `tests/test_build.py`: build graph with nodes from two files, call `prune_deleted(G, [file1])`, assert nodes from file1 removed and file2 nodes intact, assert returned IDs match removed nodes
- [x] T011 [P] [US1] Add `test_prune_deleted_empty` to `tests/test_build.py`: call `prune_deleted(G, [])`, assert graph unchanged and returns `(G, [])`
- [x] T012 [P] [US1] Add `test_detect_incremental_single_path_unchanged` to `tests/test_detect.py`: verify single `Path` argument still works identically to pre-change behaviour

**Checkpoint**: User Story 1 is fully functional — `graphify .` auto-detects and prunes ghost nodes without any flag.

---

## Phase 4: User Story 2 — Multi-Repo Federated Graph Generation (Priority: P2)

**Goal**: A workspace with `repos.yaml` produces per-repo `graph.json` files and a workspace-level `meta-graph.json` with cross-repo edges after user validation.

**Independent Test**: Create a temp workspace with `repos.yaml` listing two repos, each with source files. Run graphify at workspace root. Verify each repo has its own `graphify-out/graph.json` and `graphify-out/meta-graph.json` is written at workspace level with correct structure.

### Implementation for User Story 2

- [x] T013 [US2] Implement `multi_repo_detect(repos_config, workspace_root)` in `graphify/multi.py`: parse each entry, resolve paths, check for existing `graph.json`, call `detect_incremental()` or `detect()` per repo, return `{"repos": {name: RepoInfo dict}}`
- [x] T014 [US2] Implement `discover_cross_repo_edges(repo_graphs)` in `graphify/multi.py`: four heuristics — import_pattern (scan code node labels for other repos' package names), shared_type (identical labels across repos, 2+ signal requirement), helm_ref (service URLs in values.yaml nodes), argocd_ref (Application manifest URL nodes); each edge tagged with `discovery`, `confidence: "INFERRED"`, `confidence_score`
- [x] T015 [US2] Implement `save_meta_graph(repos_info, cross_edges, output_path)` and `load_meta_graph(path)` in `graphify/multi.py`: write/read the meta-graph JSON format as defined in `contracts/public-api.md`
- [x] T016 [US2] Add multi-repo pipeline section to `graphify/skill.md`: if `repos.yaml` exists → parse repos → per-repo incremental-or-fresh pipeline → `discover_cross_repo_edges()` → present edges to user for validation → `save_meta_graph()`

### Tests for User Story 2

- [x] T017 [P] [US2] Create `tests/test_multi.py`: `test_multi_repo_detect_fresh` — mock two repo paths with no existing graph, verify both return `has_existing_graph=False` and `detection` from `detect()`
- [x] T018 [P] [US2] Add `test_multi_repo_detect_incremental` to `tests/test_multi.py`: mock one repo with existing `graph.json`, verify it returns `has_existing_graph=True` and uses `detect_incremental()`
- [x] T019 [P] [US2] Add `test_multi_repo_detect_missing_path` to `tests/test_multi.py`: pass a repo path that doesn't exist, assert `ValueError` raised
- [x] T020 [P] [US2] Add `test_discover_cross_repo_edges_import_pattern` to `tests/test_multi.py`: build two minimal graphs where one has a code node label matching the other repo's name, assert one `import_pattern` edge emitted with `confidence_score >= 0.7`
- [x] T021 [P] [US2] Add `test_discover_cross_repo_edges_empty` to `tests/test_multi.py`: call with two graphs with no matching nodes, assert empty list returned (no exception)
- [x] T022 [P] [US2] Add `test_save_load_meta_graph` to `tests/test_multi.py`: save a meta-graph dict to `tmp_path`, load it back, assert round-trip equality
- [x] T023 [P] [US2] Add `test_detect_incremental_list_path` to `tests/test_detect.py`: call `detect_incremental([path1, path2])`, assert result contains merged `files` dict and union of `deleted_files` from both paths

### Tests for User Story 2 — merge_graphs

- [x] T024 [P] [US2] Add `test_merge_graphs_prefix` to `tests/test_build.py`: call `merge_graphs([("repo-a", G1), ("repo-b", G2)])`, assert all node IDs prefixed with `repo-a::` or `repo-b::` respectively
- [x] T025 [P] [US2] Add `test_merge_graphs_cross_edges` to `tests/test_build.py`: pass `cross_edges` list, assert edges present in merged graph between prefixed node IDs

**Checkpoint**: User Stories 1 AND 2 complete — single-repo and multi-repo flows both work independently.

---

## Phase 5: User Story 3 — Cross-Repo Edge Validation (Priority: P3)

**Goal**: Discovered cross-repo edges are presented to the user before `meta-graph.json` is saved; user can approve or skip individual edges.

**Independent Test**: Trigger `discover_cross_repo_edges()` in skill flow; verify user is prompted with each edge and only confirmed edges appear in the written `meta-graph.json`.

### Implementation for User Story 3

- [x] T026 [US3] Add edge-validation interaction to the multi-repo pipeline section in `graphify/skill.md`: after `discover_cross_repo_edges()`, present each edge (source → target, relation, confidence_score, discovery method) to the user; collect approvals; pass only confirmed edges to `save_meta_graph()`
- [x] T027 [US3] Handle zero-edge case in `graphify/skill.md`: if `discover_cross_repo_edges()` returns empty list, write `meta-graph.json` with `cross_edges: []` without prompting user

**Checkpoint**: Edge validation flow complete — no garbage edges written without user confirmation.

---

## Phase 6: User Story 4 — Ghost Node Pruning (Priority: P3)

**Goal**: Nodes from deleted files are removed from the graph on incremental update; `prune_deleted()` is correct and covered.

**Note**: The core `prune_deleted()` function is implemented in Phase 2 (T003) and tested in Phase 3 (T010–T011). This phase wires it into the skill update flow and validates the end-to-end scenario.

**Independent Test**: Build a graph, delete a source file, run incremental update. Nodes from the deleted file absent from output graph; `prune_deleted()` returns their IDs.

### Implementation for User Story 4

- [x] T028 [US4] Add integration note to `graphify/skill.md` update flow comments: document that `prune_deleted()` is called before merging new extractions, and that the list of pruned node IDs is included in the run summary shown to the user

### Tests for User Story 4

- [x] T029 [US4] Add `test_prune_deleted_integration` to `tests/test_build.py`: build a graph from a real fixture file path, simulate deletion by passing that path to `prune_deleted()`, assert zero nodes remain with that `source_file`, and remaining nodes from other files are intact

**Checkpoint**: All four user stories independently functional and tested.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Finalization tasks that span multiple user stories.

- [x] T030 [P] Run `pytest tests/ -q --tb=short` and confirm zero failures on Python 3.10 and 3.12
- [x] T031 [P] Add `pyyaml` usage example in `tests/test_multi.py` fixture setup to confirm the dependency is importable in the test environment
- [x] T032 Add CHANGELOG entry for this feature: multi-repo support, auto-detect incremental, ghost-node pruning, `graphify/multi.py` new public API
- [x] T033 [P] Review `graphify/skill.md` for consistency: confirm Step 1.5 (auto-detect), multi-repo section, and prune step are in the correct order and do not conflict with existing steps
- [x] T034 [P] Verify backwards compatibility: write a test or manual check that `graphify.detect_incremental(Path("."))` (single path, no list) behaves identically to pre-change output
- [x] T035 [P] Update `CLAUDE.md` if needed: confirm `Active Technologies` section reflects PyYAML addition (already added by `update-agent-context.sh` — verify no drift)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 — BLOCKS all user stories
- **Phase 3 (US1 — P1)**: Depends on Phase 2 (T003, T005 specifically)
- **Phase 4 (US2 — P2)**: Depends on Phase 2 (T004, T005, T006, T007 specifically)
- **Phase 5 (US3 — P3)**: Depends on Phase 4 (T014, T015)
- **Phase 6 (US4 — P3)**: Depends on Phase 2 (T003) and Phase 3 (T008) — already covered
- **Phase 7 (Polish)**: Depends on all prior phases

### User Story Dependencies

- **US1 (P1)**: Needs T003 (prune_deleted) + T005 (detect_incremental list[Path])
- **US2 (P2)**: Needs T004 (merge_graphs) + T005 + T006 (multi.py stubs) + T007 (\_\_init\_\_ map)
- **US3 (P3)**: Needs US2 complete (T014, T015)
- **US4 (P3)**: Needs T003 (already done for US1) — no additional foundational deps

### Within Each User Story

- Module implementation before tests that import it
- `graphify/multi.py` stubs (T006) before any multi.py implementation tasks (T013–T015)
- `__init__.py` update (T007) before any integration test that does `import graphify; graphify.multi_repo_detect(...)`
- skill.md updates are independent of Python code and can be done in parallel

### Parallel Opportunities

- T001 and T002 can run in parallel
- T003 and T004 can run in parallel (different functions in build.py — coordinate on file edits)
- T005, T006, T007 can run in parallel with each other (different files)
- All test tasks within a phase marked [P] can run in parallel
- US3 skill.md work (T026, T027) can run in parallel with US4 (T028, T029)
- All Phase 7 tasks marked [P] can run in parallel

---

## Parallel Example: Phase 2 Foundational

```bash
# These can run concurrently (different files):
Task: "Add prune_deleted() to graphify/build.py"           # T003
Task: "Add merge_graphs() to graphify/build.py"            # T004 — coordinate on same file
Task: "Modify detect_incremental() in graphify/detect.py"  # T005
Task: "Create graphify/multi.py stubs"                     # T006
Task: "Update graphify/__init__.py _map"                   # T007
```

```bash
# Phase 3 tests (all [P], different test functions in same file — run sequentially or split):
Task: "test_prune_deleted in tests/test_build.py"          # T010
Task: "test_prune_deleted_empty in tests/test_build.py"    # T011
Task: "test_detect_incremental_single_path_unchanged"      # T012
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T002)
2. Complete Phase 2: Foundational (T003–T007) — critical gate
3. Complete Phase 3: User Story 1 (T008–T012)
4. **STOP and VALIDATE**: Run `graphify .` in a repo with existing graph; confirm auto-detect + pruning
5. Ship as incremental improvement — multi-repo can follow

### Incremental Delivery

1. Setup + Foundational → baseline ready
2. US1 (P1) → auto-detect + pruning → demo/validate → MVP
3. US2 (P2) → multi-repo + meta-graph → demo/validate
4. US3 + US4 (P3) → edge validation + pruning polish → demo/validate

### Parallel Team Strategy

With two developers after Phase 2 completes:

- Developer A: US1 — skill.md auto-detect + prune wiring (T008–T009) + tests (T010–T012)
- Developer B: US2 — multi.py implementation (T013–T015) + tests (T017–T025)

---

## Notes

- `[P]` tasks = different files or non-conflicting changes; safe to parallelise
- `[Story]` label maps each task to its user story for traceability
- T003 and T004 both touch `graphify/build.py` — coordinate to avoid merge conflicts
- Tests MUST pass before marking implementation tasks complete
- `pytest tests/ -q` is the single gate; CI enforces Python 3.10 + 3.12
- skill.md changes (T008, T009, T016, T026–T028, T033) are markdown edits — fast, low-risk
