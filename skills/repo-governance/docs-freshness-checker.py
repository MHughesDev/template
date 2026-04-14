# skills/repo-governance/docs-freshness-checker.py
"""
BLUEPRINT: skills/repo-governance/docs-freshness-checker.py

PURPOSE:
Checks documentation freshness by comparing doc file modification timestamps
against the modification timestamps of related source code files. Flags
documentation that may be stale because its related code changed more recently.
Used by skills/repo-governance/maintaining-procedural-docs.md and as part of
scheduled documentation review cadence.

DEPENDS ON:
- pathlib (stdlib) — file discovery and stat()
- subprocess (stdlib) — git log for last modification timestamp per file
- re (stdlib) — pattern matching to find source references in docs
- argparse (stdlib) — CLI
- sys (stdlib) — exit codes

DEPENDED ON BY:
- skills/repo-governance/maintaining-procedural-docs.md — references as machinery
- docs/repo-governance/documentation-freshness.md — references for automated check

CLASSES:

  StalenessWarning:
    PURPOSE: Represents a potentially stale documentation file.
    FIELDS:
      - doc_path: str — path to the documentation file
      - related_sources: list[str] — source files that were modified after doc
      - doc_last_modified: str — ISO timestamp of doc's last git commit
      - source_last_modified: str — ISO timestamp of most recently changed related source
      - days_behind: int — how many days the doc is behind its sources

FUNCTIONS:

  get_git_mtime(path: Path, repo_root: Path) -> str | None:
    PURPOSE: Get the last git commit timestamp for a file.
    STEPS:
      1. subprocess.run(["git", "log", "-1", "--format=%cI", "--", str(path)])
      2. Parse ISO 8601 timestamp
    RETURNS: ISO timestamp string or None if file not in git

  find_related_sources(doc_path: Path, repo_root: Path) -> list[Path]:
    PURPOSE: Find source files related to a documentation file using heuristics.
    STEPS:
      1. Search doc content for paths matching apps/api/*, packages/*, scripts/*
      2. Match doc filename to likely source (e.g., docker.md → docker-compose.yml, Dockerfile)
      3. Match procedure filenames to their corresponding Make target script
    RETURNS: list[Path] of related source files

  check_staleness(doc_path: Path, repo_root: Path, threshold_days: int = 30) -> StalenessWarning | None:
    PURPOSE: Check if a doc is stale relative to its related sources.
    STEPS:
      1. Get doc's last git mtime
      2. Find related source files
      3. Get each source's last git mtime
      4. If any source newer than doc by > threshold_days: return StalenessWarning
    RETURNS: StalenessWarning or None if doc is fresh

  check_all_docs(docs_dir: Path, repo_root: Path, threshold_days: int = 30) -> list[StalenessWarning]:
    PURPOSE: Check all docs in docs_dir for staleness.
    STEPS:
      1. Walk docs_dir recursively
      2. For each .md file: run check_staleness()
      3. Collect all StalenessWarning results
    RETURNS: list[StalenessWarning] sorted by days_behind descending

  format_report(warnings: list[StalenessWarning]) -> str:
    PURPOSE: Format staleness warnings as Markdown report.
    RETURNS: Markdown string

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --docs-dir, --threshold-days, --format
      2. Run check_all_docs()
      3. Print report
      4. Exit 0 if no warnings, 1 if any warnings (for CI use)

DESIGN DECISIONS:
- Uses git log timestamps rather than filesystem mtime for accuracy (git history is the truth)
- Heuristic source matching — not exhaustive; human judgment required for ambiguous cases
- threshold_days is configurable; default 30 is a reasonable "possibly stale" threshold
- Returns exit 1 with warnings so CI can optionally fail on stale docs
"""
