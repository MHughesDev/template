# .cursor/commands/audit.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Links to: skills/agent-ops/repo-self-audit.md, skills/agent-ops/repo-self-audit.py -->
<!-- - Make target: make audit:self -->

> PURPOSE: Reusable Cursor command for comprehensive repo self-audit. Runs all audit checks and surfaces findings for remediation. Per spec §28.9 item 338.

## Command Metadata

> CONTENT: Command metadata block. Fields:
> - name: "Repo Self-Audit"
> - description: "Run comprehensive repo self-audit: spec compliance, file inventory, skill format, prompt metadata, procedure structure, queue schema, Make target documentation, file title comments."
> - trigger: "Invoke before any PR, after major changes, or on cadence (weekly/monthly)"
> - prerequisites:
>   - .venv activated
>   - All services running (for smoke check portion)
> - linked_skill: skills/agent-ops/repo-self-audit.md
> - linked_machinery: skills/agent-ops/repo-self-audit.py
> - make_target: audit:self

## Steps

> CONTENT: Ordered execution steps:
> 1. Read skills/agent-ops/repo-self-audit.md completely
> 2. Run `make audit:self` which invokes scripts/audit-self.sh
> 3. Review audit report: identifies missing files, format violations, broken links
> 4. For each finding: categorize as BLOCKING (spec-required file missing) or WARNING (format issue)
> 5. BLOCKING findings must be resolved before any PR is merged
> 6. WARNING findings create new queue items or GitHub issues for later resolution
> 7. If all checks pass: include audit output in PR description as evidence

## Audit Checks Performed

> CONTENT: List of what the audit covers (populated from scripts/audit-self.sh and skills/agent-ops/repo-self-audit.py):
> - Inventory check: all spec §26 required files exist on disk
> - File title comment: all non-JSON files start with a path/title comment (§1.7)
> - Skill format: all skills have the §6.2 required section headings
> - Prompt metadata: all prompts have §7.2 YAML front matter fields
> - Procedure structure: all procedures have §8.3 required sections
> - Queue schema: queue.csv and queuearchive.csv have correct column headers
> - Make targets: all §10.2 catalog targets are present in Makefile
> - Documentation links: no broken internal links in docs/
> - Rules format: all .cursor/rules files have frontmatter
