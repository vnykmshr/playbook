---
name: "pb-commit"
title: "Commit (Usually Automatic)"
category: "development"
difficulty: "beginner"
model_hint: "haiku"
execution_pattern: "automatic"
related_commands: ['pb-review', 'pb-start', 'pb-pr']
last_reviewed: "2026-02-17"
last_evolved: "2026-02-17"
version: "2.1.0"
version_notes: "Usually automatic (triggered by /pb-review). Manual use only if you prefer explicit control."
breaking_changes: []
---
# Commit (Usually Automatic)

**Resource Hint:** haiku — Simple utility for when you want manual control over commits.

**Usually:** `/pb-review` auto-commits when all passes. You get a notification.

**Rarely:** You want manual control. Use this command explicitly.

**Part of the ritual:** `/pb-start` → code → `/pb-review` → (automatic `/pb-commit`)

---

## The Usual Flow

```
/pb-review
  ↓ System analyzes change
  ↓ Applies your preferences
  ↓ All passes
  ↓ AUTO-COMMITS

Notification: "✓ Committed abc1234f to feature/email-verification"

You: Keep working or run /pb-start on next feature
```

**Your involvement:** 0%

**What happened:** Commit message auto-drafted with:
- What changed
- Why you did it
- Review decisions made
- Issues addressed

---

## If You Want Manual Control

```
/pb-review --no-auto-commit
  ↓ System analyzes, decides, reports
  ↓ Waits for you to manually commit

/pb-commit
  ↓ Shows auto-drafted message
  ↓ You can adjust if needed
  ↓ Confirm
  ↓ Commits and pushes
```

**When to use:** Prefer explicit control? Want to review message first? Use this mode.

---

## If Something Went Wrong

```
/pb-commit --check
  ↓ Verify last auto-commit
  ↓ Show message, changes, push status

/pb-commit --undo
  ↓ Soft-reset last commit (rare emergency)
  ↓ Changes still in working directory
```

---

## Integration

**Before:**
- `/pb-review` auto-commits when all passes

**This command:**
- Usually not needed (automatic)
- Exists if you want manual control
- Exists if something went wrong

**After:**
- Commit is in remote
- Ready for `/pb-pr` or next work

---

## Related Commands

- `/pb-review` — Runs auto-commit (you don't need to do anything)
- `/pb-start` — Begin next work
- `/pb-pr` — Peer review (next step after commit)

---

*Automatic by default | Manual if you prefer | v2.1.0*
