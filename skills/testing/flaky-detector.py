# skills/testing/flaky-detector.py
"""

PURPOSE:
Detects potentially flaky tests by running the test suite multiple times
and identifying tests that sometimes pass and sometimes fail. Produces a
ranked flaky test report for the flaky-test-triage.md skill to act on.
Optional per spec — useful for CI hygiene.

DEPENDS ON:
- subprocess (stdlib) — run pytest multiple times
- json (stdlib) — parse pytest JSON output
- pathlib (stdlib) — file paths
- argparse (stdlib) — CLI

DEPENDED ON BY:
- skills/testing/flaky-test-triage.md — references as machinery

FUNCTIONS:

  run_pytest_once(
    test_path: str = "apps/api/tests",
    extra_args: list[str] | None = None
  ) -> dict[str, bool]:
    PURPOSE: Run pytest once and return test result mapping.
    STEPS:
      1. subprocess.run(["pytest", "--tb=no", "-q", "--json-report", test_path])
      2. Parse JSON report
      3. Return dict: test_node_id → passed (True/False)
    RETURNS: dict[str, bool]

  detect_flaky_tests(
    test_path: str = "apps/api/tests",
    runs: int = 5,
  ) -> dict[str, dict]:
    PURPOSE: Run test suite N times and identify tests with inconsistent results.
    STEPS:
      1. Run pytest N times via run_pytest_once()
      2. For each test: collect results across all runs
      3. Identify tests with at least one pass AND one fail (inconsistent)
      4. Calculate pass rate: passes/total_runs
    RETURNS: dict[test_id, {pass_rate, runs, pass_count, fail_count}]

  format_report(flaky_tests: dict[str, dict]) -> str:
    PURPOSE: Format flaky test findings as Markdown report.
    STEPS:
      1. Sort by pass_rate (lowest first = most flaky)
      2. Format table: test_id | pass_rate | pass_count | fail_count
    RETURNS: Markdown report string

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --runs (default 5), --test-path, --format
      2. Run detection
      3. Print report
      4. Exit 0 (flaky test detection is informational, not blocking)

DESIGN DECISIONS:
- Exit 0 even with findings: flaky detection is informational (triage required next)
- Default 5 runs: enough to detect most flakiness without excessive CI time
- Requires pytest-json-report plugin: `pip install pytest-json-report`
- Results stored in memory only — no test ordering or retrying
"""
