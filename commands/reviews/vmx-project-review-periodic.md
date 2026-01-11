# Periodic Project Review Prompt

**Purpose:** Conduct a comprehensive multi-perspective review of the entire codebase to identify issues, improvements, and ensure production readiness.

**Recommended Frequency:** Monthly or before major releases

---

## Prompt

```
Conduct a comprehensive multi-perspective project review of this codebase. Use parallel agents for each perspective to maximize coverage and minimize bias.

## Review Perspectives

Launch the following review agents in parallel:

### 1. Security Audit
- Authentication/authorization vulnerabilities
- Input validation and sanitization
- SQL injection, XSS, CSRF protection
- Secrets management and exposure
- Dependency vulnerabilities (outdated packages)
- Rate limiting and abuse prevention
- Session management security
- Production configuration validation

### 2. Performance Review
- Database query efficiency (N+1, missing indexes)
- API response times and bottlenecks
- Frontend bundle size and code splitting
- Caching strategy effectiveness
- Memory leaks and resource cleanup
- Connection pool configuration
- Background job performance

### 3. Accessibility Audit
- WCAG 2.1 AA compliance
- Keyboard navigation completeness
- Screen reader compatibility
- Focus management and skip links
- Color contrast and visual indicators
- Error announcements and form labels
- Touch target sizes (mobile)

### 4. Architecture Review
- Code organization and separation of concerns
- Dependency management and coupling
- Error handling consistency
- Logging and observability
- Configuration management
- Database schema design
- API design consistency

### 5. Test Coverage Analysis
- Unit test coverage by module
- Integration test coverage for critical paths
- Missing test scenarios
- Test quality and maintainability
- Edge cases and error paths
- Mock usage appropriateness

### 6. Code Quality Review
- Code duplication and DRY violations
- Function/method complexity (cyclomatic)
- Dead code and unused imports
- Naming conventions consistency
- Documentation completeness
- Type safety (TypeScript strict, Python mypy)
- Linting compliance

### 7. Documentation Review
- README accuracy and completeness
- API documentation (OpenAPI/Swagger)
- Code comments quality
- Architecture decision records
- Deployment and operations guides
- Troubleshooting documentation

### 8. UX Consistency Review
- Design system adherence
- Component reuse patterns
- Loading states and error handling
- Mobile responsiveness
- Dark/light mode consistency
- Micro-interactions and feedback

### 9. Domain Expert Review (if applicable)
- Domain model accuracy
- Business logic correctness
- Content quality and accuracy
- Terminology consistency

### 10. End User Perspective
- User journey friction points
- Onboarding experience
- Error message clarity
- Feature discoverability
- Performance perception

## Output Format

For each perspective, provide:

1. **Grade:** A-F with brief justification
2. **Strengths:** What's working well (2-3 items)
3. **Issues Found:** Categorized by severity
   - CRITICAL: Must fix before production
   - HIGH: Should fix soon
   - MEDIUM: Address when convenient
   - LOW: Nice to have
4. **Specific Recommendations:** With file locations

## Consolidation

After all perspectives complete, create a consolidated report:

1. **Executive Summary**
   - Overall health score
   - Production readiness assessment
   - Top 5 priorities

2. **Issue Tracker**
   | # | Issue | Severity | Perspective | Location | Est. Effort |
   |---|-------|----------|-------------|----------|-------------|

3. **Quick Wins**
   - Items fixable in <15 minutes

4. **Technical Debt**
   - Items to track for future sprints

5. **Deferred Items**
   - Items intentionally not addressing (with rationale)

## Session Tracking

Create/update a review document at `todos/project-review-YYYY-MM-DD.md` with:
- Session number and duration
- Items completed this session
- Remaining items with status
- Commits created

## Verification Steps

After identifying issues, run:
1. `npm run lint` / `npm run build` (frontend)
2. `mypy` / `pytest` (backend)
3. Verify no regressions introduced

## Review Cadence

- **Pre-release:** Full review before major versions
- **Monthly:** Security + Test Coverage + Code Quality
- **Quarterly:** All perspectives
- **Post-incident:** Targeted review of affected areas
```

---

## Usage Notes

1. **Scope Control:** For large codebases, focus on changed files since last review:
   ```
   git diff --name-only <last-review-commit>..HEAD
   ```

2. **Incremental Reviews:** Track review commit hash to enable delta reviews

3. **Priority Alignment:** Before starting, confirm with stakeholders:
   - Is this a pre-release review?
   - Any specific concerns to prioritize?
   - Time budget for fixes?

4. **Follow-up:** Schedule remediation session after review to address findings

---

## Example Invocation

```
Conduct a periodic project review of this codebase. Focus on changes since
commit abc1234. This is a pre-release review for v1.12.0.

Priorities:
1. Security (we're adding user auth features)
2. Test coverage (new newsletter module)
3. Performance (users reported slow loading)

Time budget: 2 hours for review, 4 hours for fixes.

Create the review document at todos/project-review-2025-01-15.md
```

---

## Evolution Notes

This prompt should evolve based on:
- Recurring issues found in reviews
- New perspectives relevant to the project
- Tooling improvements (e.g., automated scanners)
- Team feedback on review usefulness

**Last Updated:** 2025-12-20
**Version:** 1.0
