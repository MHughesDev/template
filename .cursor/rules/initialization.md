---
globs:
  - "idea.md"
  - "prompts/repo_initializer.md"
description: Rules active during repo initialization. Ensures the initializer follows the correct procedure and produces a complete initialization PR.
---

# .cursor/rules/initialization.md

Constraints for **repo initialization** from **`idea.md`** (see **`docs/procedures/initialize-repo.md`**, **`prompts/repo_initializer.md`**, **`skills/init/`**).

## Before changing files

1. Read **`idea.md`** end-to-end before creating or modifying project files.
2. Run **`make idea:validate`** or **`scripts/validate-idea.sh`** when available.
3. Do not proceed if required sections are still placeholder-style empty.
4. Do **not** edit **`spec/spec.md`** during initialization — it stays canonical.
5. Write a short **plan** (profiles, modules, queue seeds, files to touch) before execution.

## Phases

Follow the phased init procedure in **`docs/procedures/initialize-repo.md`**:

1. Validate and plan before bulk writes.
2. Configure root metadata and env templates before deep scaffolding.
3. Scaffold domains before enabling optional profiles (unless the procedure orders otherwise).
4. Seed **queue** rows after core scaffolding.
5. Finish with **`make lint`**, **`make typecheck`**, **`make test`**, **`make audit:self`** (or the closest available targets).

## Initialization PR

1. Title like **`chore: initialize repository from idea.md — <project-name>`**.
2. Description lists archetype, profiles, modules, queue items, and **commands run with output**.
3. Open a **PR** to **`main`** — no direct push.
4. **All CI checks** must pass before merge.

## Do not rewrite the machine library

During initialization, **consume** **`skills/`** and **`prompts/`**; do not redesign the whole library unless that is explicitly in scope. CI layout should only change when required for the new project, with review.
