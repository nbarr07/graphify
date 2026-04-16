---
description: Validate generated documentation against all established rules, standards, and templates. Catches violations and provides actionable fix recommendations.
---

**USAGE**: `/validate-docs [SCOPE]`

**ARGUMENTS**:
- `SCOPE`: `TECHNICAL`, `PRODUCT`, `REPO`, or `ALL` (default: `ALL`)

---

## Purpose

This command validates generated documentation to ensure compliance with:
- Line limit enforcement (CRITICAL)
- Code block length restrictions (no blocks > 5 lines)
- No configuration/code copying (link instead)
- Triviality filters (no generic content)
- Diataxis quadrant purity (no mixing)
- Single source of truth (no duplication)
- Evidence-based content (no assumptions)
- Proper source code links (no codemap references)
- Frontmatter compliance
- Correct file ownership and location

Run this command after `/update-docs` completes to verify documentation quality before committing.

---

## Step 1: Determine Validation Scope

Based on the `SCOPE` argument, identify which documentation files to validate:

**SCOPE=ALL (default)**:
- `docs/technical/*.md`
- `docs/product/*.md`
- `README.md`, `DEVELOPMENT.md`, `CONTRIBUTING.md`, `CHANGELOG.md`

**SCOPE=TECHNICAL**:
- `docs/technical/*.md`

**SCOPE=PRODUCT**:
- `docs/product/*.md`

**SCOPE=REPO**:
- `README.md`, `DEVELOPMENT.md`, `CONTRIBUTING.md`, `CHANGELOG.md`

---

## Step 2: Discover Documentation Files

Use Glob to find all documentation files in scope:

```bash
# Technical docs
find docs/technical -name "*.md" -type f

# Product docs
find docs/product -name "*.md" -type f

# Repo docs
find . -maxdepth 1 -name "*.md" -type f | grep -E '(README|DEVELOPMENT|CONTRIBUTING|CHANGELOG)'
```

If no files are found, report:
```
No documentation files found in scope: {SCOPE}
Run `/update-docs` first to generate documentation.
```

---

## Step 3: Load Validation Rules

Before dispatching the validator agent, prepare a validation context that includes:

1. **Line limits per file** (from doc-templates skills):
   ```
   Technical: architecture.md (500), deployment.md (200), observability.md (300),
              security.md (120), testing.md (120), runbooks (80)
   Product: executive-1pager.md (120), user-guide.md (200), glossary-faq.md (150),
            version-history.md (100)
   Repo: README.md (150), DEVELOPMENT.md (150), CONTRIBUTING.md (100)
   ```

2. **Ownership map** (from update-docs.md):
   ```
   tech-docs-agent → docs/technical/
   product-docs-agent → docs/product/
   repo-docs-agent → README.md, DEVELOPMENT.md, CONTRIBUTING.md, CHANGELOG.md
   ```

3. **Rule sources**:
   - Core standards: `.claude/skills/doc-standards/SKILL.md`
   - Diataxis framework: `.claude/skills/diataxis-core/SKILL.md`
   - Technical templates: `.claude/skills/doc-templates-technical/SKILL.md`
   - Repo templates: `.claude/skills/doc-templates-repo/SKILL.md`
   - Product templates: `.claude/skills/doc-templates-product/SKILL.md`

4. **Repository context** (for source link validation):
   ```bash
   git remote get-url origin  # for single-repo mode
   # OR
   cat .claude/repos.yaml      # for multi-repo mode
   ```

---

## Step 4: Dispatch Validation Agent

Dispatch the `docs-validator` agent with the following context:

```
You are validating documentation in scope: {SCOPE}

Files to validate:
{list of discovered files}

Line limits:
{line limits per file type}

Ownership map:
{ownership map}

Repository URL(s):
{repo URL(s) for link validation}

Your task:
1. Read each documentation file
2. Run all validation checks (line limits, code blocks, triviality, Diataxis, duplication, evidence, links, frontmatter, location)
3. Generate a comprehensive validation report with:
   - Summary statistics
   - Pass/fail status per file
   - Detailed violation reports grouped by severity (CRITICAL, IMPORTANT, QUALITY)
   - Actionable fix recommendations for each violation

Focus on CRITICAL issues first. Be specific with line numbers and concrete examples.
```

