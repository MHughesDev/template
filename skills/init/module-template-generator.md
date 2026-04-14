# skills/init/module-template-generator.md

<!-- CROSS-REFERENCES -->
<!-- - Uses: skills/backend/module-scaffolder.py -->
<!-- - Procedure: docs/procedures/scaffold-domain-module.md -->

**Purpose:** [FULL SKILL] Generate all files for multiple domain modules from entity definitions during initialization. Uses skills/backend/module-scaffolder.py machinery. Per spec §28.7 item 333.

## Purpose

One paragraph. During initialization, multiple domain modules must be created at once (not one at a time). This skill orchestrates batch module scaffolding from the initialization plan produced by archetype-mapper.py, handles router registration order, and sequences Alembic migration creation.

## When to Invoke

During initialization Phase 3 (Scaffold Domain). Invoked once per initialization with the full list of contexts from the initialization plan.

## Prerequisites

archetype-mapper.py plan available. skills/backend/fastapi-router-module.md read. apps/api/src/ directory exists. Alembic configured.

## Relevant Files/Areas

apps/api/src/ (all module directories), apps/api/src/main.py, apps/api/tests/, skills/backend/module-scaffolder.py

## Step-by-Step Method

Numbered steps:
1. Read initialization plan: list of contexts + entities
2. For each context in dependency order (auth first, then core modules, then secondary):
   a. Run `python skills/backend/module-scaffolder.py <context> <entities>`
   b. Verify all module files created
   c. Register router in main.py
3. After all modules: create initial Alembic migration for all models together
   - `make migrate:create MESSAGE="init: create all domain tables"`
   - Test migration: `make migrate && alembic downgrade -1 && alembic upgrade head`
4. Run `make typecheck` to verify all generated code type-checks
5. Run `make test` to verify test stubs run (even if they raise NotImplementedError)

## Command Examples

- `python skills/backend/module-scaffolder.py invoices Invoice,LineItem` — one module
- `make migrate:create MESSAGE="init: domain tables"` — create migration
- `make migrate` — apply migration
- `make typecheck` — verify generated code

## Validation Checklist

- [ ] All contexts from initialization plan have scaffolded modules
- [ ] All routers registered in main.py
- [ ] make typecheck passes (generated code type-safe)
- [ ] make migrate succeeds
- [ ] alembic downgrade -1 succeeds
- [ ] make test passes (stubs run without crashing)

## Common Failure Modes

Cross-module imports at initialization time → circular import. Fix: use packages/contracts/ for shared types from the start.

## Handoff Expectations

All modules scaffolded, migrations applied, tests passing (even if all NotImplementedError).

## Related Procedures

docs/procedures/scaffold-domain-module.md, docs/procedures/initialize-repo.md

## Related Prompts

prompts/repo_initializer.md

## Related Rules

.cursor/rules/apps-api.md, .cursor/rules/initialization.md
