---
name: "pb-review-incoming"
title: "Review Incoming Changes (Authored Elsewhere)"
category: "reviews"
difficulty: "intermediate"
model_hint: "opus"
execution_pattern: "sequential"
related_commands: ['pb-review-code', 'pb-standards', 'pb-handoff', 'pb-resume', 'pb-git-hygiene']
last_reviewed: "2026-11-20"
version: "1.3.0"
version_notes: "v1.3.0: Spaced double hyphens replaced. Incoming work is checked, not presumed correct: claims compared with the diff, evidence rerun or marked unverified; a fit finding names a contradiction or a carrying cost; a verdict the session cannot settle goes to lenses; an undeclared project skips only Step 4. Declarations are read at the scope's base; agent-instruction files and the project's gates join the security signals."
breaking_changes: []
---
# Review Incoming Changes (Authored Elsewhere)

**Purpose:** A change authored somewhere else has landed in this repo. Decide whether it stays.

The author was deep in another project's context when they wrote it: they had evidence you see only as they wrote it down, and they did not have this project's conventions loaded. That asymmetry, not the diff size, is what this command is built around: **check the evidence, scrutinize the conformance, decide the fit.** Nothing in an incoming change is correct because it landed.

**Mindset:** `/pb-design-rules` says separate policy from mechanism. This command is mechanism only. What counts as a valid change is decided by the project receiving it, never by this file: a gate that checks rules the project never stated is inventing them.

**Resource Hint:** opus - judgment about whether a change belongs, against conventions that must be read rather than assumed.

---

## When to Use

- Commits, a branch, or a patch arrived from a session working primarily in another repo
- Before pushing a batch you did not author in this project's context
- A contributor dropped work and you need a conformance verdict, not a redesign
- **Before you commit into a repo you are a guest in** (Step 0: run it from the producing side)
- **A dependency you consume cut a release** and you have to decide adopt, pin or skip: a version upgrade, a library bump, a sibling package's new tag (Step 1, release mode)

**When NOT to use:** your own work in your own project (`/pb-review`), a PR where the author is present to answer (`/pb-review-code`), or a periodic health check (`/pb-review-hygiene`). Capturing a reusable pattern out of a session is `/pb-learn`, which is a different job: it writes a document and has no accept/reject axis.

---

## Why This Is Not a PR Review

`/pb-review-code` assumes the author is reachable: it ends by handing findings back, and half its body is about receiving feedback and resolving disagreement. Here the authoring session has ended. There is nobody to send findings to, so **every verdict resolves into an action you take on your own history**: take it, fix then take it, or revert it.

The second difference is what to scrutinize. A normal review weights architecture and correctness heaviest. Here the author had the failing build, the hung run, the actual stack trace. What they lacked was your conventions, and what you lack is their run: Step 3 reruns the evidence the commit body carries.

---

## Step 0: Offer (Producer Side)

Run this in the *target* repo, before committing into it. Skip if you are receiving.

You are about to write into a project whose conventions are not loaded in your context. Read what it declares (Step 2), conform to it, and put the evidence in the commit body: the failing command, the measured number, the run that hung. The evidence is the part the receiving session cannot reconstruct and the part that justifies the change; the conventions are the part you are most likely to miss.

**One commit, one concern, and its paperwork rides with it.** A changelog line, a version bump or a test that belongs to a change must land in the same commit as the change. Splitting them produces a commit that documents work its own tree does not contain, which survives every checker and breaks bisect silently.

Run the target's register against your own messages before you commit: the mechanism is in Step 4, and it costs you one command here versus a fix-forward commit in someone else's repo later. The register you have loaded is the producing repo's.

---

## Step 1: Scope What Arrived

Establish the batch boundary. It is *what this project has not ratified*, which is rarely "since the last release":

Say what arrived in whatever form is natural: "the last 4 commits", "everything since `aabbcc1`", "since origin/main", "what's in my working tree", a branch, a patch. The command normalizes it; you do not pick a form.

