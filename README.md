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
/vmx-start-dev       Start work on a feature branch
/vmx-dev-cycle       Self-review + peer review iteration
/vmx-resume-work     Resume after a break
/vmx-quick-pr        Create a pull request
```

### Planning & Architecture

```
/vmx-new-focus-area-generic    Plan a new feature/release
/vmx-adr                       Document architectural decisions
```

### Release & Operations

```
/vmx-make-release        Pre-release checks and deployment
/vmx-incident-response   P0/P1 incident handling
```

### Periodic Reviews

```
/vmx-project-review-periodic     Comprehensive 10-perspective review
/vmx-review-engineer-periodic    Code cleanup, repo health
/vmx-review-tests-periodic       Test suite quality
/vmx-review-docs-periodic        Documentation accuracy
/vmx-review-hygiene-periodic     Multi-role health check
```

### Reference

```
/vmx-engineering-playbook   Full SDLC guide with tiers and gates
/vmx-sdlc-template          Templates for commits, phases
/vmx-project-guidelines     Coding standards and principles
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
│  focus-area   →    start-dev    →       make-release       │
│  adr               dev-cycle             incident-response │
│                    resume-work                              │
│                    quick-pr                                 │
│                                                             │
│                         ↓                                   │
│                    MAINTENANCE                              │
│                    review-* (periodic)                      │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

1. **Planning a feature:**
   ```
   /vmx-new-focus-area-generic
   ```

2. **Starting development:**
   ```
   /vmx-start-dev
   ```

3. **Each iteration (develop → review → commit):**
   ```
   /vmx-dev-cycle
   ```

4. **Creating a PR:**
   ```
   /vmx-quick-pr
   ```

5. **Making a release:**
   ```
   /vmx-make-release
   ```

## Directory Structure

```
playbook/
├── commands/
│   ├── core/           # Foundation (playbook, templates, guidelines)
│   ├── planning/       # Focus areas, ADRs
│   ├── development/    # start-dev, dev-cycle, resume, quick-pr
│   ├── release/        # make-release, incident-response
│   ├── reviews/        # Periodic review commands
│   └── templates/      # working-context-template
├── docs/               # Documentation
├── scripts/            # Install/uninstall scripts
└── todos/              # Dev-only tracking (gitignored)
```

## Customization

Commands use placeholders for project-specific details:

- `[domain]` — Your production domain
- `make` commands — Adapt to your build system
- Branch naming — Adjust patterns as needed

## Uninstall

```bash
./scripts/uninstall.sh
```

## License

MIT
