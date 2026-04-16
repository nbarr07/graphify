---
description: Execute the implementation plan by processing and executing all tasks defined in ux-tasks.md
---

Given the current feature context, do this:

1. Load and analyze the implementation context:
   - **REQUIRED**: Read ux-tasks.md for the complete task list and execution plan
   - **REQUIRED**: Read us-spec.md for tech stack, architecture, and file structure
   - **IF EXISTS**: Read data-model.md for entities and relationships
   - **IF EXISTS**: Read contracts/ for API specifications and test requirements
   - **IF EXISTS**: Read research.md for technical decisions and constraints
   - **IF EXISTS**: Read quickstart.md for integration scenarios

2. Parse ux-tasks.md structure and extract:
   - **Task phases**: Setup, Tests, Core, Integration, Polish
   - **Task dependencies**: Sequential vs parallel execution rules
   - **Task details**: ID, description, file paths, parallel markers [P]
   - **Execution flow**: Order and dependency requirements

3. Execute implementation following the task plan:
   - **Phase-by-phase execution**: Complete each phase before moving to the next
   - **Respect dependencies**: Run sequential tasks in order, parallel tasks [P] can run together
   - **Follow TDD approach**: Execute test tasks before their corresponding implementation tasks
   - **File-based coordination**: Tasks affecting the same files must run sequentially
   - **Validation checkpoints**: Verify each phase completion before proceeding

4. Implementation execution rules:
   - **Setup first**: Initialize project structure, dependencies, configuration
   - **Tests before code**: If you need to write tests for contracts, entities, and integration scenarios
   - **Core development**: Implement models, services, CLI commands, endpoints
   - **Integration work**: Database connections, middleware, logging, external services
   - **Polish and validation**: Unit tests, performance optimization, documentation and all the tasks associated with each PR.

5. Progress tracking and error handling:
   - Report progress after each completed task
   - Halt execution if any non-parallel task fails
   - For parallel tasks [P], continue with successful tasks, report failed ones
   - Provide clear error messages with context for debugging
   - Suggest next steps if implementation cannot proceed
   - **IMPORTANT** For completed tasks, make sure to mark the task off as [X] in the tasks file.

6. Completion validation:
   - Verify all required tasks are completed
   - Check that implemented features match the original specification
   - Validate that tests pass and coverage meets requirements
   - Confirm the implementation follows the technical plan
   - Report final status with summary of completed work

Follow the following implementation guidelines below

## Implementation guidelines

1. Prefer using a single line to destructure the object

Example (good):
```ts
const { selectSite: controllerSelectSite, selectPurchaseOrder: controllerSelectPurchaseOrder } = usePurchaseOrderIntakeBoardController();
```

Example(bad):
```ts
const controller = usePurchaseOrderIntakeBoardController();
const { selectSite: controllerSelectSite, selectPurchaseOrder: controllerSelectPurchaseOrder } = controller;
```

2. Avoid unnecessary callback hooks

Example (bad):
```ts
  const selectSite = useCallback(
	    (siteId: string) => {
	      controllerSelectSite(siteId === "" ? null : siteId);
	    },
	    [controllerSelectSite],
	  );
```

3. Avoid calling hooks conditionally

Example (bad):
```ts
const resolvedViewModel = viewModel ?? usePurchaseOrderIntakeBoardViewModel();
```

4. Fail fast instead of silently coercing missing values, allow UI to passing values to the controller and deal with invalid arguments there by raising errors when the API require non-null values.

Example (bad):
```ts
  const selectSite = (siteId: string) => {
    controller.selectSite(siteId === "" ? null : siteId); // If SiteId is required, then this becomes a bug that will propagate to the controller and so on.
  };
```

5. Avoid swallowing exception silently, either handle them, let them bubble up if it's not critical path, or log them to console if they are non-essential things like telemetry.

Note: This command assumes a complete task breakdown exists in ux-tasks.md. If tasks are incomplete or missing, suggest running `/tasks-ux` first to regenerate the task list.
