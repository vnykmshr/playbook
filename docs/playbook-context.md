# Engineering Playbook Working Context

> **Purpose:** Onboarding context for new developers and session refresh for ongoing work.
> **Current Version:** v1.1.0 (in development) | **Last Updated:** 2026-01-11
>
> **Related Docs:** `/pb-guide` (SDLC tiers, gates, checklists) | `/pb-standards` (coding standards, conventions)

---

## What is Engineering Playbook

The **Engineering Playbook** is a comprehensive set of development workflow commands that codifies iterative development practices with built-in quality gates. It provides reusable SDLC guidance, templates, and checklists for any engineering team.

**Key User Journeys:**
1. **Feature Development** — `/pb-plan` → `/pb-start` → `/pb-cycle` (repeat) → `/pb-pr` → `/pb-release`
2. **Repository Management** — `/pb-repo-init` → `/pb-repo-organize` → `/pb-repo-readme` → `/pb-docs-publish`
3. **Periodic Maintenance** — `/pb-review`, `/pb-review-code`, `/pb-review-tests`, `/pb-review-docs`, `/pb-review-hygiene`

**Philosophy:** Iterative development, quality gates at every step, tests that matter, logical commits. No shortcuts. Do it right the first time.

**Repo:** https://github.com/vnykmshr/playbook | **Status:** v1.1.0 in active development

---

## Architecture

```
Playbook Repository Structure:

commands/                    # All 32 SDLC commands (markdown files)
├── core/                    # Foundation (guide, standards, templates)
│   ├── pb-guide.md          # Complete SDLC playbook
│   ├── pb-standards.md      # Coding standards & principles
│   └── pb-templates.md      # Templates for all phases
├── planning/                # Feature planning & architecture
│   ├── pb-plan.md           # Focus area planning
│   ├── pb-adr.md            # Architecture Decision Records
│   ├── pb-deprecation.md    # Backwards compatibility strategy
│   └── pb-observability.md  # Monitoring design
├── development/             # Daily development workflow
│   ├── pb-start.md          # Start feature branch
│   ├── pb-commit.md         # Craft atomic commits
│   ├── pb-cycle.md          # Self-review + peer review iteration
│   ├── pb-standup.md        # Async status updates
│   └── pb-resume.md         # Resume after break
├── release/                 # Release & deployment
│   ├── pb-release.md        # Production releases
│   ├── pb-incident.md       # Emergency response
│   └── pb-migrations.md     # Database migrations
├── reviews/                 # Periodic review commands
│   ├── pb-review.md         # Comprehensive 10-perspective review
│   ├── pb-review-code.md    # Code quality & cleanup
│   ├── pb-review-tests.md   # Test suite quality
│   ├── pb-review-docs.md    # Documentation accuracy
│   ├── pb-review-hygiene.md # Multi-role health check
│   ├── pb-review-product.md # Product + technical review
│   ├── pb-review-prerelease # Pre-release code review
│   └── pb-security.md       # Security review checklists
├── repo/                    # Repository management
│   ├── pb-repo-init.md      # Initialize greenfield project
│   ├── pb-repo-organize.md  # Clean up project structure
│   ├── pb-repo-readme.md    # Universal README generator
│   ├── pb-repo-about.md     # GitHub About + tags
│   ├── pb-repo-blog.md      # Technical blog with Mermaid
│   ├── pb-repo-enhance.md   # Full repository polish
│   └── pb-docs-publish.md   # Documentation publishing
└── templates/               # Context & documentation template
    └── pb-context.md        # This template (you are here)

docs/                        # Documentation & supporting materials
├── checklists.md            # Consolidated reference checklists
├── playbook-context.md      # This file (filled-in example)
├── command-dependency-graph.md
├── glossary.md
└── choosing-commands.md

scripts/                     # Installation & setup
├── install.sh               # Create symlinks to ~/.claude/commands/
└── uninstall.sh             # Remove symlinks

todos/                       # Development tracking (gitignored)
└── releases/
    └── v1.1.0/              # v1.1.0 release planning
        ├── master-tracker.md
        ├── phase-1-quick-wins.md
        ├── phase-2-high-impact.md
        ├── phase-3-medium-priority.md
        ├── phase-4-docs-publish.md
        ├── phase-5-final.md
        └── phase-6-import-prompts.md
```

