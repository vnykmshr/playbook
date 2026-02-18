# Engineering Playbook

A comprehensive, integrated set of commands and guides for structuring iterative development workflows, architectural decisions, code reviews, and team operations.

[![Latest Release](https://img.shields.io/github/v/release/vnykmshr/playbook)](https://github.com/vnykmshr/playbook/releases/latest)
[![Commands](https://img.shields.io/badge/status-active-brightgreen)](command-index.md)
[![Documentation](https://img.shields.io/badge/docs-integration%20guide-blue)](integration-guide.md)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/vnykmshr/playbook/blob/main/LICENSE)

---

## What is the Engineering Playbook?

The playbook is a **decision framework** that codifies how to approach development work—from planning through production operations. It's not a tool; it's a set of structured, well-documented processes that work together to reduce friction, prevent common mistakes, and maintain quality at every step.

**Built on two complementary insights:**

1. **Development quality depends on how teams think together**, not individual brilliance. The **Preamble** establishes principles about collaboration that make psychological safety and correctness the default.

2. **System quality depends on sound design principles**, not just clever engineering. The **Design Rules** establish 17 classical principles organized in 4 clusters (Clarity, Simplicity, Resilience, Extensibility) that guide every technical decision.

**[Read the full narrative →](why-we-build-playbooks.md)** — Why the playbook exists, how both frameworks solve real problems, and how it all works together as an integrated system.

---

## Start Here: Preamble + Design Rules

The playbook is anchored in two complementary frameworks. Understand both before diving into commands.

### The Preamble: How Teams Think Together

Before diving into commands, understand the collaborative philosophy that all playbook commands assume:

- **Challenge assumptions** — Not to be difficult, but because correctness matters more than agreement
- **Think like peers, not hierarchies** — Best ideas win regardless of who suggests them
- **Truth over tone** — Direct, clear feedback beats careful politeness
- **Think holistically** — Optimize for team outcomes, not just individual concerns

**[Preamble Quick Reference →](preamble-quick-ref.md)** | Full framework: `/pb-preamble`

### Design Rules: What We Build

Technical principles that guide every system decision and architectural choice:

- **4 Clusters of 17 Rules:** CLARITY (obvious, unsurprising), SIMPLICITY (elegant discipline), RESILIENCE (reliable & adaptive), EXTENSIBILITY (future-proof)
- Each rule with clear reasoning, examples, and when to apply
- Decision framework for when rules conflict
- Quick reference for daily use

**[Design Rules Quick Reference →](design-rules-quick-ref.md)** | Full framework: `/pb-design-rules`

### The Two Frameworks Enable Each Other

**What each framework does alone:**
- **Preamble alone:** Teams collaborate well but build systems that are hard to maintain or overly complex
- **Design rules alone:** Clear design goals, but teams debate endlessly about what's "right" without reaching decisions
- **Together:** Teams collaboratively decide on technically sound systems

**How they work together:**
- Preamble gives teams the psychological safety to challenge design decisions openly
- Design rules give teams concrete language for critiquing ideas (not just opinions)
- Preamble ensures disagreement leads to better decisions, not hierarchy wins
- Design rules ensure those decisions are technically sound and maintainable

**In practice:**
- Code review becomes: "Does this embody Clarity and Simplicity?" (design rules) asked safely by peers (preamble)
- Architecture decisions become: "Here's our choice, here's the reasoning, challenge it" (preamble) anchored in principles (design rules)
- Team culture becomes: "We disagree about Robustness trade-offs" (preamble + design rules together enable productive disagreement)

Every command in this playbook assumes both frameworks working together.

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
| **Core Foundation** | 12 | SDLC framework, standards, preamble, design rules |
| **Planning & Architecture** | 16 | Design patterns, ADRs, observability |
| **Development** | 12 | Feature development, iteration, testing |
| **Code Review & Quality** | 11 | Multiple perspectives, quality gates |
| **Release & Deployment** | 8 | Deployment, incidents, DR, SRE practices |
| **Repository Management** | 7 | Structure, README, documentation |
| **Team & People** | 3 | Onboarding, knowledge transfer, team building |
| **Templates** | 3 | Project context, CLAUDE.md generation |
| **Total** | **72** | **Unified ecosystem** |

[See full command reference →](command-index.md)

---

## Key Principles: Embodying Preamble + Design Rules

### 1. Preamble: Challenge is Built Into Process
Quality gates aren't about trust—they're about explicitly inviting challenge:
- **Self-review** challenges your own assumptions (preamble thinking)
- **Peer review** surfaces risks and flaws using design principles as language (design rules)
- **Security & testing** represent different expertise challenging the work professionally (preamble)
- **Decision documentation** makes reasoning explicit so it can be challenged (preamble) and grounded in principles (design rules)

**Why this matters:** When review is a gate, not a favor, people feel safe questioning. When they have design principles to reference, questioning becomes technical, not personal.

### 2. Design Rules: Transparent Reasoning Grounded in Principles
Every command asks "why," not just "what":
- **Commits** explain the reason for change AND which design rules guided it
- **Pull requests** document problems, alternatives, trade-offs, AND how design rules informed choices
- **Architecture decisions** record reasoning AND show which design principles matter most
- **Retrospectives** focus on learning what worked AND why (preamble + design rules)

**Why this matters:** When reasoning is transparent AND grounded in sound design principles, disagreement becomes productive. You're challenging both thinking AND technical soundness.

### 3. Design Rules: Multi-Perspective Review Prevents Authority from Winning
Code review uses design rules as shared language for expertise perspectives:
- **Code reviewer**: Clarity, Modularity — is the code obviously structured?
- **Security engineer**: Robustness, Transparency — does it fail loudly, is the design transparent?
- **Product**: Simplicity, Clarity — did we build the right thing simply?
- **Test engineer**: Robustness, Repair — does it fail loudly, can we recover?
- **Performance engineer**: Optimization discipline — did we measure before optimizing?

**Why this matters:** Design rules give reviewers concrete language. A junior person's "this is confusing" becomes "this violates the Clarity rule." Different expertise wins because it's grounded in technical principles, not rank.

### 4. Preamble + Design Rules: Logical, Atomic Commits Enable Learning
Small, well-explained commits:
- Make intent clear (preamble: easy to challenge) AND grounded in design principles (design rules)
- Keep changes focused for thoughtful review of both reasoning AND technical quality
- Maintain git history as documentation of *why* decisions happened AND what principles mattered
- Enable understanding when reversals are needed (was the principle wrong, or the implementation?)

**Why this matters:** You can learn from history when you can see both the reasoning AND the principles that guided decisions.

### 5. Preamble + Design Rules: Frameworks Enable Autonomy
The playbook provides frameworks, not commandments:
- Frameworks assume you'll challenge and adapt them (preamble)
- Checklists are starting points, not finish lines
- Patterns are tools to think with, not rules to obey
- Design rules anchor decisions: when you break a pattern, you have principles on your side
- Every command includes guidance on when to break the pattern

**Why this matters:** Psychological safety requires autonomy. Rigid rules kill challenge. Frameworks anchored in both peer thinking AND sound design principles enable you to both challenge AND make sound decisions.

### 6. Integration: Preamble + Design Rules Work as One System
The playbook's power comes from both frameworks working together:
- **Preamble without design rules**: Teams collaborate well but debate endlessly about what's "right"
- **Design rules without preamble**: Teams know what's right but can't decide together on it
- **Together**: Teams collaboratively decide on technically sound systems

This integration is woven throughout the playbook. Every command that references the preamble also references design rules. Every code review, every architecture decision, every commit assumes both matter.

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

- **Git** (for version control)
- **Bash** (for install script)
- *(Optional)* **Claude Code CLI** (Anthropic's AI development tool — enables skill invocation)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/vnykmshr/playbook.git
cd playbook

# Run installation script
./scripts/install.sh

# If using Claude Code: symlinks are created in ~/.claude/commands/
# If using another tool: commands are available as Markdown files in ./commands/
```

**With Claude Code:** Commands available as interactive skills (e.g., `/pb-start`)

**Without Claude Code:** Read commands as Markdown files and reference them in your workflow (see [Using Playbooks with Other Tools](using-with-other-tools.md))

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
- **Teams using agentic development tools** optimizing for AI-assisted workflows
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

**Status**: Production Ready | **Integration**: 9 command clusters | [View Changelog](https://github.com/vnykmshr/playbook/blob/main/CHANGELOG.md)
