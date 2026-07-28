# Playbook Vocabulary

Terms this playbook coins, or gives a narrower meaning than they carry elsewhere.

## What belongs here

A term earns an entry when it appears across many commands and a reader would otherwise
have to infer it. General software vocabulary does not qualify: *branch*, *refactor*,
*circuit breaker* and their kin are defined better elsewhere, and a copy here is a copy
that ages.

**What must never appear here:** command titles, command descriptions, command counts,
version numbers, thresholds, or file paths written as prose. Each of those already lives
in exactly one authoritative place and changes without announcing itself. This page
carried twenty-three such rows for months; seven of seven sampled were wrong, and one
published the wrong description for `/pb-review` on the public site, sending readers
confidently to a different command. A corpus-wide hygiene sweep touched this file a day
earlier and walked past all seven, because nothing here could be checked.

So the rule is mechanical rather than a matter of care:

> **Every claim on this page is either definitionally stable -- still true no matter what
> ships -- or machine-checked. Nothing in between.**

Markdown links to files are verified by `scripts/check-links.py` on every build. Command
names written in prose are verified by `tests/test_glossary_conventions.py`, which also
rejects titles, counts, and version strings outright. If a fact cannot be made checkable,
define the concept and let the fact live where it is owned.

---

## Terms

### BEACON

A marker prefixing a load-bearing section in a `CLAUDE.md` file, as `## BEACON: Non-Negotiables`.
It flags content that must survive skimming and summarization. Generated context files mark
their sections this way so the sections that matter stay findable after the file grows.

### Resource Hint

The line in a command naming which model tier it expects and why. It is guidance about the
shape of the work -- planning and adversarial review versus mechanical execution -- not a
constraint the harness enforces.

### Model Hint

The front-matter field carrying the same judgement as the Resource Hint in machine-readable
form, so tooling can reason about a command without parsing its prose.

### Persona

A named reviewing voice with a defined domain, invoked as its own command. Personas exist to
disagree: running several over one artifact surfaces the objection a single pass would smooth
over. See [Boundary & Authority](#boundary--authority).

### Boundary & Authority

The block in each persona naming four things: what it owns, what it refuses and routes
elsewhere, the persona it is most often confused with, and where its judgement is decisive.
Together these blocks are the playbook's concept-to-owner index -- distributed, each one
next to the authority it describes, which is the only arrangement that cannot drift out of
sync with the thing it indexes.

### Lane

A persona's domain. Authority is decisive in-lane and advisory outside it, which is what
lets a panel disagree without deadlocking: the owner of the lane closes the question.

### Definition of Done

The closing checklist on a multi-step command. Its purpose is to make completion observable
rather than felt -- each item states a condition that can come out either way.

### MLP

Minimum Lovable Product. The completion bar this playbook uses in place of "it works":
would you use this daily without frustration, can you recommend it without apology, and did
you build the smallest thing that feels complete. Any "no" means keep refining.

### Shadow Path

For a given data flow, the nil, empty, and error paths enumerated deliberately alongside the
happy path. Distinct from "test the edge cases": the shadow paths are named systematically,
and being unable to name them is the signal that the flow is not yet understood.

### Scope Mode

Whether the current work is expanding, holding, or reducing scope -- declared before coding
rather than discovered during review, so that "this grew" is a decision instead of a surprise.

### Working Context

The short project snapshot a session loads to recover state: current version, recent work,
and what comes next. It is regenerated rather than accumulated, and it is working material,
not a tracked artifact.

### Session Recap

The reflection written at the end of a session and surfaced at the start of the next one --
once. It is read, acted on, then archived. A recap that is only ever written is a log; the
surfacing is what makes it a loop.

### The Ritual

The default working loop: start work, write code, run the quality gate, open a pull request
when peer review is needed. Most sessions need nothing beyond these.

### Evolution Cycle

The quarterly pass that revises commands against how they have actually been used, plus the
out-of-band updates triggered when tooling capability changes underneath them.

### Tool-Agnostic

The property that a command's substance is readable as plain Markdown and executable by hand
or by any assistant. The Claude Code integration is a convenience layer over that substance,
never a prerequisite -- with the deliberate exception of the commands whose subject *is* that
integration.

---

## See Also

- **[Decision Guide](decision-guide.md)** - Which command to use?
- **[Command Reference](command-index.md)** - All commands, generated
- **[Getting Started](getting-started.md)** - Quick start
- **[How Commands Talk](voice.md)** - The register commands use with you
- **[FAQ](faq.md)** - Common questions
