# Engineering Playbook

A comprehensive, integrated set of commands and guides for structuring iterative development workflows, architectural decisions, code reviews, and team operations.

[![Latest Release](https://img.shields.io/github/v/release/vnykmshr/playbook?label=v1.2.0)](https://github.com/vnykmshr/playbook/releases/tag/v1.2.0)
[![Commands](https://img.shields.io/badge/status-active-brightgreen)](docs/command-index.md)
[![Documentation](https://img.shields.io/badge/docs-integration%20guide-blue)](docs/integration-guide.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Overview

The Engineering Playbook is a **decision framework** that codifies how to approach development work—from planning through production operations. It's not a tool; it's a set of structured, well-documented processes that work together to reduce friction, prevent common mistakes, and maintain quality at every step.

**Who it's for:**
- Teams adopting structured SDLC workflows
- Projects using Claude Code for development
- Organizations wanting repeatable, documented practices
- New team members learning your development culture

**Key capabilities:**
- **Iterative development workflows** — Clear, repeatable patterns from idea to production
- **Quality gates at every step** — Automatic checks before code moves forward
- **Multi-perspective code reviews** — Code, security, product, tests, performance
- **Pattern library** — 39 documented architectural patterns (async, database, distributed systems)
- **Team operations** — Onboarding, knowledge transfer, incident response, retrospectives
- **Repository organization** — Professional structure and documentation

---

## Installation

### Prerequisites

- **Claude Code CLI** (Anthropic's official tool for working with Claude)
- **Git** (for version control)
- **Bash** (for install script)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/vnykmshr/playbook.git
cd playbook

# Run installation script (creates symlinks in ~/.claude/commands/)
./scripts/install.sh

# Verify installation
ls ~/.claude/commands/ | grep pb-
```

All playbook commands are now available in Claude Code.

### Uninstall

```bash
./scripts/uninstall.sh
```

---

## Quick Start: Five Scenarios

### Scenario 1: Starting a New Project

You've decided to build something new. Here's how to establish a strong foundation:

```bash
# Step 1: Plan the project
/pb-plan              # Define scope, success criteria, phases

# Step 2: Set up repository
/pb-repo-init         # Initialize directory structure
/pb-repo-organize     # Clean folder layout
/pb-repo-readme       # Write compelling README

# Step 3: Document architecture
/pb-adr               # Record architectural decisions
/pb-patterns          # Reference relevant patterns

# Step 4: Begin development
/pb-start             # Create feature branch
/pb-cycle             # (Repeat) Self-review → Peer review → Commit
/pb-pr                # Create pull request

# Step 5: Release
/pb-release           # Pre-release checklist
/pb-deployment        # Choose deployment strategy
```

**See**: `/docs/integration-guide.md` for complete workflow with step-by-step guidance

---

### Scenario 2: Adopting Playbook in Existing Project

Your project already has code and processes. Let's integrate the playbook gradually:

```bash
# Step 1: Understand current state
/pb-context           # Document project context and decisions
/pb-review-code       # Audit existing code quality
/pb-review-hygiene    # Identify technical debt

# Step 2: Establish baseline
/pb-standards         # Define working principles for your team
/pb-guide             # Learn the SDLC framework
/pb-templates         # Create commit/PR templates

# Step 3: Begin structured development
/pb-start             # First feature with new workflow
/pb-cycle             # Use quality gates for code review
/pb-commit            # Structured commits

# Step 4: Scale practices
/pb-team              # Team retrospectives
/pb-knowledge-transfer # Document tribal knowledge
/pb-review-*          # Periodic reviews (monthly, quarterly)

# Step 5: Continuous improvement
/pb-incident          # Handle production issues systematically
/pb-adr               # Document major decisions
/pb-performance       # Optimize when needed
```

**See**: `/docs/integration-guide.md` → "Scenario 2: Adopting Playbook"

---

### Scenario 3: Typical Developer Day

You're in the middle of a feature sprint. Here's your daily rhythm:

```bash
# Morning: Get context
/pb-resume            # Recover context from yesterday
/pb-standup           # Write async standup for team

# Development: Code → Review → Commit (repeat)
/pb-cycle             # Self-review changes
  # Includes: /pb-testing, /pb-security, /pb-standards, /pb-documentation

/pb-commit            # Atomic, well-explained commit

# Before lunch: Big picture
/pb-context           # Refresh project context (decisions, roadmap)
/pb-patterns          # Reference patterns for next component

# Afternoon: Ready to merge?
/pb-cycle             # Final self-review
/pb-pr                # Create pull request with context

# End of day: Status
/pb-standup           # Update team on progress, blockers
```

**See**: `/docs/integration-guide.md` → "Workflow 1: Feature Development"

---

### Scenario 4: Code Review

A PR is ready for review. As a reviewer, you can follow a structured approach:

```bash
/pb-review-code       # Code quality checklist
/pb-security          # Security perspective
/pb-review-tests      # Test coverage and quality
/pb-logging           # Logging standards verification
/pb-review-product    # Product alignment (if user-facing)
```

Each command provides a different lens on the same code, catching different categories of issues.

---

### Scenario 5: Incident Response

Production is down. Execute quickly:

```bash
/pb-incident          # Assess severity, choose mitigation
  # Options: Rollback (fastest), Hotfix, Feature disable

/pb-observability     # Monitor recovery

# After incident (within 24h)
/pb-incident          # Comprehensive review
/pb-adr               # Document decision to prevent repeat
```

**See**: `/docs/integration-guide.md` → "Workflow 3: Incident Response"

---

## Command Categories

### Core Foundation (4 commands)
Master SDLC framework, working standards, and templates.

| Command | Purpose |
|---------|---------|
| `/pb-guide` | Full SDLC framework (11 phases, quality gates) |
| `/pb-standards` | Working principles and collaboration norms |
| `/pb-documentation` | Writing technical docs at 5 levels |
| `/pb-templates` | Reusable commit, PR, and testing templates |

### Planning & Architecture (10 commands)
Design systems before implementation.

| Command | Purpose |
|---------|---------|
| `/pb-plan` | Feature/release scope locking and multi-perspective analysis |
| `/pb-adr` | Architecture Decision Records (format, examples, review) |
| `/pb-patterns` | Pattern family overview (async, core, database, distributed) |
| `/pb-patterns-async` | Async patterns (callbacks, promises, job queues, goroutines) |
| `/pb-patterns-core` | Core patterns (SOA, event-driven, circuit breaker) |
| `/pb-patterns-db` | Database patterns (pooling, optimization, sharding) |
| `/pb-patterns-distributed` | Distributed patterns (saga, CQRS, eventual consistency) |
| `/pb-performance` | Performance optimization and profiling |
| `/pb-observability` | Monitoring, observability patterns, and alerting strategy |
| `/pb-deprecation` | Deprecation strategy, communication, and backwards compatibility |

### Development (8 commands)
Iterative feature development with built-in quality gates.

| Command | Purpose |
|---------|---------|
| `/pb-start` | Create feature branch, establish iteration rhythm |
| `/pb-resume` | Get back in context after a break |
| `/pb-cycle` | Self-review + peer review iteration loop |
| `/pb-standup` | Daily async status updates for distributed teams |
| `/pb-commit` | Craft atomic, meaningful commits |
| `/pb-pr` | Streamlined pull request creation |
| `/pb-testing` | Testing philosophy (unit, integration, E2E) |
| `/pb-todo-implement` | Structured implementation with checkpoint approval |

### Code Review & Quality (10 commands)
Multiple perspectives on code quality.

| Command | Purpose |
|---------|---------|
| `/pb-review` | Comprehensive multi-perspective periodic review |
| `/pb-review-code` | Code quality and best practices |
| `/pb-review-product` | Technical + product alignment |
| `/pb-review-tests` | Test suite quality and coverage |
| `/pb-review-docs` | Periodic documentation review (accuracy, completeness, maintenance) |
| `/pb-review-microservice` | Microservice architecture design |
| `/pb-review-hygiene` | Code cleanup and technical debt |
| `/pb-review-prerelease` | Senior engineer final release gate |
| `/pb-security` | Security checklist (quick/standard/deep) |
| `/pb-logging` | Logging standards and structured logging |

### Release & Operations (3 commands)
Safe production deployment and incident response.

| Command | Purpose |
|---------|---------|
| `/pb-release` | Pre-release checks and sign-off |
| `/pb-deployment` | Deployment strategies (blue-green, canary, rolling) |
| `/pb-incident` | Incident assessment and response (P0-P3) |

### Repository Management (6 commands)
Professional repository structure and presentation.

| Command | Purpose |
|---------|---------|
| `/pb-repo-init` | Initialize greenfield project structure |
| `/pb-repo-organize` | Organize and clean repository layout |
| `/pb-repo-readme` | Write high-quality README |
| `/pb-repo-about` | Generate GitHub About section |
| `/pb-repo-blog` | Write technical blog post |
| `/pb-repo-enhance` | Full repository enhancement (combines all above) |

### Team & Growth (2 commands)
Team development and knowledge sharing.

| Command | Purpose |
|---------|---------|
| `/pb-onboarding` | Structured team member onboarding |
| `/pb-team` | Team dynamics, feedback, and retrospectives |
| `/pb-knowledge-transfer` | Knowledge transfer session preparation |

### Reference (1 command)
Project context and reference.

| Command | Purpose |
|---------|---------|
| `/pb-context` | Project context, decision log, current focus |

---

## How It Works: Workflows

### Primary Feature Delivery Workflow

```
PLAN                    DEVELOP                    RELEASE
│                       │                          │
├─ /pb-plan ────────────┼─ /pb-start ──────────────┼─ /pb-release
├─ /pb-adr              │   /pb-cycle (iterate)    ├─ /pb-deployment
├─ /pb-patterns-*       │   ├─ /pb-testing         ├─ /pb-review-prerelease
├─ /pb-observability    │   ├─ /pb-security       └─ Verify in production
└─ /pb-performance      │   ├─ /pb-standards
                        │   └─ /pb-documentation
                        ├─ /pb-commit
                        └─ /pb-pr (+ reviews)
```

### Command Integration

All commands work together as a **unified system**:

- **Foundation** (`/pb-guide`, `/pb-standards`) — Principles all others implement
- **Hub commands** (`/pb-cycle`, `/pb-plan`) — Central junctions connecting workflows
- **Specialized families** (patterns, reviews, repos) — Grouped for coherence

**See** `/docs/integration-guide.md` for complete integration documentation showing all workflows and command relationships.

---

## Documentation: Finding What You Need

### For Quick Navigation
→ **[Command Index](/docs/command-index.md)** — Browse all commands by category

### For Understanding Workflows
→ **[Integration Guide](/docs/integration-guide.md)** — How commands work together
- 5 complete workflows with step-by-step execution
- 8 command clusters (groups that work together)
- Reference matrix showing which commands integrate
- Scenario-based selection guide

### For Integration Best Practices
→ **[Integration Summary](/docs/INTEGRATION-SUMMARY.md)** — How playbook commands integrate cohesively

### For Getting Started
→ **[Scenarios Above](#quick-start-five-scenarios)** — Real-world use cases

---

## Directory Structure

```
playbook/
├── commands/
│   ├── core/           # pb-guide, pb-standards, pb-templates, pb-documentation
│   ├── planning/       # pb-plan, pb-adr, pb-patterns-*, pb-performance, pb-observability
│   ├── development/    # pb-start, pb-cycle, pb-resume, pb-pr, pb-testing, pb-todo-implement, pb-standup
│   ├── release/        # pb-release, pb-incident
│   ├── reviews/        # pb-review-*, pb-security, pb-logging
│   ├── repo/           # pb-repo-*, pb-documentation
│   ├── deployment/     # pb-deployment
│   ├── people/         # pb-onboarding, pb-team, pb-knowledge-transfer
│   └── templates/      # pb-context
│
├── docs/
│   ├── command-index.md           # Quick reference for all commands
│   ├── integration-guide.md        # How commands work together (workflows, clusters)
│   ├── INTEGRATION-SUMMARY.md      # Integration improvements and patterns
│   └── checklists.md               # Reusable quality checklists
│
├── scripts/
│   ├── install.sh                 # Symlink commands to ~/.claude/commands/
│   └── uninstall.sh               # Remove symlinks
│
├── todos/                          # Dev-only tracking (gitignored)
├── README.md                       # This file
└── LICENSE
```

---

## Key Principles

### 1. Quality Gates at Every Step
Never skip the review step. Each iteration includes:
- **Self-review** — You catch your own mistakes first
- **Testing** — Code is tested alongside development
- **Security** — Verified before merging
- **Logging** — Standards checked before production
- **Peer review** — Different perspectives catch different issues

### 2. Logical, Atomic Commits
Small commits that:
- Address one concern
- Are always deployable
- Have clear, explanatory messages
- Maintain git history as documentation

### 3. Multi-Perspective Reviews
Code review isn't one perspective:
- **Code reviewer**: Architecture, patterns, maintainability
- **Security engineer**: Input validation, secrets, auth, cryptography
- **Product**: Does it align with user needs?
- **Test engineer**: Coverage, edge cases, regression tests
- **Performance engineer**: Bottlenecks, optimization opportunities

### 4. Documented Decisions
Every architectural decision is recorded (`/pb-adr`), so future team members understand the "why," not just the "what."

### 5. Structured Processes, Not Rigid Rules
The playbook provides frameworks you adapt to your team's needs, not commandments you follow blindly.

---

## Use Cases

### Perfect for:
- **New teams** — Establish practices from day one
- **Growing teams** — Repeatable processes as you scale
- **Distributed teams** — Async-first practices (standups, KT, reviews)
- **Projects adopting Claude Code** — Workflows designed for AI-assisted development
- **Organizations wanting documented practices** — Knowledge transfer, onboarding, incident response

### ℹ️ Consider alternatives if:
- Your team already has deeply established workflows
- You need language-specific guidance (Go, Python, JavaScript specific commands exist but not all)
- You're looking for IDE plugins or Git integrations

---

## Getting Help

### Documentation
- **[Command Index](/docs/command-index.md)** — Reference all commands
- **[Integration Guide](/docs/integration-guide.md)** — Understand command relationships
- **Individual commands** — Each command file has detailed guidance and examples

### Issues & Feedback
- Report bugs or request features: [GitHub Issues](https://github.com/vnykmshr/playbook/issues)
- Suggest improvements: [GitHub Discussions](https://github.com/vnykmshr/playbook/discussions)

### Contributing
Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) (or reach out for guidelines).

---

## Version History

### v1.2.0 (2026-01-11)
- **Added**: 8 new commands (45 total, was 25 at v1.1.0)
  - `/pb-todo-implement` — Checkpoint-based implementation workflow
  - `/pb-standup` — Async standup template and guidance
  - `/pb-logging` — Logging standards audit
  - `/pb-knowledge-transfer` — KT session preparation
  - `/pb-patterns-async`, `-core`, `-db`, `-distributed` — Pattern family
- **Added**: `/pb-review-microservice` — Microservice review command
- **Enhanced**: `/pb-guide` with async/distributed examples
- **Created**: Comprehensive integration documentation

### v1.1.0 (Initial Release)
- 25 commands covering planning, development, review, and release
- Comprehensive SDLC framework with quality gates
- Multi-perspective code review workflow

---

## License

MIT License — See [LICENSE](LICENSE) for details.

---

## In the Wild

The playbook is designed for:
- **Engineering teams** building with high quality standards
- **Claude Code** users wanting structured SDLC workflows
- **Organizations** codifying development practices

---

**The playbook isn't just documentation—it's a decision framework that makes good development practices the default.**

For quick reference, see [Command Index](/docs/command-index.md).
To understand how commands work together, see [Integration Guide](/docs/integration-guide.md).
