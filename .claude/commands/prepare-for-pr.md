---
description: Prepare the current checked out code for PR
---

1. Run `make lint` and `make test` and address any issues.
2. Ensure all 'Tasks to do with each PR' in @./specs/<FEATURE-FOLDER>/tasks.md are done. Especially test doc, update Project Structure in AGENTS.md and other documentation tasks.
3. Run 'make pc' twice and make sure that second time has no issues
4. Calculate the current test coverage and present in summary.
5. Calculate project stats and present in summary - lines of code, lines of tests, number of adrs (and line count), number of specs (and lines count) and the number of lines and file size for .specify/memory/prompt_history.md
