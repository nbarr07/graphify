---
description: Prepare the current checked out code for PR
---
1. Ensure Primary Reusable Components and Component Seed are enforced in the implementation, see also ux-spec.md
2. Ensure Primary Styling Strategy is enforced in the implementation, see also ux-spec.md
3. Run `make frontend-init` to install and get the latest packages for frontend, and address any issues.
4. Run `make frontend-build` to build the frontend, and address any issues.
5. Run `make frontend-build-docker` followed by `make frontend-run-docker` to verify the multi-stage container image starts and serves routes locally; address any issues.
6. Run `make frontend-test` to test the frontend, and address any issues, target 80% meaningful tests coverage - verify the inputs for mocks, verify output for processes, verify errors and messages for negative use cases. Don't exclude non-generated artifacts from coverage unless the end users approves that.
7. Run `make frontend-lint` to lint the frontend, and address any issues.
8. Run `make frontend-typecheck` to typecheck the frontend, and address any issues.
9. Run `make frontend-format` to format the frontend, and address any issues.
10. Run `TEST_ENABLE_INTERACTIVE=true make frontend-test-e2e` for Playwright coverage with telemetry enabled, then rerun with `TEST_ENABLE_INTERACTIVE=true VITE_TELEMETRY_ENABLED=false make frontend-test-e2e` to confirm the instrumentation toggle works; address any issues.
11. Run `make frontend-generate-api` to generate frontend client to backend api, and address any issues.
12. Run `make frontend-coverage` to generate code coverage report for frontend, and address any issues.
13. Ensure all 'Tasks to do with each PR' in @./specs/<FEATURE-FOLDER>/ux-tasks.md are done. Especially test doc, update Project Structure in AGENTS.md and other documentation tasks.
14. Run 'make pc' twice and make sure that second time has no issues
15. Extract the current test coverage and present in summary.
16. Calculate project stats and present in summary, for frontend: lines of code, lines of tests, number of adrs (and line count), number of specs (and lines count) and the number of lines and file size for .specify/memory/prompt_history.md