**Do not use push state as a proxy for ratification.** `origin/main..HEAD` answers *what has not been pushed*, which is a fact about the remote. Ratification is a fact about this project's review, and work that was already synced is exactly as unratified as work that was not. Conflating them makes the scope silently empty on the most common case.

Normalize any input to one of three shapes, then **print what it resolved to** before going further:

| You say | Resolves to |
|---|---|
| last N commits | `HEAD~N..HEAD` (range) |
| since `<sha>` / a tag | `<sha>..HEAD` (range) |
| since origin / a branch | `<ref>..HEAD` (range) |
| a branch or patch | merge-base..tip (range) |
| uncommitted / staged work | working tree (worktree) |
| a dependency's new version, tag, or SHA range | version delta + consumed surface (release) |

```bash
git log --format='%h %ad %s' --date=short <range>   # what is in scope
git diff --stat <range>                             # or: git diff --stat HEAD
git status --porcelain                              # worktree shape
```

**An empty resolution is a hard stop, not a pass.** If the range holds no commits and the working tree is clean, say the scope resolved to nothing and stop. A scope that quietly resolves to empty walks every remaining step, finds nothing, and reports a clean intake, which is what a genuinely clean intake also looks like. Same for a ref that does not exist or a SHA that is not an ancestor: fail on the input rather than silently falling back to `HEAD`.

Then read the commit bodies. Provenance is usually already there: the evidence that motivated the change names the project it came from.

### Which mode you are in

**Name the mode before Step 2 runs, not before Step 5.** Steps 3, 4 and 5 each fork on it, and a step that answers two modes leaves the third to be guessed.

**Range**: commits arrived. The full command applies. One further question: is this history still private? If the batch is unpushed, REVERT is free; if it is already on the remote, a revert is itself a published change. Check `git branch -r --contains <sha>` before offering it.

**Worktree**: pre-ratification, not ratification. There are no commits, so there is no message register to check, no paperwork to ride along, and nothing to revert. Steps 3 and 4 still apply to the content; Step 5 produces a **commit plan** instead of verdicts (how to split the work so each change carries its own paperwork), and you run this command again after committing.

**Release**: a dependency you consume published something and you are deciding what to do about it. Scope is not a commit range: it is the **version delta paired with the surface this project actually consumes**. Resolve both, and print both, because the delta alone will send you re-narrating a changelog.

```bash
<pkg-manager> outdated / diff <old>..<new>     # the delta, however your ecosystem expresses it
grep -rn "<dependency>" --include=<src> .      # the surface: what this project actually reads or calls
```

Release mode inherits the empty-resolution hard stop: **"already on that version" is a real answer and must be said as one.** It must not walk the remaining steps and report a clean intake, because a clean intake looks identical.

**A hard stop still owes the concerns section of the Step 5 digest.** An empty delta is a *finished* intake, not an aborted one, and resolving the scope is itself work that learns things: that a pin is a moving pointer, that the surface has a third-party dependency in it, that the project declares no policy where you expected one. Stopping at *"already on that version"* and emitting nothing throws exactly what the digest exists to preserve, one step earlier than the digest is written. Highlights and what-was-adjusted stay correctly empty here; concerns does not.

**What you consume and what was published may differ, and the delta is written about the published thing.** A SHA pin ahead of or behind the tag, a fork, a vendored copy carrying local patches, a pre-release, a registry artifact that does not match its own git tag: each breaks the same assumption, that reading the release notes tells you what you are running. Resolve the delta against **what this project actually consumes**, and when the two differ, say so in the printed scope rather than reconciling it silently. A consumer pinned to something never released is a normal early state for a sibling dependency, not an exotic one.

### Release mode's asymmetry is different in kind

The rest of this command rests on one thing: the author had evidence and did not have your conventions. **That does not describe a release.** A published artifact carries its own contract, and was authored by people who owe you nothing about your conventions.

Four of the six steps transfer to a release nearly unchanged. Step 3's release beat is the difference: the release notes are the claim to verify, in place of a commit body.

