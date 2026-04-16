---
description: Generate an actionable, dependency-ordered ux-tasks.md for the feature based on available design artifacts targeting the frontend.
---

Given the context provided as an argument, do this:

1. Load and analyze available design documents for frontend:
   - Always read ux-spec.md for tech stack and libraries, and prefer Nscale reusable components when these are available.
   - IF EXISTS: Read data-model.md for entities
   - IF EXISTS: Read contracts/ for API endpoints
   - IF EXISTS: Read research.md for technical evaluations
   - IF EXISTS: Read ./docs/adr for technical decision

   Note: Not all projects have all documents. For example:
   - CLI tools might not have contracts/
   - Simple libraries might not need data-model.md
   - Generate tasks based on what's available and top to bottom since this is a UI project - views first, view models and commands second, models third, etc. each phase with respective tests.

3. Generate tasks following the template:
   - Use `.specify/templates/tasks-template.md` as the base, and target Model-View-View-Model and top to bottom, layer by layer tasks, since this is focused on client-side (frontend Views) with client side logic (View Model) calling (Models and Commands) APIs (backend APIs)
   - Replace example tasks with actual tasks based on:
     * **Phase 1 tasks**: Project init, dependencies, makefile commands
     * **Phase 2 tasks [P]**: Views, navigation and respective tests.
     * **Phase 3 tasks [P]**: View Models and Commands integrated with Views, with respective tests.
     * **Phase 4 tasks [P]**: Models and Commands integrated with backend APIs and Auth, Views respect RBAC roles.
     * **Phase 5 tasks [P]**: Telemetry, security and performance.

4. Task generation rules:
   - Each view file → view test task marked [P]
   - Each components → implementation task [P]
   - Each view model file → view model test task marked [P]
   - Each model file → mode test task marked [P]
   - Each view commands file → implementation task per command (not parallel if shared files), command test task marked [P]
   - Each user story → e2e integration test marked and updated each phase [P]
   - Different files = can be parallel [P]
   - Same file = sequential (no [P])

5. Order tasks by dependencies:
   - Based on phases
   - Optimized for batches of roughly 500 lines changes that avoid cognitive load to reviewers

6. Include parallel execution examples:
   - Group [P] tasks that can run together
   - Show actual Task agent commands

7. Create FEATURE_DIR/ux-tasks.md with:
   - Correct feature name from implementation plan
   - Numbered tasks, based on phases Px and sub tasks Tyyy eg. UI-P1-T001, UI-P2-T001
   - Clear file paths for each task
   - Dependency notes
   - Parallel execution guidance

Context for task generation: $ARGUMENTS

The ux-tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.
