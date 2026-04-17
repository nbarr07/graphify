# Feature Specification: Graphify Fork — Multi-Repo + Doc Pipeline Integration

**Feature Branch**: `001-graphify-fork-multi-repo`  
**Created**: 2026-04-16  
**Status**: Draft  
**Input**: User description: "Graphify Fork: Multi-Repo + Doc Pipeline Integration"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Incremental single-repo rebuild (Priority: P1)

A developer runs graphify against a repo that already has a `graphify-out/graph.json`. Graphify auto-detects the existing graph and runs an incremental update (only changed files) without requiring an `--update` flag.

**Why this priority**: This is the most common daily workflow. It removes friction (no flag to remember) and makes the tool faster by default.

**Independent Test**: Run `graphify .` in a repo with an existing `graphify-out/graph.json`. Verify `detect_incremental()` is called (not `detect()`), only changed files are re-extracted, and the output graph reflects the changes.

**Acceptance Scenarios**:

1. **Given** a repo with `graphify-out/graph.json` present, **When** `graphify .` is run, **Then** graphify uses `detect_incremental()` without the user passing `--update`
2. **Given** a repo where files have been deleted since last run, **When** `graphify .` is run, **Then** `prune_deleted()` removes ghost nodes for those files before merging new extractions

---

### User Story 2 - Multi-repo federated graph generation (Priority: P2)

A developer has a workspace with `repos.yaml` listing multiple repos (radar-service, fleet-manager, radar-ingest-service). Running graphify at the workspace level generates per-repo graphs and a `meta-graph.json` linking them with cross-repo edges.

**Why this priority**: This is the core new capability. Without it, users in multi-repo settings must run graphify per-repo manually and have no cross-repo relationship visibility.

**Independent Test**: Create a workspace with `repos.yaml` and two repos each with source code. Run graphify at workspace root. Verify each repo gets its own `graphify-out/graph.json` and a `graphify-out/meta-graph.json` is written with cross-repo edges.

**Acceptance Scenarios**:

1. **Given** a workspace root with `repos.yaml` listing two repos, **When** graphify runs, **Then** each repo's graph is built independently and a `meta-graph.json` is written at the workspace level
2. **Given** two repos where one imports the other's package, **When** `discover_cross_repo_edges()` runs, **Then** an `INFERRED` edge with `discovery: "import_pattern"` is emitted in the meta-graph
3. **Given** a repo already has `graphify-out/graph.json`, **When** the multi-repo pipeline runs, **Then** that repo uses `detect_incremental()` while repos without an existing graph use `detect()`

---

### User Story 3 - Cross-repo edge validation and meta-graph save (Priority: P3)

After cross-repo edges are discovered, the user is shown the proposed edges for review before the meta-graph is saved. The user can accept or reject individual edges.

**Why this priority**: Cross-repo edges from heuristics may have false positives. User validation prevents garbage edges from polluting the meta-graph.

**Independent Test**: Trigger `discover_cross_repo_edges()` against two repos. Verify the proposed edges are presented to the user before `save_meta_graph()` is called, and that only confirmed edges are written.

**Acceptance Scenarios**:

1. **Given** cross-repo edges have been discovered, **When** graphify presents them to the user, **Then** the user can approve or skip individual edges before the meta-graph is written
2. **Given** no cross-repo edges were found, **When** the pipeline completes, **Then** an empty `cross_edges: []` meta-graph is written without prompting the user

---

### User Story 4 - Ghost node pruning on incremental update (Priority: P3)

When files are deleted from a repo between runs, nodes whose `source_file` points to those deleted files are removed from the graph before new extractions are merged in.

**Why this priority**: Without pruning, deleted code accumulates as stale "ghost" nodes, bloating the graph and producing misleading analysis.

**Independent Test**: Build a graph, delete a source file, run incremental update. Verify the nodes from the deleted file are absent from the output graph.

**Acceptance Scenarios**:

1. **Given** a graph with nodes from `foo.py`, **When** `foo.py` is deleted and an incremental run occurs, **Then** all nodes with `source_file == "foo.py"` are removed and `prune_deleted()` returns their IDs
2. **Given** no files were deleted, **When** `prune_deleted()` is called with an empty `deleted_files` list, **Then** the graph is returned unchanged

---

