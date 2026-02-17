# Engineering Playbook Development Context

> Generated: 2026-02-17
> Tech Stack: Markdown + Python + MkDocs + Self-Evolving System
> Status: v2.12.0 (released 2026-02-12, ritual updated 2026-02-17)

This file provides project-specific context for Claude Code.
Global guidelines: ~/.claude/CLAUDE.md

---

## Project Overview

**v2.12.0:** 97 development workflow commands + new simplified 3-command ritual (v2.12.0 Phase 4).

**Capabilities:**
- **Phase 1: Context Minimization** — BEACON markers system with four-layer context architecture
- **Phase 2: Session Boundary Protection** — BEACON verification at pause/resume boundaries
- **Phase 3: Git History Signal Analysis** — Data-driven insights for quarterly planning
- **Phase 4: Automated Workflow** — 90% automation, 10% human (new `/pb-review`, `/pb-preferences`)

**Recent Changes (2026-02-17):**
- Redesigned core ritual: `/pb-start` → code → `/pb-review` (automatic)
- New command: `/pb-preferences` (one-time setup of decision rules)
- Updated: `/pb-start` (scope detection), `/pb-commit` (auto-triggered)
- Deprecated: `/pb-cycle` (merged into `/pb-review`)
- Philosophy: Human handles 10%, system handles 90%

**Audience:** Playbook maintainers, command contributors, Claude Code users

---

## The Simplified Ritual

**For all development work:**

```
FIRST TIME:
/pb-preferences --setup
  ↓ 15 minutes to establish decision rules
  ↓ System saves forever

EVERY FEATURE:
/pb-start "feature description"
  ↓ 30 seconds (answer 3-4 scope questions)
  ↓ Branch created, scope recorded

[You code]

/pb-review
  ↓ Fully automatic
  ↓ Analyzes change
  ↓ Applies your preferences
  ↓ Consults personas (Linus, Alex, Jordan, Maya, Sam)
  ↓ Auto-commits if passes
  ↓ Alerts only if ambiguous (~5% of time)

REPEAT
```

**Your involvement:** ~30 sec per feature + ~1-2 min per 10 features for ambiguous decisions

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
│   ├── core/        # Foundation commands (pb-start, pb-review, pb-commit, pb-pause, pb-resume)
│   ├── development/ # Development workflow (pb-start, pb-review, pb-commit, pb-preferences)
│   ├── planning/    # Planning & architecture
│   ├── deployment/  # Deployment & operations
│   ├── reviews/     # Code review commands
│   ├── repo/        # Repository management
│   ├── people/      # Team operations
│   ├── templates/   # Context templates (pb-claude-*, pb-pause, pb-resume)
│   └── utilities/   # System maintenance
├── docs/            # MkDocs documentation + v2.12.0 Integration Guide
├── scripts/         # Python automation (git-signals, validate-conventions, etc.)
├── tests/           # pytest suite (40+ test cases, 274+ convention checks)
└── .claude/         # Context files (this file)
```

**Key changes in workflow update (2026-02-17):**
- New: `commands/development/pb-preferences.md` (one-time setup)
- New: `commands/development/pb-review.md` (replaces pb-cycle, 90% automatic)
- Updated: `commands/development/pb-start.md` (scope detection, 3-4 questions)
- Updated: `commands/development/pb-commit.md` (automatic by default)

---

## BEACON: Project Guardrails

These are non-negotiable constraints for the playbook project:

- **Command count:** 97 (v2.12.0 stable)
- **Categories:** 9 fixed structure
- **Related Commands:** ≤5 per command (pb-patterns hub: ≤8)
- **Metadata:** All 97 commands require YAML front-matter (14 fields, v1.0 schema)
- **Linting:** All markdown must pass markdownlint + yamllint
- **No breaking changes:** Commands versioned independently; v2.12.0 is backwards compatible
- **Evolution:** Quarterly cycles (Feb, May, Aug, Nov)

---

## BEACON: Development Ritual (Project Context)

**For the playbook project itself:**

```
Goal: Contribute a new command or enhance existing ones

/pb-preferences --setup
  ↓ Establish your values for this project

/pb-start "feat: add new playbook command"
  ↓ Establish scope: Is it new? Enhancement? Template?
  ↓ Does it fit 9 categories? What complexity?

