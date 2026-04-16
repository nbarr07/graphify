---
name: doc-templates-product
description: Load when writing product-facing, non-technical documentation for business stakeholders. Provides file catalogue, templates, and writing standards for executive summaries, user guides, and glossaries.
---

## File Catalogue

| File | Diataxis type | Write when | Max lines |
|------|--------------|------------|-----------|
| `docs/product/executive-1pager.md` | Explanation | ≥3 user-facing capabilities found | 120 |
| `docs/product/user-guide.md` | Tutorial | ≥2 traceable workflows found | 200 |
| `docs/product/glossary-faq.md` | Reference | ≥5 domain-specific terms found | 150 |
| `docs/product/version-history.md` | Reference | Git tags, migrations, or CHANGELOG found | 100 |

**If the evidence gate (defined in product-docs-agent) is not met, do not create the file.**

---

## Writing Standards

- Describe what users can accomplish, not how it is implemented
- No file paths, function names, class names, or technical architecture
- No performance metrics or ROI claims without hard evidence in code
- Tables over prose for structured information
- Every section must trace to codemap evidence — if you cannot point to the codemap entry that supports a claim, delete the claim

---

## Cross-Reference Rules

These topics are owned by other agents. **Do not duplicate — link instead.**

| Topic | Link to | Maximum in your file |
|-------|---------|---------------------|
| Environment variables | `DEVELOPMENT.md` | Do not mention |
| API parameters/schemas | OpenAPI spec | One example request per workflow |
| Architecture | `docs/technical/architecture.md` | One sentence summary |
| Deployment | `docs/technical/deployment.md` | Do not mention |
| CLI commands | `DEVELOPMENT.md` | Do not mention |
| Security model | `docs/technical/security.md` | One sentence summary |

---

## Templates

### executive-1pager.md

**Quadrant:** Explanation
**Max lines:** 80
**Purpose:** Orient a stakeholder in under 2 minutes of reading.

```markdown
---
title: Executive Summary — {Project Name}
last_updated: YYYY-MM-DD
last_commit: abc1234
---

## What This Is

[1-2 sentences: what the product does and who it serves. Derived from routes, models, and README.]

## Key Capabilities

[Table format. One row per capability area. Derived from route resource groupings.]

| Capability | Description |
|------------|-------------|
| {Resource area} | {What users can do — 1 sentence} |

[3-7 rows maximum. If you have more than 7, group related capabilities.]

## Target Users

[Derived from auth roles, permission checks, or distinct API consumer patterns.]

- **{Role}**: {What this user type does with the product — 1 sentence}

[2-4 roles maximum.]

## Current Status

- **Version**: {from git tag or API prefix — omit if not found}
- **Status**: {Active / Beta / Internal — from feature flags or deployment config}

[Do not include metrics, uptime, or adoption numbers unless found in code.]

## Technical Documentation

For architecture, deployment, and API details, see [Technical Docs](../technical/).
```

**Omission rules:**
- No "Target Users" section if no auth roles or distinct consumer patterns found
- No "Current Status" section if no version signals found
- If only 1-2 capabilities found, this file probably shouldn't exist — check the evidence gate

---

### user-guide.md

**Quadrant:** Tutorial
**Max lines:** 200
**Purpose:** Walk a user through real workflows with concrete examples.

```markdown
---
title: User Guide — {Project Name}
last_updated: YYYY-MM-DD
last_commit: abc1234
---

## Overview

[1-2 sentences: what users can accomplish. No architecture.]

**Full API Reference:** [{spec location}]({link to openapi.yaml or /docs})

---

## {Workflow Name}

**What you accomplish**: {Business outcome in one sentence}

**Prerequisites**: {Access or data needed — keep to one line}

### Steps

1. {Business action — e.g., "Create a new project"}

   ```bash
   curl -X POST https://api.example.com/v1/projects \
     -H "Authorization: Bearer $TOKEN" \
     -d '{"name": "My Project"}'
   ```

   → Returns: {Brief description of successful response — 1 line}

2. {Next business action}

   [Example request if multi-step]

   → Returns: {Brief description}

**Result**: {What the user has accomplished}

**Full parameters**: See [`POST /v1/projects`]({link to spec}) for all options.

---

[Repeat for each workflow — maximum 4 workflows per file]
```

**Omission rules:**
- Do not create "workflows" from single CRUD endpoints — a POST endpoint alone is not a workflow
- Maximum 4 workflows — if more exist, pick the most important and note others exist
- Omit request examples if the API has no authentication (trivial APIs don't need a user guide)
- Every example request must use realistic field values, not "string" or "example"

---

### glossary-faq.md

**Quadrant:** Reference
**Max lines:** 150
**Purpose:** Define domain terms and answer common questions.

```markdown
---
title: Glossary & FAQ
last_updated: YYYY-MM-DD
last_commit: abc1234
---

## Glossary

[Alphabetical. Only domain-specific terms — not standard programming terms.]

| Term | Definition |
|------|-----------|
| **{Term}** | {Non-technical definition in 1-2 sentences} |

## FAQ

[Only include questions that can be answered from code evidence.]

**{Question}**
{Answer in 1-3 sentences. Plain language.}
```

**Omission rules:**
- Skip generic terms: "User", "Database", "API", "Config", "Service"
- Skip terms that are self-explanatory from their name
- FAQ section is optional — omit entirely if no genuine FAQs can be derived from code
- Do not invent questions — only include questions that arise naturally from the domain model

---

### version-history.md

**Quadrant:** Reference
**Max lines:** 100
**Purpose:** Track what changed and what users need to do about it.

```markdown
---
title: Version History
last_updated: YYYY-MM-DD
last_commit: abc1234
---

## Current Version

{Version identifier} — {date if known}

Source: {git tag / API prefix / schema version — state where you found it}

## Recent Changes

| Version | Date | What Changed | User Action |
|---------|------|-------------|-------------|
| {ver} | {date} | {Business impact — 1 sentence} | None / {action} |

[Maximum 10 most recent versions. Link to CHANGELOG for full history if it exists.]

## Breaking Changes

[Only if breaking changes exist. Otherwise omit this section entirely.]

**{Version}**: {What stopped working and what users must do — 2-3 sentences max}
```

**Omission rules:**
- Skip this file entirely if there are no git tags, no migrations, and no CHANGELOG
- Do not list internal refactoring as version changes — only user-visible changes
- "Migration Notes" section only appears if actual migration steps are required by users