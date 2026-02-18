# Using Playbooks with Other Agentic Tools

These playbooks were designed for Claude Code. They're portable.

The underlying patterns work with **any agentic development tool** — different framework, same thinking.

---

## The Three Layers

### Layer 1: Principles (100% Portable)

**What it is:** How you think together and what you build

- **Preamble:** Challenge assumptions. Prefer correctness over agreement. Think like peers.
- **Design Rules:** Clarity, Simplicity, Resilience, Extensibility. 17 classical principles.
- **BEACONs:** 9 guiding principles for code quality, decision-making, team dynamics

**Portability:** Works in **any tool, any language, any team**. These are universal.

**Usage:** Read `/pb-preamble` and `/pb-design-rules`. Apply them in your workflow, whatever tool you use.

---

### Layer 2: Commands (95% Portable)

**What it is:** 100 structured prompts covering full SDLC (planning → dev → review → ship)

- **Command content:** Universal. Patterns, questions, checklists don't care about your tool.
- **Invocation:** Tool-specific. Claude Code users type `/pb-start`. You adapt to your tool.
- **Metadata:** Structured (Resource Hint, When to Use, Related Commands, etc.) — same everywhere.

**Portability:** Copy the Markdown files. Reference them however your tool surfaces prompts.

**How to use:**
1. Clone the repo: `git clone https://github.com/vnykmshr/playbook.git`
2. Read commands as Markdown: `cat commands/development/pb-start.md`
3. Apply the pattern to your workflow
4. Adapt the invocation to your tool

**Example:**

Claude Code user:
```bash
/pb-start "add user authentication"
```

You (with another tool):
- Open `commands/development/pb-start.md` in your editor
- Copy the questions from "Phase 1: Scope"
- Ask your tool to answer them
- Proceed with the ritual

---

### Layer 3: Integration (Tool-Specific)

**What it is:** How commands surface and integrate with your development environment

**Claude Code features:**
- Skills: `/pb-start` invokes directly in conversation
- Keybindings: Fast shortcuts to common commands
- Context management: Automatic pause/resume, working context snapshots
- Hooks: Advisory warnings when context gets large
- Status line: Token usage visibility

**You (with another tool):** Adapt this layer to your tool's capabilities.

**Examples:**

| Tool Feature | Claude Code | Your Tool |
|--------------|-------------|-----------|
| **Invocation** | Skill (`/pb-start`) | Shell alias, CLI subcommand, web form |
| **Context** | CLAUDE.md, working-context.md | Config files, environment vars, database |
| **Preferences** | `~/.claude/preferences.json` | `~/.config/yourtool/config`, CLI flags |
| **Integration** | Git hooks, keybindings, status line | Whatever makes sense for your platform |

---

## Adaptation Checklist

### 1. Adopt Principles (Zero Work)

Read and internalize:
- [ ] `/pb-preamble` — How your team thinks together
- [ ] `/pb-design-rules` — What you build
- [ ] Apply them to: planning, code review, decision-making, incident response

### 2. Adopt Commands (Low Work)

For each command category you care about:
- [ ] Read the Markdown file
- [ ] Understand the phases/checkpoints
- [ ] Adapt the ritual to your workflow
- [ ] Document how your team invokes it (alias, script, manual, etc.)

**Start with these core commands:**
- `/pb-start` — Begin work (scoping ritual)
- `/pb-cycle` — Self-review and iteration
- `/pb-commit` — Atomic, well-explained commits
- `/pb-review-hygiene` — Code quality checklist
- `/pb-plan` — Focus area planning

### 3. Adapt Integration (Medium Work)

Build tool-specific adapters:
- [ ] How do you invoke playbook commands? (CLI, web UI, editor plugin, manual read, etc.)
- [ ] Where do you store preferences/context? (Config files, environment, database, etc.)
- [ ] How do you get reminders? (Hooks, alerts, dashboard, manual checklist, etc.)
- [ ] How do you preserve context between sessions? (Git, files, tool-native storage, etc.)

---

## Concrete Adaptation Examples

### Example 1: Using with CLI Tool + Git

**Tool:** Command-line based, Git-aware

**Adaptation:**

```bash
# 1. Alias to playbook commands
alias pb-start='cat ~/playbook/commands/development/pb-start.md'
alias pb-cycle='cat ~/playbook/commands/development/pb-cycle.md'

# 2. Create a wrapper script for scope questions
# ~/bin/start-work.sh
#!/bin/bash
echo "=== Scope your work ==="
read -p "What are you building? " description
read -p "Why does this matter? " rationale
# ... (ask remaining questions from pb-start)
git switch -c feature/$description

# 3. Use Git hooks for checkpoints
# .git/hooks/pre-commit
# Verify: has atomic change (one concern)
# Verify: no debug artifacts
# Run: lint, tests

# 4. Environment-based context
# Set these in your shell profile
export PB_WORKING_CONTEXT="$HOME/project/context.md"
export PB_PRINCIPLES="$HOME/playbook/docs/preamble.md"
```

**Invocation:**
```bash
# Start work
start-work.sh

# During development
git diff  # See your atomic change

# Before commit
cat ~/playbook/commands/development/pb-commit.md  # Remind yourself of guidelines

# Code review
cat ~/playbook/commands/reviews/pb-review-hygiene.md  # Copy the checklist
```

