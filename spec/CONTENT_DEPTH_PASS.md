# spec/CONTENT_DEPTH_PASS.md

# Composer 2 — Content Depth Pass

## YOUR ROLE

Several files in this repository were created with thin or placeholder content. You will **deepen** each file listed below to match the spec's intent. Read `spec/spec.md` and `PYTHON_PROCEDURES.md` before starting.

**Rules:**
- Do NOT modify `spec/spec.md` or `spec/IMPLEMENTATION_PLAN.md`.
- Do NOT create new files. Only edit files listed here.
- Keep the existing file title comment (first line) in every file.
- For Python files, follow `PYTHON_PROCEDURES.md` strictly.
- After completing ALL edits, check off the corresponding rows in `spec/IMPLEMENTATION_PLAN.md` (change `[ ]` to `[x]`).

---

## 1. `apps/api/src/exceptions.py`

**Problem:** Missing two exception classes from the spec: `TenantIsolationError` and `StateTransitionError`. Also, `ExternalServiceError` and `NotFoundError` lack the extra fields we specified.

**What to add — keep all existing classes, add/modify these:**

```
TenantIsolationError(AppError):
    code = "TENANT_ISOLATION_VIOLATION"
    status_code = 403
    Carries: tenant_id (str | None), attempted_resource (str | None)
    Note: Should log at WARNING level when raised (add a note in the docstring about this)

StateTransitionError(AppError):
    code = "STATE_TRANSITION_INVALID"
    status_code = 409
    Carries: current_state (str), attempted_state (str), allowed_states (set[str])
    __init__ should build a descriptive message from these fields automatically

NotFoundError — add fields:
    entity: str (e.g., "User", "Invoice")
    identifier: str (e.g., the ID that wasn't found)
    __init__(self, entity: str, identifier: str) that builds message like f"{entity} '{identifier}' not found"

ExternalServiceError — add fields:
    service_name: str
    original_error: Exception | None = None
    __init__(self, service_name: str, message: str | None = None, original_error: Exception | None = None)

RateLimitError — add field:
    retry_after: int (seconds)
    __init__(self, retry_after: int = 60)
```

Also add to `AppError` base class:
- `detail: dict[str, object] | None = None` field for arbitrary structured metadata
- A `to_dict()` method that returns `{"code": self.code, "message": self.message, "detail": self.detail}`

---

## 2. `apps/api/src/pagination.py`

**Problem:** Currently a 13-line re-export shim. It should contain the actual query-level pagination logic that routers use, while the contract types stay in `packages/contracts/pagination.py`.

**Replace the file with a full implementation containing:**

```
Import PaginationParams, PageInfo, PaginatedResponse from packages.contracts.pagination

paginate_query(query: Select, params: PaginationParams, cursor_column: Column) -> Select:
    PURPOSE: Apply cursor-based or offset-based pagination to a SQLAlchemy Select.
    LOGIC:
    - If params.cursor is set: decode it, apply WHERE cursor_column > decoded_value, LIMIT params.limit + 1
    - If params.offset is set: apply OFFSET params.offset, LIMIT params.limit + 1
    - The +1 is to detect has_next without a separate COUNT query
    RETURNS: Modified Select statement

encode_cursor(value: Any) -> str:
    Base64url-encode the string representation of the value.

decode_cursor(cursor: str) -> str:
    Base64url-decode. Raise ValidationError on invalid input.

async paginated_response(
    query: Select,
    params: PaginationParams,
    session: AsyncSession,
    cursor_column: Column,
) -> PaginatedResponse:
    PURPOSE: Execute the paginated query and build the full PaginatedResponse.
    LOGIC:
    1. Apply paginate_query to get the modified query
    2. Execute via session
    3. Fetch limit+1 rows
    4. has_next = len(rows) > params.limit
    5. Trim to params.limit rows
    6. Build PageInfo with has_next, next_cursor (encode last row's cursor column if has_next)
    7. Return PaginatedResponse(items=rows, page_info=page_info)
```

Keep `__all__` exporting both the local functions AND the re-exported contract types.

---

## 3. `apps/api/tests/test_tenancy.py`

**Problem:** Single skipped placeholder test. Should have real tests even though domain resources don't exist yet — we can test the middleware and mixin directly.

**Replace with real tests:**

