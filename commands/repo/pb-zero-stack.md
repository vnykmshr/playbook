---
name: "pb-zero-stack"
title: "Zero-Stack App Initiation ($0/month Architecture)"
category: "repo"
difficulty: "intermediate"
model_hint: "sonnet"
execution_pattern: "interactive"
related_commands: ['pb-repo-init', 'pb-start', 'pb-patterns-cloud', 'pb-design-language']
last_reviewed: "2026-02-22"
last_evolved: ""
version: "1.0.0"
version_notes: "Initial release — extracted from production zero-cost app (N=1), validated architecture"
breaking_changes: []
---
# Zero-Stack App Initiation ($0/month Architecture)

A thinking tool for building apps that run themselves. Takes an idea and walks through the decisions that turn it into a zero-stack app — static site, edge API proxy, CI pipeline. Two vendor accounts. Zero servers. Zero monthly cost. Only fixed cost: domain registration (~$10-15/year) if you want a custom domain — the `*.pages.dev` default is free.

A structured conversation that produces architecture decisions, budget validation, and a tailored project scaffold — not a generic template you fork and gut.

**Mindset:** Apply `/pb-preamble` thinking — challenge whether the idea fits this topology before committing to it. Apply `/pb-design-rules` thinking — the topology is simple by default, modular, and fails noisily.

**Resource Hint:** sonnet — scaffolding follows established patterns; architecture decisions are guided, not open-ended

---

## When to Use

- Building a read-heavy, API-backed app with public data
- Side project that should cost $0/month to run
- Want production architecture without production ops burden
- Starting from an idea, not a template

## When NOT to Use

- User-generated content, file uploads, or auth required — use `/pb-repo-init`
- Real-time collaboration or WebSocket-heavy — use `/pb-repo-init` + `/pb-patterns-async`
- Relational data or complex queries — use `/pb-repo-init` + `/pb-patterns-db`
- SSR required — this topology serves static files at the edge

If the idea doesn't fit, redirect early. Don't force the topology.

---

## The Non-Negotiable Topology

Every zero-stack app has the same shape:

```
┌──────────────┐    ┌──────────────────┐    ┌──────────────┐
│  Static Site │    │  Edge API Proxy   │    │  CI Pipeline │
│  (CF Pages)  │◄──►│  (CF Worker + KV) │    │  (GH Actions)│
└──────────────┘    └──────────────────┘    └──────────────┘
       │                     │                      │
       └─────────────────────┴──────────────────────┘
                    Two vendor accounts
                  (Cloudflare + GitHub)
```

This is what makes it a pattern, not a collection of choices. The topology is fixed. Choices within it are flexible.

---

## Phase A: Shape (One Session)

Goal: idea to working local dev with mock data. No accounts needed.

### Step 1: Validate Fit

Ask the user to describe their idea in one sentence, then run through the fit checklist:

```
What are you building? (one sentence)
> ___

Fit checklist:
  ✓ Read-heavy? (users consume data, not create it)
  ✓ Public data? (no user auth required)
  ✓ API-backed? (data comes from an external API)
  ✓ Low write frequency? (updates hourly or less, not per-request)
```

**All four checked:** proceed to Step 2.
**Three of four?** Describe the exception. Some near-misses work with minor adaptations — a contact form can POST to a Worker that writes to KV, optional auth can use CF Access, static data sources just skip the proxy. If the adaptation is small, proceed. If it reshapes the architecture, redirect.
**Two or fewer:** redirect to `/pb-repo-init` or `/pb-plan`. Don't force the topology.

### Step 2: Data Architecture

Walk through these decisions. Each one shapes the scaffold.

**Data source:**

- What API(s) are you pulling from?
- Free tier limits? (daily request cap, rate limits)
- Auth method? API key is fine. OAuth means this probably isn't zero-stack.

**Update frequency:**

- How often does the data change? (real-time, hourly, daily)
- What freshness do users expect?
- This determines which data paths to use:

| Freshness Need | Data Path | Implementation |
|---------------|-----------|----------------|
| Minutes | Live Worker proxy | Worker fetches on request, caches in KV |
| Hours | Cron + Worker | GitHub Actions cron writes to KV, Worker serves from KV on request |
| Daily | Cron + rebuild | GitHub Actions cron fetches data and triggers a Pages rebuild with data baked into static HTML |

**Active window:**

- Usage pattern: global (24h) or regional (e.g., 14h active window)?
- This drives budget math — fewer active hours = fewer API hits

