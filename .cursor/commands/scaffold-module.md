# .cursor/commands/scaffold-module.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Links to: skills/backend/fastapi-router-module.md, skills/backend/module-scaffolder.py -->
<!-- - Procedure: docs/procedures/scaffold-domain-module.md -->

> PURPOSE: Reusable Cursor command for scaffolding a new domain module (bounded context) under apps/api/src/. Creates all required files from templates. Per spec §28.9 item 337.

## Command Metadata

> CONTENT: Command metadata block. Fields:
> - name: "Scaffold Domain Module"
> - description: "Create a new FastAPI bounded context module with router, models, schemas, service, and tests."
> - trigger: "Invoke when adding a new domain module or bounded context to the API"
> - arguments:
>   - module_name: kebab-case name of the module (e.g., "invoices", "customers")
>   - entities: comma-separated list of entity names in this module (e.g., "Invoice,LineItem")
> - linked_skill: skills/backend/fastapi-router-module.md
> - linked_machinery: skills/backend/module-scaffolder.py
> - linked_procedure: docs/procedures/scaffold-domain-module.md

## Steps

> CONTENT: Ordered execution steps:
> 1. Read skills/backend/fastapi-router-module.md completely (mandatory skill search)
> 2. Confirm module_name and entities are known
> 3. Run `make scaffold:module MODULE=<name> ENTITIES=<list>` OR invoke `skills/backend/module-scaffolder.py`
> 4. Verify all generated files were created: __init__.py, router.py, models.py, schemas.py, service.py, tests/test_<name>.py
> 5. Register router in apps/api/src/main.py (see registration pattern in fastapi-router-module.md)
> 6. Create Alembic migration: `make migrate:create MESSAGE="add <name> models"`
> 7. Run `make lint && make typecheck && make test` to verify generated code compiles
> 8. Update docs/api/endpoints.md with stub endpoint descriptions
> 9. Commit: `feat(<name>): scaffold <name> module`

## Expected Output

> CONTENT: Files created/modified by this command:
> - apps/api/src/<module>/__init__.py
> - apps/api/src/<module>/router.py (with CRUD endpoint stubs)
> - apps/api/src/<module>/models.py (with SQLAlchemy models)
> - apps/api/src/<module>/schemas.py (with Pydantic request/response models)
> - apps/api/src/<module>/service.py (with business logic stubs)
> - apps/api/tests/test_<module>.py (with parametrized test stubs)
> - apps/api/src/main.py (modified: router registered)
> - apps/api/alembic/versions/<timestamp>_add_<module>_models.py
