---
name: "pb-review-patterns"
title: "Review Skill Design Patterns (for skill authors)"
category: "reviews"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "reference"
related_commands: ['pb-review', 'pb-review-code', 'pb-new-playbook', 'pb-evolve']
last_reviewed: "2026-04-23"
last_evolved: "2026-04-23"
version: "1.0.0"
version_notes: "v2.21.0: New reference doc. First pattern: scope-locked passes. Grows as more review-skill patterns earn inclusion."
breaking_changes: []
---
# Review Skill Design Patterns

Reference for **skill authors** who design or extend review commands. Not for end-users running reviews -- those use `/pb-review`, `/pb-review-code`, etc.

**Audience:** contributors adding new `/pb-review-*` skills, extending existing ones, or building review-adjacent automation.

**Resource Hint:** opus - meta-level reasoning about skill design.

---

## When to Use

- **Designing a new `/pb-review-*` skill** - verify the chosen structure matches documented patterns.
- **Extending an existing review skill** - check that the extension preserves scope discipline.
- **Reviewing a PR that adds review-adjacent automation** - consistency check across the review family.

End-users running reviews should use `/pb-review`, `/pb-review-code`, or one of the focused `/pb-review-*` skills instead.

---

## Why This Doc Exists

Review skills have a failure mode: **the mega-review that does simplify + dedup + correctness + security + performance all at once**. It feels comprehensive. It's usually worse than a pipeline of named passes that each refuse to do the others' jobs.

This doc collects patterns that survive real-world skill use. Each pattern names an anti-pattern, the pattern that replaces it, and where it already shows up in the playbook.

New patterns earn inclusion after at least one cycle of use. Speculative patterns stay out.

---

## Pattern 1: Scope-Locked Passes

**Status:** active, informs existing agent architecture (`code-simplifier`, `silent-failure-hunter`, `type-design-analyzer`).

### Anti-Pattern: The Omnibus Review

A single review skill (or reviewer prompt) asked to evaluate correctness AND simplicity AND duplication AND performance AND security AND style AND test coverage in one pass.

**Why it fails:**

- **Cognitive overload.** The reviewer switches frames constantly. Earlier findings color later findings ("I already flagged complexity; now I'll be lenient on duplication"). Later findings get short-changed when the output budget is already spent.
- **Blurred verdicts.** "Looks OK overall, with some suggestions" is hard to act on. Was the suggestion a P0 or a nit? Both live in the same list.
- **Echo chamber with single-model.** A model reviewing its own (or similar-prompt) output inherits shared priors. Omnibus prompts make this worse -- there's no friction between concerns.
- **Hard to bound.** No natural stopping point. When is the review "done"?

**Symptom:** reviewers produce bullet lists of mixed severity, maintainers triage the list manually, iterations feel like prose back-and-forth instead of convergent fixes.

### Pattern: Named Passes with Explicit Refusal

Split the review into passes, each with a narrow mandate. Each pass explicitly says: "This pass does X. It does NOT do Y, Z, W. Route Y/Z/W concerns to Pass N."

Canonical pass division:

| Pass | Mandate | Refuses |
|---|---|---|
| Simplify | Reduce complexity, eliminate convoluted logic, remove unnecessary work | Not correctness review, not duplication. Style only when it obscures intent. |
| Dedup | Find duplicate code introduced or expanded by the diff; reuse existing utilities | Not a general review. Style/perf/security only when required to complete a dedupe safely. |
| Correctness | Assumption-first: what does code assume, and can it be violated? | Not simplification, not dedup. Will flag security if an assumption is security-relevant. |
| (optional) Security | Trust boundaries, input validation, threat model | Not performance. Not style. |

**Why it works:**

- **Each pass has a clean stopping signal:** "reviewer found nothing more to simplify" → stop simplify pass.
- **Findings are type-sorted by construction:** simplify findings go in the simplify bucket, not mixed with security.
- **Iteration is bounded per pass:** max 3 simplify iterations, max 3 dedup iterations, etc. Natural early-exit when a pass produces no findings.
- **Adversarial potential:** different passes can run different reviewer personas/models. Simplify-reviewer thinks differently than correctness-reviewer. Omnibus prompts can't split this.

### Existing Playbook Alignment

This pattern already underpins the Claude Code agent architecture:

- `code-simplifier` agent: simplification only; refuses code-review duties
- `silent-failure-hunter` agent: error-handling focus; refuses style/perf
- `type-design-analyzer` agent: type invariants; refuses unrelated concerns
- `pr-test-analyzer` agent: test coverage focus
- `code-reviewer` agent: correctness/style gate

What's missing at the skill-prose level: **explicit scope-refusal language** inside each skill file. The agents refuse by prompt training; the `/pb-review-*` skills refuse by doc-only convention. This pattern recommends making refusal explicit in skill prose.

### When to Apply

- **New review skill:** start with a narrow mandate, name what it refuses.
- **Extending an existing review skill:** resist the temptation to add "while we're here, also check X." If X warrants attention, it's a new pass or a new skill.
- **Review pipelines (e.g., `/pb-review-comprehensive`):** name the passes, sequence them, let each one refuse the others' jobs.

### Anti-Refusal Warning Signs

| Phrase in skill prose | Likely anti-pattern |
|---|---|
| "Also consider X" (where X is a different domain) | Omnibus drift |
| "As a bonus, this skill can also..." | Scope creep |
| "While reviewing, feel free to suggest..." | No scope lock |
| "Comprehensive review of..." | Omnibus by name |

### Example Refusal Language

```markdown
## Scope

This pass **does**: flag duplicate code introduced by the diff; propose reuse of existing shared utilities.

This pass **does not**: evaluate correctness, style, performance, or security. If the dedupe requires a behavior change, flag it and stop -- do not fix it. Correctness/style/perf/security belong to other passes.
```

---

## Pattern 2: (reserved)

When a new review-skill pattern earns inclusion (via real-world use, not speculation), it lands here. Candidates under observation:

- **Bounded iteration with early exit** (from broccoli distill 2026-04-23) -- max N iterations; stop when reviewer reports no findings. Worth formalizing once dogfooded in the playbook's review cycle.
- **Adversarial-persona review** (persona-amplified Linus, used in vmx `/sharpen`) -- single-model emulation of cross-vendor diversity. Needs field data before elevating to pattern status.
- **Machine-readable verdicts** -- explicitly **not** a recommended pattern for the playbook's human-judgment-driven reviews. Noted here so future contributors don't re-derive it.

---

## Meta: How Patterns Earn Inclusion

A pattern earns a spot in this doc when:

1. It appears in at least two review skills (direct use or adaptation).
2. It has survived at least one full cycle of real use -- not just design.
3. Removing it would make the skills measurably worse.

Speculative patterns stay out. Patterns that failed in practice get removed, not hidden.

---

## Related Commands

- `/pb-review` - Fast quality gate; primary end-user review entry point.
- `/pb-review-code` - Deep PR review; consumer of these patterns.
- `/pb-review-comprehensive` - Multi-pass orchestrator; scope-locked passes pattern applies directly.
- `/pb-new-playbook` - Use when authoring a new review skill; consult this doc first.
- `/pb-evolve` - Use when refactoring existing skills; check for anti-refusal warning signs.
