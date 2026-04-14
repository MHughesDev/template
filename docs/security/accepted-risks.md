# docs/security/accepted-risks.md

<!-- CROSS-REFERENCES -->
<!-- - Referenced by: docs/security/README.md, AGENTS.md §11 (Escalation) -->

**Purpose:** Accepted CVEs and review dates; links to dependency audit.

## Overview

Accepted CVEs and review dates; links to dependency audit. See [AGENTS.md](../../AGENTS.md) for validation commands and [spec/spec.md](../../spec/spec.md) for the full specification.

## Accepted findings

| CVE / ID | Component | Rationale | Review |
|----------|-----------|-----------|--------|
| [CVE-2024-23342](https://github.com/advisories/GHSA-wj6h-64fc-37mp) | PyPI `ecdsa` (transitive via `python-jose`) | Minerva timing issue in pure-Python ECC; upstream does not treat side-channel attacks as in scope and there is no patched release that satisfies scanners. JWT verification paths used here do not rely on `ecdsa` signing APIs. Prefer migrating off `python-jose` / auditing transitive crypto in a future hardening pass. | 2026-04-14 |
