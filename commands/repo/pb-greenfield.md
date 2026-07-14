---
name: "pb-greenfield"
title: "New Project, End to End (Idea → Working Repo)"
category: "repo"
difficulty: "intermediate"
model_hint: "opus"
execution_pattern: "interactive"
related_commands: ['pb-zero-stack', 'pb-claude-project', 'pb-context', 'pb-plan', 'pb-start']
last_reviewed: "2026-07-14"
last_evolved: "2026-07-14"
version: "2.0.0"
version_notes: "v2.0.0: Renamed from pb-repo-init and rewritten. Idea in, working repo out: five questions, one routing decision, playbook-layer install. Emits files, not a plan. Capped at ~150 lines -- the line budget is the guardrail against regrowing into a second /pb-zero-stack."
breaking_changes: ['Renamed from pb-repo-init - the old name no longer resolves', 'No longer emits a phase plan; that content moved to /pb-plan -> /pb-spec', 'Language directory trees removed - the ecosystem initializers own them']
---
# New Project, End to End (Idea → Working Repo)

You have a sentence. You want a repo you can start working in. This runs that conversation and writes the files.

> **Static site or small app that should cost $0/month?** `/pb-zero-stack` owns that topology and goes deeper on it than this does. Start here anyway if you're unsure -- Step 2 routes you there.

**Mindset:** Apply `/pb-preamble` thinking -- challenge the idea before scaffolding it; the best outcome of Step 1 is sometimes "don't build this." Apply `/pb-design-rules` thinking -- simple by default, and build the smallest thing that feels complete.

**Resource Hint:** opus - Step 2 is an architecture call (does the topology fit, what does the idea imply). Scaffolding is pattern application.

---

## When to Use

- **You have an idea, not a spec** - "let's build a CLI that syncs my notes"
- **You want the playbook's conventions from commit one** - `/pb-start`, `/pb-pause`, `/pb-resume` working on day two
- **New service in an existing architecture** - the shape questions still apply

## When NOT to Use

- **Scope isn't settled and the stakes are high** - `/pb-plan` locks scope first, then come back
- **The repo already exists** - `/pb-claude-project` for context, `/pb-repo-organize` for structure
- **You want a machine set up, not a project** - `/pb-setup`

---

## Step 1: Shape (Five Questions)

Ask these before scaffolding anything. The answers pick the topology in Step 2.

1. **What is it, in one sentence?** If it takes three, the idea isn't ready.
2. **Who uses it, and how often?** You alone, daily? A team, weekly? Public, rarely?
3. **Where does the data live?** Nowhere / local files / a database / someone else's API.
4. **What does it run on?** Their machine (CLI, desktop) / a browser / a server / a schedule.
5. **What's the smallest version that's useful?** Name it. That's what gets scaffolded.

**Push back here when it's warranted.** If the idea is three ideas, say so. If the smallest useful version is a shell script, say that -- and stop. A scaffold you talked someone out of is a good outcome.

---

## Step 2: The Routing Decision

One decision. Two exits.

**Fits the Gist topology** -- static files, optional edge compute, no accounts, no server-side state, read-heavy: stop here and hand to `/pb-zero-stack`. It owns that topology (complexity tiers, trust boundaries, CSP, budget math, ship gate). Don't re-derive any of it.

**Everything else** -- CLI, service, library, daemon, data pipeline, or anything with accounts, uploads, SQL, real-time, or SSR: continue to Step 3.

State the call and its reason in one line, so it's on the record: *"CLI on the user's machine, local files, no server -- general path."*

---

## Step 3: Scaffold

Use the ecosystem's own initializer -- `go mod init`, `npm create`, `uv init`, `cargo new`. Don't hand-roll a directory tree; the ecosystem already has an opinion, and it's better maintained than ours.

On top of that, only what the smallest useful version needs:

- An entry point that runs and does one real thing
- One test that asserts something real
- One lint/format config
- A README: what it is, how to run it. Two paragraphs. `/pb-repo-readme` writes the real one later, when there's more to say
- A LICENSE **if this will ever be public** - without one it's all-rights-reserved, whatever the repo's visibility says
- `.gitignore` -- `todos/` and `memory/` always (working material). `.claude/` is a choice: ignore it solo; on a team, commit `CLAUDE.md` so teammates get the context and ignore only `settings.local.json`

