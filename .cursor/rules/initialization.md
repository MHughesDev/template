---
globs:
  - "idea.md"
  - "prompts/repo_initializer.md"
  - "skills/init/*.md"
description: Initialization guardrails for the AI-driven documentation-first repo setup.
---

# .cursor/rules/initialization.md

## Required behavior

1. Treat `idea.md` as the initialization input contract.
2. Run `make idea:validate` before initialization work.
3. Follow `skills/init/initialize-repo.md` (documentation generation) before queue seeding.
4. Follow `skills/init/queue-seeder.md` with docs as source of truth; use `idea.md` §12 only as optional hints.
5. Do not use legacy/deleted pipeline artifacts (`init-manifest.json`, `make idea:parse`, `make idea:queue`, `scripts/init-from-idea.sh`, `scripts/idea-to-queue.sh`).
6. Validate initialization artifacts with `make docs:check` and `make queue:validate`.

## Prohibited

- Do not modify `spec/spec.md` during initialization unless explicitly requested.
- Do not execute obsolete phased scripts from older initialization flow.
