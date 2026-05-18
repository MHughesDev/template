# Idea Definition — Project Intake Form

> **Purpose.** `idea.md` is the single human-authored input that drives repository initialization. It is a **product-intake contract**, not a brief. The AI agent that initializes this repository (see [skills/init/repo_initialize.md](skills/init/repo_initialize.md)) treats every section below as **user intent** — what you say here becomes the project's spec, docs, and initial queue.
>
> **How to use.**
> 1. Fill out every applicable section end-to-end. Do not skip sections.
> 2. Mark inapplicable sections with `N/A` and a one-line reason. Do not leave blanks.
> 3. Mark unresolved items in **§19 Open questions** — the initializer will turn each open question into a blocked queue row or open-questions doc entry, not silently invent an answer.
> 4. Once filled out, ask an AI agent to run **`skills/init/repo_initialize.md`**. Do not invoke any `make idea:*` target — that workflow no longer exists.
>
> **Need help filling this out?** If you have source material (a PRD, design notes, a brainstorm doc, or just a free-form prompt) instead of a fully-formed product description, ask an AI agent to run **[`skills/init/idea_author.md`](skills/init/idea_author.md)** first. It will read your input, ask focused clarifying questions where the input is silent, and fill out this file. It will not invent product decisions — unresolved items become entries in §19 below.
>
> **Rules.**
> - Be specific. Vague answers become vague code.
> - Distinguish **intent** (what you want) from **implementation instruction** (how to build it). The initializer decides "how" — your job is "what" and "why."
> - The template assumes a working FastAPI + React baseline already exists under `apps/api/` and `apps/web/`. You do not need to design the baseline. You design the **product** that runs on top of it.

---

## 1. Product identity

| Field | Your answer |
|-------|-------------|
| Product name |  |
| One-sentence concept |  |
| Repository slug (e.g. `<owner>/<repo>`) |  |
| License (default: MIT) |  |

---

## 2. Target users

Describe who will use this product. Be specific about roles, not personas with names.

- **Primary user(s):**
- **Secondary user(s) (if any):**
- **Non-users (people who must not have access):**

---

## 3. Core problem

2–5 sentences. What pain exists today? Who feels it? What happens if it stays unsolved? If there is a current workaround, describe it.

>

---

## 4. MVP scope

The MVP is the smallest version of this product that is **shippable and usable** by the target users in §2. List 3–7 bullets. Each bullet must be:

- a user-visible capability (not an internal step), and
- independently testable (a reviewer can confirm it works without reading code).

Examples of good MVP bullets:
- "A registered user can create, list, and delete projects they own."
- "An admin can invite a new user via email; the invitee sets their password on first login."

Your MVP bullets:

1.
2.
3.

The initializer will use these bullets as the primary input for queue seeding. Order them by dependency: top bullet must work before subsequent bullets are meaningful.

---

## 5. Explicitly out of scope

Things this product will **not** do in initial scope. Be explicit — this is how the initializer avoids inventing features.

-
-
-

---

## 6. User stories

For each MVP bullet in §4, write 1–3 user stories in the format:

> As a `<role from §2>`, I want to `<capability>` so that `<outcome>`.

Group by role.

### 6.1 `<role>`

-

### 6.2 `<role>`

-

---

## 7. Core workflows

Describe the most important end-to-end flows in plain language. Step the user (or system) through each one. These become the basis of smoke tests and queue items.

### 7.1 `<workflow name>`

1.
2.
3.

### 7.2 `<workflow name>`

1.

---

## 8. Data and entities

List the primary domain entities. The initializer will turn these into SQLModel models, API resources, and Alembic migrations.

| Entity | Description (one sentence) | Key fields | Relationships |
|--------|---------------------------|------------|---------------|
|  |  |  |  |

Notes (cardinality, soft-delete needs, multi-tenancy ownership, derived fields):

>

---

## 9. Integrations

