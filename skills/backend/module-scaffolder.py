# skills/backend/module-scaffolder.py
"""
BLUEPRINT: skills/backend/module-scaffolder.py

PURPOSE:
Generates a new FastAPI module from embedded templates. Creates all module files
(__init__.py, router.py, models.py, schemas.py, service.py, dependencies.py)
with proper imports, type hints, and docstrings. Also creates the test file stub.
More detailed than scripts/scaffold-module.sh — produces production-quality
typed stubs that follow PYTHON_PROCEDURES.md conventions.
Invoked via: make scaffold:module MODULE=<name> or python skills/backend/module-scaffolder.py <name>

DEPENDS ON:
- pathlib (stdlib) — directory creation and file writing
- argparse (stdlib) — CLI argument parsing
- textwrap (stdlib) — template dedenting
- sys (stdlib) — exit codes

DEPENDED ON BY:
- scripts/scaffold-module.sh → make scaffold:module
- skills/backend/fastapi-router-module.md — references as machinery
- .cursor/commands/scaffold-module.md — references as machinery

FUNCTIONS:

  to_class_name(module_name: str) -> str:
    PURPOSE: Convert module name to PascalCase class name prefix.
    STEPS: Split on underscore or hyphen, capitalize each part, join.
    RETURNS: str — e.g., "invoice_items" → "InvoiceItem"

  render_init_py(module_name: str, class_name: str) -> str:
    PURPOSE: Generate __init__.py content for a new module.
    STEPS: Template with module title comment, router export.
    RETURNS: Complete file content string.

  render_router_py(module_name: str, class_name: str, entities: list[str]) -> str:
    PURPOSE: Generate router.py with CRUD endpoint stubs for each entity.
    STEPS:
      1. Import fastapi, schemas, service, dependencies
      2. Create APIRouter with prefix and tags
      3. For each entity: generate GET list, GET single, POST create, PUT update, DELETE endpoints
      4. Each endpoint: typed params, Depends(get_current_user), Depends(get_db), response_model
    RETURNS: Complete router.py content

  render_models_py(module_name: str, entities: list[str]) -> str:
    PURPOSE: Generate models.py with SQLAlchemy model stubs.
    STEPS:
      1. Import SQLAlchemy components and Base
      2. For each entity: generate class with id (UUID), created_at, updated_at columns
      3. Add TenantMixin hint (commented, human fills based on tenant requirement)
    RETURNS: Complete models.py content

  render_schemas_py(module_name: str, entities: list[str]) -> str:
    PURPOSE: Generate schemas.py with Pydantic request/response models.
    STEPS:
      1. Import Pydantic BaseModel, ConfigDict
      2. For each entity: generate Create<Entity>Request, Update<Entity>Request, <Entity>Response
      3. All request models: frozen=True
    RETURNS: Complete schemas.py content

  render_service_py(module_name: str, class_name: str, entities: list[str]) -> str:
    PURPOSE: Generate service.py with business logic class stubs.
    STEPS:
      1. Generate <ClassPrefix>Service class with AsyncSession injection
      2. For each entity: stub methods create_, get_, list_, update_, delete_
      3. Each method: typed params and return type, raise NotImplementedError
    RETURNS: Complete service.py content

  render_dependencies_py(module_name: str, class_name: str) -> str:
    PURPOSE: Generate dependencies.py with FastAPI Depends() factory.
    RETURNS: Complete dependencies.py content

  render_test_py(module_name: str, class_name: str, entities: list[str]) -> str:
    PURPOSE: Generate test_<module>.py with parametrized test stubs.
    STEPS:
      1. Import pytest, httpx, fixtures from conftest
      2. For each entity: generate test functions for each CRUD endpoint
      3. Test names follow: test_<endpoint>_<scenario>_<expected>
      4. Bodies: raise NotImplementedError (TODO for implementation agent)
    RETURNS: Complete test file content

  scaffold_module(
    module_name: str,
    entities: list[str],
    src_root: Path = Path("apps/api/src"),
    tests_root: Path = Path("apps/api/tests")
  ) -> list[Path]:
    PURPOSE: Create all module files on disk.
    STEPS:
      1. Create src_root/<module_name>/ directory
      2. Render and write all module files
      3. Create test file
      4. Print manifest of created files
    RETURNS: list[Path] of all created files
    RAISES: FileExistsError if module directory already exists (refuse to overwrite)

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: module_name (required), --entities (comma-separated), --src-root, --tests-root
      2. Validate module_name is valid Python identifier
      3. Run scaffold_module()
      4. Print next steps (register router in main.py, create migration)

CONSTANTS:
  - REQUIRED_COLUMNS: None — columns are determined by entity list
  - FILE_TITLE_TEMPLATE: str = "# apps/api/src/{module_name}/{filename}" — per §1.7

DESIGN DECISIONS:
- Uses inline string templates (not Jinja2) to avoid template dependency
- Refuses to overwrite existing modules (FileExistsError) — always create fresh
- Generates NotImplementedError stubs for service methods to force implementation
- Test file uses pytest-asyncio auto mode (asyncio_mode = "auto" assumed)
- TenantMixin usage is a comment hint — human decides if tenant-scoped
"""
