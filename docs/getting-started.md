# Getting Started with the Engineering Playbook

Welcome to the Engineering Playbook! This guide will help you get up and running quickly.

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

All 45 playbook commands are now available in Claude Code.

### Uninstall

```bash
./scripts/uninstall.sh
```

---

## Quick Start: Five Scenarios

Pick the scenario that matches your situation:

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

**See**: [Integration Guide](integration-guide.md) for complete workflow with step-by-step guidance

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

**See**: [Integration Guide](integration-guide.md) → "Scenario 2: Adopting Playbook"

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

**See**: [Integration Guide](integration-guide.md) → "Workflow 1: Feature Development"

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

**See**: [Integration Guide](integration-guide.md) → "Workflow 3: Incident Response"

---

## Next Steps

### I'm not sure which scenario fits me...
Use the [Decision Guide](decision-guide.md) to find the right command for your situation.

### I need more context...
Read the [Integration Guide](integration-guide.md) to understand how all commands work together.

### I have a specific question...
Check the [FAQ](faq.md) for common questions and answers.

### I want to browse all commands...
See the [Full Command Reference](command-index.md) organized by category.

---

## Key Principles to Remember

### Quality at Every Step
Never skip the review step. Each iteration includes self-review, testing, security checks, and peer review before committing.

### Atomic, Logical Commits
Create small commits that address one concern, are always deployable, and have clear messages explaining the "why."

### Multi-Perspective Reviews
Get feedback from different angles: code quality, security, product alignment, test coverage, and performance.

### Documented Decisions
Record architectural decisions so future team members understand the reasoning, not just the code.

### Processes, Not Rules
Adapt the playbook to your team's needs. These are frameworks, not commandments.

---

## Common Questions

**Q: Do I have to follow the playbook exactly?**
A: No. The playbook provides frameworks and best practices. Adapt them to your team's needs and context.

**Q: Can I integrate the playbook gradually?**
A: Yes! See Scenario 2 (Adopting Playbook in Existing Project) for a gradual integration approach.

**Q: Which scenario should I choose?**
A: Match your situation to the 5 scenarios above. If unsure, start with Scenario 3 (Typical Developer Day) to see how commands work together.

**Q: What if I have other questions?**
A: Check the [FAQ](faq.md) or [open an issue on GitHub](https://github.com/vnykmshr/playbook/issues).

---

## What to Read Next

1. **[Command Reference](command-index.md)** — Browse all 45 commands by category
2. **[Integration Guide](integration-guide.md)** — Understand how commands work together
3. **[Decision Guide](decision-guide.md)** — Find the right command for any situation
4. **[FAQ](faq.md)** — Common questions and troubleshooting
