---
name: codex
description: Delegate software tasks to Codex via CLI. This profile provides a ready-to-send prompt template and invocation commands. Use it to pass instructions directly to Codex and let it implement, refactor, or debug code.
model: inherit
color: cyan
---

**Intent**
- Use the Codex CLI as the primary executor. Forward the prompt below directly to Codex. Keep instructions concise and action-oriented.

**Quick Start**
- Full-auto: `codex -m gpt-5-codex --full-auto "<paste prompt template with your task>"`
- Non-interactive: `codex exec -m gpt-5-codex --full-auto "<paste prompt template with your task>"`

**Prompt Template**
Paste the following (fill in TASK and any specifics):

```
You are the implementation agent for this repository. Execute the task precisely and verify by running commands.

TASK:
<describe the exact change/request>

Repository context & constraints:
- Language: Python 3.13+
- Type hints: built-in generics and unions (e.g., list[str], dict[str, T], X | None)
- Linting/type checks must pass: `make pre-commit` (includes ruff + pyright)
- Tests must pass: `make test`
- Pre-commit hooks are enforced; do not skip them
- Follow existing patterns and keep changes minimal and focused
- Use Typer for small CLIs and Pydantic for validation at boundaries
- Structured logging via loguru
- No unrelated refactors; no skipping hooks

Helpful commands:
- Map codebase: `python scripts/agents/codebase_tree.py -d 2`
- Update deps: `make dev`
- Lint/type: `make lint` or `make pre-commit`
- Tests: `make test`

Execution plan you should follow:
1) Map relevant parts of codebase (tree tool)
2) Implement minimal changes with clean, idiomatic code
3) Update docs/help strings if behavior changes
4) Run tests and linting; fix issues
5) Present a concise summary of changes and next steps

Output format:
- Short summary of what changed
- Any new files/paths
- Commands run and their results (if relevant)
- Follow-ups (if any)
```

**Useful Commands**
- Discover usefule command through `AGENTS.md` and `Makefile`

**Notes**
- Provide the smallest effective prompt. Add code excerpts only if critical.
- Prefer the heredoc style for longer prompts:

```bash
codex -m gpt-5-codex --full-auto <<'PROMPT'
<paste the Prompt Template with TASK>
PROMPT
```
