# Migration Guide: Simplified Ritual (v2.12.0 Phase 4)

**Date:** 2026-02-17
**Version:** v2.12.0
**Change Type:** Workflow redesign (non-breaking)

---

## What Changed

The playbook workflow has been simplified from 97 commands to a **3-command ritual with 90% automation**.

| Old Workflow | New Workflow |
|--------------|--------------|
| `/pb-start` → detailed ceremony | `/pb-start` → 3-4 scope questions (30 sec) |
| `/pb-cycle` → manual review checklist | `/pb-review` → automatic (applies preferences) |
| Manual persona invocation | Automatic persona consultation |
| `/pb-commit` → manual message formatting | `/pb-commit` → auto-drafted (triggered by `/pb-review`) |
| 97 commands to remember | 3 core commands + annual `/pb-preferences` setup |

---

## New Workflow at a Glance

```
FIRST TIME:
/pb-preferences --setup (15 min, one-time)

EVERY FEATURE:
/pb-start "what"        (30 sec)
[code]
/pb-review              (automatic)
Done
```

---

## For Existing Projects Using Playbooks

### Option A: Adopt New Ritual Immediately

```
Step 1: Run /pb-preferences --setup
  ↓ Answer 15 questions about your decision rules
  ↓ Takes ~15 minutes
  ↓ Settings saved forever

Step 2: Use new workflow on next feature
  /pb-start → code → /pb-review

Step 3: Old commands still work
  /pb-cycle, /pb-review-code, etc. still exist
  But you'll naturally stop using them
```

**Benefit:** Immediate adoption. Old commands available if needed. Reduced cognitive load.

### Option B: Gradual Migration

```
Step 1: Keep using old workflow as-is
  /pb-start → /pb-cycle → /pb-commit still work

Step 2: Try new workflow on non-critical work
  /pb-start → /pb-review (new) on a small feature
  See if preferences capture your style

Step 3: Set /pb-preferences based on experience
  Make informed decisions about thresholds

Step 4: Migrate remaining work when ready
```

**Benefit:** Lower risk. Test before committing fully.

### Option C: Stay on Old Workflow

```
All old commands still work:
- /pb-start (v1.1.0)
- /pb-cycle (v1.1.0)
- /pb-review-code (exists)
- /pb-commit (v2.0.0)

You can ignore new commands indefinitely.
But you're missing 90% automation.
```

**No breaking changes.** Your choice.

---

## Key Differences Explained

### `/pb-start` Changes

**Before:**
- Long pre-start checklist (18+ items)
- Outcome clarification document creation
- Multiple verification steps
- ~10-15 minutes per start

**After:**
- 3-4 adaptive questions (interactive)
- Scope recorded automatically
- ~30 seconds per start
- System auto-detects complexity from your answers

**What You Need to Do:**
Answer these 3-4 questions clearly (they guide everything):
1. What are you building? (outcome, not solution)
2. How complex? (rough LOC/files estimate)
3. Criticality? (main path or nice-to-have?)
4. Any blockers? (resolve before coding)

### `/pb-cycle` → `/pb-review` Replacement

**Before (`/pb-cycle`):**
- Manual self-review checklist
- You decide: code quality? tests? performance?
- Manual persona invocation (`/pb-linus-agent`, `/pb-alex-infra`, etc.)
- Interactive: you choose [A] [B] [C] for each issue
- You manually commit

**After (`/pb-review`):**
- Automatic change analysis
- System decides depth (lean/standard/deep)
- Automatic persona consultation (no invocation needed)
- System applies your preferences to auto-decide issues
- Auto-commits when passing
- Only alerts you if ambiguous or new issue type

**What You Need to Do:**
- Set preferences once (`/pb-preferences --setup`)
- System handles the rest
- You only decide genuinely ambiguous cases (~5% of time)

**Migration Path:**
```
# Option 1: Forget /pb-cycle exists
Just use /pb-review going forward

# Option 2: Reference old checklist
grep -r "Step 1: Self-Review" commands/
Still applies, but automated now

# Option 3: Keep old workflow temporarily
/pb-cycle still works, but you won't need it
```

### `/pb-commit` Changes

**Before:**
- You explicitly invoke `/pb-commit`
- Manual message formatting (follow Conventional Commits)
- Review what you're staging

**After:**
- `/pb-review` auto-commits when passing
- Message auto-drafted with your review reasoning
- You rarely invoke `/pb-commit` manually
- Available if you want explicit control

**What You Need to Do:**
- Usually nothing (automatic)
- Optional: use `pb-commit --check` to verify last commit
- Optional: use `pb-commit --no-auto-commit` if you prefer manual control

---

## Preferences: The Key to Automation

**What are preferences?**

Rules about how you want to balance quality vs. speed:
- Architecture issues: always fix? defer if <1h? case-by-case?
- Testing: require 80%+ coverage? defer if deadline tight?
- Performance: always optimize? accept debt?
- Etc.

**How to set them:**

```bash
/pb-preferences --setup
  ↓ 15 interactive questions
  ↓ Saved to ~/.playbook-preferences.yaml
```

**Example answers:**
- "Architecture: Always fix critical issues"
- "Testing: Threshold - defer gaps if coverage > 80%"
- "Performance: Case-by-case - benchmark first"
- "Security: Always - never compromise"