---

## Step 2: Read What This Project Declares

This is the policy source. Read it before forming any conformance opinion:

- Project context and convention files (`.claude/CLAUDE.md`, `CONTRIBUTING.md`, `/pb-standards` output, whatever this repo actually uses)
- The commit, PR and changelog register the project follows
- Its automated gates (tests, linters, validators, hooks) and what they already cover
- Any structural rules: required metadata, files that must change together, counts kept in sync

Read them as of the scope's base (`git show <base>:<path>`; `HEAD` in worktree and release mode), not the working tree: a batch that edits a declaration or a gate is judged by the rules it arrived under, and that edit is itself a Step 3 finding.

**If the project declares nothing relevant, say so and skip Step 4; Steps 3 and 5 still run,** since a concrete failure and a security signal need no declared convention. You cannot measure conformance against conventions that were never stated, and a gate that invents them is worse than no gate: it manufactures findings the author had no way to anticipate and no basis to accept. Write the convention down before the next intake. An undeclared rule cited as a conformance finding is a preference wearing a verdict's clothes.

**Only what is already declared or already automated is in scope for conformance.** A rule you would like the project to have is a proposal for after the intake, not a conformance finding against this batch.

---

## Step 3: Review the Content by Reference

Apply the `/pb-review-code` checklist to the diff. Do not restate it here; run it there.

**Produce a finding list per commit, empty if clean.** A delegated step with no artifact gets satisfied by reading the diff and forming an impression, which is a different activity that produces a similar-sounding report. The list is how anyone, including you later, can tell which one happened.

Three adjustments for incoming work:

- **Check the evidence the change carries** (Step 0). Compare each claim that came with it (the commit body; in worktree mode, any note with the work; in release mode, the release notes below) with the diff, and rerun the failing command or the measurement at the parent and at the change. A test that arrived with the change shares its author's reading: take one expected result from the stated failure, not from the code (`/pb-jordan-testing`). Evidence you cannot rerun is marked unverified in the finding list: not proof the change is right, not grounds to revert it.
- **A content finding needs a concrete failure, not a preference.** State the input and the wrong result. "I would have structured this differently" is not a finding against someone who had the failing case in front of them and you do not.
- **Style is not a finding.** If the change is sound but not how you would have written it, that is an accept. A fit finding names what the change contradicts in this project's written text, or what it costs this project to carry; a fit call that rests on a rule nobody wrote down writes that rule where Step 2 reads, so the next intake checks it as conformance.

### Security signals

Evidence that a change fixes what it claims says nothing about a change that is careless or hostile.

**If the batch touches any of these, `/pb-security` runs before any verdict:**

- Authentication, authorization, session or credential handling
- Cryptography, secret material, key or token generation
- Deserialization, template rendering, or any parser fed external input
- Subprocess execution, shell invocation, dynamic import or eval
- Network egress, outbound URLs, webhook or callback targets
- New or bumped third-party dependencies
- File-system writes outside the project, or path construction from input
- Files that instruct an agent or a session (CLAUDE.md, AGENTS.md, skills, commands, memory, hooks, permission settings): an edit there reaches every later session
- The project's own gates and their exceptions: tests, validators, CI workflows, allowlists, baselines

Grep the diff's paths and lines for these signals rather than judging by the commit subject: the subject describes the intent, and the risk is in the lines. Escalate to `/pb-review-tests` if the batch changes test behaviour.

**Release mode narrows this list, and must.** Signal six (*new or bumped third-party dependencies*) is the entire subject matter of a release intake, so read literally it fires on every run. A rule that always fires carries no information: it gets read once, routed around, and its neighbours in the list are discredited with it. In release mode the signal is not that a version moved. It is:

- A **transitive** dependency added, removed, or moved to a different source
- A new network egress, endpoint, or callback target
- A new subprocess, shell invocation, or build/install-time hook
- A change in how untrusted input is parsed, deserialized, or rendered
- A change of maintainer, signing key, or publishing origin

