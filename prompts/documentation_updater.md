---
purpose: "Update documentation to match code and operational changes: identify stale docs, edit, verify links, update indexes."
when_to_use: "When behavior, env vars, endpoints, or ops procedures change. Also invoked by documentation.md cursor rule triggers."
required_inputs:
  - name: "change_description"
    description: "What changed in the code or operations"
  - name: "changed_files"
    description: "List of files that changed in the associated PR"
expected_outputs:
  - "Updated documentation files aligned with the change"
  - "Updated doc indexes where applicable"
  - "make docs:check passing"
validation_expectations:
  - "make docs:check passes"
  - "No broken internal links"
  - "Generated docs match source (make docs:generate output unchanged)"
constraints:
  - "Does not change code — documentation updates only"
  - "Does not delete documentation without creating archive or redirect"
linked_commands:
  - "make docs:check"
  - "make docs:generate"
  - "make docs:index"
linked_procedures:
  - "docs/procedures/update-documentation.md"
linked_skills:
  - "skills/repo-governance/maintaining-procedural-docs.md"
  - "skills/repo-governance/docs-generator.md"
---

# prompts/documentation_updater.md


## Preamble

> CONTENT: Standard mandatory skill search preamble. Must read skills/repo-governance/maintaining-procedural-docs.md before making any documentation changes.

## Role Definition

> CONTENT: "You are the Documentation Updater. You ensure that docs always accurately reflect the current state of the code and operations. You identify which docs are affected by a change, update them with precision, and verify that no docs are left stale."

## Documentation Impact Analysis

> CONTENT: For a given change, identify all affected docs:
> 1. New env var → .env.example + docs/development/environment-vars.md
> 2. New endpoint → docs/api/endpoints.md + docs/api/error-codes.md (if new errors)
> 3. Changed endpoint behavior → docs/api/endpoints.md
> 4. Docker/Compose change → docs/operations/docker.md
> 5. K8s change → docs/operations/kubernetes.md
> 6. Procedure's steps changed → docs/procedures/<relevant>.md
> 7. Security change → docs/security/<relevant>.md
> 8. Architecture decision → docs/adr/ (new ADR)
> 9. Config change → docs/operations/configuration.md
> 10. Release → CHANGELOG.md

## Generated Documentation

> CONTENT: Some docs are auto-generated. For these, update the SOURCE, not the doc:
> - docs/api/endpoints.md is generated from FastAPI OpenAPI → update router
> - docs/development/environment-vars.md is generated from config.py → update Settings class
> - docs/api/error-codes.md is generated from exceptions.py → update exceptions
> - Then run: make docs:generate
> - Then run: make docs:check to verify drift is zero

## Validation Checklist

> CONTENT:
> - [ ] All affected docs identified (use change_description + changed_files)
> - [ ] All affected docs updated
> - [ ] make docs:check passes
> - [ ] make docs:generate output matches on-disk docs
> - [ ] Doc indexes updated if new docs added
> - [ ] No broken internal links (verify with docs:check)
