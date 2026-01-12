# Atomic Commits & Commit Messages

Craft focused, logical commits that tell the story of your work. Each commit should be one complete thought.

---

## Purpose

Good commits:
- Are easy to review (one concern per commit)
- Are easy to revert if needed (isolated change)
- Make git blame and bisect useful
- Create clean, readable history
- Help future developers understand "why"

**Why this matters:** Clear commits embody `/pb-preamble` thinking (explain your reasoning so others can challenge it) and `/pb-design-rules` thinking (especially Clarity and Representation: commits should make intent obvious).

You explain your reasoning, which invites others to challenge it. That's the point. Commits that force you to articulate "why" are harder to defend when the reasoning is flawed—which is exactly what you want. Clear reasoning makes flawed thinking obvious.

---

## When to Commit

### S Tier (Small, <2 hours)
Commit when: Feature/fix is done
- 1-3 files typically
- Single logical change
- All tests passing
- 1 conventional commit

**Example**: "feat(auth): add email verification on signup"

### M Tier (Medium, phased work)
Commit when: Each logical unit is done
- 2-5 commits typical (not one mega-commit)
- Each commit: one feature or refactoring unit
- Dependencies between commits should be clear
- Review each commit message to ensure clarity

**Example breakdown**:
```
1. feat(auth): add email verification endpoint
2. feat(auth): add email verification UI form
3. test(auth): add integration tests for verification flow
```

### L Tier (Large, multi-week)
Commit frequently: After each logical unit or daily
- 5-10+ commits typical
- Helps team track progress
- Easier to review (smaller chunks)
- Makes debugging easier

**Example breakdown**:
```
1. feat(payments): add stripe integration module
2. feat(payments): implement charge endpoint
3. test(payments): add payment processing tests
4. feat(payments): add webhook handling for events
5. docs(payments): add payment API documentation
6. test(payments): add webhook validation tests
```

---

## Commit Message Format

Follow **Conventional Commits** specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type
- `feat` — New feature
- `fix` — Bug fix
- `refactor` — Code reorganization (no feature or fix)
- `test` — Adding or updating tests
- `docs` — Documentation only
- `chore` — Non-code changes (dependencies, config)
- `perf` — Performance improvements

### Scope
Optional but recommended. Name of module/feature:
- `auth`, `payments`, `database`, `api`, `ui`, etc.
- Can be omitted for global changes

### Subject
- Imperative mood ("add" not "added" or "adds")
- Lowercase first letter
- No period at end
- 50 characters max (if possible)

### Body
Optional. Explain **why**, not what:
- What you changed is in the code, show in the diff
- Why you changed it might not be obvious

**Good body**:
```
Add email verification because users were signing up with typos,
then couldn't recover their accounts. This forces email confirmation
before account creation.
```

**Bad body**:
```
Added email verification. Loop through email list and send tokens.
Check if token matches. Update database.
```

### Footer
Optional. Reference issues or breaking changes:
```
Fixes #123
BREAKING CHANGE: Email is now required for signup
```

---

## Commit Size: The "Logical Changeset" Rule

One commit = One logical change. Examples:

### [YES] GOOD: Logical, Atomic

**Commit 1**: "feat(auth): add password reset flow"
```
- Add password reset endpoint
- Add password reset UI form
- Add email sending logic
- Add tests for password reset
```
*Why it's good*: All parts of one feature, reviewable as one unit, works standalone

**Commit 2**: "refactor(auth): extract token validation to util"
```
- Create TokenValidator util
- Update login endpoint to use util
- Update password reset to use util
- Update tests
```
*Why it's good*: One refactoring, affects multiple places, still one logical change

### [NO] BAD: Too Large

```
feat(auth): add email verification and password reset and 2FA
```
*Why it's bad*: Three unrelated features, hard to review, hard to revert one without others

### [NO] BAD: Too Small

```
feat(auth): add import statement for bcrypt
```
*Why it's bad*: Doesn't work on its own, meaningless by itself

### [NO] BAD: Mixed Concerns

```
feat(auth): add password reset
fix(database): connection pool timeout
docs: update README
```
*Why it's bad*: Three unrelated things, should be 3 commits

---

## Examples: Good vs Bad

### Example 1: Authentication Feature

[NO] BAD
```
git commit -m "fix stuff"
```
- No type, scope, or description
- Impossible to understand what changed
- Useless in git blame/bisect

[YES] GOOD
```
git commit -m "feat(auth): implement JWT refresh token rotation

Add refresh token rotation on each token refresh to prevent token
reuse attacks. Refresh tokens are now single-use and rotated with
each refresh request. Access tokens remain short-lived (15 min).

Fixes #456"
```

### Example 2: Bug Fix

[NO] BAD
```
git commit -m "fixed bug in user lookup

modified the query. also cleaned up some code and added logging"
```
- Unclear what bug
- Multiple concerns (fix + cleanup + logging)
- No reference to issue

[YES] GOOD
```
git commit -m "fix(database): handle NULL values in user lookup

User lookup was failing with NULL pointer when contact_phone was NULL.
Changed INNER JOIN to LEFT JOIN to handle missing phone numbers.

Fixes #789"
```