```
import pytest
from httpx import AsyncClient (or the test client from conftest)

Tests to write (all using pytest.mark.asyncio where needed):

test_tenant_mixin_adds_tenant_id_column():
    Verify that TenantMixin when applied to a model class adds a tenant_id column.
    Import TenantMixin and Base from the tenancy module.
    Create a temporary model class that uses TenantMixin.
    Assert the model has a 'tenant_id' column in its __table__.columns.

test_tenant_middleware_sets_request_state():
    Create a mock Request with a JWT claim containing tenant_id.
    Pass it through TenantMiddleware.
    Assert request.state.tenant_id is set correctly.

test_tenant_middleware_missing_tenant_returns_403():
    Create a mock Request with no tenant_id in the JWT.
    Verify the middleware returns a 403 response or raises TenantIsolationError.

test_tenant_model_has_required_fields():
    Import Tenant model.
    Assert it has: id, name, is_active, created_at fields.

test_tenant_mixin_query_scoping():
    If TenantMixin provides a class method for scoped queries, test that it
    filters by tenant_id. If not yet implemented, write the test as a clear
    specification of expected behavior with pytest.skip("Scoped query not yet implemented").
```

Remove the existing skipped placeholder test.

---

## 4. `skills/agent-ops/queue-intelligence.py`

**Problem:** Only implements a topological sort with cycle detection. Missing the four core classes: `DependencyGraph`, `ComplexityScorer`, `BatchSuggester`, `ConflictDetector`. Missing CLI subcommands.

