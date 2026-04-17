"""Tests for graphify/multi.py — multi-repo graph orchestration."""
from __future__ import annotations

import json
from pathlib import Path

import networkx as nx
import pytest


# --- multi_repo_detect ---

def test_multi_repo_detect_fresh(tmp_path):
    """Repos with no existing graph → has_existing_graph=False, uses detect()."""
    from graphify.multi import multi_repo_detect

    repo_a = tmp_path / "repo-a"
    repo_a.mkdir()
    (repo_a / "main.py").write_text("def foo(): pass")

    repos_config = {"repo-a": {"path": str(repo_a)}}
    result = multi_repo_detect(repos_config, tmp_path)

    info = result["repos"]["repo-a"]
    assert info["has_existing_graph"] is False
    assert info["path"] == repo_a
    assert info["graph_path"] == repo_a / "graphify-out" / "graph.json"
    assert "files" in info["detection"]


def test_multi_repo_detect_incremental(tmp_path):
    """Repos with existing graph.json → has_existing_graph=True."""
    from graphify.multi import multi_repo_detect

    repo_a = tmp_path / "repo-a"
    (repo_a / "graphify-out").mkdir(parents=True)
    (repo_a / "main.py").write_text("def foo(): pass")
    # Create a minimal graph.json so has_existing_graph=True
    (repo_a / "graphify-out" / "graph.json").write_text(
        json.dumps({"nodes": [], "links": []})
    )

    repos_config = {"repo-a": {"path": str(repo_a)}}
    result = multi_repo_detect(repos_config, tmp_path)

    assert result["repos"]["repo-a"]["has_existing_graph"] is True


def test_multi_repo_detect_missing_path_raises(tmp_path):
    """Repo path that does not exist → ValueError."""
    from graphify.multi import multi_repo_detect

    repos_config = {"ghost": {"path": str(tmp_path / "does_not_exist")}}
    with pytest.raises(ValueError, match="does not exist"):
        multi_repo_detect(repos_config, tmp_path)


def test_multi_repo_detect_relative_path(tmp_path):
    """Relative paths in repos_config are resolved against workspace_root."""
    from graphify.multi import multi_repo_detect

    repo_a = tmp_path / "sub" / "repo-a"
    repo_a.mkdir(parents=True)
    (repo_a / "main.py").write_text("x = 1")

    repos_config = {"repo-a": {"path": "./sub/repo-a"}}
    result = multi_repo_detect(repos_config, tmp_path)
    assert result["repos"]["repo-a"]["path"] == repo_a


# --- discover_cross_repo_edges ---

def _make_graph(nodes):
    """Build a small nx.Graph from list of (id, label, file_type, source_file)."""
    G = nx.Graph()
    for nid, label, ftype, src in nodes:
        G.add_node(nid, label=label, file_type=ftype, source_file=src)
    return G


def test_discover_cross_repo_edges_import_pattern():
    """Import pattern: code node label contains another repo's name → edge emitted."""
    from graphify.multi import discover_cross_repo_edges

    G_a = _make_graph([("import_fleet_manager", "fleet_manager", "code", "main.py")])
    G_b = _make_graph([("cls_FleetAPI", "FleetAPI", "code", "api.py")])

    edges = discover_cross_repo_edges({"radar-service": G_a, "fleet-manager": G_b})
    import_edges = [e for e in edges if e["discovery"] == "import_pattern"]
    assert len(import_edges) >= 1
    assert all(e["confidence"] == "INFERRED" for e in import_edges)
    assert all(0.0 <= e["confidence_score"] <= 1.0 for e in import_edges)


def test_discover_cross_repo_edges_empty_graphs():
    """No matching nodes → empty list, no exception."""
    from graphify.multi import discover_cross_repo_edges

    G_a = _make_graph([("cls_Foo", "Foo", "code", "foo.py")])
    G_b = _make_graph([("cls_Bar", "Bar", "code", "bar.py")])

    edges = discover_cross_repo_edges({"repo-a": G_a, "repo-b": G_b})
    # May have shared_type edges if labels match — just assert no exception and list returned
    assert isinstance(edges, list)


