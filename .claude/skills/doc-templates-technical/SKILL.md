---
name: doc-templates-technical
description: Load when writing technical documentation for developers and operators. Provides file catalogue, templates, and writing standards for architecture docs, deployment guides, runbooks, observability guides, security, and testing documentation.
---

## File Catalogue

| File | Diataxis type | Write when | Max lines |
|------|--------------|------------|-----------|
| `docs/technical/architecture.md` | Explanation | Multiple components or meaningful topology found | 500 |
| `docs/technical/deployment.md` | How-to | Helm charts, K8s manifests, or Docker Compose found | 200 |
| `docs/technical/observability.md` | Explanation | Telemetry instrumentation found in code | 300 |
| `docs/technical/security.md` | Explanation | Auth implementation, RBAC, or network policies found | 120 |
| `docs/technical/testing.md` | How-to | Test suite exists with non-trivial setup | 120 |
| `docs/technical/runbooks/` | How-to | Operational procedures identifiable in codebase | 80 each |

**If the evidence gate (defined in tech-docs-agent) is not met, do not create the file.**

---

## Writing Standards

Use precise, verifiable language. Claims must be traceable to a file.

- Active voice and direct instructions, especially for operational procedures
- One concept per section
- Define technical terms on first use
- Stay within line limits — if a file exceeds its limit, you are including too much detail or duplicating information that belongs elsewhere

---

## Cross-Reference Rules

These topics are owned by other agents. **Do not duplicate — link instead.**

| Topic | Link to | Maximum in your file |
|-------|---------|---------------------|
| Env var full table | `DEVELOPMENT.md` | Reference specific vars inline when relevant to deployment/config |
| Setup / install steps | `DEVELOPMENT.md` | Do not duplicate |
| CLI commands full table | `DEVELOPMENT.md` | Reference specific commands when relevant |
| Business workflows | `docs/product/user-guide.md` | Do not duplicate |
| Domain glossary | `docs/product/glossary-faq.md` | Use terms, link on first use |

---

## Templates

### architecture.md

**Quadrant:** Explanation
**Max lines:** 500

```markdown
---
title: Architecture
last_updated: YYYY-MM-DD
last_commit: abc1234
---

## Overview

[2-4 sentences describing the system and its purpose.]

## System Context

[Mermaid C4 Context diagram — users, system boundary, external dependencies.]
[Caption: System context showing external actors and dependencies]

## Container View

[Mermaid C4 Container diagram — internal services, databases, message queues.]
[Caption: Internal containers and their communication paths]

## Component View — optional

[Only if a single container has enough internal complexity to warrant it.]
[Mermaid C4 Component diagram]
[Caption: Components within {container name}]

## Technology Stack

| Component | Technology | Version | Source |
|-----------|-----------|---------|--------|

## Data Flow

[How data moves through the system — verified from code only. Keep to 1-2 paragraphs or a sequence diagram.]

## Security Boundaries

[Trust zones, authentication points — from actual auth implementation. Omit if no security-specific code.]

## References

- **API Specification:** [{spec location}]({link})
- **Available Commands:** See [DEVELOPMENT.md](../../DEVELOPMENT.md)
- **Deployment:** See [deployment.md](deployment.md)
```

**Omission rules:**
- No Component View unless a container has 5+ internal components with non-obvious relationships
- No Security Boundaries section if no auth code exists — link to security.md if it exists, otherwise omit
- No Deployment Topology diagram here — that belongs in deployment.md

---

### deployment.md

**Quadrant:** How-to
**Max lines:** 200

```markdown
---
title: Deployment Guide
last_updated: YYYY-MM-DD
last_commit: abc1234
---

## Prerequisites

[Access requirements based on actual deployment method found in code.]

## Environment Configuration

For the full environment variable reference, see [DEVELOPMENT.md](../../DEVELOPMENT.md#configuration).

[Only list deployment-specific variables here that are NOT in .env.example — e.g., production secrets, cluster-specific config.]

## Deployment Workflow

### {Detected method — GitOps / Helm / Docker Compose / etc.}

[Steps derived from actual manifests, CI config, or Makefiles.]

## Rollback

[From actual method — git revert for GitOps, helm rollback for Helm, etc. Omit if no rollback mechanism found.]

## Verification

[From actual health checks, readiness probes, or monitoring endpoints. Omit if none found.]
```

---

### observability.md

**Quadrant:** Explanation
**Max lines:** 300

```markdown
---
title: Observability
last_updated: YYYY-MM-DD
last_commit: abc1234
---

## Approach

[How this service is instrumented — OpenTelemetry, Prometheus client, custom metrics, etc. 2-3 sentences.]

## Key Metrics

[Explain only metrics that operators need to understand. Do NOT list every metric.]

**`{metric_name}`**
- **What it measures:** {description}
- **Why it matters:** {operational impact}
- **Defined in:** [{path}]({github-url})

## Logging

[Log format, location, key fields. 3-5 sentences max.]

## Tracing

[Tracing approach, sampling strategy. Omit if no distributed tracing. 3-5 sentences max.]

## Alerts

[Explain critical alerts only. Link to full alert definitions in monitoring repo.]

## Dashboards

[Links to Grafana or equivalent. Omit if none exist.]
```

---

### security.md

**Quadrant:** Explanation
**Max lines:** 120

```markdown
---
title: Security
last_updated: YYYY-MM-DD
last_commit: abc1234
---

## Authentication

[Method and implementation — from actual auth code.]

## Authorization

[RBAC or permission model — from actual middleware or policy config. Omit if no authorization logic.]

## Network Boundaries

[Trust zones — from actual network policies or ingress config. Omit if not applicable.]

## Secrets Management

[How secrets are handled — from actual config. Omit if standard env vars only.]
```

---

### testing.md

**Quadrant:** How-to
**Max lines:** 120

```markdown
---
title: Testing
last_updated: YYYY-MM-DD
last_commit: abc1234
---

## Running Tests

```bash
[Actual command from Makefile or package.json]
```

## Test Structure

[From actual test directories — describe only project-specific patterns.]

## Test Coverage

[Coverage configuration — from actual setup. Omit if no coverage config.]

## Non-Standard Patterns

[Document only what is project-specific. Omit this section if everything is standard.]
```

---

### runbooks/{procedure-name}.md

**Quadrant:** How-to
**Max lines:** 80

```markdown
---
title: Runbook — {Alert or Issue Name}
last_updated: YYYY-MM-DD
last_commit: abc1234
---

## Trigger

[When to use this runbook — alert name, symptom, or incident type.]

## Prerequisites

[Access requirements, tools needed.]

## Diagnostic Steps

1. [Step with exact command]
2. [Step with exact command]

## Resolution Steps

1. [Action with exact command]
2. [Action with exact command]

## Escalation

[Who to contact if resolution fails. Omit if not determinable from code.]
```