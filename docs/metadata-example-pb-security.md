---
name: pb-security
title: "Security Review & Checklist"
category: planning
difficulty: advanced
model_hint: opus
execution_pattern: reference
related_commands: [pb-hardening, pb-patterns-security, pb-review-code]
tags: [security, compliance, review]
last_reviewed: "2026-02-05"
last_evolved: ""
summary: "Comprehensive security checklist and threat modeling framework"
prerequisites: [pb-preamble, pb-design-rules]
execution_time_estimate: "5 minutes to 2 hours (depends on checklist tier)"
frequency: monthly
constraints:
  - "Requires understanding of OWASP Top 10"
  - "For security-critical systems"
  - "Opus recommended for deep dives"
---

# Security Review & Checklist

Comprehensive security guidance for code review, design assessment, and pre-release validation. Use the checklist appropriate to your context: quick review, standard audit, or deep dive.

**Mindset:** Security review embodies `/pb-preamble` thinking (find what was missed, challenge safety assumptions) and `/pb-design-rules` thinking (especially Robustness and Transparency: systems should fail safely and be observable).

Your job is to surface risks and vulnerabilities. Reviewers should ask hard questions. Authors should welcome this scrutiny.

**Resource Hint:** opus — security review demands thorough analysis of attack surfaces, threat models, and vulnerability patterns

---

## When to Use This Command

- **Code review** — Checking PRs for security issues
- **Pre-release** — Security validation before shipping
- **Security audit** — Periodic comprehensive review
- **New authentication/authorization** — Changes to access control
- **Handling sensitive data** — PII, payments, credentials

[Rest of command content...]
