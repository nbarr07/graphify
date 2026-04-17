# Data Model: Graphify Fork — Multi-Repo + Doc Pipeline Integration

## Entities

### RepoConfig
Parsed from `repos.yaml` at workspace root.

| Field | Type | Notes |
|-------|------|-------|
| `name` | `str` | Unique repo identifier, used as node ID prefix (`{name}::`) |
| `path` | `str` | Relative or absolute path to repo root |
| `url` | `str` | Git remote URL (optional, for ArgoCD heuristic) |

### RepoInfo
Returned per-repo from `multi_repo_detect()`.

| Field | Type | Notes |
|-------|------|-------|
| `name` | `str` | From RepoConfig |
| `path` | `Path` | Resolved absolute path |
| `detection` | `dict` | Full result from `detect()` or `detect_incremental()` |
| `has_existing_graph` | `bool` | Whether `{path}/graphify-out/graph.json` existed before this run |
| `graph_path` | `Path` | `{path}/graphify-out/graph.json` |

**Validation**: `path` must exist on disk; raise `ValueError` if missing.

### CrossRepoEdge
Emitted by `discover_cross_repo_edges()`, stored in `meta-graph.json`.

| Field | Type | Notes |
|-------|------|-------|
| `source` | `str` | `"{repo_name}::{node_id}"` |
| `target` | `str` | `"{repo_name}::{node_id}"` |
| `relation` | `str` | Always `"calls"`, `"imports"`, or `"uses"` |
| `confidence` | `str` | Always `"INFERRED"` |
| `confidence_score` | `float` | 0.0–1.0, heuristic-dependent |
| `discovery` | `str` | `"import_pattern"` \| `"shared_type"` \| `"helm_ref"` \| `"argocd_ref"` |

### MetaGraph (meta-graph.json)
Written to `{workspace_root}/graphify-out/meta-graph.json`.

```json
{
  "repos": {
    "radar-service": {
      "path": "./radar-service",
      "graph": "radar-service/graphify-out/graph.json",
      "updated": "2026-04-16T12:00:00Z"
    }
  },
  "cross_edges": [
    {
      "source": "radar-service::ServiceClient",
      "target": "fleet-manager::FleetAPI",
      "relation": "calls",
      "confidence": "INFERRED",
      "confidence_score": 0.8,
      "discovery": "import_pattern"
    }
  ]
}
```

**Validation rules**:
- `repos` keys must match entries in `repos.yaml`
- `cross_edges[*].source` and `target` must be in format `"{name}::{id}"` where `name` is a known repo
- `confidence_score` must be in `[0.0, 1.0]`
- `discovery` must be one of the four known tags

## State Transitions

### detect_incremental with list[Path]

```
list[Path] input
  → for each root: detect(root)
  → for each root: load_manifest({root}/graphify-out/manifest.json)
  → merge files dicts (union by category)
  → union deleted_files across all roots
  → return merged detection result
```

### Incremental pipeline with ghost pruning

```
existing graph.json exists?
  YES → load graph (build_from_json)
      → detect_incremental(root)  # get deleted_files
      → prune_deleted(G, deleted_files)  # remove ghost nodes
      → extract changed files
      → build(new_extractions)  # new subgraph
      → merge (new nodes/edges into pruned G)
      → cluster → analyze → report → export
  NO  → detect() (full)
      → extract all files
      → build → cluster → analyze → report → export
```

### Multi-repo pipeline

```
repos.yaml exists?
  YES → multi_repo_detect(repos_config, workspace_root)
      → for each repo: load existing graph if present
      → for each repo: run single-repo pipeline (incremental or fresh)
      → discover_cross_repo_edges(all_repo_graphs)
      → present edges to user for validation
      → save_meta_graph(repos_info, validated_edges, workspace_root/graphify-out/meta-graph.json)
  NO  → single-repo pipeline (existing behavior)
```

## Function Signatures

### graphify/multi.py (new)

```python
def multi_repo_detect(
    repos_config: dict,           # parsed repos.yaml: {name: {path, url}}
    workspace_root: Path,
) -> dict:
    """Returns {"repos": {name: RepoInfo dict}}"""

def discover_cross_repo_edges(
    repo_graphs: dict[str, nx.Graph],  # {repo_name: nx.Graph}
) -> list[dict]:
    """Returns list of CrossRepoEdge dicts"""

def save_meta_graph(
    repos_info: dict,             # output of multi_repo_detect
    cross_edges: list[dict],      # validated CrossRepoEdge list
    output_path: Path,            # workspace_root/graphify-out/meta-graph.json
) -> None: ...

def load_meta_graph(path: Path) -> dict: ...
```

### graphify/build.py (additions)

```python
def prune_deleted(
    G: nx.Graph,
    deleted_files: list[str],
) -> tuple[nx.Graph, list[str]]:
    """Remove nodes whose source_file is in deleted_files.
    Returns (G, removed_node_ids)."""

def merge_graphs(
    graphs: list[tuple[str, nx.Graph]],  # [(repo_name, graph), ...]
    cross_edges: list[dict] | None = None,
) -> nx.Graph:
    """Build transient combined graph with repo-prefixed node IDs."""
```

### graphify/detect.py (modification)

```python
def detect_incremental(
    root: Path | list[Path],
    manifest_path: str = _MANIFEST_PATH,
) -> dict:
    """Backwards compatible: single Path behaves as before.
    list[Path]: iterate, merge file dicts, union deleted_files."""
```
