---
doc_id: "20.0"
title: "Full-stack FastAPI template integration"
section: "Integrations"
summary: "Provenance of apps/api and apps/web (vendored from MHughesDev/fastapi-template), plus the mechanical re-sync workflow when advancing the vendor baseline."
updated: "2026-05-17"
---

# 20.0 — Full-stack FastAPI template integration

**Status:** the initial bulk import has **already been performed**. The contents of `apps/api/` (FastAPI + SQLModel + Postgres + Alembic) and `apps/web/` (React 19 + Vite + TanStack + Tailwind v4) come from `MHughesDev/fastapi-template`. This document is now the **re-sync contract** — how to advance the vendor baseline when the upstream fork is bumped.

**Purpose:** Document how to reproduce a **mechanical import or re-sync** from the forked full-stack template using **git and rsync only** — no AI-invented file trees.

## 20.0.1 Sources of truth

| Role | Remote | Default branch | Pinned commit (verify with `git rev-parse HEAD` after checkout) |
|------|--------|----------------|------------------------------------------------------------------|
| **Fork (vendor)** | `https://github.com/MHughesDev/fastapi-template.git` | `master` | `13652b51ea0acca7dfe243ac25e2bbdc066f3c4f` |
| **Upstream (reference)** | `https://github.com/fastapi/full-stack-fastapi-template` | (see upstream repo) | _(not pinned here — use when comparing behavior)_ |

Update the **Pinned commit** row when you intentionally advance the vendor baseline; always record the new SHA in git history and ADR notes.

## 20.0.2 Clone and pin (exact commands)

Pick a writable directory (examples use `/tmp/fastapi-template-vendor`). Replace the path if your policy forbids `/tmp`.

**Full clone and checkout at the pinned SHA:**

```bash
git clone https://github.com/MHughesDev/fastapi-template.git /tmp/fastapi-template-vendor
cd /tmp/fastapi-template-vendor
git checkout 13652b51ea0acca7dfe243ac25e2bbdc066f3c4f
git rev-parse HEAD
```

The last line must print `13652b51ea0acca7dfe243ac25e2bbdc066f3c4f` (or the SHA you deliberately updated to).

**Optional — sparse checkout before the first `git checkout` (reduces working tree size):**

```bash
git clone --no-checkout https://github.com/MHughesDev/fastapi-template.git /tmp/fastapi-template-vendor
cd /tmp/fastapi-template-vendor
git sparse-checkout init --cone
git sparse-checkout set frontend backend
git checkout 13652b51ea0acca7dfe243ac25e2bbdc066f3c4f
```

Adjust the `set` list if you need root files (for example `compose.yml`). Sparse checkout is optional; a full clone is always valid.

## 20.0.3 Inspect paths after clone (read-only)

After checkout, list what you will copy or read. Examples:

```bash
cd /tmp/fastapi-template-vendor
ls
ls frontend
ls backend
```

Use these listings to drive **rsync** / **cp** commands — do not assume paths without listing.

## 20.0.4 Copy commands (illustrative — target paths in *this* repo)

**Frontend bulk copy (typical later step; queue Q-006):** sync the template `frontend/` tree into this repository’s web app root (destructive to destination — review flags first):

```bash
rsync -a --delete /tmp/fastapi-template-vendor/frontend/ /path/to/this/repo/apps/web/
```

**Selective file copy (review before running):** copy Compose or docs from the vendor root without replacing this repo wholesale:

```bash
cp /tmp/fastapi-template-vendor/compose.yml /path/to/this/repo/review-compose.yml
```

Rename `review-compose.yml` to suit your merge workflow; merge into the repo’s canonical `docker-compose.yml` by hand (queue Q-009).

## 20.0.5 Copy-vs-port matrix

| Vendor path / topic | Treatment in this repo | Rationale |
|---------------------|------------------------|-----------|
| `frontend/` | **Bulk vendored** at `apps/web/` (current contents). On re-sync: rsync with explicit review. | Preserve Vite/React stack as-is; minimal patches only (proxy, env, codegen). |
| `backend/` (e.g. app under `backend/app`) | **Bulk vendored** at `apps/api/` (current contents — see `apps/api/app/`). On re-sync: review module changes carefully. | The systemization layer (docs/skills/queue/prompts) does not own application code; the upstream app is the working baseline. |
| `compose.yml`, `compose.override.yml`, `compose.traefik.yml` | **Bulk vendored** at repo root with `./backend` and `./frontend` paths rewritten to `./apps/api` and `./apps/web`. | Avoid discarding agent-factory services and profiles. |
| Root `package.json`, `bun.lock`, `uv.lock` | **Vendored** at repo root; `package.json` workspace updated to point at `apps/web`. | Required for bun + uv workspace tooling. |
| Root `README`, Copier, or generator metadata | **Reference only** | Initialization here is driven by `idea.md` and factory scripts, not Copier. |

## 20.0.6 Related documentation

- [ADR 001 — Full-stack template vendor baseline](../adr/ADR-001-full-stack-template-vendor.md)
- [AGENTS.md](../../AGENTS.md) — agent workflow and queue policy
- Queue items **Q-005** onward — vendor script, frontend sync, compose merge (see `queue/queue.csv`)

## 20.0.7 Out of scope for this document

Writing integration **code**, running production deploys, or modifying `apps/api` without a dedicated queue item and plan.
