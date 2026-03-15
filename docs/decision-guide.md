# Decision Guide: Which Command Should I Use?

This guide helps you find the right command for any situation. Answer the questions to get directed to the command you need.

---

## Quick Command Finder

### I'm starting new work...

**Starting a new project?**
→ Use `/pb-plan` to lock scope, then `/pb-repo-init` to set up structure

**Starting a feature or bug fix?**
→ Use `/pb-start` to create a branch and establish iteration rhythm

**Resuming after a break?**
→ Use `/pb-resume` to get back in context

**Looking at code that needs review?**
→ Go to [Code Review Questions](#im-reviewing-code)

---

### I'm in the middle of development...

**Need to understand current patterns and architecture?**
→ Use `/pb-context` to document and reference project context

**Want to reference design patterns for what you're building?**
→ Use `/pb-patterns` for overview, then:
- `/pb-patterns-core` for architectural patterns (SOA, events, repository, DTO)
- `/pb-patterns-resilience` for resilience patterns (retry, circuit breaker, rate limiting)
- `/pb-patterns-async` for async/concurrency patterns
- `/pb-patterns-db` for database patterns
- `/pb-patterns-distributed` for distributed system patterns

**Ready to review your code before committing?**
→ Use `/pb-cycle` for self-review and peer review

**Ready to commit your changes?**
→ Use `/pb-commit` to create atomic, well-formatted commits

**Ready to create a pull request?**
→ Use `/pb-pr` for streamlined PR creation

**Need help with writing tests?**
→ Use `/pb-testing` for testing philosophy and patterns

---

### I'm reviewing code...

**Reviewing a PR and need a structured approach?**
→ Use `/pb-cycle` (peer review perspective) for architecture and correctness

**Need to check security?**
→ Use `/pb-security` for security checklist (quick, standard, or deep)

**Need to check logging standards?**
→ Use `/pb-logging` for structured logging validation

**Need to check test coverage and quality?**
→ Use `/pb-review-tests` for test suite quality review

**Is this user-facing code or product change?**
→ Use `/pb-review-product` for product alignment review

**Doing a comprehensive code review?**
→ Use `/pb-review-hygiene` for code quality and maintainability

**Is this a microservice change?**
→ Use `/pb-review-microservice` for service design and contract review

---

### I'm preparing for release...

**Ready to release to production?**
→ Use `/pb-release` for pre-release checks and deployment readiness

**Need to plan deployment strategy?**
→ Use `/pb-deployment` to choose strategy (blue-green, canary, rolling)

**Doing final code review before release?**
→ Use `/pb-release` for senior engineer final review

**Is this a major release?**
→ Use `/pb-review` for comprehensive multi-perspective audit

---

### I'm dealing with production issues...

**Production is down or degraded?**
→ Use `/pb-incident` for rapid assessment and mitigation

**Need to monitor system behavior?**
→ Use `/pb-observability` for monitoring, logging, tracing setup

**After incident is resolved, need to analyze?**
→ Use `/pb-incident` again for comprehensive post-mortem analysis

---

### I'm doing architecture or planning work...

**Planning a major feature or release?**
→ Use `/pb-plan` to lock scope and define success criteria

**Documenting an architectural decision?**
→ Use `/pb-adr` for Architecture Decision Records

**Need performance guidance?**
→ Use `/pb-performance` for optimization and profiling

---

### I'm working on team or organizational things...

**Onboarding a new team member?**
→ Use `/pb-onboarding` for structured onboarding process

**Doing a knowledge transfer session?**
→ Use `/pb-knowledge-transfer` for KT preparation

**Want to do team retrospective or feedback?**
→ Use `/pb-team` for team dynamics and growth

**Writing daily standup for distributed team?**
→ Use `/pb-standup` for async standup template

---

### I'm working on repository or documentation...

**Setting up a new project?**
→ Use `/pb-repo-init` to initialize structure

**Need to organize/clean up project directory?**
→ Use `/pb-repo-organize` for repository cleanup

**Writing or rewriting README?**
→ Use `/pb-repo-readme` for compelling README guidance

**Creating GitHub About section?**
→ Use `/pb-repo-about` for GitHub presentation

**Writing a technical blog post?**
→ Use `/pb-repo-blog` for blog post guidance

**Want to do all repository improvements at once?**
→ Use `/pb-repo-enhance` for full suite

---

### I'm setting standards or frameworks...

**Need to understand the SDLC framework?**
→ Use `/pb-guide` for full 11-phase SDLC with quality gates

**Setting team standards and principles?**
→ Use `/pb-standards` for coding standards and collaboration norms

**Need templates for commits, PRs, or reviews?**
→ Use `/pb-templates` for reusable templates

**Need to document how this project works?**
→ Use `/pb-context` for project context template

**Need to write technical documentation?**
→ Use `/pb-documentation` for technical writing guidance

---

## Scenario-Based Flowchart

```
START
│
├─ "I'm starting something new"
│  ├─ "Entire project?" → /pb-plan → /pb-repo-init
│  ├─ "Feature/bug?" → /pb-start
│  └─ "Resuming?" → /pb-resume
│
├─ "I'm developing"
│  ├─ "Need patterns?" → /pb-patterns-*
│  ├─ "Ready to review?" → /pb-cycle
│  ├─ "Ready to commit?" → /pb-commit
│  ├─ "Ready to PR?" → /pb-pr
│  └─ "Need tests?" → /pb-testing
│
├─ "I'm reviewing code"
│  ├─ "Architecture?" → /pb-cycle
│  ├─ "Security?" → /pb-security
│  ├─ "Tests?" → /pb-review-tests
│  ├─ "Product fit?" → /pb-review-product
│  ├─ "Logging?" → /pb-logging
│  └─ "Full review?" → /pb-review-hygiene
│
├─ "I'm releasing"
│  ├─ "Pre-release?" → /pb-release
│  ├─ "How to deploy?" → /pb-deployment
│  └─ "Final check?" → /pb-release
│
├─ "Production issue"
│  ├─ "Incident?" → /pb-incident
│  └─ "Monitoring?" → /pb-observability
│
├─ "Architecture/Planning"
│  ├─ "Lock scope?" → /pb-plan
│  ├─ "Document decision?" → /pb-adr
│  └─ "Optimize?" → /pb-performance
│
├─ "Team/Org"
│  ├─ "Onboarding?" → /pb-onboarding
│  ├─ "Knowledge transfer?" → /pb-knowledge-transfer
│  ├─ "Team health?" → /pb-team
│  └─ "Daily standup?" → /pb-standup
│
└─ "Repository/Docs"
   ├─ "New project?" → /pb-repo-init
   ├─ "Organize?" → /pb-repo-organize
   ├─ "README?" → /pb-repo-readme
   ├─ "GitHub about?" → /pb-repo-about
   ├─ "Blog post?" → /pb-repo-blog
   └─ "Full polish?" → /pb-repo-enhance
```

---

## By Frequency

### Daily
- `/pb-resume` - Get context
- `/pb-cycle` - Code and review
- `/pb-standup` - Team standup
- `/pb-commit` - Create commits
- `/pb-context` - Refresh project knowledge

### Per Feature
- `/pb-plan` - Lock scope
- `/pb-start` - Create branch
- `/pb-testing` - Add tests
- `/pb-security` - Security gate
- `/pb-pr` - Create pull request
- `/pb-commit` - Logical commits

### Per Release
- `/pb-release` - Pre-release checks
- `/pb-deployment` - Choose strategy
- `/pb-release` - Final review

### Monthly
- `/pb-review-hygiene` - Code quality
- `/pb-review-tests` - Test coverage
- `/pb-logging` - Logging standards

### Quarterly
- `/pb-review-hygiene` - Tech debt
- `/pb-review-product` - Product fit
- Team retrospective

### Occasionally
- `/pb-adr` - Major decisions
- `/pb-patterns-*` - Design decisions
- `/pb-performance` - Optimization
- `/pb-incident` - Production issues
- `/pb-observability` - Monitoring setup
- `/pb-onboarding` - New team members
- `/pb-knowledge-transfer` - Knowledge transfer
- `/pb-team` - Team dynamics

### One-Time
- `/pb-repo-init` - New project
- `/pb-repo-organize` - Cleanup
- `/pb-repo-readme` - Write README
- `/pb-repo-about` - GitHub about
- `/pb-repo-blog` - Tech blog post
- `/pb-guide` - Learn framework
- `/pb-standards` - Define standards
- `/pb-templates` - Create templates
- `/pb-context` - Document project

---

## By Role

### Individual Contributor
- Daily: `/pb-resume`, `/pb-cycle`, `/pb-standup`, `/pb-commit`
- Per feature: `/pb-plan`, `/pb-start`, `/pb-testing`, `/pb-security`, `/pb-pr`
- As needed: `/pb-patterns-*`, `/pb-context`

### Code Reviewer / Senior Engineer
- Per PR: `/pb-cycle`, `/pb-security`, `/pb-review-tests`, `/pb-review-hygiene`, `/pb-logging`
- Per release: `/pb-release`
- Periodically: `/pb-review-product`, `/pb-review-hygiene`

### Tech Lead / Architect
- Per feature: `/pb-plan`, `/pb-adr`, `/pb-patterns-*`
- Per release: `/pb-release`, `/pb-deployment`, `/pb-release`
- Periodically: `/pb-review`, `/pb-performance`, `/pb-observability`

### Engineering Manager
- Onboarding: `/pb-onboarding`, `/pb-knowledge-transfer`
- Team: `/pb-team`, `/pb-standup`, team retrospectives
- Strategy: `/pb-context`, `/pb-plan`, `/pb-adr`

### DevOps / Infrastructure
- Deployment: `/pb-deployment`, `/pb-release`
- Operations: `/pb-incident`, `/pb-observability`, `/pb-performance`
- Setup: `/pb-repo-organize`, `/pb-standards`

### Product Manager
- Planning: `/pb-plan`, `/pb-context`
- Reviews: `/pb-review-product`
- Documentation: `/pb-documentation`

---

## Next Steps

- **[Full Command Reference](command-index.md)** - See all commands
- **[Getting Started](getting-started.md)** - Pick a scenario
- **[Integration Guide](integration-guide.md)** - See how commands work together
- **[FAQ](faq.md)** - Common questions
