# skills/agent-ops/queue-triage.py
"""
BLUEPRINT: skills/agent-ops/queue-triage.py

PURPOSE:
Queue triage analyzer. Reads queue.csv and queuearchive.csv, validates schema,
checks dependency readiness, scores item quality, and outputs a prioritized
triage report. Used by the queue-triage skill to provide automated queue analysis.
Invoked by: make queue:analyze (indirectly), or directly as a script.

DEPENDS ON:
- csv (stdlib) — CSV parsing
- sys (stdlib) — exit codes
- pathlib (stdlib) — file path handling
- dataclasses — QueueItem, TriageResult data classes

DEPENDED ON BY:
- scripts/queue-analyze.sh — invokes this as part of queue:analyze
- skills/agent-ops/queue-intelligence.py — may import scoring logic

CLASSES:

  QueueItem:
    PURPOSE: Represents a single row from queue.csv with all columns.
    FIELDS:
      - id: str — unique item identifier
      - batch: str — batch identifier (optional)
      - phase: str — phase within batch (optional)
      - category: str — work category
      - summary: str — elaborative summary (the work contract)
      - dependencies: list[str] — parsed list of dependency IDs
      - notes: str — agent notes and blocker info
      - created_date: str — ISO date string
    METHODS:
      - from_csv_row(row: dict) -> QueueItem — parse from csv.DictReader row
      - is_valid_summary() -> bool — check summary length >= 100 chars
      - has_required_fields() -> bool — check all required fields present

  TriageResult:
    PURPOSE: Readiness assessment for one queue item.
    FIELDS:
      - item_id: str
      - is_ready: bool — True if all dependencies met and summary valid
      - blocked_by: list[str] — dependency IDs not yet done
      - score: int — quality score 0-100
      - issues: list[str] — problems found
    NOTES: Score affects display priority but does not reorder the CSV.

FUNCTIONS:

  load_queue(queue_path: Path) -> list[QueueItem]:
    PURPOSE: Load and parse queue.csv into QueueItem objects.
    STEPS:
      1. Open file with csv.DictReader
      2. Validate header row matches expected columns
      3. Parse each row into QueueItem (handle missing optional fields)
    RETURNS: list[QueueItem] in file order
    RAISES: FileNotFoundError if queue.csv does not exist; ValueError if schema wrong

  load_archive(archive_path: Path) -> set[str]:
    PURPOSE: Load queuearchive.csv and return set of done item IDs.
    STEPS:
      1. Open file with csv.DictReader
      2. For each row where status == "done": add id to set
    RETURNS: set[str] of completed item IDs
    RAISES: FileNotFoundError if archive does not exist

  check_dependencies(item: QueueItem, done_ids: set[str]) -> list[str]:
    PURPOSE: Return list of dependency IDs that are not yet done.
    STEPS:
      1. For each ID in item.dependencies: check if in done_ids
      2. Return IDs not in done_ids
    RETURNS: list[str] of unmet dependency IDs

  score_item(item: QueueItem) -> tuple[int, list[str]]:
    PURPOSE: Score item quality 0-100 and return list of issues.
    STEPS:
      1. Start at 100 points
      2. Deduct 30 if summary < 100 chars
      3. Deduct 20 if summary does not contain "acceptance criteria" or "definition of done"
      4. Deduct 10 if category is empty
      5. Deduct 10 if created_date is missing or invalid format
    RETURNS: (score, issues_list)

  triage_queue(queue_path: Path, archive_path: Path) -> list[TriageResult]:
    PURPOSE: Main triage function. Loads queue, checks all items, returns results.
    STEPS:
      1. Load queue items and done IDs from archive
      2. For each item: check dependencies, score quality
      3. Build TriageResult for each
    RETURNS: list[TriageResult] preserving queue order
    RAISES: Propagates FileNotFoundError from loaders

  format_report(results: list[TriageResult]) -> str:
    PURPOSE: Format triage results as human-readable Markdown report.
    STEPS:
      1. Group by: ready, blocked, quality-issues
      2. Format each group with item IDs and explanations
    RETURNS: Markdown string suitable for stdout or file output

  main() -> None:
    PURPOSE: CLI entry point. Parses args, runs triage, prints report.
    STEPS:
      1. Parse CLI args: --queue-path, --archive-path, --format (text|json)
      2. Run triage_queue()
      3. Print formatted report to stdout
      4. Exit 0 if any items are ready, 1 if all blocked, 2 if queue empty
    RAISES: SystemExit with appropriate code

CONSTANTS:
  - QUEUE_COLUMNS: tuple[str, ...] = ("id", "batch", "phase", "category", "summary", "dependencies", "notes", "created_date")
  - ARCHIVE_COLUMNS: tuple[str, ...] = QUEUE_COLUMNS + ("status", "completed_date")
  - MIN_SUMMARY_LENGTH: int = 100 — minimum summary length per spec §17.2
  - VALID_CATEGORIES_PATH: str = "docs/queue/queue-categories.md" — read at runtime

DESIGN DECISIONS:
- Uses stdlib csv only (no pandas) for minimal dependencies
- Reads VALID_CATEGORIES_PATH at runtime to stay in sync with docs
- Score is advisory: does not reorder CSV per spec §17.11.2
- Exit codes: 0=ready items exist, 1=all blocked, 2=empty queue
"""
