# Development Cycle: Self-Review + Peer Review

Run this after completing a unit of work. Guides you through self-review, quality gates, and peer review before committing.

---

## Step 1: Self-Review

Review your own changes critically before requesting peer review.

### Code Quality Checklist

- [ ] No hardcoded values (secrets, URLs, magic numbers)
- [ ] No commented-out code left behind
- [ ] No debug print statements (unless structured logging)
- [ ] Consistent naming conventions followed
- [ ] No duplicate code - extracted to shared utilities if needed
- [ ] Error messages are user-friendly and actionable

### Security Checklist

- [ ] No secrets in code or config files
- [ ] Input validation on all external data
- [ ] SQL queries use parameterized statements
- [ ] Authentication/authorization checked appropriately
- [ ] Sensitive data not logged

### Testing Checklist

- [ ] Unit tests for new/changed functions
- [ ] Edge cases covered (empty, null, boundary values)
- [ ] Error paths tested
- [ ] Tests pass locally

### Documentation Checklist

- [ ] Complex logic has comments explaining "why"
- [ ] Public functions have clear names (prefer self-documenting code)
- [ ] API changes reflected in docs if applicable

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
git add [specific files]    # Never use git add .
git status                  # Verify what's staged
git diff --staged           # Review staged changes
git commit -m "$(cat <<'EOF'
type(scope): subject

Body explaining what and why
EOF
)"
```

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

## Quick Cycle Summary

```
1. Write code following standards
2. Self-review using checklist above
3. Run: make lint && make typecheck && make test
4. Request peer review (senior engineer perspective)
5. Address any feedback
6. Commit with clear message
7. Repeat for next unit of work
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

*Every iteration gets the full cycle. No shortcuts.*
