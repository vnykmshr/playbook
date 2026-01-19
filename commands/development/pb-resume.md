# Resume Development Work

Quickly get back into context after a break. Use this to resume work on an existing feature branch.

**Mindset:** Resuming work requires understanding assumptions and decisions made.

Use `/pb-preamble` thinking: challenge your assumptions about what was decided and why. Use `/pb-design-rules` thinking: understand how the design embodies Clarity (is the code obvious?), Simplicity (are we solving this the simplest way?), and Robustness (are error cases handled?).

---

## Quick Context Recovery

### Step 1: Check Current State

```bash
# What branch am I on?
git branch --show-current

# What's the status?
git status

# What did I do last?
git log --oneline -5

# Any stashed work?
git stash list
```

### Step 2: Sync with Remote

```bash
# Fetch latest from origin
git fetch origin

# Check if main has moved
git log --oneline HEAD..origin/main

# Rebase if needed
git rebase origin/main
```

### Step 3: Review Recent Work

```bash
# See what changed on this branch
git log origin/main..HEAD --oneline

# See uncommitted changes
git diff

# See staged changes
git diff --staged
```

---

## Session Context Template

When resuming, establish context:

```
Resuming work on: [branch-name]

## Where I Left Off
- Last commit: [commit message]
- In progress: [what was being worked on]
- Blocked on: [if anything]

## Current Status
- [ ] Task 1: [status]
- [ ] Task 2: [status]
- [ ] Task 3: [status]

## Next Steps
1. [Immediate next action]
2. [Following action]

## Open Questions
- [Any unresolved questions]
```

---

## Common Resume Scenarios

### Scenario A: Clean Stop (all committed)

```bash
# Just verify and continue
git status                    # Should be clean
git log --oneline -3          # Review last commits
# Continue with next task
```

### Scenario B: Work in Progress (uncommitted changes)

```bash
# Review what's uncommitted
git diff
git diff --staged

# Option 1: Continue where you left off
# Just keep working

# Option 2: Stash and start fresh
git stash push -m "WIP: description"
# Work on something else
git stash pop  # When ready to resume
```

### Scenario C: Main Has Moved Ahead

```bash
# Rebase your branch
git fetch origin
git rebase origin/main

# Resolve conflicts if any
# Continue working
```

### Scenario D: Long Break (days/weeks)

```bash
# Full context recovery
git fetch origin
git log --oneline origin/main..HEAD  # Your changes
git log --oneline HEAD..origin/main  # What you missed

# Check for pause notes (left by /pb-pause)
cat todos/pause-notes.md 2>/dev/null | tail -50

# Read relevant docs/issues for context
# Review your branch changes thoroughly
git diff origin/main...HEAD

# Rebase and continue
git rebase origin/main
```

**If pause notes exist:** Follow documented next steps, verify blockers resolved.

---

## Recovery Checklist

Before continuing work:

- [ ] On correct branch
- [ ] Branch is up to date with main
- [ ] Checked pause notes (`todos/pause-notes.md`)
- [ ] Understand what was last done
- [ ] Know what's next
- [ ] Working context is current (if project has one)
- [ ] Dev environment running (`make dev`)
- [ ] Tests pass (`make test`)

---

## Quick Commands

| Action | Command |
|--------|---------|
| Current branch | `git branch --show-current` |
| Recent commits | `git log --oneline -5` |
| Uncommitted changes | `git diff` |
| Staged changes | `git diff --staged` |
| Stash list | `git stash list` |
| Pop stash | `git stash pop` |
| Fetch origin | `git fetch origin` |
| Rebase on main | `git rebase origin/main` |

---

## Reading and Updating Working Context

For project-level context:

```bash
# Check for working context (location and naming may vary)
ls todos/*working-context*.md 2>/dev/null

# Read project working context (or run /pb-context)
cat todos/working-context.md

# Check release tracker if on a release branch
cat todos/releases/v1.X.0/00-master-tracker.md
```

