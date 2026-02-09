---
name: "pb-review-docs"
title: "Documentation Review"
category: "reviews"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-review', 'pb-review-hygiene', 'pb-documentation', 'pb-repo-readme', 'pb-repo-docsite']
tags: ['design', 'security', 'workflow', 'review', 'deployment']
last_reviewed: "2026-02-09"
last_evolved: ""
---
# Documentation Review

**Purpose:** Conduct a comprehensive review of project documentation for accuracy, completeness, and maintainability. Ensure docs remain human-readable and actionable.

**Recommended Frequency:** Monthly or before major releases

**Mindset:** Documentation review embodies `/pb-preamble` thinking (surface gaps, challenge assumptions) and `/pb-design-rules` thinking (especially Clarity: documentation should be obviously correct).

Find unclear sections, challenge stated assumptions, and surface gaps. Good documentation invites scrutiny and makes the system's reasoning transparent.

**Resource Hint:** opus — documentation review requires nuanced judgment across accuracy, clarity, completeness, and audience fit

---

## When to Use

- Before major releases (verify docs match new features)
- Monthly maintenance check
- After significant code changes
- When onboarding reveals confusion
- When support tickets indicate doc gaps

---

## Review Perspectives

Act as these roles simultaneously:

1. **Senior Engineer** — Technical accuracy, API correctness
2. **Product Manager** — User journey, feature coverage
3. **Technical Writer** — Clarity, structure, readability
4. **Security Reviewer** — Secrets exposure, compliance gaps
5. **New Engineer** — Onboarding experience, setup clarity

---

## Review Checklist

### 1. Quick Summary

For each document:
- One or two lines describing intended purpose and audience
- Does it serve that purpose? If not, mark for rewrite or removal

### 2. Accuracy Check

- [ ] Facts, architecture diagrams, API signatures are correct
- [ ] Environment variables and configuration are current
- [ ] Commands are copy-paste ready and validated
- [ ] Links are not broken
- [ ] Code examples match current codebase

### 3. Conciseness and Focus

- [ ] No repetitive, irrelevant, or verbose sections
- [ ] No unnecessary background or history
- [ ] Each section has clear purpose
- [ ] Examples are minimal but complete

### 4. Actionability

- [ ] Instructions are copy-paste ready
- [ ] All steps are explicit (no assumed knowledge)
- [ ] Missing context is identified and added
- [ ] Next steps are clear

### 5. Completeness

For critical areas, ensure docs include:

- [ ] **Quickstart** — Works for a new contributor
- [ ] **Architecture overview** — Responsibilities and data flows
- [ ] **API reference** — Matches current code
- [ ] **Runbooks** — Common failures and recovery steps
- [ ] **Security notes** — Secrets, scopes, approvals
- [ ] **Onboarding checklist** — For new engineers
- [ ] **Changelog** — Recent major changes

### 6. Ownership and Maintenance

- [ ] Owner/maintainer identified
- [ ] Last updated date is present and recent
- [ ] Review cadence is specified
- [ ] Stale docs are flagged

### 7. Links and References

- [ ] No broken links
- [ ] No outdated external references
- [ ] No docs that duplicate each other unnecessarily

### 8. Readability and Tone

- [ ] Plain human language
- [ ] Sensible headings and clear bullets
- [ ] Example usage provided
- [ ] Active, pragmatic wording (not passive/robotic)

---

## AI Content Detection

Flag sections matching these signals:

| Signal | Example | Action |
|--------|---------|--------|
| Repetitive phrasing | Same sentences across docs | Deduplicate or rewrite |
| Generic placeholders | `<thing>` used repeatedly | Add concrete values |
| Shallow polish | Confident but no actionable content | Rewrite with specifics |
| Incorrect specifics | Wrong dates, versions, configs | Verify and correct |
| Jargon without steps | Technical terms, no examples | Add concrete examples |
| Marketing tone | PR-speak in technical docs | Rewrite for engineers |

When flagging, suggest replacement text or mark for human rewrite.

---

## Deliverables

### 1. Executive Summary

3-5 bullets of overall documentation health and top priorities.

### 2. Per-Document Findings

For each doc reviewed:

```markdown
**File:** `README.md`
- **Purpose:** Quickstart + project overview
- **Audience:** New contributors
- **Issues:**
  - Outdated command on line 45
  - Verbose background section (lines 70-120)
- **Recommended fix:**
  - Update command to `docker compose up --build`
  - Move background to `docs/history.md`
- **Priority:** Short term
- **Owner:** @alice
- **Effort:** 1 hour
```

### 3. Prioritized Action List

| Priority | File | Issue | Fix | Owner | Effort |
|----------|------|-------|-----|-------|--------|
| Immediate | security.md | Missing auth flow | Add diagram | @bob | 2h |
| Short term | README.md | Stale commands | Update | @alice | 1h |
| Long term | api.md | Incomplete | Expand | TBD | 4h |
| Remove | old-setup.md | Obsolete | Delete | @alice | 15m |

### 4. AI Content Flagged

Sections likely AI-generated, with suggested rewrites.

### 5. Metrics to Track

- Number of docs changed
- Average doc length
- Number of broken links
- Coverage of quickstart/runbooks
- Number of flagged AI-like passages

---

## Sample Output

```markdown
## Executive Summary

- README is current but verbose in background section
- API docs are 3 months stale, missing new endpoints
- Runbooks exist but lack troubleshooting steps
- No broken links found
- 2 sections flagged as potentially AI-generated

## Per-Document Findings

### README.md
- Purpose: Quickstart + overview
- Issues: Lines 70-120 too verbose, command on line 45 outdated
- Fix: Update command, move background to separate doc
- Priority: Short term | Owner: @alice | Effort: 1 hour

### docs/api.md
- Purpose: API reference
- Issues: Missing /users/profile endpoint, wrong auth header
- Fix: Add endpoint, correct header example
- Priority: Immediate | Owner: @bob | Effort: 2 hours
```

---

## Related Commands

- `/pb-review` — Orchestrate comprehensive multi-perspective review
- `/pb-review-hygiene` — Code quality and operational readiness
- `/pb-documentation` — Documentation writing guidance
- `/pb-repo-readme` — Generate comprehensive README
- `/pb-repo-docsite` — Set up documentation site

---

**Last Updated:** 2026-01-21
**Version:** 2.0
