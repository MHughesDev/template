---
alwaysApply: true
description: Universal constraints applied to every agent interaction in this repository.
---

# .cursor/rules/global.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: AGENTS.md §13, PYTHON_PROCEDURES.md -->
<!-- - Enforced by: scripts/audit-self.sh, scripts/rules-check.sh -->

> PURPOSE: Universal constraints applied to every agent interaction. Covers commit message format, scope discipline, evidence requirements, forbidden behaviors, file title comment standard (§1.7), and mandatory skill search before execution (§4.1 item 13). Per spec §26.2 item 11.

## Section: Commit Standards

> CONTENT: Numbered rules for commit messages. Rules:
> 1. Use Conventional Commits format: `<type>(<scope>): <short description>` where type is one of: feat, fix, docs, refactor, test, chore, ci, style, perf, security
> 2. Short description ≤ 72 characters
> 3. Body (if present) explains WHY not WHAT; references queue ID if applicable (`Closes queue/Q-001`)
> 4. NEVER commit with `--no-verify` (bypasses pre-commit hooks)
> 5. One logical change per commit; squash accidental commits before PR
> 6. Commit message must accurately describe the change — no "WIP", "fix", "update" without context

## Section: Scope Discipline

> CONTENT: Rules for preventing scope creep. Rules:
> 1. Only modify files directly within the scope of the current task
> 2. Out-of-scope discoveries: stop, create a queue row or GitHub issue, reference it in PR, do NOT fix in this PR
> 3. Before any file edit, verify the file is in the planned scope (established in planning step)
> 4. "While I'm here" fixes require explicit approval — create a separate PR
> 5. If scope expands by more than 20% from the plan, re-plan and document the expansion

## Section: Evidence and Handoff Requirements

> CONTENT: Rules for what evidence must accompany every meaningful change. Rules:
> 1. Every PR description must include: commands run + key output, files changed list, tests added/updated, docs updated
> 2. Queue notes must be updated before archiving (PR URL, completion date)
> 3. If a command fails in CI, paste the failure output in PR comments — do not just say "CI failed"
> 4. After any deployment or migration, capture health check output as evidence
> 5. ADR required for architectural decisions; link to the ADR in PR description

## Section: File Title Comment Standard (§1.7)

> CONTENT: Rules enforcing the file title comment standard. Per spec §1.7 — every file must begin with a path/title comment.
> Rules:
> 1. Python files: first line must be `# path/to/file.py` (exact path from repo root)
> 2. Markdown files: first line must be `# path/to/filename.md` (H1 with path) OR `<!-- path/to/filename.md -->` when different H1 is needed
> 3. YAML files: first line must be `# filename.yml` (just filename or full path)
> 4. Shell scripts: after shebang line, next line is `# scripts/filename.sh`
> 5. Dockerfile: first non-comment line is `# apps/api/Dockerfile` or equivalent
> 6. CSV files: `# queue/queue.csv` before the header row
> 7. Batch files: `REM filename.bat`
> 8. JSON files: WAIVED (JSON does not support comments)
> 9. Enforcement: `scripts/audit-self.sh` checks all non-JSON files for title comments
> 10. No file is ever empty — stubs must at minimum contain the title comment

## Section: Mandatory Skill Search (§4.1 item 13)

> CONTENT: The non-negotiable mandatory skill search rule. This is the most important rule in this file.
> Rules:
> 1. BEFORE beginning ANY task — regardless of trigger (queue, prompt, command, manual, any source) — search `skills/` for relevant skills
> 2. Procedure: `make skills:list` OR read `skills/README.md` → scan all "When to invoke" sections → read every relevant skill in full
> 3. Note machinery files (`.py` alongside `.md`) as available automation tools
> 4. For complex domain matching: use `prompts/skill_searcher.md` as a subroutine
> 5. NEVER start planning or writing code before this step is complete
> 6. Document which skills were found and used in the PR description or queue notes
> 7. If no relevant skill exists for a recurring pattern: that is a signal to create one

## Section: Forbidden Patterns

> CONTENT: Explicit prohibitions — behaviors that will cause PR rejection. Rules:
> 1. NEVER commit secrets, credentials, tokens, passwords, API keys to the repository
> 2. NEVER bypass CI: no `--no-verify`, no direct push to main, no force push to main
> 3. NEVER use `os.getenv()` outside `apps/api/src/config.py` (use Pydantic BaseSettings via DI)
> 4. NEVER use `Any` type annotation without a documented justification comment
> 5. NEVER add `# type: ignore` without an explanatory comment on the same line
> 6. NEVER query the database from a router handler (use service layer)
> 7. NEVER hardcode environment-specific values (URLs, IDs, credentials)
> 8. NEVER swallow exceptions silently (`except Exception: pass` is always wrong)
> 9. NEVER use ad hoc shell commands when a canonical `make` target exists
> 10. NEVER skip the mandatory skill search before beginning work
> 11. NEVER use `print()` for logging in production code (use `logger`)
> 12. NEVER mutate shared state between requests (use request-scoped dependencies)
