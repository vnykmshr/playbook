---
name: "pb-start"
title: "Start Development Work"
category: "development"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "interactive"
related_commands: ['pb-review', 'pb-pr', 'pb-pause', 'pb-resume', 'pb-plan']
last_reviewed: "2026-11-06"
version: "2.3.3"
version_notes: "v2.3.3: The ritual is README's: /pb-start, code, /pb-review (which commits), /pb-pr; /pb-commit is the manual path. The size signal sets review depth and is not /pb-guide's change tier; Related lists /pb-pr in place of /pb-commit."
breaking_changes: ["Replaced detailed pre-start checklist with 3-4 adaptive scope questions. Old commands pb-cycle/pb-review-code merged into /pb-review. See MIGRATION section."]
---
# Start Development Work

Begin work on a feature, bug fix, or enhancement. Establishes scope through adaptive questions, then you work. No ceremony - just clarity.

**Part of the ritual:** `/pb-start` → code → `/pb-review` (commits) → `/pb-pr`

**Mindset:** Apply `/pb-preamble` thinking (challenge assumptions) and `/pb-design-rules` thinking (verify clarity, simplicity, robustness). This command ensures you know *what* success looks like before writing code.

**Resource Hint:** sonnet - Scope detection and branch setup

**Tool-agnostic:** This command works with any development tool or agentic assistant. Claude Code users invoke as `/pb-start`. Using another tool? Read this file as Markdown and work through the phases with your tool. See [`/docs/using-with-other-tools.md`](../../docs/using-with-other-tools.md) for adaptation examples.

---

## When to Use

- Starting any new work (feature, fix, refactor)
- Need to clarify scope before coding
- Picking up work after a break (pair with `/pb-resume`)

---

## The Quick Start: 2 Minutes

```
/pb-start "feature name"
  ↓ System asks a few adaptive questions
  ↓ You answer (1-2 min)
  ↓ Branch created, scope detected
  ↓ You code
```

**What the conversation looks like:**

The system asks clarifying questions naturally, like a peer reviewing your approach before you dive in. Adapt to what you describe:

1. **What are you building?** (outcome, not solution)
   - You: "Users can reset passwords via email"
   - System uses this to understand scope

2. **How complex?** (files and LOC estimate)
   - You: "~200 LOC, 3 files, touches auth + email"
   - System detects: small/medium/large, which sets review depth (not `/pb-guide`'s XS-L change tiers)

3. **Scope mode?** (expanding, holding, or reducing)
   - **Expanding:** New capability - building something that doesn't exist yet
   - **Holding:** Hardening - bulletproofing, fixing, improving what exists
   - **Reducing:** Surgical minimalism - removing, simplifying, cutting scope
   - System adjusts review expectations: expanding gets architecture review, holding gets correctness review, reducing gets regression review

4. **Critical path?** (production, security, payment, or nice-to-have)
   - You: "Payment processing, yes"
   - System prepares review depth accordingly

5. **How will you know it's done?** (verifiable success criteria)
   - You: "Tests pass, can reset password end-to-end in staging"
   - System records criteria; `/pb-review` verifies against them

6. **Any blockers?**
   - You: "Need staging DB access" or "None"
   - System pauses if blockers exist, otherwise proceeds

---

## After You Answer

System detects complexity level, criticality, and affected domains. Creates a feature branch with conventional naming, saves your scope and success criteria for `/pb-review` later, then gets out of your way. You code. No more decisions, no ceremony.

See `/pb-llm-guidelines` §4 for the goal-driven execution pattern: strong success criteria let you loop independently; weak criteria require constant clarification.

---

## The Ritual is Simple

This command is part of a 3-command ritual:

```
/pb-start [what you're building]
  ↓ Answer a few questions
  ↓ Branch created, scope recorded

[You code here-no interruptions]

/pb-review
  ↓ Detects review depth from your change
  ↓ Consults personas automatically
  ↓ Clean? Auto-commits. Issues? Preferences decide.
  ↓ Ambiguous? Asks you, then commits.

/pb-pr
  ↓ Opens the PR for peer review
```

`/pb-commit` is the manual commit, for when you want control; `/pb-review` usually commits for you.

**Total cognitive load: 3 commands.** That's a habit.

---

## Pro Tips

**Before you start:**
- Read the outcome question carefully. "What are you building?" means *outcome*, not solution
- Be honest about complexity. Small estimate = lean review. Large = deep review.
- If blockers exist, resolve them now, don't start coding with unknowns

**After branch is created:**
- Just code. Don't think about the ritual yet.
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
| `/pb-start` (long ceremony) | `/pb-start` (a few questions, 2 min) |
| `/pb-cycle` before every commit | `/pb-review`; `/pb-cycle` stays for guided self-review |
| `/pb-review-code` on every change | `/pb-review`; `/pb-review-code` for a deep PR review |
| `/pb-security`, `/pb-performance` | Consulted automatically by `/pb-review` |
| Manual persona selection | Automatic (system decides who to consult) |

**No more commands to remember: just `/pb-start`, `/pb-review`, `/pb-pr`.**

---

## Related Commands

- `/pb-review` - Quality gate (the second part of the ritual)
- `/pb-pr` - Open the PR (the third part of the ritual)
- `/pb-pause` - Pause work, save context
- `/pb-resume` - Get back into context
- `/pb-plan` - Plan architecture before starting (optional, for complex work)

---

*One ritual. Three commands. Automagic depth detection. Quality by default.*
