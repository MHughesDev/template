# docs/repo-governance/procedure-drift-detection.md

<!-- Per spec §20 and §26.5 items 178-182 -->

**Purpose:** Detecting and fixing drift between documented procedures and the actual CI/operations reality.

## What is procedure drift?

**Procedure drift** occurs when a documented procedure describes steps that no longer match what the codebase, CI, or infrastructure actually does. Examples:

- A procedure says `make db:migrate` but that target was renamed to `make migrate`.
- A procedure references `scripts/deploy.sh` which was deleted.
- A procedure says to set `DATABASE_URL` but the app now reads `POSTGRES_DSN`.
- A procedure describes a manual approval step that CI now handles automatically.
- A CI workflow added a new required step that the procedure doesn't mention.

Drifted procedures cause agents and engineers to follow stale instructions — producing errors or, worse, silently wrong state.

## Detection methods

### 1. Automated link checking (`make docs:check`)

Catches broken file references. Run on every PR. See `docs/repo-governance/documentation-freshness.md` for details.

```bash
make docs:check
```

### 2. Makefile target audit

Check that every `make <target>` referenced in `docs/procedures/` still exists:

```bash
# List all make targets
grep -E '^[a-zA-Z0-9_:-]+:' Makefile | cut -d: -f1 | sort > /tmp/actual_targets.txt

# List all make references in procedures
grep -roh 'make [a-zA-Z0-9_:-]*' docs/procedures/ | awk '{print $2}' | sort -u > /tmp/doc_targets.txt

# Show targets mentioned in docs but missing from Makefile
comm -23 /tmp/doc_targets.txt /tmp/actual_targets.txt
```

### 3. Script path validation

Check that every script path mentioned in procedure docs exists:

```bash
grep -roh 'scripts/[a-zA-Z0-9_./\-]*\.py\|scripts/[a-zA-Z0-9_./\-]*\.sh' docs/procedures/ \
  | sort -u \
  | while read path; do
      [ -f "$path" ] || echo "MISSING: $path"
    done
```

### 4. Environment variable drift

Check that env vars referenced in docs exist in `.env.example`:

```bash
grep -roh '[A-Z_]\{3,\}' docs/procedures/ | sort -u > /tmp/doc_vars.txt
grep -oh '^[A-Z_]*=' .env.example | tr -d '=' | sort > /tmp/env_vars.txt
# Review /tmp/doc_vars.txt entries not in /tmp/env_vars.txt — some are expected, but investigate unfamiliar ones
```

### 5. CI workflow diff

When a `.github/workflows/` file changes, search for procedures that describe the workflow:

```bash
git diff --name-only HEAD~1 HEAD | grep '.github/workflows/'
# For each changed workflow, grep docs/ for its name and review
```

### 6. Quarterly procedure walk-through

Once per quarter, a human maintainer or on-call agent walks through each procedure in `docs/procedures/` step by step against the current codebase:

- Does step 1 still work?
- Does the output of step N match what step N+1 expects?
- Are there new required steps not in the procedure?

## Drift categories and severity

| Category | Example | Severity |
|----------|---------|----------|
| **Broken reference** | Script path no longer exists | High — procedure will fail mid-way |
| **Renamed target** | `make db:migrate` → `make migrate` | High — easy error, misleads agent |
| **Added required step** | New env var required before running | High — procedure will silently fail |
| **Removed manual step** | CI now handles what procedure says to do manually | Medium — safe but confusing |
| **Changed output format** | Script output parsing instructions are wrong | Medium — downstream steps may break |
| **Outdated context** | Architectural description no longer accurate | Low — misleads understanding only |

## Remediation workflow

When drift is detected:

1. **Identify the gap** — what does the doc say vs. what the current code does?
2. **Check git log** — when did the code change? Who changed it?
3. **Update the procedure** — correct all stale steps, commands, and references.
4. **Add a test for the step** if the drift could have been caught automatically.
5. **Consider adding a `make docs:check` rule** if the type of drift is automatable.
6. **Open a queue item** if the remediation requires more than 30 minutes.

### Fast-path for target renames

When renaming a Makefile target:
1. Search `docs/` for the old target name: `grep -r "make old-target" docs/`
2. Update all references in the same PR as the rename.
3. Add the old target as a deprecated alias (prints a warning) for one sprint before removal.

```makefile
## old-target: DEPRECATED — use make new-target instead
old-target:
    @echo "WARNING: 'make old-target' is deprecated. Use 'make new-target'." >&2
    @$(MAKE) new-target
```

## Prevention

The best way to handle drift is to prevent it:

- **Update docs in the same PR as the code change.** PR template includes a docs checklist.
- **Add `make docs:check` to your PR pre-flight** (already runs in CI).
- **When removing a script**, grep `docs/` for references before deleting.
- **When renaming a target**, update all procedure references in the same commit.
- **Use stable target names** — prefer `make migrate` over `make db:migrate:run:now` to reduce surface area.

## Related

- `docs/repo-governance/documentation-freshness.md` — staleness indicators and `make docs:check`
- `docs/repo-governance/improvement-loops.md` — encoding drift findings into skills and rules
- `docs/repo-governance/audits.md` — `make audit:self` checks including `makefile_help`
