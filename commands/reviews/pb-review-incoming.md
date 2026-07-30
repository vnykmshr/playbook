---
name: "pb-review-incoming"
title: "Review Incoming Changes (Authored Elsewhere)"
category: "reviews"
difficulty: "intermediate"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-review-code', 'pb-standards', 'pb-handoff', 'pb-resume', 'pb-git-hygiene']
last_reviewed: "2026-07-31"
last_evolved: "2026-07-31"
version: "1.0.0"
version_notes: "Initial: ratify changes authored in another project's session against this project's declared conventions. Policy comes from the receiving project; the command supplies mechanism. Every run installs the check that would have caught what it found by hand."
breaking_changes: []
---
# Review Incoming Changes (Authored Elsewhere)

**Purpose:** A change authored somewhere else has landed in this repo. Decide whether it stays.

The author was deep in another project's context when they wrote it -- they had evidence you cannot reconstruct, and they did not have this project's conventions loaded. That asymmetry, not the diff size, is what this command is built around: **trust the content, scrutinize the conformance.**

**Mindset:** `/pb-design-rules` says separate policy from mechanism. This command is mechanism only. What counts as a valid change is declared by the project receiving it, never by this file -- a gate that checks rules the project never stated is inventing them.

**Resource Hint:** opus - judgment about whether a change belongs, against conventions that must be read rather than assumed.

---

## When to Use

- Commits, a branch, or a patch arrived from a session working primarily in another repo
- Before pushing a batch you did not author in this project's context
- A contributor dropped work and you need a conformance verdict, not a redesign
- **Before you commit into a repo you are a guest in** (Step 0 -- run it from the producing side)

**When NOT to use:** your own work in your own project (`/pb-review`), a PR where the author is present to answer (`/pb-review-code`), or a periodic health check (`/pb-review-hygiene`).

---

## Why This Is Not a PR Review

`/pb-review-code` assumes the author is reachable: it ends by handing findings back, and half its body is about receiving feedback and resolving disagreement. Here the authoring session has ended. There is nobody to send findings to, so **every verdict resolves into an action you take on your own history** -- take it, fix then take it, or revert it.

The second difference is what to scrutinize. A normal review weights architecture and correctness heaviest. Here the author had the failing build, the hung run, the actual stack trace. What they lacked was your conventions. Weight accordingly.

---

## Step 0: Offer (Producer Side)

Run this in the *target* repo, before committing into it. Skip if you are receiving.

You are about to write into a project whose conventions are not loaded in your context. Read what it declares (Step 2), conform to it, and put the evidence in the commit body -- the failing command, the measured number, the run that hung. The evidence is the part the receiving session cannot reconstruct and the part that justifies the change; the conventions are the part you are most likely to miss.

**One commit, one concern, and its paperwork rides with it.** A changelog line, a version bump or a test that belongs to a change must land in the same commit as the change. Splitting them produces a commit that documents work its own tree does not contain, which survives every checker and breaks bisect silently.

---

## Step 1: Scope What Arrived

Establish the batch boundary. It is *what this project has not ratified*, which is rarely "since the last release":

```bash
git log --oneline <integration-branch>..HEAD    # local commits not yet upstream
git log --format='%h %ad %s' --date=short <range>
git diff --stat <range>
```

For a branch or patch, diff against the merge base. Name the range explicitly in your output -- a review whose scope is implicit cannot be checked later.

Then read the commit bodies. Provenance is usually already there: the evidence that motivated the change names the project it came from.

---

## Step 2: Read What This Project Declares

This is the policy source. Read it before forming any conformance opinion:

- Project context and convention files (`.claude/CLAUDE.md`, `CONTRIBUTING.md`, `/pb-standards` output, whatever this repo actually uses)
- The commit, PR and changelog register the project follows
- Its automated gates -- tests, linters, validators, hooks -- and what they already cover
- Any structural rules: required metadata, files that must change together, counts kept in sync

**If the project declares nothing relevant, say so and stop.** You cannot measure conformance against conventions that were never stated, and a gate that invents them is worse than no gate: it manufactures findings the author had no way to anticipate and no basis to accept. Write the convention down first, then run this command. An undeclared rule is a preference wearing a verdict's clothes.

**Only what is already declared or already automated is in scope.** A rule you would like the project to have is a proposal for after the intake, not a finding against this batch.

