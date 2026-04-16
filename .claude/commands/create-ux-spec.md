---
description: Identify user journeys, personas and views and generate ux-spec file for it, that will be useful for automated generation of the UX
---

AI - DON'T CHANGE THIS FILE

You are creating or updating the project ux-spec at `ux-spec.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`). Your job is to (a) collect/derive concrete values from end user, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts. This means writing an updated project ux-spec.


Follow this execution flow:

1. Load the existing ux-spec template at `.specify/templates/user-experience-template.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more details than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.
   - Do search for files and directories that look like placeholder tokens e.g. [SOMETHING].

2. Collect/derive values for placeholders:
   - Ask the end user about important UX expectations or technology choices, or derive that from existing code base when possible. Do confirm discrepancies, deprecated dependencies and anti-patterns when those identified.
   - Otherwise infer from existing repo context (README, docs, specs, prior ux-spec versions if embedded).

3. Draft the updated ux-spec content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each section: succinct name line, paragraph, bullet list, or tree structure, capturing existing or target project structure details, and there are no unidentified or undocumented folders, and there are no misalignments between the project technologies being used and the information in agents-file.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/user-experience-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read existing ux-spec.md, if available. You may need to update it based on this workflow.

5. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - ux-spec are informative, accurate and is useful for AI to generate a UI out of it, addressing the UX specifications, and understand technologies and reusable components being preferred custom implementations.

6. Write the completed ux-spec back to `./specs/[FEATURE-FOLDER]/ux-spec.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend ux-spec.md to reflect changes to ...`).

Formatting & Style Requirements:
- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.
- Finish document with an empty newline.

If the user supplies partial updates (e.g., only view), still perform validation and version decision steps.

If critical info missing (e.g., project name is unknown), insert `TODO(<FIELD_NAME>): explanation` and include that in output to the user.

Do not create a new template; always operate on the existing `ux-spec.md` file, or create one based on the template when missing.
