---
description: Review git actions for quality and security related issues
---

1. Review .github folder and identify bugs or security risks.
2. Identify race conditions (e.g. access to actions before checkout), file name expectations (e.g. action.yml instead of action.yaml), non-pinned external actions and similar issues when it comes to github actions.
3. If not issues were identified finish the workflow
4. If issues were identified:
    a. Identify an action plan to remediate, and for any issue that requires clarification, ask the user.
    b. Remediate the issues
    c. GOTO step 1