External systems this product depends on. Mark **required for MVP** vs **post-MVP**.

| Service | Direction | Purpose | MVP? |
|---------|-----------|---------|------|
|  | inbound / outbound |  | yes / no |

---

## 10. Authentication and permissions assumptions

| Field | Your answer |
|-------|-------------|
| Sign-up model (open, invite-only, SSO-only, …) |  |
| Roles (e.g. `user`, `admin`, `owner`) |  |
| Resource ownership rules (who can see/edit what) |  |
| Multi-tenancy (yes/no — if yes, isolation model in 1 line) |  |
| Session/token style (default: JWT access token) |  |

Note: the baseline ships JWT password auth with a single superuser. State here if your product needs more — SSO, invite-only, role gates, tenant scoping — and the initializer will queue the work.

---

## 11. Frontend expectations

| Field | Your answer |
|-------|-------------|
| Public surface (e.g. landing page, signup) |  |
| Authenticated surface (key screens / routes) |  |
| Mobile / responsive expectations |  |
| Design system (default: shadcn/ui + Tailwind v4 baseline) |  |
| Anything explicitly out-of-scope for the UI |  |

The baseline frontend (`apps/web/`) already includes login, signup, items CRUD, user settings, and an admin view. State here which of those to keep, repurpose, or replace.

---

## 12. Backend / API expectations

| Field | Your answer |
|-------|-------------|
| API style (default: REST + OpenAPI) |  |
| Versioning (default: `/api/v1/`) |  |
| Pagination style (default: offset; cursor where needed) |  |
| Rate limiting needs (yes/no, threshold) |  |
| Background work needs (yes/no, what kind) |  |

Key endpoints you can already name (path + method + one-sentence purpose):

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
|  |  |  |  |

---

## 13. Deployment expectations

| Field | Your answer |
|-------|-------------|
| Target environment(s) |  |
| Cloud provider / host |  |
| Domain & TLS plan |  |
| CI/CD beyond the default GitHub Actions |  |
| Observability (Sentry default; specify more if needed) |  |

---

## 14. Security and privacy constraints

| Field | Your answer |
|-------|-------------|
| Compliance regimes (GDPR, SOC2, HIPAA, PCI, none) |  |
| PII handled (yes/no — list categories) |  |
| Data retention policy |  |
| Data residency constraints |  |
| Secrets management approach |  |

Hard constraints (one per line; the initializer will lift these into `docs/security/`):

-

---

## 15. Testing expectations

| Field | Your answer |
|-------|-------------|
| Unit test depth (default: per service / per route) |  |
| Integration tests (default: per route group, real Postgres in CI) |  |
| End-to-end tests (default: Playwright on the React app) |  |
| Coverage floor (default: as configured in `pyproject.toml`) |  |
| Performance / load testing (yes/no, basic targets) |  |

---

## 16. Acceptance criteria for "initialized"

When this repository is considered initialized for this product, what must be true? These are the conditions an MVP-path queue row will be tested against.

-
-
-

---

## 17. Non-functional requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| Availability |  |  |
| Latency (p95) |  |  |
| Throughput |  |  |
| Scalability plan |  |  |
| Backup RPO / RTO |  |  |

---

## 18. Hard constraints

Things that absolutely must be true. The initializer treats these as inviolable and will refuse to design around them.

-
-

---

## 19. Open questions

List anything you are **unsure** about. The initializer will turn each open question into either:
- a blocked queue row (when execution depends on the answer), or
- an `docs/open-questions.md` entry (when only docs depend on the answer).

It will **not** silently choose an answer.

1.
2.

---

## 20. Additional context

Links, sketches, ERDs, design refs, competitor URLs, prior conversations.

>

---

**End of idea definition.**

> Once every applicable section above is filled out, ask an AI agent in this repo to run **`skills/init/repo_initialize.md`**. The skill is the single canonical initialization procedure — there is no `make idea:*` command.
