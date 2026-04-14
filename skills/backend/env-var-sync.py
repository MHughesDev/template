# skills/backend/env-var-sync.py
"""

PURPOSE:
Synchronizes .env.example with actual env var usage in the codebase.
Detects: (1) vars used in code but missing from .env.example, and
(2) vars documented in .env.example but not used anywhere in code.
Part of the documentation generation pipeline (§9.4) for docs/development/environment-vars.md.

DEPENDS ON:
- ast (stdlib) — parse Python files for BaseSettings field names
- pathlib (stdlib) — file discovery
- re (stdlib) — pattern matching for env var references
- argparse (stdlib) — CLI

DEPENDED ON BY:
- skills/repo-governance/docs-generator.py — called for env-vars doc target
- scripts/audit-self.sh — may call for env var drift check

FUNCTIONS:

  scan_settings_class(config_path: Path) -> dict[str, str]:
    PURPOSE: Parse apps/api/src/config.py and extract all Settings field names.
    STEPS:
      1. ast.parse() on config_path
      2. Find Settings class (subclass of BaseSettings)
      3. For each field: extract name and alias (env var name if different from field name)
    RETURNS: dict[field_name, env_var_name] mapping

  scan_env_example(env_example_path: Path) -> dict[str, str]:
    PURPOSE: Parse .env.example and extract all documented var names.
    STEPS:
      1. Read file line by line
      2. Skip comment lines (starting with #)
      3. Parse VAR_NAME=value pairs
      4. Also extract commented-out vars (# VAR_NAME=value)
    RETURNS: dict[var_name, default_value] — all vars in .env.example

  find_missing_from_example(
    settings_vars: dict[str, str],
    example_vars: dict[str, str]
  ) -> list[str]:
    PURPOSE: Find vars defined in Settings but not in .env.example.
    RETURNS: list[str] of missing var names

  find_orphaned_in_example(
    settings_vars: dict[str, str],
    example_vars: dict[str, str]
  ) -> list[str]:
    PURPOSE: Find vars in .env.example with no corresponding Settings field.
    NOTES: These may be intentional (profile vars not yet in Settings) — flag as WARNING
    RETURNS: list[str] of potentially orphaned var names

  generate_env_docs(
    settings_vars: dict[str, str],
    example_vars: dict[str, str],
    config_path: Path
  ) -> str:
    PURPOSE: Generate docs/development/environment-vars.md content.
    STEPS:
      1. For each var: combine Settings field info with .env.example comment
      2. Format as Markdown table: Variable | Description | Type | Default | Required | Profile
    RETURNS: Markdown table string

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --config-path, --env-example-path, --mode (check|report|generate-docs)
      2. Run scans and comparisons
      3. Report findings
      4. Exit 1 if missing vars found (BLOCKING) in check mode

DESIGN DECISIONS:
- Missing vars (in code but not in .env.example) are BLOCKING — agents can't know what to set
- Orphaned vars (in .env.example but not in code) are WARNING — may be profile-specific
- Uses ast not import to avoid startup side effects
"""
