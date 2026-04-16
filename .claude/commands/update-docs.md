---
description: Generate or review documentation for this repository using specialized agents
---

**USAGE**: `/refresh-docs [TYPE]`

**ARGUMENTS**:
- `TYPE`: `TECHNICAL`, `PRODUCT`, `REPO`, or `ALL` (default: `ALL`)

---

## Non-Negotiable: Evidence-Based Only

Before doing anything else, internalize this constraint and pass it to every agent you spawn:

- Document only what exists in the codebase — verified with `Read`, `Grep`, `Glob`, or `Bash`
- Never infer, assume, or extrapolate — if you cannot point to a specific file or line, do not write it
- Never document intended or planned features — only the current state of the code
- If something is unclear or missing, use explicit markers:
  - `[UNCLEAR]` — exists but behaviour uncertain
  - `[NOT_FOUND]` — referenced elsewhere but no implementation found
- A document with gaps and markers is far more valuable than a complete-looking document built on assumptions
- **Omit entire sections** rather than filling them with guesses — a missing section is honest, a fabricated section is harmful

---

## Step 1: Resolve Repository Context

Determine single-repo vs multi-repo mode. This decision propagates to all agents.

### Single-repo detection
```bash
git remote get-url origin  # → https://github.com/org/repo
```
Set `REPO_URL` to the result. All file links resolve against this.

### Multi-repo detection
Check for `.claude/repos.yaml` in the workspace root:
```yaml
repos:
  service-a:
    url: https://github.com/org/service-a
    path: ./service-a          # local checkout path
  service-b:
    url: https://github.com/org/service-b
    path: ./service-b
```

If found, set `MULTI_REPO=true` and load the mapping. Every agent receives this mapping.

**If `.claude/repos.yaml` references repos that are not checked out locally, stop and ask the user.** Do not guess paths.

---

## Step 2: Generate Codemaps

Run `/update-codemaps` before dispatching any agents.

This produces `.reports/codemaps/` — a verified snapshot of the codebase that all agents consume. Do not skip this step. Agents must not re-scan the codebase independently.

In multi-repo mode, codemaps are generated per repo:
```
.reports/codemaps/
├── service-a.md
├── service-b.md
└── shared-lib.md
```

Wait for the codemap to complete before proceeding.

---

## Step 3: Build the Ownership Map

Before dispatching agents, build a single ownership map that eliminates duplication. Each piece of information has exactly one owner.

| Information | Owner | Others may |
|-------------|-------|-----------|
| Environment variables (full table) | `repo-docs-agent` → DEVELOPMENT.md | Link to DEVELOPMENT.md |
| API endpoints (full reference) | OpenAPI spec (canonical) | Link to spec |
| Architecture & component design | `tech-docs-agent` → architecture.md | Link to architecture.md |
| Deployment procedures | `tech-docs-agent` → deployment.md | Link to deployment.md |
| User-facing workflows | `product-docs-agent` → user-guide.md | Summarize in 1 sentence + link |
| CLI commands / make targets | `repo-docs-agent` → DEVELOPMENT.md | Link to DEVELOPMENT.md |
| Domain glossary terms | `product-docs-agent` → glossary-faq.md | Use terms, link to glossary |
| Security model | `tech-docs-agent` → security.md | Summarize in 1 sentence + link |

**Rule: If you are not the owner, write at most one sentence and link to the owner.** Never duplicate tables, lists, or detailed descriptions across agents.

Pass this ownership map to every agent at dispatch time.

---

## Step 4: Identify Sources of Truth

| Source | Generates |
|--------|-----------|
| `package.json` / `Makefile` / `pyproject.toml` | Available commands reference |
| `.env.example` or config files | Environment variable documentation |
| `openapi.yaml` / route files | API endpoint reference |
| Source code exports | Public API documentation |
| `Dockerfile` / `docker-compose.yml` | Infrastructure setup docs |

Generate a script reference table from the build system and include it in the dispatch context for all agents:

```markdown
| Command | Description | Source |
|---------|-------------|--------|
| `make dev` | Start development server | Makefile:12 |
| `make test` | Run test suite | Makefile:18 |
```

---

## Step 5: Dispatch Agents

Based on `TYPE`, dispatch the following agents. Each agent receives:
1. The ownership map from Step 3
2. The script reference from Step 4
3. The repo context (single/multi + URLs) from Step 1
4. Path to their codemap(s) in `.reports/codemaps/`

**TYPE=ALL (default)** — dispatch all three in parallel:
- `tech-docs-agent`
- `product-docs-agent`
- `repo-docs-agent`

**TYPE=TECHNICAL** — dispatch `tech-docs-agent` only
**TYPE=PRODUCT** — dispatch `product-docs-agent` only
**TYPE=REPO** — dispatch `repo-docs-agent` only

---

## Agent Ownership

Each agent owns a strict set of output paths. Agents must not write outside their owned paths.

| Agent | Owns |
|-------|------|
| `tech-docs-agent` | `docs/technical/` |
| `product-docs-agent` | `docs/product/` |
| `repo-docs-agent` | `README.md`, `DEVELOPMENT.md`, `CONTRIBUTING.md`, `CHANGELOG.md` |

---

## Output Structure

```
docs/
├── technical/
│   ├── architecture.md
│   ├── deployment.md
│   ├── observability.md
│   ├── security.md
│   ├── testing.md
│   └── runbooks/
├── product/
│   ├── executive-1pager.md
│   ├── user-guide.md
│   ├── glossary-faq.md
│   └── version-history.md
README.md
DEVELOPMENT.md
CONTRIBUTING.md
CHANGELOG.md
```

**Not all files will be generated.** Agents select files based on what the codemap evidence supports. An agent that finds no evidence for a file must skip it entirely — never create empty or placeholder files.

---

## Step 6: Show Summary

After all agents complete:

```
Documentation Update
──────────────────────────────
Created:  docs/technical/architecture.md (87 lines)
Created:  docs/product/executive-1pager.md (42 lines)
Updated:  DEVELOPMENT.md (env vars table refreshed)
Skipped:  docs/technical/observability.md (no telemetry found)
Skipped:  docs/product/version-history.md (no migrations found)
Flagged:  docs/product/user-guide.md — [NOT_FOUND] markers present
──────────────────────────────
Files with markers needing human review:
  - docs/product/user-guide.md:34 — [NOT_FOUND] auth flow
```

---

## Rules

- **Single source of truth**: Each fact lives in one file only. Others link to it.
- **Preserve manual sections**: Only update generated sections; leave hand-written prose intact.
- **Mark generated content**: Use `<!-- AUTO-GENERATED -->` markers around generated sections.
- **Omit, don't fabricate**: A missing section is better than a wrong section.
- **Length discipline**: No single file should exceed 500 lines. If it does, the agent must split it or cut scope.