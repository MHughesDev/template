# skills/security/tenant-isolation-checker.py
"""

PURPOSE:
Static analysis tool for tenant isolation. Scans SQLAlchemy queries in the
codebase for missing tenant_id filters on tenant-scoped models. Checks that
all tenant-scoped models use TenantMixin. Verifies middleware is applied to
relevant routes. Produces an isolation compliance report.
Part of the security skill machinery per §17.11 and .cursor/rules/security.md.

DEPENDS ON:
- ast (stdlib) — parse Python files without importing them
- pathlib (stdlib) — file discovery
- re (stdlib) — pattern matching
- argparse (stdlib) — CLI

DEPENDED ON BY:
- skills/security/rbac-tenant-isolation.md — references as machinery
- scripts/security-scan.sh — may call for tenant isolation check

CLASSES:

  IsolationFinding:
    PURPOSE: Represents a potential tenant isolation violation.
    FIELDS:
      - severity: Literal["CRITICAL", "WARNING"]
      - file_path: str
      - line_number: int
      - description: str — what the violation is
      - recommendation: str — how to fix it

FUNCTIONS:

  find_tenant_scoped_models(src_path: Path) -> set[str]:
    PURPOSE: Find all SQLAlchemy models that use TenantMixin or have tenant_id column.
    STEPS:
      1. Walk src_path for models.py files
      2. Parse each with ast
      3. Find ClassDef nodes with TenantMixin in bases or tenant_id column definition
    RETURNS: set[str] of model class names

  scan_queries_for_tenant_filter(
    src_path: Path,
    tenant_scoped_models: set[str]
  ) -> list[IsolationFinding]:
    PURPOSE: Find SQLAlchemy queries on tenant-scoped models that lack tenant_id filter.
    STEPS:
      1. Walk src_path for .py files
      2. Parse each with ast
      3. Find select() and filter() patterns on tenant-scoped model names
      4. Check if the query chain includes .where(Model.tenant_id == ...) pattern
      5. Queries without tenant_id filter → CRITICAL finding
    RETURNS: list[IsolationFinding]
    NOTES: AST analysis is heuristic — may have false positives in complex query builders

  check_tenancy_middleware(main_path: Path = Path("apps/api/src/main.py")) -> list[IsolationFinding]:
    PURPOSE: Verify TenantContextMiddleware is registered in main.py.
    STEPS:
      1. Parse main.py
      2. Check for TenantContextMiddleware in app.add_middleware() calls
      3. If missing: CRITICAL finding
    RETURNS: list[IsolationFinding]

  check_models_use_tenant_mixin(src_path: Path) -> list[IsolationFinding]:
    PURPOSE: Find models with a tenant_id column but not inheriting TenantMixin.
    STEPS:
      1. Find all model classes with tenant_id column
      2. Check if they inherit TenantMixin
      3. Missing mixin → WARNING (may be inconsistent enforcement)
    RETURNS: list[IsolationFinding]

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --src-path, --format
      2. Run all checks
      3. Print report
      4. Exit 1 if any CRITICAL findings

DESIGN DECISIONS:
- AST analysis is heuristic — cannot catch all dynamic query patterns
- CRITICAL: direct query on tenant model without filter (high confidence violation)
- WARNING: missing TenantMixin (may be intentional for global models)
- Does not replace integration tests in test_tenancy.py — complements them
"""
