# Documentation numbering plan

## Discovery

### `find` inventory

Saved at [.evidence/docs-map/find-output.txt](find-output.txt) (108 files before `DOCS_MAP.md` exists; current tree has 109 `.md` files under `docs/` excluding the not-yet-created map).

### Section ordering

Canonical directories present under `docs/`, in required order:

1. `getting-started/`
2. `architecture/`
3. `development/`
4. `api/`
5. `procedures/`
6. `operations/`
7. `adr/`

Additional top-level directories, alphabetically after the canonical list:

8. `agents/`
9. `optional-clients/`
10. `prompts/`
11. `quality/`
12. `queue/`
13. `release/`
14. `repo-governance/`
15. `runbooks/`
16. `security/`
17. `troubleshooting/`

**Root-level markdown** (`docs/README.md`, `docs/glossary.md`): assigned to **section 18**. `docs/README.md` is **18.0** (hub README). `docs/glossary.md` is **18.1**. This matches the rule that a section README uses `N.0`; the docs hub has no containing folder, so the root hub file takes `18.0`.

**Deviation note:** `docs/queue/` has **no** `README.md`. Files are ordered alphabetically and numbered **12.1–12.3** (no **12.0**), so IDs stay contiguous within the section. Same pattern would apply to any future folder without a README.

### Ambiguities / flags

| File | Note |
|------|------|
| `docs/api/endpoints.md`, `docs/development/environment-vars.md` | Marked as generated or sourced from OpenAPI / Settings in comments. Heading order is stable enough to number; **no file left unmodified**. |
| `docs/development/init-manifest-schema.md`, some procedures | First body heading is `## Overview` or `## Purpose` rather than a `**Purpose:**` pseudo-heading; summaries were taken from the first substantive paragraph or `## Purpose` body. |

No duplicate docs, no deletes, no section over 50 files (largest: `docs/procedures/` with 27 files).

### Estimated modifications

| Category | Count |
|----------|------:|
| Markdown files under `docs/` with stable `doc_id` (excl. `DOCS_MAP.md`, excl. `docs/generated/*`) | 109 |
| New `docs/DOCS_MAP.md` | 1 |
| New `scripts/check_docs_map.py` | 1 |
| `Makefile` (one target) | 1 |
| `README.md` (one table row) | 1 |
| Evidence / plan | 2 |

**Machine-generated:** `docs/generated/*.md` is produced by `make docs:generate`, listed in `DOCS_MAP.md` §0.5, and **excluded** from `doc_id` frontmatter so `make docs:check` stays green.

**Total indexed with stable IDs:** 109 + map (`doc_id` `0`) = 110 rows in the numbered index.

---

## Full inventory (proposed `doc_id`)

