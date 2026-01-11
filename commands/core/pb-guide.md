# **Engineering SDLC Playbook**

A reusable end-to-end guide for any feature, enhancement, refactor, or bug fix.
Right-size your process using **Change Tiers**, then follow required sections.

---

## **Quick Reference: Change Tiers**

Determine tier FIRST, then follow only required sections.

| Tier | Examples | Required Sections | Approvals |
|------|----------|-------------------|-----------|
| **XS** | Typo fix, config tweak, dependency bump | 1.1, 5.2, 8.1, 10.2 | Self |
| **S** | Bug fix, small UI change, single-file refactor | 1, 3, 5, 6.1, 8, 10 | Peer review |
| **M** | New endpoint, feature enhancement, multi-file change | 1-6, 7.1, 8, 10, 11 | Tech lead |
| **L** | New service, architectural change, breaking changes | All sections | Tech lead + Product |

**Default to one tier higher if uncertain.**

---

## **Definition of Ready (Before Starting)**

Before starting implementation, confirm:

- [ ] Tier determined and documented
- [ ] Scope documented (in-scope / out-of-scope)
- [ ] Acceptance criteria defined and agreed
- [ ] Dependencies identified and unblocked
- [ ] Security implications assessed (see Appendix A)

---

## **Definition of Done (Before Release)**

Before marking complete:

- [ ] All acceptance criteria met
- [ ] Tests passing (per tier requirements)
- [ ] Security checklist completed (Appendix A)
- [ ] Documentation updated (if applicable)
- [ ] Monitoring/alerting configured (M/L tiers)
- [ ] PR approved and merged
- [ ] Deployed and smoke tested

---

## **Checkpoints & Gates**

| Gate | After Section | Who Signs Off | Tier |
|------|---------------|---------------|------|
| **Scope Lock** | §3 | Product + Engineering | M, L |
| **Design Approval** | §4 | Tech Lead | M, L |
| **Ready for QA** | §5 | Developer (self-review) | S, M, L |
| **Ready for Release** | §6 | QA + Product | M, L |
| **Post-Release OK** | §10.3 | On-call / Developer | M, L |

Do not proceed past a gate without sign-off.

---

## **0. Emergency Path (Hotfixes Only)**

For P0/P1 production incidents requiring immediate fixes:

**Process:**
1. Fix the immediate problem (minimal change)
2. Get expedited review (sync, not async)
3. Deploy with rollback ready
4. Backfill documentation within 24 hours
5. Schedule post-incident review

**Required:** §1.1 (brief), §5.2, §8.2 (rollback), §10.2, §10.3

**Skip:** §2 (most), §4 (most), §9

**Post-hotfix:** Create follow-up ticket to address root cause properly.

---

## **1. Intake & Clarification**

Before starting any work:

**1.1 Restate the request**

Document:
* What is asked
* Why it matters (business value)
* Expected outcome
* Success criteria (measurable)
* Assumptions requiring validation
* **Tier assignment** (XS/S/M/L)

**1.2 Clarification checklist**

Ask for details on:
* Missing acceptance criteria
* Ambiguities in requirements
* Conflicting requirements
* Third-party constraints
* Dependencies on other teams or systems

**If anything is unclear, stop and clarify.**

---

## **2. Stakeholder Involvement & Alignment**

*Required for: M, L tiers*

Every significant change needs validation from multiple angles.

**2.1 Product**
* Confirm user story
* Confirm acceptance criteria
* Define measurable success metrics
* Check interactions with existing features
* Confirm visual/UI/UX expectations (if applicable)

**2.2 Engineering (Backend, Frontend, Infra)**
* Impact on architecture
* Data flow changes
* Service boundary / API changes
* Storage requirements
* Observability needs
* Performance expectations

**2.3 Business & Operations**
* Risk assessment
* Compliance (PII, audit, GDPR if applicable)
* Revenue or cost implications
* Customer impact and rollout timing

**Output:** Single aligned understanding documented before proceeding.

---

## **3. Requirements & Scope Definition**

*Required for: S, M, L tiers*

Create a clear boundary so the team knows what to deliver.

**3.1 In-scope**
Everything this change must include.

**3.2 Out-of-scope**
Anything explicitly excluded to avoid scope creep.

**3.3 Edge cases**
List special scenarios: failures, retries, degraded modes, empty states.

**3.4 Dependencies**
* API or service dependencies
* Schema updates
* External systems
* Libraries/packages
* Feature flag or config dependencies

