# Development Checklists & Quality Gates

Single source of truth for all checklists used in the playbook. Reference these from `/pb-cycle`, `/pb-templates`, `/pb-guide`, and other commands.

---

## Self-Review Checklist

Run through this before requesting peer review. Use after development, before `/pb-cycle` step 2.

### Code Quality
- [ ] No hardcoded values (secrets, URLs, magic numbers)
- [ ] No commented-out code left behind
- [ ] No debug print statements (unless structured logging)
- [ ] Consistent naming conventions followed
- [ ] No duplicate code - extracted to shared utilities
- [ ] Error messages are user-friendly and actionable

### Security
- [ ] No secrets in code or config files
- [ ] Input validation on all external data
- [ ] SQL queries use parameterized statements
- [ ] Authentication/authorization checked appropriately
- [ ] Sensitive data not logged

### Testing
- [ ] Unit tests for new/changed functions
- [ ] Edge cases covered (empty, null, boundary values)
- [ ] Error paths tested
- [ ] Tests pass locally (`go test ./...`, `npm test`, `pytest`, etc.)

### Documentation
- [ ] Complex logic has comments explaining "why"
- [ ] Public functions have clear names and doc comments
- [ ] API changes reflected in docs if applicable
- [ ] README updated if new setup steps needed

### Database (if applicable)
- [ ] Migration is reversible (has DOWN migration)
- [ ] Indexes added for query patterns
- [ ] Foreign key constraints appropriate
- [ ] No breaking changes to existing data

### Performance
- [ ] No N+1 query patterns
- [ ] Pagination on list endpoints
- [ ] Appropriate timeouts set
- [ ] No unbounded loops or recursion

---

## Peer Review Checklist

For the reviewing engineer. Check these after code is submitted for review.

### Correctness
- [ ] Logic solves the stated problem
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No regressions in existing functionality

### Quality
- [ ] Code is readable and maintainable
- [ ] Naming is clear and consistent
- [ ] Functions are not too long (single responsibility)
- [ ] No code duplication
- [ ] Performance is acceptable

### Security
- [ ] No security vulnerabilities introduced
- [ ] Secrets are not exposed
- [ ] Input validation is complete
- [ ] Authorization checks are correct

### Testing
- [ ] Tests cover new functionality
- [ ] Tests cover error paths
- [ ] Test naming is clear

### Architecture
- [ ] Change fits existing patterns
- [ ] No unnecessary dependencies added
- [ ] API design is consistent
- [ ] Database schema changes are appropriate

---

## Code Quality Gates Checklist

Run before committing. All must pass to proceed.

- [ ] `make lint` passes (or equivalent linting)
- [ ] `make typecheck` passes (or equivalent type checking)
- [ ] `make test` passes (or equivalent test suite)
- [ ] `make format` passes (or equivalent formatting)
- [ ] No breaking changes to public APIs (unless documented)

---

## Pre-Release Checklist

Before merging to main and releasing.

- [ ] All tests passing
- [ ] All linting passing
- [ ] Code reviewed and approved
- [ ] CHANGELOG updated
- [ ] Version number bumped
- [ ] Documentation updated
- [ ] Monitoring/alerting configured (M/L tiers)
- [ ] Feature flags configured (if applicable)
- [ ] Rollback plan documented

---

## Pre-Deployment Checklist

Before deploying to production.

- [ ] Pre-release checklist completed
- [ ] Health checks configured
- [ ] Deployment plan reviewed
- [ ] Rollback tested
- [ ] On-call engineer notified
- [ ] Stakeholders informed (if applicable)

---

## Post-Deployment Checklist

After deployment to production.

- [ ] Monitor error rates (0 duration)
- [ ] Monitor latency (0 duration)
- [ ] Monitor resource usage (0 duration)
- [ ] Check logs for anomalies (0 duration)
- [ ] Verify SLO adherence (for M/L tiers, 1+ hours)
- [ ] Smoke test key flows (if applicable)
- [ ] Notify stakeholders of successful deployment

---

## Documentation Checklist

For updating documentation alongside code changes.

### README
- [ ] Overview/purpose still accurate
- [ ] Setup instructions still work
- [ ] Examples still valid
- [ ] New features documented
- [ ] Known limitations updated

### API/Integration Documentation
- [ ] New endpoints/methods documented
- [ ] Request/response examples updated
- [ ] Error codes documented
- [ ] Authentication/authorization updated
- [ ] OpenAPI spec updated (if applicable)

### Architecture/Design Documentation
- [ ] Architecture diagrams updated
- [ ] Data flow diagrams updated
- [ ] Component descriptions updated
- [ ] Decision rationale documented

### Troubleshooting/Runbooks
- [ ] New error scenarios documented
- [ ] Debugging instructions included
- [ ] Common issues updated
- [ ] Runbooks created for operational changes

---

## Security Checklist (Quick Review)

Quick security check for S tier changes. Reference `/pb-security` for comprehensive list.

- [ ] No secrets in code
- [ ] Input validation present
- [ ] Authentication required where needed
- [ ] Authorization checks present
- [ ] Sensitive data not logged
- [ ] HTTPS used where applicable
- [ ] No known vulnerabilities in dependencies

