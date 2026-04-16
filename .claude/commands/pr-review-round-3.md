---
allowed-tools: Bash(git fetch:*), Bash(git diff:*), Bash(git branch:*), Bash(mkdir:*), Read, Write, Glob, Grep
description: Perform Round 3 final authoritative review with actionable recommendations
---

Use the Github CLI to ensure the main branch is up to date with origin.

Then look at the git diff to main.
This is the PR you should review.
In this project, we are use prompt engineering in MD files to guide an LLM in generating code.
Consult the MD files to get the full context of the project, then review the PR.

I had you do this exercise already in 2 previous sessions, and you generated your 2nd draft review
in `pr-reviews/{git_branch_name}/claude/pr-review-second-pass.md`.
Read it. With that context of your 2nd pass, as you analyse the code create a new 3rd and final
improved version of your original review.

**Critical thinking required**: Actively look for where previous rounds may have:
- Over-complicated simple issues (e.g., treating typos as critical blockers)
- Missed the root cause (e.g., staging issues vs design flaws)
- Inflated severity (documentation ≠ P0, preferences ≠ defects)
- Added unnecessary complexity (validation that natural errors handle)

Focus on what actually matters for the PR's functionality and user experience. If previous rounds
spiraled into over-analysis, cut through to the core issue.

Don't overwrite `pr-review-second-pass.md`. Save your final review to `pr-reviews/{git_branch_name}/claude/pr-review-third-pass.md`.

Make sure your suggestions are accurate, in the spirit of the PR and follow best idiomatic Python
principles, ultra think.

Give actionable improvements that can be made, and don't hesitate to disagree with your previous
conclusions if you find them to be incorrect or immature.
