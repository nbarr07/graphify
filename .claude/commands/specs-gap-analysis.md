---
description: Incrementally sync feature specs with latest implemented features by performing code→spec gap analysis (generic, repo‑agnostic)
---

AI - DON'T CHANGE THIS FILE

Goal
- Keep designated spec documents incrementally up to date with repository code, with minimal diffs.
- Make precise, surgical edits that preserve existing section order, wording, and formatting style.

Inputs
- Optional: a brief summary of what changed (e.g., features, endpoints, entities).
- Optional: environment or ARGUMENTS to scope the run
  - SPEC_FILES: comma‑separated list of spec files to update (defaults to discovering `**/spec.md` and `**/ux-spec.md`).
  - DIFF_BASE: git ref to diff against (default: `main`, fallback: `origin/main`).

Execution Flow (main)
1) Identify change set
   - Resolve diff base: prefer `main`; if missing, use `origin/main`.
   - Collect changed files since base: `git diff --name-only --diff-filter=AMDR <BASE>...HEAD`.
   - Filter to implementation code (exclude docs/spec/tests unless relevant to behaviour).

2) Discover implemented changes (framework‑agnostic)
   - Endpoints/contracts: Prefer OpenAPI/Swagger files; else parse common routing constructs (FastAPI/Flask decorators, Express/Nest routers, Rails routes, Spring mappings, Go routers).
   - Entities/models: Parse common model definitions (Pydantic/dataclasses, TS interfaces/types or Zod, JPA/validation‑annotated classes, ActiveRecord models).
   - Flows: Skim integration/e2e tests and README/quickstarts for user‑visible behaviours.

3) Read current specs
   - Determine SPEC_FILES (argument or discover typical locations: `**/spec.md`, `**/ux-spec.md`).
   - Load each spec and index sections: Execution Flow, Quick Guidelines, Personas, Views, Activities, User Scenarios, Acceptance Scenarios, Edge Cases, Requirements (FR/NFR), Key Entities, Contracts, Review Checklist, Mermaid sequences.

4) Gap analysis (code → spec)
   - Contracts/Endpoints: Add missing implemented endpoints; move removed ones to a “Removed/Planned” note if present.
   - Entities/Models: Ensure new/changed core entities appear in Key Entities with succinct definitions.
   - Activities/Flows: Ensure newly added user flows (upload/import/create/list/update) are present with correct endpoint references.
   - UX/Sequences: Ensure client→API→persistence diagrams reflect current posture (UI/API) and use GitHub‑compatible Mermaid (simple arrows, optional Note lines only).
   - Acceptance/Edge cases: Add scenarios that cover new behaviours; avoid deleting existing scenarios.

5) Draft incremental patches (minimal diffs)
   - Do NOT rewrite entire documents. Patch only:
     - Missing/incorrect endpoints under Contracts.
     - Activities bullets (add/update) and Acceptance/Edge cases (additive only).
     - Mermaid sequences (simplify to render reliably on GitHub).
     - Posture wording (UI/API) only when clearly divergent from current reality.
   - Preserve headings, spacing, bullet style, and existing ordering.

6) Validate
   - No TODO/placeholder tokens remain.
   - Dates in headers remain accurate; bump only if materially changed (YYYY‑MM‑DD).
   - Mermaid blocks render (no alt/opt blocks; prefer Note lines and simple arrows).
   - Implemented vs Planned/Removed clearly delineated in Contracts.

7) Output
   - summarise the code changes from git diff..HEAD analysis
   - Apply patches to SPEC_FILES.
   - Summarize changes (endpoints, activities, scenarios, sequences) and list touched files.
   - Suggest a commit message, e.g.: `docs(specs): incremental gap‑sync for specs; endpoints, activities, sequences`.

Style & Constraints
- Keep existing structure; don’t rename sections unless necessary.
- Keep changes narrowly scoped; avoid editorial rewrites.
- If something can’t be confidently inferred, prefer adding an Acceptance Scenario or Edge Case over inventing requirements.

Safety & Review
- If the diff exceeds ~80 lines in any one file, pause and present a summary for user confirmation before proceeding.
- Never delete sections unless they are exact duplicates.
