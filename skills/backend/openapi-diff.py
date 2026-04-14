# skills/backend/openapi-diff.py
"""

PURPOSE:
Compares current FastAPI OpenAPI spec against a stored baseline to detect
breaking API changes. Used before releases and in CI to prevent accidental
breaking changes from being deployed. Classifies changes as breaking vs non-breaking
per OpenAPI compatibility rules.

DEPENDS ON:
- json (stdlib) — parse OpenAPI JSON
- pathlib (stdlib) — file paths
- subprocess (stdlib) — import FastAPI app and get OpenAPI spec
- argparse (stdlib) — CLI
- sys (stdlib) — exit codes

DEPENDED ON BY:
- docs/api/openapi-baseline.json — the baseline this compares against
- skills/backend/api-versioning.md — references as machinery for release checks

CLASSES:

  ApiChange:
    PURPOSE: Represents a single detected API change.
    FIELDS:
      - path: str — API path affected (e.g., "/api/v1/invoices")
      - method: str — HTTP method
      - change_type: str — "endpoint_removed", "param_required", "response_schema", etc.
      - is_breaking: bool — True if this change would break existing clients
      - description: str — human-readable description of the change

FUNCTIONS:

  get_current_openapi(app_module: str = "apps.api.src.main:app") -> dict:
    PURPOSE: Import FastAPI app and return its OpenAPI schema dict.
    STEPS:
      1. subprocess to run Python with FastAPI app import
      2. Capture app.openapi() output as JSON
    RETURNS: OpenAPI schema dict
    RAISES: ImportError if app cannot be imported

  load_baseline(baseline_path: Path = Path("docs/api/openapi-baseline.json")) -> dict:
    PURPOSE: Load the stored OpenAPI baseline from disk.
    RETURNS: OpenAPI schema dict
    RAISES: FileNotFoundError if no baseline exists

  compare_schemas(baseline: dict, current: dict) -> list[ApiChange]:
    PURPOSE: Compare two OpenAPI schemas and classify all changes.
    STEPS:
      1. Compare paths: find added, removed, changed endpoints
      2. For removed endpoints: create BREAKING change
      3. For changed endpoints: compare parameters, request body, response schemas
      4. New required parameter → BREAKING
      5. Changed response schema (field removed/type changed) → BREAKING
      6. New optional parameter → NON-BREAKING
      7. New endpoint → NON-BREAKING
    RETURNS: list[ApiChange]

  update_baseline(current_schema: dict, baseline_path: Path) -> None:
    PURPOSE: Write current OpenAPI schema to baseline file.
    STEPS:
      1. Serialize with stable sort (ensure_ascii=False, sort_keys=True, indent=2)
      2. Write to baseline_path
    NOTES: Run after confirming current schema is intentional.

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --mode (check|update), --app-module, --baseline-path
      2. In check mode: compare current vs baseline, report changes, exit 1 if BREAKING
      3. In update mode: write current as new baseline

CONSTANTS:
  - BREAKING_CHANGE_TYPES: set[str] — change types classified as breaking

DESIGN DECISIONS:
- Stable JSON serialization (sort_keys=True) ensures baseline is diffable in git
- Breaking change detection is conservative — flags anything that could break clients
- Update mode (not run automatically) requires human decision to update baseline
"""
