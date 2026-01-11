# Engineering Playbook

A comprehensive set of development workflow commands for Claude Code. Codifies iterative development practices with built-in quality gates.

## Philosophy

- **Iterative, incremental development** — Small, focused changes
- **Quality gates at every step** — Lint, typecheck, test before proceeding
- **Self-review + peer review** — Every iteration gets the full cycle
- **Tests that matter** — Catch real bugs, not chase coverage numbers
- **Logical commits** — One concern per commit, always deployable

## Commands

| Category | Commands | Purpose |
|----------|----------|---------|
| **Core** | 3 | SDLC foundation, standards, guidelines |
| **Planning** | 2 | Focus area planning, ADRs |
| **Development** | 4 | Feature branches, reviews, PRs |
| **Release** | 2 | Deployment, incidents |
| **Reviews** | 7 | Periodic codebase reviews |
| **Templates** | 1 | Project context template |

### Development Workflow

```
/pb-start     Start work on a feature branch
/pb-cycle     Self-review + peer review iteration
/pb-resume    Resume after a break
/pb-pr        Create a pull request
```

### Planning & Architecture

```
/pb-plan      Plan a new feature/release
/pb-adr       Document architectural decisions
```

### Release & Operations

```
/pb-release   Pre-release checks and deployment
/pb-incident  P0/P1 incident handling
```

### Periodic Reviews

```
/pb-review           Comprehensive 10-perspective review
/pb-review-code      Code cleanup, repo health
/pb-review-tests     Test suite quality
/pb-review-docs      Documentation accuracy
/pb-review-hygiene   Multi-role health check
/pb-review-product   Technical + product review
/pb-review-prerelease Pre-release code review
```

### Reference

```
/pb-guide      Full SDLC guide with tiers and gates
/pb-templates  Templates for commits, phases
/pb-standards  Coding standards and principles
/pb-context    Project context template
```

## Installation

```bash
# Clone the repo
git clone https://github.com/vnykmshr/playbook.git
cd playbook

# Install commands (symlinks to ~/.claude/commands/)
./scripts/install.sh
```

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│  PLANNING          DEVELOPMENT              RELEASE         │
│                                                             │
│  pb-plan    →      pb-start     →        pb-release        │
│  pb-adr            pb-cycle               pb-incident       │
│                    pb-resume                                │
│                    pb-pr                                    │
│                                                             │
│                         ↓                                   │
│                    MAINTENANCE                              │
│                    pb-review-* (periodic)                   │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
/pb-plan      # Plan a feature
/pb-start     # Create branch, establish rhythm
/pb-cycle     # Develop → Review → Commit (repeat)
/pb-pr        # Create pull request
/pb-release   # Deploy to production
```

## Directory Structure

```
playbook/
├── commands/
│   ├── core/           # pb-guide, pb-templates, pb-standards
│   ├── planning/       # pb-plan, pb-adr
│   ├── development/    # pb-start, pb-cycle, pb-resume, pb-pr
│   ├── release/        # pb-release, pb-incident
│   ├── reviews/        # pb-review-*
│   └── templates/      # pb-context
├── docs/               # Documentation
├── scripts/            # Install/uninstall scripts
└── todos/              # Dev-only tracking (gitignored)
```

## Uninstall

```bash
./scripts/uninstall.sh
```

## License

MIT
