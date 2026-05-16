# .cursor/commands/initialize.md

Run the **full repository initialization** flow from a filled **`idea.md`**, using the master prompt and init skills.

| Field | Value |
|-------|--------|
| **Name** | Initialize repository |
| **Description** | Read **`idea.md`**, validate, map archetype → profiles, scaffold modules, seed **`queue/`**, generate env — produce one initialization PR. |
| **When to use** | New project bootstrap after **`idea.md`** is complete. |
| **Prerequisites** | Python 3.12+, Docker, Make; **`idea.md`** filled (no placeholder-only sections). |
| **Primary prompt** | [`prompts/repo_initializer.md`](../prompts/repo_initializer.md) |
| **Procedure** | [`docs/procedures/initialize-repo.md`](../docs/procedures/initialize-repo.md) |
| **Skills** | [`skills/init/idea-validator.md`](../skills/init/idea-validator.md), [`skills/init/initialize-repo.md`](../skills/init/initialize-repo.md), [`skills/init/queue-seeder.md`](../skills/init/queue-seeder.md) |

## Steps

1. Read this command and **[AGENTS.md](../AGENTS.md)** — run **mandatory skill search** before coding.
2. Open and read [`prompts/repo_initializer.md`](../prompts/repo_initializer.md) end-to-end.
3. Read **`idea.md`** completely; do not scaffold until it is coherent.
4. Run **`make idea:validate`** (or `scripts/validate-idea.sh`) — fix failures before continuing.
5. Execute [`docs/procedures/initialize-repo.md`](../docs/procedures/initialize-repo.md) (validate → docs initialization → docs-derived queue → verify).
6. Run **`make lint`**, **`make typecheck`**, **`make test`**, **`make audit:self`** (or the closest available targets).
7. Open **one** PR to **`main`** with evidence: commands, files touched, risks, profiles enabled.

## Expected output

- Initialization **PR** with green CI.
- Project documentation initialized per **`idea.md`**.
- **`queue/queue.csv`** seeded from generated docs (with `idea.md` §12 as optional hints).
- `docs/project-state.md` updated for fast orientation.
