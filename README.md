# Engineering Playbook

A comprehensive, integrated set of commands and guides for structuring iterative development workflows, architectural decisions, code reviews, and team operations.

[![Latest Release](https://img.shields.io/github/v/release/vnykmshr/playbook)](https://github.com/vnykmshr/playbook/releases/latest)
[![Commands](https://img.shields.io/badge/status-active-brightgreen)](docs/command-index.md)
[![Documentation](https://img.shields.io/badge/docs-integration%20guide-blue)](docs/integration-guide.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Overview

The Engineering Playbook is a **decision framework** that codifies how to approach development work—from planning through production operations. It's not a tool; it's a set of structured, well-documented processes that work together to reduce friction, prevent common mistakes, and maintain quality at every step.

**Built on two complementary insights:**

1. **Development quality depends on how teams think together**, not individual brilliance. The playbook anchors this in a philosophy about collaboration—the **Preamble**—that makes psychological safety and correctness the default.

2. **Systems quality depends on sound design principles**, not just clever code. The playbook anchors this in 17 classical design rules—the **Design Rules**—organized into 4 clusters (Clarity, Simplicity, Resilience, Extensibility) that guide every architectural decision.

**Who it's for:**
- Teams wanting to shift from hierarchy-based to peer-based thinking
- Projects using Claude Code for development
- Organizations building cultures where the best ideas win regardless of source
- New team members learning your development culture and decision-making patterns

**Key capabilities (enabled by Preamble + Design Rules):**
- **Psychological safety by design** — Preamble principle: challenge is professional, not disrespectful
- **Transparent decision-making** — Preamble principle: explain reasoning, enable intelligent challenge
- **Clarity-first systems** — Design Rules principle: obvious interfaces, unsurprising behavior
- **Simplicity with robustness** — Design Rules principle: simple design with complexity only where justified
- **Iterative development workflows** — Clear, repeatable patterns from idea to production
- **Quality gates at every step** — Automatic checks before code moves forward
- **Multi-perspective code reviews** — Code, security, product, tests, performance all informed by both frameworks
- **Pattern library** — Comprehensive patterns covering async, core, database, distributed, security, cloud deployment, all embodying design rules
- **Explicit learning culture** — Preamble principle: failures teach when blame doesn't
- **Team operations** — Onboarding, knowledge transfer, incident response, retrospectives built on both frameworks
- **Repository organization** — Professional structure and documentation guided by clarity and representation rules
- **Integrated commands** — Comprehensive guidance from planning through production operations, all referencing both frameworks

---

## Start Here: The Preamble and Design Rules

**Before using any other command, read `/pb-preamble` and `/pb-design-rules`.** Together, they establish the complete framework that all playbook commands assume:

### The Preamble: How Teams Think Together
- Challenge assumptions. Prefer correctness over agreement.
- Think like peers, not hierarchies. Disagreement is professional.
- Truth over tone. Direct, clear feedback beats careful politeness.
- Think holistically. Optimize for outcomes, not just individual concerns.

### Design Rules: What We Build
- 17 classical design principles organized in 4 clusters
- CLARITY: Obvious, unsurprising interfaces and code
- SIMPLICITY: Simple design with complexity only where justified
- RESILIENCE: Reliable systems that fail loudly and recover
- EXTENSIBILITY: Systems designed to adapt without rebuilds

**Why both matter:**
- Preamble thinking without design rules = good collaboration building bad systems
- Design rules without preamble thinking = endless debates about correct design
- Together = better decisions, clearer discussions, systems that scale

Every command in this playbook—from `/pb-guide` to `/pb-cycle` to `/pb-security`—assumes both mindsets. The preamble and design rules are foundational.

**Learning path:**
1. **Read preamble** → Understand how to think together
2. **Read design rules** → Understand what to build
3. **See them together** → Read `/pb-preamble` section I.5 (connection) and `/pb-adr` (decisions using both)
4. **Apply them** → Use as anchor for `/pb-plan`, `/pb-commit`, `/pb-pr`, all review and architecture commands
5. **Use quick references** → `/docs/preamble-quick-ref.md` and `/docs/design-rules-quick-ref.md` for daily lookup

**Key insight:** The preamble + design rules aren't about process—they're about *how* you think and *what* you build together.

---

## Genesis & Hierarchy

### Why This Playbook Exists

Good engineering requires both *how to think together* and *what to build*. Without collaboration principles, teams build wrong things together. Without design rules, teams collaborate well toward poor outcomes. Together: better decisions, better systems, better teams.

### Document Hierarchy

When guidance conflicts, specificity wins:

1. **Project CLAUDE.md** — Project-specific needs take precedence
2. **Global CLAUDE.md** — Personal standards apply across projects
3. **Playbook commands** — Framework defaults

Preamble + Design Rules are foundational. All other commands assume them.

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
/pb-review-hygiene       # Audit existing code quality
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

# End of day: Wrap up
/pb-pause             # Preserve context, update trackers, document state
```

**See**: `/docs/integration-guide.md` → "Workflow 1: Feature Development"

---

### Scenario 4: Code Review

A PR is ready for review. As a reviewer, you can follow a structured approach:

```bash
/pb-review-hygiene       # Code quality checklist
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

> Comprehensive command library organized by category. Key commands shown below.
> See [command-index](https://vnykmshr.github.io/playbook/command-index/) for the complete list.

### Core Foundation
Master SDLC framework, working standards, templates, and thinking partner methodology.

| Command | Purpose |
|---------|---------|
| `/pb-guide` | Full SDLC framework (11 phases, quality gates) |
| `/pb-standards` | Working principles and collaboration norms |
| `/pb-documentation` | Writing technical docs at 5 levels |
| `/pb-templates` | Reusable commit, PR, and testing templates |
| `/pb-think` | Unified thinking partner (modes: ideate, synthesize, refine) |

### Planning & Architecture
Design systems before implementation.

| Command | Purpose |
|---------|---------|
| `/pb-plan` | Feature/release scope locking and multi-perspective analysis |
| `/pb-adr` | Architecture Decision Records (format, examples, review) |
| `/pb-patterns` | Pattern family overview (async, core, database, distributed) |
| `/pb-patterns-async` | Async patterns (callbacks, promises, job queues, goroutines) |
| `/pb-patterns-core` | Core architectural patterns (SOA, event-driven, repository, DTO) |
| `/pb-patterns-resilience` | Resilience patterns (retry, circuit breaker, rate limiting, cache-aside) |
| `/pb-patterns-db` | Database patterns (pooling, optimization, sharding) |
| `/pb-patterns-distributed` | Distributed patterns (saga, CQRS, eventual consistency) |
| `/pb-performance` | Performance optimization and profiling |
| `/pb-observability` | Monitoring, observability patterns, and alerting strategy |
| `/pb-deprecation` | Deprecation strategy, communication, and backwards compatibility |

### Development
Iterative feature development with built-in quality gates.

| Command | Purpose |
|---------|---------|
| `/pb-what-next` | Intelligent recommendations based on your current work state |
| `/pb-start` | Create feature branch, establish iteration rhythm |
| `/pb-resume` | Get back in context after a break |
| `/pb-pause` | Gracefully pause work, preserve context for later |
| `/pb-cycle` | Self-review + peer review iteration loop |
| `/pb-ship` | Complete review suite → PR → merge → release → verify |
| `/pb-standup` | Daily async status updates for distributed teams |
| `/pb-commit` | Craft atomic, meaningful commits |
| `/pb-pr` | Streamlined pull request creation |
| `/pb-testing` | Testing philosophy (unit, integration, E2E) |
| `/pb-todo-implement` | Structured implementation with checkpoint approval |

### Code Review & Quality
Multiple perspectives on code quality.

| Command | Purpose |
|---------|---------|
| `/pb-review` | Orchestrate multi-perspective reviews (Quick/Standard/Deep) |
| `/pb-review-hygiene` | Code quality + operational readiness |
| `/pb-review-product` | Technical + product alignment |
| `/pb-review-tests` | Test suite quality and coverage |
| `/pb-review-docs` | Documentation review (accuracy, completeness, maintenance) |
| `/pb-review-microservice` | Microservice architecture design |
| `/pb-security` | Security checklist (quick/standard/deep) |
| `/pb-logging` | Logging standards and structured logging |
| `/pb-a11y` | Accessibility audit |

### Release & Operations
Safe production deployment and incident response.

| Command | Purpose |
|---------|---------|
| `/pb-release` | Release orchestrator: readiness gate, versioning, deploy trigger |
| `/pb-deployment` | Execute deployment with surgical precision |
| `/pb-incident` | Incident assessment and response (P0-P3) |

### Repository Management
Professional repository structure and presentation.

| Command | Purpose |
|---------|---------|
| `/pb-repo-init` | Initialize greenfield project structure |
| `/pb-repo-organize` | Organize and clean repository layout |
| `/pb-repo-readme` | Write high-quality README |
| `/pb-repo-about` | Generate GitHub About section |
| `/pb-repo-blog` | Write technical blog post |
| `/pb-repo-enhance` | Full repository enhancement (combines all above) |

### Team & People
Team development and knowledge sharing.

| Command | Purpose |
|---------|---------|
| `/pb-onboarding` | Structured team member onboarding |
| `/pb-team` | Team dynamics, feedback, and retrospectives |
| `/pb-knowledge-transfer` | Knowledge transfer session preparation |

### Templates & Reference
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
├─ /pb-plan ────────────┼─ /pb-start ──────────────┼─ /pb-release (orchestrator)
├─ /pb-adr              │   /pb-cycle (iterate)    │   ├─ Readiness gate
├─ /pb-patterns-*       │   ├─ /pb-testing         │   ├─ Version & tag
├─ /pb-observability    │   ├─ /pb-security        │   └─ /pb-deployment
└─ /pb-performance      │   ├─ /pb-standards       └─ Verify in production
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

### For Getting Started
→ **[Scenarios Above](#quick-start-five-scenarios)** — Real-world use cases

---

## Directory Structure

```
playbook/
├── commands/
│   ├── core/           # pb-guide, pb-standards, pb-templates, pb-documentation
│   ├── planning/       # pb-plan, pb-adr, pb-patterns-*, pb-performance, pb-observability
│   ├── development/    # pb-start, pb-cycle, pb-resume, pb-pause, pb-pr, pb-testing, pb-todo-implement
│   ├── deployment/     # pb-deployment, pb-release, pb-incident, pb-dr, pb-sre-practices
│   ├── reviews/        # pb-review-*, pb-security, pb-logging
│   ├── repo/           # pb-repo-*, pb-documentation
│   ├── people/         # pb-onboarding, pb-team, pb-knowledge-transfer
│   └── templates/      # pb-context
│
├── docs/
│   ├── command-index.md           # Quick reference for all commands
│   ├── integration-guide.md        # How commands work together (workflows, clusters)
│   ├── decision-guide.md           # When to use which command
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

## How the Playbook Works: Preamble + Design Rules in Practice

The playbook integrates two frameworks that enable each other:

**Preamble** enables teams to think together: challenge assumptions, prefer correctness, operate as peers.
**Design Rules** guide what to build: clarity, simplicity, robustness, extensibility.

When teams have both, they build systems that are not just technically sound but arrived at through trustworthy processes.

### 1. Preamble: Challenge is Embedded in Process
Quality gates aren't about trust; they're about explicitly inviting challenge:
- **Self-review** — Challenge your own assumptions before others see them
- **Peer review** — Ask reviewers to surface risks, not just approve
- **Security & testing** — Different specialists challenge from different angles
- **Decision documentation** — Record the reasoning so decisions can be intelligently challenged

**Why this matters:** Challenge is not optional. It's built into every workflow. When review is a gate, not a favor, people feel safe questioning.

### 2. Preamble: Transparent Reasoning, Design Rules: Sound Thinking
Every command in the playbook asks "why," not just "what":
- **Commits** — Explain the reason for change AND verify design rules are honored
- **Pull requests** — Document the problem, alternatives, AND trace back to design principles
- **Architecture decisions** — Record trade-offs AND show how design rules informed the choice
- **Retrospectives** — Focus on learning what worked AND why (preamble + design rules both)

**Why this matters:** When reasoning is transparent AND grounded in sound design principles, disagreement becomes productive. You're challenging both thinking AND technical soundness.

### 3. Design Rules: Multi-Perspective Review Prevents Hierarchy from Winning
Code review isn't one person's opinion—it's expertise perspectives checking for design principles:
- **Code reviewer**: Clarity, Modularity (does code embody design rules?)
- **Security engineer**: Robustness, Transparency (secure design, fail loudly)
- **Product**: Simplicity, Clarity (did we build the right thing, simply?)
- **Test engineer**: Robustness, Repair (systems fail loudly, recovery is possible)
- **Performance engineer**: Optimization discipline (measure before optimizing, don't over-engineer)

**Why this matters:** Design rules give reviewers concrete language for critique. A junior person's "this isn't clear" becomes "this violates the Clarity rule." Disagreements are about technical principles, not authority.

### 4. Logical, Atomic Commits Maintain Thinking Quality
Small, well-explained commits:
- Make it easy to understand intent (and challenge it)
- Keep changes focused so review is manageable
- Maintain git history as documentation of *why* decisions happened
- Enable easy reversal if a decision turns out wrong

**Why this matters:** Atomic commits make learning possible. When you can see why a decision was made, you can understand if it was good.

### 4. Preamble + Design Rules: Frameworks Enable Autonomy
The playbook provides frameworks you adapt, not commandments you follow:
- Frameworks assume you'll challenge them (preamble thinking)
- Checklists are starting points, not finish lines
- Patterns are tools to think with, not rules to obey
- Every command includes guidance on when to break the pattern
- Design rules anchor decisions: when you break a pattern, you should have design rules on your side

**Why this matters:** Psychological safety requires autonomy. Rigid rules kill challenge. Frameworks anchored in sound principles enable it. You can say "yes, let's break this pattern" because you can point to why the design rules support that decision.

### 5. Integration: Preamble + Design Rules Work Together
- **Without preamble:** Teams apply design rules but debate endlessly about "correctness"
- **Without design rules:** Teams collaborate well but build systems that are hard to maintain
- **Together:** Teams build systems that are both technically sound AND arrived at through trustworthy processes

Every command in the playbook assumes both frameworks. Both matter. Both are foundational.

---

## Dependency Management

[Dependabot](https://dependabot.com) automatically manages dependencies for npm, pip, Go, and GitHub Actions. See [CONTRIBUTING.md](.github/CONTRIBUTING.md#dependency-management) for review guidelines and [Security Advisories](../../security/dependabot) for vulnerabilities.

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
Contributions are welcome! See [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md) for guidelines.

---

## Version History

### Latest Release

For detailed release notes and full version history, see the [CHANGELOG.md](CHANGELOG.md).

The playbook continues to evolve with new commands and patterns added regularly. See [CHANGELOG.md](CHANGELOG.md) for complete history and feature additions.

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
