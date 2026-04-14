# CHANGELOG.md

All notable changes to this project are documented in this file.

This file follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) version **1.1.0**. This project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

### Changed

- Consolidated open Dependabot updates: GitHub Actions (checkout, stale, docker/build-push-action, setup-buildx-action), API Docker base image to Python 3.14-slim, and Python dependency floors in `pyproject.toml` (asyncpg, bandit, email-validator, pydantic-settings, pytest-cov).

### Fixed

### Removed

### Security

### Deprecated

## [0.1.0] — 2026-04-14

### Added

- Initial agent-operated template repository structure per **spec v4.0**
- FastAPI modular monolith layout (health, auth, tenancy) with tests and tooling
- CSV queue (`queue/queue.csv`, `queue/queuearchive.csv`) and queue SOPs
- Documentation tree, skills library, and prompt templates
- CI workflows (lint, typecheck, test, security) and Dependabot configuration
- Kubernetes base manifests with dev/staging/prod overlays
- Cross-platform bootstrap scripts (`setup.sh` / `setup.bat`, `run.sh` / `run.bat`)
- Makefile as the canonical command entrypoint

[Unreleased]: https://github.com/MHughesDev/template/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/MHughesDev/template/releases/tag/v0.1.0