**Agent dispatch:**
```
Use Task tool with:
- subagent_type: "docs-validator"
- description: "Validate documentation quality"
- prompt: [context above]
```

---

## Step 5: Present Validation Results

After the validator agent completes, present a summary to the user:

```
Documentation Validation Complete
════════════════════════════════════════════════

Scope: {SCOPE}
Files validated: {count}

Results:
  ❌ CRITICAL issues: {count}
  ⚠️  IMPORTANT issues: {count}
  ℹ️  QUALITY improvements: {count}

Status:
  ✅ Passed: {count} files
  ❌ Failed (critical): {count} files
  ⚠️  Needs improvement: {count} files

════════════════════════════════════════════════

{If CRITICAL issues exist:}
⚠️  CRITICAL ISSUES MUST BE FIXED

The validator found {count} critical issues that must be addressed:
- {brief summary of critical issues}

See detailed report below for fix recommendations.

{If no CRITICAL issues:}
✅ No critical issues found

{If IMPORTANT issues exist:}
⚠️  {count} important issues should be fixed before committing.

{If only QUALITY issues exist:}
ℹ️  Documentation is acceptable. {count} quality improvements suggested.

════════════════════════════════════════════════

Detailed Validation Report:
{Full agent report}
```

---

## Step 6: Provide Next Steps

Based on validation results, suggest appropriate next actions:

**If CRITICAL issues exist:**
```
Next steps:
1. Review the critical issues above
2. Fix violations manually or regenerate affected files
3. Run `/validate-docs` again to verify fixes
4. Only commit documentation after validation passes
```

**If only IMPORTANT/QUALITY issues exist:**
```
Next steps:
1. Review the issues above
2. Consider fixing important issues before committing
3. Quality improvements are optional but recommended
4. Documentation can be committed if important issues are addressed
```

**If no issues (all passed):**
```
✅ Documentation validation passed!

All files comply with established rules and standards.
You can safely commit the documentation.

Suggested commit message:
docs: update documentation

Generated documentation for {SCOPE} scope
- {list key files updated}

All validation checks passed.
```

---

## Usage Examples

### Validate all documentation
```
/validate-docs
```

### Validate only technical docs
```
/validate-docs TECHNICAL
```

### Validate after fixing issues
```
# After fixing violations
/validate-docs ALL
```

---

## Important Notes

- **Run after generation**: Always run this after `/update-docs` completes
- **Critical issues block commit**: Do not commit documentation with critical violations
- **Iterative process**: Fix issues and re-validate until critical issues are resolved
- **Agent limitations**: The validator reads and reports only; it does not fix issues automatically
- **Manual fixes**: Some violations require manual editing or regeneration of affected files
- **Scope matching**: Use the same scope as your `/update-docs` command for consistency

---

## Validation Rules Reference

The validator checks against these rule categories:

1. **Line limits** (CRITICAL) — Hard limits per file type
2. **Code block length** (CRITICAL) — Max 5 lines per block
3. **No code copying** (CRITICAL) — Link instead of embedding
4. **Triviality filter** (IMPORTANT) — No generic content
5. **Diataxis purity** (IMPORTANT) — One quadrant per doc
6. **Single source of truth** (IMPORTANT) — No duplication across files
7. **Evidence-based** (IMPORTANT) — Only verified claims
8. **Source code links** (IMPORTANT) — Actual source, not codemaps
9. **Frontmatter** (SHOULD FIX) — All required fields present
10. **File location** (CRITICAL) — Correct ownership paths

See `.claude/skills/doc-standards/SKILL.md` and `.claude/skills/diataxis-core/SKILL.md` for complete rule definitions.
