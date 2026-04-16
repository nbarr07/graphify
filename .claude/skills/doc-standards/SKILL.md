---
name: doc-standards
description: Load when writing any documentation. Provides evidence-based writing standards, transparency markers, and quality checklist shared across all documentation agents.
---

## Evidence-Based Only

Document only what exists in the codebase. Never infer, assume, or extrapolate. If you cannot point to a specific file or line that confirms a claim, do not write it.

Never document intended or planned features — only the current state of the code.

**The omission rule:** It is always better to omit a section than to fill it with uncertain content. A document with 3 solid sections is more valuable than one with 6 sections where 3 are guesswork.

---

## Project Ecosystem Detection

Detect ecosystem from files present. Use appropriate commands in examples.

**Build System:**
1. Makefile → `make [target]` (help: `make help`)
2. package.json scripts → `npm run [script]` / `yarn` / `pnpm`
3. pyproject.toml → `poetry` / `uv` / `pip`
4. Cargo.toml → `cargo [command]`
5. go.mod → `go [command]`

**Package Manager** (detect from lock files):
- `package-lock.json` → npm
- `yarn.lock` → yarn
- `pnpm-lock.yaml` → pnpm
- `poetry.lock` → poetry
- `uv.lock` → uv

**API Documentation — link to canonical source, never duplicate:**
- OpenAPI/Swagger → `/docs` endpoint + `openapi.yaml`
- gRPC → proto files in `proto/` directory

**Container/Orchestration:**
- Docker: `Dockerfile`, `docker-compose.yaml`
- Helm: `charts/`, `Chart.yaml`
- ArgoCD: `*.yaml` with `kind: Application`
- Kustomize: `kustomization.yaml`

---

## Transparency Markers

Use sparingly — only when you genuinely cannot determine something from code.

| Marker | When to use |
|--------|------------|
| `[UNCLEAR]` | Exists in code but behaviour uncertain |
| `[NOT_FOUND]` | Referenced elsewhere but no implementation found |

**Do not use markers as an excuse to include speculative content.** If something is unclear, mark it and move on. Do not write a paragraph explaining what it might be.

---

## Single Source of Truth — Ownership Rules

Every piece of information has exactly one documentation owner. If you are not the owner, you may include **at most one sentence** and a link.

**How to check:** Before writing any table, list, or detailed description, ask: "Am I the designated owner of this information?" If not, write a link instead.

Common violations to avoid:
- Tech agent and repo agent both listing environment variables → **Repo agent owns this**
- Product agent and tech agent both describing the API → **OpenAPI spec owns this**
- Multiple agents describing the deployment process → **Tech agent owns this**

---

## Strict Line Limit Enforcement

**CRITICAL RULE: Line limits are HARD STOPS, not suggestions.**

Before writing any file, know your agent's line limits:
- `tech-docs-agent`: architecture.md (500), deployment.md (250), observability.md (200), security.md (120), testing.md (120), runbooks (80 each)
- `product-docs-agent`: executive-1pager.md (120), user-guide.md (200), glossary-faq.md (150), version-history.md (100)
- `repo-docs-agent`: README.md (150), DEVELOPMENT.md (150), CONTRIBUTING.md (100)

**Enforcement procedure:**
1. **Before writing:** Outline sections and estimate lines per section
2. **During writing:** Count lines after each major section
3. **After writing:** Run `wc -l` on the file to verify
4. **If exceeded:** You MUST either:
   - Cut entire sections (prioritize operational needs over comprehensive coverage)
   - Reduce detail (replace explanations with links to source code)

**What counts toward line limit:**
- All content lines (text, code blocks, headings, blank lines)
- Frontmatter does NOT count (lines between `---` markers)

**Example validation:**
```bash
# Count lines excluding frontmatter
tail -n +$(grep -n "^---$" deployment.md | sed -n 2p | cut -d: -f1) deployment.md | wc -l
```

If file exceeds limit, **STOP and fix immediately**. Do not proceed to next file.

---

## Never Copy Code or Configuration

**CRITICAL RULE: Link to source code, NEVER copy it into documentation.**

### What NOT to include

**NEVER copy:**
- Function implementations or class definitions
- YAML configuration files or snippets (Helm values, K8s manifests, docker-compose)
- Kubernetes resource definitions (Deployments, Services, ConfigMaps)
- Environment variable values from .env files
- Code showing "how to calculate" or "build process" (algorithms, build steps)
- API response schemas or payload structures
- Database schemas or migration SQL
- Any code block longer than 5 lines

**Instead, use links:**
```markdown
**Resource Configuration**: See [values.yaml](https://github.com/org/repo/blob/main/charts/service/values.yaml#L130-L151)

**Build Process**: See [Dockerfile](https://github.com/org/repo/blob/main/backend/Docker/Dockerfile)

**HMAC Authentication**: Implementation in [servicely.py:26-46](https://github.com/org/repo/blob/main/backend/src/service/clients/servicely.py#L26-L46)
```

### What you CAN include (minimally)

