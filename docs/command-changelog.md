# Command Changelog

This document tracks version history for individual playbook commands. Commands are versioned independently from playbook releases to enable tracking command-specific evolution.

**Versioning Scheme:** Semantic versioning (MAJOR.MINOR.PATCH)
- MAJOR: Breaking changes, removed sections, changed purpose
- MINOR: New sections, new examples, enhanced guidance (non-breaking)
- PATCH: Typos, clarifications, reorganization (non-breaking)

---

## v1.1.0 (2026-02-09) — Phase 1-4 Enhancements

### New Commands (Phase 1: Persona Agents)

#### 5 Specialized Review Agents

- **pb-linus-agent** v1.1.0 — Direct technical feedback with pragmatic security lens
  - 584 lines, 18KB
  - Philosophy: Challenge assumptions, surface flaws, question trade-offs
  - Automatic rejection criteria: hardcoded secrets, SQL injection, XSS, command injection, buffer overflow, silent failures, race conditions

- **pb-alex-infra** v1.1.0 — Infrastructure resilience and failure mode analysis
  - 438 lines, 18KB
  - Philosophy: "Everything fails—excellence = recovery speed"
  - Categories: Failure modes, degradation, deployment, observability, capacity planning

- **pb-maya-product** v1.1.0 — Product strategy and user value focus
  - 1000+ lines, 15KB
  - Philosophy: "Features are expenses; value determined by users"
  - 6-step decision framework for feature evaluation

- **pb-sam-documentation** v1.1.0 — Documentation clarity and knowledge transfer
  - 1000+ lines, 21KB
  - Philosophy: "Documentation is first-class infrastructure"
  - Three-layer documentation approach (Conceptual, Procedural, Technical)

- **pb-jordan-testing** v1.1.0 — Testing coverage quality and reliability review
  - 1200+ lines, 22KB
  - Philosophy: "Tests reveal gaps, not correctness"
  - Categories: Test coverage, error handling, concurrency, data integrity, integration

### New Commands (Phase 2: Multi-Persona Review Workflows)

- **pb-review-backend** v1.1.0 — Backend review combining infrastructure + testing perspectives
  - 16KB, multi-perspective decision tree
  - Combines: Alex (Infrastructure) + Jordan (Testing)

- **pb-review-frontend** v1.1.0 — Frontend review combining product + documentation perspectives
  - 17KB, multi-perspective decision tree
  - Combines: Maya (Product) + Sam (Documentation)

- **pb-review-infrastructure** v1.1.0 — Infrastructure review combining resilience + security perspectives
  - 18KB, multi-perspective decision tree
  - Combines: Alex (Infrastructure) + Linus (Security)

### Enhanced Commands (Phase 3: Outcome-First Workflows)

- **pb-start** v1.1.0 — Added Outcome Clarification section
  - New: 5-step outcome definition process (define outcome, success criteria, approval path, blockers, Definition of Done)
  - New: Outcome documentation template (`todos/work/[task-date]-outcome.md`)
  - Impact: Prevents scope creep and "finished but doesn't solve the problem" problems

- **pb-cycle** v1.1.0 — Added Step 0: Outcome Verification before self-review
  - New: Step 0 verifies success criteria met before proceeding to self-review
  - Enhanced: Step 3 peer review now includes outcome verification
  - Impact: Validates problem is solved before reviewing code quality

- **pb-evolve** v1.1.0 — Added evolution success criteria validation
  - New: Three evolution types with specific success criteria
  - New: Pre-release checklist requiring success criteria verification
  - Impact: Makes evolution cycles accountable to measurable outcomes

### Enhanced Commands (Phase 4: Philosophy Expansion)

- **pb-design-rules** v1.1.0 — Added philosophy sections to 5 core design rules
  - Enhanced Rule 1 (Clarity): "Clarity is an act of respect for future readers"
    - Links to `/pb-sam-documentation`
  - Enhanced Rule 5 (Simplicity): "Scope discipline and feature-as-expense"
    - Links to `/pb-maya-product`
  - Enhanced Rule 9 (Robustness): "Transparency as defense against cascading failures"
    - Links to `/pb-alex-infra` and `/pb-jordan-testing`
  - Enhanced Rule 10 (Repair): "Fail loudly at the source, not silently downstream"
    - Links to `/pb-linus-agent`
  - Enhanced Rule 12 (Optimization): "Measure before optimizing, clarity before speed"
    - Links to `/pb-sam-documentation` and `/pb-alex-infra`
  - Impact: Design rules now explicitly teach multi-perspective thinking

---

## v1.0.0 (2025-12-XX) — Initial Baseline

All other 82 commands at version 1.0.0 represent the v2.10.0 playbook baseline.

**Total commands:** 82 baseline (v1.0.0) + 12 enhanced/new (v1.1.0) = 94 commands

---

## Breaking Changes Log

### v1.1.0 Breaking Changes

None. All v1.1.0 changes are additive and non-breaking.

- New commands don't affect existing commands
- Enhanced commands add sections without removing existing content
- Philosophy sections are supplementary

**Migration Path:** Existing users don't need to change anything. New features are opt-in:
- Use `/pb-start` with or without outcome clarification
- Use new persona review agents (`/pb-linus-agent`, etc.) alongside existing reviews
- Multi-persona reviews (`/pb-review-backend`, etc.) coexist with single-perspective reviews

---

## Deprecation Timeline

**Current:** No commands deprecated

**Planned for Future:** None currently planned, but potential future deprecations:
- Single-perspective review commands might eventually recommend multi-perspective alternatives
- Commands might consolidate if personas merge

**Deprecation Process:** When a command is deprecated:
1. Command gets version bump to MAJOR (e.g., 1.0.0 → 2.0.0)
2. `breaking_changes` field documents deprecation
3. Command references alternative (See `/pb-new-alternative` for updated approach)
4. Deprecation announced 1-2 releases before removal
5. Command removed 2-3 releases after deprecation announcement

---

## Future Versioning

As playbook evolves, commands will be updated and versioned:

### Minor Bumps (MINOR.x.0)
- New sections or enhanced guidance added
- Examples updated or expanded
- Cross-references added or updated
- Internal reorganization for clarity (same content)

### Patch Bumps (.x.PATCH)
- Typo fixes
- Clarifying rewrites
- Grammar improvements
- Date updates

### Major Bumps (MAJOR.0.0)
- Scope or purpose change
- Sections removed or significantly modified
- Replaces another command
- Architectural change

---

## Related Documentation

- **Versioning Strategy:** See [command-versioning.md](command-versioning.md) for detailed versioning guidelines
- **Command Index:** See [command-index.md](command-index.md) for full command list

---

*Last updated: 2026-02-09 (Phase 5)*
