# Makefile
# Canonical command entrypoint. Prefer `make <target>` over ad hoc shell.

SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

.PHONY: help dev lint fmt fmt-check fmt-fix typecheck test test-unit test-integration test-smoke \
        migrate migrate\:create ci-migrate-dry-run db-reset db-seed docs-check docs-generate docs-index \
        queue-peek queue-validate queue-archive queue-graph queue-analyze \
        prompt-list skills-list rules-check audit-self \
        security-scan secret-scan image-build image-scan \
        release-prepare release-verify \
        k8s-render k8s-validate docker-up docker-down \
        init idea-validate idea-parse idea-plan idea-execute init-from-idea \
        scaffold-module profile-enable idea-queue env-generate inventory-check \
        codebase-summary skill-docs-gen \
        test-scaffold env-sync coverage-ratchet rule-lint adr-index \
        clean health-check

## help: Show targets (see also: scripts/README.md)
help:
	@echo "Targets:"
	@grep -E '^##' $(MAKEFILE_LIST) | sed 's/^## //' | column -t -s ':'

## dev: Run API with uvicorn --reload
dev:
	@scripts/dev.sh

## lint: Ruff lint
lint:
	@scripts/lint.sh

## fmt: Apply Ruff formatting
fmt:
	@scripts/fmt.sh

## fmt-check: Ruff format verify (CI mode)
fmt-check:
	@scripts/fmt-check.sh

## fmt-fix: Alias for fmt (apply formatting)
fmt-fix: fmt

## typecheck: mypy strict
typecheck:
	@scripts/typecheck.sh

## test: pytest with coverage
test:
	@scripts/test.sh

## test-unit: unit tests only
test-unit:
	@TEST_TYPE=unit scripts/test.sh

## test-integration: integration tests only
test-integration:
	@TEST_TYPE=integration scripts/test.sh

## test-smoke: smoke tests only
test-smoke:
	@TEST_TYPE=smoke scripts/test.sh

## migrate: alembic upgrade head
migrate:
	@scripts/migrate.sh

## migrate\:create: alembic revision --autogenerate (MESSAGE= required)
migrate\:create:
	@MESSAGE="$(MESSAGE)" scripts/migrate.sh create

## ci-migrate-dry-run: same SQLite migration checks as CI (preview + apply)
ci-migrate-dry-run:
	@scripts/ci-migrate-dry-run.sh

## db-reset: reset local sqlite + migrate
db-reset:
	@scripts/db-reset.sh

## db-seed: optional seed data
db-seed:
	@scripts/seed-db.sh

## docs-check: documentation link check
docs-check:
	@scripts/docs-check.sh

## docs-generate: placeholder for generated docs
docs-generate:
	@scripts/docs-generate.sh

## docs-index: placeholder for docs index
docs-index:
	@scripts/docs-index.sh

## queue-peek: show queue header + first row
queue-peek:
	@scripts/queue-peek.sh

## queue-validate: validate queue CSV schema
queue-validate:
	@scripts/queue-validate.sh

## queue-archive: move row to archive (QUEUE_ID= required)
queue-archive:
	@QUEUE_ID="$(QUEUE_ID)" scripts/queue-archive.sh

## queue-graph: mermaid stub / graph placeholder
queue-graph:
	@scripts/queue-graph.sh

## queue-analyze: validate + analysis stub
queue-analyze:
	@scripts/queue-analyze.sh

## prompt-list: list prompts/*.md
prompt-list:
	@scripts/prompt-list.sh

## skills-list: list skills by folder
skills-list:
	@scripts/skills-list.sh

## rules-check: cursor rules front matter
rules-check:
	@scripts/rules-check.sh

## audit-self: repo self-audit
audit-self:
	@scripts/audit-self.sh

## security-scan: bandit + pip-audit
security-scan:
	@scripts/security-scan.sh

## image-build: docker build API image
image-build:
	@scripts/image-build.sh

## image-scan: trivy scan image
image-scan:
	@scripts/image-scan.sh

## release-prepare: changelog sanity check
release-prepare:
	@scripts/release-prepare.sh

## release-verify: lint + fmt check + typecheck + test
release-verify:
	@scripts/release-verify.sh

## k8s-render: kubectl kustomize overlay (OVERLAY=dev|staging|prod)
k8s-render:
	@OVERLAY="$(or $(OVERLAY),dev)" scripts/k8s-render.sh

## k8s-validate: validate kustomize output
k8s-validate:
	@OVERLAY="$(or $(OVERLAY),dev)" scripts/k8s-validate.sh

## docker-up: docker compose up -d
docker-up:
	docker compose up -d

## docker-down: docker compose down
docker-down:
	docker compose down

## init: pip install -e and .env stub
init:
	@scripts/init-repo.sh

## idea-validate: idea.md placeholder check
idea-validate:
	@scripts/validate-idea.sh

