# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
