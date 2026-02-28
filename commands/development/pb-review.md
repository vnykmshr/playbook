---
name: "pb-review"
title: "Automated Quality Gate"
category: "development"
difficulty: "beginner"
model_hint: "haiku"
execution_pattern: "automatic"
related_commands: ['pb-start', 'pb-commit', 'pb-review-code', 'pb-review-comprehensive']
last_reviewed: "2026-02-28"
last_evolved: "2026-02-28"
version: "2.3.0"
version_notes: "v2.3.0: Tightened prose -- removed 4 redundant ritual descriptions and duplicate sections. Clarified decision model: clean = auto-commit, issues found = preferences decide, ambiguous = ask. Same behavior, less repetition."
breaking_changes: []
---
# Automated Quality Gate

**Resource Hint:** haiku — Lightweight automation that applies your preferences and auto-commits after code review.

Run this after you finish coding. System analyzes what you built, applies your established preferences, and commits if everything checks out. You get a report when done.

> **Note:** This is the fast quality gate in the `/pb-start` → code → `/pb-review` workflow. For deep, comprehensive project reviews, see `/pb-review-comprehensive`.

**Part of the ritual:** `/pb-start` → code → `/pb-review` → done

**Voice:** Prose-driven feedback. Specific reasoning (what matters + why), not diagnostic checklists. See `/docs/voice.md` for how commands communicate.

**Tool-agnostic:** The quality gate principles (verify outcomes, check code quality, run tests, address feedback) work with any development tool. Claude Code users invoke as `/pb-review`. Using another tool? Read this file as Markdown for the checklist and process. Adapt the execution to your tool. See [`/docs/using-with-other-tools.md`](/docs/using-with-other-tools.md) for examples.

---

## Code Review Family

- **Use `/pb-review`** (YOU ARE HERE) for **fast quality gate** right after coding
- **Use `/pb-review-code`** for **deep review of a specific PR/commit**
- **Use `/pb-review-hygiene`** for **monthly codebase health check**
- **Use `/pb-review-tests`** for **monthly test suite quality check**

---

## How It Works

System analyzes your change (LOC, files, domains, complexity, criticality), determines review depth, and runs quality checks through your preferences (from `/pb-preferences`).

**Three outcomes:**

1. **Clean** — No issues found. Auto-commits and reports.
2. **Issues covered by preferences** — Preferences decide: auto-fix, auto-defer, or auto-accept. Then auto-commits.
3. **Ambiguous** — Issue doesn't fit your preferences, or new issue type. Asks you. Remembers your answer for next time.

Most reviews hit outcome 1 or 2. You only get involved for genuinely ambiguous cases.

---

## Examples

### Clean review (no issues)

```
/pb-review
✓ Analyzed: 30 LOC, 1 file, logging statement
✓ No issues found
✓ Committed: 3c8f9a2d
```

### Issues covered by preferences

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

### Ambiguous issue (asks you)

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

You pick A or B. System remembers for next time.

---

## Preferences

Setup once (`/pb-preferences --setup`, takes ~15 minutes). Answer questions about your values: architecture (always fix or threshold?), testing (require 80%+ coverage?), security (zero-tolerance?), performance (benchmark-driven?), etc.

During `/pb-review`, system matches each issue to your preference and decides. Only asks when genuinely ambiguous:

- **Preference doesn't cover it** — New issue type. You set the precedent, system remembers.
- **Borderline** — Coverage is exactly at your threshold. You decide.
- **Override needed** — Use `pb-review --override` for edge cases.

---

## Usage

- **After coding:** `/pb-review` — primary use case
- **After fixing feedback:** `/pb-review` again to re-verify
- **Manual commit control:** `pb-review --no-auto-commit` to review the message first

---

## Related Commands

- `/pb-start` — Begin work (sets scope signal)
- `/pb-preferences` — Set your decision rules once
- `/pb-commit` — Usually automatic, but can be manual if you prefer
- `/pb-pr` — Peer review (next step after commit)

---

*Fast quality gate. Preferences decide. You handle the edge cases. | v2.3.0*
