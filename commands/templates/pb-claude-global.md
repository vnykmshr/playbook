---
name: "pb-claude-global"
title: "Generate Global CLAUDE.md"
category: "templates"
difficulty: "beginner"
model_hint: "haiku"
execution_pattern: "sequential"
related_commands: ['pb-claude-project', 'pb-claude-orchestration', 'pb-preamble', 'pb-design-rules', 'pb-standards']
tags: ['design', 'testing', 'security', 'workflow', 'review']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Generate Global CLAUDE.md

Generate or regenerate the global `~/.claude/CLAUDE.md` file from Engineering Playbook principles.

**Purpose:** Create a concise, authoritative context file that informs Claude Code behavior across ALL projects.

**Philosophy:** Playbooks are the source of truth. Global CLAUDE.md is a derived artifact—concise, with references to playbooks for depth.

**Resource Hint:** sonnet — template generation from existing playbook content.

---

## When to Use

- Initial setup of Claude Code environment
- After significant playbook updates (new version release)
- When you want to refresh/realign Claude Code behavior
- Periodically (monthly) to ensure alignment with evolving practices

---

## Generation Process

### Step 1: Read Source Playbooks

Read these playbooks to extract key principles:

```
/pb-preamble              → Collaboration philosophy
/pb-design-rules          → Technical design principles
/pb-standards             → Coding standards
/pb-commit                → Commit conventions
/pb-pr                    → PR practices
/pb-guide                 → SDLC framework overview
/pb-cycle                 → Development iteration pattern
/pb-claude-orchestration  → Model selection and resource efficiency
```

### Step 2: Generate CLAUDE.md

Create `~/.claude/CLAUDE.md` with this structure:

```markdown
# Development Guidelines

> Generated from Engineering Playbook vX.Y.Z
> Source: https://github.com/vnykmshr/playbook
> Last generated: YYYY-MM-DD

---

## How We Work (Preamble)

- **Challenge assumptions** — Correctness matters more than agreement
- **Think like peers** — Best ideas win regardless of source
- **Truth over tone** — Direct feedback beats careful politeness
- **Explain reasoning** — Enable intelligent challenge
- **Failures teach** — When blame is absent, learning happens

For full philosophy: `/pb-preamble`

---

## What We Build (Design Rules)

| Cluster | Core Principle |
|---------|----------------|
| **CLARITY** | Obvious interfaces, unsurprising behavior |
| **SIMPLICITY** | Simple design first, complexity only where justified |
| **RESILIENCE** | Fail loudly, recover gracefully |
| **EXTENSIBILITY** | Adapt without rebuilds, stable interfaces |

For full design rules: `/pb-design-rules`

---

## Guardrails

- **Verify before done** — "It should work" is not acceptable; test the change
- **Preserve functionality** — Never fix a bug by removing a feature
- **Plan multi-file changes** — Outline approach for cross-file work, confirm before acting
- **Git safety** — Pull before writing, use Edit over Rewrite, diff after changes

---

## Quality Bar (MLP)

Before declaring done, ask:
- Would you use this daily without frustration?
- Can you recommend it without apology?
- Did you build the smallest thing that feels complete?

If no: keep refining. If yes: ship it.

---

## Code Quality

- **Atomic changes** — One concern per commit, one concern per PR
- **No dead code** — Delete unused code, don't comment it out
- **No debug artifacts** — Remove console.log, print statements before commit
- **Tests for new functionality** — Coverage for happy path + key edge cases
- **Error handling** — Fail loudly, no silent swallowing of errors
- **Security awareness** — No hardcoded secrets, validate inputs at boundaries

For detailed standards: `/pb-standards`

---

## Commits & PRs

**Commits:** Conventional format (`<type>(<scope>): <subject>`), atomic, explain WHY not what, present tense. Types: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `perf:`. For detailed guidance: `/pb-commit`

**PRs:** One concern per PR. Summary (what + why), Changes, Test Plan. Self-review before requesting review. Squash merge. For detailed guidance: `/pb-pr`

---

## Development Workflow

1. `/pb-start` or `/pb-resume` — Begin or resume work
2. `/pb-cycle` — Iterate: code → self-review → refine
3. `/pb-commit` — Atomic, well-explained commits
4. `/pb-pr` — Create PR when ready

**Non-negotiables:** Never ship known bugs. Never skip testing. Never ignore warnings.

---

## Context & Resource Efficiency

### Model Selection

| Tier | Model | Use For |
|------|-------|---------|
| Architect | opus | Planning, architecture, security deep-dives, critical reviews |
| Engineer | sonnet | Code implementation, test writing, routine reviews |
| Scout | haiku | File search, validation, formatting, status checks |

When unsure, start with sonnet. Upgrade if results lack depth. Downgrade if task is mechanical.

### Context Efficiency

- **Subagents for exploration** — Separate context window, doesn't pollute main
- **Surgical file reads** — Specify line ranges when you know the area
- **Plans in files** — Reference by path, don't paste into chat
- **Commit frequently** — Each commit is a context checkpoint

### Continuous Improvement

Record operational learnings in auto-memory. Surface playbook gaps when discovered. Propose improvements — don't self-modify silently.

For detailed guidance: `/pb-claude-orchestration`

---

## Quick Reference

| Situation | Command |
|-----------|---------|
| Starting new work | `/pb-start` |
| During development | `/pb-cycle` |
| Ready to commit | `/pb-commit` |
| Creating PR | `/pb-pr` |
| Code review | `/pb-review-code` |
| Security check | `/pb-security` |
| Architecture decision | `/pb-adr` |
| Unsure what's next | `/pb-what-next` |

---

## Project-Specific Overrides

Project-level `.claude/CLAUDE.md` can override or extend these guidelines.
When conflicts exist, project-specific guidance takes precedence.

---

*Regenerate with `/pb-claude-global` when playbooks are updated.*
```

### Step 3: Write the File

Write the generated content to `~/.claude/CLAUDE.md`.

If the file exists, back it up first:
```bash
cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.backup
```

### Step 4: Verify

Confirm the file was written:
```bash
head -20 ~/.claude/CLAUDE.md
```

---

## Output Checklist

After generation, verify:

- [ ] File exists at `~/.claude/CLAUDE.md`
- [ ] Version and date are current
- [ ] All sections are populated
- [ ] Playbook references are correct
- [ ] **File is under 150 lines / 2K tokens** (context efficiency)
- [ ] No duplication of content available in playbooks (reference instead)
- [ ] Context & Resource Efficiency section includes model selection table
- [ ] Continuous improvement directive present (auto-memory, surface gaps)

---

## Customization Points

The generated CLAUDE.md can be manually edited for:

- **Personal preferences** not covered by playbooks
- **Tool-specific settings** (editor, terminal, etc.)
- **Organization-specific standards** beyond playbooks

Mark manual additions clearly so they're preserved on regeneration:

```markdown
## Custom (Manual)
[Your additions here - preserved on regeneration]
```

---

## Maintenance

**When to regenerate:**
- After playbook version updates (v1.5.0 → v1.6.0)
- After adding new playbook commands you want reflected
- Monthly refresh to ensure alignment

**Version tracking:**
The generated file includes version and date. Check periodically:
```bash
head -5 ~/.claude/CLAUDE.md
```

---

## Related Commands

- `/pb-claude-project` — Generate project-specific CLAUDE.md
- `/pb-claude-orchestration` — Model selection and resource efficiency guide
- `/pb-preamble` — Full collaboration philosophy
- `/pb-design-rules` — Complete design rules reference
- `/pb-standards` — Detailed coding standards

---

*This command generates your global Claude Code context from playbook principles.*
