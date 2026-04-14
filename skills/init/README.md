# skills/init/README.md

<!-- CROSS-REFERENCES -->
<!-- - Used by: prompts/repo_initializer.md, .cursor/commands/initialize.md -->
<!-- - Procedure: docs/procedures/initialize-repo.md -->

> PURPOSE: Index for initialization skills. Lists all skills used during the repo initialization process from idea.md. Per spec §28.7 item 328.

## Overview

> CONTENT: Brief description of the initialization skill collection. State that these skills are invoked exclusively during repository initialization (the process of turning the blank template into a configured project). The repo_initializer prompt orchestrates these skills in sequence.

## Skills in This Category

> CONTENT: Table of initialization skills. Columns: Skill, Machinery, Purpose. Rows:
> - idea-validator.md | idea-validator.py | Validate idea.md completeness and consistency
> - archetype-mapper.md | archetype-mapper.py | Map archetype+profiles to scaffolding plan
> - module-template-generator.md | (uses backend/module-scaffolder.py) | Generate domain module files
> - queue-seeder.md | queue-seeder.py | Populate queue.csv from idea.md §12
> - profile-resolver.md | profile-resolver.py | Resolve profile enablement with dependency checking
> - env-generator.md | env-generator.py | Generate .env.example for enabled profiles

## Invocation Order

> CONTENT: The initialization skills are invoked in this order during initialization:
> 1. idea-validator.md — Phase 1 (Validate and Plan)
> 2. archetype-mapper.md — Phase 1 (Validate and Plan)
> 3. profile-resolver.md — Phase 4 (Configure Profiles)
> 4. env-generator.md — Phase 4 (Configure Profiles)
> 5. module-template-generator.md — Phase 3 (Scaffold Domain)
> 6. queue-seeder.md — Phase 5 (Seed Queue)

## Related Resources

> CONTENT: Links to docs/procedures/initialize-repo.md, prompts/repo_initializer.md, .cursor/commands/initialize.md, spec/spec.md §27
