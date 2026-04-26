---
name: "pb-review"
title: "Automated Quality Gate"
category: "development"
difficulty: "beginner"
model_hint: "sonnet"
execution_pattern: "automatic"
related_commands: ['pb-start', 'pb-commit', 'pb-review-code', 'pb-review-comprehensive']
last_reviewed: "2026-04-26"
last_evolved: "2026-04-26"
version: "2.6.0"
version_notes: "v2.6.0: Reference global GitHub Artifact Register rule for auto-commit messages via single-line pointer; tighten example body."
breaking_changes: []
---
# Automated Quality Gate

**Resource Hint:** sonnet - Quality gate that applies your preferences, checks LLM trust boundaries, and auto-commits after code review.

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

1. **Clean** - No issues found. Auto-commits and reports.
2. **Issues covered by preferences** - Preferences decide: auto-fix, auto-defer, or auto-accept. Then auto-commits.
3. **Ambiguous** - Issue doesn't fit your preferences, or new issue type. Asks you. Remembers your answer for next time.
4. **Loop detected** - Same issue flagged 3+ times across fix-review cycles. Stop auto-fixing. Surface to user: "This issue has come back 3 times. It may be a design problem, not a code problem. [describe the recurring issue]. Continuing to auto-fix risks masking the root cause." Escalate as a design question, not a code fix.

Most reviews hit outcome 1 or 2. You only get involved for genuinely ambiguous cases or loop detection.

**Pre-check: Diff-aware flow mapping.** Before reviewing, system maps changed files to affected user flows. "This diff touches `auth/` and `email/` - affected flows: login, password reset, signup verification." This focuses review on what the change actually impacts, not the entire codebase.

**LLM trust boundary.** If changes include LLM-generated code (SQL, auth logic, security boundaries, data mutations), system flags for elevated scrutiny. LLM output is untrusted input - validate it at trust boundaries the same way you'd validate user input. Escalates to `/pb-review-code` or `/pb-security` if LLM-generated code touches security-critical paths.

**Critical-severity surfacing.** When a critical-severity finding is detected, system surfaces it individually - one issue at a time, not batched. Critical findings require explicit acknowledgment before proceeding. This prevents critical issues from getting lost in a list of suggestions.

**Commit message register.** Auto-drafted messages follow `~/.claude/CLAUDE.md` § GitHub Artifact Register.

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

  Email service extracted so signup flow can reuse it.
```

### Ambiguous issue (asks you)

```
/pb-review
✓ Analyzed: 180 LOC, 2 files, retry logic
✓ Depth: Standard

⚠ Issue: Complex retry logic with 4 nested loops + 3 state machines

Your preference doesn't quite cover this. The code works, tests pass,
no logic errors. But it's clever-potentially hard to maintain.

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

- **Preference doesn't cover it** - New issue type. You set the precedent, system remembers.
- **Borderline** - Coverage is exactly at your threshold. You decide.
- **Override needed** - Use `pb-review --override` for edge cases.

---

## When to Use

- **After coding:** `/pb-review` - primary use case
- **After fixing feedback:** `/pb-review` again to re-verify
- **Manual commit control:** `pb-review --no-auto-commit` to review the message first

---

## Related Commands

- `/pb-start` - Begin work (sets scope signal)
- `/pb-preferences` - Set your decision rules once
- `/pb-commit` - Usually automatic, but can be manual if you prefer
- `/pb-pr` - Peer review (next step after commit)

---

*Fast quality gate. Preferences decide. You handle the edge cases. | v2.6.0*
