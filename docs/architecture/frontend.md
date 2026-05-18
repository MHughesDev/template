---
doc_id: "2.17"
title: "frontend"
section: "Architecture"
status: "pending-init"
summary: "Frontend architecture: page/route inventory, component hierarchy, API integration, state management. Populated during initialization from IDEA.md §11."
updated: "2026-05-17"
---

# Frontend Architecture
<!-- derived from: IDEA.md §11 — populated by repo_initialize -->

## Page/route inventory

| Route | Purpose | Auth required |
|-------|---------|---------------|
| `/` | _[Landing/dashboard]_ | _[Yes/No]_ |
| `/login` | _[Authentication]_ | _[No]_ |
| `/dashboard` | _[Main app view]_ | _[Yes]_ |

## Component hierarchy

```
App
├── Layout
│   ├── Header
│   ├── Sidebar
│   └── Footer
├── Pages
│   ├── Dashboard
│   └── Settings
└── Shared
    ├── Button
    └── Modal
```

## State management

_[e.g., TanStack Query for server state, Zustand for client state]_

_[This section is populated by `skills/init/repo_initialize.md` during repository initialization.]_
