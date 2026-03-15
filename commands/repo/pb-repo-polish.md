---
name: "pb-repo-polish"
title: "Repository AI Discoverability Audit"
category: "repo"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "sequential"
related_commands: ['pb-repo-enhance', 'pb-repo-about', 'pb-repo-readme', 'pb-repo-organize']
last_reviewed: "2026-03-01"
last_evolved: "2026-03-01"
version: "1.0.0"
version_notes: "Initial release"
breaking_changes: []
---
# Repository AI Discoverability Audit

Audit a repository's visibility to AI coding agents and developer search.

**Mindset:** AI agents are becoming the primary way developers discover libraries. A functionally strong library that scores poorly on machine-readable signals will never get recommended. This command measures the gap between code quality and discoverability -- and surfaces what polish can fix vs. what requires usage evidence that polish alone cannot create.

**Resource Hint:** sonnet -- structured audit with concrete rubrics, optional content drafting

---

## When to Use

- Before publishing or promoting a library
- Periodic audit of existing public repositories
- After `/pb-repo-enhance` to measure remaining discoverability gaps
- When a library has low adoption despite solid code
- Fleet-wide audit across an org (`--status` mode)

---

## Objective

Produce a scorecard measuring how well a repository converts when discovered by AI agents or developer search. Five scored dimensions (0-3 each, max 15) plus an informational usage evidence section that honestly surfaces what polish cannot fix.

---

## Invocations

```
/pb-repo-polish owner/repo           Full audit: scorecard + action items
/pb-repo-polish owner/repo --draft   Audit + generate content drafts (llms.txt, README sections)
/pb-repo-polish --status             Fleet view: which repos polished, scores
```

---

## Review Checklist

### Dimension 1: Search Term Alignment (0-3)

Does the description, README, and topics contain the words developers actually search?

| Score | Criteria |
|-------|----------|
| 0 | Description is generic or missing ("A Go library") |
| 1 | Description names the category ("circuit breaker for Go") |
| 2 | Description + README first line contain likely search terms |
| 3 | Description + README + topics all hit the search terms a developer would use |

**How to assess:** Think about what a developer would type into Google, pkg.go.dev, npm, or ask an AI agent. Compare those terms against the repo's description, README opening paragraph, and GitHub topics. Misalignment here is the highest-ROI fix for small libraries.

### Dimension 2: README Machine-Readability (0-3)

Can an AI agent extract what this library does, how to install it, and when to use it from the README alone?

| Score | Criteria |
|-------|----------|
| 0 | No README or stub |
| 1 | Has description and install command |
| 2 | Above + working example with imports within first 60 lines |
| 3 | Above + "when to use this" section and standalone first paragraph |

**How to assess:** Read the README as if you have zero context. Can you answer: what does it do, how do I install it, show me an example, when should I use this vs. alternatives? Each missing answer costs a point.

### Dimension 3: Registry Presence (0-3)

Is the library findable and current on the expected package registry?

| Score | Criteria |
|-------|----------|
| 0 | Not on expected registry |
| 1 | Published but stale (local version ahead) or module path issue |
| 2 | Published, current, but no importers/downloads visible |
| 3 | Published, current, correct path, visible on registry search |

**How to assess:**
- Go: check `pkg.go.dev/{module}` -- is it indexed? Is the latest version shown? Is the module path correct (especially `/v2` suffixes)?
- Node: check `npmjs.com/package/{name}` -- is it published? Is the latest version current?
- Other: check the language-appropriate registry

### Dimension 4: Metadata Completeness (0-3)

Does GitHub metadata make the repo discoverable and credible at a glance?

| Score | Criteria |
|-------|----------|
| 0 | No description or topics |
| 1 | Description exists, <3 topics |
| 2 | Description + 3-4 topics + license |
| 3 | Keyword-rich description + 5+ relevant topics + license + homepage |

**How to assess:** Run `gh repo view owner/repo --json description,repositoryTopics,licenseInfo,homepageUrl` and evaluate against the rubric. Topics should include the language, the problem domain, and the specific technique.

### Dimension 5: Examples Quality (0-3)

Can a developer copy-paste a working example without reading the full source?

| Score | Criteria |
|-------|----------|
| 0 | No examples anywhere |
| 1 | README has inline examples but no `examples/` directory |
| 2 | `examples/` dir exists with 1+ example |
| 3 | `examples/` dir with 3+ problem-oriented examples, all runnable with imports |

**How to assess:** Check for `examples/` directory. If it exists, verify examples compile/run and have complete import statements. Problem-oriented means each example solves a specific use case, not just "basic usage."

### Dimension 6: Usage Evidence (informational, not scored)

Surface the signals that polish cannot create. This section is honest about what metadata improvements can and cannot do.

**What to check:**
- Dependents count (pkg.go.dev "Imported by" or npm dependents)
- Download stats (npm weekly downloads)
- External references (blog posts, Stack Overflow mentions, conference talks)
- Stars and forks (weak signal but still signal)

---

