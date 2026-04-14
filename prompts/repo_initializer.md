---
purpose: "Initialize the repository from a filled idea.md, configuring the entire project machine from scratch."
when_to_use: "First action after cloning the template with a filled idea.md. Do not use on a repo that is already initialized."
required_inputs:
  - name: "idea.md"
    description: "Fully filled project intake form with all 17 sections completed"
expected_outputs:
  - "Initialization PR with all phases completed and CI passing"
  - "Configured README.md, pyproject.toml, .env.example, docker-compose.yml with project specifics"
  - "Scaffolded domain modules for each bounded context in idea.md §4"
  - "Configured profiles per idea.md §5"
  - "Seeded queue/queue.csv from idea.md §12"
validation_expectations:
  - "make lint passes"
  - "make typecheck passes"
  - "make test passes (stub tests)"
  - "make audit:self passes"
  - "make queue:validate passes"
constraints:
  - "Does not modify spec/spec.md"
  - "Does not write final implementations — scaffolds stubs only"
  - "Does not merge the initialization PR — human reviews first"
linked_commands:
  - "make idea:validate"
  - "make scaffold:module"
  - "make profile:enable"
  - "make idea:queue"
  - "make audit:self"
linked_procedures:
  - "docs/procedures/initialize-repo.md"
  - "docs/procedures/validate-idea-md.md"
  - "docs/procedures/scaffold-domain-module.md"
  - "docs/procedures/enable-profile.md"
linked_skills:
  - "skills/init/idea-validator.md"
  - "skills/init/archetype-mapper.md"
  - "skills/init/profile-resolver.md"
  - "skills/init/queue-seeder.md"
  - "skills/init/env-generator.md"
  - "skills/init/module-template-generator.md"
  - "skills/backend/fastapi-router-module.md"
---

# prompts/repo_initializer.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - This is the MOST IMPORTANT prompt in the template library -->
<!-- - Referenced by: .cursor/commands/initialize.md, docs/agents/initialization-guide.md -->
<!-- - Procedure: docs/procedures/initialize-repo.md (canonical source for steps) -->

## Preamble (Mandatory)

> CONTENT: Standard preamble that MUST appear in every prompt body. Content:
> "Before taking any action:
> 1. Run `make skills:list` or read `skills/README.md`
> 2. Scan all 'When to invoke' sections for skills relevant to initialization
> 3. Read ALL initialization skills in `skills/init/` in full
> 4. Also read: skills/backend/fastapi-router-module.md, skills/backend/service-repository-pattern.md
> 5. Do not begin until this step is complete.
> Reference: AGENTS.md §13 (Mandatory Skill Search)"

## Role Definition

> CONTENT: Role statement for the initialization agent. State:
> "You are the Repository Initialization Agent. Your authority scope is the entire repository. Your mission is to transform this blank template into a configured, running project ready for queue-driven development. You have full authority to create and modify files during initialization. You do NOT modify spec/spec.md, spec/IMPLEMENTATION_PLAN.md, PYTHON_PROCEDURES.md, skills/, or prompts/ (except to consume them)."

## Context Injection Points

> CONTENT: Describe the context injection model. The agent reads:
> - `{{idea_md_content}}` — the full contents of idea.md (read the actual file)
> - `{{spec_sections}}` — relevant sections from spec/spec.md (§27.3, §27.4)
>
> No literal injection — the agent reads the files directly.

## Archetype-to-Profile Mapping Table

> CONTENT: Reproduce the spec §27.3 mapping table in full for quick lookup during initialization:
> | Archetype | Profiles enabled by default | Default queue categories |
> |-----------|----------------------------|--------------------------|
> | API service | (none required) | core-api, infrastructure, testing, documentation |
> | Full-stack web app | web | core-api, frontend, infrastructure, testing, documentation |
> | Full-stack with mobile | web, mobile | core-api, frontend, mobile, infrastructure, testing, documentation |
> | Platform / internal tool | workers | core-api, admin, infrastructure, testing, documentation |
> | Data pipeline / ETL | workers, scheduled-jobs | pipeline, infrastructure, testing, documentation |
> | AI / ML service | ai-rag, workers | core-api, ai, infrastructure, testing, documentation |
> | Marketplace / multi-sided | web, multi-tenancy | core-api, marketplace, frontend, infrastructure, testing, documentation |
> | SaaS product | web, multi-tenancy, billing | core-api, saas, frontend, billing, infrastructure, testing, documentation |

