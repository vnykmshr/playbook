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
version: "1.1.0"
version_notes: "v1.1.0: Scope is resolved from any input (last N, since a SHA, a branch, a patch, the working tree) and printed, because push state was never a proxy for ratification -- an already-synced batch is equally unratified, and origin/main..HEAD silently resolved to empty on it. An empty resolution is now a hard stop. Worktree scope is a distinct mode outputting a commit plan rather than verdicts. The register check gained a mechanism (quote, extract, compare, cite) instead of asserting conformance, and trust-the-content now stops at a declared security signal list. Initial: ratify changes authored in another project's session against this project's declared conventions. Policy comes from the receiving project; the command supplies mechanism. Every run installs the check that would have caught what it found by hand."
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

Run the target's register against your own messages before you commit -- the mechanism is in Step 4, and it costs you one command here versus a fix-forward commit in someone else's repo later. The register you have loaded is the producing repo's.

---

## Step 1: Scope What Arrived

Establish the batch boundary. It is *what this project has not ratified*, which is rarely "since the last release":

Say what arrived in whatever form is natural -- "the last 4 commits", "everything since `aabbcc1`", "since origin/main", "what's in my working tree", a branch, a patch. The command normalizes it; you do not pick a form.

**Do not use push state as a proxy for ratification.** `origin/main..HEAD` answers *what has not been pushed*, which is a fact about the remote. Ratification is a fact about this project's review, and work that was already synced is exactly as unratified as work that was not. Conflating them makes the scope silently empty on the most common case.

Normalize any input to one of two shapes, then **print what it resolved to** before going further:

| You say | Resolves to |
|---|---|
| last N commits | `HEAD~N..HEAD` (range) |
| since `<sha>` / a tag | `<sha>..HEAD` (range) |
| since origin / a branch | `<ref>..HEAD` (range) |
| a branch or patch | merge-base..tip (range) |
| uncommitted / staged work | working tree (worktree) |

```bash
git log --format='%h %ad %s' --date=short <range>   # what is in scope
git diff --stat <range>                             # or: git diff --stat HEAD
git status --porcelain                              # worktree shape
```

**An empty resolution is a hard stop, not a pass.** If the range holds no commits and the working tree is clean, say the scope resolved to nothing and stop. A scope that quietly resolves to empty walks every remaining step, finds nothing, and reports a clean intake -- which is what a genuinely clean intake also looks like. Same for a ref that does not exist or a SHA that is not an ancestor: fail on the input rather than silently falling back to `HEAD`.

Then read the commit bodies. Provenance is usually already there: the evidence that motivated the change names the project it came from.

### Which mode you are in

**Worktree scope is pre-ratification, not ratification.** There are no commits, so there is no message register to check, no paperwork to ride along, and nothing to revert. Steps 3 and 4 still apply to the content; Step 5 produces a **commit plan** instead of verdicts -- how to split the work so each change carries its own paperwork -- and you run this command again after committing. Say which mode you are in before Step 5.

**Range scope has a second question: is this history still private?** If the batch is unpushed, REVERT is free. If it is already on the remote, a revert is itself a published change. Check `git branch -r --contains <sha>` before offering it.

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

**Produce a finding list per commit, empty if clean.** A delegated step with no artifact gets satisfied by reading the diff and forming an impression, which is a different activity that produces a similar-sounding report. The list is how anyone -- including you, later -- can tell which one happened.

Two adjustments for incoming work:

- **A content finding needs a concrete failure, not a preference.** State the input and the wrong result. "I would have structured this differently" is not a finding against someone who had the failing case in front of them and you do not.
- **Do not redesign.** If the change is sound but not how you would have written it, that is an accept. The cost of relitigating a change whose evidence you lack is that you lose the change.

### Where trusting the content stops

Trust-the-content is a rule about *unfamiliar style*, not about unexamined risk. Incoming code is untrusted input: you did not watch it being written, and the asymmetry that justifies trusting it -- the author had evidence you lack -- says nothing about a change that is careless or hostile.

**If the batch touches any of these, the default inverts and `/pb-security` runs before any verdict:**

- Authentication, authorization, session or credential handling
- Cryptography, secret material, key or token generation
- Deserialization, template rendering, or any parser fed external input
- Subprocess execution, shell invocation, dynamic import or eval
- Network egress, outbound URLs, webhook or callback targets
- New or bumped third-party dependencies
- File-system writes outside the project, or path construction from input

Grep the diff for these signals rather than judging by the commit subject -- the subject describes the intent, and the risk is in the lines. Escalate to `/pb-review-tests` if the batch changes test behaviour.

---

## Step 4: Check Conformance

This is the pass the authoring session structurally could not run. Against the declarations from Step 2, check what changed:

| Check | Why it fails on incoming work |
|---|---|
| Required metadata updated with the change | The author did not know the field existed |
| Paperwork rides with its commit | Changelog or version landed in a neighbouring commit; bisect now lies |
| Files that must change together did | The project's coupling is undeclared outside its own context |
| Register followed (commit/PR/changelog format) | The producing repo's register is different and was loaded -- see below |
| Counts, indexes and nav kept in sync | Invisible from anywhere but here |
| Automated gates still pass | Cheap, and it is the floor rather than the bar |

