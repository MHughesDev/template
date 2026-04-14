---
globs:
  - "prompts/**"
description: Rules for prompt files. Ensures prompts have required YAML front matter and follow the metadata convention.
---

# .cursor/rules/prompts.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: docs/procedures/add-prompt-template.md, docs/prompts/conventions.md -->
<!-- - Validation: skills/repo-governance/rule-linter.py -->

> PURPOSE: Rules governing prompt template files in prompts/. Ensures every prompt has complete YAML front matter with all §7.2 required fields, uses the standard placeholder syntax, includes a validation checklist, and links to at least one procedure. Per spec §28.5 item 297.

## Section: Required YAML Front Matter

> CONTENT: Rules about required metadata. Rules:
> 1. Every prompt `.md` file MUST begin with YAML front matter delimited by `---`
> 2. Required front matter fields (per spec §7.2): `purpose`, `when_to_use`, `required_inputs`, `expected_outputs`, `validation_expectations`, `constraints`, `linked_commands`, `linked_procedures`, `linked_skills`
> 3. `purpose` must be a single clear sentence
> 4. `when_to_use` must be a specific trigger description (not "when you need to...")
> 5. `required_inputs` is a list of named inputs the template needs to work
> 6. `expected_outputs` is a list of artifacts the prompt produces

## Section: Prompt Body Requirements

> CONTENT: Rules about prompt body content. Rules:
> 1. Every prompt body MUST begin with a preamble that includes: reference to mandatory skill search (AGENTS.md §13), reference to prompts/skill_searcher.md as a subroutine
> 2. Placeholder variables use `{{double_braces}}` syntax — no other placeholder format
> 3. Every prompt MUST include a section describing the agent's role (e.g., "You are the implementation agent...")
> 4. Every prompt MUST include an ordered step-by-step execution section
> 5. Every prompt MUST include a validation checklist using `- [ ]` format at the end
> 6. Output format requirements must be explicitly stated (e.g., "Produce a PR description in markdown")

## Section: Prompt Linking Requirements

> CONTENT: Rules about linking prompts to other artifacts. Rules:
> 1. Every prompt MUST link to at least one `docs/procedures/` file in `linked_procedures`
> 2. Every prompt MUST link to at least one `skills/` file in `linked_skills`
> 3. The `docs/prompts/index.md` MUST be updated when a new prompt is added
> 4. When updating a prompt, verify all linked procedures and skills still exist and are relevant
> 5. Deprecated prompts MUST have a `deprecated: true` front matter field and a note pointing to the replacement
