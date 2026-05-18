---
doc_id: "2.15"
title: "bounded contexts"
section: "Architecture"
status: "pending-init"
summary: "Per-context owns / does-not-own / exposes / consumes map; inter-context dependency diagram. Populated during initialization from IDEA.md §8."
updated: "2026-05-17"
---

# Bounded Contexts
<!-- derived from: IDEA.md §8 — populated by repo_initialize -->

_[Product name]_ is organized into the following bounded contexts:

## Context list

| Context | Owns | Exposes | Consumes |
|---------|------|---------|----------|
| _[Context 1]_ | _[Entities]_ | _[APIs/events]_ | _[Other contexts]_ |
| _[Context 2]_ | _[Entities]_ | _[APIs/events]_ | _[Other contexts]_ |

## Context map

```mermaid
flowchart TB
    subgraph Core["Core Domain"]
        C1[Context 1]
        C2[Context 2]
    end

    subgraph Supporting["Supporting Domains"]
        S1[Supporting 1]
        S2[Supporting 2]
    end

    C1 --> C2
    C1 --> S1
    S1 --> S2
```

_[Replace with actual context map showing relationships between bounded contexts.]_

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization.]_
