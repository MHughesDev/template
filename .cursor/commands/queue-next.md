# .cursor/commands/queue-next.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- CROSS-REFERENCES -->
<!-- - Links to: docs/procedures/start-queue-item.md, queue/QUEUE_INSTRUCTIONS.md -->
<!-- - Make targets: queue:peek, queue:validate -->

> PURPOSE: Optional reusable Cursor command to claim and begin processing the next queue item. Guides the agent through reading the queue, checking readiness, creating a branch, and beginning work. Per spec §26.2 item 18.

## Command Metadata

> CONTENT: Command metadata block. Fields:
> - name: "Queue Next"
> - description: "Claim and begin processing the next ready queue item. Reads top row, checks dependencies, creates branch, reads linked docs, confirms understanding."
> - trigger: "When ready to start new queue work. Use after previous item is archived."
> - linked_procedure: docs/procedures/start-queue-item.md
> - linked_skill: skills/agent-ops/queue-triage.md

## Steps

> CONTENT: Ordered steps:
> 1. Run `make queue:peek` — read the current top row of queue.csv
> 2. Read the COMPLETE summary column of the top row — this is the contract
> 3. Check dependencies: verify all listed dependency IDs appear in queuearchive.csv with status=done
> 4. If dependencies not met: document in notes column as `blocked_by: [Q-XXX, ...]` and STOP
> 5. Run `make queue:validate` to ensure queue integrity before starting
> 6. Create branch: `git checkout -b queue/<id>-short-slug`
> 7. Read all files referenced in the summary
> 8. Run mandatory skill search: `make skills:list` → find relevant skills → read them in full
> 9. Produce a plan: files to change, acceptance criteria, risks, scope bounds
> 10. Document the plan in PR description draft or queue notes
> 11. Begin implementation per docs/procedures/implement-change.md

## Expected Output

> CONTENT: What this command produces:
> - A new branch named `queue/<id>-short-slug`
> - A documented plan (acceptance criteria, files, risks, scope)
> - Understanding of all relevant skills
> - Ready to begin implementation
