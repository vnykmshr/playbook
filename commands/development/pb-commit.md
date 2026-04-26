---
name: "pb-commit"
title: "Commit (Usually Automatic)"
category: "development"
difficulty: "beginner"
model_hint: "sonnet"
execution_pattern: "automatic"
related_commands: ['pb-review', 'pb-start', 'pb-pr']
last_reviewed: "2026-04-26"
last_evolved: "2026-04-26"
version: "2.3.0"
version_notes: "v2.3.0: Reference global GitHub Artifact Register rule via single-line pointer; drop local restatement and implicit 4-bullet template."
breaking_changes: []
---
# Commit (Usually Automatic)

**Resource Hint:** sonnet - Commit message drafting with context-aware summaries and bisectable splitting guidance.

**Tool-agnostic:** This command documents commit discipline (atomic, clear messages) that works with any version control system. Claude Code users invoke as `/pb-commit`. Using another tool? Read this file as Markdown for commit principles and message format. See [`/docs/using-with-other-tools.md`](/docs/using-with-other-tools.md) for how to adapt the ritual.

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

**What happened:** Commit message auto-drafted per the global register rule (see `~/.claude/CLAUDE.md` § GitHub Artifact Register). Subject line only by default; body added only when the WHY is non-obvious.

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

## Bisectable Commit Splitting

For changes touching >3 files across >1 concern, consider splitting into bisectable commits. This makes `git bisect` useful and rollbacks surgical.

**Dependency order:**
1. **Infrastructure/config** - Schema migrations, configuration changes, dependencies
2. **Data/models + tests** - Data layer changes with their tests together
3. **Logic/controllers/UI** - Application logic, API endpoints, frontend
4. **Versioning** - VERSION, CHANGELOG, release metadata last

**When to split:**
- Multiple concerns in one change (infra + logic + tests)
- Changes that could independently cause failures
- Large changes where isolating the breaking commit matters

**When NOT to split:**
- Single-concern changes (even across many files - e.g., a rename)
- Small changes (<50 LOC) where splitting adds noise
- Tightly coupled changes where splitting would leave broken intermediate states

---

## Message Register

Follow `~/.claude/CLAUDE.md` § GitHub Artifact Register for format, length ceilings, strip list, and never-write list. Subject-only by default.

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

- `/pb-review` - Runs auto-commit (you don't need to do anything)
- `/pb-start` - Begin next work
- `/pb-pr` - Peer review (next step after commit)

---

*Automatic by default | Manual if you prefer | v2.3.0*