Those are the lines to read the diff for; the version number is not one of them.

### The release notes are a claim about the code

**In release mode this beat is mandatory: it is Step 3's evidence check, with the release notes as the claim.** Do not assert that the notes are accurate. The mechanism is the one Step 4 already uses for the register: extract, compare, cite.

1. **Take each claim in the release notes that touches your consumed surface.** Ignore the rest; a claim about a subsystem you never call cannot mislead you.
2. **Read the code that implements it**: the diff for that change, not the summary of it.
3. **Cite the disagreement when they differ**, quoting both sides. A note saying a flag moved into config, against a diff where it moved and the old flag still silently wins, is two different systems.

A release note can be wrong in a way no test of yours will catch, because your tests encode what you believed the release said. When notes and code disagree, **the code is what you are running**, and the disagreement is a concern that survives adoption even if it does not block it. It goes in the Step 5 digest whether or not it changes the verdict.

---

## Step 4: Check Conformance

This is the pass the authoring session structurally could not run. Against the declarations from Step 2, check what changed:

| Check | Why it fails on incoming work |
|---|---|
| Required metadata updated with the change | The author did not know the field existed |
| Paperwork rides with its commit | Changelog or version landed in a neighbouring commit; bisect now lies |
| Files that must change together did | The project's coupling is undeclared outside its own context |
| Register followed (commit/PR/changelog format) | The producing repo's register is different and was loaded; see below |
| Counts, indexes and nav kept in sync | Invisible from anywhere but here |
| Automated gates still pass | Cheap, and it is the floor rather than the bar |

Run the project's own gates before forming a verdict. **Note explicitly which checks passed automatically and which you performed by hand**: the hand-performed ones are the input to Step 6.

### Checking the register, not asserting it

"Follows the register" is a claim, and a claim with no mechanism behind it is the defect `/pb-handoff` v1.1.0 exists to fix. Give it one:

1. **Quote the register from where the project declares it**: the format string, the length ceilings, the required and forbidden elements. If you cannot quote it, the project has no register and this check is out of scope (Step 2).
2. **Extract what arrived** and compare mechanically, not impressionistically:

```bash
git log --format='%s' <range>     # subjects -- format, mood, length
git log --format='%b' <range>     # bodies -- ceilings, forbidden trailers
```

3. **Report per commit, quoting the violating text.** "Subject is 84 chars, ceiling is 72" is a finding; "messages look fine" is not a check.

Forbidden elements are the ones that survive review most often, because they read as normal: attribution and generated-by trailers, co-author lines the project does not use, engagement footers, emoji the register bans. They arrive from the producing repo's conventions and nobody reads past the subject line.

**Per mode, so none is left implied:** range mode checks the messages as above. **Worktree mode** has no messages to check: carry the register into the commit plan instead (Step 5). **Release mode** has no messages of yours at all: the table above is about work authored into this project, and a release was not. What conformance means there is narrower and entirely local: did your own pin, lockfile, config and contract checks move together, and do the project's gates still pass against the new version? A release cannot violate your register. Your adoption of it can.

---

## Step 5: Verdict and Action

In every mode, a verdict the session cannot settle (TAKE or REVERT, commit or leave out, ADOPT or PIN) goes to lenses (`/pb-huddle`) before it is acted on; a REVERT or a leave-out on fit alone goes to the user with its reason.

### Range mode: one verdict per commit

**This table is range mode only.** Worktree mode produces a commit plan and release mode has its own vocabulary; both are below.

Not per batch. A batch is rarely uniformly good, and a single verdict on five commits hides the one that is wrong.

| Verdict | Meaning | Action |
|---|---|---|
| **TAKE** | Content checked, fits, conforms | Keep it. Push with the batch; unverified claims stay in the finding list |
| **FIX THEN TAKE** | Content checked and fits, conformance gap | Fix forward in a new commit; do not rewrite the author's history to hide the gap |
| **REVERT** | Content does not survive review, or the change does not fit: the verdict names what it contradicts or what it costs to carry | Below: the action depends on whether the history is still private |

