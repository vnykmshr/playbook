---
name: "pb-preferences"
title: "Set Your Decision Rules (One-Time Setup)"
category: "development"
difficulty: "beginner"
model_hint: "haiku"
execution_pattern: "interactive-once"
related_commands: ['pb-review', 'pb-start', 'pb-linus-agent']
last_reviewed: "2026-02-17"
last_evolved: "2026-02-17"
version: "1.0.0"
version_notes: "NEW: Enables 90/10 automation. You set rules once, system applies them forever."
breaking_changes: []
---
# Set Your Decision Rules (One-Time Setup)

**Resource Hint:** haiku — One-time setup (15 minutes) that enables 90% automation forever.

Run this once (or annually) to establish how you want `/pb-review` to auto-decide issues. After this, the system handles 90% of decisions automatically.

**You:** 15 minutes of setup
**System:** Everything else, forever

---

## When to Use

- **First time:** `pb-preferences --setup` (full questionnaire)
- **Annual refresh:** `pb-preferences --review` (revisit decisions)
- **One-off update:** `pb-preferences --adjust [category]` (change one preference)

---

## How It Works

### First Time Setup

```
/pb-preferences --setup
  ↓ System asks 15 questions (takes ~10 min)
  ↓ You answer based on your values
  ↓ Preferences saved
  ↓ /pb-review uses them forever

Example questions:
  1. Architecture issues (e.g., tight coupling): always fix? defer if <1h? accept?
  2. Code quality: strict (fix everything) or pragmatic (accept some debt)?
  3. Testing: require 80%+ coverage? defer gaps if coverage good? accept risk?
  4. Performance: always optimize? accept debt if deadline tight? benchmark first?
  5. Security: zero-tolerance (always fix)? severity-based? case-by-case?
  6. Refactoring: always simplify if possible? defer if working? case-by-case?
  7. Documentation: always complete? defer if clear code? accept gaps?
  8. Breaking changes: auto-rebase before commit? squash? accept?
  9. Commit frequency: after every feature? batch by day? by complexity?
  10. Error handling: strict (all cases) or pragmatic (main paths only)?
  11. Async/concurrency: always add tests? defer if low-risk? accept?
  12. Database: require indexes upfront? performance-driven? accept?
  13. Dependencies: strict (minimize)? pragmatic (use what helps)? accept?
  14. Logging: verbose (capture everything)? selective? minimal?
  15. Deadline pressure: relax standards? compress testing? accept tech debt?
```

### Your Answer Format

For each question, choose:
- **Always** — Auto-fix every time
- **Never** — Auto-defer every time
- **Threshold** — Auto-fix if [condition], otherwise decide case-by-case
- **Case-by-case** — Ask me each time

**Example answer:**
```
Q: "Testing: how strict?"
A: "Threshold: Always fix if coverage < 80%, defer if >= 85%, case-by-case if 80-84%"

Q: "Security: tolerance level?"
A: "Always: Fix security issues regardless of effort"

Q: "Performance: when to optimize?"
A: "Threshold: Auto-fix if effort < 1 hour, case-by-case if longer"

Q: "Breaking changes?"
A: "Case-by-case: Depends on impact"
```

### Preferences Saved

```
.playbook-preferences.yaml
  Architecture:
    tight_coupling: "threshold<1h"
    circular_dependencies: "always"
    single_point_of_failure: "always"
  Code Quality:
    dry_violations: "threshold<30min"
    error_handling: "always"
    variable_naming: "case-by-case"
  Testing:
    coverage_target: 80
    failure_path_coverage: "always"
    edge_cases: "threshold<1h"
  Performance:
    optimization_threshold: 1h
    n_plus_one: "always"
    caching_opportunities: "case-by-case"
  Security:
    input_validation: "always"
    authentication: "always"
    data_access: "always"
  # ... etc
```

---

## Using Your Preferences

### During `/pb-review`

System applies your preferences automatically:

```
Issue: "Architecture: Email service should be extracted"
Your preference: "Architecture: threshold<1h"
Effort estimate: 30 minutes
Decision: AUTO-FIX ✓

Issue: "Testing: Missing edge cases in retry logic"
Your preference: "Testing failure paths: always"
Decision: AUTO-FIX ✓

Issue: "Performance: Consider caching strategy"
Your preference: "Performance optimization: case-by-case"
Decision: ASK YOU ⚠ (brief question)

Issue: "Documentation: Variable naming unclear"
Your preference: "Variable naming: case-by-case"
Decision: ASK YOU ⚠ (brief question)
```

### When System Asks (The 10%)

```
Issue: "Complex retry logic (nested loops + state machine)"
Your preferences don't cover this type of complexity
System: "New issue type: Excessive code complexity. Usually fix? [Always] [Never] [Threshold] [Case-by-case]"
You: "Threshold: Fix if effort < 2h"
System: "This is 1.5 hours. Fixing it."
System: Saves your answer for future
```

### When You Want to Override

```
/pb-review --override "skip-testing-defer"
  ↓ Issue that would normally auto-defer gets fixed
  ↓ System logs: "User overrode preference on [date] for [reason]"
  ↓ Quarterly report shows pattern if it happens often
```