**Budget math** (calculate for the user):

```
API hits/day = (active_hours * 60 / kv_ttl_minutes) + cron_runs
```

Show the result against free tier headroom:

| Resource | Free Tier | This App | Headroom |
|----------|-----------|----------|----------|
| Workers requests | 100K/day | [calculated] | [remaining] |
| KV reads | 100K/day | [calculated] | [remaining] |
| KV writes | 1K/day | [calculated] | [remaining] |
| Pages builds | 500/month | [calculated] | [remaining] |
| GH Actions | 2K min/month | [calculated] | [remaining] |

> **Sharing a CF account across apps?** KV writes (1K/day) are shared across all apps on the account. Divide the limit by your app count.

**What happens when you exceed free tier:** Workers requests beyond 100K/day return 1015 errors (visible). KV reads beyond 100K/day return errors (visible). KV writes beyond 1K/day silently fail — this is the dangerous one, your cron updates stop landing and you won't know unless you check. Pages builds beyond 500/month queue and may time out.

**Production lessons to surface in this step:**

- Two-tier cache (edge response cache + KV storage) prevents thundering herd across Cloudflare's 200+ PoPs. Set edge TTL shorter than KV TTL — edge serves stale while one PoP refreshes from KV.
- Set `expirationTtl` on every KV put. Without it, stale entries live forever if your cron stops or your key format changes.
- Cloudflare WAF rate limiting is a paid feature. Don't investigate it — the built-in cache layers are sufficient for read-heavy patterns.
- Validate API response shape before caching. If the upstream API changes its schema, you want to fail at write time, not serve corrupt cached data.

### Step 3: Project Shape

**Basics:**

- Project name (lowercase, hyphenated)
- Single page or multi-page? (default: single, grow later)
- Primary display: dashboard, ticker, list, map, or other?
- PWA with service worker? (default: yes — offline shows stale data with timestamp)

**Design choices** (two decisions, not a design system):

| Choice | Options | Default |
|--------|---------|---------|
| Palette direction | warm / cool / mono | mono |
| Font vibe | system / geometric / humanist | system |

These produce a `design-tokens.css` in the scaffold. For deeper design work, run `/pb-design-language` after scaffolding.

### Step 4: Stack Confirmation

Show the default stack with rationale. Allow substitutions but warn about cascading effects.

| Layer | Default | Why | Substitution Notes |
|-------|---------|-----|--------------------|
| SSG | Astro | Islands architecture, zero JS by default | Hugo if no JS needed at all |
| Islands | Preact | 3KB, React-compatible API | Svelte if team prefers; vanilla JS if minimal |
| CSS | Tailwind v4 | Zero-config Vite plugin | Vanilla CSS if app is small |
| Host | CF Pages | Free, atomic deploys, edge network | Vercel if already invested (changes proxy layer too) |
| Proxy | CF Worker | Same vendor as Pages, KV built-in | Vercel Edge if Pages moved to Vercel |
| Cache | CF KV | Global, free 100K reads/day | Upstash if on different host |
| CI | GitHub Actions | Native git integration, cron support | GitLab CI if repo lives there |

The default stack is chosen as a unit — single vendor for hosting means one API token, one dashboard, one set of docs. Substituting one piece may cascade. Flag this clearly:

> Changing the host from CF Pages also changes the proxy, cache, and deployment story. That's fine if you're already on Vercel — just know it's a package deal.

Confirm or adjust, then proceed.

### Step 5: Scaffold

Generate project files with the decisions from Steps 2-4 baked in. The scaffold must work immediately with mock data — no Cloudflare account needed.

The structure below is representative — the actual scaffold adapts to the conversation. No `normalizer.ts` if the API has a stable schema. No `data-cron.yml` if the data path is live-only. The command shapes the files, not the other way around.

**Representative structure:**

```
project-name/
├── src/
│   ├── pages/              # Astro pages
│   ├── components/         # Preact islands
│   ├── styles/
│   │   └── design-tokens.css  # From Step 3 choices
│   └── lib/
│       └── api.ts          # Data fetching (uses mock in dev)
├── worker/
│   ├── index.ts            # Edge proxy
│   ├── cache.ts            # KV cache with TTLs from Step 2
│   └── normalizer.ts       # Response shape validation
├── .github/
│   └── workflows/
│       ├── ci.yml          # Lint + type check + test
│       ├── deploy.yml      # Pages + Worker deploy
│       └── data-cron.yml   # (if cron path chosen in Step 2)
├── docs/
│   └── setup.md            # Bootstrap checklist (Phase B)
├── mock/
│   └── data.json           # Mock API response for local dev
├── wrangler.toml           # Worker config with TTLs, bindings
├── astro.config.mjs
├── package.json
├── tsconfig.json
└── README.md
```

