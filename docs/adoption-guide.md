# Playbook Adoption Guide

Integrating the engineering playbook into your team's workflow. This guide shows how to adopt across different team sizes and contexts.

---

## Quick Start by Team Size

### **Startup (2-5 engineers)**
- **Week 1**: Read `/pb-guide` (understand 11 phases) + `/pb-preamble` (collaboration style)
- **Week 2**: Start using `/pb-start` → `/pb-cycle` → `/pb-commit` → `/pb-pr` for feature work
- **Week 3**: Add `/pb-review-cleanup` for peer review, `/pb-standards` for decision-making
- **Payoff**: Clear development rhythm, better code review, shared decision language
- **Effort**: 2-3 hours per engineer for onboarding

### **Small Team (6-12 engineers)**
- **Phase 1 (Week 1-2)**:
  - Run workshop: `/pb-guide` (SDLC overview) + `/pb-preamble` (team collaboration)
  - Establish team norms from `/pb-standards`
  - Pick 3-4 core commands: `/pb-start`, `/pb-cycle`, `/pb-commit`, `/pb-pr`
- **Phase 2 (Week 3-4)**:
  - Add `/pb-plan` for feature planning
  - Add `/pb-review-cleanup` + `/pb-security` for code review gates
  - Document team decisions in `/pb-context`
- **Payoff**: Structured planning, consistent code quality, documented decisions
- **Effort**: 4-6 hours per engineer over 4 weeks

### **Medium Team (13-30 engineers)**
- **Phase 1 (Week 1-2)**:
  - Lead architect reads entire playbook
  - Creates team guide: custom command selection + team-specific examples
  - Runs workshops for different roles (frontend, backend, infra, QA)
- **Phase 2 (Week 3-4)**:
  - Rollout core workflow: `/pb-plan` → `/pb-adr` → `/pb-cycle` → `/pb-review-*` → `/pb-release`
  - Establish review ceremony using `/pb-review-cleanup`, `/pb-review-tests`
  - Create project `/pb-context` document for current work
- **Phase 3 (Week 5-8)**:
  - Integrate `/pb-patterns-*` into architecture discussions
  - Establish release process using `/pb-release` + `/pb-deployment`
  - Monitor adoption via `/pb-review` (periodic) and `/pb-standards` (decisions)
- **Payoff**: Scaled decision-making, architecture consistency, knowledge sharing
- **Effort**: 6-8 hours initial per engineer, 1-2 hours/week ongoing

### **Large Team (30+ engineers) or Multiple Teams**
- **Phase 1**:
  - Platform/core team leads customize playbook
  - Create role-specific subsets (frontend guide, backend guide, SRE guide)
  - Run quarterly strategy sessions using `/pb-preamble` and `/pb-design-rules`
- **Phase 2**:
  - Rollout 8-week adoption program with checkpoints
  - Pair experienced + new engineers on `/pb-cycle` and `/pb-todo-implement`
  - Establish command adoption metrics (% using core workflow)
- **Payoff**: Org-wide consistency, reduced onboarding time, better incident response
- **Effort**: Ongoing, integrate into new engineer onboarding

---

## 4-Phase Adoption Pathway

### **Phase 1: Foundation (Weeks 1-2)**

**Goal**: Team understands philosophy and core workflow

**Activities**:
- [ ] Team reads `/pb-guide` (1-2 hours) and `/pb-preamble` (30 min)
- [ ] Lead architect reads `/pb-design-rules` and creates team-specific reference
- [ ] Establish working group: core decision-makers + IC representatives
- [ ] Define team's tier system (XS/S/M/L) for task sizing

**Success Signals**:
- 80%+ team members attended workshop
- Shared understanding of 11 SDLC phases
- Written team norms (from `/pb-standards`)

---

### **Phase 2: Development Workflow (Weeks 3-4)**

**Goal**: Daily development process uses playbook

**Activities**:
- [ ] Integrate `/pb-start` → `/pb-cycle` → `/pb-commit` → `/pb-pr` into real features
- [ ] Use `/pb-testing` alongside `/pb-cycle` for test-driven development
- [ ] Establish review process: `/pb-review-cleanup` for every PR
- [ ] Create project `/pb-context` document for current decisions
- [ ] Track metrics: % of features using playbook workflow

**Success Signals**:
- 50%+ of PRs reference playbook commands in PR description
- Code review feedback uses `/pb-review-cleanup` language
- Commit messages follow `/pb-templates` format

---

### **Phase 3: Planning & Architecture (Weeks 5-8)**

**Goal**: Major decisions documented using playbook frameworks

**Activities**:
- [ ] Next feature uses `/pb-plan` + `/pb-adr` workflow
- [ ] Architecture decisions reference applicable `/pb-design-rules`
- [ ] Team uses `/pb-patterns-*` for system design
- [ ] Add `/pb-observability` and `/pb-performance` to planning
- [ ] Establish `/pb-review` (monthly) and `/pb-review-tests` (monthly) cadence

**Success Signals**:
- All major features have `/pb-adr` documents
- Design discussions explicitly reference design rules
- Monthly review ceremonies happening

---

### **Phase 4: Release & Operations (Weeks 9+)**

**Goal**: Production safety and incident response follow playbook

**Activities**:
- [ ] Implement `/pb-release` checklist before every release
- [ ] Use `/pb-deployment` for deployment strategy selection
- [ ] Establish incident response using `/pb-incident`
- [ ] Connect observability to `/pb-observability` strategy
- [ ] Run quarterly `/pb-team` retrospectives