Run the project's own gates before forming a verdict. **Note explicitly which checks passed automatically and which you performed by hand** -- the hand-performed ones are the input to Step 6.

### Checking the register, not asserting it

"Follows the register" is a claim, and a claim with no mechanism behind it is the defect `/pb-handoff` v1.1.0 exists to fix. Give it one:

1. **Quote the register from where the project declares it** -- the format string, the length ceilings, the required and forbidden elements. If you cannot quote it, the project has no register and this check is out of scope (Step 2).
2. **Extract what arrived** and compare mechanically, not impressionistically:

```bash
git log --format='%s' <range>     # subjects -- format, mood, length
git log --format='%b' <range>     # bodies -- ceilings, forbidden trailers
```

3. **Report per commit, quoting the violating text.** "Subject is 84 chars, ceiling is 72" is a finding; "messages look fine" is not a check.

Forbidden elements are the ones that survive review most often, because they read as normal: attribution and generated-by trailers, co-author lines the project does not use, engagement footers, emoji the register bans. They arrive from the producing repo's conventions and nobody reads past the subject line.

**Worktree mode has no messages to check.** Carry the register into the commit plan instead -- Step 5.

---

## Step 5: Verdict and Action

### Range mode: one verdict per commit

Not per batch. A batch is rarely uniformly good, and a single verdict on five commits hides the one that is wrong.

| Verdict | Meaning | Action |
|---|---|---|
| **TAKE** | Content sound, conforms | Keep it. Push with the batch |
| **FIX THEN TAKE** | Content sound, conformance gap | Fix forward in a new commit; do not rewrite the author's history to hide the gap |
| **REVERT** | Content does not survive review | Below -- the action depends on whether the history is still private |

Fix forward rather than amend. The gap is evidence about the intake path, and rewriting it away deletes the only record that the path has a hole.

**Before offering REVERT, check whether the batch is still private:**

```bash
git branch -r --contains <sha>    # empty = still local
```

Local history: drop the commit from the branch, cost is zero. Already on the remote: `git revert` is itself a published change with its own blast radius -- anyone who pulled has the original, and a revert without a stated reason reads as a mistake and gets re-contributed. Record the reason in the revert body, not just in the review.

### Worktree mode: a commit plan, not verdicts

There is nothing to take or revert yet, which is the advantage -- every conformance gap Step 4 found is still free to fix. Output the split instead:

- **One commit per concern**, each carrying its own paperwork -- the changelog line, version bump, metadata and tests that belong to it (Step 0).
- **The register applied to each proposed message**, since Step 4 had none to check.
- **Anything that should not be committed at all**, named with a reason.

Then commit the plan and run this command again in range mode. The second pass is cheap and it is the one that produces verdicts.

---

## Step 6: Install the Check

**A run that ends in a verdict has to be repeated. A run that ends in an assertion does not.**

For every conformance item in Step 4 that you checked by hand and a machine could have checked, add the check to this project before you push -- a test, a validator rule, a hook, a CI step. This is the step that makes the command shrink its own future workload: the second batch should be cheaper to ratify than the first, and if it is not, the checks are not being installed.

Two things this cannot do, stated plainly:

- **The first batch into any project is unguarded.** Nothing is installed yet. That is inherent, not a defect to design away.
- **Judgment does not mechanize.** Whether a change belongs in this project stays human. Only conformance moves into the machine, and that is the whole point of moving it.

---

## Definition of Done

- [ ] Scope resolved and **printed** -- range or worktree, never implied, never silently empty
- [ ] Mode stated (range = verdicts, worktree = commit plan)
- [ ] Project's declared conventions read before any conformance finding was formed
- [ ] `/pb-review-code` run, producing a **per-commit finding list** (empty if clean) -- not an impression of the diff
- [ ] Diff grepped for the security signal list; `/pb-security` run if any hit
- [ ] Register quoted from where the project declares it, and compared against extracted messages
- [ ] Conformance checked, with hand-checked items distinguished from automatically-checked ones
- [ ] One verdict per commit, each resolving to a concrete action; publish state checked before offering REVERT
- [ ] Every hand-checked mechanical item either installed as a check or recorded with a reason it cannot be
- [ ] Project's own gates green before push

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Check against conventions the project never declared | Read Step 2 first; if nothing is declared, stop and declare it |
| Use `origin/main..HEAD` as the scope | That is push state, not ratification state -- already-synced work is equally unratified |
| Proceed when the scope resolves to nothing | Hard stop. An empty scope and a clean batch produce the same report |
| Assert the register is followed | Quote it, extract the messages, compare, cite the violating text |
| Let "trust the content" cover security-relevant lines | Grep the signal list; a hit inverts the default and runs `/pb-security` |
| Run range-mode steps against a dirty working tree | Worktree mode outputs a commit plan; verdicts come on the second pass |
| Offer REVERT without checking publish state | `git branch -r --contains` first -- a published revert has its own blast radius |
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

*The author had the evidence. You have the conventions. Neither of you had both. | v1.1.0*
