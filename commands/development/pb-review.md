---
name: "pb-review"
title: "Automated Quality Gate"
category: "development"
difficulty: "beginner"
model_hint: "haiku"
execution_pattern: "automatic"
related_commands: ['pb-start', 'pb-commit', 'pb-preferences', 'pb-linus-agent']
last_reviewed: "2026-02-17"
last_evolved: "2026-02-17"
version: "2.1.0"
version_notes: "90% automation: System auto-decides based on preferences. Human only if ambiguous or new."
breaking_changes: []
---
# Automated Quality Gate

**Resource Hint:** haiku — Lightweight automation that applies your preferences and auto-commits after code review.

Run this after you finish coding. System analyzes what you built, applies your established preferences, and commits if everything checks out. Fully automatic. You get a report when done.

**Part of the ritual:** `/pb-start` → code → `/pb-review` (automatic) → done

**Voice:** Prose-driven feedback. Specific reasoning (what matters + why), not diagnostic checklists. See `/docs/voice.md` for how commands communicate.

---

## When to Use

- **After coding session:** Run `/pb-review` to analyze, decide, and auto-commit
- **After fixing feedback:** Run again to re-verify and commit
- **With manual control:** Use `pb-review --no-auto-commit` if you prefer to review the message first
- **To override preferences:** Use `pb-review --override` for edge cases

---

## How It Works

System analyzes your change (LOC, files, domains, complexity, criticality), determines review depth, runs quality checks through your preferences, and auto-commits if everything passes. Your preferences (from `/pb-preferences`) handle 90% of decisions automatically—architecture issues always fixed, performance debt accepted if < 1 hour, security issues never skipped, etc.

Human involvement (your 10%) only happens when an issue doesn't fit your established preferences (genuinely ambiguous), when it finds a new issue type, or when something needs creative judgment. Otherwise: no interaction.

---

## Example: Standard Review (90% automatic)

```
/pb-review
✓ Analyzed: 250 LOC, 3 files, auth flow
✓ Depth: Standard

Issues found:

1. Email service is inline (architecture)
   Your preference: "Extract to service if possible"
   → Auto-fixing: extracting to separate service

2. Token expiration path doesn't handle cache failure (error handling)
   Your preference: "Error handling must be explicit"
   → Auto-fixing: adding explicit error handler

3. Failure paths untested (testing)
   Coverage: 85%
   Your preference: "Defer testing if coverage > 80%"
   → Auto-deferring: gap noted for later

✓ Ready to commit
✓ Committed: abc1234f
  feat(auth): add email verification with retry logic

  Extract email service for reuse, add explicit error handling
  on token expiration. Testing gap deferred (coverage 85%).
```

**Your involvement: 0%** — System handled everything based on your preferences.

---

## Example: Ambiguous Issue (5% human involvement)

```
/pb-review
✓ Analyzed: 180 LOC, 2 files, retry logic
✓ Depth: Standard

⚠ Issue: Complex retry logic with 4 nested loops + 3 state machines

Your preference doesn't quite cover this. The code works, tests pass,
no logic errors. But it's clever—potentially hard to maintain.

Linus recommends: "This is too clever, simplify."

Two paths:
  A: Simplify (~2 hours, low risk, easier maintenance)
  B: Accept (~0 effort, higher maintenance burden later)

What's your call?
```

**Your involvement: 1 minute** — You pick A or B based on your priorities, system proceeds.

---

## Example: Auto-Fix (0% human involvement)

```
/pb-review
✓ Small fix: 30 LOC, 1 file, logging statement
✓ No issues found
✓ Committed: 3c8f9a2d
```

**Total time: Instant** — System handles it, you don't even need to know it ran.

---

## Your Preferences Drive Decisions

Setup once (`/pb-preferences --setup`, takes ~15 minutes). Answer questions about your values: architecture (always fix or threshold?), testing (require 80%+ coverage?), security (zero-tolerance?), performance (benchmark-driven?), etc. System saves your answers.

During `/pb-review`, system matches each issue to your established preference and auto-decides. Architecture coupling found? Your preference says "always fix"—fixed automatically. Performance debt but deadline is tight? Your preference says "threshold<1h"—deferred automatically.

Only asks if the issue doesn't fit your preferences (genuinely ambiguous). You can override if needed (`/pb-review --override`); system learns from it.

---

## Your 10% Involvement

System asks only when genuinely ambiguous:

- **Preference doesn't cover it:** Linus says "simplify this," but your preferences don't address this complexity type. System: "Should we always simplify? [Yes] [No] [Case-by-case]" You pick. System remembers.

- **On the fence:** Coverage is exactly 80.0%—your preference kicks in at 80%, but it's borderline. System: "Fix or defer? [Fix] [Defer]" You decide.

- **New issue type:** System finds something it hasn't seen before (e.g., "thread pool exhaustion risk"). System: "Usually fix these? [Yes] [No]" You answer once. System learns.

Brief, decisive, rare. That's it.

---

## What Happens After Auto-Commit

```
✓ Committed: abc1234f5
  Message: "feat(auth): add email verification with retry logic

  Changes: Endpoint + EmailService + retry with exponential backoff
  Review: Architecture (extracted), Code (error handling), Tests (defer)
  Decisions: Followed preferences, no conflicts
  Pushed to: origin/feature/email-verification"

Next step? /pb-start another feature
Or: Check email to see if this needs peer review (/pb-pr)
```

**The ritual:**
```
/pb-start → code → /pb-review (automatic) → /pb-commit (automatic) → repeat
```

**Or even simpler if you set it up:**
```
/pb-start → code → /pb-review (automatic with auto-commit) → repeat
```

(One command in the middle, everything else is background)

---

## When to Manually Invoke

- **After coding session:** `pb-review`
- **After fixing review feedback:** `pb-review` again
- **If you want to override preferences:** `pb-review --override`
- **To update preferences:** `pb-preferences --setup` (annual refresh)

---

## Integration

**Before:**
- `/pb-start` — Establish scope, set complexity signal

**This command:**
- `/pb-review` — Auto-analyze, auto-decide, auto-commit

**No "after"** — You're done. Ready for `/pb-pr` (peer review by humans) or next work.

---

## The Ritual (Simplified)

```
Your workflow:
/pb-start "what you're building"
[code]
/pb-review
Done. Commit is in remote.

System's workflow:
Analyze → Apply preferences → Consult personas → Auto-decide → Commit
```

**You provide:** 30 seconds of setup per feature
**System provides:** Everything else

---

## Related Commands

- `/pb-start` — Begin work (sets scope signal)
- `/pb-preferences` — Set your decision rules once
- `/pb-commit` — (Usually automatic, but can be manual if you prefer)
- `/pb-pr` — Peer review (next step)

---

*Fully automatic quality gate | 90% system, 10% human | v2.1.0*
