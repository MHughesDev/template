# skills/init/queue-seeder.py
"""
BLUEPRINT: skills/init/queue-seeder.py

PURPOSE:
Extracts queue items from idea.md §12 and §15, generates properly formatted
queue.csv rows with sequential IDs, batch assignments from phases, and summaries
that meet the minimum quality bar (≥100 chars). Validates output with queue schema.
Invoked by: scripts/idea-to-queue.sh → make idea:queue

DEPENDS ON:
- pathlib (stdlib) — file reading/writing
- csv (stdlib) — CSV generation
- re (stdlib) — Markdown table parsing
- argparse (stdlib) — CLI
- datetime (stdlib) — created_date generation

DEPENDED ON BY:
- scripts/idea-to-queue.sh → make idea:queue
- skills/init/queue-seeder.md — references as machinery

CLASSES:

  QueueSeedItem:
    PURPOSE: A queue item extracted from idea.md before CSV formatting.
    FIELDS:
      - priority: int — original priority from idea.md §12
      - category: str — category from idea.md §12
      - raw_summary: str — original brief summary from idea.md
      - expanded_summary: str — elaborated summary meeting quality bar
      - phase: str — from idea.md §15 (batch assignment)
      - batch: str — derived from phase

FUNCTIONS:

  parse_queue_items_from_idea(idea_content: str) -> list[QueueSeedItem]:
    PURPOSE: Parse idea.md §12 work items and §15 phases into QueueSeedItems.
    STEPS:
      1. Find ## 12. Initial queue items section
      2. Parse Markdown table rows (| Priority | Category | Summary |)
      3. Find ## 15. Timeline and phasing section
      4. Parse Markdown table rows (| Phase | Milestone | Scope |)
      5. Map priority → phase → batch (Phase 1 → batch "init", Phase 2 → batch "beta", etc.)
    RETURNS: list[QueueSeedItem] sorted by priority

  expand_summary(
    raw: str,
    category: str,
    context_from_idea: str
  ) -> str:
    PURPOSE: Expand a brief summary into one that meets the ≥100 char quality bar.
    STEPS:
      1. Start with raw summary
      2. If len < 100: append generic acceptance criteria template for the category
      3. Template: "Goal: <raw>. Acceptance criteria: implementation complete, tests passing, docs updated. Definition of done: PR merged, queue archived."
    RETURNS: Expanded summary string ≥100 chars

  generate_queue_csv_rows(
    items: list[QueueSeedItem],
    id_prefix: str = "Q"
  ) -> list[dict[str, str]]:
    PURPOSE: Convert QueueSeedItems to queue.csv row dicts.
    STEPS:
      1. Assign sequential IDs: Q-001, Q-002, etc.
      2. Set created_date to today (ISO format)
      3. Leave notes and dependencies empty (to be filled by agents)
      4. Include expanded_summary in summary column
    RETURNS: list of row dicts matching queue.csv column schema

  write_queue_csv(rows: list[dict], queue_path: Path) -> None:
    PURPOSE: Write queue rows to queue.csv (append or replace).
    STEPS:
      1. If queue.csv has data rows: raise FileExistsError (do not overwrite existing work)
      2. Write header row
      3. Write all item rows
    RAISES: FileExistsError if queue.csv already has data (initialization should only run once)

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --idea-path, --queue-path, --id-prefix, --dry-run
      2. Read idea.md
      3. Parse queue items
      4. Generate CSV rows
      5. In dry-run: print rows to stdout
      6. Otherwise: write to queue.csv
      7. Run validation: check each row has summary ≥100 chars

DESIGN DECISIONS:
- Refuses to overwrite existing queue data (initialization is a one-time operation)
- ID prefix is configurable: default "Q" (e.g., Q-001), or project-specific
- Expands summaries rather than rejecting short ones — initialization should succeed
- Phase → batch mapping: Phase 1 → batch "1-mvp", Phase 2 → batch "2-beta", Phase 3 → batch "3-ga"
"""
