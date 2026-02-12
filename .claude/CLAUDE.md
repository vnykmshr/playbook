# Engineering Playbook Development Context

> Generated: 2026-02-12
> Tech Stack: Markdown + Python + MkDocs + Self-Evolving System
> Status: v2.12.0 (released 2026-02-12)

This file provides project-specific context for Claude Code.
Global guidelines: ~/.claude/CLAUDE.md

---

## Project Overview

**v2.12.0:** 97 development workflow commands for Claude Code with self-evolving system that keeps playbooks aligned with Claude capability improvements.

**Capabilities:**
- **Phase 1: Context Minimization** — BEACON markers system with four-layer context architecture
- **Phase 2: Session Boundary Protection** — BEACON verification at pause/resume boundaries
- **Phase 3: Git History Signal Analysis** — Data-driven insights for quarterly planning

**Audience:** Playbook maintainers, command contributors, Claude Code users integrating playbooks

**Success Metrics:**
- All 97 commands working with zero breaking changes
- 100% metadata coverage (YAML front-matter on all commands)
- Quarterly evolution cycles running (Q1 2026 initial cycle complete)
- BEACON system preventing silent guideline loss
- Git-signals enabling data-driven planning

**Repository:** https://github.com/vnykmshr/playbook
**Release:** v2.12.0 (2026-02-12)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Content | Markdown (CommonMark compatible) |
| Documentation | MkDocs + Material theme |
| Scripts | Python 3.11 |
| Linting | markdownlint + yamllint |
| CI/CD | GitHub Actions |
| Hosting | GitHub Pages |

---

## Project Structure

```
playbook/
├── commands/        # 97 commands across 9 categories (all with YAML metadata v1.0)
│   ├── core/        # Foundation commands (pb-start, pb-cycle, pb-pause, pb-resume, etc.)
│   ├── planning/    # Planning & architecture
│   ├── development/ # Development workflow
│   ├── deployment/  # Deployment & operations
│   ├── reviews/     # Code review commands
│   ├── repo/        # Repository management
│   ├── people/      # Team operations
│   ├── templates/   # Context templates + reference implementations
│   └── utilities/   # System maintenance
├── docs/            # MkDocs documentation + v2.12.0 Integration Guide
├── scripts/         # Python automation (including git-signals analyzer)
├── tests/           # pytest suite (40+ test cases, 274+ convention checks)
└── .claude/         # Context files (this file)
```

**Key Changes in v2.12.0:**
- Added: `scripts/git-signals.py` (440 lines, GitSignalsAnalyzer class)
- Added: `commands/core/pb-git-signals.md` (220 lines, adoption/churn/pain-point analysis)
- Added: `docs/v2.12.0-integration-guide.md` (460+ lines, comprehensive v2.12.0 overview)
- Enhanced: `docs/beacon-verification-at-boundaries.md` (BEACON system documentation)
- Enhanced: `commands/templates/pb-pause-enhanced.md`, `pb-resume-enhanced.md` (reference implementations)

Key locations: `commands/*/pb-*.md`, `docs/*.md`, `scripts/*.py`, `tests/test_*.py`

For full tree: See README.md

---

## BEACON: Project Guardrails

These are non-negotiable constraints for the playbook project:

- **Command count:** 97 (v2.12.0 stable): 86 + 11 from v2.11.0 + pb-git-signals (Phase 3)
- **Categories:** 9 fixed structure (core, planning, development, deployment, reviews, repo, people, templates, utilities)
- **Related Commands:** ≤5 per command (hub exception: pb-patterns keeps 8)
- **Metadata:** All 97 commands require YAML front-matter with 14 fields (v1.0 schema)
- **Linting:** All markdown must pass markdownlint + yamllint
- **No breaking changes:** Commands versioned independently; v2.12.0 is backwards compatible (opt-in phases)
- **Evolution:** Quarterly cycles (Feb, May, Aug, Nov) to keep playbooks aligned with Claude capabilities

---

## BEACON: Audit Conventions (v2.12.0)

Every command MUST follow these conventions:

**Structure Requirements:**
- **Resource Hint:** opus/sonnet/haiku with 1-2 sentence rationale (why that model is chosen)
- **When to Use:** 2-4 bullets describing appropriate contexts
- **Mindset:** References /pb-preamble or /pb-design-rules (thinking principles)
- **Metadata:** YAML front-matter with 14 required fields (see .playbook-metadata-schema.yaml)

**YAML Metadata Schema (v1.0):**
Required fields: name, title, category, difficulty, model_hint, execution_pattern, related_commands, last_reviewed, last_evolved, version, version_notes, breaking_changes

**Convention Checks (40+ test cases, 274+ automated verifications):**
- Command file naming: `pb-<name>.md`
- YAML front-matter: Complete and valid (all 14 required fields)
- Resource Hint: Present with meaningful rationale
- When to Use section: Exists with 2-4 bullets
- Mindset references: Links to /pb-preamble or /pb-design-rules
- Related Commands: ≤5 items (except pb-patterns hub: ≤8)
- Markdown compliance: markdownlint passes all checks
- YAML compliance: yamllint passes (handled by CI)
- MkDocs build: Successful with no broken anchors
- Metadata consistency: Resource hints match body explanations