[Code the command]
  ↓ Write markdown command file
  ↓ Follow metadata schema (14 fields, v1.0)
  ↓ Include BEACON references
  ↓ Test with /pb-review

/pb-review
  ↓ Auto-detects: Metadata completeness, markdown lint, anchor validation
  ↓ Checks: Related commands ≤5, YAML valid, convention compliance
  ↓ Consults: Sam (documentation clarity), Linus (principles alignment)
  ↓ Auto-commits if passes

/pb-commit
  ↓ Message includes: Command name, metadata version, category

[Push to remote]

[Create PR for peer review]
```

---

## BEACON: Audit Conventions (v2.12.0)

Every command MUST follow these conventions:

**Structure Requirements:**
- **Resource Hint:** opus/sonnet/haiku with 1-2 sentence rationale
- **When to Use:** 2-4 bullets describing appropriate contexts
- **Mindset:** References `/pb-preamble` or `/pb-design-rules`
- **Metadata:** YAML front-matter with 14 required fields

**Verification (run before committing):**
```bash
find commands -name "*.md" | wc -l          # Should be 98 (97 + pb-preferences)
./scripts/install.sh                         # Verify symlinks work
mkdocs build 2>&1 | tail -3                  # Build + anchor checks
npx markdownlint-cli --config .markdownlint.json 'commands/**/*.md'
python scripts/validate-conventions.py      # Convention test suite
git status                                   # CI enforcement
```

---

## BEACON: Key Patterns

Critical operational patterns for this project:

**Bidirectional links:** When adding command to family (pb-claude-*, pb-review-*), check all siblings for back-links immediately.

**Dropped references:** When swapping Related Commands, verify dropped link isn't referenced elsewhere before removing.

**MkDocs anchors:** `:` in headings → slug includes all words. `&` → stripped. Stale counts → slug changes (update TOC).

**Files to touch together:** New command → `commands/<category>/`, `docs/command-index.md`, `CHANGELOG.md`

---

## Relevant Playbooks for This Project

| Command | Relevance |
|---------|-----------|
| `/pb-documentation` | Writing guidelines for commands |
| `/pb-review-docs` | Documentation review standards |
| `/pb-standards` | Content and code quality standards |
| `/pb-git-signals` | Git history analysis for evolution planning |
| `/pb-commit` | Commit conventions (playbook uses same conventions) |
| `/pb-pause` | Pause work with BEACON verification |
| `/pb-resume` | Resume work with context loading |
| `/pb-evolve` | Quarterly evolution cycles |

---

## New Workflow Integration

**Old playbook approach (for reference):**
- Users invoiced `/pb-cycle` → manual review checklist
- Users manually selected personas (`/pb-linus-agent`, etc.)
- `/pb-commit` required manual message formatting

**New playbook approach (2026-02-17+):**
- Automatic quality gate (`/pb-review`) with preference-driven decisions
- Personas consulted automatically (no user selection needed)
- Messages auto-drafted with reasoning from review

**For the playbook project:** When contributing commands, use the new ritual. Old commands still work; new commands should follow conventions.

---

## Migration Path

**If working on the playbook itself:**
1. Read this context (you're here)
2. Run `/pb-preferences --setup` once (set your values)
3. Use `/pb-start` → code → `/pb-review` for new commands
4. Follow command structure in `docs/command-template.md`
5. Verify with convention checks before commit

**If using playbooks in your project:** Use simplified 3-command ritual (from global CLAUDE.md)

---

## Session Commands

```bash
# Verify playbook state
git status && find commands -name "*.md" | wc -l

# Validate before committing
mkdocs build 2>&1 | tail -3
npx markdownlint-cli --config .markdownlint.json 'commands/**/*.md'

# Preview docs
mkdocs serve
```

---

## Session Ritual

- `/pb-pause` before breaks — saves state, archives old entries, reports context health
- `/pb-resume` to start — loads context, shows sizes, flags stale data
- `/pb-context` to regenerate working context on release/milestone
- See `docs/v2.12.0-integration-guide.md` for BEACON system and git-signals details

---

*Regenerate with `/pb-claude-project` when project structure changes significantly.*
