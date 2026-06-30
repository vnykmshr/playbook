---
name: "pb-resume"
title: "Resume Development Work"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-start', 'pb-pause', 'pb-cycle']
last_reviewed: "2026-03-28"
last_evolved: "2026-06-30"
version: "1.4.0"
version_notes: "v1.4.0: Add Session Recap Review (Step 0) — surface, decide, archive loop."
breaking_changes: []
---
# Resume Development Work

Quickly get back into context after a break. Use this to resume work on an existing feature or branch.

**Mindset:** Resuming requires understanding assumptions made and verifying context is complete. Apply `/pb-preamble` thinking: challenge what was decided and why. Apply `/pb-design-rules` thinking: is the code clear, simple, and robust?

**Resource Hint:** sonnet - context recovery, state assessment, health check

---

## Modes

```
/pb-resume             → Standard (default): git state, sync, load context, health check
/pb-resume deep        → Deep: standard + verify/regenerate stale layers + run tests
```

**When to use deep:** After long breaks (days/weeks), picking up someone else's work, or when standard mode flags stale context layers.

---

## Standard Mode (Default)

### Step 0: Session Recap Review

Read the `### Session Recap` section from `todos/pause-notes.md`. If present, surface it before loading state:

```
## Session Recap (from last session)

[recap content]
```

**After surfacing, the assistant handles it:**

1. **Append to `memory/lessons.md`** first (before stripping — prevents data loss if interrupted):
   ```markdown
   ## [YYYY-MM-DD] — [session context]
   [recap content]
   ```
2. **Strip from pause notes** after confirming the archive write succeeded.
3. **Act on findings with sensible defaults:**
   - Obvious fix (wording, guardrail, convention) → apply it. Commit.
   - Complex or needs operator judgment → flag: "Noted for this session: [finding]" — add to working context.
   - No immediate action needed → archived; `/pb-evolve` mines it later.

The operator can override any action, but the default is "handle it, don't present a menu."

**If no Session Recap section exists:** skip silently. (First-time use with pre-v1.5.0 pause notes: say "Session Recap: none — recaps are written by `/pb-pause` when a session produces learnings." Once.)

---

### Step 1: Check Current State

```bash
git branch --show-current
git status
git log --oneline -5
git stash list
```

### Step 2: Sync with Remote

```bash
git fetch origin
git log --oneline HEAD..origin/main
```

If main has moved ahead, review what changed before rebasing:

```bash
git log --oneline HEAD..origin/main    # What you missed
git diff origin/main...HEAD            # Your full branch diff
git rebase origin/main
```

### Step 3: Review Recent Work

```bash
git log origin/main..HEAD --oneline    # Branch commits
git diff                                # Uncommitted changes
git diff --staged                       # Staged changes
```

### Step 4: Load Session State + Context Health Check

**Load session state:**

```bash
cat todos/1-working-context.md         # Project snapshot
cat todos/pause-notes.md               # Where you left off
```

**If pause notes exist:** Follow documented next steps, verify blockers resolved.

**Context health check — report actual sizes:**

```bash
wc -l ~/.claude/CLAUDE.md              # Global (target: ~160)
wc -l .claude/CLAUDE.md                # Project (target: ~180)
# memory/MEMORY.md                     # Auto-loaded (target: ~100)
wc -l todos/1-working-context.md       # Working context (target: ~50)
wc -l todos/pause-notes.md             # Pause notes (target: ~30)
```

**Flag issues:**
- Working context version doesn't match `git describe --tags` → stale, consider `/pb-resume deep`
- Pause notes has multiple entries → old entries should have been archived by `/pb-pause`
- Any layer missing → run the appropriate regeneration command

---

## Deep Mode

Run standard mode first, then continue with these steps.

### Step 5: Verify and Regenerate Context Layers

Check each layer for staleness and regenerate as needed:

```bash
git describe --tags                    # Current version
```

- **Working context stale** (version mismatch) → run `/pb-context`
- **Project CLAUDE.md stale** (structural changes since last update) → run `/pb-claude-project`
- **Global CLAUDE.md stale** (playbook version changed) → run `/pb-claude-global`

### Step 6: Verify Baseline

```bash
# Run project tests (adapt to your project)
python3 -m pytest tests/ -q            # or: make test, npm test, go test ./...

# Verify CI status
gh run list --limit 1
```

Confirm baseline is green before starting new work.

---

## Recovery Checklist

Before continuing work:

- [ ] On correct branch
- [ ] Branch is up to date with main
- [ ] Checked pause notes
- [ ] Understand what was last done
- [ ] Know what's next
- [ ] Working context is current

---

## Quick Commands

| Action | Command |
|--------|---------|
| Current branch | `git branch --show-current` |
| Recent commits | `git log --oneline -5` |
| Uncommitted changes | `git diff` |
| Stash list | `git stash list` |
| Fetch origin | `git fetch origin` |
| Rebase on main | `git rebase origin/main` |

---

## If Completely Lost

```bash
git branch -a                          # What branches exist?
git reflog | head -20                  # What branch was I on?
git log --all --oneline --graph -20    # What work exists?
cat todos/pause-notes.md               # Any breadcrumbs?
```

---

## Related Commands

- `/pb-start` - Begin work on a new feature or fix
- `/pb-pause` - Gracefully pause work and preserve context
- `/pb-cycle` - Self-review and peer review during development

---

*Context is expensive to rebuild. Leave breadcrumbs for future you.*