**Common locations:** `todos/working-context.md`, `todos/1-working-context.md`

**Working context currency check:**
```bash
# Compare working context version with actual state
git describe --tags                    # Current version
git log --oneline -5                   # Recent commits
```

If the working context is stale (version mismatch, outdated commits, missing recent releases):
1. Run `/pb-context` to review and update
2. Update version, date, recent commits, and active development sections
3. Verify session checklist commands still work

---

## Reading Pause Notes

If you (or someone else) used `/pb-pause` before stopping, look for handoff context:

```bash
# Check for pause notes
cat todos/pause-notes.md 2>/dev/null | tail -50

# Or grep for your branch
grep -A 30 "$(git branch --show-current)" todos/pause-notes.md
```

**Pause notes contain:**
- Where work left off (last commit, in-progress items)
- Current task status
- Next steps (prioritized)
- Open questions and blockers
- Gotchas and environment notes

**After reading pause notes:**
1. Verify current state matches documented state
2. Check if blockers have been resolved
3. Review next steps and adjust if needed
4. Clear old pause notes once context is recovered

```bash
# Archive old pause notes (optional)
mv todos/pause-notes.md todos/pause-notes-$(date +%Y%m%d).md
```

---

## If Completely Lost

```bash
# 1. What branches exist?
git branch -a

# 2. What branch was I on?
git reflog | head -20

# 3. What work exists?
git log --all --oneline --graph -20

# 4. Read the working context
# /pb-standards for patterns
# /pb-context for project context and decision log
# /pb-guide for SDLC framework reference
```

---

## Tips for Better Resume

### Before Stopping Work (Use `/pb-pause`)

Run `/pb-pause` before stepping away. It guides you through:

1. **Preserve work state** — Commit or stash, push to remote
2. **Update trackers** — Mark progress, document blockers
3. **Update context** — Run `/pb-context`, `/pb-claude-project` if needed
4. **Write pause notes** — Document where you left off in `todos/pause-notes.md`

**Quick pause (short breaks):**
```bash
git add -A && git commit -m "wip: [state]" && git push
```

### When Resuming

1. **Start with status** - `git status` first
2. **Read before writing** - Review recent commits
3. **Verify environment** - Ensure services running
4. **Run tests** - Confirm baseline is green
5. **Post standup** - Write /pb-standup to align with team

---

## Integration with Playbook

**Part of development workflow:**
```
/pb-start → /pb-cycle → /pb-commit → /pb-ship
     ↑                                   │
     │         ┌─────────────┐           │
     │         │   SESSION   │           ↓
     └─────────│   BOUNDARY  │       Reviews →
               └─────────────┘       PR → Merge →
                     ↑               Release
                     ↓
              /pb-resume ←──────── /pb-pause
              (recover)            (preserve)
```

**Commands:**
- `/pb-start` → Create branch, set iteration rhythm
- **`/pb-resume`** → Get back in context after break (YOU ARE HERE)
- `/pb-cycle` → Iterate with reviews
- `/pb-pause` → Gracefully pause, preserve context
- `/pb-commit` → Atomic commits
- `/pb-ship` → Full review → PR → release workflow

**When to use `/pb-resume`:**
- After a context switch (lunch break, context switching)
- After a day off or weekend
- After a long meeting
- When resuming work from a different branch
- When you've been on a different task for hours

**Related commands:**
- `/pb-start` — Starting new feature (before /pb-resume context recovery)
- `/pb-pause` — Gracefully pause work (complement to /pb-resume)
- `/pb-ship` — When ready to ship (reviews → PR → release)
- `/pb-context` — Read project context (use alongside /pb-resume)
- `/pb-standup` — Write after resuming (post status for team)
- `/pb-standards` — Refresh working principles
- `/pb-guide` — SDLC framework reference

**See also:** `/docs/integration-guide.md` for how all commands work together

---

*Context is expensive to rebuild. Leave breadcrumbs for future you.*
