# Engineering Playbook

A comprehensive, integrated set of commands and guides for structuring iterative development workflows, architectural decisions, code reviews, and team operations.

[![Latest Release](https://img.shields.io/github/v/release/vnykmshr/playbook?label=v1.3.0)](https://github.com/vnykmshr/playbook/releases/tag/v1.3.0)
[![Commands](https://img.shields.io/badge/status-active-brightgreen)](command-index.md)
[![Documentation](https://img.shields.io/badge/docs-integration%20guide-blue)](integration-guide.md)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/vnykmshr/playbook/blob/main/LICENSE)

---

## What is the Engineering Playbook?

The playbook is a **decision framework** that codifies how to approach development work—from planning through production operations. It's not a tool; it's a set of structured, well-documented processes that work together to reduce friction, prevent common mistakes, and maintain quality at every step.

**Built on a core insight:** The quality of development depends less on individual brilliance and more on *how teams think together*. This framework is anchored in the **Preamble** — a set of principles about collaboration that makes psychological safety and correctness the default.

**[Read the full technical narrative →](technical-blog.md)** — Why the playbook exists, how it solves real problems, and how it all works together as an integrated system.

---

## Start Here: The Preamble

Before diving into commands, understand the collaborative philosophy that all playbook commands assume:

- **Challenge assumptions** — Not to be difficult, but because correctness matters more than agreement
- **Think like peers, not hierarchies** — Best ideas win regardless of who suggests them
- **Truth over tone** — Direct, clear feedback beats careful politeness
- **Think holistically** — Optimize for team outcomes, not just individual concerns

Every command in the playbook is designed around these principles. You'll see them in how code reviews work (surface flaws, don't just approve), how decisions are documented (reasoning, so they can be intelligently challenged), and how failures become learning (not blame).

**[Read the complete Preamble Framework →](../commands/core/pb-preamble.md)**

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

**[See playbook in action →](playbook-in-action.md)**
Real-world walkthroughs showing development teams using playbook commands end-to-end

---

## Commands

Organized by category:

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

## Key Principles: Embodying Preamble Thinking

### 1. Challenge is Built Into Process
Quality gates aren't about trust—they're about explicitly inviting challenge:
- **Self-review** challenges your own assumptions
- **Peer review** surfaces risks and flaws
- **Security & testing** represent different expertise challenging the work
- **Decision documentation** makes reasoning explicit so it can be intelligently questioned

**Why this matters:** When review is a gate, not a favor, people feel safe questioning.

### 2. Transparent Reasoning Over Hierarchy
Every command asks "why," not just "what":
- **Commits** explain the reason for the change, not just list files
- **Pull requests** document problems, alternatives, and trade-offs
- **Architecture decisions** record reasoning explicitly
- **Retrospectives** focus on learning, not blame

**Why this matters:** When reasoning is transparent, disagreement becomes productive. You're challenging thinking, not authority.

### 3. Multi-Perspective Review Prevents Authority from Winning
Code review isn't one person's opinion—it's multiple expertise perspectives:
- **Code reviewer**: Architecture, patterns, maintainability
- **Security engineer**: Input validation, secrets, auth, cryptography
- **Product**: Does it align with user needs?
- **Test engineer**: Coverage, edge cases, regression tests
- **Performance engineer**: Bottlenecks, optimization opportunities

**Why this matters:** A junior person's security concern carries weight. A senior person's performance idea gets questioned. Different expertise wins, not different rank.

### 4. Logical, Atomic Commits Enable Learning
Small, well-explained commits:
- Make intent clear (and easy to challenge)
- Keep changes focused for thoughtful review
- Maintain git history as documentation of *why* decisions happened
- Enable understanding when reversals are needed

**Why this matters:** You can learn from history when you can see why decisions were made.

### 5. Structured Processes Enable Autonomy
The playbook provides frameworks, not commandments:
- Frameworks assume you'll challenge and adapt them
- Checklists are starting points, not finish lines
- Patterns are tools to think with, not rules to obey
- Every command includes guidance on when to break the pattern

**Why this matters:** Psychological safety requires autonomy. Rigid rules kill challenge; frameworks enable it.

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

## Philosophy: How Teams Think Together

> **The playbook isn't just documentation—it's a decision framework that makes good development practices the default by making peer thinking the default.**

The Engineering Playbook is built on the insight that **the quality of development depends on how teams think together, not individual brilliance**. This means:

### On Collaboration
- **Challenge is professional, not disrespectful** — Surface flaws because correctness matters, not because you disagree
- **Hierarchy shouldn't determine who's right** — Peer thinking means best ideas win regardless of rank
- **Truth over tone** — Direct feedback beats careful politeness; clarity beats harmony
- **Psychological safety is built, not assumed** — Design processes that invite challenge, visibly reward it, and never punish it

### On Process
- **Quality shouldn't require heroic effort** — Good processes make quality the default
- **Teams learn faster with documented patterns** — Don't reinvent, iterate on proven approaches
- **Async-first communication scales better** — Document decisions, share knowledge asynchronously
- **Code review catches different issues from different perspectives** — Not just code quality, but security, product fit, tests, and performance

### On Learning
- **Atomic commits maintain useful git history** — History becomes a teaching tool, not noise
- **Documented decisions enable faster iteration** — Future changes understand the "why" behind current decisions
- **Failures teach when blame doesn't** — Post-mortems focus on "what did we learn" not "who messed up"

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

**Last Updated**: 2026-01-12 | **Version**: v1.3.0 | **Commands**: 49 | **Integration**: 9 command clusters | **Status**: Production Ready
