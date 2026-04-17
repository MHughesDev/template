<!-- .github/PULL_REQUEST_TEMPLATE.md -->
<!-- Per spec §26.7 item 202 -->

## Summary of Changes

<!-- One paragraph: what this PR does and why -->

## Agent onboarding (required)

- [ ] I read **[README.md](../README.md)** this session.
- [ ] I read **[AGENTS.md](../AGENTS.md)** this session (and again before merge if policy or handoff details apply).

## Queue Item ID (if applicable)

<!-- Queue ID: Q-XXX — link to queue row or queuearchive entry -->
Closes queue item: <!-- Q-XXX or N/A -->

## Files Changed

<!-- List of key files changed with one-line description each -->
| File | Change |
|------|--------|
| `path/to/file.py` | <!-- what changed --> |

## Commands Run (Evidence)

<!-- Paste the key output from validation commands — not full logs, just pass/fail and key lines -->

```
$ make lint
✓ No lint errors

$ make typecheck
✓ No type errors

$ make test
✓ 42 passed, 0 failed — coverage: 87%

$ make audit:self
✓ No BLOCKING findings
```

## Tests Added/Updated

<!-- List new or modified test functions -->
- [ ] `test_<unit>_<scenario>_<expected>` — added
- [ ] _(none — explain why)_

## Documentation Updated

<!-- Check all that apply -->
- [ ] `docs/api/endpoints.md` updated
- [ ] `.env.example` updated (new env var: `VAR_NAME`)
- [ ] `CHANGELOG.md` updated
- [ ] _(none required for this change)_

## Risks and Follow-ups

<!-- Residual risks discovered during implementation -->
- _(none)_

<!-- Follow-up items created -->
- New queue item: <!-- Q-XXX — link or description -->

## Checklist

- [ ] CI passing (all checks green)
- [ ] Acceptance criteria from queue item met
- [ ] No scope creep (all changes are in the planned file list)
- [ ] Docs updated where applicable
- [ ] Queue item archived (or link to archive step)
- [ ] After merge: delete this PR’s feature branch (remote and local per [AGENTS.md](../AGENTS.md) section 4)