**Verification (run before committing):**
```bash
find commands -name "*.md" | wc -l          # Should be 97
./scripts/install.sh                         # Verify symlinks work
mkdocs build 2>&1 | tail -3                  # Build + anchor checks
npx markdownlint-cli --config .markdownlint.json 'commands/**/*.md'
python scripts/validate-conventions.py      # Run convention test suite
git status                                   # CI enforcement: all must pass before merge
```

---

## BEACON: Key Patterns

Critical operational patterns for this project:

**Bidirectional links**: When adding command to family (pb-claude-*), check all siblings for back-links immediately.

**Dropped references**: When swapping Related Commands, verify dropped link isn't referenced elsewhere (e.g., Mindset line) before removing.

**MkDocs anchors**: `:` in headings → slug includes all words. `&` → stripped. Stale counts → slug changes (update TOC).

**Files to touch together**: New command → `commands/<category>/`, `docs/command-index.md`, `CHANGELOG.md`

**Operational resilience**: Every command should include or reference recovery steps. When evolving commands, consider rollback paths and graceful degradation. See `/pb-deployment` for recovery patterns.

---

## Relevant Playbooks

| Command | Relevance |
|---------|-----------|
| `/pb-documentation` | Writing guidelines for commands |
| `/pb-review-docs` | Documentation review standards |
| `/pb-standards` | Content and code quality standards |
| `/pb-git-signals` | Git history analysis for evolution planning |
| `/pb-pause` | Pause work with BEACON verification (v2.12.0 Phase 2) |
| `/pb-resume` | Resume work with context loading and BEACON verification (v2.12.0 Phase 2) |
| `/pb-evolve` | Quarterly evolution cycles using git-signals (v2.12.0 Phase 3) |

---

## Overrides from Global

- **Structure**: Documentation/tooling project, not standard code project
- **Commits**: `feat:`, `fix:`, `docs:`, `chore:` for command changes
- **Testing**: Convention tests are primary quality gate
- **Build**: `mkdocs build` instead of `make build`

---

## Session Commands

```bash
# Verify state
git status && find commands -name "*.md" | wc -l

# Validate
mkdocs build 2>&1 | tail -3

# Preview docs
mkdocs serve
```

---

## v2.12.0 Capabilities

**The Self-Evolving Playbook System** with three interlocking phases:

### Phase 1: Context Minimization
- **BEACON markers:** 9 critical guidelines (6 global + 3 project) with dual-presence architecture
- **Four-layer context:** Global principles → Project structure → Learned patterns → Session state
- **Efficiency:** Prevent silent guideline loss while minimizing context bloat
- **Documentation:** `docs/beacon-verification-at-boundaries.md`

### Phase 2: Session Boundary Protection
- **Enhanced /pb-pause:** Step 6.5 verifies all 9 BEACONs before pausing
- **Enhanced /pb-resume:** Steps 3.5-3.6 load context layers and verify BEACONs
- **Safety:** Prevent silent guideline loss during session transitions
- **Reference implementations:** `commands/templates/pb-pause-enhanced.md`, `pb-resume-enhanced.md`

### Phase 3: Git History Signal Analysis
- **Command:** `/pb-git-signals` analyzes git history for adoption, churn, pain points
- **Data-driven planning:** Adoption metrics (what's active), churn analysis (volatility), pain scores (problematic areas)
- **Integration:** Signals inform `/pb-evolve` quarterly planning decisions
- **Usage:** Weekly trends, pre-planning analysis, investigation of pain areas
- **Implementation:** `scripts/git-signals.py` (440 lines), `commands/core/pb-git-signals.md` (220 lines)

### Integration Guide
- **Comprehensive documentation:** `docs/v2.12.0-integration-guide.md` explains how all three phases work together
- **Real-world scenarios:** Pause/resume/planning cycle documented with time-based examples
- **Backwards compatible:** All new capabilities are opt-in; no breaking changes from v2.11.0

---

## Session State Management (v2.12.0)

**Context Architecture:** Four-layer system for efficient session resumption

1. **Global CLAUDE.md** — Universal principles, BEACONs (load globally)
2. **Project CLAUDE.md** — Project structure, patterns, guardrails (load per project)
3. **Memory** — Learned patterns, accumulated insights (durable)
4. **Session State** — Working-context (durable) + Pause-notes (ephemeral)

**Working-Context (Durable):**
- Location: `todos/1-working-context.md`
- Updated: On releases, version changes, quarterly reviews
- Purpose: Track project state across sessions
- Survives: Multiple sessions, weeks, months
- Regenerate: Run `/pb-context` to refresh when stale

**Pause-Notes (Ephemeral):**
- Location: `todos/pause-notes.md` (append chronologically)
- Updated: Each session via `/pb-pause`
- Purpose: Fast resumption (where work paused, immediate next steps)
- Survives: Until resumption, then can be archived
- Maintenance: Keep 3-5 recent entries, archive old to `todos/done/`

See global CLAUDE.md "Session State Management" section for full context architecture.

---

*Regenerate with `/pb-claude-project` when project structure changes significantly.*
