# skills/repo-governance/rule-linter.py
"""
BLUEPRINT: skills/repo-governance/rule-linter.py

PURPOSE:
Lints .cursor/rules/*.md files for correct structure: frontmatter presence,
valid glob patterns, description field, and potential contradictions between
rule files. Used by make rules:check and skills/repo-governance/authoring-cursor-rules.md.

DEPENDS ON:
- pathlib (stdlib) — file discovery
- re (stdlib) — pattern matching for YAML frontmatter and glob validation
- sys (stdlib) — exit codes
- argparse (stdlib) — CLI

DEPENDED ON BY:
- scripts/rules-check.sh → make rules:check
- skills/repo-governance/authoring-cursor-rules.md — references as machinery

CLASSES:

  RuleLintError:
    PURPOSE: Represents a single rule file linting finding.
    FIELDS:
      - file: str — path to the rule file
      - severity: Literal["ERROR", "WARNING"] — ERROR blocks, WARNING informs
      - message: str — what is wrong
      - suggestion: str — how to fix it

FUNCTIONS:

  parse_frontmatter(content: str) -> dict[str, object] | None:
    PURPOSE: Extract and parse YAML frontmatter from rule file content.
    STEPS:
      1. Check if content starts with "---\n"
      2. Find closing "---" delimiter
      3. Parse YAML between delimiters (using simple key: value parsing, no PyYAML dependency)
      4. Return parsed dict or None if no frontmatter
    RETURNS: dict with parsed frontmatter keys or None

  lint_rule_file(path: Path) -> list[RuleLintError]:
    PURPOSE: Lint a single rule file and return all findings.
    STEPS:
      1. Read file content
      2. Check frontmatter exists: ERROR if missing
      3. Check alwaysApply or globs is present: ERROR if both absent
      4. If globs: validate each glob pattern is syntactically valid (no empty strings, no spaces)
      5. Check description field is present: WARNING if missing
      6. Check file has rule content (not just frontmatter): WARNING if body is empty
      7. Check rules use imperative keywords (NEVER, MUST, ALWAYS, DO NOT): WARNING if not found
    RETURNS: list[RuleLintError]

  detect_contradictions(rule_files: list[Path]) -> list[RuleLintError]:
    PURPOSE: Detect potential contradictions between rule files.
    STEPS:
      1. Extract all imperative rules from each file (lines containing NEVER/MUST/ALWAYS)
      2. Compare pairs for semantic opposites (simple heuristic: same noun phrase with opposing verb)
      3. Flag suspicious pairs as WARNING
    RETURNS: list[RuleLintError] (WARNING severity only — full contradiction analysis requires human review)
    NOTES: This is heuristic, not exhaustive. Human must review flagged pairs.

  lint_all(rules_dir: Path) -> list[RuleLintError]:
    PURPOSE: Lint all rule files in the rules directory.
    STEPS:
      1. Find all *.md files in rules_dir
      2. Lint each file individually
      3. Run contradiction detection across all files
      4. Return combined list of findings
    RETURNS: list[RuleLintError]

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --rules-dir (default .cursor/rules/), --format (text|json)
      2. Run lint_all()
      3. Print formatted findings
      4. Exit 0 if no ERRORs, 1 if any ERRORs

DESIGN DECISIONS:
- No PyYAML dependency: frontmatter parsed with simple regex to avoid extra install
- contradiction detection is heuristic: marks suspicious pairs for human review
- Exit code 1 only on ERROR (not WARNING) to allow gradual improvement
"""