### Edge Cases

- What happens when `repos.yaml` lists a path that doesn't exist on disk?
- What happens when two repos have nodes with identical labels — are cross-repo "shared type" edges only emitted when 2+ signals confirm the match?
- What happens when `detect_incremental()` is called with a `list[Path]` that mixes repos with and without existing graphs?
- How does `merge_graphs()` handle node ID collisions between repos (both have a node named `main`)?
- What happens when `meta-graph.json` is corrupt or from an older schema version?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST auto-detect `graphify-out/graph.json` presence and select `UPDATE_MODE` (incremental) or `FRESH_MODE` (full) without requiring an explicit flag
- **FR-002**: System MUST support `repos.yaml` at workspace root with `{name, path, url}` entries to define a multi-repo workspace
- **FR-003**: `multi_repo_detect()` MUST return per-repo detection results including whether an existing graph was found and which detection mode was used
- **FR-004**: `discover_cross_repo_edges()` MUST apply four heuristics: import patterns, shared types (2+ signals required), Helm/K8s service URL references, ArgoCD app-of-apps manifests
- **FR-005**: Each discovered cross-repo edge MUST be tagged with `discovery` (heuristic name), `confidence` (`INFERRED`), and `confidence_score`
- **FR-006**: `save_meta_graph()` MUST write workspace-level `graphify-out/meta-graph.json` containing only cross-repo edges (not duplicating per-repo graph data)
- **FR-007**: `prune_deleted(G, deleted_files)` MUST remove all nodes whose `source_file` attribute matches any path in `deleted_files` and return the list of removed node IDs
- **FR-008**: `merge_graphs()` MUST prefix node IDs with `{repo_name}::` to avoid collisions when building a transient combined graph for cross-repo analysis
- **FR-009**: `detect_incremental()` MUST accept `Path | list[Path]` and remain backwards compatible with single-path callers
- **FR-010**: New functions (`multi_repo_detect`, `discover_cross_repo_edges`, `merge_graphs`, `prune_deleted`) MUST be exposed in `graphify/__init__.py` lazy-import map
- **FR-011**: `graphify/skill.md` MUST include auto-detect step (Step 1.5), multi-repo pipeline section, and updated incremental flow with prune step

### Key Entities

- **Workspace**: A directory containing `repos.yaml` and a workspace-level `graphify-out/` for the meta-graph
- **RepoInfo**: Per-repo detection result `{path, detection, has_existing_graph, graph_path}`
- **CrossRepoEdge**: `{source: "repo::NodeId", target: "repo::NodeId", relation, confidence, confidence_score, discovery}`
- **MetaGraph**: JSON file with `{repos: {name: {path, graph, updated}}, cross_edges: [CrossRepoEdge]}`

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running `graphify .` on a repo with an existing graph produces the same result as `graphify . --update` with no user-visible difference
- **SC-002**: A workspace with 3 repos produces 3 independent `graph.json` files and 1 `meta-graph.json` in a single graphify invocation
- **SC-003**: `prune_deleted()` removes exactly the nodes associated with deleted files — no more, no fewer — verified by unit test
- **SC-004**: `discover_cross_repo_edges()` emits at least one correct import-pattern edge when two repos have a documented import relationship, verified by fixture test
- **SC-005**: `detect_incremental()` called with `list[Path]` produces the same result as calling it once per path and merging, verified by unit test
- **SC-006**: All new public functions pass `validate_extraction()` schema checks where they produce extraction dicts

## Assumptions

- `repos.yaml` uses simple `{name, path, url}` structure; no authentication or SSH config handling is in scope for this feature
- Cross-repo edge discovery is heuristic-only — LLM-assisted edge inference is out of scope
- The `merge_graphs()` combined graph is transient (used for analysis only); it is not persisted to disk
- `--update` flag continues to work as an explicit override; auto-detection is additive, not a breaking change
- The doc agent rewrites (Branch 2: graph-agents) are a separate branch and out of scope for this spec — only the Python package changes (Branch 1: graphify-fork) and SKILL.md orchestration are in scope here
- Per-repo graphs remain authoritative for their own entities; the meta-graph contains only cross-repo edges, never duplicates intra-repo structure
- Python 3.10+ compatibility must be maintained (no 3.11+ syntax)
