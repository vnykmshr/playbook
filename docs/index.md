# Engineering Playbook

A comprehensive, integrated set of commands and guides for structuring iterative development workflows, architectural decisions, code reviews, and team operations.

[![Latest Release](https://img.shields.io/github/v/release/vnykmshr/playbook?label=v1.2.0)](https://github.com/vnykmshr/playbook/releases/tag/v1.2.0)
[![Commands](https://img.shields.io/badge/status-active-brightgreen)](command-index.md)
[![Documentation](https://img.shields.io/badge/docs-integration%20guide-blue)](integration-guide.md)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/vnykmshr/playbook/blob/main/LICENSE)

---

## What is the Engineering Playbook?

The playbook is a **decision framework** that codifies how to approach development work—from planning through production operations. It's not a tool; it's a set of structured, well-documented processes that work together to reduce friction, prevent common mistakes, and maintain quality at every step.

### For New Teams
Establish engineering practices from day one with clear, repeatable processes covering planning, development, code review, and operations.

### For Growing Teams
Scale your team confidently with documented workflows that maintain quality and culture as you grow.

### For Distributed Teams
Async-first practices designed for distributed teams: standups, knowledge transfer, reviews, and documentation.

---

## Quick Navigation

### I want to...

**[Start a new project →](getting-started.md#scenario-1-starting-a-new-project)**
Set up a strong foundation with architecture, directory structure, and documentation

**[Adopt the playbook in existing code →](getting-started.md#scenario-2-adopting-playbook-in-existing-project)**
Gradually integrate playbook workflows into your current development process

**[Understand daily developer workflow →](getting-started.md#scenario-3-typical-developer-day)**
See how commands work together from morning standup through end-of-day status

**[Review code professionally →](getting-started.md#scenario-4-code-review)**
Use multi-perspective reviews (code, security, product, tests, performance)

**[Respond to production incidents →](getting-started.md#scenario-5-incident-response)**
Handle P0/P1 incidents systematically with assessment, mitigation, and recovery

**[Find a specific command →](decision-guide.md)**
Decision tree showing which command to use for any situation

**[Answer a common question →](faq.md)**
FAQ section covering setup, workflow, integration, and common issues

---

## The 45 Commands

Organized in 9 categories:

| Category | Count | Purpose |
|----------|-------|---------|
| **Core Foundation** | 4 | SDLC framework, standards, templates |
| **Planning & Architecture** | 8 | Design, patterns, decisions |
| **Development** | 8 | Feature development, iteration, reviews |
| **Code Review & Quality** | 9 | Multiple perspectives, quality gates |
| **Release & Operations** | 4 | Deployment, incidents, observability |
| **Repository Management** | 6 | Structure, README, documentation |
| **Team & Growth** | 2 | Onboarding, feedback, growth |
| **Reference** | 1 | Project context |
| **Total** | All | **Unified ecosystem** |

[See full command reference →](command-index.md)

---

## Key Principles

### 1. Quality Gates at Every Step
Never skip review. Every iteration includes self-review, testing, security checks, and peer review.

### 2. Logical, Atomic Commits
Small commits that address one concern, are always deployable, and have clear messages documenting the "why."

### 3. Multi-Perspective Code Review
Code quality, security, product alignment, test coverage, and performance—each perspective catches different issues.

### 4. Documented Decisions
Every architectural decision is recorded, so future team members understand the "why," not just the "what."

### 5. Structured Processes, Not Rigid Rules
The playbook provides frameworks you adapt to your team's needs, not commandments you follow blindly.

---

## How It Works

### Primary Feature Delivery Workflow

```
PLAN                    DEVELOP                    RELEASE
│                       │                          │
├─ /pb-plan             ├─ /pb-start               ├─ /pb-release
├─ /pb-adr              │   /pb-cycle (iterate)    ├─ /pb-deployment
├─ /pb-patterns         │   ├─ /pb-testing        └─ Verify in
├─ /pb-observability    │   ├─ /pb-security          production
└─ /pb-performance      │   └─ /pb-standards
                        ├─ /pb-commit
                        └─ /pb-pr (+ reviews)
```

[See all workflows →](workflows.md)

---

## Getting Started

### Option 1: Just Learning
Start with the [Getting Started guide](getting-started.md) and pick a scenario that matches your situation.

### Option 2: New Project
Follow [Scenario 1: Starting a New Project](getting-started.md#scenario-1-starting-a-new-project) with step-by-step commands.

### Option 3: Existing Project
Follow [Scenario 2: Adopting Playbook](getting-started.md#scenario-2-adopting-playbook-in-existing-project) to integrate gradually.

### Option 4: Need Help
- **[Decision Guide](decision-guide.md)** — Which command should I use?
- **[FAQ](faq.md)** — Common questions and answers
- **[Integration Guide](integration-guide.md)** — How commands work together
- **[Full Command Reference](command-index.md)** — Browse all commands

---

## Installation

### Prerequisites
- Claude Code CLI (Anthropic's official tool for working with Claude)
- Git (for version control)
- Bash (for install script)

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

---

## Philosophy

> **The playbook isn't just documentation—it's a decision framework that makes good development practices the default.**

The Engineering Playbook believes that:

- **Quality shouldn't require heroic effort** — Good processes make quality the default
- **Teams learn faster with documented patterns** — Don't reinvent, iterate on proven approaches
- **Async-first communication scales better** — Document decisions, share knowledge asynchronously
- **Code review catches different issues from different perspectives** — Not just code quality, but security, product fit, tests, and performance
- **Atomic commits maintain useful git history** — History becomes a teaching tool, not noise
- **Documented decisions enable faster iteration** — Future changes understand the "why" behind current decisions

---

## Use Cases

### Perfect For
- **New teams** establishing practices from day one
- **Growing teams** scaling with repeatable processes
- **Distributed teams** needing async-first workflows
- **Projects adopting Claude Code** for AI-assisted development
- **Organizations** wanting documented, transferable practices

### ℹ️ Consider Alternatives If
- Your team has deeply established, different workflows
- You need language-specific frameworks (Go, Python, JavaScript specialization)
- You're looking for IDE plugins or Git integrations

---

## Next Steps

**[Getting Started →](getting-started.md)**
Pick a scenario and follow the step-by-step workflow

**[Decision Guide →](decision-guide.md)**
Find the right command for your situation

**[Command Reference →](command-index.md)**
Browse commands by category

**[Integration Guide →](integration-guide.md)**
Understand how all commands work together as a system

---

## Contributing

The playbook is open source and welcomes contributions.

- **Report bugs or request features** — [GitHub Issues](https://github.com/vnykmshr/playbook/issues)
- **Suggest improvements** — [GitHub Discussions](https://github.com/vnykmshr/playbook/discussions)
- **Contribute documentation** — See [CONTRIBUTING.md](https://github.com/vnykmshr/playbook/blob/main/CONTRIBUTING.md)

---

## License

MIT License — See [LICENSE](https://github.com/vnykmshr/playbook/blob/main/LICENSE) for details.

---

**Last Updated**: 2026-01-11 | **Version**: v1.2.0 | **Commands**: 45 | **Integration**: 9 command clusters