| doc_id | Path |
|--------|------|
| 1.0 | docs/getting-started/README.md |
| 1.1 | docs/getting-started/prerequisites.md |
| 1.2 | docs/getting-started/quickstart.md |
| 2.0 | docs/architecture/README.md |
| 2.1 | docs/architecture/ai-rag-chromadb.md |
| 2.2 | docs/architecture/api-design.md |
| 2.3 | docs/architecture/auth-multi-tenancy.md |
| 2.4 | docs/architecture/data-layer.md |
| 2.5 | docs/architecture/diagrams/README.md |
| 2.6 | docs/architecture/domain-model.md |
| 2.7 | docs/architecture/error-handling.md |
| 2.8 | docs/architecture/modular-monolith.md |
| 2.9 | docs/architecture/system-context.md |
| 3.0 | docs/development/README.md |
| 3.1 | docs/development/coding-standards.md |
| 3.2 | docs/development/dependency-management.md |
| 3.3 | docs/development/docs-generation.md |
| 3.4 | docs/development/environment-vars.md |
| 3.5 | docs/development/git-workflow.md |
| 3.6 | docs/development/init-manifest-schema.md |
| 3.7 | docs/development/local-setup.md |
| 3.8 | docs/development/module-patterns.md |
| 3.9 | docs/development/testing-guide.md |
| 4.0 | docs/api/README.md |
| 4.1 | docs/api/endpoints.md |
| 4.2 | docs/api/error-codes.md |
| 5.0 | docs/procedures/README.md |
| 5.1 | docs/procedures/add-make-target.md |
| 5.2 | docs/procedures/add-mcp-tool.md |
| 5.3 | docs/procedures/add-optional-app-profile.md |
| 5.4 | docs/procedures/add-prompt-template.md |
| 5.5 | docs/procedures/add-queue-category.md |
| 5.6 | docs/procedures/archive-queue-item.md |
| 5.7 | docs/procedures/database-migration.md |
| 5.8 | docs/procedures/dependency-upgrade.md |
| 5.9 | docs/procedures/enable-profile.md |
| 5.10 | docs/procedures/extract-service-from-monolith.md |
| 5.11 | docs/procedures/handle-blocked-work.md |
| 5.12 | docs/procedures/handoff.md |
| 5.13 | docs/procedures/implement-change.md |
| 5.14 | docs/procedures/incident-rollback.md |
| 5.15 | docs/procedures/initialize-from-idea.md |
| 5.16 | docs/procedures/initialize-repo.md |
| 5.17 | docs/procedures/open-pull-request.md |
| 5.18 | docs/procedures/plan-change.md |
| 5.19 | docs/procedures/release-preparation.md |
| 5.20 | docs/procedures/scaffold-domain-module.md |
| 5.21 | docs/procedures/start-queue-item.md |
| 5.22 | docs/procedures/update-documentation.md |
| 5.23 | docs/procedures/update-or-create-rule.md |
| 5.24 | docs/procedures/update-or-create-skill.md |
| 5.25 | docs/procedures/validate-change.md |
| 5.26 | docs/procedures/validate-idea-md.md |
| 6.0 | docs/operations/README.md |
| 6.1 | docs/operations/backups.md |
| 6.2 | docs/operations/configuration.md |
| 6.3 | docs/operations/database-operations.md |
| 6.4 | docs/operations/docker.md |
| 6.5 | docs/operations/health-checks.md |
| 6.6 | docs/operations/kubernetes.md |
| 6.7 | docs/operations/observability.md |
| 6.8 | docs/operations/rollback.md |
| 6.9 | docs/operations/scaling.md |
| 7.0 | docs/adr/README.md |
| 7.1 | docs/adr/template.md |
| 8.0 | docs/agents/README.md |
| 8.1 | docs/agents/evolving-from-incidents.md |
| 8.2 | docs/agents/initialization-guide.md |
| 8.3 | docs/agents/pr-audit-checklist.md |
| 8.4 | docs/agents/quality-ratcheting.md |
| 8.5 | docs/agents/reviewing-ai-diffs.md |
| 8.6 | docs/agents/supervision-guide.md |
| 9.1 | docs/optional-clients/mobile.md |
| 9.2 | docs/optional-clients/web.md |
| 10.0 | docs/prompts/README.md |
| 10.1 | docs/prompts/conventions.md |
| 10.2 | docs/prompts/index.md |
| 11.0 | docs/quality/README.md |
| 11.1 | docs/quality/coverage-policy.md |
| 11.2 | docs/quality/flake-policy.md |
| 11.3 | docs/quality/testing-strategy.md |
| 12.1 | docs/queue/queue-categories.md |
| 12.2 | docs/queue/queue-intelligence.md |
| 12.3 | docs/queue/queue-system-overview.md |
| 13.0 | docs/release/README.md |
| 13.1 | docs/release/changelog-guide.md |
| 13.2 | docs/release/promotion.md |
| 13.3 | docs/release/versioning.md |
| 14.0 | docs/repo-governance/README.md |
| 14.1 | docs/repo-governance/audits.md |
| 14.2 | docs/repo-governance/documentation-freshness.md |
| 14.3 | docs/repo-governance/improvement-loops.md |
| 14.4 | docs/repo-governance/procedure-drift-detection.md |
| 15.0 | docs/runbooks/README.md |
| 15.1 | docs/runbooks/api-down.md |
| 15.2 | docs/runbooks/chroma-unavailable.md |
| 15.3 | docs/runbooks/db-failure.md |
| 15.4 | docs/runbooks/jwt-key-rotation.md |
| 16.0 | docs/security/README.md |
| 16.1 | docs/security/accepted-risks.md |
| 16.2 | docs/security/cors-policy.md |
| 16.3 | docs/security/incident-response.md |
| 16.4 | docs/security/secrets-management.md |
| 16.5 | docs/security/threat-model-stub.md |
| 16.6 | docs/security/token-lifecycle.md |
| 17.0 | docs/troubleshooting/README.md |
| 17.1 | docs/troubleshooting/common-issues.md |
| 18.0 | docs/README.md |
| 18.1 | docs/glossary.md |

---

## Definition of done (task)

- [ ] `docs/DOCS_MAP.md` created with structure from prompt §`docs/DOCS_MAP.md specification`
- [ ] Every `docs/**/*.md` except `DOCS_MAP.md` has YAML frontmatter and updated H1 / H2 prefixes per scheme
- [ ] `scripts/check_docs_map.py` + `make docs:map-check`
- [ ] `README.md` Key resources row for `docs/DOCS_MAP.md`
- [ ] `make lint`, `fmt-check`, `typecheck`, `test`, `docs:check`, `docs:map-check` pass
