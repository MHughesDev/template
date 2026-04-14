# skills/security/secret-scanner.py
"""

PURPOSE:
Scans the codebase for potential secrets: high-entropy strings, known secret
patterns (API keys, JWT tokens, passwords with real values), and env vars
with default values that look like real secrets. Complements detect-secrets
pre-commit hook with a standalone CLI for CI and on-demand scanning.

DEPENDS ON:
- pathlib (stdlib) — file discovery
- re (stdlib) — regex pattern matching
- math (stdlib) — Shannon entropy calculation
- argparse (stdlib) — CLI
- sys (stdlib) — exit codes

DEPENDED ON BY:
- scripts/security-scan.sh → make security:scan
- skills/security/secret-handling.md — references as machinery

CLASSES:

  SecretFinding:
    PURPOSE: Represents a potential secret found in the codebase.
    FIELDS:
      - file_path: str — path to the file
      - line_number: int — line where found
      - pattern_name: str — which pattern matched (e.g., "AWS_ACCESS_KEY", "JWT_TOKEN")
      - severity: Literal["HIGH", "MEDIUM", "LOW"]
      - context: str — surrounding line content (with potential secret masked)
      - masked_value: str — the matched value with middle characters replaced by ***

FUNCTIONS:

  shannon_entropy(data: str) -> float:
    PURPOSE: Calculate Shannon entropy of a string to detect high-entropy (likely random) values.
    STEPS:
      1. Count character frequency
      2. Calculate entropy: -sum(p * log2(p) for each unique char)
    RETURNS: float — entropy value (>4.5 suggests high entropy / potential secret)

  scan_file(file_path: Path, patterns: list[tuple[str, str, str]]) -> list[SecretFinding]:
    PURPOSE: Scan a single file for secret patterns.
    STEPS:
      1. Read file content
      2. For each line: apply each regex pattern
      3. For matched values: calculate entropy
      4. If entropy > threshold: create HIGH finding
      5. For known patterns (API key formats): create finding regardless of entropy
    RETURNS: list[SecretFinding]

  scan_directory(
    scan_path: Path,
    patterns: list[tuple[str, str, str]],
    skip_paths: set[str]
  ) -> list[SecretFinding]:
    PURPOSE: Recursively scan all files in a directory.
    STEPS:
      1. Walk scan_path
      2. Skip: .git, .venv, node_modules, __pycache__, *.pyc, binary files
      3. Skip .env.example (intentional CHANGEME placeholders)
      4. Call scan_file() for each eligible file
    RETURNS: list[SecretFinding] from all files

  format_report(findings: list[SecretFinding]) -> str:
    PURPOSE: Format findings as human-readable report.
    RETURNS: Markdown report with findings grouped by severity

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --scan-path, --format (text|json), --baseline (path to .secrets.baseline for exclusions)
      2. Load exclusions from baseline if provided
      3. Run scan
      4. Filter excluded findings
      5. Print report
      6. Exit 0 if no HIGH findings, 1 if any HIGH findings

CONSTANTS:
  - SECRET_PATTERNS: list[tuple[str, str, str]] — (pattern_name, regex, severity)
    Includes: AWS_ACCESS_KEY, AWS_SECRET_KEY, STRIPE_API_KEY, OPENAI_API_KEY,
    GITHUB_TOKEN, JWT_TOKEN (header.payload.signature pattern), private_key_header,
    POSTGRES_PASSWORD assignment with non-CHANGEME value
  - HIGH_ENTROPY_THRESHOLD: float = 4.5 — strings above this entropy are flagged
  - MIN_SECRET_LENGTH: int = 16 — minimum length to flag as potential secret
  - SKIP_PATHS: set[str] — directories to never scan

DESIGN DECISIONS:
- .env.example is explicitly excluded (it contains intentional CHANGEME placeholders)
- High entropy threshold (4.5) is tuned to catch real secrets while minimizing false positives on hashes
- Masked values in reports prevent re-leakage through the report itself
- Baseline exclusion allows false positives to be acknowledged without being noisy
"""
