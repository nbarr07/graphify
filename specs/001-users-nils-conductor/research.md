# Research: Graphify Fork — Multi-Repo + Doc Pipeline Integration

## Decision 1: repos.yaml parsing — PyYAML vs stdlib

**Decision**: Use `PyYAML` (`import yaml`) for `repos.yaml` parsing.  
**Rationale**: YAML is the natural format for the workspace config (matches Helm/ArgoCD tooling the user already uses). PyYAML is not currently in `graphify`'s dependencies — it must be added to `pyproject.toml`. Alternatives:
- **TOML** (stdlib in 3.11+): rejected — not compatible with Python 3.10 constraint.
- **JSON**: simpler but `repos.yaml` implies YAML and the spec is explicit on filename.
- **Alternatives considered**: `ruamel.yaml` (preserves comments) — overkill for a simple config read.

**Action**: Add `pyyaml` to `dependencies` in `pyproject.toml`.

---

## Decision 2: detect_incremental(root) — Path | list[Path] union type

**Decision**: Modify `detect_incremental` to accept `Path | list[Path]` using a `Union` annotation (not `|` operator, which requires 3.10+ but is safe here since `requires-python = ">=3.10"`).  
**Rationale**: The existing `detect()` function takes a single `Path`. For multi-repo, we want `detect_incremental` to accept a list so the caller can treat multiple repos uniformly. The implementation iterates the list, calls `detect()` per path, and merges `files` dicts by category. Manifest lookup per-repo uses `{root}/graphify-out/manifest.json` — each root has its own manifest.  
**Alternatives considered**: A separate `detect_incremental_multi()` — rejected to keep the API surface small.

---

## Decision 3: Cross-repo edge discovery — heuristic ordering and confidence scoring

**Decision**: Run four heuristics in order; emit edges with `confidence: "INFERRED"` and `confidence_score` per heuristic. Shared-type edges require 2+ signals (label match + at least one co-occurrence signal).

| Heuristic | discovery tag | confidence_score |
|-----------|--------------|-----------------|
| Import patterns (code node `imports` another repo's package name) | `import_pattern` | 0.8 |
| Shared types (identical label in 2+ repos, 2+ signals) | `shared_type` | 0.65 |
| Helm/K8s service URL references in `values.yaml` | `helm_ref` | 0.7 |
| ArgoCD Application manifests referencing other repo URLs | `argocd_ref` | 0.75 |

**Rationale**: These scores reflect decreasing ambiguity. Import patterns are explicit; shared type names could be coincidental, hence requiring 2 signals and a lower score. Scores are advisory — they flow into the meta-graph JSON and are shown to the user during validation.  
**Alternatives considered**: LLM-assisted edge inference — explicitly out of scope per spec.

---

## Decision 4: merge_graphs() — transient, not persisted

**Decision**: `merge_graphs(graphs, cross_edges)` builds a temporary `nx.DiGraph` with `{repo_name}::` prefixed node IDs. It is never written to disk — callers use it only for cross-repo analysis (e.g., `analyze()` on the combined graph).  
**Rationale**: Persisting a merged graph would duplicate data already in per-repo `graph.json` files and create staleness problems. The meta-graph JSON stores only the cross-repo edge list, not the full merged graph.

---

## Decision 5: Auto-detect mode — where the check lives

**Decision**: The auto-detect logic (`graphify-out/graph.json` exists → `UPDATE_MODE`) belongs in `graphify/skill.md` (SKILL.md Step 1.5), not in `__main__.py` CLI. The CLI `--update` flag continues to work as an explicit override.  
**Rationale**: The skill orchestrates the pipeline from Claude Code; the CLI is for direct invocation. Auto-detect in the skill matches the "always-on" usage pattern. The Python library functions remain mode-agnostic — callers decide which detect function to call.

---

## Decision 6: prune_deleted() placement — build.py not detect.py

**Decision**: `prune_deleted(G, deleted_files)` lives in `build.py`.  
**Rationale**: It operates on an `nx.Graph` object, which is a build-layer concern. `detect.py` already computes `deleted_files` in `detect_incremental()` — the caller passes this list to `prune_deleted` after loading the existing graph.

---

## Resolved NEEDS CLARIFICATION items

All items from spec were concrete. No NEEDS CLARIFICATION flags were present. Research focused on dependency and API surface decisions.
