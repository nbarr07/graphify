---
description: Create end user documentation for the project
---
AI - DON'T CHANGE THIS FILE

Expected arguments or inputs for this workflow:
* [PRODUCT-NAME] - the externally facing name for the project
* [PRODUCTION-ENDPOINT] - the endpoint to use for real production traffic
* [PERSONAS] - the mapped personas in this project
* [NSCALE-ROLES] - the role names which the personas can be assigned with or assume
* [OPENAPI-SPEC-FILE] - the location of openAPI schema, default location: `backend/schema/openapi.yaml`
* [FEATURE-FOLDER] - where to look at the different specs, plans and other important documents, default location `/specs/<FEATURE-FOLDER>`

Workflow steps:
1. Ensure all inputs for this workflow is resolved or collected. Don't assume things, ask and clarify.
2. Review each persona in [PERSONAS], and map them to [NSCALE-ROLES]. Prompt to end user to confirm or amend the mapping.
3. Review the OpenAPI specs in [OPENAPI-SPEC-FILE], and propose a reasonable mapping of APIs to persona. Expect [PRODUCTION-ENDPOINT] to be the one used by end users.
4. Review [FEATURE-FOLDER] for any user journeys and extract the relevant ones.
5. Draft in docs/[FEATURE-FOLDER]/enduser-documentation.md a documentation based on each persona in [PERSONAS], using user journeys as the way to show case the APIs, since openAPI spec is available to endusers already. Document expectations about assigned or assumed roles from [NSCALE-ROLES].
6. Review the checklist below, and what was done, check off what was completed, and present the updated checklist of the effort to end user:
```
[ ] Personas: (list of personals)
[ ] Roles: <persona>:<role>, ...
[ ] User Journeys for <persona>: 5 journeys documented with APIs (/v1/API1, /v2/API2, ...)
```
