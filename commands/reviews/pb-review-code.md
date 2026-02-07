# Code Review

**Purpose:** Conduct thorough code review for pull requests, peer review during development iterations, or any code changes requiring review.

**Use when:**
- Reviewing a pull request before merge
- Peer reviewing during `/pb-cycle` iteration
- Reviewing code changes at any stage of development

**Mindset:** This review assumes `/pb-preamble` thinking (challenge assumptions, surface flaws, question trade-offs) and applies `/pb-design-rules` (check for clarity, simplicity, modularity, robustness).

**Resource Hint:** opus — code review demands deep reasoning across architecture, correctness, security, and maintainability

---

## When to Use

- Reviewing a pull request before merge
- Peer reviewing during `/pb-cycle` iteration
- Evaluating code changes after a significant refactor
- Spot-checking critical paths before a release

---

## Before You Start

1. **Understand the context:**
   - What problem does this change solve?
   - What's the scope of the change?
   - Are there related issues or tickets?

2. **Check the basics:**
   ```bash
   git diff main...HEAD --stat    # See scope of changes
   git log main..HEAD --oneline   # See commit history
   ```

3. **Run quality gates:**
   ```bash
   make lint        # Linting passes
   make typecheck   # Type checking passes
   make test        # All tests pass
   ```

---

## Review Checklist

### Architecture Review

- [ ] Changes align with existing patterns in the codebase
- [ ] No unnecessary complexity introduced
- [ ] Separation of concerns maintained
- [ ] Dependencies appropriate (not pulling in large libs for small tasks)
- [ ] Changes don't break existing interfaces without good reason
- [ ] Error boundaries and recovery points are well-placed
- [ ] API responses use explicit shapes, not serialized data models (see `/pb-patterns-api` Response Design)

### Correctness Review

- [ ] Logic handles all stated requirements
- [ ] Edge cases considered (empty inputs, nulls, boundaries)
- [ ] Error handling is comprehensive (no silent failures)
- [ ] Race conditions considered for concurrent operations
- [ ] State management is correct (no stale state, proper cleanup)
- [ ] Data validation at system boundaries

### Maintainability Review

- [ ] Code is readable without extensive comments
- [ ] Functions are single-purpose and reasonably sized
- [ ] Magic values extracted to constants with clear names
- [ ] Naming clearly expresses intent
- [ ] No dead code or commented-out code
- [ ] No debug artifacts (console.log, print statements)

### Security Review

- [ ] No injection vulnerabilities (SQL, command, XSS, etc.)
- [ ] Authorization properly enforced
- [ ] Sensitive operations properly audited/logged
- [ ] No information leakage in error responses or API payloads (see `/pb-security` Authorization & Access Control)
- [ ] No hardcoded secrets or credentials
- [ ] Input validation at trust boundaries

### Test Review

- [ ] Tests actually verify the behavior (not just coverage%)
- [ ] Test names describe what they verify
- [ ] Happy path and key edge cases covered
- [ ] Error paths tested
- [ ] Mocks/stubs used appropriately (not over-mocked)
- [ ] No flaky tests introduced

### Documentation Review

- [ ] Comments explain "why" not "what" (code is self-documenting)
- [ ] API changes documented (if applicable)
- [ ] README updated if behavior changes significantly
- [ ] Breaking changes clearly noted

---

## Giving Feedback

### Tone and Approach

- **Be direct** — Surface flaws clearly, don't hedge
- **Be specific** — Point to exact lines/patterns, not vague concerns
- **Be constructive** — Suggest alternatives when criticizing
- **Be curious** — Ask questions when you don't understand a choice

### Feedback Categories

Use these prefixes to clarify intent:

| Prefix | Meaning |
|--------|---------|
| **MUST** | Blocking — must be fixed before merge |
| **SHOULD** | Strong recommendation — fix unless there's good reason |
| **CONSIDER** | Suggestion — take it or leave it |
| **NIT** | Minor style/preference — non-blocking |
| **QUESTION** | Seeking clarification — not necessarily a change request |

### Example Feedback

