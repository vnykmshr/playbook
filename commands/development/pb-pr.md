---
name: "pb-pr"
title: "Quick PR Creation"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-start', 'pb-commit', 'pb-cycle', 'pb-review-code', 'pb-ship']
last_reviewed: "2026-11-06"
version: "1.2.0"
version_notes: "v1.2.0: Small-PR body is one sentence of what plus upgrader impact; the drafted title and body are checked against the register before the PR opens; Related lists /pb-start."
breaking_changes: []
---
# Quick PR Creation

Streamlined workflow for creating a pull request with proper context and description.

**Mindset:** PR review is built on `/pb-preamble` thinking (challenge assumptions, surface issues) and applies `/pb-design-rules` thinking (reviewers check that code is Clear, Simple, Modular, Robust).

Reviewers will challenge your decisions. That's the point. Welcome that feedback. It makes code better. Your job as author is to explain your reasoning clearly so reviewers can engage meaningfully.

**Resource Hint:** sonnet - PR creation and description formatting

---

## When to Use This Command

- **Ready to create PR** - Code complete, reviewed, and tested
- **Need PR guidance** - Unsure about PR structure or description
- **PR description help** - Want template for clear PR descriptions

---

## Pre-PR Checklist

Before creating PR, verify:

- [ ] All commits are logical and atomic
- [ ] Quality gates pass: `make lint && make typecheck && make test`
- [ ] Self-review completed (`/pb-cycle`)
- [ ] Branch is up to date with main
- [ ] No merge conflicts

---

## Step 1: Prepare Branch

```bash
# Ensure branch is up to date
git fetch origin main
git rebase origin/main

# Verify all changes are committed
git status

# Push branch to remote
git push -u origin $(git branch --show-current)
```

---

## Step 2: Review Changes

Before writing PR description, understand the full scope:

```bash
# See all commits on this branch
git log origin/main..HEAD --oneline

# See full diff against main
git diff origin/main...HEAD --stat
```

---

## Step 3: Create PR

PR body register follows the global rule (see `~/.claude/CLAUDE.md` § GitHub Artifact Register). Pick the form that matches the change size, then check the drafted title and body against the register before opening the PR.

### Default: small PR (≤3 files OR single concern)

No headers. One sentence of what the PR does, plus one of upgrader impact when there is any.

```bash
gh pr create --title "<type>(<scope>): <description>" --body "$(cat <<'EOF'
<one sentence: what; a second only for upgrader impact>
EOF
)"
```

### Large PR (>3 files OR multiple concerns)

Sectioned template:

```bash
gh pr create --title "<type>(<scope>): <description>" --body "$(cat <<'EOF'
## Summary
<1-3 bullets: what changed and why>

## Changes
<key technical changes, grouped logically>

## Test Plan
<specific steps to verify; edge cases>
EOF
)"
```

---

## PR Title Format

```
<type>(<scope>): <subject>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `docs`: Documentation
- `test`: Tests
- `chore`: Build/config changes

**Examples:**
```
feat(audio): add study mode with guided narration
fix(auth): handle expired token redirect loop
refactor(miniplayer): extract shared button components
perf(fonts): self-host fonts for faster loading
```

---

## Quick Commands

```bash
# Create PR with default template
gh pr create --fill

# Create PR and open in browser
gh pr create --web

# Create draft PR
gh pr create --draft --title "WIP: feature name"

# View PR status
gh pr status

# View PR checks
gh pr checks
```

---

## After PR Created

1. **Verify CI passes** - Watch for lint, typecheck, test failures
2. **Self-review in GitHub** - Read through the diff one more time
3. **Request review** - Tag appropriate reviewers
4. **Respond to feedback** - Address comments promptly

---

## Merge Strategy

**Squash and merge** - Keeps main history clean

Before merging:
- [ ] All checks green
- [ ] Approved by reviewer
- [ ] Conflicts resolved
- [ ] PR description accurate

---

## Related Commands

- `/pb-start` - Begin the work this PR closes (the ritual's first step)
- `/pb-commit` - Craft atomic commits before creating PR
- `/pb-cycle` - Self-review and peer review workflow
- `/pb-review-code` - Code review checklist for reviewers
- `/pb-ship` - Full review, merge, and release workflow

---

*Good PRs are small, focused, and well-described.*
