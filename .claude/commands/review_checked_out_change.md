---
description: Review checked out changes
---

Follow the steps below, by spawning a NEW subagent with new context, and reviewing the changes. Use AGENTS.md for general orientation across the project, and @./specs/<FEATURE-FOLDER>, e.g. <FEATURE-FOLDER> = `001-dc-inventory-system-v1`, for what we're trying to achieve eventually (some of it may not be implemented yet).

Provide final summary for each section, identifying critical, high, medium, low and suggestion priorities, including a rationale.
DON'T CHANGE OR DELETE ANYTHING!

1. Review currently checked out changes for bugs.
2. Review currently checked out changes for subtle functional changes that might not be intended
3. Review currently checked out changes for breaking changes
4. Review currently checked out changes for security flaws
5. Assume you are a security expert and identify risk of  hijacking, injection, and client side manipulation that can create malicious impact on Nscale or other users.
6. Review currently checked out changes for anti-patterns
7. Review currently checked out changes for modern approaches to solve problems and new libraries that potentially do things better.
8. Review currently checked out changes for kubernetes, helm and docker and identify bugs, anti-patterns, security issues and risks, and conformance related adjustments.
9. Create an output of your findings and rationale or repro steps, in the following format
```md
    # Findings

    ## Bugs
    ### Critical
    1. ...
    ### High
    2. ...
    ### Medium
    3. ...
    ### Low
    4. ...

    ## Breaking changes
    1. ...

    ## Security Flaws and Risks
    ### Critical
    1. ...
    ### High
    2. ...
    ### Medium
    3. ...
    ### Low
    4. ...

    ## Patterns and Anti-Patterns
    ### Patterns and libraries to consider
    1. ...

    ### Anti-Patterns to avoid
    1. ...
```
