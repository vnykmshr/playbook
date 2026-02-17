---
name: "pb-start"
title: "Start Development Work"
category: "development"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "interactive"
related_commands: ['pb-review', 'pb-commit', 'pb-pause', 'pb-plan']
last_reviewed: "2026-02-17"
last_evolved: "2026-02-17"
version: "2.0.0"
version_notes: "Simplified ritual: adaptive scope detection replaces ceremony. Part of 3-command workflow."
breaking_changes: ["Replaced detailed pre-start checklist with 3-4 adaptive scope questions. Old commands pb-cycle/pb-review-code merged into /pb-review. See MIGRATION section."]
---
# Start Development Work

Begin work on a feature, bug fix, or enhancement. Establishes scope through adaptive questions, then you work. No ceremony—just clarity.

**Part of the ritual:** `/pb-start` → code → `/pb-review` → decide → `/pb-commit`

**Mindset:** Apply `/pb-preamble` thinking (challenge assumptions) and `/pb-design-rules` thinking (verify clarity, simplicity, robustness). This command ensures you know *what* success looks like before writing code.

**Resource Hint:** sonnet — Scope detection and branch setup

---

## When to Use

- Starting any new work (feature, fix, refactor)
- Need to clarify scope before coding
- Picking up work after a break (pair with `/pb-resume`)

---

## The Quick Start: 5 Minutes

```
/pb-start "feature name"
  ↓ System asks 3-4 adaptive questions
  ↓ You answer (1-2 min)
  ↓ Branch created, scope detected
  ↓ You code
```

**Questions the system will ask (adaptive based on your answers):**

1. **What are you building?** (1-line outcome, not solution)
   - *Example:* "Users can reset passwords via email link"
   - *Not:* "Implement password reset endpoint"

2. **How complex is this?** (Files affected? LOC estimate?)
   - *Example:* "~200 LOC, 3 files, touches auth + email"
   - System uses this to detect depth: small/medium/large

3. **Is this on critical path?** (production feature? security? payment?)
   - *Example:* "Yes, payment processing" or "No, nice-to-have"
   - System uses this to detect: lean/standard/deep review later

4. **Any blockers right now?** (If any, resolve before starting)
   - *Example:* "Need staging DB access" or "None"
   - System: Pause if blockers exist, otherwise proceed

---

## What Happens After You Answer

**System detects:**
- Complexity level (small/medium/large)
- Criticality (low/medium/high)
- Domains affected (auth? payment? infra? testing?)

**System creates:**
- Feature branch with naming convention
- Working context snapshot
- Complexity profile stored for `/pb-review` later

**You then:**
- Just code. No more decisions. No ceremony.
- System watches (detects change complexity as you work)

---

## The Ritual is Simple

This command is part of a 3-command ritual:

```
/pb-start [what you're building]
  ↓ Answer 3-4 questions
  ↓ Branch created, scope recorded

[You code here—no interruptions]

/pb-review
  ↓ System detects complexity
  ↓ Runs Garry's framework at right depth
  ↓ Consults personas automatically
  ↓ Presents recommendation
  ↓ You decide: Ready to commit? Fix issues? Questions?

/pb-commit
  ↓ Auto-drafts message with reasoning
  ↓ Captures your decisions from /pb-review
  ↓ Commits and pushes
```

**Total cognitive load: 3 commands.** That's a habit.

---

## Pro Tips

**Before you start:**
- Read the outcome question carefully. "What are you building?" means *outcome*, not solution
- Be honest about complexity. Small estimate = lean review. Large = deep review.
- If blockers exist, resolve them now, don't start coding with unknowns

**After branch is created:**
- Just code. Don't think about the ritual yet.
- System is watching (tracking your changes)
- When done, run `/pb-review`

---

## Branch Naming

System auto-creates branch with conventional naming:
- `feature/short-description` for new features
- `fix/issue-description` for bug fixes
- `refactor/what-changed` for refactoring

You don't need to think about this.

---

## Migration from Old Workflow

**If you've used the playbook before, here's what changed:**

| Old | New |
|-----|-----|
| `/pb-start` (long ceremony) | `/pb-start` (3-4 questions, 2 min) |
| `/pb-cycle` (self-review) | `/pb-review` (auto-detects depth) |
| `/pb-review-code` (peer review) | Built into `/pb-review` |
| `/pb-security`, `/pb-performance` | Consulted automatically by `/pb-review` |
| Manual persona selection | Automatic (system decides who to consult) |

**No more commands to remember: just `/pb-start`, `/pb-review`, `/pb-commit`.**

---

## Related Commands

- `/pb-review` — Quality gate (the second part of the ritual)
- `/pb-commit` — Make the commit (the third part)
- `/pb-pause` — Pause work, save context
- `/pb-resume` — Get back into context
- `/pb-plan` — Plan architecture before starting (optional, for complex work)

---

*One ritual. Three commands. Automagic depth detection. Quality by default.*
