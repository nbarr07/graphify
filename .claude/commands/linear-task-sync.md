---
description: Sync tasks to linear using mcp
---

Follow this execution flow:

1. Review all tasks e.g. T005, in all phases in @./specs/[FEATURE-FOLDER]ux-tasks.md and sync them to Linear: under `[LINEAR PROJECT]` Project, in a `Todo` status, and label 'frontend', and ensure it's cross referenced in ux-tasks.md e.g. T005 - ([LEV-112](https://linear.app/nscale-workspace/issue/LEV-112))

2. Review all tasks e.g. T005, in all phases in @./specs/[FEATURE-FOLDER]/tasks.md and sync them to Linear under: `[LINEAR PROJECT]`  Project, in a `Todo` status and label 'backend', and ensure it's cross referenced in tasks.md e.g. T005 - ([LEV-112](https://linear.app/nscale-workspace/issue/LEV-112))

3. List every task whose line changed e.g. [ ] -> [x], regardless of status, so the review tells the full story of what’s different. The default behavior is to look at uncommitted vs. committed lines, but the user may ask to diff current branch again main, and you need to list these changes instead.

For all tasks:
* Ensure you identify or ask for `[FEATURE-FOLDER]`
* Ensure you identify or ask for `[LINEAR PROJECT]`
* Ensure the label is set
* Ensure the status is correct:
    * Todo - when not implemented
    * In Progress - when implementing, which is determined by diffing current uncommitted tasks against what is committed
    * In Review - when sending to PR, which is determined by diffing current checked in branch against target branch, normally main
    * Done - when PR is merged, which is determined by inspecting the main branch and seeing that the task is done
* Don't create new Linear tasks if one is already assigned and referenced, but ensure to review the label, description and status for updates.
* Never infer status, it should be set explicitly or clarified with the user.

In the end display a summary in the format below
* T005 - ([LEV-112](https://linear.app/nscale-workspace/issue/LEV-112)) - <Status>

Note to developers, AI should ignore from this point until end of document:

To setup MCP on Codex, add the following to config.toml, and close the chat window.
```
[mcp_servers.linear]
command = "npx"
args = ["-y", "mcp-remote", "https://mcp.linear.app/mcp"]
```
