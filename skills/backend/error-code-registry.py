# skills/backend/error-code-registry.py
"""
BLUEPRINT: skills/backend/error-code-registry.py

PURPOSE:
Error code registry validator and documentation generator. Scans the codebase
for error code definitions (AppError subclasses in exceptions.py with code fields),
validates uniqueness, checks that all codes are documented in docs/api/error-codes.md,
and generates updated error documentation if gaps are found.
Part of the documentation generation pipeline (§9.4).

DEPENDS ON:
- ast (stdlib) — parse exceptions.py without importing it
- pathlib (stdlib) — file discovery
- re (stdlib) — pattern matching for error code constants
- argparse (stdlib) — CLI

DEPENDED ON BY:
- skills/backend/error-taxonomy.md — references as machinery
- skills/repo-governance/docs-generator.py — may call for error-codes doc target

CLASSES:

  ErrorCodeEntry:
    PURPOSE: Represents a single error code definition.
    FIELDS:
      - code: str — error code string (e.g., "AUTH_INVALID_CREDENTIALS")
      - class_name: str — Python exception class name
      - status_code: int — HTTP status code
      - message_template: str — default error message
      - source_file: str — file where defined
      - source_line: int — line number

FUNCTIONS:

  scan_error_codes(exceptions_path: Path) -> list[ErrorCodeEntry]:
    PURPOSE: Parse exceptions.py and extract all AppError subclass definitions.
    STEPS:
      1. Parse exceptions.py with ast.parse()
      2. Find all ClassDef nodes that inherit from AppError or its subclasses
      3. For each class: extract code, status_code, message from class body
      4. Return list of ErrorCodeEntry
    RETURNS: list[ErrorCodeEntry]
    RAISES: FileNotFoundError if exceptions.py not found; ValueError if AppError base not found

  check_uniqueness(entries: list[ErrorCodeEntry]) -> list[str]:
    PURPOSE: Check that all error codes are unique.
    STEPS:
      1. Count occurrences of each code value
      2. Return list of duplicate codes
    RETURNS: list[str] of duplicate code values (empty if all unique)

  load_documented_codes(error_codes_doc_path: Path) -> set[str]:
    PURPOSE: Parse docs/api/error-codes.md and extract documented error codes.
    STEPS:
      1. Read file content
      2. Find Markdown table rows
      3. Extract code column values (first column)
    RETURNS: set[str] of documented error codes

  find_gaps(defined: list[ErrorCodeEntry], documented: set[str]) -> tuple[list[str], list[str]]:
    PURPOSE: Compare defined vs documented codes.
    RETURNS: (undocumented_codes, orphaned_codes) where:
      - undocumented_codes: defined in code but not in docs
      - orphaned_codes: documented but not found in code

  generate_error_docs(entries: list[ErrorCodeEntry]) -> str:
    PURPOSE: Generate complete docs/api/error-codes.md content from entries.
    STEPS:
      1. Sort entries by HTTP status code, then by code alphabetically
      2. Group by domain (AUTH, VALIDATION, SYSTEM, etc. — derived from code prefix)
      3. Format as Markdown table: Error Code | HTTP Status | Description | Client Action
    RETURNS: Markdown table string

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --exceptions-path, --docs-path, --mode (check|generate)
      2. Scan and validate
      3. In check mode: exit 1 if gaps found
      4. In generate mode: write updated docs

DESIGN DECISIONS:
- Uses ast not import to avoid FastAPI startup side effects
- Error code prefix convention: AUTH_, VALIDATION_, NOT_FOUND_, CONFLICT_, SYSTEM_
- Docs organized by HTTP status group for client consumption
"""
