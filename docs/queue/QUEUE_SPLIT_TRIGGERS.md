# Queue Split Triggers — Quick Reference

Before adding any row to `queue.csv`, run this checklist. If ANY item is
true, the row is L-complexity and must be split. See
`docs/procedures/queue-decomposition.md` for the full SOP.

---

## The Seven Triggers

| # | Trigger | Example |
|---|---|---|
| 1 | `touch_files` would exceed limit (S: >2, M: >3) | "I need to edit 4 files" |
| 2 | `goal` contains "and" for two distinct behaviors | "Add auth and add rate limiting" |
| 3 | Tests are a major deliverable alongside implementation | "Implement X and write tests" |
| 4 | A new package/dependency is required | "Add redis and use it in service" |
| 5 | Work crosses two or more feature/module boundaries | "Update UI and update API and update DB" |
| 6 | `acceptance_criteria` has more than 5 items | Count them |
| 7 | You cannot describe the output in one commit message | Try writing it — if it uses "and", split |

---

## Common Split Patterns

```
Interface → Implementation
  a: Define interface/schema/type (S, 1 file)
  b: Implement against it (S/M, ≤3 files)
  b.dependencies = [a]

Implementation → Tests
  a: Implement feature (S/M)
  b: Write tests (S, 1 test file)
  b.dependencies = [a]

Dependency → Consumer
  a: Add package to manifest (S, 2 files: manifest + lock)
  b: Wire consumer code (S/M)
  b.dependencies = [a]

Feature → Localization
  a: Build feature (M)
  b: Add i18n strings (S, 1–2 files)
  b.dependencies = [a]

Feature → Docs
  a: Implement (S/M)
  b: Update spec/docs (S, 1 doc file)
  b.dependencies = [a]
```

---

## ID Convention

Parent: `Q-042` (never enters queue)
Children: `Q-042a`, `Q-042b`, `Q-042c`