**Success Signals**:
- 100% of releases use `/pb-release` checklist
- Incident response time reduced
- Team retention improved (per `/pb-team` feedback)

---

## Adoption by Context

### **By Codebase Maturity**

| Stage | Focus | Key Commands |
|-------|-------|--------------|
| **Greenfield** | Structure first | `/pb-repo-init`, `/pb-plan`, `/pb-adr`, `/pb-patterns-*` |
| **Growth** | Quality gates | `/pb-cycle`, `/pb-review-*`, `/pb-testing`, `/pb-standards` |
| **Maintenance** | Consistency | `/pb-review-hygiene`, `/pb-deprecation`, `/pb-context` |
| **Scaling** | Governance | `/pb-plan`, `/pb-adr`, `/pb-design-rules`, `/pb-review` |

### **By Team Distribution**

| Distribution | Approach | Key Commands |
|--------------|----------|--------------|
| **Co-located** | In-person workshops, real-time decision-making | `/pb-preamble`, `/pb-cycle`, `/pb-team` |
| **Distributed** | Async decision framework, written decisions | `/pb-preamble-async`, `/pb-adr`, `/pb-context` |
| **Mixed** | Hybrid: in-person planning, async execution | `/pb-plan`, `/pb-preamble-decisions`, `/pb-standup` |

### **By Risk Profile**

| Risk Level | Approach | Governance |
|------------|----------|-----------|
| **Low-risk** | Move fast, minimal gates | XS/S tier commands only |
| **Medium-risk** | Balanced approach | S/M tier with `/pb-review-cleanup` |
| **High-risk** | Multiple gates, documentation | M/L tier with `/pb-adr`, `/pb-security` |
| **Mission-critical** | All gates, design review | M/L with `/pb-release`, `/pb-incident` |

---

## Measuring Success

### **Adoption Metrics** (Track weekly)
- % of engineers actively using core commands
- % of features following `/pb-start` → `/pb-cycle` → `/pb-pr` workflow
- % of PRs using `/pb-review-cleanup` perspective
- % of major decisions documented in `/pb-adr`

### **Quality Metrics** (Track monthly)
- Code review feedback quality (using design rules language)
- Test coverage maintenance
- Security issue density (post `/pb-security` adoption)
- Deployment success rate (post `/pb-release` + `/pb-deployment` adoption)

### **Team Metrics** (Track quarterly)
- Time to onboard new engineer (-30% after 3 months)
- Team satisfaction with decision-making (+20% per `/pb-team` surveys)
- Incident response time (-25% average)
- Knowledge retention across team transitions

---

## Common Pitfalls & Solutions

| Pitfall | Symptom | Solution |
|---------|---------|----------|
| **Adoption fatigue** | Teams use 1-2 commands, ignore rest | Start small: focus 3-4 core commands for 4 weeks, then expand incrementally |
| **Misaligned tier system** | Features skip `/pb-plan` because "it's just code" | Define team's tier system explicitly; make `/pb-plan` requirement for M/L features |
| **Design rules as dogma** | Team debates "which rule applies" instead of deciding | Emphasize decision framework: rules guide, don't dictate; preamble thinking resolves conflicts |
| **No shared context** | Engineers make decisions in isolation | Enforce `/pb-context` updates during `/pb-start`; review monthly |
| **Review ceremonies die** | Established `/pb-review` and `/pb-review-tests` → skip after month 2 | Calendar invites, rotate facilitators, document findings in `/pb-context` |
| **Preamble not internalized** | Good intentions but team reverts to hierarchical decision-making | Schedule bi-weekly preamble discussion (30 min); connect to real decisions |
| **Too much documentation** | Engineers write ADRs for tiny changes | Only require `/pb-adr` for M/L features; use decision framework to know when |

---

## Implementation Checklist

### **Before Launch**
- [ ] Leadership team reads `/pb-guide` and `/pb-preamble`
- [ ] Select initial command set (recommend: 5-7 commands to start)
- [ ] Customize examples for your tech stack
- [ ] Identify 2-3 "playbook champions" to drive adoption
- [ ] Schedule workshops

### **Week 1-2: Kickoff**
- [ ] Run 60-min workshop: `/pb-guide` overview + `/pb-preamble`
- [ ] Create team guide document
- [ ] Establish `/pb-context` for current project
- [ ] Share adoption timeline

### **Week 3-8: Rollout**
- [ ] Weekly 30-min "command spotlight" sessions
- [ ] Include playbook reference in PR templates
- [ ] Track adoption metrics
- [ ] Address questions/concerns in Slack #playbook channel

### **Month 3+: Iterate**
- [ ] Run `/pb-team` retrospective on adoption
- [ ] Refine command set based on feedback
- [ ] Expand to advanced commands
- [ ] Document team-specific customizations

---

## FAQ

**Q: Do we need to use ALL commands?**
A: No. Start with 5-7 core commands; expand based on team needs.

**Q: How long does adoption take?**
A: 4-8 weeks to establish core workflow; 12 weeks to full integration.

**Q: What if we're already using different processes?**
A: Use playbook commands that fill gaps or improve existing process. Merge gradually.

**Q: Should we customize the playbook?**
A: Yes. Keep philosophy intact; customize examples, tools, and process for your team.

**Q: How do we handle team pushback?**
A: Connect to pain points: "ADRs solve our knowledge loss problem" or "Design rules help us debate architecture better."

---

**Start with Phase 1 this week. Pick 4 core commands. Add one workshop. Measure adoption in 30 days.**