**Production lessons baked into the scaffold:**

- `wrangler.toml`: no `[env.dev.vars]` section — it causes interactive prompts in CI. Use `.dev.vars` file locally instead.
- `deploy.yml`: content-hash comparison to skip no-change deploys. Never deploy locally with dev config — CI is the only deploy path.
- `worker/index.ts`: accepts both GET and HEAD requests. Uptime monitors send HEAD; returning 405 looks like downtime.
- `ci.yml` and `deploy.yml` are separate workflows. Push doesn't automatically deploy — release-gated deploys mean push != ship.

**First run:**

```bash
npm install && npm run dev
```

Pages render with mock data. Islands hydrate. Fallback chain works (live → cached → mock). Ready for real API integration.

---

## Phase B: Deploy (When Ready)

Goal: scaffold to production. Human-paced, no rush.

### Step 6: Bootstrap Checklist

Generate `docs/setup.md` with paste-able commands. Each step is one command with expected output.

```markdown
## One-Time Setup (~30 minutes)

### 1. Cloudflare Account
- Sign up at dash.cloudflare.com (free plan)
- Install Wrangler: `npm install -g wrangler`
- Login: `wrangler login`
  Expected: browser opens, authorize, "Successfully logged in"

### 2. KV Namespace
- Create: `wrangler kv namespace create "CACHE"`
  Expected: prints namespace ID
- Create preview: `wrangler kv namespace create "CACHE" --preview`
  Expected: prints preview namespace ID
- Update wrangler.toml with both IDs

### 3. API Secrets (if your data source needs an API key)
- Set secret: `wrangler secret put API_KEY`
  Expected: prompts for value, confirms "Success"
- Add to GitHub: repo Settings → Secrets → `CF_API_TOKEN`
  (Create token at dash.cloudflare.com/profile/api-tokens)

### 4. GitHub Actions
- Enable Actions in repo Settings → Actions → General
- Add secrets: `CF_API_TOKEN`, `CF_ACCOUNT_ID`

### 5. DNS (optional — skip for *.pages.dev default)
- Custom domain: Pages → Custom domains → Add
- CNAME subdomain (easy) or apex (needs registrar redirect)
```

### Step 7: First Deploy

```bash
git push origin main
```

CI runs. Pages deploy. Worker deploy. Verify:

- Pages serve at `project-name.pages.dev`
- Worker proxies at `project-name.workers.dev/api/...`
- Cron runs on schedule (if applicable)
- `/health` returns 200 on both GET and HEAD

---

## Stack Rationale (Reference)

Why these defaults as a unit:

**Cloudflare (Pages + Workers + KV):** Single vendor means one authentication flow, one dashboard, one billing page (free), and same-origin advantage between Pages and Workers. KV is globally replicated with no configuration.

**Astro:** Islands architecture means zero JavaScript ships by default. Interactive components hydrate individually. Perfect for read-heavy dashboards where most content is static.

**GitHub Actions:** Native cron for data refresh. Same platform as the repo. Free tier (2K minutes/month) is generous for CI + scheduled data fetches.

**The unit matters more than any piece.** Swapping one component is fine if you swap its dependencies too. The command warns about cascading changes.

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Force-fit an idea that needs auth | Redirect to `/pb-repo-init` in Step 1 |
| Skip budget math | Calculate it — free tier surprise is the #1 failure mode |
| Deploy before local dev works | Phase A must complete before Phase B |
| Use `[env.dev.vars]` in wrangler.toml | Use `.dev.vars` file (not committed) |
| Deploy from local machine | CI is the only deploy path |
| Set up CF account before writing code | Scaffold works with mocks — deploy when ready |
| Build a framework or CLI tool | This is a thinking tool that produces a scaffold |

---

## Related Commands

- `/pb-repo-init` — Generic greenfield initiation (when zero-stack doesn't fit)
- `/pb-start` — Begin feature work after scaffolding
- `/pb-patterns-cloud` — Cloud deployment patterns reference
- `/pb-design-language` — Deeper design system work (optional, after scaffold)

---

*Opinionated about topology. Flexible about content. $0/month is a feature, not a constraint.*
