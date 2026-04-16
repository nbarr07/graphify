---
allowed-tools: Bash(git fetch:*), Bash(git diff:*), Bash(git branch:*), Bash(mkdir:*), Read, Write, Glob, Grep
description: Perform Round 2 second-pass review building on Round 1 and save improved draft
---

Use the Github CLI to ensure the main branch is up to date with origin.

Then look at the git diff to main.
This is the PR you should review.
In this project, we are use prompt engineering in MD files to guide an LLM in generating code.
Consult the MD files to get the full context of the project, then review the PR.

I had you do this exercise already in a previous session, and you generated your review in
`pr-reviews/{git_branch_name}/claude/pr-review.md`.
Read it.

With that context of your first pass, as you analyse the code create a new 2nd improved draft of your original review.
**Important**: Don't just accept Round 1's conclusions - validate them independently by examining the actual code.
Challenge assumptions and verify severity classifications are appropriate
(P0 = showstoppers like security/data corruption, not documentation issues).

Don't overwrite `pr-review.md`. Save your second-pass review to `pr-reviews/{git_branch_name}/claude/pr-review-second-pass.md`.