---

### Example 2: Using with Web-Based Tool

**Tool:** Web-based IDE or cloud development platform

**Adaptation:**

```
1. Import playbook as documentation
   - Create wiki/docs project in your tool
   - Copy all commands as pages
   - Link navigation between related commands

2. Create templates
   - PR template: Copy from /pb-pr guidance
   - Commit template: Copy from /pb-commit guidance
   - Issue template: Copy from /pb-plan phases

3. Dashboard/checklist
   - Pin key commands (Preamble, Design Rules, pb-cycle)
   - Create quick-reference card for your team

4. Workflows
   - Create automation that suggests relevant command
   - Example: "PR created → suggest /pb-review-code checklist"
```

---

### Example 3: Using with Agent-Specific Tool (e.g., different LLM provider)

**Tool:** Different AI provider with agent/tool APIs

**Adaptation:**

```
1. Load commands as tool definitions
   - Playbook commands → Tool/function definitions
   - Metadata becomes tool descriptions
   - Phases become sequential steps

2. Example: /pb-start as a tool
   Tool: start-work
   Description: "Scope development work. Ask discovery questions."
   Input: Project description
   Output: Scope statement, success criteria, phases
   Next: Suggest /pb-plan if multi-phase

3. Chain tools together
   start-work → plan-focus → implement → review → commit → ship

4. Preserve context differently
   - Each message includes: current phase, why it matters, next checkpoint
   - Agent chooses which command/tool to invoke next
```

---

## What Doesn't Translate (And Why)

### 1. Skill Invocation (`/pb-start`)

Claude Code surface commands as skills. Your tool has different affordances.

**Solution:** Use the closest equivalent (alias, CLI subcommand, web form, manual reference).

### 2. Keybindings

Claude Code offers keyboard shortcuts. Your tool may not support them, or works differently.

**Solution:** Use your tool's native shortcuts, or create a workflow guide for your team.

### 3. Context Bar (Token Usage)

Claude Code shows token usage in a status line. Different tools have different capabilities.

**Solution:** Use your tool's native monitoring (IDE metrics, logs, API dashboards).

### 4. Hooks (Advisory Warnings)

Claude Code warns when context is approaching limits. Your tool may not have this concept.

**Solution:** Manual checkpoint: "Every 1 hour, review context size" or use your tool's alerts.

---

## Quick Reference: Command Mapping

| Claude Code | Your Tool | Rationale |
|------------|-----------|-----------|
| `/pb-start` | Read `pb-start.md`, answer questions, create branch | Scoping ritual is universal |
| `/pb-cycle` | Read `pb-cycle.md`, run lint/tests, review checklist | Self-review pattern is universal |
| `/pb-commit` | Read `pb-commit.md`, write atomic commit with good message | Commit discipline is universal |
| `/pb-plan` | Read `pb-plan.md`, work through discovery/analysis phases | Planning ritual is universal |
| `/pb-review-code` | Read `pb-review-code.md`, use checklist for PR review | Review patterns are universal |

---

## Principles Over Rules

The playbook is built on **principles, not rules**.

- Principle: "Atomic changes are easier to review and revert"
  - Claude Code: Enforce via commit templates
  - Your tool: Enforce via PR naming convention
  - Manual: Document the expectation, review for it

- Principle: "Code quality gates prevent regressions"
  - Claude Code: Automatic lint/test checks
  - Your tool: CI/CD pipeline
  - Manual: Pre-commit checklist

**Bottom line:** Adapt the **mechanism** (how you enforce it) to your tool. Keep the **principle** (why it matters) universal.

---

## Getting Started (Choose Your Path)

### Path A: I Use Claude Code
You're all set. Commands are available as skills. Read the integration guide to understand workflows.

### Path B: I Use Another Tool, Want Full Integration
1. Read `/pb-preamble` and `/pb-design-rules` (15 min)
2. Clone the playbook repo
3. Create adapters for your tool (1-2 hours)
4. Document your team's workflow (30 min)
5. Start using commands for your next project

### Path C: I Want to Explore First
1. Read `/pb-preamble` and `/pb-design-rules`
2. Pick one command (e.g., `/pb-plan`)
3. Read it as Markdown
4. Use it manually for your next project
5. Iterate and adapt as you learn

---

## FAQ

**Q: Will using these commands without Claude Code be awkward?**

A: Not at all. The patterns are the point. How you invoke them is implementation detail. Many teams use similar rituals without special tooling.

**Q: Can I modify commands for my team?**

A: Yes. Fork the repo, adapt to your needs, share with your team. The principles are stable; implementation is flexible.

**Q: Is there a "right" way to integrate with my tool?**

A: No. Whatever makes sense for your team. Some teams use aliases and Markdown. Some build dashboards. Some print them and post them on the wall. All valid.

**Q: Will these playbooks stay useful as tools evolve?**

A: Yes. The principles (Preamble, Design Rules) never change. Commands may be refreshed quarterly. Integration mechanisms (how you invoke them) are tool-specific and always adaptable.

---

**Start here:** Read `/pb-preamble` and `/pb-design-rules`. Everything else flows from there.