**Components:**
- **Playbook Commands** — 32 markdown files covering full SDLC
- **Installation Scripts** — Bash scripts to symlink commands to ~/.claude/commands/
- **Documentation** — Supporting docs, checklists, guides
- **Release Planning** — Tracked in todos/releases/ (gitignored)

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Format | Markdown (.md files, CommonMark compatible) |
| Installation | Bash scripts (install.sh, uninstall.sh) |
| Distribution | Git + GitHub symlinks to ~/.claude/commands/ |
| Integration | Claude Code CLI (/pb-command syntax) |
| Version Control | Git (commits, tags, releases) |
| Hosting | GitHub https://github.com/vnykmshr/playbook |
| Development | Markdown editor (any editor works) |

---

## Getting Started

**Prerequisites:**
- Git (for cloning the repo)
- Bash (for installation scripts)
- Claude Code (to use the commands)

**Setup:**

```bash
# Clone the playbook
git clone https://github.com/vnykmshr/playbook.git
cd playbook

# Install commands (creates symlinks to ~/.claude/commands/)
./scripts/install.sh

# Verify installation
ls ~/.claude/commands/ | grep pb-

# You're ready! Commands now available as /pb-* in Claude Code
```

**After Setup:**
- Commands available as `/pb-*` in Claude Code (e.g., `/pb-start`, `/pb-cycle`)
- Run `/pb-guide` first for comprehensive SDLC overview
- Run `./scripts/install.sh` again to update after pulling changes

**Common Commands:**

```bash
# Check which commands are installed
ls ~/.claude/commands/ | grep pb-

# See all commands
cat commands/*/*.md | grep "^# "

# Run installation (or re-run after updates)
./scripts/install.sh

# Uninstall if needed
./scripts/uninstall.sh
```

---

## Development Workflow (SDLC)

**Philosophy:** Eat your own dogfood — use playbook commands to develop the playbook itself. Stay committed to full SDLC flow. No shortcuts.

> **Work Tiers:** S (small, <2h) | M (medium, phased) | L (large, multi-week). See `/pb-guide` for tier definitions, gates, and checklists.

### 1. Planning
- Define what commands to add or enhance
- Document scope in `todos/releases/vX.Y.Z/`
- For M/L tier: Lock scope with stakeholder approval

### 2. Development
- Create feature branch: `feature/v1.1.0-command-name`
- Edit markdown files in appropriate category
- Logical, atomic commits with conventional format
- Follow `/pb-standards` for tone and structure

### 3. Quality Checks
```bash
# Verify markdown syntax (CommonMark compatible)
# Check for broken /pb-* references
# Ensure consistent heading levels and formatting
# Test command installation: ./scripts/install.sh
# Verify symlinks created correctly
```

### 4. Self Review
- Review your own diff with `git diff`
- Check for: typos, unclear instructions, missing sections
- Verify all internal `/pb-*` cross-references are valid
- Ensure markdown renders cleanly in monospace CLI

### 5. Commit & Push
```bash
git add commands/[category]/pb-command.md
git commit -m "feat(category): add/update pb-command description"
git push origin feature/branch-name
```

### 6. Peer Review
- Playbook commands reviewed for clarity and utility
- Check: Does it solve a real problem? Is it clear? Does it integrate?

### 7. Merge to Main
- After peer review approval, merge to main
- One commit per logical change (clean history)

### 8. Release
- Version bump (major.minor.patch, semantic versioning)
- Update CHANGELOG.md with all changes
- Create git tag: `git tag -a v1.1.0 -m "v1.1.0 - description"`
- Push tag: `git push origin v1.1.0`
- Create GitHub release with release notes

---

## Command Categories & Relationships

### Core Foundation (Read First)
- `/pb-guide` — Start here, SDLC overview
- `/pb-standards` — Coding standards & tone
- `/pb-templates` — Templates for all phases
- `/pb-context` — Documentation template

### Planning (Before Development)
- `/pb-plan` — Plan focus area
- `/pb-adr` — Architecture decisions
- `/pb-deprecation` — Backwards compatibility
- `/pb-observability` — Monitoring design

### Development (During Feature Work)
- `/pb-start` — Begin feature branch
- `/pb-commit` — Craft atomic commits
- `/pb-cycle` — Iterate with reviews
- `/pb-standup` — Async status updates
- `/pb-resume` — Resume after break
- `/pb-pr` — Create pull request