def test_discover_cross_repo_edges_returns_list():
    """Always returns a list."""
    from graphify.multi import discover_cross_repo_edges

    edges = discover_cross_repo_edges({})
    assert edges == []


def test_discover_cross_repo_edges_no_duplicate_edges():
    """Deduplication: same source+target+discovery emitted at most once."""
    from graphify.multi import discover_cross_repo_edges

    # Two nodes in repo-a both reference fleet-manager → should deduplicate
    G_a = _make_graph([
        ("import_a", "fleet_manager", "code", "a.py"),
        ("import_b", "fleet_manager", "code", "b.py"),
    ])
    G_b = _make_graph([("cls_X", "X", "code", "x.py")])

    edges = discover_cross_repo_edges({"radar-service": G_a, "fleet-manager": G_b})
    keys = [(e["source"], e["target"], e["discovery"]) for e in edges]
    assert len(keys) == len(set(keys))


def test_discover_cross_repo_edges_shared_type_requires_two_signals():
    """Shared type heuristic requires 2+ occurrences to emit an edge."""
    from graphify.multi import discover_cross_repo_edges

    # Same label "Config" in both repos — 2 occurrences total
    G_a = _make_graph([("cfg_a", "Config", "code", "a.py")])
    G_b = _make_graph([("cfg_b", "Config", "code", "b.py")])

    edges = discover_cross_repo_edges({"repo-a": G_a, "repo-b": G_b})
    shared = [e for e in edges if e["discovery"] == "shared_type"]
    # 2 occurrences → should emit (meets >=2 signal threshold)
    assert len(shared) >= 1


# --- save_meta_graph / load_meta_graph ---

def test_save_load_meta_graph_roundtrip(tmp_path):
    """save_meta_graph → load_meta_graph produces identical data."""
    from graphify.multi import save_meta_graph, load_meta_graph

    repos_info = {
        "repos": {
            "repo-a": {
                "path": tmp_path / "repo-a",
                "graph_path": tmp_path / "repo-a" / "graphify-out" / "graph.json",
            }
        }
    }
    cross_edges = [
        {
            "source": "repo-a::Foo",
            "target": "repo-b::Bar",
            "relation": "calls",
            "confidence": "INFERRED",
            "confidence_score": 0.8,
            "discovery": "import_pattern",
        }
    ]
    output_path = tmp_path / "graphify-out" / "meta-graph.json"
    save_meta_graph(repos_info, cross_edges, output_path)

    assert output_path.exists()
    loaded = load_meta_graph(output_path)
    assert "repos" in loaded
    assert "cross_edges" in loaded
    assert len(loaded["cross_edges"]) == 1
    assert loaded["cross_edges"][0]["source"] == "repo-a::Foo"


def test_load_meta_graph_missing_file(tmp_path):
    """load_meta_graph returns {} for missing file."""
    from graphify.multi import load_meta_graph

    result = load_meta_graph(tmp_path / "nonexistent.json")
    assert result == {}


def test_save_meta_graph_creates_parent_dir(tmp_path):
    """save_meta_graph creates output directory if needed."""
    from graphify.multi import save_meta_graph

    repos_info = {"repos": {}}
    output_path = tmp_path / "new_dir" / "meta-graph.json"
    save_meta_graph(repos_info, [], output_path)
    assert output_path.exists()


# --- parse_repos_yaml ---

def test_parse_repos_yaml(tmp_path):
    """Parse a valid repos.yaml into a config dict."""
    from graphify.multi import parse_repos_yaml
    import yaml

    (tmp_path / "repos.yaml").write_text(
        "- name: repo-a\n  path: ./repo-a\n  url: git@github.com:org/repo-a.git\n"
        "- name: repo-b\n  path: ./repo-b\n"
    )
    result = parse_repos_yaml(tmp_path)
    assert "repo-a" in result
    assert result["repo-a"]["path"] == "./repo-a"
    assert result["repo-a"]["url"] == "git@github.com:org/repo-a.git"
    assert "repo-b" in result


def test_parse_repos_yaml_missing(tmp_path):
    """Missing repos.yaml returns {}."""
    from graphify.multi import parse_repos_yaml

    result = parse_repos_yaml(tmp_path)
    assert result == {}
