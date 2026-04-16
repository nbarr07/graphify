---
description: Creates PRD based on complete business problem document focused on 1 phase of the project
---

AI - DON'T CHANGE THIS FILE

Goal
=====

The goal of the PRD document is to prove the problem is real, the importance is high, and to define the MVP for a particular phase of the project and clearly articulate what success means for that phase.

**Inputs**

- Signals: user interviews, support tickets, usage data, competitor analysis, internal research
- Strategy: business goals, guardrails, constraints
- Design: user needs, journeys/flows, concepts & prototypes
- Additional details: scoping, phasing, risk, impact and urgency.

**Outputs**

- PRD - 1‑pager document targeting non-technical business and product people.
- PRD appendix: Scope & acceptance criteria for MVP
- PRD appendix: Risk check (security/privacy/data) with required actions
- PRD appendix: Identified key stakeholders

Follow this execution flow:

1. Get the inputs from the user and analyze the inputs
2. Analyze the `PRD Format` and follow up with asking the product owner for clarification on gaps, lack of clarity, in consistency or conflicting messaging.
3. Draft a PRD
4. Review the PRD against the expectations in `PRD Format` and create an output check list for:
    [ ] Summary
    [ ] Business case
    [ ] Solution
    [ ] Implementation
    [ ] Rollout
5. Create or update the file under @./docs/spec/business/prd-<phase>.md. When no phase could be inferred assume MVP.

PRD Format
---------
- Summary: overview, phases, success metrics
- Business case: problem, audience, opportunity, commercials
- Solution: MVP scope & features, user stories, acceptance criteria, designs
- Implementation: phases, timeframe, guardrails and risk mitigation approaches
- Rollout: federated vs. centralized, feature flags? beta release and focus group, comms & GTM, monitoring and KPI metrics, and key upstream and downstream dependencies to align with

----
AI IGNORE FROM THIS POINT

**Usage**

Follow @./.claude/commands/create-prd.md to generate a prod for MVP articulated in this document: @./docs/spec/business_problem.md
