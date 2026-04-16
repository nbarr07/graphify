---
description: Create implementation plan from UX specs and figma designs
---

Follow this execution flow:

1. Review @./specs/[FEATURE-FOLDER]/ux-[COMPONENT-NAME]-spec.md and extract:
- Component names
- Views included in this flow
- UX states
- Related Figma design URLs (full URLs with node IDs)
- Acceptance criteria
- Interaction notes
- Navigation logic

2. Analyze Current Implementation For each component/view defined in this UX spec:
- Locate existing view + view-model + services
- Identify mismatches between:
    - Figma reference
    - UX spec requirements
    - Current implementation
- Identify missing states or incomplete flows
- Identify repeated UI that should become base components
- Identify logic in the wrong place (view vs view-model)

3. Generate Task Plan, produce tasks grouped under Phases and Slices:
- **View tasks**
- **View-model tasks**
- **Command/service tasks**
- **Component extraction tasks**
- **Asset tasks (icons, svg cleanup)**
- **Routing/navigation tasks**
- **Styling/spacing/typography fixes**
- **Accessibility improvements**

Each task MUST include:
- **Related UX states** (exact state names from the UX spec)
- **Related Figma references** (full URLs with node IDs)
- **Target files** (files to modify or create)
- **Acceptance criteria**
- **Dependencies**
- **Output artifacts** (files created/updated/deleted)
- **Verification steps**, including:
  1. Run `figma-extract` for referenced Figma node(s)
  2. Capture local UI screenshot after implementation
  3. Run `figma-verify` comparing screenshots
  4. Ensure semantic match score ≥ 95%
  5. Repeat until verification passes

4. Append newly generated tasks to the file:'specs/[FEATURE-FOLDER]/ui-tasks.md' while preserving existing tasks
