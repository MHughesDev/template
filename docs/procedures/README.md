# docs/procedures/README.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: AGENTS.md §3 (Required Workflow), CONTRIBUTING.md -->
<!-- - All procedures referenced from AGENTS.md and various skills -->

> PURPOSE: Procedures index. Lists all SOPs with one-line descriptions and links. These are canonical workflows written for agents first, usable by humans. Per spec §26.5 item 138.

## What Are Procedures?

> CONTENT: Brief explanation: procedures (SOPs) are canonical workflows. Each is written in exactly-ordered steps with exact commands. Agents use them to navigate complex recurring tasks without guesswork. Linked from AGENTS.md §3 (Required Workflow step 5).

## Index of All Procedures

> CONTENT: Ordered list of all procedure files with one-line descriptions and links. Ordered by most-commonly-used first:
>
> **Core agent workflow:**
> - [start-queue-item.md](start-queue-item.md) — Claim top queue row, create branch, read linked docs
> - [plan-change.md](plan-change.md) — Create implementation plan with acceptance criteria and scope bounds
> - [implement-change.md](implement-change.md) — Execute code changes in small validated increments
> - [validate-change.md](validate-change.md) — Run full validation matrix before opening PR
> - [open-pull-request.md](open-pull-request.md) — Create PR with evidence and queue linkage
> - [handoff.md](handoff.md) — Write complete handoff documentation
> - [archive-queue-item.md](archive-queue-item.md) — Move completed queue row to archive
> - [handle-blocked-work.md](handle-blocked-work.md) — Document blockers and optionally requeue
>
> **Initialization:**
> - [initialize-repo.md](initialize-repo.md) — Full repo initialization from idea.md (6-phase procedure)
> - [validate-idea-md.md](validate-idea-md.md) — Validate idea.md completeness before initialization
> - [scaffold-domain-module.md](scaffold-domain-module.md) — Create bounded context module in apps/api/src/
> - [enable-profile.md](enable-profile.md) — Enable optional profile with dependency checking
>
> **Development lifecycle:**
> - [update-documentation.md](update-documentation.md) — When and how to update docs alongside code
> - [update-or-create-skill.md](update-or-create-skill.md) — Skill lifecycle management
> - [update-or-create-rule.md](update-or-create-rule.md) — Rule lifecycle management
> - [dependency-upgrade.md](dependency-upgrade.md) — Safe dependency upgrades with CI evidence
> - [database-migration.md](database-migration.md) — Alembic migrations with rollback notes
> - [release-preparation.md](release-preparation.md) — Changelog, version bump, tag, verification
> - [incident-rollback.md](incident-rollback.md) — Rollback during production incident
>
> **Architecture and governance:**
> - [extract-service-from-monolith.md](extract-service-from-monolith.md) — Strangler pattern service extraction
> - [add-optional-app-profile.md](add-optional-app-profile.md) — Enable web/mobile/worker profile
> - [add-queue-category.md](add-queue-category.md) — Add new queue category with validators
> - [add-prompt-template.md](add-prompt-template.md) — Add prompt template with full metadata
