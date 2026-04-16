---
allowed-tools: Task, Bash(gh pr comment:*), Read
description: Orchestrate a 3-round PR review process and post the final review to GitHub
---

This command orchestrates a 3-round PR review process with isolated context for each round.

## Round 1: Initial Review
Spawn a subagent to execute the `/pr-review-round-1` command.

Wait for Round 1 to complete and verify `pr-reviews/{git_branch_name}/claude/pr-review.md` was created before proceeding to Round 2.

## Round 2: Second Pass Review
Spawn a NEW subagent to execute the `/pr-review-round-2` command.

Wait for Round 2 to complete and verify `pr-reviews/{git_branch_name}/claude/pr-review-second-pass.md` was created before proceeding to Round 3.

## Round 3: Final Review
Spawn a NEW subagent to execute the `/pr-review-round-3` command.

After all three rounds complete, report the locations of all three review files to the user.

## Round 4: Post to GitHub
After all three reviews are complete:
1. Read the final review from `pr-reviews/{git_branch_name}/claude/pr-review-third-pass.md`
2. Post it as a comment on the current PR using: `gh pr comment --body-file pr-reviews/{git_branch_name}/claude/pr-review-third-pass.md`
3. Confirm to the user that the review has been posted to GitHub with a link to the PR