---

## Your Preferences Ladder (Typical)

**Strict Mode** (high quality, longer dev time)
```
Architecture: always fix
Code quality: always fix
Testing: always 80%+ coverage
Performance: always optimize
Security: always fix
Documentation: always complete
```

**Pragmatic Mode** (ship faster, accept debt)
```
Architecture: threshold<1h fix, else defer
Code quality: threshold<30min fix, else case-by-case
Testing: threshold<80% coverage accept, else case-by-case
Performance: threshold<1h optimize, else defer
Security: always fix (never compromise)
Documentation: case-by-case
```

**Balanced Mode** (default)
```
Architecture: always fix if critical, threshold<1h otherwise
Code quality: always fix error handling, threshold<30min else
Testing: require 80%+ coverage, defer gaps if timeline tight
Performance: case-by-case, benchmark if unsure
Security: always fix
Documentation: case-by-case
```

---

## Annual Review

```
/pb-preferences --review
  ↓ System shows what you've decided this past year
  ↓ "Auto-fixed 387 issues, 47 ambiguous cases, 12 overrides"
  ↓ "Most common: error handling (78 fixes), testing (65 defers)"
  ↓ "Do your preferences still align? [Yes] [Adjust] [Reset]"
  ↓ Update any preferences that no longer fit
```

---

## Examples: Setting Preferences

### Example 1: Security-Critical Project

```
Q: Security issues?
A: "Always: Fix everything regardless of effort"

Q: Error handling?
A: "Always: Explicit error handling on all paths"

Q: Testing?
A: "Always: 90%+ coverage required"

Q: Performance?
A: "Threshold: Optimize if < 2h, defer if longer"

Q: Architecture?
A: "Always: Fix assumptions, dependency issues"

Q: Breaking changes?
A: "Always: Proper deprecation path"
```

→ `/pb-review` becomes conservative (fixes almost everything)

---

### Example 2: Startup MVP

```
Q: Security issues?
A: "Always: But only critical (auth, data loss)"

Q: Testing?
A: "Threshold: 60% coverage OK, defer gaps if timeline tight"

Q: Performance?
A: "Case-by-case: Optimize after users find issues"

Q: Architecture?
A: "Threshold: Fix if <30min, defer if longer"

Q: Code quality?
A: "Pragmatic: Fix DRY if reused 3+times, else skip"

Q: Documentation?
A: "Never: Code is self-documenting enough for MVP"
```

→ `/pb-review` becomes lenient (ships fast, fixes only critical)

---

### Example 3: Your Playbook (Recommended)

```
Q: Architecture?
A: "Always: Fix assumptions, dependencies, scaling"

Q: Code quality?
A: "Always: Error handling, DRY where it matters"

Q: Testing?
A: "Threshold: 80%+ coverage, defer if deadline < 1h away"

Q: Performance?
A: "Case-by-case: Benchmark first, then decide"

Q: Security?
A: "Always: Never compromise"

Q: Documentation?
A: "Always: Clear code + minimal docs for complex parts"

Q: Breaking changes?
A: "Always: Deprecation path required"
```

→ `/pb-review` enforces quality by default, pragmatic on timeline

---

## Quick Setup (5 Minutes)

**If you want fast setup:**

```
/pb-preferences --template "balanced"
  ↓ System loads balanced defaults
  ↓ You review, adjust key ones
  ↓ Done

Default categories to adjust:
  - Security: [Your tolerance]
  - Performance: [Your threshold]
  - Testing: [Your coverage target]
  - Deadline: [Your pressure point]
```

---

## What Gets Saved

```
~/.playbook-preferences.yaml
  version: 1.0
  last_updated: 2026-02-17
  preset: "balanced"

  Architecture:
    - issue_type: "tight_coupling"
      rule: "threshold<1h"
    - issue_type: "single_point_of_failure"
      rule: "always"
    # ...

  CodeQuality:
    - issue_type: "dry_violations"
      rule: "threshold<30min"
    # ...

  Testing:
    - issue_type: "coverage_gaps"
      rule: "threshold>80"
    # ...
```

This file is checked into your `.claude/` directory (not repo) so it persists.

---

## Integration

**One-time:**
- `/pb-preferences --setup` (15 min)

**Then forever:**
- `/pb-review` uses your preferences
- System auto-decides 90% of issues
- You only decide truly ambiguous cases

**Annual:**
- `/pb-preferences --review` (5 min, optional adjustment)

---

## The Philosophy

**Goal:** Codify your values into decision rules.

- **Quality standards** don't change per-commit (captured in preferences)
- **Deadlines don't override standards** (preferences handle timeline tension)
- **Automation doesn't mean mediocrity** (your preferences enforce quality)
- **Human judgment matters** (only for genuinely ambiguous cases)

**Result:** Consistency, speed, quality. Pick two? No. Get all three.

---

## Related Commands

- `/pb-review` — Uses these preferences to auto-decide
- `/pb-start` — Establishes scope (feeds into depth detection)
- `/pb-linus-agent` — For deep dives if preferences don't cover something

---

*One-time setup enables automagic forever | v1.0.0*
