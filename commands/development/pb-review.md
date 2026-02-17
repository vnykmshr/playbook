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

Run this after you finish coding. System analyzes change, runs Garry's framework, applies your preferences, and commits if all passes.

**Fully automatic. You don't interact. You get a report when done.**

**Part of the ritual:** `/pb-start` → code → `/pb-review` (automatic) → done

---

## How It Works

### Step 1: System Analyzes Your Change
- LOC, files, domains, complexity, criticality
- Determines review depth (lean/standard/deep)

### Step 2: System Runs Garry's Framework
- Architecture, code quality, tests, performance checks
- Consults personas (Linus, Alex, Jordan, Maya, Sam)
- Finds issues and generates recommendations

### Step 3: System Applies Your Preferences
- You established preferences once (see `/pb-preferences`)
- System uses them to auto-decide each issue:
  - "Always fix architecture issues" → Fixes automatically
  - "Always accept perf debt if < 1 hour" → Defers automatically
  - "Security issues always fix" → Fixes automatically
  - Etc.

### Step 4: System Auto-Commits (If All Pass)
- If all issues resolved by preference rules → Auto-commits
- Message auto-drafted with reasoning
- Pushed to remote
- **You get a notification: "✓ Committed [hash]"**

### Step 5: Human Involvement (Only If Needed)
- **If issue conflicts with preferences** (ambiguous) → Alerts you
- **If new issue type** (not in preferences) → Asks you once
- **If can't auto-fix** (needs creative decision) → Presents options
- Otherwise: No interaction needed

---

## Example: Standard Review (90% automatic)

```
/pb-review
  ↓ System: Analyzing 250 LOC, 3 files, auth flow...
  ↓ System: Depth = STANDARD (no persona wait)
  ↓ System: Running checks...

  Issues found:
  1. Architecture: Email service inline
     → Your preference: "Extract to service if possible"
     → Decision: EXTRACT (auto-fixed in suggestion)

  2. Code quality: Token expiration not handled
     → Your preference: "Error handling must be explicit"
     → Decision: ADD ERROR HANDLER (auto-suggestion)

  3. Testing: Failure paths untested
     → Your preference: "Defer testing if coverage > 80%"
     → Coverage is 85%
     → Decision: DEFER (auto-decided)

  4. Performance: Reasonable
     → No issues

  ✓ READY TO COMMIT

  System: Making suggested fixes + auto-commit
  ✓ Committed: abc1234f
  Message: "feat(auth): add email verification..."
```

**Your involvement: 0%** — System handled everything based on your preferences.

---

## Example: Ambiguous Issue (5% human involvement)

```
/pb-review
  ↓ System: Analyzing...
  ↓ System: Found issue

  Issue: Complex retry logic (4 nested loops, 3 state machines)
  Recommendation: SIMPLIFY
  Your preference: "Simplify if clearly worse"

  ⚠ AMBIGUOUS: Could be simplified OR acceptable complexity
  → Linus recommends: "This is too clever, simplify"
  → Code works, tests pass, no logic errors

  NEEDS HUMAN DECISION:
  - Option A: Simplify (effort: 2 hours, risk: low)
  - Option B: Accept (effort: 0, risk: maintenance burden)

  Waiting for your input...
```

**Your involvement: 1 minute** — Choose A or B, move on.

---

## Example: Auto-Fix (0% human involvement)

```
/pb-review
  ✓ Small fix: 30 LOC, 1 file, logging statement
  ✓ Lean review triggered
  ✓ No issues found
  ✓ Auto-commit

  Committed: 3c8f9a2d
```

**Total time: 30 seconds** — You're not even aware `/pb-review` ran.

---

## Preferences System

**First time setup (one-time):**
```
/pb-preferences --setup
  ↓ System asks 10-15 questions about your values:
    - Architecture issues: always fix? defer if <1h? accept risk?
    - Code quality: strict or pragmatic?
    - Testing: require 80%+ coverage? defer gaps? accept risk?
    - Performance: always optimize? accept technical debt?
    - Security: zero-tolerance? case-by-case?
    - Breaking changes: rebase before commit? squash?
    - Commit frequency: after every change? batch?
  ↓ Preferences saved
```

**During `/pb-review`:**
- System applies your preferences automatically
- Matches each issue type to your established rule
- Only asks if issue doesn't fit your rules

**Override if needed:**
```
/pb-review --override
  ↓ Issue that would normally auto-defer
  ↓ You want to fix it anyway
  ↓ System fixes it, updates preference learning
```

---

## Your 10% Involvement

**When system asks for input:**

1. **Ambiguous decision** (issue doesn't fit your preferences)
   - Linus says: "Simplify this"
   - Your preference doesn't cover this complexity type
   - System: "This is new. Should we always simplify complex logic? [Yes] [No] [Case-by-case]"
   - You pick one
   - System remembers for future

2. **Conflicting signals**
   - Garry's test section: "Missing edge cases"
   - Your preference: "Defer testing if coverage > 80%"
   - But coverage is exactly 80.0%
   - System: "On the fence. Fix it or defer? [Fix] [Defer]"
   - You pick one

3. **New issue type**
   - System finds something it hasn't categorized before
   - System: "Found 'thread pool exhaustion risk'. Usually fix these? [Yes] [No]"
   - You answer once
   - System remembers

**That's your 10%.** Brief, decisive, rare.

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
