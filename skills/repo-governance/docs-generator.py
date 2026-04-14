# skills/repo-governance/docs-generator.py
"""
BLUEPRINT: skills/repo-governance/docs-generator.py

PURPOSE:
Documentation generation engine for the auto-sync pipeline (§9.4).
Parses heterogeneous sources (FastAPI OpenAPI, Pydantic BaseSettings, pyproject.toml,
docker-compose.yml, K8s YAML, Makefile, Alembic versions, .cursor/rules) and
generates Markdown documentation files. Supports two modes:
  --generate: produce fresh documentation from source (make docs:generate)
  --check: verify on-disk docs match generated output; exit non-zero on drift (make docs:check)
Custom Python tooling (not Sphinx/MkDocs) because sources are heterogeneous and
output must be token-optimized Markdown per spec §9.4.

DEPENDS ON:
- pathlib (stdlib) — file discovery and reading
- subprocess (stdlib) — run FastAPI app to get OpenAPI JSON
- json (stdlib) — parse OpenAPI JSON
- re (stdlib) — pattern matching for Makefile target extraction
- argparse (stdlib) — CLI (--generate, --check, --target)
- ast (stdlib) — parse Python files for Settings class fields
- sys (stdlib) — exit codes
- hashlib (stdlib) — detect drift between generated and on-disk content
- csv (stdlib) — read queue.csv columns for docs

DEPENDED ON BY:
- scripts/docs-generate.sh → make docs:generate
- scripts/docs-check.sh → make docs:check (in check mode)
- skills/repo-governance/docs-generator.md — skill playbook references this
- docs/development/docs-generation.md — explains how to extend this

CLASSES:

  DocTarget:
    PURPOSE: Represents a single source → target documentation mapping.
    FIELDS:
      - name: str — human-readable name (e.g., "API Endpoints")
      - source_paths: list[str] — files read to generate this doc
      - target_path: str — output doc file path
      - generator_fn: str — name of the function that generates this section
      - source_annotation: str — comment added to generated section, e.g., "<!-- Generated from: apps/api/src/config.py -->"
    NOTES: All targets are registered in TARGETS list at module level.

  DriftDetected(Exception):
    PURPOSE: Raised when --check mode finds on-disk content differs from generated content.
    FIELDS:
      - target_path: str
      - generated_hash: str
      - on_disk_hash: str

FUNCTIONS:

  generate_endpoint_docs(app_module: str = "apps.api.src.main:app") -> str:
    PURPOSE: Generate docs/api/endpoints.md from FastAPI OpenAPI spec.
    STEPS:
      1. Import the FastAPI app
      2. Call app.openapi() to get OpenAPI dict
      3. Parse paths dict: for each path, extract method, summary, request body schema, response schemas, auth
      4. Format as Markdown table: Method | Path | Description | Auth | Request Schema | Response Schema | Error Codes
      5. Add source annotation comment
    RETURNS: Markdown table string
    RAISES: ImportError if app cannot be imported; RuntimeError if OpenAPI generation fails

  generate_env_var_docs(config_path: Path = Path("apps/api/src/config.py")) -> str:
    PURPOSE: Generate docs/development/environment-vars.md from Pydantic BaseSettings.
    STEPS:
      1. Parse config.py with ast module
      2. Find Settings class (BaseSettings subclass)
      3. For each field: extract name, type annotation, default, Field description
      4. Cross-check against .env.example (flag fields in code but missing from .env.example)
      5. Format as Markdown table: Variable | Description | Type | Default | Required | Profile
    RETURNS: Markdown table string
    RAISES: FileNotFoundError if config.py not found; ValueError if Settings class not found

  generate_error_code_docs(exceptions_path: Path = Path("apps/api/src/exceptions.py")) -> str:
    PURPOSE: Generate docs/api/error-codes.md from exceptions.py.
    STEPS:
      1. Parse exceptions.py with ast module
      2. Find AppError subclasses with code and status_code fields
      3. Format as Markdown table: Error Code | HTTP Status | Description | Client Action
    RETURNS: Markdown table string

  generate_dependency_docs(pyproject_path: Path = Path("pyproject.toml")) -> str:
    PURPOSE: Generate dependency section for docs/development/dependency-management.md.
    STEPS:
      1. Read and parse pyproject.toml (simple TOML parsing or tomllib if 3.11+)
      2. Extract [project.dependencies] and [project.optional-dependencies]
      3. Format as Markdown tables: Package | Version | Purpose
    RETURNS: Markdown table string

  generate_docker_docs(compose_path: Path = Path("docker-compose.yml")) -> str:
    PURPOSE: Generate service documentation for docs/operations/docker.md.
    STEPS:
      1. Read docker-compose.yml (yaml parsing via stdlib or simple regex)
      2. For each service: extract image/build, ports, volumes, profiles, env
      3. Format as Markdown: service name, description, profile, ports, volumes
    RETURNS: Markdown section string

  generate_k8s_docs(k8s_base: Path = Path("deploy/k8s/base")) -> str:
    PURPOSE: Generate documentation for docs/operations/kubernetes.md.
    STEPS:
      1. Read all YAML files in deploy/k8s/base/
      2. For each manifest: extract kind, metadata.name, key spec fields
      3. Format as Markdown: manifest type, name, key configuration
    RETURNS: Markdown section string

  generate_makefile_docs(makefile_path: Path = Path("Makefile")) -> str:
    PURPOSE: Generate command table for docs/development/local-setup.md and README.md.
    STEPS:
      1. Read Makefile
      2. Extract target names and help comments (lines before target matching "## help text")
      3. Format as Markdown table: Target | Description
    RETURNS: Markdown table string

  run_generate(targets: list[str] | None = None) -> dict[str, str]:
    PURPOSE: Run all (or specified) doc generators, return target → content mapping.
    STEPS:
      1. Determine which targets to run
      2. Call each generator function
      3. Add source annotations to each generated section
      4. Return mapping of target_path → generated_content
    RETURNS: dict[str, str]

  run_check(targets: list[str] | None = None) -> bool:
    PURPOSE: Check if on-disk docs match what would be generated.
    STEPS:
      1. Run run_generate() to get expected content
      2. For each target: read on-disk content
      3. Compare hashes
      4. If any drift: collect all drifted targets and raise DriftDetected
    RETURNS: True if all match, raises DriftDetected if any drift

  write_generated(generated: dict[str, str], repo_root: Path = Path(".")) -> None:
    PURPOSE: Write generated content to target files.
    STEPS:
      1. For each (target_path, content) pair: write to disk
      2. Preserve existing non-generated sections (identified by "<!-- GENERATED" markers)
    RAISES: IOError if file cannot be written

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --generate | --check, --target (specific target or "all")
      2. Run appropriate mode
      3. Print results
      4. Exit 0 if success, 1 if check fails (drift detected)

CONSTANTS:
  - TARGETS: list[DocTarget] — registered source → target mappings
  - GENERATED_SECTION_START: str = "<!-- GENERATED FROM SOURCE — DO NOT EDIT MANUALLY"
  - GENERATED_SECTION_END: str = "<!-- END GENERATED SECTION -->"

DESIGN DECISIONS:
- Source annotations embedded in each generated section for transparency
- Generated sections wrapped in HTML comment markers so non-generated content is preserved
- --check mode compares hashes (not full diff) for speed; CI can diff if needed
- Uses ast (not import) for config.py parsing to avoid FastAPI startup side effects
- TOML parsing uses tomllib (stdlib in Python 3.11+) with fallback to tomli package
"""
