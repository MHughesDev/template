---
doc_id: "5.34"
title: "code review"
section: "Procedures"
summary: "Review code changes for quality, security, correctness, and adherence to standards."
status: "accepted"
updated: "2026-05-17"
---

# 5.34 — Code Review

**Purpose:** Review code changes thoroughly before merge.

**When to use:**
- PR submitted for review
- Review requested by author
- Spot-checking AI-generated code

**Review types:**
- **Light:** Typos, obvious issues (< 5 min)
- **Standard:** Full review (10-30 min)
- **Deep:** Complex changes, security-sensitive (30+ min)

---

## Prerequisites

- [ ] PR description clear
- [ ] Tests included
- [ ] CI passing
- [ ] Scope appropriate

---

## Steps

### 1. Understand context

Read:
- PR description
- Linked issues/tickets
- Acceptance criteria
- Changed files overview

### 2. High-level review

Check:
- [ ] Right files changed
- [ ] No scope creep
- [ ] Architecture consistent
- [ ] API contracts maintained

### 3. Detailed review

**Security:**
- [ ] No secrets in code
- [ ] Input validated
- [ ] Auth checks present
- [ ] SQL injection prevented
- [ ] XSS prevented

**Correctness:**
- [ ] Logic correct
- [ ] Edge cases handled
- [ ] Error paths covered
- [ ] Race conditions checked

**Quality:**
- [ ] Tests adequate
- [ ] Naming clear
- [ ] Comments where needed
- [ ] Complexity reasonable

**Standards:**
- [ ] Style guide followed
- [ ] Type hints present
- [ ] Docstrings added

### 4. Test verification

```bash
# Pull branch
git fetch origin pull/XXX/head:pr-XXX
git checkout pr-XXX

# Run tests
make test

# Manual testing if needed
make dev
# Test affected feature
```

### 5. Provide feedback

**Approach:**
- Be specific
- Explain why
- Suggest fixes
- Distinguish nitpick from blocker

**Comment format:**
```
**Issue:** {what's wrong}
**Why:** {impact}
**Suggestion:** {fix}
**Priority:** {blocker/warning/nitpick}
```

### 6. Decision

| Action | When |
|--------|------|
| **Approve** | No blockers, minor issues optional |
| **Request changes** | Blockers found |
| **Comment** | Questions, not ready to decide |

### 7. Follow-up

If changes requested:
- Re-review after fixes
- Verify blockers resolved
- Check no new issues introduced

---

## Review Checklist

**Every PR:**
- [ ] Security scan passed
- [ ] Tests pass
- [ ] Lint/typecheck pass
- [ ] PR size reasonable (< 500 lines ideal)
- [ ] Commit messages clear

**Feature PRs:**
- [ ] Tests for new code
- [ ] Docs updated
- [ ] API changes documented

**Bugfix PRs:**
- [ ] Regression test added
- [ ] Root cause explained

---

## Common Issues

| Issue | Resolution |
|-------|------------|
| Too large | Request split into smaller PRs |
| No tests | Request test coverage |
| Unclear purpose | Request better description |
| Scope creep | Request remove unrelated changes |

---

## See Also

- PR audit: `docs/agents/pr-audit-checklist.md`
- Reviewing AI diffs: `docs/agents/reviewing-ai-diffs.md`
- Git workflow: `docs/development/git-workflow.md`
