# skills/testing/coverage-ratchet.py
"""

PURPOSE:
Reads current test coverage percentage, compares against the floor defined in
docs/quality/coverage-policy.md, updates the floor if coverage improved, and
fails with a gap report if coverage dropped below the floor. Implements the
"ratchet" mechanism where coverage only goes up, never down.
Invoked by: make test (as post-test hook) or manually.

DEPENDS ON:
- json (stdlib) — parse coverage.json report
- pathlib (stdlib) — file paths
- re (stdlib) — parse coverage floor from policy doc
- argparse (stdlib) — CLI
- sys (stdlib) — exit codes

DEPENDED ON BY:
- scripts/test.sh — called after pytest to enforce ratchet
- docs/quality/coverage-policy.md — contains the floor this updates

FUNCTIONS:

  read_coverage(coverage_json_path: Path = Path(".coverage.json")) -> float:
    PURPOSE: Read total coverage percentage from pytest-cov JSON report.
    STEPS:
      1. Load .coverage.json (created by pytest --cov-report json)
      2. Extract totals.percent_covered
    RETURNS: float — coverage percentage (0-100)
    RAISES: FileNotFoundError if coverage report not found

  read_floor(policy_path: Path = Path("docs/quality/coverage-policy.md")) -> float:
    PURPOSE: Parse the current coverage floor from the policy document.
    STEPS:
      1. Read policy doc content
      2. Find pattern: "Current coverage floor: XX%" or similar
      3. Parse percentage
    RETURNS: float — current floor percentage
    RAISES: ValueError if floor not found in policy doc

  update_floor(policy_path: Path, new_floor: float) -> None:
    PURPOSE: Update the coverage floor in the policy document.
    STEPS:
      1. Read policy doc
      2. Replace floor value with new_floor (rounded down to 1 decimal)
      3. Write updated doc
    NOTES: Floor is rounded DOWN to avoid fluctuation on marginal improvements

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --coverage-json, --policy-path, --dry-run
      2. Read current coverage
      3. Read current floor
      4. If coverage > floor: update floor, print "Coverage improved: X% → Y%"
      5. If coverage == floor: print "Coverage maintained at X%"
      6. If coverage < floor: print gap report, exit 1

DESIGN DECISIONS:
- Floor is stored in human-readable policy doc (not a config file) for transparency
- Floor only increases (hence "ratchet") — never decreases automatically
- Dry-run mode reports without updating the file (useful in CI for reporting only)
- Rounding: new floor = floor(current_coverage * 10) / 10 (round down to tenths)
- Exit 1 when coverage drops → CI fails → protects the floor
"""
