---
doc_id: "5.32"
title: "create skill"
section: "Procedures"
summary: "Create a new agent skill with proper structure, registration, and cross-references."
status: "accepted"
updated: "2026-05-17"
---

# 5.32 — Create Skill

**Purpose:** Create a new skill in `skills/` for agent use.

**When to use:**
- Workflow repeated twice (encode it)
- New tool integration needed
- Domain expertise not captured
- Agent capability gap identified

**When NOT to use:**
- One-off task (use queue)
- Simple command (use Makefile)
- Already exists (reference existing)

---

## Skill Structure

```
skills/{category}/
├── SKILL.md           # This skill
├── README.md          # (optional) Category readme
└── machinery/         # (optional) Scripts, templates
    ├── script.py
    └── template.j2
```

---

## Steps

### 1. Validate need

Check for existing:
```bash
grep -r "concept" skills/
make skills:list | grep -i "concept"
```

### 2. Choose category

| Category | Use For |
|----------|---------|
| `procedures/` | Doc/procedure creation |
| `backend/` | API development |
| `frontend/` | Web client |
| `mobile/` | Flutter mobile |
| `testing/` | Test writing |
| `security/` | Security reviews |
| `repo-governance/` | Repo maintenance |

### 3. Name the skill

Format: `skills/{category}/{kebab-name}/SKILL.md`

Rules:
- Kebab-case
- Verb-noun format (e.g., `add-procedure`, `write-tests`)
- Clear purpose from name

### 4. Create SKILL.md

Template:
```markdown
# {Title}

{One-sentence description}

## When to invoke

- Situation 1
- Situation 2

## When NOT to invoke

- Situation to avoid

## Procedure

### 1. Step one
Details...

### 2. Step two
Details...

## Validation

Checklist...

## See Also

- Related skill
- Related procedure
```

### 5. Add machinery (if needed)

If skill needs automation:
```bash
mkdir skills/{category}/{name}/machinery/
# Add scripts, templates, configs
```

### 6. Register skill

Edit `skills/README.md`:
```markdown
## {Category}

- [{Title}]({category}/{name}/SKILL.md) - {description}
```

### 7. Create cross-references

Reference from:
- Related skills
- Procedures that use this skill
- Prompts that invoke this skill

### 8. Test skill

Simulate invocation:
```
Human: "Do {skill purpose}"
→ Agent should read SKILL.md
→ Follow procedure
→ Produce correct output
```

---

## Validation

- [ ] SKILL.md exists
- [ ] When to invoke clear
- [ ] When NOT to invoke clear
- [ ] Procedure actionable
- [ ] Registered in skills/README
- [ ] Cross-references added

---

## See Also

- Skill index: `skills/README.md`
- Add procedure: `docs/procedures/add-procedure.md`
- Update skill: `docs/procedures/update-or-create-skill.md`
