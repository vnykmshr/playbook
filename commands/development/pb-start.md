---
name: "pb-start"
title: "Start Development Work"
category: "development"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "interactive"
related_commands: ['pb-preamble', 'pb-review', 'pb-commit', 'pb-pause', 'pb-plan']
last_reviewed: "2026-02-18"
last_evolved: "2026-02-18"
version: "2.1.0"
version_notes: "v2.13.1: Added pb-preamble backward reference (Mindset: challenge assumptions before starting)"
breaking_changes: ["Replaced detailed pre-start checklist with 3-4 adaptive scope questions. Old commands pb-cycle/pb-review-code merged into /pb-review. See MIGRATION section."]
---
# Start Development Work

Begin work on a feature, bug fix, or enhancement. Establishes scope through adaptive questions, then you work. No ceremony—just clarity.

**Part of the ritual:** `/pb-start` → code → `/pb-review` → decide → `/pb-commit`

**Mindset:** Apply `/pb-preamble` thinking (challenge assumptions) and `/pb-design-rules` thinking (verify clarity, simplicity, robustness). This command ensures you know *what* success looks like before writing code.

**Resource Hint:** sonnet — Scope detection and branch setup

**Voice:** Conversational. System asks clarifying questions naturally, like a peer reviewing your plan. See `/docs/voice.md` for how commands communicate.

**Tool-agnostic:** This command works with any development tool or agentic assistant. Claude Code users invoke as `/pb-start`. Using another tool? Read this file as Markdown and work through the phases with your tool. See [`/docs/using-with-other-tools.md`](/docs/using-with-other-tools.md) for adaptation examples.

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

**What the conversation looks like:**

The system asks clarifying questions naturally—like a peer reviewing your approach before you dive in. Adapt to what you describe:

1. **What are you building?** (outcome, not solution)
   - You: "Users can reset passwords via email"
   - System uses this to understand scope

2. **How complex?** (files and LOC estimate)
   - You: "~200 LOC, 3 files, touches auth + email"
   - System detects: small/medium/large

3. **Critical path?** (production, security, payment, or nice-to-have)
   - You: "Payment processing, yes"
   - System prepares review depth accordingly

4. **Any blockers?**
   - You: "Need staging DB access" or "None"
   - System pauses if blockers exist, otherwise proceeds

---

## After You Answer

System detects complexity level, criticality, and affected domains. Creates a feature branch with conventional naming, saves your scope for `/pb-review` later, then gets out of your way. You code. No more decisions, no ceremony. System watches in the background, tracking change complexity as you work.

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
