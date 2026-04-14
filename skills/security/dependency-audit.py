# skills/security/dependency-audit.py
"""

PURPOSE:
Audits Python dependencies for known vulnerabilities by wrapping pip-audit
(or safety) with structured output, severity classification, and cross-referencing
against the project's accepted-risk list (docs/security/accepted-risks.md).
Produces an actionable report distinguishing new CVEs from accepted ones.

DEPENDS ON:
- subprocess (stdlib) — run pip-audit
- json (stdlib) — parse pip-audit JSON output
- pathlib (stdlib) — file paths
- re (stdlib) — parse accepted-risks.md
- argparse (stdlib) — CLI

DEPENDED ON BY:
- scripts/security-scan.sh → make security:scan
- skills/security/dependency-review.md — references as machinery

FUNCTIONS:

  run_pip_audit() -> list[dict]:
    PURPOSE: Run pip-audit and return JSON output.
    STEPS:
      1. subprocess.run(["pip-audit", "--format=json", "--progress-spinner=off"])
      2. Parse JSON output
      3. Return list of vulnerability dicts
    RETURNS: list[dict] with vuln data
    RAISES: RuntimeError if pip-audit not installed or fails unexpectedly

  classify_severity(vuln: dict) -> Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
    PURPOSE: Classify vulnerability severity from pip-audit output.
    STEPS:
      1. Extract CVSS score if available
      2. Map to severity: CVSS >= 9.0 = CRITICAL, >= 7.0 = HIGH, >= 4.0 = MEDIUM, < 4.0 = LOW
      3. If no CVSS: use pip-audit's own severity field
    RETURNS: severity string

  load_accepted_risks(accepted_risks_path: Path) -> set[str]:
    PURPOSE: Parse docs/security/accepted-risks.md and extract accepted CVE IDs.
    STEPS:
      1. Read file
      2. Find CVE-YYYY-NNNN patterns
      3. Return set of accepted CVE IDs
    RETURNS: set[str]

  generate_report(vulnerabilities: list[dict], accepted: set[str]) -> str:
    PURPOSE: Generate actionable Markdown report.
    STEPS:
      1. Separate into: new CVEs (not in accepted), accepted CVEs
      2. For new CVEs: show package, version, CVE ID, severity, fix version, description
      3. For accepted: show brief listing
      4. Count by severity
    RETURNS: Markdown report string

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --accepted-risks-path, --format, --fail-on (severity threshold)
      2. Run audit
      3. Load accepted risks
      4. Generate report
      5. Exit 1 if any non-accepted CVEs above fail-on threshold

DESIGN DECISIONS:
- fail-on defaults to HIGH — CRITICAL and HIGH CVEs fail CI unless accepted
- MEDIUM and LOW are reported but don't fail by default (can be tightened)
- Accepted risks must be in docs/security/accepted-risks.md with review date
"""
