# skills/init/archetype-mapper.py
"""

PURPOSE:
Maps project archetype to default profiles, queue categories, module set,
and file manifest. Produces a structured JSON initialization plan that
subsequent initialization skills and scripts consume.
Implements the spec §27.3 archetype-to-profile mapping table.

DEPENDS ON:
- pathlib (stdlib) — file reading
- json (stdlib) — output serialization
- re (stdlib) — parsing idea.md archetype selection
- argparse (stdlib) — CLI

DEPENDED ON BY:
- skills/init/archetype-mapper.md — references as machinery
- scripts/init-repo.sh — may call this to generate plan

CLASSES:

  InitializationPlan:
    PURPOSE: The complete initialization plan for a project.
    FIELDS:
      - archetype: str — the selected archetype
      - profiles: list[str] — profiles to enable (resolved with overrides)
      - queue_categories: list[str] — queue categories to add to QUEUE_INSTRUCTIONS.md
      - modules: list[str] — bounded context module names from idea.md §4.2
      - files_to_create: list[str] — files to scaffold (module files, profile files)
      - files_to_modify: list[str] — existing files to update (main.py, docker-compose.yml, etc.)
      - env_var_groups: list[str] — profile groups to add to .env.example
    NOTES: Serialized as JSON for consumption by downstream scripts.

CONSTANTS:

  ARCHETYPE_PROFILES: dict[str, list[str]] — per §27.3
    Mapping of archetype name → default enabled profiles:
    - "api_service": []
    - "full_stack_web": ["web"]
    - "full_stack_with_mobile": ["web", "mobile"]
    - "platform_internal": ["workers"]
    - "data_pipeline": ["workers", "scheduled_jobs"]
    - "ai_ml_service": ["ai_rag", "workers"]
    - "marketplace": ["web", "multi_tenancy"]
    - "saas_product": ["web", "multi_tenancy", "billing"]

  ARCHETYPE_QUEUE_CATEGORIES: dict[str, list[str]] — per §27.3
    Mapping of archetype → default queue categories.

  PROFILE_FILES: dict[str, list[str]] — files each profile requires
    Mapping of profile name → list of files to create when profile is enabled.

FUNCTIONS:

  parse_archetype(idea_content: str) -> str:
    PURPOSE: Extract the selected archetype from idea.md §3.
    STEPS:
      1. Find the archetype table section
      2. Find the row with `[x]` checkbox
      3. Extract the archetype name (first column)
    RETURNS: str archetype name (normalized, e.g., "api_service")
    RAISES: ValueError if no archetype or multiple archetypes selected

  parse_profile_overrides(idea_content: str) -> dict[str, bool]:
    PURPOSE: Extract explicit profile enable/disable selections from idea.md §5.
    STEPS:
      1. Find the profile selection table
      2. For each row: parse "yes" or "no" from the Enable? column
    RETURNS: dict[profile_name, enabled_bool]

  parse_bounded_contexts(idea_content: str) -> list[str]:
    PURPOSE: Extract bounded context names from idea.md §4.2.
    STEPS:
      1. Find the bounded contexts table
      2. Extract context name from first column of each row
      3. Normalize to Python module names (lowercase, underscores)
    RETURNS: list[str] of context names

  build_plan(
    archetype: str,
    profile_overrides: dict[str, bool],
    contexts: list[str]
  ) -> InitializationPlan:
    PURPOSE: Build the complete initialization plan.
    STEPS:
      1. Start with archetype default profiles from ARCHETYPE_PROFILES
      2. Apply profile overrides from idea.md §5
      3. Expand profile dependencies (billing requires auth)
      4. Get queue categories from ARCHETYPE_QUEUE_CATEGORIES
      5. List module files for each context (from templates)
      6. List profile files for each enabled profile
      7. List files to modify (main.py, docker-compose.yml, .env.example, etc.)
    RETURNS: InitializationPlan

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: idea_path, --output (json file or stdout)
      2. Read idea.md
      3. Parse archetype, overrides, contexts
      4. Build plan
      5. Serialize to JSON and write to output

DESIGN DECISIONS:
- Profile overrides from idea.md §5 always win over archetype defaults
- Profile dependency expansion: billing → requires auth; multi_tenancy → requires auth
- Context names are normalized to valid Python identifiers
- Output JSON is the authoritative initialization plan used by downstream tools
"""
