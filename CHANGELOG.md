# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.3.0] - 2026-01-12

### Added
- **Example Projects**: Three complete, production-ready examples demonstrating playbook patterns:
  - Go Backend API (Go 1.22 + PostgreSQL): REST API with connection pooling, graceful shutdown, table-driven tests
  - Python Data Pipeline (Python 3.11 + SQLAlchemy): Async event processing pipeline with aggregation
  - Node.js REST API (Node.js 20 + TypeScript): Type-safe Express API with request tracing and structured logging
- **Playbook in Action Guide**: Comprehensive walkthrough (`docs/playbook-in-action.md`) showing:
  - Real-world workflows using `/pb-start`, `/pb-cycle`, `/pb-pr` with three example projects
  - Step-by-step development scenarios and common patterns
  - Testing, code quality, and deployment strategies for each stack
- **Example Integration**: Updated command-index with references to example projects
- **Project Templates**: Complete Dockerfile, docker-compose, Makefile, and documentation templates

### Documentation
- Added `docs/playbook-in-action.md`: Real-world playbook usage guide with complete examples
- Updated `docs/command-index.md`: Added Example Projects section with links and quick reference
- Each example project includes comprehensive README and DEVELOPMENT.md guides

### Fixed
- Go Backend API: Updated to Go 1.22 for PathValue support in HTTP routing
- Node.js API: Added missing TypeScript type definitions (@types/pg, @types/uuid, @types/supertest)
- Node.js API: Updated npm ci syntax to --omit=dev for production builds
- All examples: Validated with docker-compose, endpoints tested and working

### Validation
- All 3 example projects tested with docker-compose
- Go Backend API: Health check and CRUD endpoints verified
- Node.js API: TypeScript compilation and test suite passing
- Python Pipeline: Async pipeline execution validated
- Total: 5375+ lines of code and documentation across 28 new files

### Deferred to v1.3.1
- GitHub Discussions community infrastructure
- Community contribution guidelines (`/docs/community.md`)
- Case study templates and community project showcase
- Additional documentation and integration examples

## [v1.2.1] - 2026-01-11

### Added
- **Release Automation**: `scripts/release.sh` for automated version management and git tagging
- **Git Configuration**: `.gitattributes` for consistent line ending normalization (LF)
- **Command Structure Guidelines**: Enhanced `CONTRIBUTING.md` with detailed command creation standards

### Documentation
- Added command structure requirements: title, overview, sections, examples, checklists
- Added linting standards and formatting guidelines for command files
- Added pre-submission checklist for contributors
- Added example command template

### Changed
- Extended CI/CD pipeline (`.github/workflows/deploy-docs.yml`) to validate both `docs/` and `commands/` directories
- Enhanced contributor documentation with command structure expectations

### Fixed
- Established line ending normalization via `.gitattributes` to prevent CRLF issues across platforms

## [v1.2.0] - 2026-01-11

### Added
- **Pattern Library**: 4 pattern family commands (async, core, database, distributed)
- **Structured Implementation**: `pb-todo-implement` with checkpoint-based review
- **Knowledge Transfer**: `pb-knowledge-transfer` for team handoff
- **Logging Standards**: `pb-logging` for audit and compliance
- **Documentation Pipeline**: Mkdocs + GitHub Pages deployment
- **CI/CD Integration**: Automated lint, build, and deploy workflow

### Fixed
- Resolved duplicate `/pb-incident.md` (kept deployment version, deleted release version)
- Recategorized `/pb-knowledge-transfer` from Team & Growth to Development
- Removed broken INTEGRATION-SUMMARY.md reference

### Changed
- Removed emojis from all playbook commands for text-only style
- Updated command count references for dynamic flexibility

### Documentation
- Created `.github/CONTRIBUTING.md` with contribution guidelines
- Published docs site at https://vnykmshr.github.io/playbook/
- Added command-index, integration-guide, decision-guide, workflows, faq, best-practices, checklists, glossary

## [v1.1.0] - Earlier

- Initial release with 25 core commands

---

## How to Update This File

When releasing a new version:

1. Add new section at top: `## [vX.Y.Z] - YYYY-MM-DD`
2. Use these categories as needed:
   - **Added**: New features/commands
   - **Changed**: Modifications to existing commands
   - **Fixed**: Bug fixes and corrections
   - **Removed**: Deleted commands or features
   - **Deprecated**: Commands marked for removal in future versions
   - **Documentation**: Docs-only changes
   - **Security**: Security-related fixes

3. Keep "Unreleased" section at top for in-progress work (remove when releasing)

4. Link versions at bottom: `[vX.Y.Z]: https://github.com/vnykmshr/playbook/releases/tag/vX.Y.Z`