**Keep the existing `load_graph` and `kahn` functions (they're good). Add:**

```
Imports: add dataclasses, re, subprocess (for git log), json, datetime

@dataclass
class QueueItem:
    id: str
    batch: str
    phase: str
    category: str
    summary: str
    dependencies: list[str]
    notes: str
    created_date: str
    status: str = ""

@dataclass
class ComplexityScore:
    value: int          # 1-10
    label: str          # S/M/L/XL
    factors: list[str]  # human-readable explanations

@dataclass
class ConflictReport:
    item_a: str
    item_b: str
    overlapping_patterns: list[str]
    risk: str           # low/medium/high

class DependencyGraph:
    Wraps the existing kahn() logic in a class.
    __init__(self, items: list[QueueItem], archived_ids: set[str])
    build() -> None: populate internal adjacency from items
    get_ready_items() -> list[QueueItem]: deps all in archived_ids
    get_blocked_items() -> list[tuple[QueueItem, list[str]]]: items + their missing dep IDs
    detect_cycles() -> list[list[str]]: uses kahn, returns cycle members if any
    render_mermaid() -> str: output a Mermaid flowchart string (graph TD, arrows for deps, color blocked items red)
    topological_sort() -> list[QueueItem]: returns items in dependency-safe order

class ComplexityScorer:
    score(item: QueueItem, archive: list[QueueItem]) -> ComplexityScore:
        Factors to score:
        - summary length (longer = more complex, likely)
        - number of dependencies (more deps = more integration risk)
        - category heuristic (infrastructure/security = higher base)
        - historical: if archive has same-category items, average their created-to-completed span
        Map total to 1-10 and S/M/L/XL

class BatchSuggester:
    suggest(items: list[QueueItem]) -> list[list[QueueItem]]:
        Group items by:
        - Same batch value (explicit grouping)
        - Shared module references in summary (regex for apps/api/src/<name>/)
        - Shared dependencies (items depending on same prerequisite)
        Return list of suggested batches

class ConflictDetector:
    detect(items: list[QueueItem]) -> list[ConflictReport]:
        For each pair of open items:
        - Extract file/module references from summary (regex patterns for paths)
        - If overlapping references found, create ConflictReport
        - Risk: high if >3 overlapping patterns, medium if 1-3, low if only directory-level overlap

def load_items(path: Path) -> list[QueueItem]:
    Parse CSV into QueueItem list (handle the comment line at top)

def load_archive_ids(path: Path) -> set[str]:
    Parse archive CSV, return set of IDs with status=done

def full_analysis(repo_root: Path) -> dict:
    Load queue + archive
    Build DependencyGraph, run all analyses
    Return structured dict with: ready_items, blocked_items, cycles, complexity_scores, batch_suggestions, conflicts

Rewrite main() with argparse subcommands:
    graph: print DependencyGraph.render_mermaid()
    analyze: run full_analysis, print formatted report
    ready: print only ready items
    blocked: print only blocked items with reasons
```

---

## 5. `skills/repo-governance/docs-generator.py`

**Problem:** 13-line placeholder that just prints a reminder. Should be the documentation generation engine.

**Replace entirely with:**

```
Imports: ast, tomllib, csv, io, json, re, sys, argparse, pathlib, yaml (PyYAML), dataclasses

@dataclass
class DocTarget:
    name: str
    source_paths: list[str]
    output_path: str
    generator: Callable  # reference to the generator function
    description: str

@dataclass
class GenerationResult:
    target: str
    status: str  # generated | unchanged | drifted
    diff_lines: int

def generate_makefile_doc(makefile_path: Path) -> str:
    Parse Makefile for lines matching "^## target: description"
    Build a Markdown table: | Target | Description |
    Sort by category (group dev, test, queue, docs, deploy, etc.)

def generate_env_vars_doc(config_path: Path) -> str:
    Use ast.parse on config.py
    Find the Settings class (BaseSettings subclass)
    Extract field names, type annotations, default values, and Field(description=...) if present
    Group by comment sections (scan for "# Section" comments before field groups)
    Build a Markdown table: | Variable | Type | Default | Required | Description |

def generate_compose_doc(compose_path: Path) -> str:
    Parse docker-compose.yml with yaml.safe_load
    Extract services with their image, ports, profiles, depends_on, healthcheck
    Build Markdown table: | Service | Image | Ports | Profile | Health Check |

def generate_k8s_doc(k8s_base_path: Path) -> str:
    Parse each .yaml file in the directory
    Extract kind, metadata.name, key spec fields (replicas, image, ports, resources, probes)
    Build Markdown summary per resource

def generate_rules_index(rules_path: Path) -> str:
    For each .md file in .cursor/rules/:
    Parse YAML frontmatter (between --- markers)
    Extract alwaysApply or globs, and first paragraph as summary
    Build Markdown table: | Rule | Scope | Summary |

def generate_migration_history(versions_path: Path) -> str:
    Scan .py files in alembic/versions/
    Extract revision id from `revision = "..."`, down_revision, and module docstring
    Build Markdown table: | Revision | Description | Down Revision |

def run_pipeline(mode: str, targets: list[DocTarget], repo_root: Path) -> list[GenerationResult]:
    For each target:
        generated_content = target.generator(repo_root / target.source_paths[0])
        Add "<!-- Generated from: {source} — do not edit manually -->" header
        If mode == "generate": write to output_path, report generated/unchanged
        If mode == "check": compare against existing file, report drifted/unchanged
    Return results

TARGETS: list[DocTarget] — registry of all source-to-target mappings:
    - Makefile -> section of docs/development/local-setup.md
    - config.py -> docs/development/environment-vars.md
    - docker-compose.yml -> section of docs/operations/docker.md
    - deploy/k8s/base/ -> section of docs/operations/kubernetes.md
    - .cursor/rules/ -> rule index section
    - alembic/versions/ -> migration history section

def main() -> int:
    argparse: --mode generate|check, --target (optional specific target), --repo-root
    Run pipeline, print summary
    Exit 0 if all unchanged/generated, exit 1 if any drifted (in check mode)
```

Note: The FastAPI OpenAPI and error-codes generators require the app to be importable, so those should be clearly marked as "requires running app" and skipped gracefully if import fails. Focus on the AST-based and file-parsing generators which always work.

---

## 6. `setup.sh`

**Problem:** Missing Docker Compose startup and health check waiting. Also missing Docker/docker-compose tool check.

**Add to the existing script (keep everything that's there, insert new steps):**

After the `need python3` / `need make` block, add:
```
need docker
need git

# Check docker compose (v2 plugin or standalone)
if docker compose version >/dev/null 2>&1; then
  COMPOSE="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE="docker-compose"
else
  echo "Missing: docker compose (v2 plugin or docker-compose standalone)" >&2
  exit 1
fi
```

After `pip install -e ".[dev]"` and the `.env` copy block, add:
```
echo "Starting Docker Compose services..."
$COMPOSE up -d

echo "Waiting for services to be healthy..."
MAX_WAIT=60
WAITED=0
until $COMPOSE ps --format json | python3 -c "
import sys, json
data = json.loads(sys.stdin.read())
services = data if isinstance(data, list) else [data]
all_healthy = all(s.get('Health','') in ('healthy','') for s in services if s.get('State')=='running')
sys.exit(0 if all_healthy else 1)
" 2>/dev/null; do
  sleep 2
  WAITED=$((WAITED + 2))
  if [ $WAITED -ge $MAX_WAIT ]; then
    echo "Services did not become healthy within ${MAX_WAIT}s" >&2
    $COMPOSE logs --tail=20
    exit 1
  fi
done
echo "Services healthy."
```

---

## 7. `setup.bat`

**Problem:** Missing Docker startup, health wait, and lint/typecheck/test steps that the `.sh` version has.

**Replace entirely with a full implementation that mirrors setup.sh:**

```
@echo off
REM setup.bat — Windows bootstrap (requires Python 3.12+, Docker, Make on PATH)
setlocal enabledelayedexpansion
cd /d "%~dp0"

where python >nul 2>nul || (echo ERROR: Python not found on PATH & exit /b 1)
where docker >nul 2>nul || (echo ERROR: Docker not found on PATH & exit /b 1)
where make >nul 2>nul || (echo ERROR: Make not found on PATH & exit /b 1)
where git >nul 2>nul || (echo ERROR: Git not found on PATH & exit /b 1)

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -e ".[dev]"

if not exist .env (
    copy .env.example .env
    echo Created .env from .env.example
)

set PYTHONPATH=%CD%

echo Starting Docker Compose services...
docker compose up -d
timeout /t 10 /nobreak >nul

make migrate
make lint
make typecheck
make test

echo.
echo Setup complete. Run run.bat or make dev to start the API.
endlocal
```

---

## 8. `run.sh`

**Problem:** Doesn't start Docker services or wait for health. Just delegates to dev.sh.

**Add Docker startup before the exec line:**

After the `.env` check and venv activation, before `exec "$ROOT/scripts/dev.sh"`, add:
```
# Ensure Docker services are running
if command -v docker >/dev/null 2>&1 && [ -f docker-compose.yml ]; then
  if ! docker compose ps --status running --format '{{.Name}}' 2>/dev/null | grep -q .; then
    echo "Starting Docker Compose services..."
    docker compose up -d
    sleep 3
  fi
fi

echo "API: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo "Health: http://localhost:8000/health"
```

---

## 9. `run.bat`

**Problem:** Doesn't start Docker services.

**Add before the uvicorn line:**

```
echo Starting Docker services if not running...
docker compose up -d 2>nul
timeout /t 3 /nobreak >nul

echo API: http://localhost:8000
echo Docs: http://localhost:8000/docs
```

---

## 10. `AGENTS.md`

**Problem:** Missing explicit link to `PYTHON_PROCEDURES.md`.

**Add a new section 15 at the end (before any closing content), or append to section 14:**

```
## 15. Python implementation procedures

All Python code in this repository MUST follow **[PYTHON_PROCEDURES.md](PYTHON_PROCEDURES.md)** — the 18 implementation procedures that govern type safety, boundary definitions, import direction, error handling, configuration, async patterns, and testing.

Key rules enforced:
- Every public function is fully typed (params, return, errors).
- Boundary shapes (requests, responses, config) defined as Pydantic models before logic.
- Import direction: `router` → `service` → `repository`. Never reverse.
- No `os.getenv()` outside `apps/api/src/config.py`.
- State modeled with `Enum` and explicit transition maps.
- `None` handled explicitly; never used as an error signal.

See the full document for all 18 procedures, the condensed 12-point rule set, and refactor triggers. Code review (procedure 18) checks compliance with all of these.
```

---

## 11. `.cursor/rules/global.md`

**Problem:** "Canonical commands" rule is only implied, not explicit.

**Add a new section after "Mandatory skill search" and before "Forbidden patterns":**

```
## Canonical commands

1. **Always use `make` targets** over ad hoc shell commands. Run `make help` to see all targets.
2. If a `make` target exists for an operation, use it. Do not run the underlying script directly unless debugging the script itself.
3. Colon-form targets (`make queue:validate`) and hyphen-form (`make queue-validate`) are equivalent aliases. Either form is acceptable.
4. If you need a command that has no target, **propose adding one** (new script in `scripts/` + Makefile entry) rather than running a one-off.
5. Document all commands you run in PR descriptions using the Make target form.
```

---

---

## 12. `packages/contracts/pagination.py`

**Problem:** Has `PaginationParams`, `encode_cursor`, `decode_cursor`, and `calculate_offset` but is missing `PageInfo` and `PaginatedResponse[T]` — the generic response models that every list endpoint needs.

**Add these classes after the existing code:**

```
class PageInfo(BaseModel):
    """Pagination metadata returned with every list response."""
    model_config = {"frozen": True}

    has_next: bool
    has_previous: bool = False
    next_cursor: str | None = None
    previous_cursor: str | None = None
    total_count: int | None = None   # Optional — expensive for large tables

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    """Standard envelope for all paginated list endpoints."""
    items: list[T]
    page_info: PageInfo
```

Add `PageInfo` and `PaginatedResponse` to `__all__` if present, or add an `__all__` list.

---

## 13. `apps/api/src/dependencies.py`

**Problem:** Currently 17 lines that only re-export `get_db`. Should be the central wiring point that all routers import from.

**Replace with a full implementation:**

```
from apps.api.src.database import get_db
from apps.api.src.config import Settings, get_settings
from apps.api.src.auth.dependencies import get_current_user, require_auth
from starlette.requests import Request

async def get_db_session():
    Re-export get_db (async generator yielding AsyncSession)

def get_app_settings() -> Settings:
    Return get_settings() — thin wrapper for consistency in Depends() usage

def get_correlation_id(request: Request) -> str:
    Extract correlation_id from request.state (set by CorrelationIdMiddleware).
    Fallback: generate uuid4 if not present.

Re-export get_current_user and require_auth from auth.dependencies for convenience.
Routers should import from here, not reach into auth/ directly.

__all__ = ["get_db", "get_app_settings", "get_correlation_id", "get_current_user", "require_auth"]
```

---

## 14. CI Workflow — `.github/workflows/ci.yml`

**Problem:** Single job with no matrix testing, no image build, no security scan, no migration dry-run, no k8s validation. The spec (§11.2) requires: lint, typecheck, tests (SQLite + Postgres matrix), image build + scan, docs check, migration dry-run, k8s validate.

**Replace the single `validate` job with multiple jobs:**

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-python
      - run: make lint
      - run: make fmt

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-python
      - run: make typecheck

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        db: [sqlite, postgres]
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-python
      - name: Set DB URL
        run: |
          if [ "${{ matrix.db }}" = "postgres" ]; then
            echo "DATABASE_URL=postgresql+asyncpg://test:test@localhost:5432/test" >> $GITHUB_ENV
          else
            echo "DATABASE_URL=sqlite+aiosqlite:///test.db" >> $GITHUB_ENV
          fi
      - run: make test
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage-${{ matrix.db }}
          path: coverage.xml

  build:
    runs-on: ubuntu-latest
    needs: [lint, typecheck, test]
    steps:
      - uses: actions/checkout@v4
      - run: make image-build
      - run: make image-scan || true

  queue-validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-python
      - run: make queue-validate
```

Use `actions/checkout@v4` (not v6 which doesn't exist).

---

## 15. CI Workflow — `.github/workflows/security.yml`

**Problem:** Only runs `make security-scan`. The spec requires dependency review on PRs, code scanning, and image scanning.

**Expand to:**

```yaml
on:
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 12 * * 1"
  workflow_dispatch: {}

jobs:
  dependency-review:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/dependency-review-action@v4

  code-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-python
      - run: make security-scan

  image-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make image-build
      - name: Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: template-api:local
          severity: CRITICAL,HIGH
```

---

## 16. CD Workflow — `.github/workflows/cd.yml`

**Problem:** Only builds an image on manual dispatch. Missing environment promotion (dev -> staging -> prod), release verification, and environment protection.

**Expand to:**

```yaml
on:
  push:
    branches: [main]
    tags: ["v*"]
  workflow_dispatch:
    inputs:
      environment:
        description: "Target environment"
        required: true
        type: choice
        options: [dev, staging, prod]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    outputs:
      image_tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}/api
      - uses: docker/build-push-action@v6
        with:
          context: .
          file: apps/api/Dockerfile
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-dev:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: dev
    steps:
      - uses: actions/checkout@v4
      - run: echo "Deploy to dev — implement with kubectl/helm"

  deploy-staging:
    needs: build
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-python
      - run: make release-verify
      - run: echo "Deploy to staging — implement with kubectl/helm"

  deploy-prod:
    needs: deploy-staging
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment: prod
    steps:
      - uses: actions/checkout@v4
      - run: echo "Deploy to prod — implement with kubectl/helm"
```

---

## 17. `scripts/repo_self_audit.py`

**Problem:** Only checks 6 required paths and runs queue validation. Should be the comprehensive audit per spec §24: check all critical files exist, check skills have required section headings, check prompts have YAML front matter, check file title comments, check Make targets are documented.

**Expand the REQUIRED_PATHS list significantly and add these checks:**

```
Expand REQUIRED_PATHS to include at least:
    AGENTS.md, PYTHON_PROCEDURES.md, spec/spec.md, Makefile, pyproject.toml,
    .gitignore, .dockerignore, .gitattributes, .env.example, docker-compose.yml,
    apps/api/Dockerfile, apps/api/src/main.py, apps/api/src/config.py,
    apps/api/src/exceptions.py, apps/api/src/database.py,
    queue/queue.csv, queue/queuearchive.csv, queue/QUEUE_INSTRUCTIONS.md,
    queue/QUEUE_AGENT_PROMPT.md, LICENSE, CONTRIBUTING.md, README.md,
    .github/workflows/ci.yml, .github/workflows/cd.yml

Add check: file_title_comments()
    For each .py, .md, .sh, .yml file in the repo (excluding .git/, node_modules/, .venv/):
    Check first meaningful line has the file title comment per §1.7 convention.
    Report files missing their title comment.

Add check: skills_have_sections()
    For each .md file in skills/:
    Check it contains headings for: Purpose, When to invoke, Prerequisites
    (at minimum — full §6.2 check for [FULL] skills)
    Report skills missing required headings.

Add check: prompts_have_frontmatter()
    For each .md file in prompts/ (except README.md):
    Check it starts with YAML front matter (--- delimiters)
    Report prompts missing front matter.

Add check: makefile_targets_documented()
    Parse Makefile for targets.
    Check each target has a ## help comment.
    Report undocumented targets.
```

Print a structured report with pass/fail per check category and an overall status.

---

## 18. Dockerfile — `apps/api/Dockerfile`

**Problem:** Uses `python:3.14-slim` which doesn't exist yet. Should be `python:3.12-slim` to match the spec's "Python 3.12+" requirement. Also missing the multi-stage build pattern the spec requires (§16.1).

**Replace with proper multi-stage build:**

```dockerfile
# apps/api/Dockerfile
FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml README.md ./
COPY apps apps
COPY packages packages
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir .

FROM python:3.12-slim AS runner
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/* \
 && useradd --create-home --uid 1000 app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /build/apps /app/apps
COPY --from=builder /build/packages /app/packages

USER app
ENV PYTHONPATH=/app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8000/health >/dev/null || exit 1

CMD ["python", "-m", "uvicorn", "apps.api.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 19. `.github/actions/setup-python/action.yml`

**Problem:** Need to verify it installs dev dependencies and caches properly. Check and fix if needed.

**Should contain:**

```yaml
name: Setup Python
description: Install Python, cache pip, install project with dev extras
runs:
  using: composite
  steps:
    - uses: actions/setup-python@v5
      with:
        python-version: "3.12"
        cache: pip
    - run: pip install -e ".[dev]"
      shell: bash
    - run: echo "PYTHONPATH=${{ github.workspace }}" >> $GITHUB_ENV
      shell: bash
```

---

## 20. `queue/queue.csv` — Seed Data

**Problem:** Empty CSV with just headers. After template initialization, the queue should have at least a few seed items demonstrating the format and driving the first agent work.

**Add seed rows (keep the comment line and header):**

```csv
# queue/queue.csv
id,batch,phase,category,summary,dependencies,related_files,notes,created_date
Q-001,1,1,infrastructure,"Configure production PostgreSQL connection: update apps/api/src/config.py with connection pool settings (pool_size, max_overflow, pool_timeout), verify docker-compose.yml db profile works with asyncpg, add integration test that connects to Postgres, update docs/architecture/data-layer.md with connection configuration details. Acceptance: make test passes with DATABASE_URL pointing to Postgres container.",,template-seed,2025-01-01
Q-002,1,2,core-api,"Implement a sample domain module to validate the scaffolding pattern: create apps/api/src/example/ with router.py, service.py, models.py, schemas.py following docs/development/module-patterns.md. Include CRUD endpoints for a simple Example entity. Add tests in apps/api/tests/test_example.py. Register router in main.py. Acceptance: all CRUD endpoints return correct status codes, tests pass, module follows Python procedures.",Q-001,template-seed,2025-01-01
Q-003,1,3,testing,"Increase test coverage to 70%: audit existing tests for gaps, add edge-case tests for auth (expired tokens, malformed JWTs, duplicate registration), add integration tests for health endpoints with database down scenario, add tenant middleware tests. Acceptance: make test reports >=70% coverage.",Q-002,template-seed,2025-01-01
```

---

## EXECUTION

Work through items 1–20 in order. For each:
1. Read the current file content.
2. Apply the changes described above.
3. Verify the file is syntactically valid (Python files should parse, YAML should be valid, shell scripts should have correct syntax).
4. After all 20 items are done, check off the corresponding files in `spec/IMPLEMENTATION_PLAN.md`.
