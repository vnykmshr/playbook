---
name: "pb-review-tests"
title: "Test Suite Review (Coverage & Reliability)"
category: "reviews"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-review', 'pb-review-code', 'pb-review-hygiene', 'pb-testing', 'pb-cycle']
last_reviewed: "2026-02-18"
last_evolved: "2026-02-18"
version: "2.0.0"
version_notes: "v2.13.1: Clarified focus on test quality (not code quality). Part of code review family decision tree."
breaking_changes: []
---
# Test Suite Review (Coverage & Reliability)

**Purpose:** Comprehensive review of the project's unit and integration tests. Focus on test quality, coverage gaps, flakiness, and brittleness.

**Use when:** You want to audit **test suite health** (not code quality or specific code changes). Focuses on: coverage gaps, flaky tests, brittle assertions, duplication.

**When NOT to use:** For reviewing specific code changes (use `/pb-review-code` instead) or general codebase health (use `/pb-review-hygiene` instead).

**Recommended Frequency:** Monthly or when test suite feels slow/flaky

**Mindset:** This review embodies `/pb-preamble` thinking (question assumptions, surface flaws) and `/pb-design-rules` thinking (tests should verify Clarity, verify Robustness, and confirm failures are loud).

Question test assumptions. Challenge coverage claims. Point out flaky or brittle tests. Surface duplication. Your role is to find problems, not validate the test suite.

**Resource Hint:** opus — evaluating test quality requires deep reasoning about coverage gaps, brittleness, and test design

---

## Code Review Family Decision Tree

See `/pb-review-code` for the complete decision tree. Key distinction:

- **Use `/pb-review-code`** for reviewing a specific PR or commit
- **Use `/pb-review-hygiene`** for code quality and codebase health checks
- **Use `/pb-review-tests`** for test suite quality, coverage, and reliability focus

---

## When to Use

- **Monthly test suite maintenance** ← Primary use case (scheduled, periodic)
- **When tests are slow or flaky** (investigate reliability)
- **After major refactoring** (verify tests still make sense)
- **When coverage numbers don't match confidence** (coverage gaps)
- **Before major releases** (test suite health check before shipping)

---

## Review Perspectives

Act as **senior engineer and test architect** responsible for a test suite that is:
- Lean (no redundant tests)
- Reliable (no flaky tests)
- Meaningful (tests behavior, not implementation)
- Maintainable (easy to update when code changes)

---

## Review Goals

### 1. Prune Bloat

- [ ] Identify redundant, outdated, or overly defensive tests
- [ ] Remove or merge tests that don't add new coverage
- [ ] Flag duplicated logic or repetitive data setups
- [ ] Delete tests that test framework behavior, not your code

### 2. Evaluate Practicality

- [ ] Tests validate meaningful behavior, not implementation details
- [ ] Tests are not too brittle or reliant on unstable mocks
- [ ] Test naming and descriptions are clear and human-friendly
- [ ] Failures produce useful error messages

### 3. Assess Integration Depth

- [ ] Integration tests verify real system interactions (APIs, DB, queues)
- [ ] Integration tests don't duplicate what unit tests already cover
- [ ] No slow, flaky, or unmaintainable integration tests
- [ ] E2E tests focus on critical user journeys only

### 4. Check Test Organization

- [ ] Tests are co-located or logically organized
- [ ] Shared fixtures and helpers are reusable
- [ ] Test data is sane and isolated
- [ ] No hidden dependencies between tests

---

## Test Quality Checklist

### Unit Tests

| Check | Question |
|-------|----------|
| Coverage | Are critical code paths covered? |
| Isolation | Do tests run independently? |
| Speed | Do unit tests run in < 30 seconds total? |
| Clarity | Can you understand what failed from the error? |
| Maintainability | Will tests break if implementation changes? |

### Integration Tests

| Check | Question |
|-------|----------|
| Real interactions | Do they test actual service boundaries? |
| No duplication | Do they avoid re-testing unit-covered logic? |
| Reliability | Do they pass consistently (no flakiness)? |
| Speed | Are they fast enough for CI? |
| Cleanup | Do they clean up test data properly? |

### Test Data

| Check | Question |
|-------|----------|
| Isolation | Is test data independent per test? |
| Realism | Does test data reflect real scenarios? |
| Maintenance | Is test data easy to update? |
| Security | No production data or secrets in tests? |

---

## Common Problems to Find

| Problem | Signal | Fix |
|---------|--------|-----|
| Flaky tests | Random failures, works on retry | Find race condition or mock issue |
| Brittle tests | Break when refactoring | Test behavior, not implementation |
| Slow tests | CI takes > 10 min | Parallelize or reduce scope |
| Low value tests | Test trivial getters/setters | Delete them |
| Duplicate tests | Same assertion in multiple tests | Consolidate |
| Missing tests | Critical paths untested | Add focused tests |

---

## Deliverables

### 1. Summary of Key Issues

Overview of:
- Bloat (redundant tests)
- Duplication (same test logic repeated)
- Poor coverage (critical paths missing)
- Misaligned focus (testing wrong things)
- Reliability issues (flaky tests)

### 2. Concrete Recommendations

What to:
- **Delete** — Tests that add no value
- **Merge** — Duplicate tests
- **Rewrite** — Brittle or unclear tests
- **Add** — Missing coverage for critical paths

### 3. Next Steps Plan

Specific actions:
- Split slow suites
- Remove problematic mocks
- Improve naming conventions
- Add missing edge case tests

### 4. Metrics to Track

- Test runtime (total and by suite)
- Coverage % (lines, branches, critical paths)
- Flakiness rate (failures per run)
- Test count (unit vs integration vs E2E)

---

## Example Output

```markdown
## Summary of Key Issues

**Overall Health:** Needs Attention

- Test suite runs in 8 minutes (target: < 5 min)
- 3 flaky tests in API suite causing CI failures
- 15% of tests are redundant (same assertions repeated)
- Missing coverage for payment flow error handling
- Integration tests duplicate unit test coverage

## Concrete Recommendations

### Delete
- `test_user_exists.py` — Duplicates `test_user_creation.py`
- `test_config_defaults.py` — Tests framework, not our code

### Rewrite
- `test_api_auth.py` — Brittle, breaks on header changes
- `test_payment_flow.py` — No error path coverage

### Add
- Error handling tests for payment service
- Edge cases for user validation

## Next Steps

1. [1 hour] Fix 3 flaky tests in API suite
2. [2 hours] Delete 12 redundant tests
3. [4 hours] Add payment error handling tests
4. [1 hour] Split slow integration suite

## Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Total runtime | 8 min | < 5 min |
| Flaky tests | 3 | 0 |
| Unit test coverage | 72% | 80% |
| Integration tests | 45 | 30 (reduce) |
```

---

## Related Commands

- `/pb-review` — Orchestrate comprehensive multi-perspective review
- `/pb-review-hygiene` — Code quality and operational readiness
- `/pb-testing` — Testing guidance and patterns
- `/pb-cycle` — Self-review + peer review iteration

---

**Last Updated:** 2026-01-21
**Version:** 2.0