**CHECKPOINT: Scope Lock (M/L tiers) - Get sign-off before proceeding.**

---

## **4. Architecture & Design Preparation**

*Required for: M, L tiers*

Provide a solid technical foundation.

**4.1 High-level architecture**
Include:
* Diagrams (flow, sequence, state as needed)
* Inputs, outputs, transformations
* Error pathways
* Retry/timeout/circuit breaker behavior

**4.2 Data Model Design**
* Schema updates
* Indexing strategy
* Backward compatibility
* Migration approach (online/offline, rollout steps)

**4.3 API/Interface Design**
* Request/response format
* Error codes and messages
* Pagination, filtering, sorting
* Idempotency requirements
* Compatibility with existing consumers

**4.4 Performance & Reliability**
* Expected load
* Stress points
* Concurrency handling
* Latency targets
* Resource usage (CPU, RAM, DB connections)

**4.5 Security Design**
Reference **Appendix A: Security Checklist** and document:
* How each applicable item is addressed
* Any security trade-offs or accepted risks

**CHECKPOINT: Design Approval (M/L tiers) - Get tech lead sign-off.**

---

## **5. Development Plan**

*Required for: S, M, L tiers*

Break work into implementable steps.

**5.1 Implementation roadmap**

For each component:
* Backend tasks
* Frontend tasks
* Infra tasks
* Data migration tasks
* Monitoring/logging tasks

**5.2 Coding practices**

Follow standards:
* Clean, readable structure
* Type safety
* Error handling with context
* Proper logging (no sensitive data)
* Retry & timeout patterns
* Minimize duplication
* Graceful degradation paths

**5.3 Developer checklist**

Before marking code complete:
- [ ] Handle success path
- [ ] Handle failure paths
- [ ] Handle malformed/unexpected inputs
- [ ] Handle concurrency and race conditions
- [ ] Add cleanup logic where needed
- [ ] Add idempotency where needed
- [ ] Confirm testability

**5.4 Iteration protocol**

During implementation, if scope or design changes are needed:
* **Minor adjustment:** Document in PR description, proceed
* **Significant change:** Return to §3 or §4, get re-approval before continuing

Don't silently expand scope.

**CHECKPOINT: Ready for QA - Self-review complete.**

---

## **6. Testing & Quality Assurance**

*Required for: S, M, L tiers (scope varies by tier)*

**6.1 Test Philosophy: Quality Over Quantity**

Tests should catch bugs, not just increase coverage numbers.

**DO Test:**
- Error handling and edge cases
- State transitions and side effects
- Business logic and calculations
- Integration points (API calls, storage)
- Security-sensitive paths (auth, validation)

**DON'T Test:**
- Static data structures (config, constants)
- Implementation details / internal functions
- Every permutation of valid inputs
- UI rendering details (prefer visual regression or E2E)
- Trivial getters/setters

**Anti-patterns to avoid:**
- Re-implementing internal functions in test files to test them
- Testing that data exists (instead of testing behavior)
- Over-parameterized tests for diminishing returns
- Slow integration tests that should be unit tests

**6.2 Test requirements by tier**

| Tier | Required Tests |
|------|----------------|
| **XS** | Existing tests pass |
| **S** | Unit tests for changed code + manual verification |
| **M** | Unit + Integration + QA scenarios |
| **L** | Unit + Integration + E2E + Load tests (if perf-critical) |

**6.3 Test types reference**

* **Unit tests** - Isolated function/method testing
* **Integration tests** - Component interaction testing
* **End-to-end tests** - Full user flow testing
* **API contract tests** - Request/response validation
* **Regression tests** - Ensure existing functionality unbroken
* **Negative tests** - Invalid inputs, error conditions
* **Load tests** - Performance under expected/peak load

**6.4 QA scenarios (M/L tiers)**

Document actual test cases covering:
* Happy path
* Alternate flows
* Error scenarios
* State transitions
* Data consistency checks
* Frontend usability (if applicable)

**6.5 Test data**

Create controlled, realistic test datasets. Never use production PII.

**6.6 Test maintenance**

Periodically review test suite for:
* Low-value tests to prune (static data tests, over-parameterized tests)
* Slow tests to speed up (missing mocks, over-integrated)
* Flaky tests to fix or quarantine
* Coverage gaps in critical paths

**Target:** Fewer, faster, more meaningful tests.