---

## Performance Review Checklist

Before shipping performance-sensitive changes.

- [ ] Load test completed
- [ ] Stress test completed
- [ ] Latency targets met
- [ ] Memory usage acceptable
- [ ] Database query performance acceptable
- [ ] Caching strategy effective
- [ ] No resource leaks
- [ ] Monitoring configured for metrics

---

## Testing Strategy Checklist

Verify test coverage before considering complete.

- [ ] Happy path tested
- [ ] Error paths tested
- [ ] Edge cases tested (empty, null, boundary)
- [ ] Concurrency tested (if applicable)
- [ ] Integration tested (if applicable)
- [ ] Integration with existing code tested
- [ ] Backwards compatibility tested
- [ ] Performance tested (if applicable)

---

## Migration Checklist (Database)

For database schema or data migration changes.

- [ ] Migration script tested on staging data
- [ ] Rollback script tested and verified
- [ ] Data validation queries prepared
- [ ] Deployment window planned
- [ ] Communication sent to stakeholders
- [ ] Monitoring configured for migration
- [ ] Post-migration verification script prepared
- [ ] Original data backed up
- [ ] Migration can be done without downtime
- [ ] Version that requires new schema is ready

---

## Release Checklist

Final checklist before tagging a release.

- [ ] Version bumped in package.json / pyproject.toml / etc.
- [ ] CHANGELOG.md updated with all changes
- [ ] All commits on main are intentional
- [ ] All tests passing
- [ ] All linting passing
- [ ] Documentation updated for public changes
- [ ] Backwards compatibility confirmed (or breaking changes documented)
- [ ] Deployment procedures documented
- [ ] Monitoring/alerting for new features configured

---

## Incident Response Checklist

During production incident.

- [ ] Incident declared (who, what, when, where)
- [ ] On-call engineer paged (if not already)
- [ ] Communication channel opened
- [ ] Customer/stakeholder notified (if applicable)
- [ ] Root cause identified (or incident marked "investigating")
- [ ] Mitigation attempted
- [ ] If mitigation successful: monitor closely, schedule RCA
- [ ] If mitigation unsuccessful: escalate, attempt rollback
- [ ] All actions documented with timestamps
- [ ] Post-incident RCA scheduled within 24 hours

---

## Accessibility (WCAG 2.1 AA) Checklist

For any user-facing changes (web UI, mobile UI).

- [ ] Keyboard navigation works (Tab, Enter, Escape)
- [ ] Focus indicators visible in light and dark modes
- [ ] ARIA labels present on interactive elements
- [ ] Decorative icons hidden with `aria-hidden="true"`
- [ ] Modal/drawer focus trapped and restored
- [ ] Touch targets minimum 44x44px
- [ ] Color contrast ratio >= 4.5:1 (normal text), 3:1 (large text)
- [ ] Images have alt text
- [ ] Links have descriptive text (not "click here")
- [ ] Form labels associated with inputs
- [ ] Error messages associated with fields
- [ ] Tested with screen reader (NVDA, JAWS, VoiceOver)
- [ ] Tested with keyboard only (no mouse)

---

## Cross-Browser Compatibility Checklist

For new frontend features.

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Chrome
- [ ] Mobile Safari
- [ ] No console errors
- [ ] Layout responsive (mobile, tablet, desktop)
- [ ] Performance acceptable on all browsers

---

## Deployment Checklist by Environment

### Local Development
- [ ] Service runs locally
- [ ] Tests pass
- [ ] Database migrates correctly
- [ ] Sample data loads

### Staging
- [ ] Service deploys successfully
- [ ] All tests pass in staging
- [ ] Smoke tests pass
- [ ] No errors in logs
- [ ] Monitoring working

### Production
- [ ] Deployment plan communicated
- [ ] Rollback plan tested
- [ ] Health checks passing
- [ ] No errors in logs
- [ ] Metrics within expected ranges
- [ ] On-call engineer monitoring
- [ ] Stakeholders notified

---

## Checklist Usage in Playbook Commands

| Checklist | Used By | Section |
|-----------|---------|---------|
| Self-Review | `/pb-cycle`, `/pb-templates` | Before peer review |
| Peer Review | `/pb-cycle`, `/pb-templates` | During review |
| Code Quality Gates | `/pb-cycle`, `/pb-guide` | Before commit |
| Pre-Release | `/pb-release`, `/pb-guide` | Before tag |
| Pre-Deployment | `/pb-release`, `/pb-guide` | Before deploy |
| Post-Deployment | `/pb-release`, `/pb-guide` | After deploy |
| Security | `/pb-cycle`, `/pb-security` | Before commit & release |
| Testing | `/pb-guide`, `/pb-review-tests` | During development |

---

## Tips for Effective Checklists

✅ **DO:**
- Use these as starting points, customize for your project
- Check items as you verify them
- Skip items that don't apply to your change
- Add project-specific items
- Review checklists periodically and update

❌ **DON'T:**
- Check items without actually verifying
- Use as a replacement for thinking
- Add so many items it becomes overwhelming
- Forget to actually fix issues found

---

*Created: 2026-01-11 | Last Updated: 2026-01-11 | Single source of truth for all playbook checklists*