**Acceptable inline code (max 5 lines):**
- Example API requests: `curl -X POST /v1/endpoint -H "Authorization: Bearer $TOKEN"`
- Environment variable names only: `OAUTH_DISCOVERY=https://...` (not full .env file)
- Short snippets showing usage pattern (not implementation)

**If you find yourself writing a code block longer than 5 lines, STOP and replace it with a link.**

---

## Triviality Filters — What NOT to Document

**CRITICAL RULE: Skip documenting standard tools, generic patterns, and trivial operations.**

### Do NOT document (Kubernetes/DevOps):
- How to create Kubernetes secrets (`kubectl create secret`)
- How to scale deployments (`kubectl scale`)
- Standard kubectl commands that operators should already know
- Generic Helm installation procedures
- Standard health check configurations (readiness/liveness probes)
- Generic container security contexts (unless unusual)
- Standard image pull secrets
- Generic resource requests/limits (document only if unusual values)

### Do NOT document (Authentication/Security):
- Generic OAuth 2.0 or OIDC flow explanations
- JWT token structure basics
- Standard TLS/HTTPS configuration
- Generic webhook secret mechanisms (unless custom implementation)
- Standard network policy patterns
- Generic RBAC concepts

### Do NOT document (Testing/Development):
- Standard test framework usage (pytest, jest, etc.)
- Generic test patterns (mocking, fixtures) unless project-specific
- Standard linting/formatting tool configuration
- Generic pre-commit hook setup
- Standard CI/CD patterns (checkout, install, test, deploy)

### Do NOT document (Generic Tools):
- Python/Node/Go installation
- Docker installation
- IDE setup (unless project requires specific plugins)
- Git basics
- Standard package manager usage

### DO document (Project-Specific Focus):
**For security docs, focus on:**
- Project-specific roles and their scopes (e.g., `fleet-operator` role)
- Project-specific ACL commands (`make get-acl`, `make get-acl-prod`)
- Links to credential retrieval documentation specific to this organization
- Custom authentication flows unique to this project
- Non-standard security decisions and why they were made

**For deployment docs, focus on:**
- GitOps patterns specific to this organization's infrastructure
- Multi-repo deployment coordination
- Environment-specific override patterns
- Non-standard deployment procedures

**For testing docs, focus on:**
- Project-specific test setup (custom fixtures, non-standard database setup)
- Unique testing patterns developed for this codebase
- Integration test requirements specific to external dependencies

**When in doubt, ask: "Would a competent engineer already know this?" If yes, skip it or link to external docs.**

---

## Quality Checklist

Before finalising any document, verify:

**Critical — must fix**
- [ ] All technical claims verified against actual code
- [ ] No features documented that do not exist in the codebase
- [ ] No sections filled with assumptions or placeholder content
- [ ] Links always point to actual source code files, never to `.reports/` or codemap files
- [ ] Document written to its correct output path
- [ ] No information duplicated from another agent's owned files — links used instead
- [ ] **File is within its line limit (verified with `wc -l`)**
- [ ] **No code blocks longer than 5 lines (replaced with links)**
- [ ] **No generic/trivial information included**

**Important — should fix**
- [ ] Logical hierarchy and scannable structure
- [ ] Active voice and present tense throughout
- [ ] YAML frontmatter present (title, last_updated, last_commit)
- [ ] Links to related documentation where relevant
- [ ] Every section traceable to a codemap entry or source file

**Quality improvements**
- [ ] Diagrams simple, accurate, with descriptive captions
- [ ] No redundant explanations
- [ ] Terminology consistent across the document

---

## Source Code References

Always link to actual source code files, never to codemap files (which are build artifacts).

### Repository Resolution

**Single-repo mode:**
- Run `git remote get-url origin` to get the repository URL
- Convert to GitHub web format: `git@github.com:owner/repo.git` → `https://github.com/owner/repo`

**Multi-repo mode:**
- Load `.claude/repos.yaml` from workspace root
- All file paths must include repo prefix: `service-a/src/auth.py`
- Resolve URLs from the repos.yaml mapping

### GitHub URL Format

| Type | Format |
|------|--------|
| Single line | `{repo-url}/blob/main/{path}#L{line}` |
| Line range | `{repo-url}/blob/main/{path}#L{start}-L{end}` |
| Directory | `{repo-url}/tree/main/{path}` |
| Entire file | `{repo-url}/blob/main/{path}` |

### When to Use Links vs Inline Code

**Use links for:** function/class definitions, business logic locations, configuration constants, implementation details.

**Use inline code for:** API request/response examples, configuration file templates, CLI commands, short examples under 5 lines.

**Never inline:** function implementations, complex algorithms, code that will drift from source, K8s manifests.

---

## API Documentation

**Never duplicate API specifications in documentation.**

Link to canonical source (OpenAPI spec, Swagger UI, proto files). In documentation, include only:
- Example requests with realistic values
- Links to spec for full parameter lists
- High-level endpoint purposes

---

## Frontmatter

Every document must include YAML frontmatter:

```markdown
---
title: [Document title]
last_updated: YYYY-MM-DD
last_commit: [git short SHA]
---
```