# Best Practices Guide

Proven patterns and anti-patterns from the Engineering Playbook in practice.

---

## Development Process Best Practices

### DO:Commit Frequently and Logically

**Practice**: Create commits after each meaningful unit of work (feature, fix, refactor), not at end of day.

```bash
# Good: Logical commits
git commit -m "feat: add user authentication"
git commit -m "test: add auth tests"
git commit -m "docs: update README with auth setup"

# Bad: Monolithic commit
git commit -m "add auth and tests and update docs"
```

**Why**: Logical commits make git history useful for understanding decisions and debugging. They also make cherry-picking and reverting easier.

---

### DO:Self-Review Before Requesting Peer Review

**Practice**: Always use `/pb-cycle` self-review before requesting peer review.

Checklist from self-review:
- [ ] Code follows team standards
- [ ] No hardcoded values (everything configurable)
- [ ] No commented-out code
- [ ] No debug logs left in
- [ ] Tests pass and cover new code
- [ ] No obvious bugs or edge cases missed
- [ ] Documentation updated alongside code

**Why**: Self-review catches 80% of issues before peer review. It respects reviewers' time and speeds up the process.

---

### DO:Keep Pull Requests Small

**Practice**: Target PR scope: one feature or one fix, 200-500 lines of code.

```
Good PR: "Add password reset feature" (adds 150 lines)
Bad PR: "Auth system overhaul" (adds 2,000 lines)
```

**Why**: Small PRs are reviewed faster, are easier to understand, and reduce merge conflicts.

---

### DO:Write Clear Commit Messages

**Practice**: Use format from `/pb-commit`:
```
type(scope): short subject (50 chars max)

Body explaining what and why (not how).
Link to issues if applicable.
```

Example:
```
feat(auth): implement password reset flow

Adds password reset via email token. Tokens expire in 24 hours.
Implements rate limiting (5 resets per hour per user) to prevent abuse.

Fixes #42, relates to #38
```

**Why**: Clear commit messages become documentation. Future engineers understand not just what changed, but why.

---

### DON'T:Skip Testing

**Anti-Pattern**: "I'll add tests later" or "This doesn't need tests"

