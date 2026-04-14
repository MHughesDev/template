# skills/agent-ops/repo-self-audit.py
"""

PURPOSE:
Automated repository spec-compliance audit. Checks that the repository meets
the requirements in spec/spec.md: required files exist (§26), skills have all
required sections (§6.2), prompts have front matter (§7.2), procedures have
required fields (§8.3), queue schema is valid, Make targets are documented (§10.2),
and all non-JSON files begin with a file title comment (§1.7).
Produces a structured Markdown audit report with BLOCKING/WARNING findings.
Invoked by: scripts/audit-self.sh → make audit:self.

DEPENDS ON:
- pathlib (stdlib) — file discovery
- re (stdlib) — pattern matching for section headings
- csv (stdlib) — queue schema validation
- subprocess (stdlib) — run make -qp to inspect Makefile targets
- argparse (stdlib) — CLI argument parsing
- sys (stdlib) — exit codes

DEPENDED ON BY:
- scripts/audit-self.sh — invokes this as main audit engine
- .cursor/commands/audit.md — documents this as audit machinery

CLASSES:

  AuditFinding:
    PURPOSE: Represents a single audit finding.
    FIELDS:
      - severity: Literal["BLOCKING", "WARNING"] — finding severity
      - check: str — which audit check found this (e.g., "inventory", "skill-format")
      - path: str — file path related to the finding
      - message: str — what is wrong and how to fix it
      - spec_reference: str — which spec section this relates to (e.g., "§26.4 item 39")
    NOTES: Pydantic frozen model for immutability in report generation.

  AuditReport:
    PURPOSE: Collection of all findings from an audit run.
    FIELDS:
      - timestamp: datetime — when the audit ran
      - findings: list[AuditFinding] — all findings
      - checks_run: list[str] — which checks were performed
    METHODS:
      - blocking_count() -> int — count BLOCKING findings
      - warning_count() -> int — count WARNING findings
      - passed() -> bool — True if no BLOCKING findings
      - to_markdown() -> str — format as Markdown report
      - to_json() -> str — format as JSON for machine consumption

FUNCTIONS:

  check_file_inventory(repo_root: Path) -> list[AuditFinding]:
    PURPOSE: Check that all §26 required files exist on disk.
    STEPS:
      1. Load required file list from a hardcoded set matching spec §26 (or from a manifest file)
      2. For each required file: check Path(repo_root / path).exists()
      3. For missing files: create BLOCKING finding with spec reference
    RETURNS: list[AuditFinding] for missing required files
    RAISES: No exceptions — captures errors as findings

  check_title_comments(repo_root: Path) -> list[AuditFinding]:
    PURPOSE: Verify all non-JSON files begin with a file title comment (§1.7).
    STEPS:
      1. Walk repo_root recursively, skip: .git, .venv, node_modules, __pycache__
      2. For each file: read first line
      3. Apply per-extension check:
         - .py: first line must start with "# " (comment)
         - .md: first line must be "# " (H1) or "<!-- "
         - .yml/.yaml: first line must start with "# "
         - .sh: second line (after shebang) must start with "# "
         - .csv: first line must start with "# "
         - .bat: first line must start with "REM "
         - JSON: skip (waived)
      4. If check fails: WARNING finding
    RETURNS: list[AuditFinding]

  check_skill_format(repo_root: Path) -> list[AuditFinding]:
    PURPOSE: Verify all skill .md files have §6.2 required sections.
    STEPS:
      1. Find all *.md files under skills/ (excluding README.md files)
      2. For each skill file: read content
      3. Check for presence of each required section heading:
         "## Purpose", "## When to Invoke", "## Prerequisites", "## Relevant",
         "## Step-by-Step Method", "## Command Examples", "## Validation Checklist",
         "## Common Failure Modes", "## Handoff Expectations",
         "## Related Procedures", "## Related Prompts", "## Related Rules"
      4. Missing sections → WARNING finding per section
    RETURNS: list[AuditFinding]

  check_prompt_metadata(repo_root: Path) -> list[AuditFinding]:
    PURPOSE: Verify all prompt .md files have §7.2 required YAML front matter fields.
    STEPS:
      1. Find all *.md files under prompts/ (excluding README.md)
      2. For each prompt: extract YAML front matter (between --- delimiters)
      3. Check for all required fields: purpose, when_to_use, required_inputs, expected_outputs,
         validation_expectations, constraints, linked_commands, linked_procedures, linked_skills
      4. Missing fields → WARNING finding per field
    RETURNS: list[AuditFinding]

  check_procedure_structure(repo_root: Path) -> list[AuditFinding]:
    PURPOSE: Verify all procedure .md files have §8.3 required sections.
    STEPS:
      1. Find all *.md files under docs/procedures/ (excluding README.md)
      2. For each procedure: check for sections:
         "## Purpose" or "Purpose", "## Prerequisites", "## Steps" or ordered steps,
         "## Validation", "## Rollback" or "## Failure Handling", "## Handoff"
      3. Missing sections → WARNING finding
    RETURNS: list[AuditFinding]

  check_queue_schema(repo_root: Path) -> list[AuditFinding]:
    PURPOSE: Verify queue.csv and queuearchive.csv have correct header schemas.
    STEPS:
      1. Read queue.csv first row (header)
      2. Compare against required columns: id, batch, phase, category, summary, dependencies, notes, created_date
      3. Read queuearchive.csv first row
      4. Compare against required columns (same + status, completed_date)
      5. Schema mismatch → BLOCKING finding
    RETURNS: list[AuditFinding]

  check_make_targets(repo_root: Path) -> list[AuditFinding]:
    PURPOSE: Verify all §10.2 required Make targets are present in Makefile.
    STEPS:
      1. Load required targets list from §10.2 (hardcoded)
      2. Read Makefile and parse target names (lines matching "^<name>:" pattern)
      3. For missing targets: WARNING finding
    RETURNS: list[AuditFinding]

  run_audit(repo_root: Path, checks: list[str] | None = None) -> AuditReport:
    PURPOSE: Run all (or specified) audit checks and return report.
    STEPS:
      1. Determine which checks to run (all if checks is None)
      2. Run each check function, collect findings
      3. Build AuditReport with all findings
    RETURNS: AuditReport

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --check (specific check or "all"), --format (markdown|json), --repo-root
      2. Run audit
      3. Print formatted report
      4. Exit 0 if passed (no BLOCKING), 1 if has BLOCKING findings

CONSTANTS:
  - REQUIRED_SKILL_SECTIONS: tuple[str, ...] — the §6.2 headings
  - REQUIRED_PROMPT_FIELDS: tuple[str, ...] — the §7.2 front matter keys
  - REQUIRED_MAKE_TARGETS: tuple[str, ...] — the §10.2 target names
  - QUEUE_COLUMNS: tuple[str, ...] — the queue CSV column names
  - SKIP_DIRS: frozenset[str] = {".git", ".venv", "node_modules", "__pycache__", "htmlcov"}

DESIGN DECISIONS:
- Each check is independent and can run in isolation (--check flag)
- JSON format allows CI to parse and upload as artifact
- Exit code 1 on BLOCKING = CI fails if audit fails
- Required file list is hardcoded (to avoid circular reference to spec) and version-pinned
"""
