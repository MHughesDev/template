# Makefile
# Canonical command entrypoint for the repository (see AGENTS.md and docs/development/local-setup.md).

SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

.PHONY: help dev lint fmt typecheck test test-unit test-integration test-smoke \
        migrate db-reset db-seed docs-check docs-generate docs-index \
        queue-peek queue-validate queue-archive queue-graph queue-analyze \
        prompt-list skills-list rules-check audit-self \
        security-scan image-build image-scan \
        release-prepare release-verify \
        k8s-render k8s-validate docker-up docker-down \
        init idea-validate scaffold-module profile-enable idea-queue env-generate inventory-check \
        clean health-check

## help: Show this help message
help:
	@echo "Repository make targets:"
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/## //' | column -t -s ':'

## ─────────────────────────────────────────────
## DEVELOPMENT
## ─────────────────────────────────────────────

## dev: Start local API with hot reload
dev:
	@scripts/dev.sh

## lint: Run ruff lint (no auto-fix)
lint:
	@scripts/lint.sh

## fmt: Apply ruff formatting
fmt:
	@scripts/fmt.sh

## typecheck: Run mypy --strict
typecheck:
	@scripts/typecheck.sh

## test: Run full test suite with coverage
test:
	@scripts/test.sh

## test\:unit: Run unit tests only
test\:unit:
	@TEST_TYPE=unit scripts/test.sh

## test\:integration: Run integration tests only
test\:integration:
	@TEST_TYPE=integration scripts/test.sh

## test\:smoke: Run smoke tests only
test\:smoke:
	@TEST_TYPE=smoke scripts/test.sh

## ─────────────────────────────────────────────
## DATABASE
## ─────────────────────────────────────────────

## migrate: Apply database migrations (alembic upgrade head)
migrate:
	@scripts/migrate.sh

## migrate\:create: Scaffold new migration (MESSAGE=<description> required)
migrate\:create:
	@MESSAGE="$(MESSAGE)" scripts/migrate.sh create

## db\:reset: Drop and recreate local database; run migrations
db\:reset:
	@scripts/db-reset.sh

## db\:seed: Populate local database with sample data
db\:seed:
	@scripts/seed-db.sh

## ─────────────────────────────────────────────
## DOCUMENTATION
## ─────────────────────────────────────────────

## docs\:check: Check documentation for drift and broken links
docs\:check:
	@scripts/docs-check.sh

## docs\:generate: Generate all auto-generated documentation from source
docs\:generate:
	@scripts/docs-generate.sh

## docs\:index: Regenerate documentation index files
docs\:index:
	@scripts/docs-index.sh

## ─────────────────────────────────────────────
## QUEUE
## ─────────────────────────────────────────────

## queue\:peek: Read-only: header + first open queue row
queue\:peek:
	@scripts/queue-peek.sh

## queue\:validate: Validate queue schema and invariants
queue\:validate:
	@scripts/queue-validate.sh

## queue\:archive: Move completed row to archive (QUEUE_ID=<id> required)
queue\:archive:
	@QUEUE_ID="$(QUEUE_ID)" scripts/queue-archive.sh

## queue\:graph: Render queue dependency graph (Mermaid)
queue\:graph:
	@scripts/queue-graph.sh

## queue\:analyze: Full queue intelligence analysis
queue\:analyze:
	@scripts/queue-analyze.sh

## ─────────────────────────────────────────────
## AGENT TOOLING
## ─────────────────────────────────────────────

## prompt\:list: List all prompt templates
prompt\:list:
	@scripts/prompt-list.sh

## skills\:list: List all skills by category
skills\:list:
	@scripts/skills-list.sh

## rules\:check: Validate .cursor/rules/ files
rules\:check:
	@scripts/rules-check.sh

## audit\:self: Comprehensive repo spec-compliance audit
audit\:self:
	@scripts/audit-self.sh

## ─────────────────────────────────────────────
## SECURITY
## ─────────────────────────────────────────────

## security\:scan: Run bandit SAST + dependency audit + secret scanner
security\:scan:
	@scripts/security-scan.sh

## image\:build: Build API container image
image\:build:
	@scripts/image-build.sh

## image\:scan: Scan built container image with Trivy
image\:scan:
	@scripts/image-scan.sh

## ─────────────────────────────────────────────
## RELEASE
## ─────────────────────────────────────────────

## release\:prepare: Update CHANGELOG, verify version
release\:prepare:
	@scripts/release-prepare.sh

## release\:verify: Pre-tag verification (all checks + changelog + version)
release\:verify:
	@scripts/release-verify.sh

## ─────────────────────────────────────────────
## KUBERNETES
## ─────────────────────────────────────────────

## k8s\:render: Render K8s manifests from Kustomize (OVERLAY=dev|staging|prod)
k8s\:render:
	@OVERLAY="$(or $(OVERLAY),dev)" scripts/k8s-render.sh

## k8s\:validate: Validate rendered K8s manifests
k8s\:validate:
	@scripts/k8s-validate.sh

## ─────────────────────────────────────────────
## DOCKER
## ─────────────────────────────────────────────

## docker\:up: Start Docker Compose services
docker\:up:
	docker compose up -d

## docker\:down: Stop Docker Compose services
docker\:down:
	docker compose down

## ─────────────────────────────────────────────
## INITIALIZATION
## ─────────────────────────────────────────────

## init: Run initialization pre-checks and guidance
init:
	@scripts/init-repo.sh

## idea\:validate: Validate idea.md completeness
idea\:validate:
	@scripts/validate-idea.sh

## scaffold\:module: Scaffold a new domain module (MODULE=<name> required)
scaffold\:module:
	@MODULE="$(MODULE)" scripts/scaffold-module.sh

## profile\:enable: Enable an optional profile (PROFILE=<name> required)
profile\:enable:
	@PROFILE="$(PROFILE)" scripts/profile-enable.sh

## idea\:queue: Extract queue items from idea.md and seed queue.csv
idea\:queue:
	@scripts/idea-to-queue.sh

## env\:generate: Generate .env from .env.example
env\:generate:
	@scripts/generate-env.sh

## inventory\:check: Verify all spec-required files exist
inventory\:check:
	@scripts/inventory-check.sh

## ─────────────────────────────────────────────
## UTILITY
## ─────────────────────────────────────────────

## clean: Remove build artifacts and caches
clean:
	@scripts/clean.sh

## health\:check: Check API health endpoints (/health /ready /live)
health\:check:
	@scripts/health-check.sh
