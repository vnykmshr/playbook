# Resume Development Work

Quickly get back into context after a break. Use this to resume work on an existing feature branch.

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

# Read relevant docs/issues for context
# Review your branch changes thoroughly
git diff origin/main...HEAD

# Rebase and continue
git rebase origin/main
```

---

## Recovery Checklist

Before continuing work:

- [ ] On correct branch
- [ ] Branch is up to date with main
- [ ] Understand what was last done
- [ ] Know what's next
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

## Reading Working Context

For project-level context:

```bash
# Read project working context
/pb-context (or cat todos/prompts/1-working-context.md)

# Check release tracker if on a release branch
cat todos/releases/v1.X.0/00-master-tracker.md
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

### Before Stopping Work

1. **Commit or stash** - Never leave uncommitted work overnight
2. **Write a note** - Quick TODO comment or session end note
3. **Push to remote** - Backup your work
4. **Leave context** - Update /pb-context decision log or standup

### When Resuming

1. **Start with status** - `git status` first
2. **Read before writing** - Review recent commits
3. **Verify environment** - Ensure services running
4. **Run tests** - Confirm baseline is green
5. **Post standup** - Write /pb-standup to align with team

---

## Integration with Playbook

**Part of development workflow:**
- `/pb-start` → Create branch, set iteration rhythm
- **`/pb-resume`** → Get back in context after break (YOU ARE HERE)
- `/pb-cycle` → Iterate with reviews
- `/pb-standup` → Daily async visibility (write after resuming)
- `/pb-commit` → Atomic commits
- `/pb-pr` → Pull request

**When to use `/pb-resume`:**
- After a context switch (lunch break, context switching)
- After a day off or weekend
- After a long meeting
- When resuming work from a different branch
- When you've been on a different task for hours

**Related commands:**
- `/pb-start` — Starting new feature (before /pb-resume context recovery)
- `/pb-context` — Read project context (use alongside /pb-resume)
- `/pb-standup` — Write after resuming (post status for team)
- `/pb-standards` — Refresh working principles
- `/pb-guide` — SDLC framework reference

**See also:** `/docs/integration-guide.md` for how all commands work together

---

*Context is expensive to rebuild. Leave breadcrumbs for future you.*
