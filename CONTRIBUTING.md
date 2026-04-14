# CONTRIBUTING.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Referenced by: README.md, .github/PULL_REQUEST_TEMPLATE.md -->
<!-- - Links to: AGENTS.md, queue/QUEUE_INSTRUCTIONS.md, docs/procedures/open-pull-request.md -->

> PURPOSE: Contribution guide for both humans and agents. Links to AGENTS.md (agent policy), the queue system (agent work orchestration), and key procedures. Per spec §26.1 item 9.

## How to Contribute

> CONTENT: Opening paragraph that welcomes both human contributors and AI agents. State that this repository is primarily agent-operated; humans contribute by filling out `idea.md`, reviewing PRs, and maintaining the machine (rules, skills, procedures, CI). Link to AGENTS.md as the primary policy document.

## Development Setup

> CONTENT: Brief setup overview with link to `docs/getting-started/` for detailed instructions. Quick steps: clone → `./setup.sh` → `make dev`. Mention that `setup.sh` handles all dependencies, environment, and initial validation. Link to `docs/development/local-setup.md` for all Make targets.

## Branch Naming Conventions

> CONTENT: Two valid branch naming patterns:
> - **Queue-driven work:** `queue/<id>-short-slug` — the queue item ID is mandatory in the branch name
> - **Agent/Cursor initiated:** `cursor/<descriptive-slug>-<4-char-suffix>` — for non-queue agent work
> - **Human hotfixes:** `hotfix/<description>` — for urgent human-initiated fixes
>
> State that branches without a valid naming pattern will not be accepted for merge.

## Pull Request Process

> CONTENT: Steps for opening a PR. Reference `.github/PULL_REQUEST_TEMPLATE.md` as the required description format. Key requirements:
> - All CI checks must be green
> - PR description must include: queue ID (if applicable), files changed, commands run with output, tests added/updated, docs updated, risks
> - Link to `docs/procedures/open-pull-request.md` for the full SOP
> - No direct push to main — all changes via PR
> - One logical change per PR where possible

## Queue-Driven Work

> CONTENT: Explanation of the CSV queue as the primary agent work orchestration system (not a product backlog). Key points:
> - `queue/queue.csv` top row = the current active work item
> - Agents read the full row, branch as `queue/<id>-slug`, implement, and archive on completion
> - Link to `queue/QUEUE_INSTRUCTIONS.md` for the full SOP
> - Link to `docs/procedures/start-queue-item.md` and `docs/procedures/archive-queue-item.md`
> - State: "Adding items to the queue is how humans direct agent work."

## Code of Conduct

> CONTENT: Brief reference to CODE_OF_CONDUCT.md (if present) or statement that contributors are expected to be respectful and constructive. Link to the file.

## Questions and Escalation

> CONTENT: Where to go for help. For spec or policy questions: open a GitHub issue. For blocked queue items: follow `docs/procedures/handle-blocked-work.md`. For security concerns: see SECURITY.md. For architecture questions: open a discussion or create an ADR PR.
