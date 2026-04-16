---
description: Scans the codebase and generates a verified structural codemap consumed by documentation agents. Must be run before any doc agents are dispatched. Never infers or assumes — only documents what exists in the code.
---

# Update Codemaps

Analyze the codebase structure and generate token-lean architecture snapshots for documentation agents.

## Step 1: Resolve Repositories

1. Check for `.claude/repos.yaml` in the workspace root
2. If found: iterate over each repo entry, verify the local path exists
3. If not found: treat current directory as a single-repo project
4. Run `git remote get-url origin` in each repo to capture the GitHub URL

**Output:** A list of `(repo_name, local_path, github_url)` tuples.

---

## Step 2: Scan Each Repository

For each repository, collect the following using `Glob`, `Grep`, `Read`, and `Bash` only. **Do not infer structure — only record what exists.**

### 2a. Project Metadata
- Language and framework (from lock files, manifests, entry points)
- Build system (Makefile, package.json scripts, pyproject.toml, Cargo.toml)
- Package manager (from lock files: package-lock.json → npm, yarn.lock → yarn, etc.)

### 2b. Entry Points and Routes
- Application entry points (main.*, index.*, app.*, etc.)
- API route definitions (scan for route decorators, router files, controller files)
- Record: `HTTP_METHOD /path → handler_function (file:line)`

### 2c. Component Map
- Services, controllers, repositories, middleware (from directory structure and imports)
- Record: `component_name → file_path (line_count)`
- Do NOT record internal implementation details

### 2d. Data Layer
- Database models / ORM definitions (file paths and model names only)
- Migration files (count and date range only)
- External data stores (from connection strings, client instantiation)

### 2e. Infrastructure
- Dockerfile(s) — base image and exposed ports
- docker-compose.yml — service names and dependencies
- Helm charts / K8s manifests — if present, list chart names
- CI/CD config — pipeline file paths only

### 2f. Dependencies
- External services (from API client instantiation, SDK imports)
- Message queues, caches, search engines (from connection code)
- Record: `dependency_name → purpose (detected from file:line)`

---

## Step 3: Write Codemaps

Write one codemap per repository to `.reports/codemaps/`:

**Single-repo:** `.reports/codemaps/codemap.md`
**Multi-repo:** `.reports/codemaps/{repo-name}.md`

### Codemap Format

```markdown
<!-- Generated: YYYY-MM-DD | Commit: abc1234 | Files scanned: N -->

# {Repo Name} Codemap

## Metadata
- **Language**: Python 3.11 / TypeScript 5.x / etc.
- **Framework**: FastAPI / Next.js / etc.
- **Build system**: Makefile / npm scripts / etc.
- **GitHub**: https://github.com/org/repo

## Entry Points
src/main.py — FastAPI application entry
src/cli.py — CLI entry point

## Routes
POST /api/users → controllers/user.py:create_user (line 45)
GET  /api/users/:id → controllers/user.py:get_user (line 67)
[... all routes ...]

## Components
| Component | Path | Lines | Purpose |
|-----------|------|-------|---------|
| UserService | src/services/user.py | 120 | User business logic |
| AuthMiddleware | src/middleware/auth.py | 45 | JWT validation |

## Data Layer
| Model | Path | Fields |
|-------|------|--------|
| User | src/models/user.py:12 | id, email, name, created_at |
| Order | src/models/order.py:8 | id, user_id, total, status |

Migrations: 14 files (2024-01-15 to 2025-03-01)
Database: PostgreSQL (from src/db/connection.py:5)

## Infrastructure
- Dockerfile: python:3.11-slim, port 8000
- docker-compose.yml: app, postgres, redis
- Helm chart: charts/service/ (values.yaml has 3 environments)

## External Dependencies
| Dependency | Purpose | Detected From |
|------------|---------|---------------|
| Stripe | Payment processing | src/services/payment.py:3 |
| SendGrid | Email delivery | src/services/email.py:7 |
| Redis | Session cache | src/cache/redis.py:1 |
```

### Token Budget

Each codemap must stay under **1500 tokens**. To achieve this:
- File paths and line references only — never paste code
- Signature-level detail for routes and components — never implementation
- Flat tables over nested structures
- Omit standard/obvious patterns (e.g., don't list every CRUD route if they follow a uniform pattern — summarize as "Standard CRUD for /api/users, /api/orders, /api/products")

---

## Step 4: Diff Detection

1. If previous codemaps exist in `.reports/codemaps/`:
   - Compare old vs new using line-by-line diff
   - If changes affect >30% of lines: show diff summary and ask user to confirm before overwriting
   - If changes ≤30%: update in place silently
2. If no previous codemaps exist: write fresh

---

## Step 5: Write Summary

Write `.reports/codemap-summary.txt`:

```
Codemap Update — YYYY-MM-DD
────────────────────────────
Repos scanned: 1 (or N for multi-repo)
Total files scanned: 142
  service-a: 89 files, codemap 1,200 tokens
  service-b: 53 files, codemap 900 tokens

Changes since last scan:
  + src/services/payment.py (new)
  + src/models/subscription.py (new)
  ~ src/routes/user.py (modified)
  - src/legacy/old_handler.py (removed)

New dependencies detected: Stripe (payment.py)
────────────────────────────
```

---

## Constraints

- **Only document what exists** — if a directory is empty or a pattern is not found, skip it
- **No implementation details** — file paths, signatures, and line counts only
- **No assumptions** — if you cannot determine a component's purpose from its name, path, and imports, mark it as `[UNCLEAR]`
- **Deterministic output** — running this twice on the same commit must produce identical codemaps