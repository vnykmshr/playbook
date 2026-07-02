# Sketch: Paul Skills Adoption — `/pb-threat-hunt` + Pattern Hardening

**Created:** 2026-07-02
**Status:** decisions pending

## Problem

Paul Greenberg shipped 12 agent skills in a 24-commit burst across go-authcrunch and caddy-security. His threat-hunting methodology is the most complete security audit workflow committed to an agent skill — 12 executable steps with per-step commands, adversarial payload catalog, 5-level severity rubric, and 9-checkbox DoD. The playbook's `/pb-security` is a checklist, not a deep audit methodology. Other Paul patterns (Tests honesty, generated-artifact awareness, DoD checklists) are lightweight improvements the playbook should absorb without importing Paul's full agent-skill architecture.

## Scope Summary

**In Scope:**
- New command: `/pb-threat-hunt` in `commands/reviews/` — executable 12-step security audit methodology
- DoD checklist convention documented in `/pb-documentation`
- 4 pattern hardenings: Tests honesty in `/pb-commit`, generated artifacts in `/pb-claude-project`, prohibition audit in `/pb-standards`, cross-ref from `/pb-security` → `/pb-threat-hunt`
- Version bump v2.24.1 → v2.25.0 (MINOR — new command)
- Attribution in command footer + CHANGELOG
- Bookkeeping: `mdbook/SUMMARY.md`, `CHANGELOG.md`, two EXPECTED_COUNT files (113→114)

**Out of Scope:**
- AGENTS.md, per-skill platform metadata (tool-agnostic principle)
- Configuration router formalization (category structure already solves this)
- 4-section commit template (1-3 line register is deliberate)
- Existing-command DoD audit (Q3 evolution, noted)
- `/bounty-hunt` cross-reference (vmx orchestrator local command — user handles)

## Approach Summary

One PR, 6 commits on main (playbook ships single-commit to main). `/pb-threat-hunt` as executable command (Go default + Python/Node appendices). DoD checklist convention documented in `/pb-documentation` as a structural convention. Phase 2 pattern hardenings folded in. Paul's meta-architecture rejected — CLAUDE.md already serves the entry-point role, Related Commands is already composition, BEACON non-negotiables already use "Never."

## Decision Forks

### Fork 1: Which command to drop from `/pb-security` Related Commands?

**Why this fork exists:** `/pb-security` has 5 Related Commands in both frontmatter and body: pb-review, pb-review-hygiene, pb-hardening, pb-secrets, pb-patterns-security. Adding `/pb-threat-hunt` requires dropping one. The ≤5 constraint is enforced by convention checks.

Options:
- 1-a) Drop `pb-review-hygiene` — periodic health check, least security-specific. Body mentions it once ("Security section in code review").
    - Recommended if keeping the most security-adjacent commands. Reasoning: review-hygiene is a general code-quality command; threat-hunt is directly security-audit.
- 1-b) Drop `pb-patterns-security` — reference patterns, not executable. Already body-linked as "Security patterns for microservices."
    - Recommended if keeping executable commands over reference ones. Reasoning: threat-hunt is executable; patterns-security is passive reference.
- 1-c) Drop `pb-review` — the comprehensive review orchestrator. Cited in body as "Comprehensive multi-perspective review orchestrator."
    - NOT recommended. Reasoning: pb-review is the primary review entry point; dropping it breaks the discoverability chain.

**Recommended:** 1-b (drop `pb-patterns-security`). Reasoning: threat-hunt is executable; patterns-security is reference. Replacing reference with executable strengthens the Related Commands list. pb-patterns-security still appears in the body as a cross-reference under Integration with Playbook.

### Fork 2: Language generalization strategy in `/pb-threat-hunt`

**Why this fork exists:** Paul's search passes are Go-specific (`rg 'ParseWithClaims|jwt\.Sign'`, `rg 'go func'`, `rg '\.\(\w+\)'`). The playbook is multi-language. Generalization can be inline (one workflow with language-agnostic descriptions) or appendix-based (Go as default, appendices for Python/Node).

Options:
- 2-a) Fully language-agnostic — describe each search pass by vulnerability class (e.g., "JWT confusion: flag libraries that parse without algorithm validation"), provide idiomatic `rg` patterns for Go/Python/Node inline.
    - Recommended if the command should work for any project without preamble. Reasoning: more usable out of the box, but verbose (3x pattern blocks per step).