Fix forward rather than amend. The gap is evidence about the intake path, and rewriting it away deletes the only record that the path has a hole.

**Before offering REVERT, check whether the batch is still private:**

```bash
git branch -r --contains <sha>    # empty = still local
```

Local history: drop the commit from the branch, cost is zero. Already on the remote: `git revert` is itself a published change with its own blast radius: anyone who pulled has the original, and a revert without a stated reason reads as a mistake and gets re-contributed. Record the reason in the revert body, not just in the review.

### Worktree mode: a commit plan, not verdicts

There is nothing to take or revert yet, which is the advantage: every conformance gap Step 4 found is still free to fix. Output the split instead:

- **One commit per concern**, each carrying its own paperwork: the changelog line, version bump, metadata and tests that belong to it (Step 0).
- **The register applied to each proposed message**, since Step 4 had none to check.
- **Anything that should not be committed at all**, named with a reason.

Then commit the plan and run this command again in range mode. The second pass is cheap and it is the one that produces verdicts.

### Release mode: adopt / pin / skip, per unit of the delta

Per unit, not per release: the same reason range mode is per commit. A release is rarely uniformly adoptable, and one verdict on twelve changes hides the one that breaks you.

| Verdict | Meaning | Action |
|---|---|---|
| **ADOPT** | Lands, with whatever migration it requires | Move the pin. Land the migration and the contract updates in the same commit |
| **PIN** | Not now, and here is the version we stay on | Record the version, the date, and the reason. A pin is a decision, not a deferral |
| **SKIP** | Does not touch what this project consumes | Say so explicitly: it is what makes the next delta smaller |

**A pin with no reason and no date is how a project ends up four majors behind with nobody able to say why.** Write both, where the pin lives, so the next intake reads a decision rather than an accident.

### The digest: required, and the reason the run was worth doing

A verdict answers *does this land*. It does not answer what the consumer opened the release for. Emit this as a named block; a skipped block is visible, a skipped habit is not.

```markdown
## Intake digest: <dependency> <old> → <new>

### Concerns surviving adoption
- ...

### Highlights, filtered through what we consume     (omit if genuinely none)
- ...

### What was adjusted                                (omit if genuinely none)
- ...
```

**Concerns surviving adoption is mandatory and has no empty case**, including on a run that hard-stopped at Step 1 with an empty delta, which reaches this block for the concerns section and nothing else. If nothing worries you, write that sentence and say what you checked to reach it. This is the highest-value output and the easiest to lose, because a green intake feels finished: a release-notes-versus-code disagreement from Step 3 lands here even when it did not block adoption, and so does behaviour that changed in a way this project tolerates now and might not later. These are the input to the next intake and the justification for every pin.

The other two are **required when non-empty** rather than always. Highlights are a projection, not a restatement: of everything in this release, the items touching what this project actually reads or calls, with the rest noted as not applicable. A consumer who reads twelve entries and names the two that matter has done the work; one who reproduces all twelve has not. Forcing a line into an empty section teaches filler, and filler is how the whole block stops being read.

---

## Step 6: Install the Check

**A run that ends in a verdict has to be repeated. A run that ends in an assertion does not.**

For every conformance item in Step 4 that you checked by hand and a machine could have checked, add the check to this project before you push: a test, a validator rule, a hook, a CI step. This is the step that makes the command shrink its own future workload: the second batch should be cheaper to ratify than the first, and if it is not, the checks are not being installed.

Two things this cannot do, stated plainly:

- **The first batch into any project is unguarded.** Nothing is installed yet. That is inherent, not a defect to design away.
- **Judgment does not mechanize.** Whether a change belongs in this project stays human. Only conformance moves into the machine, and that is the whole point of moving it.

---

## Definition of Done