```
MUST: This SQL query is vulnerable to injection. Use parameterized queries.
Location: src/db/users.js:42

SHOULD: This function is doing 3 things. Consider extracting validation
into a separate function for testability.
Location: src/handlers/auth.js:78-120

CONSIDER: Using a Map instead of object here would give O(1) lookups.
Not critical for current scale.

NIT: Prefer `const` over `let` since this value isn't reassigned.

QUESTION: Why did you choose to handle this error silently? Is there
a recovery path I'm missing?
```

### Approval Decision Matrix

Map findings to merge decisions:

| Finding Level | Maps To | Can Merge? |
|---------------|---------|------------|
| **Critical** | MUST | No — must fix first |
| **Warning** | SHOULD | With documented justification |
| **Suggestion** | CONSIDER, NIT | Yes |

### Review Verdicts

After completing review, provide an explicit verdict:

| Verdict | When to Use |
|---------|-------------|
| **APPROVED** | No critical or warning-level issues found |
| **CONDITIONAL** | Warning-level items only; author acknowledges trade-offs |
| **BLOCKED** | Critical issues detected; must resolve before merge |

**Example verdict:**

```
VERDICT: CONDITIONAL

Critical: 0
Warning: 2
  - Missing input validation (src/api/users.js:45)
  - No error handling for network timeout (src/services/fetch.js:78)
Suggestions: 3

Approve if author confirms validation will be added in follow-up PR,
or resolves inline before merge.
```

---

## Receiving Feedback

### For the Author

- **Welcome criticism** — Reviewers are helping you catch problems early
- **Don't argue** — If feedback is valid, just fix it
- **Ask for clarity** — If feedback is unclear, ask for specific suggestions
- **Respond to everything** — Every comment deserves acknowledgment
- **Learn from patterns** — If same feedback keeps coming, internalize it

### Resolving Disagreements

1. **Understand the concern** — Restate it to confirm understanding
2. **Explain your reasoning** — Share context the reviewer may lack
3. **Find common ground** — Often there's a third option
4. **Escalate if needed** — Get a third opinion for significant disagreements
5. **Document decisions** — Note why a particular choice was made

---

## Review Workflow

### For Pull Requests

```
1. Read PR description and linked issues
2. Run the code locally (if significant changes)
3. Review diff file by file
4. Run test suite
5. Leave feedback using categories above
6. Approve, Request Changes, or Comment
```

### For Peer Review (during /pb-cycle)

```
1. Author explains the changes and intent
2. Review code together (sync or async)
3. Walk through the checklist above
4. Discuss any concerns directly
5. Author addresses feedback
6. Re-review if significant changes
```

---

## Red Flags

Stop and discuss if you see:

- **Breaking changes** without migration path
- **Security vulnerabilities** (injection, auth bypass, data exposure)
- **Data loss potential** (destructive operations without backup/undo)
- **Performance regression** (N+1 queries, unbounded loops, missing pagination, oversized API payloads)
- **Scope creep** — Changes unrelated to stated purpose
- **Missing tests** for critical paths
- **Hardcoded secrets** or credentials

---

## Quick Review (Time-Boxed)

For smaller changes or when time is limited:

1. **Skim the diff** — Get overall sense of change
2. **Check the critical paths** — Focus on error handling, security, data flow
3. **Verify tests exist** — At minimum, happy path covered
4. **Run quality gates** — lint, typecheck, test
5. **Spot-check naming** — If names are clear, code is likely clear

---

## Integration with Playbook

**During development cycle:**
- Author runs `/pb-cycle` (includes self-review)
- Author requests peer review
- Reviewer runs `/pb-review-code` (YOU ARE HERE)
- Author addresses feedback
- Author commits with `/pb-commit`

**During PR review:**
- Reviewer uses `/pb-review-code` checklist
- Combine with `/pb-security` for security-critical changes
- Combine with `/pb-review-tests` for test coverage analysis

---

## Related Commands

- `/pb-cycle` — Author's development iteration (includes self-review)
- `/pb-review` — Comprehensive periodic project review orchestrator
- `/pb-review-hygiene` — Code quality and operational readiness
- `/pb-review-tests` — Test coverage review
- `/pb-security` — Security audit

---

*Every change deserves thoughtful review. Catch problems in review, not production.*
