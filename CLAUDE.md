# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`graphify` is a Python library and Claude Code skill that generates knowledge graphs from codebases. Pipeline: `detect → extract → build_graph → cluster → analyze → report → export`. The package is published as `graphifyy` on PyPI (double-y to avoid conflicts).

The skill file lives at `graphify/skill.md` (and platform variants like `skill-codex.md`). The CLI entry point is `graphify/__main__.py`.

## Commands

```bash
# Install for development
pip install -e ".[all]"

# Run tests
pytest tests/ -q --tb=short

# Run a single test file
pytest tests/test_languages.py -q

# Run the CLI
graphify [path]                  # full pipeline
graphify [path] --update         # incremental rebuild
graphify [path] --watch          # rebuild on file changes
graphify install [--platform X]  # write platform skill files
```

No Makefile. CI runs Python 3.10 and 3.12 via `.github/workflows/ci.yml`.

## Architecture

Each pipeline stage is a single function in its own module. They pass plain Python dicts and NetworkX graphs — no shared state, no side effects outside `graphify-out/`.

| Module | Key function | Role |
|--------|-------------|------|
| `detect.py` | `collect_files(root)` | File discovery and sensitivity filtering |
| `extract.py` | `extract(path)` | AST extraction via tree-sitter (25+ languages) |
| `build.py` | `build_graph(extractions)` | Merges extraction dicts into `nx.Graph` |
| `cluster.py` | `cluster(G)` | Leiden/Louvain community detection |
| `analyze.py` | `analyze(G)` | God nodes, surprising connections, questions |
| `report.py` | `render_report(G, analysis)` | Writes `GRAPH_REPORT.md` |
| `export.py` | `export(G, out_dir, ...)` | HTML, JSON, SVG, GraphML, Obsidian, Neo4j |
| `cache.py` | `check_semantic_cache` | SHA256 cache to skip unchanged files |
| `validate.py` | `validate_extraction(data)` | Schema enforcement before `build_graph()` |
| `security.py` | validation helpers | URL/path/label sanitization |
| `serve.py` | `start_server(graph_path)` | MCP stdio server + BFS/DFS graph queries |
| `ingest.py` | `ingest(url, ...)` | URL fetching for papers, tweets, videos |
| `watch.py` | `watch(root, flag_path)` | Incremental rebuild watcher |

## Extraction schema

Every extractor returns this structure (enforced by `validate.py`):

```json
{
  "nodes": [{"id": "...", "label": "...", "source_file": "...", "source_location": "L42"}],
  "edges": [{"source": "...", "target": "...", "relation": "calls|imports|uses|...", "confidence": "EXTRACTED|INFERRED|AMBIGUOUS"}]
}
```

Confidence labels: `EXTRACTED` = explicit in source, `INFERRED` = reasonable deduction (call-graph second pass), `AMBIGUOUS` = uncertain, flagged in report.

## Adding a new language extractor

1. Add `extract_<lang>(path: Path) -> dict` in `extract.py` (tree-sitter parse → walk nodes → call-graph second pass for INFERRED `calls` edges).
2. Register the suffix in `extract()` dispatch and `collect_files()`.
3. Add the suffix to `CODE_EXTENSIONS` in `detect.py` and `_WATCHED_EXTENSIONS` in `watch.py`.
4. Add the tree-sitter package to `pyproject.toml` dependencies.
5. Add a fixture file to `tests/fixtures/` and tests to `tests/test_languages.py`.

## Security

All external input goes through `graphify/security.py`:
- URLs → `validate_url()` (http/https only, blocks `file://` redirects)
- Graph file paths → `validate_graph_path()` (must resolve inside `graphify-out/`)
- Node labels → `sanitize_label()` (strips control chars, caps 256 chars, HTML-escapes)

## Platform install system

`graphify install --platform X` writes platform-specific skill/hook/config files. Supported platforms include Claude Code, Codex, Cursor, VS Code Copilot Chat, OpenCode, Gemini CLI, Aider, Kiro, and others. Platform-specific skill files are in `graphify/skill-*.md`. The install logic for each platform lives in `graphify/__main__.py`.

## Output directory

All outputs go to `graphify-out/` in the scanned root:
- `graph.json` — NetworkX node-link format
- `GRAPH_REPORT.md` — audit trail (god nodes, surprising connections, confidence breakdown)
- `graph.html` — interactive vis.js visualization
- `cache/` — SHA256 semantic cache

## Active Technologies
- Python 3.10+ (matches `requires-python = ">=3.10"` in pyproject.toml) + networkx, PyYAML (for `repos.yaml` parsing), tree-sitter (existing), graspologic/python-louvain (existing clustering) (001-users-nils-conductor)
- JSON files on disk (`graph.json`, `meta-graph.json`, `manifest.json`); no database (001-users-nils-conductor)

## Recent Changes
- 001-users-nils-conductor: Added Python 3.10+ (matches `requires-python = ">=3.10"` in pyproject.toml) + networkx, PyYAML (for `repos.yaml` parsing), tree-sitter (existing), graspologic/python-louvain (existing clustering)
