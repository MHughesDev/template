# Open Questions

A living register of questions the system has not yet resolved. This is not a scratchpad —
it is the durable record of every consequential fork the project has faced, how it was decided,
and what evidence decided it.

## When to add an entry

Add an open question **whenever you compare important parts of the system or weigh trade-offs
between variations** — choosing a data store, an API to integrate, a pattern, a boundary between
components. If a decision is worth making deliberately, the question behind it is worth recording here.

## How entries move

1. **Open** — the question is raised. Record the options on the table and what would decide between them.
2. **Researching** — a research brief is underway (link it).
3. **Resolved** — the question is answered. Record the answer, the evidence that settled it, and the
   ADR or spec that now carries the decision.

Never delete a resolved question. The point of this file is that six months from now, anyone can see
not just *what* was decided but *why*, and which alternatives were already ruled out.

---

## Register

| ID | Question | Status | Options Weighed | Resolution | Evidence / Links |
|----|----------|--------|-----------------|------------|------------------|
| Q-1 | *(example — delete)* Which auth provider fits a multi-tenant B2B app with a 2-person team? | Resolved | Auth0 vs. Clerk vs. custom JWT | Clerk | [research/example-auth-provider-comparison.md](./research/example-auth-provider-comparison.md) → [adr/0001-example-use-clerk-for-auth.md](./adr/0001-example-use-clerk-for-auth.md) |

> Replace the example row. Number questions sequentially: `Q-1`, `Q-2`, …

---

## Entry Detail (optional)

For questions that need more than a table row, add a section below. Keep the table as the index.

### Q-1: [Question]

**Status:** Open | Researching | Resolved
**Raised:** YYYY-MM-DD

**Why it matters:** [What part of the system this affects and what's at stake in getting it wrong.]

**Options weighed:**
- Option A — [trade-off]
- Option B — [trade-off]

**What would decide it:** [The evidence, benchmark, or constraint that resolves this.]

**Resolution:** [Filled in when resolved — the answer, and the research/ADR that carries it.]
