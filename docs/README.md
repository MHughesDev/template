# docs/README.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: README.md (root), AGENTS.md §Navigation -->

> PURPOSE: Documentation hub. Index of all doc sections with one-line descriptions and links. Per spec §26.5 item 111.

## Documentation Structure

> CONTENT: Ordered list of every docs/ subdirectory with description and link to its README. Grouped by purpose:
>
> **Getting started:**
> - [getting-started/](getting-started/README.md) — Prerequisites and quickstart from clone to green dev
>
> **Understanding the system:**
> - [architecture/](architecture/README.md) — System design, bounded contexts, data layer, auth
> - [api/](api/README.md) — Endpoint catalog and error codes
> - [queue/](queue/queue-system-overview.md) — Agent work queue: concepts, lifecycle, intelligence
> - [glossary.md](glossary.md) — Ubiquitous language and domain glossary
>
> **Operating the system:**
> - [development/](development/README.md) — Local setup, coding standards, testing, env vars
> - [operations/](operations/README.md) — Docker, Kubernetes, observability, backups, rollback
> - [security/](security/README.md) — Threat model, secrets, incident response, token lifecycle
> - [runbooks/](runbooks/README.md) — Failure scenario runbooks (API down, DB failure, JWT rotation)
>
> **Agent and human governance:**
> - [procedures/](procedures/README.md) — Canonical SOPs for recurring workflows (agents first)
> - [agents/](agents/README.md) — Human supervision of agent work
> - [prompts/](prompts/README.md) — Prompt library conventions and index
> - [adr/](adr/README.md) — Architecture Decision Records
>
> **Quality and releases:**
> - [quality/](quality/README.md) — Testing strategy, coverage policy, flake policy
> - [release/](release/README.md) — Versioning, promotion path, changelog guide
> - [repo-governance/](repo-governance/README.md) — Improvement loops, audits, procedure drift
>
> **Optional profiles:**
> - [optional-clients/](optional-clients/web.md) — Web and mobile profile documentation
> - [troubleshooting/](troubleshooting/README.md) — Common issues and solutions
