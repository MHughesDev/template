# docs/procedures/initialize-from-idea.md

## Purpose

Execute structured repository initialization from a completed `idea.md` using the
initialization engine. Produces a deterministic, auditable initialization PR.

## Trigger / when to use

- When cloning this template for a new project
- After filling `idea.md` completely for the first time
- When re-initializing after a significant archetype change (rare)

## Prerequisites

- `idea.md` filled out completely with no `<!--` placeholders in required sections
- INIT_META block present in `idea.md` with `initialized: false`
- Python 3.12+ available
- Docker and Docker Compose available
- `make idea:validate` passes with zero errors

## Exact commands

```text
make idea:validate       # must pass before proceeding
make idea:parse          # produces init-manifest.json — review it
make idea:plan           # dry-run: print decisions without executing (optional review step)
make idea:execute        # execute all decisions; opens PR when done
# OR the all-in-one:
make init:from-idea      # validate + parse + execute sequentially
```

## Ordered steps

1. Fill `idea.md` completely. Validate: `make idea:validate`
2. Review resolved decisions: `make idea:plan`
3. If decisions look wrong: adjust `idea.md` and re-run step 1–2.
4. Execute: `make idea:execute` (or `make init:from-idea` for one command)
5. Review the opened PR diff carefully:
   - Verify bounded context scaffolding is correct
   - Verify env vars are complete
   - Verify queue items have rich summaries
   - Resolve open questions from `idea.md §16`
6. Merge the PR to main.
7. Delete the initialization branch:
   `git branch -d feature/idea-init-engine && git push origin --delete feature/idea-init-engine`
8. Run `./setup.sh` (or `./run.sh` if already set up) to boot the initialized project.

## Expected artifacts / outputs

- `init-manifest.json` — the resolved initialization plan (commit it)
- Modified `idea.md` §18 initialization log
- New modules under `apps/api/src/<context>/`
- New packages under `packages/` per enabled profiles
- Updated `docker-compose.yml` with activated services
- Updated `.env.example` with all required env vars
- Seeded `queue/queue.csv` with initial work items
- Initialization PR on `feature/idea-init-engine`

## Validation checks

- `make queue:validate` — queue schema and lifecycle
- `make audit:self` — full repo self-audit
- `make test` — all tests pass (stubs generate passing placeholder tests)
- `make lint` — no lint errors in generated code

## Rollback / failure handling

- Parser failures: fix `idea.md` validation errors, re-run `make idea:parse`
- Profile script failures: check `init-manifest.log`, fix the failing script, re-run
  `scripts/profiles/enable-<profile>.sh` manually, then continue with `make idea:execute`
- Orchestrator aborts mid-run: it is idempotent — re-running will skip already-completed
  steps (detect by checking if modules already exist, if env vars already present, etc.)
- To fully reset: delete `init-manifest.json`, reset `idea.md` INIT_META to
  `initialized: false`, and re-run.

## Handoff expectations

After the initialization PR merges:

- CODEBASE_SUMMARY.md reflects new module count
- Queue has initial work items with rich summaries
- Next agent reads queue top row and begins implementation work
- `docs/agents/supervision-guide.md` reviewed by human maintainer

## Related procedures

- `docs/procedures/scaffold-domain-module.md`
- `docs/procedures/start-queue-item.md`
- `docs/procedures/validate-idea-md.md`

## Related prompts

- `prompts/repo_initializer.md`
- `prompts/domain_modeler.md`

## Related rules

- `.cursor/rules/global.md` (mandatory skill search before execution)
- `.cursor/rules/queue.md` (queue lifecycle)
