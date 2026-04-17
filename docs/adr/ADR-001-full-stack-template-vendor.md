---
doc_id: "7.2"
title: "ADR-001 full-stack template vendor baseline"
section: "ADR"
summary: "Accepted: mechanical import from MHughesDev/fastapi-template with SHA pin; bulk-copy frontend; port backend into apps/api contexts."
updated: "2026-04-17"
---

# 7.2 — ADR-001: Full-stack template vendor baseline

**Status:** Accepted

**Date:** 2026-04-17

## 7.2.1 Context

This repository is an **agent-operated software factory** with its own FastAPI layout (`apps/api/src/`), tenancy, queue, and docs. We also want feature parity with the **full-stack FastAPI template** ecosystem (Vite frontend, compose, SMTP-backed flows, etc.). Regenerating that stack with an LLM is brittle and wastes tokens; **provenance** from a known git remote is required.

## 7.2.2 Decision

1. **Vendor remote:** Use fork `https://github.com/MHughesDev/fastapi-template.git`, default branch `master`, pinned at commit **`13652b51ea0acca7dfe243ac25e2bbdc066f3c4f`** (record updates when the pin moves).
2. **Upstream reference:** Treat `https://github.com/fastapi/full-stack-fastapi-template` as the conceptual upstream for behavior and layout comparisons.
3. **Frontend:** **Bulk-copy** the `frontend/` tree from a checkout of the pin into `apps/web/` (mechanical rsync/cp), then minimal config patches only.
4. **Backend:** **Do not** replace `apps/api/` with the template backend. **Port** features by reading/copying from the vendor `backend/` tree into existing bounded contexts under `apps/api/src/`.
5. **Automation:** A vendor sync script and Make target (queue **Q-005**) will wrap `git clone` / `git fetch` and `rsync` with safety flags (e.g. no overwrite of `apps/api` unless explicitly forced).

## 7.2.3 Consequences

- **Easier:** Reproducible imports, clear SHA audit trail, alignment with a known FastAPI full-stack baseline.
- **Harder:** Merge work for Compose, CI, and settings; ongoing resync when the pin advances.
- **Risks accepted:** Drift between vendor pin and upstream; mitigated by documenting the pin and re-baselining deliberately.

## 7.2.4 Alternatives considered

| Alternative | Rejected because |
|-------------|------------------|
| Replace `apps/api` entirely with template `backend/` | Would discard modular monolith, tenancy, and factory-specific modules. |
| AI-generate equivalent frontend/backend from scratch | Loses provenance and duplicates known-good template code. |
| Depend on Copier for this repo’s init | Factory uses `idea.md` and internal orchestration; Copier is not the source of truth here. |

## 7.2.5 References

- [docs/integrations/full-stack-fastapi-template.md](../integrations/full-stack-fastapi-template.md)
- Upstream: [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template)
- Fork: [MHughesDev/fastapi-template](https://github.com/MHughesDev/fastapi-template)
- `queue/queue.csv` — Q-004 through Q-013 integration plan
