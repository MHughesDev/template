# skills/devops/compose-profile-matrix.py
"""
BLUEPRINT: skills/devops/compose-profile-matrix.py

PURPOSE:
Tests Docker Compose profile combinations. Validates that each profile can be
enabled independently and in common combinations without port conflicts or
missing dependency services. Produces a compatibility matrix.
Optional per spec — recommended for projects with multiple profiles.

DEPENDS ON:
- subprocess (stdlib) — run docker compose commands
- json (stdlib) — parse docker compose config output
- pathlib (stdlib) — file paths
- argparse (stdlib) — CLI

DEPENDED ON BY:
- skills/devops/compose-profiles.md — references as machinery

FUNCTIONS:

  get_profiles(compose_path: Path = Path("docker-compose.yml")) -> list[str]:
    PURPOSE: Extract all profile names from docker-compose.yml.
    STEPS:
      1. subprocess.run(["docker", "compose", "config", "--profiles"])
      2. Parse output to extract profile names
    RETURNS: list[str] of profile names

  test_profile_combination(profiles: list[str]) -> dict:
    PURPOSE: Test that a specific profile combination is valid.
    STEPS:
      1. subprocess.run(["docker", "compose", "--profile", p for p in profiles, "config"])
      2. Check for port conflicts in output
      3. Check for missing depends_on services
      4. Return result dict: valid (bool), errors (list)
    RETURNS: dict with test results

  generate_compatibility_matrix(profiles: list[str]) -> dict[tuple, dict]:
    PURPOSE: Test all single-profile and common multi-profile combinations.
    STEPS:
      1. Test each profile alone
      2. Test common pairs (db+ai, db+worker, ai+worker)
      3. Test full combination (all profiles)
    RETURNS: dict mapping profile tuple → test result

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --compose-path, --format
      2. Get profiles
      3. Generate matrix
      4. Print results
      5. Exit 1 if any combination fails

DESIGN DECISIONS:
- Tests individual profiles first (baseline sanity)
- Only tests common combinations, not all 2^N permutations (impractical for many profiles)
- Requires Docker to be running (skips with warning if not available)
"""
