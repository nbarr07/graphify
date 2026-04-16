---
name: doc-templates-repo
description: Load when writing repository-level documentation. Provides file catalogue, templates, and writing standards for README, DEVELOPMENT.md, CONTRIBUTING.md, and CHANGELOG.md.
---

## File Catalogue

| File | Diataxis type | Write when |
|------|--------------|------------|
| `README.md` | Exception (signpost) | Always — update if stale |
| `DEVELOPMENT.md` | How-to | Always — create if missing |
| `CONTRIBUTING.md` | How-to | Always — create if missing |
| `CHANGELOG.md` | Reference | Always — update if stale |

---

## Writing Standards

Use verifiable, testable language. Every command must be derived from an actual project file.

- Numbered lists for procedures, bullet points for options
- Code blocks with language tags for all commands
- Short paragraphs — 3 to 5 sentences maximum
- All documents must end with a Documentation Summary block

---

## Templates

### README.md

**Quadrant:** Exception (signpost - sits outside quadrants)

```markdown
---
title: [Project Name]
last_updated: YYYY-MM-DD
last_commit: abc1234
---

# [Project Name]

[1-2 sentence elevator pitch — what this is and who it is for]

## Quick Start

[Minimum steps to get running — detect build system from doc-standards and use appropriate commands]

```bash
git clone [repo-url]
cd [repo-name]
[install-command]  # Detected from ecosystem
[dev-command]      # Detected from build system
```

## What This Does

[Brief explanation of core capabilities — 3-5 bullets derived from codebase]

## Documentation

| Document | Audience | Description |
|----------|---------|-------------|
| [docs/technical/](docs/technical/) | Developers, operators | Architecture, API reference, runbooks |
| [docs/product/](docs/product/) | Product, stakeholders | Features, user guide, data dictionary |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Contributors | Local setup, testing, workflows |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contributors | Branching, commits, PR process |

## License

[From LICENSE file — omit if not found]

---

## Documentation Summary
**Created**: README.md
**Key Sections**: [list]
**Needs Attention**: [TODOs or areas requiring human input]
**Automation Opportunities**: [what could be auto-generated]
```

---

### DEVELOPMENT.md

**Quadrant:** How-to

```markdown
---
title: Development Guide
last_updated: YYYY-MM-DD
last_commit: abc1234
---

# Development Guide

[1 sentence on what this guide covers]

## Prerequisites

[Specific versions required — from package.json, pyproject.toml, or Dockerfile only]

- [Tool] [version] — [why needed]

## Setup

[Steps derived from actual Makefile, docker-compose, or setup scripts only]

1. Clone the repository

```bash
git clone [repo]
cd [project]
```

2. Configure environment

```bash
cp .env.example .env
# Edit .env — see Configuration section below
```

3. Install dependencies

```bash
[actual command from Makefile or package.json]
```

4. Start services

```bash
[actual command — e.g. make dev, docker-compose up]
```

## Configuration

[Environment variables from .env.example or config files only]

| Variable | Purpose | Required | Default |
|----------|---------|----------|---------|
| `VAR_NAME` | [description] | Yes/No | [value or none] |

## Common Tasks

[Derived from actual Makefile targets or package.json scripts or similar files based on the programminglanguage]

```bash
make test          # [description from Makefile comment]
make lint          # [description from Makefile comment]
make build         # [description from Makefile comment]
```

## Troubleshooting

[Common issues — only document if evidence exists in code, issues, or existing docs]

### [Issue]
**Symptom**: [what the developer sees]
**Fix**: [actual resolution]

---

## Documentation Summary
**Created**: DEVELOPMENT.md
**Key Sections**: [list]
**Needs Attention**: [TODOs or areas requiring human input]
**Automation Opportunities**: [what could be auto-generated]
```

---

### CONTRIBUTING.md

**Quadrant:** How-to

```markdown
---
title: Contributing Guide
last_updated: YYYY-MM-DD
last_commit: abc1234
---

# Contributing

[1-2 sentences on how contributions are welcomed]

## Development Setup

See [DEVELOPMENT.md](DEVELOPMENT.md) to get your environment running.

## Branching Strategy

[From existing docs, CI config, or CODEOWNERS — use [ASSUMPTION] if inferred]

- `main` — [description]
- `feature/[name]` — [description]


## Pull Requests

[From existing docs or PR templates in .github/ — omit if not found]

- [ ] Tests pass (`make test`)
- [ ] Linting passes (`make lint`)
- [ ] Documentation updated if needed

## Code Ownership

[From CODEOWNERS file — omit if not found]

## Release Process

[From existing docs, CI config, or Makefile release targets — omit if not found]

---

## Documentation Summary
**Created**: CONTRIBUTING.md
**Key Sections**: [list]
**Needs Attention**: [TODOs or areas requiring human input]
**Automation Opportunities**: [what could be auto-generated]
```

---

### CHANGELOG.md

**Quadrant:** Reference

```markdown
---
title: Changelog
last_updated: YYYY-MM-DD
last_commit: abc1234
---

# Changelog

All notable changes to this project are documented here.

## [Unreleased]

## [vX.X.X] — YYYY-MM-DD

### Added
- [Feature or capability added]

### Changed
- [Existing behaviour that changed]

### Fixed
- [Bug that was fixed]

### Removed
- [Feature or capability removed]

[Derived from git history, release tags, or existing CHANGELOG — do not invent entries]
```
