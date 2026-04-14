# skills/init/profile-resolver.py
"""

PURPOSE:
Resolves the final set of enabled profiles from archetype defaults and idea.md §5
explicit selections. Validates profile dependencies (billing requires auth +
multi_tenancy), detects conflicts, and produces the authoritative enabled profile
set for the initialization procedure.

DEPENDS ON:
- pathlib (stdlib) — file reading
- re (stdlib) — parse idea.md profile table
- json (stdlib) — output serialization
- argparse (stdlib) — CLI

DEPENDED ON BY:
- skills/init/profile-resolver.md — references as machinery
- skills/init/archetype-mapper.py — may import ARCHETYPE_PROFILES constant

CLASSES:

  ProfileResolutionResult:
    PURPOSE: Result of profile resolution.
    FIELDS:
      - enabled: list[str] — final set of enabled profile names
      - disabled: list[str] — explicitly disabled profiles
      - implicitly_enabled: list[str] — profiles enabled as dependencies of other profiles
      - warnings: list[str] — non-blocking issues (e.g., implicit enablement)
      - errors: list[str] — blocking conflicts that prevent resolution
    NOTES: If errors is non-empty, initialization should stop and human must fix idea.md.

CONSTANTS:

  PROFILE_DEPENDENCIES: dict[str, list[str]]
    Profiles that require other profiles to be enabled:
    - "billing": ["auth", "multi_tenancy"]  — billing needs tenant isolation
    - "workers": []  — independent
    - "ai_rag": []  — independent
    - "web": []  — independent
    - "mobile": []  — independent
    - "multi_tenancy": ["auth"]  — tenancy needs auth
    - "scheduled_jobs": ["workers"]  — scheduled jobs need broker infrastructure

  PROFILE_CONFLICTS: list[tuple[str, str]]
    Pairs of profiles that conflict with each other:
    - Currently none — all profiles are designed to coexist

FUNCTIONS:

  parse_profile_selections(idea_content: str) -> dict[str, bool | None]:
    PURPOSE: Parse profile enable/disable selections from idea.md §5.
    STEPS:
      1. Find ## 5. Profile selection section
      2. Parse table rows: profile name → "yes"/"no" (or None if not filled)
    RETURNS: dict[profile_name, enabled] — None means not explicitly set

  resolve_profiles(
    archetype_defaults: list[str],
    explicit_selections: dict[str, bool | None]
  ) -> ProfileResolutionResult:
    PURPOSE: Resolve final profile set from defaults and explicit selections.
    STEPS:
      1. Start with archetype_defaults as the base enabled set
      2. Apply explicit overrides from idea.md §5 (yes/no override defaults)
      3. Expand dependencies: for each enabled profile, enable its dependencies
      4. Check for conflicts in the resolved set
      5. Build ProfileResolutionResult
    RETURNS: ProfileResolutionResult

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: idea_path, --archetype-defaults (JSON list or via archetype-mapper)
      2. Parse idea.md profile selections
      3. Resolve profiles
      4. Print result as JSON
      5. Exit 1 if any errors in resolution

DESIGN DECISIONS:
- Archetype defaults loaded from ARCHETYPE_PROFILES in archetype-mapper.py constants
- Explicit yes in idea.md §5 always wins (enables regardless of archetype default)
- Explicit no in idea.md §5 always wins (disables regardless of archetype default)
- Implicit enablement (dependency) is reported as warning for human awareness
- Profile names use underscore convention: multi_tenancy, ai_rag, etc.
"""
