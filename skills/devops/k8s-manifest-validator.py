# skills/devops/k8s-manifest-validator.py
"""
BLUEPRINT: skills/devops/k8s-manifest-validator.py

PURPOSE:
Validates Kubernetes manifests beyond schema validation: checks resource
requests/limits present, probe configuration complete, securityContext set,
namespace consistency across manifests.

DEPENDS ON:
- pathlib (stdlib) — file discovery
- re (stdlib) — pattern matching
- argparse (stdlib) — CLI

DEPENDED ON BY:
- skills/devops/k8s-probes.md — references as machinery
- scripts/k8s-validate.sh — may call this

FUNCTIONS:

  load_manifest(manifest_path: Path) -> list[dict]:
    PURPOSE: Load a YAML manifest (potentially multi-document) into list of dicts.
    STEPS:
      1. Read file content
      2. Split on "---" document separator
      3. Parse each document as simple YAML (key:value without full PyYAML)
    RETURNS: list of manifest dicts

  check_deployment(manifest: dict) -> list[dict[str, str]]:
    PURPOSE: Validate a Deployment manifest.
    STEPS:
      1. Check containers have resource requests AND limits (CPU + memory)
      2. Check liveness probe configured
      3. Check readiness probe configured
      4. Check securityContext.runAsNonRoot = true
      5. Check securityContext.readOnlyRootFilesystem = true (recommended)
    RETURNS: list of finding dicts

  check_all_manifests(k8s_dir: Path) -> list[dict[str, str]]:
    PURPOSE: Validate all manifests in a Kustomize base or overlay directory.
    STEPS:
      1. Find all *.yaml files in k8s_dir
      2. Load each manifest
      3. Dispatch to appropriate check function by kind
    RETURNS: aggregated list of findings

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --k8s-dir (default deploy/k8s/base)
      2. Run validation
      3. Print report
      4. Exit 1 if any CRITICAL findings

DESIGN DECISIONS:
- Simple YAML parsing without PyYAML dependency for portability
- CRITICAL: missing resource limits (production safety)
- WARNING: missing readOnlyRootFilesystem (security recommendation)
"""