**Reality**:
- Later never comes (tests don't get written)
- Everything needs tests (or shouldn't be in code)
- Bugs in untested code get to production

**Solution**: Write tests alongside code using `/pb-testing`. Tests are part of the feature, not optional.

---

### DON'T:Commit Large Files

**Anti-Pattern**: Committing large binaries, databases, or configuration with secrets

```bash
# Bad
git add credentials.json
git commit -m "add config"

# Good
echo "credentials.json" >> .gitignore
git commit -m "chore: add .gitignore"
```

**Why**: Large files bloat git history and make cloning slow. Secrets in git are impossible to truly remove.

---

## Code Review Best Practices

### DO:Request Review Early and Often

**Practice**: Don't wait until code is "perfect" to request review. Review feedback often improves the design.

```
Good: Request review after implementing core logic
Bad: Request review only after everything is polished
```

**Why**: Early feedback prevents wasted effort on wrong approaches.

---

### DO:Provide Constructive Feedback

**Practice**: When reviewing, explain the "why" behind suggestions:

```
Good: "This should validate input before processing.
       See [OWASP input validation](url).
       Example: users can inject SQL."

Bad: "This is wrong. Fix it."
```

**Why**: Constructive feedback helps reviewees learn and build trust.

---

### DO:Request Changes for Real Issues Only

**Practice**: Distinguish between "must fix" and "nice to have":

| Category | Action |
|----------|--------|
| **Security issue** | Request changes |
| **Performance problem** | Request changes |
| **Bug** | Request changes |
| **Code style preference** | Suggest, don't require |
| **Alternative approach** | Discuss, let author decide |

**Why**: Requiring changes for everything slows down development and demoralizes authors.

---

### DON'T:Approve Without Reading Code

**Anti-Pattern**: Approving PRs without thoroughly reviewing

**How to detect**:
- No specific comments
- Approved within minutes of creation
- Reviewer doesn't understand the changes

**Why**: Rubber-stamp reviews don't catch bugs. Reviews exist to improve code quality.

---

## Quality & Testing Best Practices

### DO:Test Edge Cases

**Practice**: For each feature, test:
- Happy path (normal usage)
- Error cases (what can go wrong)
- Boundary cases (limits and extremes)
- Concurrency (if applicable)

```python
# Good test coverage
def test_password_reset_successful():
    """Happy path: valid reset token"""

def test_password_reset_expired_token():
    """Error: token expired"""

def test_password_reset_invalid_email():
    """Error: user not found"""

def test_password_reset_rate_limited():
    """Boundary: too many attempts"""
```

**Why**: Edge case testing prevents production bugs. Most bugs hide in error paths.

---

### DO:Use Meaningful Test Names

**Practice**: Test names should describe what they test:

```python
# Good: reads like a specification
test_user_cannot_reset_password_with_expired_token()
test_rate_limiter_allows_5_resets_per_hour()
test_password_must_contain_uppercase_and_digit()

# Bad: vague or redundant
test_reset()
test_password1()
test_it_works()
```

**Why**: Meaningful test names serve as documentation. They help find failing tests quickly.

---

### DON'T:Have Flaky Tests

**Anti-Pattern**: Tests that sometimes pass and sometimes fail (usually due to timing, randomness, or external dependencies)

```python
# Bad: depends on system time
def test_token_expires():
    token = create_token()
    time.sleep(1)  # Flaky: might take longer
    assert is_expired(token)

# Good: use fixed time
def test_token_expires():
    token = create_token(created_at=now - 25*hours)
    assert is_expired(token)
```

**Why**: Flaky tests destroy team trust in the test suite. People stop believing failures.

---

## Architecture Best Practices

### DO:Document Architectural Decisions

**Practice**: Use `/pb-adr` to record decisions as you make them.

```
Title: Use async/await for database queries

Status: Decided

Context:
- Database calls block server threads
- Need to handle 1000s of concurrent users

Decision:
- Use async/await pattern for all DB queries
- Switch to connection pooling

Consequences:
- Need async-aware framework
- More complex error handling
- Better scalability
```

**Why**: Documented decisions preserve knowledge. Future engineers understand the "why," not just the "what."

---

### DO:Reference Relevant Patterns

**Practice**: Before implementing a feature, check `/pb-patterns-*` for relevant patterns.

```
Building a notification system?
→ Check /pb-patterns-async (job queues, workers)
→ Check /pb-patterns-distributed (event-driven)
→ Use established patterns, don't reinvent
```

**Why**: Patterns are proven solutions. Using them improves consistency and reduces bugs.

---

### DO:Plan for Observability Early

**Practice**: As you design, plan what you'll monitor:

```
Feature: User signup
Metrics to track:
- Signup attempt rate
- Success rate
- Error rate by error type
- Signup duration (p50, p95, p99)

Alerting:
- Alert if success rate < 95%
- Alert if duration p95 > 2s
```

**Why**: Observable systems are easier to debug. Observability planned in design is better than bolted on later.

---

### DON'T:Build Without Measuring

**Anti-Pattern**: "We can optimize later" without gathering baseline metrics

**Reality**:
- Optimization without data is guessing
- You optimize the wrong things
- No way to measure improvement

**Solution**: Use `/pb-performance` to establish baselines and measure improvements.

---

## Team & Communication Best Practices

### DO:Write Async Standups

**Practice**: Use `/pb-standup` for daily async status:

```
## Today's Status

### Completed
- [YES]Implemented password reset feature
- [YES]Added integration tests

### In Progress
- Working on password complexity validation
- PR under review

### Blockers
- None

### Help Needed
- Review on PR #42 would be appreciated
```

**Why**: Async standups enable distributed teams and create searchable record of progress.

---

### DO:Discuss Big Changes Before Implementing

**Practice**: For major changes, discuss approach before spending days on implementation.

```
Bad: Implement for 3 days, submit PR, get feedback
Good: Discuss approach for 30 min, implement for 1 day, PR, iterate
```

**Why**: Discussion prevents wasted effort on wrong approaches.

---

### DON'T:Use Meeting for Information Transfer

**Anti-Pattern**: Using synchronous meetings to share information

**Better**: Use documentation, async standups, and discussion threads

**When to meet**: Decisions, brainstorming, conflict resolution

**Why**: Async communication scales better and respects people's time zones and focus time.

---

## Security Best Practices

### DO:Validate Input at Boundaries

**Practice**: Never trust user input. Validate at API boundary:

```python
# Good: validate at boundary
@app.post("/reset-password")
def reset_password(request):
    token = validate_and_sanitize(request.token)  # Validate here
    new_password = validate_password_strength(request.password)
    # ... rest of logic

# Bad: trust input, validate later
@app.post("/reset-password")
def reset_password(request):
    token = request.token  # No validation
    new_password = request.password  # No validation
    # ... logic might fail mysteriously
```

**Why**: Input validation prevents injection attacks and data corruption.

---

### DO:Check Authorization for Every Action

**Practice**: Every operation should verify user is authorized:

```python
# Good: always check auth
@app.delete("/users/{user_id}")
def delete_user(user_id, current_user):
    if not current_user.is_admin:
        raise PermissionError()
    # ... delete

# Bad: forget auth check
@app.delete("/users/{user_id}")
def delete_user(user_id, current_user):
    # ... delete user without checking permission
```

**Why**: Authorization checks prevent unauthorized access.

---

### DON'T:Log Sensitive Data

**Anti-Pattern**: Logging passwords, tokens, credit card numbers

```python
# Bad
logger.info(f"User {email} logging in with password {password}")

# Good
logger.info(f"User {email} logging in")
```

**Why**: Logs often end up in monitoring systems. Secrets in logs are a major security risk.

---

## Performance Best Practices

### DO:Measure Before Optimizing

**Practice**: Profile to identify bottlenecks, then optimize:

```
Bad: "Let's use caching because caching is fast"
Good: "Profile shows DB query is 10s of response time.
       Add caching, re-measure, confirm improvement"
```

**Why**: Optimization without data is guessing. You optimize wrong things and waste time.

---

### DO:Monitor Production After Changes

**Practice**: After optimization, verify it actually helped:

```
Before: p95 latency = 500ms
After optimization: 250ms
Verified with: tail latency metrics in prod, 1hr monitoring window
```

**Why**: Verification ensures optimization actually helped and didn't break something else.

---

### DON'T:Prematurely Optimize

**Anti-Pattern**: Optimizing code before it's proven slow

```
Bad: Spend 2 days optimizing algorithm for speed
     when database query is the bottleneck

Good: Profile first, optimize bottleneck
```

**Why**: Premature optimization wastes time and reduces readability.

---

## Release Best Practices

### DO:Use Automated Deployments

**Practice**: Automate deployment to reduce human error:

```
Good: git push → CI tests → auto-deploy to staging →
      manual approval → auto-deploy to prod

Bad: Manual deployment steps on shared script
```

**Why**: Automation is reliable. Manual steps are error-prone.

---

### DO:Have Rollback Plan

**Practice**: Before releasing, know how to rollback:

```
Feature: New payment system
Rollback plan: Revert to previous deployment (5 min),
              or disable feature flag (1 min)

Test rollback procedure before release
```

**Why**: Rollback plans mean you can recover fast if something breaks.

---

### DON'T:Release on Friday Afternoon

**Anti-Pattern**: Pushing code right before weekend

**Why**: If something breaks, no one is available to fix it for 2 days.

---

## Summary

| Do | Don't |
|----|-------|
| Commit frequently and logically | Skip testing |
| Self-review before peer review | Commit large binaries or secrets |
| Keep PRs small | Approve without reading code |
| Write clear commit messages | Leave flaky tests |
| Document decisions | Optimize without measuring |
| Test edge cases | Log sensitive data |
| Plan observability early | Release on Friday |
| Validate at boundaries | Skip authorization checks |
| Measure before optimizing | Optimize prematurely |
| Have rollback plans | Release without plan |

---

## Next Steps

- **[Getting Started](getting-started.md)** — Pick a workflow
- **[Decision Guide](decision-guide.md)** — Find a command
- **[FAQ](faq.md)** — Get answers
- **[Integration Guide](integration-guide.md)** — Deep dive on workflows