### Release (After Development)
- `/pb-release` — Production release
- `/pb-incident` — Emergency response
- `/pb-migrations` — Database changes

### Repository (Project Setup & Maintenance)
- `/pb-repo-init` — New project
- `/pb-repo-organize` — Structure cleanup
- `/pb-repo-readme` — Generate README
- `/pb-repo-about` — GitHub metadata
- `/pb-repo-blog` — Technical blog
- `/pb-repo-enhance` — Full polish
- `/pb-docs-publish` — Documentation site

### Reviews (Periodic Maintenance)
- `/pb-review` — Comprehensive 10-perspective
- `/pb-review-code` — Code cleanup
- `/pb-review-tests` — Test quality
- `/pb-review-docs` — Documentation
- `/pb-review-hygiene` — Health check
- `/pb-review-product` — Product alignment
- `/pb-review-prerelease` — Final code review
- `/pb-security` — Security review

---

## Key Patterns

| Pattern | Implementation |
|---------|----------------|
| Naming | `/pb-<action>` or `/pb-<category>-<target>` |
| Structure | Title, sections with `---` dividers, clear headings |
| Tone | Professional, concise, no fluff, no AI-speak |
| Cross-refs | Use `/pb-command` format for references |
| Examples | Include practical, runnable examples |
| Checklists | Reference `docs/checklists.md` (single source of truth) |

---

## Release History

| Version | Date | Status | Highlights |
|---------|------|--------|------------|
| v1.1.0 | 2026-02-15 (planned) | In Development | +7 new commands, 4 enhanced commands, docs consolidation |
| v1.0.0 | 2026-01-11 | Released | Initial release: 25 commands across 7 categories |

---

## Active Development Context

### Current Work (v1.1.0)
- **Phase 1**: Quick wins (standup, security, consolidation, ADR examples, context example)
- **Phase 2**: High-impact commands (commit, deprecation, integration tests, observability)
- **Phase 3**: Polish existing (runbooks, test patterns, migrations, cross-refs)
- **Phase 4**: Documentation publishing tool (`/pb-docs-publish`)
- **Phase 5**: Final release docs and validation
- **Phase 6** (optional): Import additional prompts (knowledge-transfer, logging)

### Recently Completed (This Session)
1. ✅ Created `/pb-standup` — Async status template
2. ✅ Consolidated checklists → `docs/checklists.md`
3. ✅ Enhanced `/pb-adr` — Added 4 real-world examples
4. ✅ Created `/pb-security` — Comprehensive security review

### Next Up
- Document playbook as `/pb-context` example (THIS)
- Create `/pb-logging` command
- Create `/pb-knowledge-transfer` command
- Final release prep and v1.1.0 tag

### Known Issues / Gaps (for Future Versions)
- None identified in v1.1.0 scope
- **v1.2.0 candidates**: Language-specific guides (Go, Python, Rust), microservice review, experiment workflows

---

## Session Checklist

```bash
cd /Users/vmx/workspace/github/vnykmshr/playbook

# Verify current state
git status                                          # Check for uncommitted changes
git log --oneline -5                                # Recent commits
find commands -name "*.md" | wc -l                  # Command count (should be 32 for v1.1.0)
git describe --tags 2>/dev/null || echo "No tags"   # Current version

# Verify installation
./scripts/install.sh                                # Reinstall if needed
ls ~/.claude/commands/ | grep pb- | wc -l           # Check symlinks created

# Check structure
ls -la commands/                                    # Verify 7 categories
ls -la docs/                                        # Verify support docs
```

---

## Quick Command Reference

**Most Used Commands:**
- `/pb-start` — Begin new feature work
- `/pb-cycle` — Self-review + peer review
- `/pb-pr` — Create pull request
- `/pb-release` — Production release

**Planning & Architecture:**
- `/pb-plan` — Plan new focus area
- `/pb-adr` — Architecture decision record

**Periodic Maintenance:**
- `/pb-review` — Comprehensive review
- `/pb-review-code` — Code cleanup
- `/pb-review-tests` — Test quality
- `/pb-security` — Security review

**Repository Setup:**
- `/pb-repo-init` — New project
- `/pb-docs-publish` — Documentation publishing

---

*Created: 2026-01-11 | Example of filled-in `/pb-context` template | Copy and adapt for your project*
