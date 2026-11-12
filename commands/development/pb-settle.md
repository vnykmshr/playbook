---
name: "pb-settle"
title: "Settle Leftovers to a Clean Baseline"
category: "development"
difficulty: "advanced"
model_hint: "opus"
execution_pattern: "interactive"
related_commands: ['pb-resume', 'pb-forge', 'pb-huddle', 'pb-evolve', 'pb-review-hygiene']
last_reviewed: "2026-11-12"
version: "1.0.0"
version_notes: "v1.0.0: Rule on every leftover a resume surfaces and stop at a stated clean baseline before new work starts."
breaking_changes: []
---
# Settle Leftovers to a Clean Baseline

`/pb-settle` works down what earlier sessions left behind: recap findings, notes from other projects, open proposals, stale plans, pending PRs and pins. It rules on each item, lands the small ones now, gives the rest a durable home, and stops at a stated clean baseline before new work starts. It runs after `/pb-resume`, never inside it: resume rebuilds context and proposes; settling the list is a separate decision.

**Resource Hint:** opus - rulings on mixed items, a lead's vet, and a release call.

**Tool-agnostic:** Claude Code users invoke as `/pb-settle`. Using another tool? Read this file and run the steps by hand; the round's record is a plain markdown file.

---

## Mindset

Apply `/pb-preamble` thinking: a leftover's status line is a claim, and whoever wrote it may have been wrong about what is still open. Apply `/pb-design-rules` thinking: simple by default (most rows are a move or a one-line fix) and fail noisily (a row with no home is a finding, not a pass).

---

## When to Use

- After `/pb-resume` proposes more than you would do inline: findings, notes and proposals that each need a ruling.
- Before a quarter's work, a large deliverable, or a regroup on what comes next.
- After a release whose Land left items behind.

Skip it when the list is one or two obvious items: do them.

---

## The Round

A round is one `/pb-forge` deliverable with many rows. Its record is a forge cursor (`todos/forge/<slug>.md`), so a session that stops mid-round resumes from it.

### 1. State clean first

Write the round's falsifier before ruling on any row: the observable checks that, all passing, mean new work can start. Typical clauses: the project's tests exit 0 on a clean tree; every row has a ruling and a home; local matches remote. Add the project's own clauses (an empty inbox, a current context file). A clause you cannot check is not part of clean.

### 2. Intake

One table, one row per leftover: source, claim, check (measured, inferred or unverified), lean. Sources are everything `/pb-resume` proposed plus whatever else the project keeps: notes other projects left, open PRs and dependency bumps, red CI, plan and sketch files, open cursors, stashes. A status line that claims open work is checked against the artifact before it gets a lean: plans marked open are often already shipped.

### 3. Fold in, or give it a home

A row lands in this round only if all three hold: it is one change with no design question; it names an observed failure, not a preference or a note that something worked; it contradicts nothing already written. A mechanical row (a reversible move, an archive entry) needs only its check. Every row gets a ruling and a durable home:

| Ruling | Home |
|---|---|
| TAKE | lands in this round |
| OWN ARC | its own Frame-stage `/pb-forge` deliverable, its cursor written before the round closes so the next resume lists it |
| DEFER | a named later cycle (`/pb-evolve`, a dated plan) that will read it |
| REJECT | with the reason, where the source's next reader looks (the recap archive, a ledger, the closed PR), so it is not proposed again |
| DONE | the artifact that shows it already shipped |

A deferral nobody will read is a rejection with a delay: reject it. Rows that act on a remote or live infrastructure, cannot be undone, or need the user's hands leave the batch as their own gated stops. The round must not become the next planning cycle.

### 4. Vet, then stop

The lead for the round's main lane vets the leans, as forge does at every stop, convening lenses only for disputed or cross-lane rows (see `/pb-huddle`). Each TAKE carries its exact change, so the vetted rulings are the plan. Stop once with them, and with every question only the user can answer (a preference, a constraint, a landing route with no precedent, a row that needs their hands), each carrying a lean. Execution starts when the user has confirmed or overridden each one.

### 5. Land the TAKEs

Mechanical rows (reversible moves, archive entries) run inline. Rows that edit shipped text or code run through forge from Execute (`--arc build`): steps 1-4 were the front arc, so forge starts at Execute; its Self-gate still runs on the diff. A source (a note, a plan file) moves to the archive only once its rows are taken in. Land the way this project lands (a PR, a branch, or commits to main) and in its commit and writing style: follow the precedent in its history; where there is none, the route is one of step 4's questions.

### 6. Decide release at the close

Record the release call as open when the round starts, and decide it at the close from what landed. The lead brings a lean (nothing; a tag; a tag with notes), and forge's Land and `/pb-release` carry it out, each step gated. A lean toward a tag runs forge's code-review on the round's range first, since an open call only offered it. Nothing means the round owes no release: its cursor closes after the last merge or push (forge's "the merge if not"), and a later release that ships these changes is its own deliverable.

### 7. Run the falsifier, report, stop

Run every clause from step 1. Report clean, or name the clause that fails and why. Then hand over: the session's own work starts here.

---

## Definition of Done

The round is not complete until ALL boxes are checked:

- [ ] The falsifier was written before any row was ruled
- [ ] Every row has a ruling and a home
- [ ] Status claims were checked against artifacts
- [ ] The user confirmed or overrode every ruling and question before execution
- [ ] TAKEs landed with the project's tests passing per commit
- [ ] The release call was made at the close and recorded, "none" included
- [ ] Every falsifier clause ran and passed, or the failing clause is reported

---

## Related Commands

- `/pb-resume` - Rebuilds context and proposes; settle runs after it, as its own decision
- `/pb-forge` - The round's cursor, Execute and Self-gate
- `/pb-huddle` - Lenses for disputed rows
- `/pb-evolve` - The usual home for deferred rows
- `/pb-review-hygiene` - A codebase audit whose findings can feed a round's intake

---

*Rule on every leftover. Land what is small. Start new work on a stated baseline.*