**Not now:** observability, DR, ADRs, multi-language support, design tokens, CONTRIBUTING, CI beyond lint+test, abstractions for the second feature. If the smallest useful version doesn't need it, it isn't in v1. Come back when you have the problem.

---

## Step 4: The Playbook Layer

This is what makes it a playbook project instead of a directory:

1. **`git init`** - if it isn't a repo, nothing below survives
2. **Hand to `/pb-context`** for `todos/1-working-context.md` - `todos/` is the working-material root; pause notes land beside it later
3. **Hand to `/pb-claude-project`** for the project `.claude/CLAUDE.md`. Do this *after* step 2, not before: it reads the working context to populate its Tech Stack and Active Development sections, so an empty `todos/` gives you a hollow CLAUDE.md
4. **One CI workflow:** lint + test. That's it.
5. **First commit:** `git add -A && git commit -m "chore: initial scaffold"`. Then `/pb-start` for the first real feature.

The test for this step: **on day two, `/pb-resume` works.** It reads `todos/1-working-context.md` -- so an empty `todos/` directory fails this test. Seed the working context, or day two starts cold.

---

## Step 5: What's Next (Optional)

A personal tool needs none of this. Offer these, don't impose them -- each earns its place only when its condition is already true.

| When this is true | Hand to | Why not just later |
|---|---|---|
| It has an interface | `/pb-design-language` | Vocabulary and constraints cost less to set before the second screen than after the tenth |
| It'll be public | `/pb-repo-about` -- your Step 1 sentence is the input | The description propagates into every doc, tag, and search result |
| It publishes prose | `/pb-voice`, then `/pb-handcraft` | Only once prose exists -- two paragraphs don't have a voice yet |

Voice and positioning are discovered by building, not declared at minute three. The project's posture is already set: it's in the design rules the entry point follows, and in the sentence you wrote in Step 1.

---

## Definition of Done

- [ ] Five questions answered; the one-sentence version is written down
- [ ] Routing call stated, with its reason
- [ ] Entry point runs
- [ ] Test passes
- [ ] README says what it is and how to run it; LICENSE present if it will ever be public
- [ ] `.gitignore` covers `todos/` and `memory/`, and `.claude/` matches the solo-or-team call
- [ ] `todos/1-working-context.md` exists (via `/pb-context`) - not just an empty `todos/`
- [ ] `.claude/CLAUDE.md` exists (via `/pb-claude-project`, run *after* `/pb-context`) and isn't hollow
- [ ] `git init`, and the first commit actually contains the source: `git ls-tree -r --name-only HEAD`. `git add -A` won't warn you -- a bare `myapp` in `.gitignore` also matches `cmd/myapp/`, so root it as `/myapp`
- [ ] `/pb-resume` works in the new repo - actually run it, don't assume

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Emit a phase plan describing the repo | Write the files -- a plan is `/pb-plan`'s job |
| Hand-roll a directory tree | Use the ecosystem's initializer |
| Re-derive zero-stack's tiers, CSP, or budget math | Route to `/pb-zero-stack` in Step 2 |
| Scaffold the idea you'll have in six months | Scaffold the smallest useful version |
| Skip Step 4 because "I'll add it later" | Day-two `/pb-resume` is the whole point |
| Grow this command to cover one more topology | Topology depth belongs in a specialist, not here |

---

## Related Commands

- `/pb-zero-stack` - Static, $0/month topology (Step 2 routes here when it fits)
- `/pb-claude-project` - Generates the project CLAUDE.md (Step 4 hands off here)
- `/pb-context` - Generates the working context that day-two resume reads (Step 4 hands off here)
- `/pb-plan` - Lock scope before building, when the stakes warrant it
- `/pb-start` - Begin the first feature once the scaffold exists

---

*A sentence in, a repo out. If it emits a plan, it regressed.*