**CHECKPOINT: Ready for Release (M/L tiers) - QA sign-off.**

---

## **7. Infra, Deployment & Security Readiness**

*Required for: M, L tiers (7.1 always; 7.2-7.3 for L)*

**7.1 Infrastructure changes**
* New services or containers
* New environment variables
* New storage (DB, cache, files)
* New queues/topics
* Additional monitoring or logs

**7.2 Security hardening**

Reference **Appendix A** and confirm:
* All applicable items addressed
* No new attack surfaces introduced
* Secrets properly managed

**7.3 Observability**
* New dashboards needed?
* Alert rules defined?
* Log retention configured?
* SLO metrics identified?

---

## **8. CI/CD Requirements**

*Required for: All tiers*

**8.1 CI (All tiers)**
* Linting passes
* Type checks pass
* Automated tests pass
* Build succeeds

**8.2 CD (S, M, L tiers)**
* Deployment sequencing defined
* Feature flag plan (if applicable)
* **Rollback plan documented**
* Health checks in place
* Canary/phased rollout (L tier)

---

## **9. Documentation**

*Required for: M, L tiers*

**9.1 Developer documentation**
* Architecture notes
* Code flow explanation
* Important decisions and trade-offs

**9.2 API docs (if API changed)**
* Updated schemas
* Example requests/responses
* Error structures
* Versioning notes

**9.3 Operational docs (L tier)**
* Runbooks for common issues
* Monitoring instructions
* Scaling guidelines

**9.4 User/business documentation (if user-facing)**
* Release notes
* Customer-facing updates

---

## **10. Release & Post-Deployment**

*Required for: All tiers (scope varies)*

**10.1 Pre-release checklist (M/L tiers)**
- [ ] All tests passed
- [ ] All approvals obtained
- [ ] Monitoring/alerting configured
- [ ] Feature flags tested (if used)
- [ ] Rollback validated

**10.2 Release execution (All tiers)**
* Deploy
* Validate live metrics (M/L)
* Validate logs
* Smoke test

**10.3 Post-release monitoring (M/L tiers)**

Observe for at least 1 hour (L tier: 24 hours):
* Error rates
* Latency
* Resource usage
* DB load
* Logs for anomalies
* SLO adherence

**10.4 Follow-up work**
* Bugs discovered
* Optimizations identified
* Out-of-scope items to backlog
* Tech debt created

**CHECKPOINT: Post-Release OK - Confirm stable before moving on.**

---

## **11. Deliverable Summary Template**

*Required for: M, L tiers*

Copy and fill for each significant change:

```markdown
## Deliverable Summary: [Feature/Change Name]

**Tier:** [XS/S/M/L]
**Date:** [YYYY-MM-DD]
**Author:** [Name]

### What & Why
[One paragraph: what was built and the business value]

### How It Works
[Brief technical explanation of the approach]

### Key Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [e.g., Auth method] | [e.g., JWT] | [Why this choice] |

### Files Changed
[List key files or link to PR]

### Config Changes
- Environment variables: [List]
- Feature flags: [List or N/A]

### Migration
- Required: [Yes/No]
- Rollback steps: [Description]

### Testing Evidence
- Unit tests: [X added/modified]
- Integration tests: [X scenarios]
- Manual QA: [Link to test results or N/A]

### Monitoring
- Dashboard: [Link or N/A]
- Alerts: [List or N/A]

### Known Limitations
[What doesn't work yet or known issues]

### Follow-up Items
[Backlog tickets created for future work]
```

---

## **Appendix A: Security Checklist**

Reference this checklist from §4.5 and §7.2. Check all applicable items.

### Input & Data
- [ ] All user inputs validated and sanitized
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] File upload restrictions (type, size, content validation)
- [ ] No sensitive data in logs
- [ ] PII handling compliant with policy

### Authentication & Authorization
- [ ] Authentication required for protected endpoints
- [ ] Authorization checks at correct layer
- [ ] Session management secure (timeout, invalidation)
- [ ] Password/token handling follows best practices

### Secrets & Configuration
- [ ] No secrets in code or version control
- [ ] Secrets in secure storage (env vars, secrets manager)
- [ ] API keys scoped to minimum required permissions
- [ ] Secrets rotation plan exists

### Network & Infrastructure
- [ ] HTTPS enforced
- [ ] CORS configured correctly
- [ ] Rate limiting in place
- [ ] No unnecessary ports exposed
- [ ] Internal services not publicly accessible

