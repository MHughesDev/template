# docs/development/init-manifest-schema.md

## Overview

`init-manifest.json` is produced by `scripts/idea-parser.py` from structured fields in
`idea.md`. It is the **contract** for `scripts/init-from-idea.py` and for agents using
`prompts/repo_initializer.md`.

The manifest is **write-once per initialization** for a given project decision set. To
change profile decisions after init, update `idea.md`, delete `init-manifest.json`, set
INIT_META `initialized: false`, and re-run `make init:from-idea`.

## Top-level keys

| Key | Type | Description |
|-----|------|-------------|
| `meta` | object | Parser metadata (version, paths, timestamps, hash). |
| `project` | object | Identity fields from §1 (`project_name`, `display_name`, etc.). |
| `archetype` | string | Internal archetype key (e.g. `api_service`, `saas_product`). |
| `primary_database` | string | `sqlite` or `postgresql`. |
| `profiles` | array | Per-profile enablement and source (`explicit` vs `resolved_by_archetype`). |
| `bounded_contexts` | array | Rows from §4.2 (name, entities, description). |
| `resolved_decisions` | object | Flattened orchestration plan (see below). |

### `meta` sub-schema

| Key | Type | Description |
|-----|------|-------------|
| `init_version` | string | Engine version (e.g. `2.0`). |
| `idea_path` | string | Absolute or relative path parsed. |
| `parsed_at` | string | ISO-8601 timestamp. |
| `initialized` | boolean | Always `false` at parse time; orchestrator updates `idea.md` when done. |
| `init_manifest_hash` | string | SHA-256 of canonical JSON (without the hash field), hex digest. |

## `resolved_decisions` sub-schema

| Key | Type | Description |
|-----|------|-------------|
| `compose_services` | string[] | Logical Compose services (always includes `api`; may include `db`, `redis`, `worker`, `chroma`, `nginx`). |
| `python_dependencies` | string[] | PEP 508 dependency strings to ensure in `[project.dependencies]`. |
| `env_vars` | object | Key → placeholder value for `.env.example` / `.env`. |
| `modules_to_scaffold` | string[] | Snake_case module names under `apps/api/src/`. |
| `profiles_enabled` | string[] | Profile script stems to `source` (`enable-<stem>.sh`). |
| `profiles_discarded` | string[] | Profile script stems for `discard-<stem>.sh`. |
| `queue_seed_rows` | object[] | Rows matching `queue/queue.csv` columns. |
| `ci_additions` | string[] | Logical CI job names (e.g. `tenant_isolation_integration_test`). |
| `use_postgres` | boolean | True when PostgreSQL URL and deps are applied. |
| `archetype_resolved_fields` | string[] | Profile keys filled from archetype defaults (`[ ]` in §5). |
| `open_questions` | string[] | Non-blocking items from §16. |

## Example: `saas_product` with billing, email, workers

This annotated example illustrates typical keys; values are illustrative.

```json
{
  "meta": {
    "init_version": "2.0",
    "initialized": false,
    "init_manifest_hash": "…"
  },
  "project": {
    "project_name": "acme-saas",
    "display_name": "Acme SaaS",
    "one_line_pitch": "Multi-tenant B2B billing and onboarding.",
    "repository_slug": "acme/saas"
  },
  "archetype": "saas_product",
  "primary_database": "postgresql",
  "profiles": [],
  "bounded_contexts": [],
  "resolved_decisions": {
    "compose_services": ["api", "db", "redis", "worker", "nginx"],
    "python_dependencies": [
      "asyncpg",
      "celery[redis]",
      "redis",
      "sendgrid",
      "stripe"
    ],
    "env_vars": {
      "DATABASE_URL": "postgresql+asyncpg://user:password@localhost:5432/dbname",
      "CELERY_BROKER_URL": "redis://localhost:6379/0",
      "VITE_API_URL": "http://localhost:8000",
      "STRIPE_SECRET_KEY": "sk_test_REPLACE_ME"
    },
    "modules_to_scaffold": ["billing", "customers"],
    "profiles_enabled": ["web", "workers", "email", "billing"],
    "profiles_discarded": ["mobile", "ai-rag"],
    "queue_seed_rows": [],
    "ci_additions": ["tenant_isolation_integration_test"],
    "use_postgres": true,
    "archetype_resolved_fields": [],
    "open_questions": []
  }
}
```

## Reading order for agents

1. Read `meta.init_version` and `init_manifest_hash` for traceability.
2. Read `resolved_decisions` in full — **no inference from prose in `idea.md`** during execution.
3. Cross-check `open_questions` against the PR risk list.
