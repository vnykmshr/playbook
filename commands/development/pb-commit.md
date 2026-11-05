---
name: "pb-commit"
title: "Commit (Usually Automatic)"
category: "development"
difficulty: "beginner"
model_hint: "sonnet"
execution_pattern: "automatic"
related_commands: ['pb-review', 'pb-start', 'pb-pr']
last_reviewed: "2026-11-05"
version: "2.4.0"
version_notes: "v2.4.0: Message Register points to the register instead of restating a body length, and checks the drafted message before committing. Mindset added."
breaking_changes: []
---
# Commit (Usually Automatic)

**Mindset:** Apply `/pb-design-rules` thinking (clarity over cleverness, one concern per commit): the subject is all most readers see.

**Resource Hint:** sonnet - Commit message drafting with context-aware summaries and bisectable splitting guidance.

**Tool-agnostic:** This command documents commit discipline (atomic, clear messages) that works with any version control system. Claude Code users invoke as `/pb-commit`. Using another tool? Read this file as Markdown for commit principles and message format. See [`/docs/using-with-other-tools.md`](../../docs/using-with-other-tools.md) for how to adapt the ritual.

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

**Gate the commit on the command that proves it.** `npm test | tail -5 && git commit ...` gates on `tail`, which succeeds whatever the tests did. Run the check on its own, or under `set -o pipefail`, and commit on its exit code.

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

Default: `<type>(<scope>): <subject>`, present tense, subject only. No attribution trailers. The rest (defaults, strip list, never-write list) is the GitHub Artifact Register that `/pb-claude-global` writes into `~/.claude/CLAUDE.md`; check the drafted message against it before committing. When a body includes test results: name the exact command run, or state "not run" with reason. No silent validation gaps.

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
