---
name: "pb-review-product"
title: "Technical + Product Review"
category: "reviews"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-review', 'pb-review-code', 'pb-review-hygiene', 'pb-plan', 'pb-adr']
last_reviewed: "2026-02-09"
last_evolved: ""
version: "1.0.0"
version_notes: "v2.10.0 baseline"
breaking_changes: []
---
# Technical + Product Review

**Purpose:** Periodic, in-depth review from four expert perspectives: Senior Engineer, Technical Architect, Security Expert, and Product Manager.

**Recommended Frequency:** Quarterly or before major product decisions

**Mindset:** Multi-perspective review embodies `/pb-preamble` thinking (each perspective challenges the others) and `/pb-design-rules` thinking (design decisions should honor Clarity, Simplicity, and user needs).

Surface disagreements—they often surface real problems that single views miss.

**Resource Hint:** opus — multi-perspective review spanning engineering, architecture, security, and product strategy

---

## When to Use

- Quarterly strategic alignment check
- Before major product decisions or pivots
- After significant feature launches
- When engineering and product seem misaligned
- Before annual planning

---

## Context

You are seasoned, pragmatic experts in your field. You value simplicity, maintainability, and genuine user value over theoretical perfection or trendy complexity. Provide critical, constructive feedback grounded in real-world experience.

Write in a natural, conversational yet professional tone — not stilted AI-generated language.

---

## Review Perspectives

### 1. Senior Engineer (Code Health & Maintainability)

**Readability & Clarity:**
- Does the code tell a clear story?
- Can a new engineer understand flow and intent without excessive comments?
- Point to specific files or modules that are exemplary or problematic.

**Simplicity & Over-engineering:**
- Where have we made things more complex than necessary?
- Look for convoluted abstractions, dogmatic design patterns, or "clever" code that sacrifices readability.

**Technical Debt & Bottlenecks:**
- Identify areas of accumulating technical debt.
- Are there slow tests, flaky integrations, or modules that are difficult to change?
- Be specific about potential consequences.

**Testing Strategy:**
- Is the test suite effective and practical?
- Good balance of unit, integration, and end-to-end tests?
- Are tests focused on behavior rather than implementation?

### 2. Technical Architect (System Design & Evolution)

**Architectural Integrity:**
- Is the system's design adhering to its intended principles?
- Have recent features introduced coupling or violated separation of concerns?

**Scalability & Efficiency:**
- How does the architecture handle scale?
- Are there components that would become bottlenecks under load?
- Consider data flow, API design, and database interactions.

**Dependency & Bloat Audit:**
- Are we using dependencies effectively?
- Are there libraries we've outgrown or that are overly heavy for our use case?
- Are we at risk of dependency hell?

**Future-Proofing:**
- How easy would it be to extend the system with a new significant feature?
- Are the right extension points in place?

### 3. Security Expert (Security & Compliance)

**Practical Security Review:**
- How is security actually implemented?
- Are secrets managed properly?
- Is authentication/authorization logic consistent and robust?
- Are we logging security-relevant events effectively?

**Dependency Vulnerabilities:**
- State of dependency vulnerability management?
- Are we responsive to patches?

**Data Handling & Privacy:**
- Is sensitive data handled appropriately?
- Are we following least privilege and data minimization principles?

**Anti-Patterns:**
- Custom crypto?
- Exposed internal errors?
- Misconfigured security headers?

### 4. Product Manager (Product Fit & Value)

**Feature Efficacy & Usage:**
- Are features delivering expected user value?
- Based on what evidence (metrics, feedback)?
- Are there features that are underused or could be simplified/removed?

**Avoiding Bloat:**
- Where are we adding complexity without commensurate value?
- Are we building for edge cases at the cost of common cases?

**Cohesion & User Journey:**
- Does the product feel like a cohesive whole?
- Is the user experience consistent?

**Pragmatism vs. Perfection:**
- Did we over-invest in perfecting a feature that only needed "good enough"?
- Did we under-invest in a critical user-facing area?

---

## Cross-Cutting Concerns

Be a guardian against **bloat and synthetic code artifacts**:

- **Unnecessary Abstraction:** Code abstracted too early or for a single use case.
- **Overly Descriptive Naming:** Variable names so verbose they harm readability.
- **Inconsistent Code Style:** Sections that feel alien, suggesting copy-paste without integration.
- **Solution in Search of a Problem:** Components that are architecturally "interesting" but solve trivial or non-existent problems.

---

## Goals

- Keep codebase **lean, human-readable, maintainable**
- Eliminate **bloat, redundancy, over-abstraction**
- Encourage **clarity, simplicity, real-world usefulness**
- Maintain **human tone** in naming, docs, and communication

---

## Deliverables

### 1. Summary of Key Findings
Per-role summary of most important observations.

### 2. Actionable Recommendations
Specific, prioritized as:
- **High:** Must address soon
- **Medium:** Should address when convenient
- **Low:** Nice to have

### 3. Next Steps
What should be done before the next review cycle.

### 4. Risk Assessment (Optional)
Trade-offs, effort estimates, or risks of inaction.

---

## Output Format

```markdown
## Review Summary

### Senior Engineer
[Key findings in 2-3 paragraphs]

### Technical Architect
[Key findings in 2-3 paragraphs]

### Security Expert
[Key findings in 2-3 paragraphs]

### Product Manager
[Key findings in 2-3 paragraphs]

---

## Recommendations

| Priority | Area | Recommendation | Rationale |
|----------|------|----------------|-----------|
| High | [Area] | [Specific action] | [Why] |
| Medium | [Area] | [Specific action] | [Why] |

---

## Next Steps

1. [Immediate action]
2. [Follow-up action]
3. [Longer-term consideration]
```

---

## Related Commands

- `/pb-review` — Orchestrate comprehensive multi-perspective review
- `/pb-review-code` — Code change review for PRs
- `/pb-review-hygiene` — Code quality and operational readiness
- `/pb-plan` — Feature and release planning
- `/pb-adr` — Architecture decision records

---

**Last Updated:** 2026-01-21
**Version:** 2.0
