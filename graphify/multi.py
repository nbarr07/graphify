# Multi-repo graph orchestration
#
# Federated model: each repo keeps its own graphify-out/graph.json.
# This module discovers cross-repo relationships and writes a workspace-level
# meta-graph.json that stores only cross-repo edges (not per-repo graph data).
#
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import networkx as nx

from .detect import detect, detect_incremental


def multi_repo_detect(repos_config: dict, workspace_root: Path) -> dict:
    """Detect files across multiple repos, respecting existing graphs.

    repos_config: {name: {path, url}} — parsed from repos.yaml
    workspace_root: absolute path to the workspace directory

    Returns {"repos": {name: RepoInfo dict}} where RepoInfo contains:
      path, detection, has_existing_graph, graph_path
    """
    result: dict[str, dict] = {}
    for name, config in repos_config.items():
        raw_path = config.get("path", name)
        repo_path = Path(raw_path)
        if not repo_path.is_absolute():
            repo_path = (workspace_root / repo_path).resolve()
        if not repo_path.exists():
            raise ValueError(f"Repo path does not exist: {repo_path!r} (repo: {name!r})")

        graph_path = repo_path / "graphify-out" / "graph.json"
        has_existing = graph_path.exists()
        manifest_path = str(repo_path / "graphify-out" / "manifest.json")

        if has_existing:
            detection = detect_incremental(repo_path, manifest_path=manifest_path)
        else:
            detection = detect(repo_path)

        result[name] = {
            "path": repo_path,
            "detection": detection,
            "has_existing_graph": has_existing,
            "graph_path": graph_path,
        }

    return {"repos": result}


def discover_cross_repo_edges(repo_graphs: dict[str, nx.Graph]) -> list[dict]:
    """Discover cross-repo edges using four heuristics.

    repo_graphs: {repo_name: nx.Graph} — keyed by repo name

    Returns a list of CrossRepoEdge dicts:
      {source, target, relation, confidence, confidence_score, discovery}

    Each edge uses '{repo_name}::{node_id}' format for source/target.
    """
    edges: list[dict] = []
    repo_names = list(repo_graphs.keys())

    # Pre-compute node label → (repo, node_id) index for shared-type heuristic
    label_index: dict[str, list[tuple[str, str]]] = {}
    for repo_name, G in repo_graphs.items():
        for node_id, attrs in G.nodes(data=True):
            label = attrs.get("label", "")
            if label:
                label_index.setdefault(label, []).append((repo_name, node_id))

    for i, repo_a in enumerate(repo_names):
        G_a = repo_graphs[repo_a]
        for repo_b in repo_names[i + 1:]:
            G_b = repo_graphs[repo_b]

            # Heuristic 1: Import patterns
            # Look for code nodes in repo_a whose label matches repo_b's name (and vice versa)
            for node_id, attrs in G_a.nodes(data=True):
                label = attrs.get("label", "").lower()
                if repo_b.lower().replace("-", "_") in label or repo_b.lower() in label:
                    if attrs.get("file_type") == "code" or "import" in label:
                        edges.append({
                            "source": f"{repo_a}::{node_id}",
                            "target": f"{repo_b}::",  # repo-level reference
                            "relation": "imports",
                            "confidence": "INFERRED",
                            "confidence_score": 0.8,
                            "discovery": "import_pattern",
                        })

            for node_id, attrs in G_b.nodes(data=True):
                label = attrs.get("label", "").lower()
                if repo_a.lower().replace("-", "_") in label or repo_a.lower() in label:
                    if attrs.get("file_type") == "code" or "import" in label:
                        edges.append({
                            "source": f"{repo_b}::{node_id}",
                            "target": f"{repo_a}::",
                            "relation": "imports",
                            "confidence": "INFERRED",
                            "confidence_score": 0.8,
                            "discovery": "import_pattern",
                        })

            # Heuristic 2: Shared types — identical labels across repos (require 2+ signals)
            for label, occurrences in label_index.items():
                repos_with_label = {r for r, _ in occurrences}
                if repo_a in repos_with_label and repo_b in repos_with_label:
                    # Require at least 2 occurrences total to confirm (2+ signals)
                    if len(occurrences) >= 2:
                        nodes_a = [nid for r, nid in occurrences if r == repo_a]
                        nodes_b = [nid for r, nid in occurrences if r == repo_b]
                        edges.append({
                            "source": f"{repo_a}::{nodes_a[0]}",
                            "target": f"{repo_b}::{nodes_b[0]}",
                            "relation": "uses",
                            "confidence": "INFERRED",
                            "confidence_score": 0.65,
                            "discovery": "shared_type",
                        })

            # Heuristic 3: Helm/K8s references
            # Look for nodes whose label contains another repo's service name (in yaml files)
            for node_id, attrs in G_a.nodes(data=True):
                src_file = attrs.get("source_file", "")
                label = attrs.get("label", "").lower()
                if ("values.yaml" in src_file or "values.yml" in src_file):
                    if repo_b.lower().replace("-", "_") in label or repo_b.lower() in label:
                        edges.append({
                            "source": f"{repo_a}::{node_id}",
                            "target": f"{repo_b}::",
                            "relation": "uses",
                            "confidence": "INFERRED",
                            "confidence_score": 0.7,
                            "discovery": "helm_ref",
                        })

            # Heuristic 4: ArgoCD app-of-apps references
            for node_id, attrs in G_a.nodes(data=True):
                src_file = attrs.get("source_file", "")
                label = attrs.get("label", "").lower()
                is_argocd = (
                    "application" in label
                    and (src_file.endswith(".yaml") or src_file.endswith(".yml"))
                )
                if is_argocd:
                    b_url = repos_config.get(repo_b, {}).get("url", "")
                    if b_url and b_url.lower() in label:
                        edges.append({
                            "source": f"{repo_a}::{node_id}",
                            "target": f"{repo_b}::",
                            "relation": "uses",
                            "confidence": "INFERRED",
                            "confidence_score": 0.75,
                            "discovery": "argocd_ref",
                        })

    # Remove duplicate edges (same source+target+discovery)
    seen: set[tuple] = set()
    unique: list[dict] = []
    for edge in edges:
        key = (edge["source"], edge["target"], edge["discovery"])
        if key not in seen:
            seen.add(key)
            unique.append(edge)

    return unique


