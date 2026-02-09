---
name: "pb-cycle"
title: "Development Cycle: Self-Review + Peer Review"
category: "development"
difficulty: "advanced"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-start', 'pb-commit', 'pb-pr', 'pb-review-code', 'pb-testing']
tags: ['design', 'testing', 'security', 'workflow', 'review']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Development Cycle: Self-Review + Peer Review

Run this after completing a unit of work. Guides you through self-review, quality gates, and peer review before committing.

**Resource Hint:** sonnet — iterative code review and quality gate checks

---

## When to Use This Command

- **After completing a feature/fix** — Before committing changes
- **During development iterations** — Each cycle of code → review → refine
- **Before creating a PR** — Final self-review pass
- **When unsure if code is ready** — Checklist helps verify completeness

---

## Step 1: Self-Review

Review your own changes critically before requesting peer review.

**Use the Self-Review Checklist** from `/docs/checklists.md`:
- Code Quality: hardcoded values, dead code, naming, DRY, error messages
- Security: no secrets, input validation, parameterized queries, auth checks, logging
- Testing: unit tests, edge cases, error paths, all tests passing
- Documentation: comments for "why", clear names, API docs updated
- Database: reversible migrations, indexes, constraints, no breaking changes
- Performance: N+1 queries, pagination, timeouts, unbounded loops

---

## Step 2: Quality Gates

Run before proceeding to peer review:

```bash
make lint        # Linting passes
make typecheck   # Type checking passes
make test        # All tests pass
```

**All gates must pass. Fix issues before proceeding.**

---

## Step 3: Peer Review

Request review from senior engineer perspective.

**For reviewers:** Use `/pb-review-code` for the complete code review checklist.

**Important:** Peer review assumes `/pb-preamble` thinking (challenge assumptions, surface flaws, question trade-offs) and applies `/pb-design-rules` (check for clarity, simplicity, modularity).

Reviewer should:
- Challenge architectural choices and design decisions
- Check that code follows design rules: Clarity, Simplicity, Modularity
- Ask clarifying questions about trade-offs
- Surface flaws directly

Author should welcome and respond to critical feedback. This is how we catch problems early—in code review, not production.

### Architecture Review

- [ ] Changes align with existing patterns
- [ ] No unnecessary complexity introduced
- [ ] Separation of concerns maintained
- [ ] Dependencies appropriate (not pulling in large libs for small tasks)

### Correctness Review

- [ ] Logic handles all stated requirements
- [ ] Edge cases considered
- [ ] Error handling is comprehensive
- [ ] Race conditions considered for concurrent operations

### Maintainability Review

- [ ] Code is readable without extensive comments
- [ ] Functions are single-purpose and reasonably sized
- [ ] Magic values extracted to constants
- [ ] Naming clearly expresses intent

### Security Review

- [ ] No injection vulnerabilities (SQL, command, etc.)
- [ ] Authorization properly enforced
- [ ] Sensitive operations properly audited
- [ ] No information leakage in error responses

### Test Review

- [ ] Tests actually verify the behavior (not just coverage%)
- [ ] Test names describe what they verify
- [ ] Mocks/stubs used appropriately
- [ ] No flaky tests introduced

---

## Step 4: Address Feedback

If issues identified:

1. **Fix the issues** - Don't argue, just fix
2. **Re-run self-review** - Ensure fix didn't break something else
3. **Re-run quality gates** - All must pass again
4. **Request re-review if needed** - For significant changes

---

## Step 5: Commit

After reviews pass, create a logical commit:

```bash
git add [specific files]    # NEVER use git add . or git add -A
git status                  # Verify what's staged
git diff --staged           # Review staged changes
git commit -m "$(cat <<'EOF'
type(scope): subject

Body explaining what and why
EOF
)"
```

**Warning:** Never use `git add .` or `git add -A`. Always stage specific files intentionally. Blind adds lead to:
- Committing debug code, secrets, or unrelated changes
- Losing track of what's in each commit
- Breaking atomic commit discipline

### Commit Message Guidelines

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change (no behavior change)
- `docs`: Documentation only
- `test`: Adding/updating tests
- `chore`: Build, config, tooling
- `perf`: Performance improvement

**Good Example:**
```
feat(audio): add section track for study mode

- SectionTrack component with labeled horizontal pipeline
- Progress calculation spans all sections
- Visual states: completed (filled), current (glow), upcoming (hollow)
```