---

## Step 3: Review the Content -- By Reference

Apply the `/pb-review-code` checklist to the diff. Do not restate it here; run it there.

Two adjustments for incoming work:

- **A content finding needs a concrete failure, not a preference.** State the input and the wrong result. "I would have structured this differently" is not a finding against someone who had the failing case in front of them and you do not.
- **Do not redesign.** If the change is sound but not how you would have written it, that is an accept. The cost of relitigating a change whose evidence you lack is that you lose the change.

Escalate to `/pb-security` if the batch touches trust boundaries, and to `/pb-review-tests` if it changes test behaviour.

---

## Step 4: Check Conformance

This is the pass the authoring session structurally could not run. Against the declarations from Step 2, check what changed:

| Check | Why it fails on incoming work |
|---|---|
| Required metadata updated with the change | The author did not know the field existed |
| Paperwork rides with its commit | Changelog or version landed in a neighbouring commit; bisect now lies |
| Files that must change together did | The project's coupling is undeclared outside its own context |
| Register followed (commit/PR/changelog format) | The producing repo's register is different and was loaded |
| Counts, indexes and nav kept in sync | Invisible from anywhere but here |
| Automated gates still pass | Cheap, and it is the floor rather than the bar |

Run the project's own gates before forming a verdict. **Note explicitly which checks passed automatically and which you performed by hand** -- the hand-performed ones are the input to Step 6.

---

## Step 5: Verdict and Action

One verdict per commit, not per batch. A batch is rarely uniformly good, and a single verdict on five commits hides the one that is wrong.

| Verdict | Meaning | Action |
|---|---|---|
| **TAKE** | Content sound, conforms | Keep it. Push with the batch |
| **FIX THEN TAKE** | Content sound, conformance gap | Fix forward in a new commit; do not rewrite the author's history to hide the gap |
| **REVERT** | Content does not survive review | `git revert`, or drop it from the branch if unpushed. Record why -- an unexplained revert gets re-contributed next month |

Fix forward rather than amend. The gap is evidence about the intake path, and rewriting it away deletes the only record that the path has a hole.

---

## Step 6: Install the Check

**A run that ends in a verdict has to be repeated. A run that ends in an assertion does not.**

For every conformance item in Step 4 that you checked by hand and a machine could have checked, add the check to this project before you push -- a test, a validator rule, a hook, a CI step. This is the step that makes the command shrink its own future workload: the second batch should be cheaper to ratify than the first, and if it is not, the checks are not being installed.

Two things this cannot do, stated plainly:

- **The first batch into any project is unguarded.** Nothing is installed yet. That is inherent, not a defect to design away.
- **Judgment does not mechanize.** Whether a change belongs in this project stays human. Only conformance moves into the machine, and that is the whole point of moving it.

---

## Definition of Done

- [ ] Batch boundary named explicitly, not implied
- [ ] Project's declared conventions read before any conformance finding was formed
- [ ] Content reviewed by reference to `/pb-review-code`, with no finding resting on preference
- [ ] Conformance checked, with hand-checked items distinguished from automatically-checked ones
- [ ] One verdict per commit, each resolving to a concrete action
- [ ] Every hand-checked mechanical item either installed as a check or recorded with a reason it cannot be
- [ ] Project's own gates green before push

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Check against conventions the project never declared | Read Step 2 first; if nothing is declared, stop and declare it |
| Redesign work whose evidence you cannot see | Accept sound-but-different; require a concrete failure for content findings |
| One verdict for the whole batch | One per commit -- batches are rarely uniform |
| Amend the author's commits to hide a gap | Fix forward; the gap is evidence about the intake path |
| End at a verdict and move on | Install the check, or record why it cannot be |
| Treat the producing repo's register as this one's | Registers are per-project; the producing repo's was the loaded one |
| Pile contributions up for a periodic sweep | Ratify on arrival, while the evidence is still attached |

---

## Related Commands

- `/pb-review-code` - The review checklist this delegates to (author present, findings handed back)
- `/pb-standards` - Where a project declares the conventions this checks against
- `/pb-handoff` - The mirror direction: written here, run there
- `/pb-resume` - Where an unratified batch usually surfaces
- `/pb-git-hygiene` - Commit atomicity and bisectability

---

*The author had the evidence. You have the conventions. Neither of you had both. | v1.0.0*
