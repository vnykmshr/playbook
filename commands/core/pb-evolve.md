---
name: "pb-evolve"
title: "Evolve Playbooks to Match Claude Capabilities"
category: "core"
difficulty: "beginner"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-claude-global', 'pb-claude-project', 'pb-standards', 'pb-preamble', 'pb-design-rules']
last_reviewed: "2026-11-04"
version: "2.0.0"
version_notes: "v2.0.0: Rewritten for one owner and many repos. Step 0 takes in harvested feedback until the harvester exits 0; each release runs as one /pb-forge arc; push, tag and release are separately gated; rollback redeploys the previous tag. Team machinery, the snapshot, log and diff steps, mkdocs and pbai are gone."
breaking_changes: ['Quarterly calendar dates, Evolution Manager, review meeting and pre-evolution checklist removed', 'Steps 1.5 and 4-11 replaced: no evolution-snapshot.py, evolution-log.py or evolution-diff.py step; rollback is a redeploy of the previous tag', 'Report, dashboard, log-structure and rollback-report templates removed', 'Step 0 Intake added: the cycle closes only when scripts/feedback-harvest.py exits 0']
---

# Evolve Playbooks to Match Claude Capabilities

**Purpose:** Once a quarter, or when a model or harness release lands, take in the feedback every repo has written about the playbook, check each surface against what the model can now do, and ship the changes. One owner, many repos.

**Mindset:** Apply `/pb-preamble` thinking (challenge what is still true, past rulings included) and `/pb-design-rules` thinking (does each command still earn its clarity and simplicity?). The evidence is the sessions' feedback and the vendor's docs, never the model's account of itself.

**Resource Hint:** opus - capability assessment, disposition calls and design decisions.

---

## When to Use

- **Quarterly:** Feb, May, Aug, Nov
- **A model or harness release** that changes defaults, context, tools or pricing
- **A harvested backlog** large enough to be a cycle of its own

---

## Step 0: Intake

```bash
python3 scripts/feedback-harvest.py; echo "exit $?"
```

The harvester reads every `~/workspace/github/*/*/todos/` and the Claude memory `feedback_*.md` files, keys each item on its normalised text, and writes `todos/evolve/digest-YYYY-MM-DD.md`. It never writes the ledger.

| Exit | Meaning | Do |
|------|---------|----|
| 0 | Every key dispositioned | Go to Step 1 |
| 1 | Undisposed keys, or taken keys seen again | Disposition or re-rule them |
| 2 | Nothing found, a malformed ledger, or an error | Fix the root, the ledger or the error; the digest is not evidence |

Keys seen in more repos rank first; memory items come last. Cluster near-duplicates by hand, then give every key one row in `todos/evolve/harvest-ledger.tsv`, tab-separated `key disposition version date`:

- `taken`: a release this cycle carries it; version names that release
- `rejected`: the reason goes in the cycle record
- `deferred`: names where it goes (a later release, a single decision)
- `dup-of:<key>`: the cluster's representative carries the disposition

Markers in the digest:

- `may be fixed`: the named command changed its body and version after the note, and the line shows that version's notes. Any body edit forces a bump, dash and fence fixes included, so it is a hint to check, never a reason to close a key.
- `private`: the source is an org listed in `todos/evolve/private-orgs` (untracked, one per line).
- **Taken, then seen again**: a dated note repeats a `taken` key after its row's date, so the fix did not reach the sessions that wrote it. It holds exit 1 until you edit that row. Memory files and undated notes cannot recur.

**The cycle does not close until the harvester exits 0.**

## Step 1: Prepare

```bash
git status                                    # clean
git checkout main && git pull origin main
python3 scripts/evolve.py --analyze           # model_hint and category counts (Step 3)
python3 scripts/evolve.py --validate
python3 scripts/git-signals.py                # adoption, churn, pain points: todos/git-signals/latest/
```

Open the cycle record, `todos/evolve-YYYY-qN/`: `inputs.md` (taken and deferred keys, git signals), `ground-truth.md` (Step 2), `huddle.md` and `plan.md` (Steps 3-4).

## Step 2: Capability Ground Truth

What changed since the last cycle: tiers and their speed or cost, context windows, tools, harness features and defaults.

Fetch the vendor's current prompting guidance and harness docs to disk and extract `ground-truth.md`. The model under review is not a reliable witness to its own capabilities: the 2026-06 Fable trial and a 2026-09 research subagent both asserted capability facts the docs contradicted. A capability claim that is not in the ground-truth file does not enter the review.

## Step 3: Help or Constrain

**The question:** does each playbook surface still structure and check the model's work, or has it become a constraint that keeps a stronger model from its best work? It runs every cycle, including cycles with no model release: a harness change or a session's evidence moves the line as much as a new model does.

**The line.** A surface earns its place when it carries what the model cannot derive from the repo or would not do by default:

- Decisions and consent boundaries the owner made
- This project's conventions, couplings and gotchas
- Behaviours the vendor documents as needing instruction (response length and scope, as of 2026-09)
- Checks that execute: a test, a guard, a hook

It constrains when it:

- Re-teaches what the model does natively or what the harness already does
- Instructs re-verification of work the model already verifies
- Prescribes reasoning steps where stating the outcome would do
- States facts that rot (model versions, SHAs, counts) in a file loaded every session

**Where to look, by cost.** Auto-loaded surfaces first (generated global and project CLAUDE.md, the memory index): every line is paid every session and cannot be corrected mid-session. Then commands that chain or stack checks. On-demand reference commands last: they cost nothing until invoked, so review them only when a finding points there.

**Two-sided, by rule.** Before proposing any cut, name at least one place where the model needs *more* structure, with evidence, or state that you looked and found none. A review that only deletes is a prune machine run one line at a time. The 2026-09 panel of four argued deletion and nobody argued addition, while the one addition that cycle (a scope rule) answered a documented weakness.

**Deletion needs evidence, not self-report.** The model judging the rules is the model the rules govern, and "I would do that anyway" is the one claim it cannot make about itself. Cut a behavioural rule on vendor documentation or on observed sessions, never on the model's account of its own defaults. The 2026-09 session that argued verification is native also repeated the cheapest-surface mistake its own memory warned about.

**Scope:** this review changes what commands say. It does not retire commands; retirement stays a single human decision.

**Run it as a huddle** (`/pb-huddle`): same brief to every panelist, ground-truth file attached, this question alongside the cycle's own. Record a trend row in the cycle record so the next cycle compares rather than re-derives:

| Measure | Q3 2026 baseline |
|---------|------------------|
| Global CLAUDE.md, generated lines | 158 |
| Project CLAUDE.md (the playbook's own), lines | 86 |
| Verify-instructions in auto-loaded files | 0 (was 4) |
| Model-version strings in generator templates | 0 (`TestTemplateCurrency`) |
| Structure added / cut | 1 / ~12 |

## Step 4: Propose and Run

Group the taken keys and the Step 3 findings into releases, one deliverable each, and write them to `plan.md` with the keys each release carries. Run each release as one `/pb-forge` arc: a huddle only where a fork exists, Self-gate as forge defines it, Land through Step 6.

## Step 5: Regenerate and Verify

```bash
python3 scripts/evolve.py --generate          # indices
./scripts/build-mdbook.sh                     # build first: check-links reads the built site
python3 scripts/check-links.py
python3 -m pytest tests/ -q
```

Then regenerate with `/pb-claude-project` and `/pb-claude-global` and diff before keeping; both preserve `## Custom (Manual)`.

## Step 6: Release and Rollback

Release each version with `/pb-release`. The push, the tag and the GitHub release are three separately approved actions under the external action gate; never push a tag in the same command as a branch.

If a deploy breaks a site, redeploy the previous tag (rehearsed 2026-09-24, about a minute for both), then fix forward on main:

```bash
gh workflow run deploy-docs.yml --ref <prev-tag>
gh workflow run deploy-book.yml --ref <prev-tag>
```

---

## Scenarios

| Signal | Action |
|--------|--------|
| A faster or cheaper tier | Revisit `model_hint` and the tier table; measure on real tasks before moving a hint |
| A larger context window or a new tier | Keep context hygiene for the default; name the workflows that justify the larger tier |
| A key recurs across repos | Read the sources, not only the digest line; fix the step sessions keep working around; mark it `taken` with the release |
| A new capability or harness feature | Ground-truth it first; add or cut structure on documentation or observed sessions |

## What Doesn't Change

- **Preamble thinking** (challenge assumptions, peer collaboration)
- **Design rules** (clarity, simplicity, robustness)
- **Atomic commits and quality gates**
- **Test-first discipline**

---

## Definition of Done

- [ ] `scripts/feedback-harvest.py` exits 0: every key has a ledger row
- [ ] Help-or-constrain review run (Step 3): ground-truth-backed, two-sided, trend row recorded
- [ ] All playbooks validated (`python3 scripts/evolve.py --validate`); no circular cross-references
- [ ] `python3 -m pytest tests/ -q` and markdownlint pass
- [ ] Fresh `./scripts/build-mdbook.sh`, then `python3 scripts/check-links.py` passes
- [ ] CHANGELOG updated, one entry per shipped version
- [ ] Cycle record complete in `todos/evolve-YYYY-qN/`
- [ ] Each tag pushed only after CI is green on its commit; both sites verified

---

## Related Commands

- `/pb-claude-global` - Regenerate global CLAUDE.md
- `/pb-claude-project` - Regenerate project CLAUDE.md
- `/pb-standards` - Quality standards (validated by evolution)
- `/pb-preamble` - Thinking philosophy (doesn't change)
- `/pb-design-rules` - Design principles (doesn't change)

---

*Evidence in, dispositions out. The cycle closes when the harvester exits 0.*
