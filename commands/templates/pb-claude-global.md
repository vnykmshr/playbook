# Generate Global CLAUDE.md

Generate or regenerate the global `~/.claude/CLAUDE.md` file from Engineering Playbook principles.

**Purpose:** Create a concise, authoritative context file that informs Claude Code behavior across ALL projects.

**Philosophy:** Playbooks are the source of truth. Global CLAUDE.md is a derived artifact—concise, with references to playbooks for depth.

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
/pb-preamble          → Collaboration philosophy
/pb-design-rules      → Technical design principles
/pb-standards         → Coding standards
/pb-commit            → Commit conventions
/pb-pr                → PR practices
/pb-guide             → SDLC framework overview
/pb-cycle             → Development iteration pattern
```

### Step 2: Generate CLAUDE.md

Create `~/.claude/CLAUDE.md` with this structure:

```markdown
# Development Guidelines

> Generated from Engineering Playbook vX.Y.Z
> Source: https://github.com/vnykmshr/playbook
> Last generated: YYYY-MM-DD

---

## How We Work Together (Preamble)

[Extract 5-7 key principles from /pb-preamble]

- **Challenge assumptions** — Correctness matters more than agreement
- **Think like peers** — Best ideas win regardless of source
- **Truth over tone** — Direct feedback beats careful politeness
- **Explain reasoning** — Enable intelligent challenge
- **Failures teach** — When blame is absent, learning happens

For full philosophy: `/pb-preamble`

---

## What We Build (Design Rules)

17 classical design principles in 4 clusters:

| Cluster | Core Principle |
|---------|----------------|
| **CLARITY** | Obvious interfaces, unsurprising behavior, self-documenting code |
| **SIMPLICITY** | Simple design first, complexity only where justified |
| **RESILIENCE** | Fail loudly, recover gracefully, no silent failures |
| **EXTENSIBILITY** | Adapt without rebuilds, stable interfaces |

For full design rules: `/pb-design-rules`

---

## Code Quality Standards

[Extract from /pb-standards, /pb-guide]

- **Atomic changes** — One concern per commit, one concern per PR
- **No dead code** — Delete unused code, don't comment it out
- **No debug artifacts** — Remove console.log, print statements before commit
- **Tests for new functionality** — Coverage for happy path + key edge cases
- **Error handling** — Fail loudly, no silent swallowing of errors
- **Security awareness** — No hardcoded secrets, validate inputs at boundaries

For full standards: `/pb-standards`

---

## Commits

[Extract from /pb-commit]

**Format:** Conventional commits
```
<type>(<scope>): <description>

[optional body explaining WHY]
```

**Types:** `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `perf:`

**Principles:**
- Atomic — One logical change per commit
- Explain WHY, not just WHAT
- Present tense ("add feature" not "added feature")
- Reference issues when relevant

For detailed guidance: `/pb-commit`

---

## Pull Requests

[Extract from /pb-pr]

**Structure:**
```
## Summary
[1-3 bullet points: what and why]

## Changes
[Key changes, not line-by-line]

## Test Plan
[How to verify this works]
```

**Principles:**
- One concern per PR
- Self-review before requesting review
- Respond to all review comments
- Squash merge to keep history clean

For detailed guidance: `/pb-pr`

---

## Development Workflow

**Daily rhythm:**
1. `/pb-start` or `/pb-resume` — Begin or resume work
2. `/pb-cycle` — Iterate: code → self-review → refine
3. `/pb-commit` — Atomic, well-explained commits
4. `/pb-pr` — Create PR when ready

**Planning:**
- `/pb-plan` — Scope and phase planning
- `/pb-adr` — Architecture decisions
- `/pb-patterns-*` — Reference patterns

**Quality gates:**
- `/pb-review-cleanup` — Code quality checklist
- `/pb-security` — Security checklist
- `/pb-testing` — Test coverage guidance

**Unsure what to do?**
- `/pb-what-next` — Context-aware recommendations

---

## Quick Reference

| Situation | Command |
|-----------|---------|
| Starting new work | `/pb-start` |
| Resuming after break | `/pb-resume` |
| During development | `/pb-cycle` |
| Ready to commit | `/pb-commit` |
| Creating PR | `/pb-pr` |
| Code review | `/pb-review-cleanup` |
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
- [ ] File is under 300 lines (concise)

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
- `/pb-preamble` — Full collaboration philosophy
- `/pb-design-rules` — Complete design rules reference
- `/pb-standards` — Detailed coding standards
- `/pb-guide` — Full SDLC framework

---

*This command generates your global Claude Code context from playbook principles.*
