import json
from pathlib import Path
from graphify.build import build_from_json, build, prune_deleted, merge_graphs

FIXTURES = Path(__file__).parent / "fixtures"

def load_extraction():
    return json.loads((FIXTURES / "extraction.json").read_text())

def test_build_from_json_node_count():
    G = build_from_json(load_extraction())
    assert G.number_of_nodes() == 4

def test_build_from_json_edge_count():
    G = build_from_json(load_extraction())
    assert G.number_of_edges() == 4

def test_nodes_have_label():
    G = build_from_json(load_extraction())
    assert G.nodes["n_transformer"]["label"] == "Transformer"

def test_edges_have_confidence():
    G = build_from_json(load_extraction())
    data = G.edges["n_attention", "n_concept_attn"]
    assert data["confidence"] == "INFERRED"

def test_ambiguous_edge_preserved():
    G = build_from_json(load_extraction())
    data = G.edges["n_layernorm", "n_concept_attn"]
    assert data["confidence"] == "AMBIGUOUS"

def test_build_merges_multiple_extractions():
    ext1 = {"nodes": [{"id": "n1", "label": "A", "file_type": "code", "source_file": "a.py"}],
            "edges": [], "input_tokens": 0, "output_tokens": 0}
    ext2 = {"nodes": [{"id": "n2", "label": "B", "file_type": "document", "source_file": "b.md"}],
            "edges": [{"source": "n1", "target": "n2", "relation": "references",
                       "confidence": "INFERRED", "source_file": "b.md", "weight": 1.0}],
            "input_tokens": 0, "output_tokens": 0}
    G = build([ext1, ext2])
    assert G.number_of_nodes() == 2
    assert G.number_of_edges() == 1


# --- prune_deleted tests (US1) ---

def _two_file_graph():
    """Helper: graph with nodes from two source files."""
    import networkx as nx
    G = nx.Graph()
    G.add_node("n1", label="Foo", source_file="foo.py")
    G.add_node("n2", label="Bar", source_file="foo.py")
    G.add_node("n3", label="Baz", source_file="bar.py")
    return G


def test_prune_deleted_removes_nodes_from_deleted_file():
    G = _two_file_graph()
    G, removed = prune_deleted(G, ["foo.py"])
    assert "n1" not in G
    assert "n2" not in G
    assert "n3" in G
    assert set(removed) == {"n1", "n2"}


def test_prune_deleted_empty_list_is_noop():
    G = _two_file_graph()
    original_nodes = set(G.nodes())
    G, removed = prune_deleted(G, [])
    assert set(G.nodes()) == original_nodes
    assert removed == []


def test_prune_deleted_nonexistent_file_is_noop():
    G = _two_file_graph()
    original_nodes = set(G.nodes())
    G, removed = prune_deleted(G, ["ghost.py"])
    assert set(G.nodes()) == original_nodes
    assert removed == []


def test_prune_deleted_returns_same_graph_object():
    G = _two_file_graph()
    G2, _ = prune_deleted(G, ["foo.py"])
    assert G2 is G


# --- merge_graphs tests (US2) ---

def _simple_graph(nodes):
    """Helper: build a small graph from list of (id, label, source_file)."""
    import networkx as nx
    G = nx.Graph()
    for nid, label, src in nodes:
        G.add_node(nid, label=label, source_file=src)
    return G


def test_merge_graphs_prefixes_node_ids():
    G_a = _simple_graph([("cls_Foo", "Foo", "foo.py")])
    G_b = _simple_graph([("cls_Bar", "Bar", "bar.py")])
    combined = merge_graphs([("repo-a", G_a), ("repo-b", G_b)])
    assert "repo-a::cls_Foo" in combined
    assert "repo-b::cls_Bar" in combined
    assert "cls_Foo" not in combined
    assert "cls_Bar" not in combined


def test_merge_graphs_preserves_attributes():
    G_a = _simple_graph([("cls_Foo", "Foo", "foo.py")])
    combined = merge_graphs([("repo-a", G_a)])
    assert combined.nodes["repo-a::cls_Foo"]["label"] == "Foo"
    assert combined.nodes["repo-a::cls_Foo"]["_repo"] == "repo-a"


def test_merge_graphs_adds_cross_edges():
    G_a = _simple_graph([("cls_A", "A", "a.py")])
    G_b = _simple_graph([("cls_B", "B", "b.py")])
    cross = [{"source": "repo-a::cls_A", "target": "repo-b::cls_B",
               "relation": "calls", "confidence": "INFERRED"}]
    combined = merge_graphs([("repo-a", G_a), ("repo-b", G_b)], cross_edges=cross)
    assert combined.has_edge("repo-a::cls_A", "repo-b::cls_B")
