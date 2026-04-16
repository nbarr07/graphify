---
allowed-tools: Bash(git fetch:*), Bash(git diff:*), Bash(git branch:*), Bash(mkdir:*), Read, Write, Glob, Grep
description: Perform Round 1 initial review of a PR and save to pr-reviews directory
---

Use the Github CLI to ensure the main branch is up to date with origin.

Then look at the git diff to main.
This is the PR you should review.
In this project, we are use prompt engineering in MD files to guide an LLM in generating code.
Consult the MD files to get the full context of the project, then review the PR.

Store your review in `pr-reviews/{git_branch_name}/claude/pr-review.md`, inserting the current
git branch name.
