# docs/procedures/initialize-repo.md

<!-- CROSS-REFERENCES -->
<!-- - Referenced by: prompts/repo_initializer.md, .cursor/commands/initialize.md -->
<!-- - Skills: skills/init/ (all), skills/backend/fastapi-router-module.md -->

> PURPOSE: SOP for initializing the repo from idea.md. The canonical procedure that the repo_initializer prompt follows. Turns a blank template into a configured project. Per spec §28.3 item 281 and §8.3.

## Purpose

> CONTENT: Full sentence describing: this procedure turns the blank template repository into a configured, working project by reading idea.md, scaffolding domain modules, configuring profiles, seeding the queue, and producing an initialization PR.

## Trigger / When to Use

> CONTENT: When idea.md has been filled out completely (all 17 sections, no placeholder HTML comments) and the template needs to be initialized for a specific project.

## Prerequisites

> CONTENT:
> - idea.md filled with real content (all 17 sections)
> - `make idea:validate` passes
> - Python 3.12+, Docker, Make installed
> - Fresh clone of the template repository
> - No prior initialization has been run

## Exact Commands

> CONTENT: List of all make targets used in this procedure:
> - `make idea:validate` — Phase 1: validate idea.md
> - `make scaffold:module MODULE=<name>` — Phase 3: scaffold each module
> - `make profile:enable PROFILE=<name>` — Phase 4: enable each profile
> - `make idea:queue` — Phase 5: seed queue from idea.md §12
> - `make queue:validate` — Phase 5: verify queue
> - `make lint && make fmt && make typecheck && make test` — Phase 6: validate
> - `make audit:self` — Phase 6: spec compliance check

## Ordered Steps

> CONTENT: The 6-phase procedure per spec §27.4. Each phase with numbered sub-steps and checkpoint commands.
>
> **Phase 1 — Validate and Plan**
> 1. Read idea.md completely (every section)
> 2. Run `make idea:validate` — fix any failing sections before proceeding
> 3. Flag open questions from idea.md §16 — create blocked queue items for each
> 4. Run `python skills/init/archetype-mapper.py idea.md` — generate initialization plan
> 5. Document the plan (store in PR description draft or a temporary file)
> CHECKPOINT: idea:validate passes, plan documented
>
> **Phase 2 — Configure Root**
> 6. Update README.md: replace placeholder project name/description with idea.md §1
> 7. Update pyproject.toml: project name, description, initial dependencies from idea.md §5
> 8. Run `python skills/init/env-generator.py --profiles <resolved_profiles>` → .env.example
> 9. Update docker-compose.yml: enable profile services per resolved profiles
> 10. Update AGENTS.md §1 (Mission): add project-specific context from idea.md §2
> 11. Add project-specific constraints to .cursor/rules/ from idea.md §13 (hard constraints)
> CHECKPOINT: make lint passes
>
> **Phase 3 — Scaffold Domain**
> 12. For each bounded context in idea.md §4.2:
>     - `make scaffold:module MODULE=<context_name>`
>     - Register router in apps/api/src/main.py
> 13. Create initial Alembic migration: `make migrate:create MESSAGE="init: create domain tables"`
> 14. Apply migration: `make migrate`
> 15. Update docs/api/endpoints.md with stub endpoint descriptions
> CHECKPOINT: make typecheck passes
>
> **Phase 4 — Configure Profiles**
> 16. For each enabled profile: `make profile:enable PROFILE=<name>`
>     - Each profile enables its Compose service, adds env vars, creates stubs
> CHECKPOINT: make test passes (stub tests)
>
> **Phase 5 — Seed Queue**
> 17. Run `make idea:queue` — extract items from idea.md §12
> 18. Add blocked items for each open question in idea.md §16
> 19. Add standard verification items (review init PR, run all make targets)
> 20. Run `make queue:validate` — verify queue integrity
> CHECKPOINT: queue:validate passes
>
> **Phase 6 — Validate and Handoff**
> 21. Run `make lint && make fmt`
> 22. Run `make typecheck`
> 23. Run `make test`
> 24. Run `make audit:self`
> 25. Create initialization PR with full evidence per step 5-6 outputs

## Expected Artifacts / Outputs

> CONTENT:
> - Initialization PR with evidence of all 6 phases
> - Updated: README.md, pyproject.toml, .env.example, docker-compose.yml, AGENTS.md
> - Scaffolded: one module directory per bounded context in apps/api/src/
> - Configured: all enabled profiles (Compose, env vars, stubs)
> - Seeded: queue/queue.csv with items from idea.md §12
> - Passing: all CI checks on the initialization PR

## Validation Checks

> CONTENT:
> - [ ] make idea:validate passes
> - [ ] All bounded contexts from idea.md §4.2 have modules
> - [ ] make lint passes
> - [ ] make typecheck passes
> - [ ] make test passes
> - [ ] make queue:validate passes
> - [ ] make audit:self passes

## Rollback or Failure Handling

> CONTENT: If any phase fails: stop. Do not proceed to next phase. Fix the failing step and re-run the phase from the beginning. For Phase 6 failures: fix the lint/type/test error before creating the PR.

## Handoff Expectations

> CONTENT: Initialization PR opened with full evidence. PR description includes: phases completed, commands run with output, files changed, CI results. First queue item identified and ready for next agent to process.