- 2-b) Go default + language appendices — preamble says "This methodology targets Go projects by default." Appendices A (Python) and B (Node) provide idiomatic equivalents for language-specific passes. Language-agnostic passes (URL canonicalization, redirect trust) work for all.
    - Recommended if Paul's Go-specific voice should be preserved as the primary path. Reasoning: cleaner primary workflow, appendices are reference-only.
- 2-c) Keep Go-specific — don't generalize. Document it as "designed for Go projects; adapt patterns for other languages."
    - Recommended if the playbook shouldn't maintain multi-language search pass catalogs. Reasoning: honest about scope, zero maintenance burden, but limits audience.

**Recommended:** 2-b (Go default + appendices). Reasoning: preserves Paul's battle-tested Go patterns as the primary path without limiting the command to Go-only projects. Appendices are maintainable — they're reference tables, not duplicated workflows.

### Fork 3: DoD checklist convention — where to document?

**Why this fork exists:** The huddle decided to document the DoD checklist as a structural convention so `/pb-threat-hunt` is the exemplar, not a one-off. Three candidate homes with different audiences.

Options:
- 3-a) `/pb-documentation` — the writing guidelines for commands. Add a section: "Multi-step commands should end with a Definition of Done checklist." `/pb-threat-hunt` becomes the example.
    - Recommended if DoD is primarily a documentation convention. Reasoning: `/pb-documentation` is the natural home for "how to write a command"; the existing Documentation Checklist already models the pattern.
- 3-b) `/pb-standards` — the quality standards. Add a non-negotiable: "Multi-step commands include a terminal DoD checklist."
    - Recommended if DoD should be enforced, not just suggested. Reasoning: non-negotiables get mechanical enforcement (convention check scripts).
- 3-c) `/pb-templates` — the SDLC templates reference. Add DoD as a template pattern.
    - Recommended if DoD is a general SDLC pattern, not just a playbook-command convention. Reasoning: broader audience, but `/pb-templates` is already dense.

**Recommended:** 3-a (`/pb-documentation`). Reasoning: it's a documentation convention for command authors, not a quality standard that needs mechanical enforcement (yet — Q3 audit may elevate it). The existing Documentation Checklist in `/pb-documentation` (lines 776-793) already models the pattern; a new "Command Structure" section integrating DoD is a natural extension. This is Sam's recommendation from huddle; Linus's push for non-negotiable status can be the Q3 audit outcome.

### Fork 4: CHANGELOG format

**Why this fork exists:** The handoff proposes 6 changes (new command + 5 hardenings). The CHANGELOG can consolidate them under one `### Added` entry or list them separately.

Options:
- 4-a) Single consolidated `### Added` entry: "**Paul Greenberg Agent Skills Adoption** — `/pb-threat-hunt` security audit methodology (12-step executable workflow, adapted from greenpau/go-authcrunch, Apache 2.0). Pattern hardenings: Tests honesty in `/pb-commit` register, generated-artifact awareness in `/pb-claude-project`, DoD checklist convention in `/pb-documentation`, cross-reference from `/pb-security`."
    - Recommended if the changes form a coherent deliverable. Reasoning: tells the story as one adoption, not 6 disconnected changes. Follows the "don't split Added+Fixed across the same release" lesson from the session recap.
- 4-b) Separate entries per change: `/pb-threat-hunt`, Tests honesty, generated artifacts, DoD convention, cross-reference.
    - Recommended if each change is independently notable. Reasoning: granular, but scatters the Paul attribution across entries.

**Recommended:** 4-a (consolidated). Reasoning: these are one deliverable — Paul's patterns adopted into playbook. The consolidation avoids the two-phase-narrative trap (Added: feature → Fixed: ordering corrected) the session recap flagged. Attribution stays coherent: one entry credits Paul once.

## Recommended Picks (copy/paste)

`1-b, 2-b, 3-a, 4-a`

## Open Questions

- `/pb-security` frontmatter `related_commands` lists `pb-patterns-security` but body lists `pb-review-hygiene` instead of `pb-patterns-security` — which is authoritative? The body (line 735) and frontmatter (line 8) actually both list the same 5. Checked; they match. No drift.
- Should the adversarial payload catalog live in `/pb-threat-hunt`'s body or as a separate `docs/reference/threat-hunting-payloads.md`? Recommendation: inline — it's executable content, not passive reference.

## Feeds Into

- `/pb-spec` — takes this sketch + resolved decisions, produces detailed implementation steps
- `/pb-adr` — if the command/reference distinction or DoD convention warrants formal recording
