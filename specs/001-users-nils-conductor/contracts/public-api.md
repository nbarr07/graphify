# Public API Contract: graphify multi-repo extension

## Library API (importable from `graphify`)

These four symbols are added to `graphify/__init__.py`'s lazy `_map` and become part of the public API:

```python
import graphify

# Multi-repo detection
repos_info = graphify.multi_repo_detect(repos_config, workspace_root)

# Cross-repo edge discovery
edges = graphify.discover_cross_repo_edges(repo_graphs)

# Graph utilities
G_pruned, removed_ids = graphify.prune_deleted(G, deleted_files)
G_merged = graphify.merge_graphs(graphs, cross_edges=edges)
```

### `multi_repo_detect(repos_config, workspace_root)`
- **Input**: `repos_config: dict` — e.g., `{"radar-service": {"path": "./radar-service", "url": "..."}}`, `workspace_root: Path`
- **Output**: `{"repos": {name: {"path": Path, "detection": dict, "has_existing_graph": bool, "graph_path": Path}}}`
- **Errors**: `ValueError` if a repo path does not exist on disk

### `discover_cross_repo_edges(repo_graphs)`
- **Input**: `repo_graphs: dict[str, nx.Graph]` — keyed by repo name
- **Output**: `list[dict]` — each dict is a valid `CrossRepoEdge`
- **Errors**: Returns empty list if no edges found; never raises on empty input

### `prune_deleted(G, deleted_files)`
- **Input**: `G: nx.Graph`, `deleted_files: list[str]`
- **Output**: `tuple[nx.Graph, list[str]]` — mutated graph and list of removed node IDs
- **Contract**: Modifies G in-place AND returns it. Empty `deleted_files` → no-op, returns `(G, [])`

### `merge_graphs(graphs, cross_edges=None)`
- **Input**: `graphs: list[tuple[str, nx.Graph]]`, `cross_edges: list[dict] | None`
- **Output**: `nx.Graph` with node IDs prefixed as `"{repo_name}::{original_id}"`
- **Contract**: Returned graph is transient — callers must not persist it to disk

## repos.yaml Schema

```yaml
# workspace/repos.yaml
- name: radar-service        # required, unique
  path: ./radar-service      # required, relative or absolute
  url: git@github.com:...    # optional
- name: fleet-manager
  path: ./fleet-manager
```

## meta-graph.json Schema

```json
{
  "repos": {
    "<name>": {
      "path": "<relative path>",
      "graph": "<relative path to graph.json>",
      "updated": "<ISO 8601 timestamp>"
    }
  },
  "cross_edges": [
    {
      "source": "<repo>::<node_id>",
      "target": "<repo>::<node_id>",
      "relation": "calls|imports|uses",
      "confidence": "INFERRED",
      "confidence_score": 0.0,
      "discovery": "import_pattern|shared_type|helm_ref|argocd_ref"
    }
  ]
}
```

## Backwards Compatibility Guarantees

- `detect_incremental(Path)` (single path) — behaviour unchanged
- `build_from_json()`, `build()` — unchanged
- All existing `graphify.__init__` exports — unchanged
- `graphify-out/graph.json` format — unchanged
- `--update` CLI flag — continues to work as explicit override
