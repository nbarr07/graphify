---
description: Map user journeys, personas, sequences in generate ux-spec file to detailed specification of a system view (one file per view).
---

AI - DON'T CHANGE THIS FILE

You are creating or updating the view ux-<view>-spec at `ux-<view>-spec.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`). Your job is to (a) collect/derive concrete values from end user, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts. This means writing an updated view ux-<view>-spec.


Follow this execution flow:

1. Load the existing ux-spec template at `.specify/templates/user-experience-view-template.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]` or `<VIEW NAME>`
   **IMPORTANT**: The user might require less or more details than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.
   - Do search for files and directories that look like placeholder tokens e.g. [SOMETHING] or <SOMETHING>

2. Collect/derive values for placeholders:
   - Ask the end user about important UX view preference, or derive that from existing code base when possible. Do confirm discrepancies, deprecated dependencies and anti-patterns when those identified.
   - Otherwise infer from existing repo context (README, docs, specs, ux-spec and prior ux-<view>-spec versions if embedded).

3. Draft the updated ux-<view>-spec content, for the specific <view> that was identified:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each section: succinct name line, paragraph, bullet list, or tree structure, capturing existing or target project structure details, and there are no unidentified or undocumented folders, and there are no misalignments between the project technologies being used and the information in agents-file.
   - Review existing code as required, to understand current structure, when the end users wants to create a spec based on what is currently implemented already.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/user-experience-view-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.claude/agents/react-expert.md` and ensure compliance.
   - Read `.claude/agents/typescript-expert.md` and ensure compliance.
   - Read existing ux-<view>-spec.md, if available. You may need to update it based on this workflow, including renaming based on changed view name.

5. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - ux-<view>-spec are informative, accurate and is useful for AI to generate a UI out of it, addressing the UX specifications, and understand navigation, filter and visual aspects of those components.
   - All client side navigation urls exist and implemented or planned in ux-spec.md.

6. Write the completed ux-spec back to `./specs/[FEATURE-FOLDER]/ux-<view>-spec.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend ux-<view>-spec.md to reflect changes to ...`).

Formatting & Style Requirements:
- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.
- Finish document with an empty newline.

If the user supplies partial updates (e.g., only view), still perform validation and version decision steps.

If critical info missing (e.g., project name is unknown), insert `TODO(<FIELD_NAME>): explanation` and include that in output to the user.

Do not create a new template; always operate on the existing `ux-<view>-spec.md` file, or create one based on the template when missing.
