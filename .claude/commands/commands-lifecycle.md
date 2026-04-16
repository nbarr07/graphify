---
description: Create README.md to represent how the different commands are supposed to be used across the project lifecycle
---
AI - DON'T CHANGE THIS FILE

You are updating the project commands-readme at `.claude/commands/README.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[COMMAND NAME]`). Your job is to (a) collect/derive concrete values from end user, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts. This means writing an updated project agents-file.

Project Lifecycle
-----------------
    1. Write down the philosophy and principles into constitution
    2. Backend:
        2.a. Specify the features, focusing on what vs. how
        2.b. Plan the work, incorporating technology dependencies and approaches
        2.c. Breakdown the plan to tasks
        2.d. While not all tasks are implemented:
            2.d.i. Identify set of task to implement which include code and tests and don't create cognitive load on the reviewer
            2.d.ii. Implement tasks
            2.d.iii. Perform local review, clean up and prepare to PR (code, github, documentation, test coverage, adrs etc)
            2.d.iv. Create a PR
            2.d.v. Review the PR
            2.d.vi. Address PR feedback and merge to main
    3. Frontend:
        3.a. Specify the user journeys into a spec with activities, personas, views, and sequence diagrams
        3.b. Analyze gaps in respect to backend and update backend tasks for any identified tasks, kicking of 2.d loop
        3.c. Breakdown the specification to tasks for executions using patterns and technologies of choice e.g. React, TypeScript, MVVM.
        4.d. While not all ux tasks are implemented:
            2.d.i. Identify set of ux task to implement which include code and tests and don't create cognitive load on the reviewer
            2.d.ii. Implement the ux tasks
            2.d.iii. Perform local review for ux, clean up and prepare to PR (code, github, documentation, test coverage, adrs etc)
            2.d.iv. Create a PR
            2.d.v. Review the PR
            2.d.vi. Address PR feedback and merge to main


Follow this execution flow:

1. Consider the `Project Lifecycle` as the conceptual stages for each project using this methodology.
2. Identify all the commands in `.claude/commands`, including the existing `.claude/commands/README.md` (if available)
3. Draft a mermaid diagram that shows where each command is supposed to be used and the expected arguments e.g. `specify.md` (BRANCH_NAME: my-branch, FEATURE_NAME: my feature, SPEC: my feature needs A, B, C.).
   - Capture arguments expected by each command with very short examples, if there are non omit arguments.
   - Preserve just file names (no folder names are required)
   - Every stage may include multiple commands and multiple commands maybe used in different phases e.g. review_git_actions.md when setting up github actions as part of the initial implementation steps.
   - There are no characters which are not supported by mermaid e.g. use ` ` instead of `\n`
   - Every command has a relative mermaid hyperlink

5. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - diagrams are accurate and useful for people to navigate the projects and understand the methodologies and the commands to use for each phase.

6. Write the completed agents-file back to `.claude/commands/README.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend README.md to reflect changes to ...`).

Formatting & Style Requirements:
- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If critical info missing (e.g., not sure what to do about the argument), insert `TODO(<FIELD_NAME>): explanation` and include that in output to the user.

Do not create a new template; always operate on the existing `.claude/commands/README.md` file.