## Phase-by-Phase Execution Instructions

> CONTENT: The 6-phase initialization procedure per spec §27.4. Each phase has checkpoint commands that must pass before proceeding:
>
> **Phase 1 — Validate and Plan**
> Steps 1-5 from spec §27.4. Run make idea:validate. Produce initialization plan document (list files to create, profiles to enable, queue items to seed). Do not proceed if plan is not complete.
>
> **Phase 2 — Configure Root**
> Steps 6-11 from spec §27.4. Update README.md, pyproject.toml, .env.example, docker-compose.yml, AGENTS.md mission section, and .cursor/rules/ with project-specific constraints. Checkpoint: make lint passes.
>
> **Phase 3 — Scaffold Domain**
> Steps 12-15 from spec §27.4. For each bounded context in idea.md §4.2, run make scaffold:module. Register routers. Create initial migration. Update docs/api/endpoints.md. Checkpoint: make typecheck passes.
>
> **Phase 4 — Configure Profiles**
> Step 16 from spec §27.4. For each enabled profile, run make profile:enable <profile>. Verify Compose, env vars, package stubs, and docs. Checkpoint: make test passes.
>
> **Phase 5 — Seed Queue**
> Steps 17-20 from spec §27.4. Run make idea:queue to extract items from idea.md §12. Add blocked items for open questions from idea.md §16. Run make queue:validate.
>
> **Phase 6 — Validate and Handoff**
> Steps 21-24 from spec §27.4. Run make lint && make fmt && make typecheck. Run make test. Run make audit:self. Create initialization PR with full evidence.

## Profile Enablement Decision Tree

> CONTENT: Step-by-step decision logic for each profile:
> - Web: if idea.md §5 web=yes → make profile:enable web → creates apps/web/ with AGENTS.md and README.md
> - Mobile: if idea.md §5 mobile=yes → make profile:enable mobile → creates apps/mobile/
> - Workers: if idea.md §5 workers=yes → make profile:enable worker → scaffolds packages/tasks implementations, adds Redis to Compose
> - AI/RAG: if idea.md §5 ai=yes → make profile:enable ai → scaffolds packages/ai/ implementations, adds ChromaDB to Compose
> - Multi-tenancy: if idea.md §5 multi-tenancy=yes → verify TenantContextMiddleware is active, add tenant fixtures
> - Each additional profile: create integration stub under packages/<profile>/

## Validation Checklist Before PR

> CONTENT: Pre-PR checklist the initialization agent MUST complete:
> - [ ] idea.md has no placeholder HTML comments remaining
> - [ ] All bounded contexts from idea.md §4.2 have scaffolded modules
> - [ ] All enabled profiles from idea.md §5 are configured
> - [ ] queue/queue.csv has all items from idea.md §12
> - [ ] make lint passes
> - [ ] make fmt passes (no formatting changes)
> - [ ] make typecheck passes
> - [ ] make test passes (stub tests)
> - [ ] make queue:validate passes
> - [ ] make audit:self passes
> - [ ] README.md updated with project name and description
> - [ ] AGENTS.md mission section updated with project context
> - [ ] .env.example has all vars for enabled profiles

## Output Format

> CONTENT: Required format for the initialization PR description. Sections:
> - Summary: what was initialized (archetype, profiles, modules)
> - Phase 1 output: validation report (pass/fail per idea.md section)
> - Phase 2-5 output: files created/modified per phase
> - Phase 6 output: all validation commands with output
> - Open questions: items from idea.md §16 that became blocked queue items
> - Next steps: first queue item to process after PR is merged