## idea-parse: parse idea.md into init-manifest.json
idea-parse:
	@python3 scripts/idea-parser.py

## idea-plan: parse idea.md and print resolved decisions (dry-run, no files written)
idea-plan:
	@python3 scripts/idea-parser.py --dry-run

## idea-execute: run full initialization from init-manifest.json (run idea-parse first)
idea-execute:
	@scripts/init-from-idea.sh

## init-from-idea: validate + parse + execute in one command
init-from-idea: idea-validate idea-parse idea-execute

## scaffold-module: MODULE= name
scaffold-module:
	@MODULE="$(MODULE)" scripts/scaffold-module.sh

## profile-enable: PROFILE= name
profile-enable:
	@PROFILE="$(PROFILE)" scripts/profile-enable.sh

## idea-queue: queue seeding stub
idea-queue:
	@scripts/idea-to-queue.sh

## env-generate: copy .env.example to .env
env-generate:
	@scripts/generate-env.sh

## inventory-check: verify completed IMPLEMENTATION_PLAN paths exist
inventory-check:
	@scripts/inventory-check.sh

## codebase-summary: regenerate CODEBASE_SUMMARY.md
codebase-summary:
	@scripts/codebase-summary.sh

## skill-docs-gen: run docs-generator.py (regenerate docs/generated)
skill-docs-gen:
	@python3 skills/repo-governance/docs-generator.py --mode generate --repo-root .

## secret-scan: scan for potential secrets (heuristic)
secret-scan:
	@python3 skills/security/secret-scanner.py --repo-root .

## test-scaffold: print pytest stubs for a module router (MODULE= required)
test-scaffold:
	@python3 skills/testing/test-scaffolder.py --repo-root . --module "$(MODULE)"

## env-sync: compare .env.example with Settings fields (heuristic)
env-sync:
	@python3 skills/backend/env-var-sync.py --repo-root .

## coverage-ratchet: compare coverage.xml to policy floor
coverage-ratchet:
	@python3 skills/testing/coverage-ratchet.py --repo-root .

## rule-lint: lint .cursor/rules front matter
rule-lint:
	@python3 skills/repo-governance/rule-linter.py --repo-root .

## adr-index: regenerate docs/adr/README.md
adr-index:
	@python3 skills/repo-governance/adr-index-generator.py --repo-root .

## clean: remove caches and build artifacts
clean:
	@scripts/clean.sh

## health-check: curl /health
health-check:
	@scripts/health-check.sh

# --- Colon-style aliases (spec §10.2 and docs). GNU Make needs escaped colons in target names.
.PHONY: skills\:list queue\:peek queue\:validate queue\:archive queue\:graph queue\:analyze audit\:self rules\:check \
        docs\:check docs\:generate docs\:index security\:scan release\:prepare release\:verify docker\:up docker\:down \
        health\:check idea\:validate idea\:parse idea\:plan idea\:execute init\:from-idea profile\:enable idea\:queue \
        scaffold\:module test\:unit test\:integration \
        test\:smoke fmt\:fix fmt\:check prompt\:list db\:reset db\:seed ci\:migrate-dry-run image\:build image\:scan \
        k8s\:render k8s\:validate env\:generate inventory\:check skill\:docs-gen \
        secret\:scan test\:scaffold env\:sync coverage\:ratchet rule\:lint adr\:index

skills\:list: skills-list
queue\:peek: queue-peek
queue\:validate: queue-validate
queue\:archive: queue-archive
queue\:graph: queue-graph
queue\:analyze: queue-analyze
audit\:self: audit-self
rules\:check: rules-check
docs\:check: docs-check
docs\:generate: docs-generate
docs\:index: docs-index
security\:scan: security-scan
release\:prepare: release-prepare
release\:verify: release-verify
docker\:up: docker-up
docker\:down: docker-down
health\:check: health-check
idea\:validate: idea-validate
idea\:parse: idea-parse
idea\:plan: idea-plan
idea\:execute: idea-execute
init\:from-idea: init-from-idea
profile\:enable: profile-enable
idea\:queue: idea-queue
scaffold\:module: scaffold-module
test\:unit: test-unit
test\:integration: test-integration
test\:smoke: test-smoke
fmt\:fix: fmt-fix
fmt\:check: fmt-check
prompt\:list: prompt-list
db\:reset: db-reset
db\:seed: db-seed
ci\:migrate-dry-run: ci-migrate-dry-run
image\:build: image-build
image\:scan: image-scan
k8s\:render: k8s-render
k8s\:validate: k8s-validate
env\:generate: env-generate
inventory\:check: inventory-check
skill\:docs-gen: skill-docs-gen
secret\:scan: secret-scan
test\:scaffold: test-scaffold
env\:sync: env-sync
coverage\:ratchet: coverage-ratchet
rule\:lint: rule-lint
adr\:index: adr-index