**Bad Example:**
```
update code
```

---

## Step 6: Update Tracker

After each commit, update your progress tracker to capture what's done and what remains.

```bash
# Check for master tracker / phase docs
ls todos/*.md
ls todos/releases/*/
```

**Update in tracker:**
- [ ] Mark completed task as done
- [ ] Note commit hash for reference
- [ ] Review remaining tasks
- [ ] Identify next task for upcoming iteration

**Why this matters:** Trackers keep you aligned with original goals. Without updates:
- You lose track of progress
- Next steps become "guessed" instead of planned
- Scope creep goes unnoticed
- Context is lost between sessions

**Tracker update template:**
```markdown
## [Date] Iteration Update

**Completed:**
- [x] Task description — commit: abc1234

**In Progress:**
- [ ] Next task — starting next iteration

**Remaining:**
- [ ] Task 3
- [ ] Task 4
```

**Tip:** If no tracker exists, create one. Even a simple `todos/tracker.md` prevents drift.

---

## Step 7: Context Checkpoint

After committing, assess context health. See `/pb-claude-orchestration` for detailed context management strategies (compaction timing, thresholds, preservation techniques).

**Quick check:** If 3+ iterations completed or 5+ files read this session, consider checkpointing — update tracker, start fresh session.

---

## Quick Cycle Summary

```
1. Write code following standards
2. Self-review using checklist above
3. Run: make lint && make typecheck && make test
4. Request peer review (senior engineer perspective)
5. Address any feedback
6. Commit with clear message (specific files, not git add -A)
7. Update tracker (mark done, note commit, identify next)
8. Context checkpoint (assess if session should continue or refresh)
9. Repeat for next unit of work
```

---

## When to Stop and Ask

- Requirements are unclear
- Multiple valid approaches exist
- Change impacts system architecture
- Peer review raises design concerns
- Scope is expanding beyond original intent

**Don't proceed with uncertainty. Clarify first.**

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Do This Instead |
|--------------|--------------|-----------------|
| Skip self-review | Wastes peer reviewer's time | Always self-review first |
| Ignore lint warnings | Warnings become bugs | Fix all warnings |
| "It works" without tests | Technical debt | Add tests alongside code |
| Large commits | Hard to review/revert | Small, logical commits |
| Vague commit messages | History is useless | Explain what and why |
| Push and hope | Quality degradation | Verify before push |

---

## Iteration Frequency

**Commit after each meaningful unit of work:**

| After completing... | Commit type |
|---------------------|-------------|
| A new component/feature | `feat:` |
| A bug fix | `fix:` |
| A refactor (no behavior change) | `refactor:` |
| Backend API changes | `feat/fix:` |
| Config/build changes | `chore:` |
| Test additions | `test:` |

**Don't wait until end of session. Commit incrementally.**

---

## Integration with Playbook

**Part of feature development workflow:**
- `/pb-start` → Create branch, set iteration rhythm
- `/pb-resume` → Get back in context (if context switching)
- **`/pb-cycle`** → Self-review + peer review (YOU ARE HERE)
  - Includes: `/pb-testing` (write tests), `/pb-standards` (check principles), `/pb-security` (security gate)
  - Peer reviewer uses: `/pb-review-code` (code review checklist)
- `/pb-commit` → Craft atomic commits (after approval)
- `/pb-pr` → Create pull request
- `/pb-review-*` → Additional reviews if needed
- `/pb-release` → Deploy

**Key integrations during /pb-cycle:**
- **Peer Review**: `/pb-review-code` for reviewer's code review checklist
- **Testing**: `/pb-testing` for test patterns (unit, integration, E2E)
- **Security**: `/pb-security` checklist during self-review
- **Logging**: `/pb-logging` standards for logging validation
- **Standards**: `/pb-standards` for working principles
- **Documentation**: `/pb-documentation` for updating docs alongside code

**After /pb-cycle approval:**
- `/pb-commit` — Craft atomic, well-formatted commit
- `/pb-pr` — Create pull request with context

**See also**: `/docs/integration-guide.md` for how all commands work together

---

## Related Commands

- `/pb-start` — Begin new development work
- `/pb-commit` — Create atomic commits after cycle
- `/pb-pr` — Create pull request when ready
- `/pb-review-code` — Code review checklist for peer reviewers
- `/pb-testing` — Test patterns and strategies

---

*Every iteration gets the full cycle. No shortcuts.*
