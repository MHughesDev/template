# skills/testing/test-scaffolder.py
"""

PURPOSE:
Generates test stubs for a given module. Analyzes the router file for endpoint
decorators and the service file for public methods, then produces parametrized
test functions with descriptive names following the naming convention:
test_<unit>_<scenario>_<expected>. Generated stubs raise NotImplementedError
to force the implementation agent to fill them in.
Invoked via: python skills/testing/test-scaffolder.py <module_path>

DEPENDS ON:
- ast (stdlib) — parse router.py and service.py without importing
- pathlib (stdlib) — file discovery
- argparse (stdlib) — CLI argument parsing
- textwrap (stdlib) — template dedenting

DEPENDED ON BY:
- skills/testing/pytest-conventions.md — references as machinery
- skills/backend/module-scaffolder.py — may call to generate test file alongside module files

FUNCTIONS:

  extract_router_endpoints(router_path: Path) -> list[dict[str, str]]:
    PURPOSE: Parse router.py and extract all endpoint definitions.
    STEPS:
      1. ast.parse() router file
      2. Find function definitions decorated with @router.get, @router.post, etc.
      3. For each: extract method, path, function_name, response_model
    RETURNS: list of endpoint dicts with keys: method, path, function_name, response_model

  extract_service_methods(service_path: Path) -> list[str]:
    PURPOSE: Parse service.py and extract all public method names.
    STEPS:
      1. ast.parse() service file
      2. Find class methods not starting with _ (public methods)
    RETURNS: list of method names

  generate_endpoint_tests(endpoints: list[dict], module_name: str) -> str:
    PURPOSE: Generate test functions for each endpoint.
    STEPS:
      1. For each endpoint: generate 3 test stubs:
         - Happy path: test_<fn>_valid_request_returns_<2xx>
         - Auth failure: test_<fn>_unauthenticated_returns_401
         - Validation failure: test_<fn>_invalid_body_returns_422 (for POST/PUT)
      2. Each test body: raise NotImplementedError(f"TODO: Implement test for {endpoint}")
    RETURNS: Test functions as string

  generate_test_file(
    module_path: Path,
    module_name: str
  ) -> str:
    PURPOSE: Generate complete test file content for a module.
    STEPS:
      1. Generate imports (pytest, httpx, fixtures)
      2. Generate endpoint tests
      3. Add markers (@pytest.mark.unit or @pytest.mark.integration hints)
    RETURNS: Complete test file content

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: module_path, --output (stdout or file path)
      2. Generate test file
      3. Write to output

DESIGN DECISIONS:
- Generated tests raise NotImplementedError (not pass) to force explicit implementation
- Test naming strictly follows: test_<endpoint_fn>_<scenario>_<expected>
- Fixtures referenced by name matching conftest.py (client, auth_headers, db_session)
- NotImplementedError includes helpful TODO message with endpoint details
"""
