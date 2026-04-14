# skills/agent-ops/handoff-template-generator.py
"""
BLUEPRINT: skills/agent-ops/handoff-template-generator.py

PURPOSE:
Generates a pre-filled handoff document from git diff, recent commands, and
queue state. Reduces token cost and error rate by auto-populating boilerplate
sections of the handoff document. The generated template is then filled in
by the agent with acceptance criteria verification, risks, and follow-ups.

DEPENDS ON:
- subprocess (stdlib) — run git commands
- csv (stdlib) — read queue.csv for current item
- pathlib (stdlib) — file paths
- argparse (stdlib) — CLI argument parsing
- datetime (stdlib) — timestamp generation

DEPENDED ON BY:
- skills/agent-ops/implementation-handoff.md — references this as machinery

FUNCTIONS:

  get_git_diff_stat(base_ref: str = "HEAD~1") -> str:
    PURPOSE: Run `git diff --stat <base_ref>..HEAD` and return output.
    STEPS:
      1. subprocess.run(["git", "diff", "--stat", f"{base_ref}..HEAD"])
      2. Return stdout as string
    RETURNS: Formatted diff stat string
    RAISES: RuntimeError if git command fails

  get_changed_files(base_ref: str = "HEAD~1") -> list[tuple[str, str]]:
    PURPOSE: Return list of (filename, change_type) pairs for files changed since base_ref.
    STEPS:
      1. subprocess.run(["git", "diff", "--name-status", base_ref])
      2. Parse output: "A filename" → ("filename", "added"), "M filename" → ("filename", "modified"), etc.
    RETURNS: list of (path, change_type) tuples
    RAISES: RuntimeError if git command fails

  get_queue_item(queue_id: str, queue_path: Path = Path("queue/queue.csv")) -> dict[str, str] | None:
    PURPOSE: Read the queue row for the given queue ID.
    STEPS:
      1. Open queue.csv with csv.DictReader
      2. Find row where id == queue_id
      3. Return row as dict
    RETURNS: Row dict or None if not found

  generate_template(queue_id: str | None, base_ref: str) -> str:
    PURPOSE: Generate the pre-filled Markdown handoff template.
    STEPS:
      1. Get changed files list
      2. Get queue item (if queue_id provided)
      3. Build Markdown template with filled sections:
         - Header with timestamp
         - Files changed table (auto-filled from git)
         - Queue item summary (auto-filled if queue_id provided)
         - Acceptance criteria section (filled with criteria from queue summary)
         - Commands run section (placeholder for agent to fill)
         - Risks section (placeholder)
         - Follow-ups section (placeholder)
         - PR link placeholder
    RETURNS: Complete Markdown template string

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --queue-id (optional), --base-ref (default HEAD~1), --output (stdout or file)
      2. Call generate_template()
      3. Write to output destination
    RAISES: SystemExit 1 on error

DESIGN DECISIONS:
- base_ref defaults to HEAD~1 (last commit); agent can pass a branch name for full branch diff
- Queue item is optional — works without it for non-queue work
- Output goes to stdout by default so agent can copy-paste into PR description
- Acceptance criteria are extracted from queue summary using heuristic pattern matching
"""
