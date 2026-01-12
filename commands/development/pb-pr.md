# Quick PR Creation

Streamlined workflow for creating a pull request with proper context and description.

**Mindset:** PR review is built on `/pb-preamble` thinking. Reviewers will challenge assumptions and surface issues. That's the point. Welcome that feedback—it makes code better.

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

Use this template:

```bash
gh pr create --title "<type>(<scope>): <description>" --body "$(cat <<'EOF'
## Summary

<!-- 1-3 bullet points: what changed and why -->
-
-

## Changes

<!-- Key technical changes, grouped logically -->
-

## Test Plan

<!-- How to verify this works -->
- [ ]
- [ ]

## Screenshots

<!-- If UI changes, add before/after screenshots -->

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

## PR Description Guidelines

### Summary Section
- What changed (user-facing impact)
- Why this change (problem being solved)
- Keep to 1-3 bullet points

### Changes Section
- Group related changes logically
- Mention key files/components affected
- Note any breaking changes

### Test Plan Section
- Specific steps to verify the change
- Include edge cases tested
- Note any manual testing performed

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

*Good PRs are small, focused, and well-described.*
