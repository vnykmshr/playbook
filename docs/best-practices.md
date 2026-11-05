# Best Practices Guide

Proven patterns and anti-patterns from the Engineering Playbook in practice.

---

## Development Process Best Practices

### DO:Commit Frequently and Logically

**Practice**: Create commits after each meaningful unit of work (feature, fix, refactor), not at end of day.

**Why**: Logical commits make git history useful for understanding decisions and debugging. They also make cherry-picking and reverting easier.

---

### DO:Self-Review Before Requesting Peer Review

**Practice**: Always run `/pb-review` before requesting peer review.

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

**Why**: Small PRs are reviewed faster, are easier to understand, and reduce merge conflicts.

---

### DO:Write Clear Commit Messages

**Practice**: Use the format from `/pb-commit`.

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

**Why**: Large files bloat git history and make cloning slow. Secrets in git are impossible to truly remove.

---

## Code Review Best Practices

### DO:Request Review Early and Often

**Practice**: Don't wait until code is "perfect" to request review. Review feedback often improves the design.

**Why**: Early feedback prevents wasted effort on wrong approaches.

---

### DO:Provide Constructive Feedback

**Practice**: When reviewing, explain the "why" behind suggestions.

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

**Why**: Edge case testing prevents production bugs. Most bugs hide in error paths.

---

### DO:Use Meaningful Test Names

**Practice**: Test names should describe what they test.

**Why**: Meaningful test names serve as documentation. They help find failing tests quickly.

---

### DON'T:Have Flaky Tests

**Anti-Pattern**: Tests that sometimes pass and sometimes fail (usually due to timing, randomness, or external dependencies)

**Why**: Flaky tests destroy team trust in the test suite. People stop believing failures.

---

## Architecture Best Practices

### DO:Document Architectural Decisions

**Practice**: Use `/pb-adr` to record decisions as you make them.

**Why**: Documented decisions preserve knowledge. Future engineers understand the "why," not just the "what."

---

### DO:Reference Relevant Patterns

**Practice**: Before implementing a feature, check `/pb-patterns-*` for relevant patterns.

**Why**: Patterns are proven solutions. Using them improves consistency and reduces bugs.

---

### DO:Plan for Observability Early

**Practice**: As you design, plan what you'll monitor.

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

**Practice**: Use `/pb-standup` for daily async status.

**Why**: Async standups enable distributed teams and create searchable record of progress.

---

### DO:Discuss Big Changes Before Implementing

**Practice**: For major changes, discuss approach before spending days on implementation.

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

**Practice**: Never trust user input. Validate at API boundary.

**Why**: Input validation prevents injection attacks and data corruption.

---

### DO:Check Authorization for Every Action

**Practice**: Every operation should verify user is authorized.

**Why**: Authorization checks prevent unauthorized access.

---

### DON'T:Log Sensitive Data

**Anti-Pattern**: Logging passwords, tokens, credit card numbers

**Why**: Logs often end up in monitoring systems. Secrets in logs are a major security risk.

---

## Performance Best Practices

### DO:Measure Before Optimizing

**Practice**: Profile to identify bottlenecks, then optimize.

**Why**: Optimization without data is guessing. You optimize wrong things and waste time.

---

### DO:Monitor Production After Changes

**Practice**: After optimization, verify it actually helped.

**Why**: Verification ensures optimization actually helped and didn't break something else.

---

### DON'T:Prematurely Optimize

**Anti-Pattern**: Optimizing code before it's proven slow

**Why**: Premature optimization wastes time and reduces readability.

---

## Release Best Practices

### DO:Use Automated Deployments

**Practice**: Automate deployment to reduce human error.

**Why**: Automation is reliable. Manual steps are error-prone.

---

### DO:Have Rollback Plan

**Practice**: Before releasing, know how to rollback.

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

- **[Getting Started](getting-started.md)** - Pick a workflow
- **[Decision Guide](decision-guide.md)** - Find a command
- **[FAQ](faq.md)** - Get answers
- **[Integration Guide](integration-guide.md)** - Workflow maps and step-by-step scenarios