## Scoring

**Max score: 15** (5 dimensions x 3 points each)

| Tier | Score | Meaning |
|------|-------|---------|
| Ship-ready | 13-15 | Metadata is strong. Focus shifts to usage evidence. |
| Functional but invisible | 9-12 | Code works, but AI agents and search won't find or recommend it. |
| Significant gaps | 5-8 | Missing basics. Fix before any promotion effort. |
| Not ready | 0-4 | Needs `/pb-repo-enhance` first. |

---

## Deliverables

### Scorecard (always produced)

```
## AI Discoverability Scorecard: {owner}/{repo}

| # | Dimension | Score | Notes |
|---|-----------|-------|-------|
| 1 | Search Term Alignment | X/3 | {specific finding} |
| 2 | README Machine-Readability | X/3 | {specific finding} |
| 3 | Registry Presence | X/3 | {specific finding} |
| 4 | Metadata Completeness | X/3 | {specific finding} |
| 5 | Examples Quality | X/3 | {specific finding} |
|   | **Total** | **X/15** | **{tier}** |

## Usage Evidence

Dependents: N (pkg.go.dev) / N (npm)
Downloads: ~N/week (npm only)
External references: {found or "none found"}

Note: Metadata polish improves conversion but not discovery.
For this repo to be recommended by AI agents, it needs usage
evidence: blog posts, SO answers, or dependents that reference it.
```

### Action Items (always produced)

Ordered by impact. Each item is concrete and actionable:

```
## Action Items (ordered by impact)

1. **[Dim X]** {Specific action} - {why this moves the score}
2. **[Dim X]** {Specific action} - {why this moves the score}
...
```

### Content Drafts (--draft flag only)

When `--draft` is passed, produce these after the scorecard:

**1. llms.txt draft** (P2 -- experimental format, not widely consumed yet):

```
# {name}
> {one-line from description}

## What it does
{2-3 sentences}

## Install
{install command}

## Quick start
{minimal working example}

## API
{key functions/types}

## When to use this
{use cases}

## When NOT to use this
{anti-use-cases, alternatives}
```

**2. README "When to use this" section** -- comparison anchor against the dominant alternative. Format:

```markdown
## When to Use This

Use {name} when you need {specific scenario}.

**Choose {name} over {alternative} when:**
- {differentiator 1}
- {differentiator 2}

**Choose {alternative} instead when:**
- {scenario where alternative wins}
```

**3. Description improvement** -- if search terms are missing from the current description, draft a better one (max 160 chars).

**4. Metadata fix commands** -- exact `gh repo edit` commands:

```bash
gh repo edit owner/repo --description "new description"
gh repo edit owner/repo --add-topic topic1 --add-topic topic2
```

### Fleet View (--status mode)

```
## AI Discoverability Status: {org}

| Repo | Score | Tier | Last Audited | Top Gap |
|------|-------|------|-------------|---------|
| repo-1 | 12/15 | Functional | 2026-03-01 | Examples |
| repo-2 | 8/15 | Gaps | 2026-02-15 | Search terms |
| repo-3 | -- | Not audited | -- | -- |
```

---

## Process

### Step 1: Gather Data

```bash
# Repository metadata
gh repo view owner/repo --json description,repositoryTopics,licenseInfo,homepageUrl

# README content
gh api repos/owner/repo/readme --jq '.content' | base64 -d

# Check for examples directory
gh api repos/owner/repo/contents/examples 2>/dev/null

# Registry check (Go)
# Visit pkg.go.dev/{module-path}

# Registry check (Node)
# Visit npmjs.com/package/{name}
```

### Step 2: Score Each Dimension

Walk through each dimension's rubric. Be precise -- score what exists, not what could exist.

### Step 3: Identify Search Terms

Think like a developer searching for this type of library:
- What problem are they solving?
- What words would they type?
- Compare against description, README first paragraph, and topics

### Step 4: Produce Scorecard + Action Items

Use the deliverable templates above. Action items ordered by score impact (biggest gaps first).

### Step 5: Draft Content (--draft only)

Generate llms.txt, "When to use this" section, improved description, and `gh repo edit` commands.

---

## Anti-Patterns to Avoid

| Problem | Solution |
|---------|----------|
| Scoring on vibes | Use the rubric criteria exactly |
| Inflating scores to be nice | A 2 is not a 3. Be honest. |
| Pretending polish fixes adoption | Usage evidence section exists for this reason |
| Auditing project health (CI, tests) | That's `/pb-review-hygiene` territory |
| Writing final content in audit mode | Audit scores and suggests. `--draft` generates. |
| Generic action items ("improve README") | Be specific: "Add install command before line 20" |

---

## Related Commands

- `/pb-repo-enhance` -- Full repository polish (organize + docs + presentation)
- `/pb-repo-about` -- Generate GitHub About section + tags
- `/pb-repo-readme` -- Write or rewrite project README
- `/pb-repo-organize` -- Clean up project root structure

---

*Discoverable repo, discoverable library.*
