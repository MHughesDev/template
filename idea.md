# Idea Definition — [Product Name]

> **Purpose.** `IDEA.md` is the single human-authored input that drives repository initialization. Fill out every applicable section below. The initialization skill ([`skills/init/repo_initialize.md`](skills/init/repo_initialize.md)) reads this file and produces design docs + MVP queue rows.
>
> For help completing this document, run [`skills/init/idea_author.md`](skills/init/idea_author.md).

---

## 1. Product identity

| Field | Your answer |
|-------|-------------|
| Product name | _[Name]_ |
| One-sentence concept | _[What does it do and for whom?]_ |
| Repository slug | _[e.g., myproduct]_ |
| License | _[e.g., MIT]_ |

---

## 2. Target users

- **Primary user(s):**
  - _[Who are they?]_
- **Secondary user(s):**
  - _[Who else might use it?]_
- **Non-users (must not have access):**
  - _[Who should be explicitly blocked?]_

---

## 3. Core problem

_[Describe the problem this product solves. 2-4 paragraphs.]_

---

## 4. Initial shippable scope (v1)

_[3–7 user-visible, testable capabilities. Each should be independently deliverable.]_

1. _[Capability 1]_
2. _[Capability 2]_
3. _[Capability 3]_

---

## 5. Explicitly out of scope

_[What this product will NOT do. Explicit non-goals prevent scope creep.]_

- _[Non-goal 1]_
- _[Non-goal 2]_

---

## 6. User stories

### 6.1 Primary user stories

- As a _[role]_, I want _[goal]_ so that _[benefit]_.

### 6.2 Secondary user stories

- As a _[role]_, I want _[goal]_ so that _[benefit]_.

---

## 7. Core workflows

### 7.1 Primary workflow

1. _[Step 1]_
2. _[Step 2]_
3. _[Step 3]_

### 7.2 Secondary workflow

1. _[Step 1]_
2. _[Step 2]_

---

## 8. Data and entities

_[Primary domain entities. Use a table format:]_

| Entity | Description | Key fields | Relationships |
|--------|-------------|------------|---------------|
| _[Entity1]_ | _[One sentence]_ | _[id, name, etc.]_ | _[has many X]_ |
| _[Entity2]_ | _[One sentence]_ | _[id, email, etc.]_ | _[belongs to Y]_ |

---

## 9. Integrations

_[Third-party services and APIs. Use a table:]_

| Service | Direction | Purpose | In v1? |
|---------|-----------|---------|--------|
| _[Service 1]_ | _[inbound/outbound]_ | _[Purpose]_ | _[yes/no]_ |
| _[Service 2]_ | _[inbound/outbound]_ | _[Purpose]_ | _[yes/no]_ |

---

## 10. Authentication and permissions assumptions

| Field | Your answer |
|-------|-------------|
| Sign-up model | _[How do users authenticate?]_ |
| Roles | _[What roles exist?]_ |
| Resource ownership rules | _[Who owns what?]_ |
| Multi-tenancy | _[Yes/No/Row-level/DB-per-tenant]_ |
| Session/token style | _[JWT/API keys/etc.]_ |

---

## 11. Frontend expectations

| Field | Your answer |
|-------|-------------|
| Public surface | _[Marketing site, landing pages, etc.]_ |
| Authenticated surface | _[Dashboards, admin panels, etc.]_ |
| Mobile / responsive | _[Mobile-first/desktop-only]_ |
| Design system | _[shadcn/ui, custom, etc.]_ |
| Anything explicitly out-of-scope | _[No mobile app, no marketing site, etc.]_ |

---

## 12. Backend / API expectations

| Field | Your answer |
|-------|-------------|
| API style | _[REST/gRPC/GraphQL]_ |
| Versioning | _[URL path/headers]_ |
| Pagination | _[Offset/cursor]_ |
| Rate limiting needs | _[Per-user/global/etc.]_ |
| Background work needs | _[Yes/No + type: Celery/Temporal/etc.]_ |

---

## 13. Deployment expectations

| Field | Your answer |
|-------|-------------|
| Target environment(s) | _[Local dev/staging/production]_ |
| Cloud provider / host | _[AWS/GCP/Azure/self-hosted]_ |
| Domain & TLS plan | _[Custom domain/subdomain]_ |
| CI/CD beyond default GitHub Actions | _[Special requirements?]_ |
| Observability | _[Sentry/Datadog/CloudWatch]_ |

---

## 14. Security and privacy constraints

| Field | Your answer |
|-------|-------------|
| Compliance regimes | _[GDPR/SOC2/PCI/etc. or None]_ |
| PII handled | _[What personal data is stored?]_ |
| Data retention policy | _[How long is data kept?]_ |
| Data residency | _[Regions/countries]_ |
| Secrets management | _[Vault/AWS Secrets Manager/etc.]_ |

**Hard constraints:**
- _[Any security mandates]_

---

## 15. Testing expectations

| Field | Your answer |
|-------|-------------|
| Unit test depth | _[What needs unit testing?]_ |
| Integration tests | _[External service mocks needed?]_ |
| End-to-end tests | _[Critical user flows to cover]_ |
| Coverage floor | _[Target percentage]_ |
| Performance / load | _[Any load testing requirements?]_ |

---

## 16. Acceptance criteria for "initialized"

_[When is initialization considered complete?]_

- _[Criteria 1: e.g., All design docs populated from IDEA.md]_
- _[Criteria 2: e.g., Initial MVP queue rows seeded]_
- _[Criteria 3: e.g., ADR created for any template-default overrides]_

---

## 17. Non-functional requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| Availability | _[e.g., 99.9%]_ | _[Notes]_ |
| Latency (p95) | _[e.g., <200ms]_ | _[Notes]_ |
| Throughput | _[e.g., 1000 req/s]_ | _[Notes]_ |
| Scalability plan | _[Vertical/horizontal]_ | _[Notes]_ |

---

## 18. Hard constraints

_[Non-negotiable technical or business constraints.]_

- _[Constraint 1]_
- _[Constraint 2]_

---

## 19. Open questions

_[Unresolved questions that would change architecture or implementation.]_

1. _[Question 1: e.g., "Which payment processor should we use?"]_
2. _[Question 2: e.g., "Do we need real-time updates or polling?"]_

---

## 20. Additional context

_[Research notes, links to PRDs, prior discussions, etc.]_

- _[Link or note 1]_
- _[Link or note 2]_

---

**End of idea definition.**

> Once every applicable section above is filled out, ask an AI agent in this repo to run **`skills/init/repo_initialize.md`**. The skill will produce: refreshed design docs under `docs/`, the initial queue with MVP rows in dependency order, and updated `AGENTS.md` scope references.
