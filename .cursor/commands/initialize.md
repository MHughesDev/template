# .cursor/commands/initialize.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Links to: prompts/repo_initializer.md, docs/procedures/initialize-repo.md -->
<!-- - Skills: skills/init/ -->

> PURPOSE: Reusable Cursor command definition for full repo initialization flow. Provides a named shortcut that an agent can invoke by referencing this command. Per spec §28.9 item 336.

## Command Metadata

> CONTENT: YAML or structured metadata block for the command. Fields:
> - name: "Initialize Repository"
> - description: "Run the full repo initialization flow from idea.md. Reads idea.md, maps archetype to profiles, scaffolds domain modules, seeds queue, and produces initialization PR."
> - trigger: "Reference this command and idea.md to start initialization"
> - prerequisites:
>   - idea.md is filled out (all 17 sections, no placeholder comments remaining)
>   - Template repository freshly cloned
>   - Python 3.12+, Docker, Make installed
> - linked_prompt: prompts/repo_initializer.md
> - linked_procedure: docs/procedures/initialize-repo.md
> - linked_skills:
>   - skills/init/idea-validator.md
>   - skills/init/archetype-mapper.md
>   - skills/init/profile-resolver.md
>   - skills/init/queue-seeder.md
>   - skills/init/env-generator.md

## Steps

> CONTENT: Ordered execution steps that the agent follows when this command is invoked:
> 1. Read this command definition completely
> 2. Read prompts/repo_initializer.md completely (the master prompt)
> 3. Read idea.md completely — do not start until read in full
> 4. Run `make idea:validate` to check idea.md completeness
> 5. If validation fails: list failing sections and STOP — do not proceed until human fills them
> 6. Follow the 6-phase initialization procedure in docs/procedures/initialize-repo.md
> 7. Run `make audit:self` after all phases complete
> 8. Create initialization PR with full evidence

## Expected Output

> CONTENT: What the agent produces when this command completes:
> - One initialization PR against main branch
> - All modules scaffolded per idea.md §4
> - All profiles configured per idea.md §5
> - queue/queue.csv seeded from idea.md §12
> - All CI checks passing
> - Documentation updated (README, AGENTS.md mission, .env.example)
