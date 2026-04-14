# skills/repo-governance/adr-index-generator.py
"""

PURPOSE:
Generates the ADR index file (docs/adr/README.md) from ADR files in docs/adr/.
Parses the title, status, date, and context from each ADR file and produces
a formatted index table sorted by ADR number. Invoked when a new ADR is added.

DEPENDS ON:
- pathlib (stdlib) — file discovery
- re (stdlib) — parsing ADR metadata from Markdown
- argparse (stdlib) — CLI

DEPENDED ON BY:
- skills/repo-governance/writing-adrs.md — references as machinery
- scripts/docs-generate.sh — may include ADR index generation

FUNCTIONS:

  parse_adr_metadata(adr_path: Path) -> dict[str, str]:
    PURPOSE: Extract ADR metadata from a single ADR file.
    STEPS:
      1. Read file content
      2. Extract title from first H1 heading (# ADR-NNN: Title)
      3. Extract number from filename (ADR-001-name.md → "001")
      4. Extract status from "**Status:** Accepted/Proposed/Deprecated/Superseded" line
      5. Extract date from "**Date:** YYYY-MM-DD" line
      6. Extract one-line context summary from Context section (first sentence)
    RETURNS: dict with keys: number, title, status, date, context_summary, path

  generate_index(adrs_dir: Path) -> str:
    PURPOSE: Generate the complete docs/adr/README.md index content.
    STEPS:
      1. Find all *.md files in adrs_dir, excluding README.md and template.md
      2. Parse metadata from each ADR
      3. Sort by ADR number
      4. Generate Markdown table: Number | Title | Status | Date | Summary
      5. Prepend header with explanation of ADR process
    RETURNS: Complete Markdown content for docs/adr/README.md

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --adrs-dir, --output (default stdout or docs/adr/README.md)
      2. Run generate_index()
      3. Write to output

DESIGN DECISIONS:
- Overwrites docs/adr/README.md completely (content is fully generated)
- Skips README.md and template.md in docs/adr/ (they are not ADR files)
- Status values: Proposed, Accepted, Deprecated, Superseded (standard ADR states)
- Sorted by ADR number for stable, predictable output
"""