### Example 3: Refactoring

[NO] BAD
```
git commit -m "refactored code

Extracted common logic, renamed variables, updated imports"
```
- What common logic?
- Why extract it?
- No impact analysis

[YES] GOOD
```
git commit -m "refactor(api): extract request validation middleware

Move duplicate validation logic from 5 endpoints into reusable
RequestValidator middleware. Reduces code duplication, makes
validation consistent across endpoints.

Closes #234"
```

---

## Commit Discipline Checklist

Before committing, verify:

### Code Quality
- [ ] Code compiles without warnings
- [ ] All tests pass locally
- [ ] Linter passes (`make lint` or equivalent)
- [ ] No debug code, print statements, or TODOs

### Commit Quality
- [ ] One logical change per commit
- [ ] Commit message follows Conventional Commits
- [ ] Subject is clear and specific (not vague)
- [ ] Body explains "why" if not obvious
- [ ] Issue references in footer if applicable

### Integration
- [ ] Commit doesn't break existing tests
- [ ] Commit builds/runs on its own (or with previous commits)
- [ ] No merge conflicts (rebase if needed)

---

## Integration with Playbook

**Part of workflow:**
- `/pb-start` → Create feature branch, work begins
- `/pb-cycle` → Iteration with self-review and peer review
- `/pb-commit` → Craft atomic commits (YOU ARE HERE)
- `/pb-pr` → Create pull request with commits
- `/pb-release` → Deploy

**Related Commands:**
- `/pb-start` — Starting a feature (before commits)
- `/pb-cycle` — Code quality and testing (before commits)
- `/pb-pr` — Creating pull request (after commits)
- `/pb-guide` — SDLC tiers and workflow

---

## Common Patterns

### Feature with Multiple Steps

Instead of:
```
feat(payments): implement stripe payments
```

Do:
```
1. feat(payments): add stripe API integration module
2. feat(payments): implement charge endpoint
3. feat(payments): implement refund endpoint
4. test(payments): add payment integration tests
5. docs(payments): add payment API documentation
```

Each commit works, can be reviewed independently, easy to bisect if issue found.

### Bug Fixes

**Format**:
```
fix(scope): brief description

Explain the root cause and why this fix works.

Fixes #123
```

**Example**:
```
fix(auth): prevent session fixation in login endpoint

Session ID was being reused from pre-login request. Now we generate
a new session ID after successful authentication, preventing attackers
from fixing a session before the user logs in.

Fixes #890
```

### Refactoring

**Format**:
```
refactor(scope): description of what changed

Explain why the refactoring was needed and what benefit it provides.
```

**Example**:
```
refactor(database): consolidate query builders into QueryHelper

Previously had duplicate query building logic in 3 repositories.
Consolidated into QueryHelper class for consistency and easier
maintenance. All queries still produce identical SQL.
```

### Dependencies and Configuration

**Format**:
```
chore(scope): description

Breaking change note if applicable.
```

**Example**:
```
chore(deps): upgrade express from 4.17 to 4.18

Includes security patches for XSS vulnerability in query parser.

BREAKING CHANGE: Requires Node 14+
```

---

## Tips for Great Commits

### [YES] DO

- **Be specific**: "add email validation" not "add validation"
- **One thought per commit**: All parts of one feature, not multiple features
- **Make it reviewable**: Each commit should be easy for someone else to understand
- **Explain why**: "why did you do this?" often matters more than "what did you do?"
- **Link to issues**: Reference the issue/ticket being fixed
- **Use present tense**: "add feature" not "added feature"

### [NO] DON'T

- **Don't mix concerns**: One fix + one refactor + one docs update = 3 commits
- **Don't make mega-commits**: If you can't describe it in one sentence, it's too big
- **Don't commit WIP**: Make commits that work/compile on their own
- **Don't say "fixed stuff"**: Be specific about what and why
- **Don't bury important info**: Put key info in subject, not deep in body
- **Don't format inconsistently**: Follow Conventional Commits for all commits

---

## Handling Mistakes

### Oops, committed too much?

Undo and split:
```bash
git reset HEAD~1           # Undo last commit, keep changes
git add file1.js           # Stage first logical change
git commit -m "feat: first part"
git add file2.js           # Stage second logical change
git commit -m "feat: second part"
```

### Oops, wrong message?

Amend (only if not pushed):
```bash
git commit --amend -m "correct message"
```

### Oops, wrong changes in commit?

Remove from commit:
```bash
git reset HEAD~1           # Undo
git add <only-correct-files>
git commit -m "correct commit"
```

---

## Commit Message Template

Copy this into your commits:

```
<type>(<scope>): <subject line, 50 chars max>

<body explaining why, 72 chars per line>

Fixes #<issue-number>
```

**Example**:
```
feat(auth): add two-factor authentication

Add optional 2FA for user accounts. When enabled, users receive
a TOTP code via authenticator app. Verified on each login.

Fixes #345
```

---

*Created: 2026-01-11 | Category: Development | Tier: S/M/L*
