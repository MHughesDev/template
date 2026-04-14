# skills/init/idea-validator.py
"""

PURPOSE:
Validates idea.md structure and content completeness. Checks every required
section (all 17 per spec §27.2) has real content beyond HTML comment placeholders.
Validates internal consistency: archetype-profile alignment, entity-context coverage.
Produces a per-section validation report. Exit non-zero if any required section fails.
Invoked by: scripts/validate-idea.sh → make idea:validate

DEPENDS ON:
- pathlib (stdlib) — file reading
- re (stdlib) — section parsing and placeholder detection
- argparse (stdlib) — CLI
- sys (stdlib) — exit codes
- dataclasses — ValidationResult

DEPENDED ON BY:
- scripts/validate-idea.sh → make idea:validate
- skills/init/idea-validator.md — references as machinery

CLASSES:

  SectionResult:
    PURPOSE: Validation result for a single idea.md section.
    FIELDS:
      - section_number: int — section number (1-17)
      - section_title: str — section heading text
      - passed: bool — True if section has sufficient real content
      - issues: list[str] — specific problems found
      - content_length: int — character count of non-comment content

  ValidationReport:
    PURPOSE: Complete validation report for idea.md.
    FIELDS:
      - sections: list[SectionResult]
      - consistency_issues: list[str] — cross-section consistency problems
      - passed: bool — True if all required sections pass
    METHODS:
      - to_text() -> str — format as human-readable text report
      - to_json() -> str — format as JSON for machine consumption

FUNCTIONS:

  parse_sections(idea_content: str) -> dict[int, str]:
    PURPOSE: Parse idea.md into sections by H2 heading number.
    STEPS:
      1. Split content on `## ` headings
      2. Map section number (from content) to section text
      3. Return dict[section_number, section_content]
    RETURNS: dict mapping section number to section content

  has_real_content(section_content: str, min_length: int = 50) -> bool:
    PURPOSE: Check if a section has real content beyond HTML comment placeholders.
    STEPS:
      1. Remove all HTML comment blocks (<!-- ... -->)
      2. Remove all markdown table separators (| --- |)
      3. Check remaining content length > min_length
    RETURNS: bool

  validate_section(number: int, title: str, content: str) -> SectionResult:
    PURPOSE: Validate a single idea.md section.
    STEPS:
      1. Check has_real_content()
      2. For specific sections: additional checks
         - §1 (Identity): project name and slug filled
         - §3 (Archetype): exactly one archetype selected [x]
         - §4.2 (Bounded contexts): at least one context row with content
         - §5 (Profiles): all profile rows have yes/no answer
         - §12 (Queue items): at least one row with category and summary
    RETURNS: SectionResult

  check_consistency(sections: dict[int, str]) -> list[str]:
    PURPOSE: Check cross-section consistency.
    STEPS:
      1. Extract archetype from §3
      2. Extract enabled profiles from §5
      3. Verify archetype-profile alignment (SaaS should have multi-tenancy)
      4. Extract entities from §4.1
      5. Extract contexts from §4.2
      6. Verify each entity appears in at least one context
    RETURNS: list[str] of consistency issues

  validate_idea_md(idea_path: Path) -> ValidationReport:
    PURPOSE: Run complete validation of idea.md.
    STEPS:
      1. Read idea.md content
      2. Parse sections
      3. Validate each section
      4. Run consistency checks
      5. Build ValidationReport
    RETURNS: ValidationReport

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: idea_path (default idea.md), --format (text|json)
      2. Run validate_idea_md()
      3. Print report
      4. Exit 0 if passed, 1 if any failures

CONSTANTS:
  - REQUIRED_SECTIONS: tuple[int, ...] = tuple(range(1, 18)) — sections 1-17 all required
  - MIN_CONTENT_LENGTH: dict[int, int] — per-section minimum content length

DESIGN DECISIONS:
- HTML comment removal (not just detection) to measure actual content
- Exit 1 on any failure: initialization should not proceed with incomplete idea.md
- Consistency checks are warnings (not blocking) — recommendations, not hard requirements
- min_length varies by section: §1 needs 30 chars, §2 needs 100 chars, etc.
"""