def save_meta_graph(
    repos_info: dict,
    cross_edges: list[dict],
    output_path: Path,
) -> None:
    """Write the workspace-level meta-graph JSON.

    repos_info: output of multi_repo_detect ({"repos": {name: RepoInfo}})
    cross_edges: validated list of CrossRepoEdge dicts
    output_path: absolute path to write meta-graph.json
    """
    repos_section: dict = {}
    for name, info in repos_info.get("repos", {}).items():
        graph_path = info.get("graph_path")
        repo_path = info.get("path")
        rel_graph = str(graph_path.relative_to(output_path.parent.parent)) if graph_path else ""
        rel_repo = str(repo_path.relative_to(output_path.parent.parent)) if repo_path else name
        repos_section[name] = {
            "path": f"./{rel_repo}",
            "graph": rel_graph,
            "updated": datetime.now(timezone.utc).isoformat(),
        }

    meta = {
        "repos": repos_section,
        "cross_edges": cross_edges,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")


def load_meta_graph(path: Path) -> dict:
    """Load a meta-graph.json file. Returns {} if missing or corrupt."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def parse_repos_yaml(workspace_root: Path) -> dict:
    """Parse repos.yaml from workspace_root. Returns {} if not found.

    Expected format:
      - name: repo-name
        path: ./relative/path
        url: git@github.com:org/repo.git  # optional
    """
    repos_yaml = workspace_root / "repos.yaml"
    if not repos_yaml.exists():
        return {}
    try:
        import yaml  # pyyaml
        raw = yaml.safe_load(repos_yaml.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            return {}
        return {
            entry["name"]: {k: v for k, v in entry.items() if k != "name"}
            for entry in raw
            if isinstance(entry, dict) and "name" in entry
        }
    except Exception:
        return {}