- [ ] Scope resolved and **printed**: range, worktree or release, never implied, never silently empty
- [ ] Mode stated **before Step 2** (range = verdicts, worktree = commit plan, release = adopt/pin/skip + digest)
- [ ] Project's declared conventions read, as of the scope's base, before any conformance finding was formed
- [ ] `/pb-review-code` run, producing a **per-commit finding list** (empty if clean): not an impression of the diff; claims that came with the change compared with the diff, and evidence rerun or marked unverified
- [ ] Diff grepped for the security signal list; `/pb-security` run if any hit. In release mode, the **narrowed** list: not "a version moved"
- [ ] Register quoted from where the project declares it, and compared against extracted messages
- [ ] Conformance checked, with hand-checked items distinguished from automatically-checked ones
- [ ] One verdict per commit, each resolving to a concrete action; a fit verdict names a contradiction or a carrying cost; publish state checked before offering REVERT
- [ ] Every hand-checked mechanical item either installed as a check or recorded with a reason it cannot be
- [ ] Project's own gates green before push

**Release mode also:**

- [ ] Delta resolved against **what this project consumes**, not only what was published; any divergence stated in the printed scope
- [ ] Release notes verified against the code for every claim touching the consumed surface, disagreements cited with both sides quoted
- [ ] One verdict per unit of the delta; every PIN carries a version, a date and a reason
- [ ] **Digest emitted as a named block.** Concerns surviving adoption is present and non-empty: "nothing worries me" is written as a sentence with what was checked, never as an omission. **This survives a hard stop:** an empty delta ends the run, not the digest

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Check against conventions the project never declared | Read Step 2 first; if nothing is declared, say so, skip Step 4 and declare it after the intake |
| Use `origin/main..HEAD` as the scope | That is push state, not ratification state; already-synced work is equally unratified |
| Proceed when the scope resolves to nothing | Hard stop. An empty scope and a clean batch produce the same report |
| Assert the register is followed | Quote it, extract the messages, compare, cite the violating text |
| Credit the evidence a change carries unchecked | Compare its claims with the diff and rerun it; mark what you cannot rerun as unverified |
| Run range-mode steps against a dirty working tree | Worktree mode outputs a commit plan; verdicts come on the second pass |
| Offer REVERT without checking publish state | `git branch -r --contains` first: a published revert has its own blast radius |
| Redesign sound work to your own style | Accept sound-but-different; a content finding needs a concrete failure, a fit finding a contradiction or a carrying cost |
| One verdict for the whole batch | One per commit; batches are rarely uniform |
| Amend the author's commits to hide a gap | Fix forward; the gap is evidence about the intake path |
| End at a verdict and move on | Install the check, or record why it cannot be |
| Treat the producing repo's register as this one's | Registers are per-project; the producing repo's was the loaded one |
| Pile contributions up for a periodic sweep | Ratify on arrival, while the evidence is still attached |
| Take the release notes as the record of what changed | They are a claim about the code; extract, compare, cite. The code is what you are running |
| Read the delta without resolving what you actually consume | A SHA pin, fork, vendored patch or pre-release means published ≠ consumed |
| Let the dependency-bump signal fire on every release intake | A rule that always fires carries no information; use the narrowed list |
| Restate the changelog as the digest | Highlights are a projection onto your consumed surface; the rest is noted as not applicable |
| End a release intake at adopt/pin/skip | The digest is the output; a verdict alone throws away everything the run learned |
| Record a pin without a date and a reason | That is a deferral wearing a decision's clothes, and nobody can undo it later |

---

## Related Commands

- `/pb-review-code` - The review checklist this delegates to (author present, findings handed back)
- `/pb-standards` - Where a project declares the conventions this checks against
- `/pb-handoff` - The mirror direction: written here, run there
- `/pb-resume` - Where an unratified batch usually surfaces
- `/pb-git-hygiene` - Commit atomicity and bisectability

---

*The author had the evidence: check it. You have the conventions and the call. A release has a contract, and claims you verify. | v1.3.0*