### Error Handling
- [ ] Errors don't leak sensitive information
- [ ] Stack traces not exposed to users
- [ ] Audit logging for security events

### Dependencies
- [ ] No known vulnerabilities in dependencies
- [ ] Dependencies from trusted sources
- [ ] Lock files committed

---

## **Appendix B: Quick Checklist by Tier**

### XS Tier
- [ ] Change described (§1.1)
- [ ] Coding standards followed (§5.2)
- [ ] CI passes (§8.1)
- [ ] Deployed and verified (§10.2)

### S Tier
- [ ] Request restated (§1)
- [ ] Scope defined (§3)
- [ ] Implementation complete (§5)
- [ ] Unit tests added (§6.1)
- [ ] CI/CD passes (§8)
- [ ] Deployed and verified (§10)

### M Tier
- [ ] All S tier items
- [ ] Stakeholders aligned (§2)
- [ ] Design documented (§4)
- [ ] Integration tests added (§6.1)
- [ ] QA scenarios tested (§6.3)
- [ ] Infra changes documented (§7.1)
- [ ] Documentation updated (§9)
- [ ] Deliverable summary complete (§11)
- [ ] Post-release monitoring done (§10.3)

### L Tier
- [ ] All M tier items
- [ ] All checkpoints passed with sign-off
- [ ] Security checklist complete (Appendix A)
- [ ] Load testing done (if applicable)
- [ ] Operational docs created (§9.3)
- [ ] 24-hour post-release monitoring

---

## **Appendix C: Operational Practices**

### Deployment

- **Use standardized deploy command** (e.g., `make deploy`) - Single command that handles git push, server pull, secrets decryption, and container rebuild.
- **Root access** - Only use root/SSH when deploy command cannot perform a specific action (e.g., debugging container issues, manual restarts).
- **Verify after deploy** - Always check service health after deployment via dashboard or container status.

### Secrets Management

- **Use standardized secrets command** (e.g., `make secrets-add`) - Add production secrets to encrypted secrets file.
- **Keep secrets in sync** - Always maintain consistency across:
  - `.env` (local development)
  - `.env.example` (template with placeholder values)
  - Encrypted secrets file for production
- **Never commit plaintext secrets** - All production secrets must be encrypted.

### Git Commit Practices

- **Never use `git add .`** - Considered risky; can accidentally stage unintended files.
- **Make logical commits** - Add specific files that belong together logically.
- **Use descriptive commit messages** - Follow conventional commits format (feat, fix, chore, etc.).
- **Review staged changes** - Always run `git status` and `git diff --staged` before committing.

### Configuration & Templating

- **Provisioning files** - YAML/config provisioning files may not support environment variable interpolation. Use deploy-time substitution with `sed` for dynamic values.
- **Personal/sensitive info** - Never hardcode personal email addresses or identifiable info in repo files. Use environment variables with deploy-time substitution.

### Monitoring & Observability

- **Background workers** - Workers without HTTP endpoints cannot be scraped directly. Monitor via queue/job metrics from the message broker.
- **Prometheus targets** - Only add services that expose `/metrics` endpoints.
- **Dashboard panels** - Ensure metrics exist before adding panels; missing metrics show as "No data".

### Frontend Compatibility

- **Check browser support** - Newer language features may not work in older browsers.
- **Use polyfills or alternatives** - When using cutting-edge features, verify browser compatibility or use libraries with broader support.
- **Test in multiple browsers** - Especially for user-facing features.

### Accessibility (WCAG 2.1 AA)

- **Keyboard navigation** - All interactive elements must be keyboard accessible. Every `onClick` needs a keyboard equivalent (`onKeyDown` for Enter/Space).
- **Focus management** - Modals/drawers must trap focus and restore it on close.
- **ARIA labels** - Icon-only buttons require `aria-label`. Hide decorative icons with `aria-hidden="true"`.
- **Focus visibility** - Focus indicators must be visible in both light and dark modes.
- **Semantic HTML** - Use appropriate elements (`button` not `div` with onClick).
- **Touch targets** - Minimum 44x44px for mobile touch targets.

### Troubleshooting

- **Container crash loops** - Check container logs to identify startup failures.
- **Provisioning errors** - Often caused by invalid YAML syntax or missing required fields. Check for proper indentation and required settings.
- **Environment variable issues** - Shell sourcing may fail with special characters. Use `grep` + `cut` instead of `source` for robust extraction.