**System uses them:**
- During `/pb-review`, every issue is matched to your rules
- Auto-decided based on your preferences
- Only asks if issue doesn't fit your rules

**Update them:**
- `/pb-preferences --review` (annual refresh)
- `/pb-preferences --adjust [category]` (one-off change)

---

## Old Commands: Still Available

These commands still work and haven't changed:

| Command | Status | Notes |
|---------|--------|-------|
| `/pb-start` | Updated v2.0 | Simpler, scope detection |
| `/pb-cycle` | v1.1.0 (legacy) | Still works, but replaced by `/pb-review` |
| `/pb-review-code` | v1.0.0 | Still works for peer review checklist |
| `/pb-security` | v1.0.0 | Automatic consultation in `/pb-review`, or invoke directly |
| `/pb-performance` | v1.0.0 | Automatic consultation in `/pb-review`, or invoke directly |
| `/pb-testing` | v1.0.0 | Automatic consultation in `/pb-review`, or invoke directly |
| `/pb-commit` | v2.1.0 | Usually automatic, manual mode available |
| `/pb-pause` | v1.2.0 | Updated with context hygiene, works as before |
| `/pb-resume` | v1.2.0 | Updated with context hygiene, works as before |

---

## Personas: Now Automatic

**Old behavior (manual):**
```
You: "I want Linus to review this"
/pb-linus-agent
System: [Linus feedback on code]
You: [read and decide]
System: [waiting for you]
```

**New behavior (automatic):**
```
/pb-review
System: [detects security assumptions issue]
System: [auto-consults Linus in background]
System: [Linus recommendation + your preference]
System: [auto-decides]
You: [only if ambiguous]
```

**What changed:**
- You don't invoke personas manually anymore
- System determines who to consult based on issue type
- Consultation happens in parallel (fast, no waiting)
- Recommendations are synthesized into one coherent suggestion

---

## Command Count

**Before v2.12.0 Phase 4:** 97 commands

**After v2.12.0 Phase 4:** 99 commands
- `/pb-preferences` (new)
- `/pb-review` in development category (new, different from `/pb-review` in reviews)
- `/pb-cycle` still exists (legacy)

**No breaking changes.** All 97 old commands still work. New commands are additions.

---

## Quick Migration Checklist

### For Individual Contributors

- [ ] Read this migration guide
- [ ] Run `/pb-preferences --setup` (15 min, one-time)
- [ ] Try new workflow on next feature: `/pb-start` → code → `/pb-review`
- [ ] Note if you're making override decisions (`/pb-review --override`)
- [ ] After 3-5 features, adjust preferences if needed

### For Teams

- [ ] Share this guide with team
- [ ] Agree on preference defaults (or everyone sets their own)
- [ ] Try new workflow on one sprint
- [ ] Gather feedback on automation vs. manual control balance
- [ ] Adjust preferences as team consensus emerges

### For Project Leads

- [ ] Update team onboarding docs to reference new ritual
- [ ] Ensure `/pb-preferences` is first task for new contributors
- [ ] Monitor override patterns (if high, adjust preferences)
- [ ] Quarterly review of preference effectiveness

---

## Troubleshooting

### Q: I want to revert to old workflow
**A:** All old commands still work. Use `/pb-cycle` instead of `/pb-review`. Keep using manual `pb-commit`. No penalty.

### Q: `/pb-review` made a decision I disagree with
**A:** Use `pb-review --override [decision]` to override for this instance, then update your preferences if the rule needs adjusting.

### Q: My preferences don't cover all cases
**A:** System will ask you when it encounters a new issue type. Answer once, and system remembers for future. Over time, fewer ambiguous cases.

### Q: I want to bulk-update preferences
**A:**
```bash
/pb-preferences --review
  ↓ Shows all decisions made this past period
  ↓ Review and adjust as needed
```

---

## Learning & Measurement

System automatically tracks:
- Issues fixed vs. deferred
- How often your preferences are applied
- When ambiguous decisions occur (new issue types)
- Persona recommendation accuracy

**Quarterly report** shows:
- What issues were most common
- Where preferences are misaligned
- Which personas are most valuable
- Suggested adjustments to preferences

**Use this to refine preferences** each quarter.

---

## Timeline

**2026-02-17:** New ritual deployed (Phase 4)

**2026-02-17 → 2026-05-17:** Adoption period
- Teams experiment with new workflow
- Preferences stabilize
- Override patterns emerge
- Learning from failures

**2026-05-17:** Q2 Evolution cycle
- Run `/pb-evolve`
- Assess new ritual's effectiveness
- Adjust if needed based on data

**2026-08-17:** Q3 Evolution cycle
- Review preference effectiveness
- Consider additional automation

---

## Not Breaking. Choose Your Pace.

**Key principle:** This is an opt-in enhancement.

Old workflow works forever. New workflow is better (90% automation). Your choice when to adopt.

- No deadline
- No mandate
- No fear of breaking change
- Migrate when it makes sense for you

---

## Questions?

- New workflow confused? Read `/pb-review` and `/pb-preferences` documentation
- Old workflow questions? Read `/pb-cycle` and `/pb-commit` docs (still available)
- Preferences not capturing your style? Adjust via `/pb-preferences --adjust [category]`

---

*Migration Guide v1.0 | 2026-02-17 | Part of v2.12.0 Phase 4*
