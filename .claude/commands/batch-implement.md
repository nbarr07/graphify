---
description: Identify tasks to implement in a reasonable size batch for human reviewer
---

1. Review $ARGUMENTS (which "@./specs/<FEATURE-FOLDER>/tasks.md" to focus on e.g. <FEATURE-FOLDER> = `001-dc-inventory-system-v1`) and identify an implementation and test tasks that we should start from. You can review the more detailed specifications under ./specs/<FEATURE-FOLDER> directory for respective feature.
Optimize for similar code areas and avoid inflicting cognitive load to those that will be reviewing the implementation.
Choose from the following strategies:
    - Select complete components with their immediate dependency as long as we have 1-3 components, with the relevant tests.
    - Select from top layer which hasn't been implemented and implement it, stubbing any dependent classes or method with `// TODO: implement in task XYZ-123`
    - Start from bottom component which hasn't been implemented and has low or no unimplemented dependencies, and implement it, stubbing any dependent classes or method with `// TODO: implement in task XYZ-123`
What I want in the end is a recommended list of tasks to tackle (1-5), and the rationale why they were chosen, in the following format:
```
* <Task id> - <reference to linear task>
    - Task Description: ...
    - Selection Rationale: ...
```
Example:
If chose this task:
[ ] T001 ([XYZ-123](https://linear.app/nscale-workspace/issue/LXYZ-123)) Update `backend/pyproject.toml`
The formatted text would be:
```
* T001 - [XYZ-123](https://linear.app/nscale-workspace/issue/XYZ-123)
    - Task Description: Update `backend/pyproject.toml`
    - Selection Rationale: The only remaining task.
```

2. Identify if it's worth adding more tasks, without greatly increasing the number of files being looked at, by following up with the following questions:
    - Are there any additional relevant or tightly couple tasks that is worth adding to the list?
    - Can we just do <.TASK NUMBER.> for a complete e2e for this component? or do we need other tasks?
Ask end user to decide when its not obvious.
Provide the intermediate summary to end user for visibility.

3. Follow @/.claude/commands/implement.md workflow to implement the tasks below for specifications under the relevant ./specs/<FEATURE-FOLDER> directory.
The tasks needed to be ready for PR. The code and tests implementation style and preference are based on what was agreed in @./specs/<FEATURE-FOLDER>>/spec.md and @./specs/<FEATURE-FOLDER>/plan.md

Tasks:
* T789 - [XYZ-123]
* ... the chosen tasks

Use appropriate templates to collect and represent end user inputs.
Use @/AGENTS.md to identify project structure and key directories.

4. Run `make lint` and `make test` and address any issues.

5. Ensure all 'Tasks to do with each PR' in @./specs/<FEATURE-FOLDER>/tasks.md are done.
