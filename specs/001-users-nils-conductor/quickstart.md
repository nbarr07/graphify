# Quickstart: Multi-Repo Graphify

## Single-repo incremental (auto-detect, no flag needed)

```bash
# First run — no graph.json exists → full extraction
graphify .

# Subsequent runs — graph.json found → incremental automatically
graphify .
# Ghost nodes for deleted files are pruned automatically
```

## Multi-repo workspace

1. Create `repos.yaml` at workspace root:

```yaml
- name: radar-service
  path: ./radar-service
- name: fleet-manager
  path: ./fleet-manager
- name: radar-ingest-service
  path: ./radar-ingest-service
```

2. Run graphify at workspace root:

```bash
graphify .
```

This produces:
- `radar-service/graphify-out/graph.json`
- `fleet-manager/graphify-out/graph.json`
- `radar-ingest-service/graphify-out/graph.json`
- `graphify-out/meta-graph.json` (cross-repo edges, after user validation)

## Python library usage

```python
from pathlib import Path
import graphify

# Multi-repo detection
repos_config = {
    "radar-service": {"path": "./radar-service"},
    "fleet-manager": {"path": "./fleet-manager"},
}
repos_info = graphify.multi_repo_detect(repos_config, Path("."))

# Ghost-node pruning (incremental update)
import networkx as nx
from networkx.readwrite import json_graph
import json

G = json_graph.node_link_graph(json.loads(Path("graphify-out/graph.json").read_text()))
detection = graphify.detect_incremental(Path("."))
G, removed = graphify.prune_deleted(G, detection["deleted_files"])
```
