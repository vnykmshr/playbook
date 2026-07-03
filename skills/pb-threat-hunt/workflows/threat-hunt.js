// threat-hunt.js — Executable security threat hunt workflow
//
// Drives the automated phases of /pb-threat-hunt. Stops for manual judgment
// at scoping, provider boundaries, and fix application. Human auditor owns
// the decisions; this script owns the mechanical coverage.
//
// CONVENTION: All schemas are var declarations at the top. Never inline
// schema objects in agent() calls — the workflow parser is brittle with
// inline objects and error messages are unhelpful. See plugin-dev/skills/
// command-development/references/advanced-workflows.md § JS Workflow Script Patterns.
//
// Usage: invoke via /pb-threat-hunt skill, or load this script into a
// Workflow call. The skill's SKILL.md is the entry point.
//
// Phases:
//   0. Pre-Hunt Sweeps (govulncheck, config drift, supply-chain)
//   1. Search passes (7 parallel grep patterns + hit batching)
//   2. Deep audit (payload canonicalization, header trust, CSP, tokens, parsers, concurrency)
//   3. Adversarial verify (Scope Sweep gate → 3-vote panel per finding)

export const meta = {
  name: 'threat-hunt',
  description: '12-step executable security threat hunt with automated sweep→search→audit→verify pipeline',
  phases: [
    { title: 'Pre-Hunt Sweeps' },
    { title: 'Search Passes' },
    { title: 'Deep Audit' },
    { title: 'Adversarial Verify' },
  ],
}

// --- Schema declarations (all var, never inline) ---

var PRE_HUNT_SCHEMA = {
  type: 'object',
  properties: {
    govulncheck: {
      type: 'object',
      properties: {
        ran: { type: 'boolean' },
        findings: { type: 'array', items: { type: 'string' } },
        summary: { type: 'string' },
      },
      required: ['ran', 'findings', 'summary'],
    },
    configDrift: {
      type: 'object',
      properties: {
        ran: { type: 'boolean' },
        flags: { type: 'array', items: { type: 'string' } },
        summary: { type: 'string' },
      },
      required: ['ran', 'flags', 'summary'],
    },
    supplyChain: {
      type: 'object',
      properties: {
        actionsShaPinned: { type: 'boolean' },
        goSumPresent: { type: 'boolean' },
        summary: { type: 'string' },
      },
      required: ['actionsShaPinned', 'goSumPresent', 'summary'],
    },
  },
  required: ['govulncheck', 'configDrift', 'supplyChain'],
}

var SEARCH_HIT_SCHEMA = {
  type: 'object',
  properties: {
    passName: { type: 'string' },
    file: { type: 'string' },
    line: { type: 'number' },
    match: { type: 'string' },
    initialAssessment: {
      type: 'string',
      enum: ['needs-review', 'likely-safe', 'unknown'],
    },
  },
  required: ['passName', 'file', 'line', 'match', 'initialAssessment'],
}

var DEEP_AUDIT_FINDING = {
  type: 'object',
  properties: {
    title: { type: 'string' },
    severity: {
      type: 'string',
      enum: ['Critical', 'High', 'Medium', 'Low', 'Info'],
    },
    location: { type: 'string' },
    inputVector: { type: 'string' },
    decisionPath: { type: 'string' },
    exploitScenario: { type: 'string' },
    currentMitigation: { type: 'string' },
    recommendedFix: { type: 'string' },
  },
  required: ['title', 'severity', 'location', 'decisionPath', 'exploitScenario'],
}

var SCOPE_SWEEP_SCHEMA = {
  type: 'object',
  properties: {
    acceptedRisks: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          description: { type: 'string' },
          source: { type: 'string' },
        },
        required: ['description', 'source'],
      },
    },
    preFilteredFindings: {
      type: 'array',
      items: { type: 'string' },
    },
    summary: { type: 'string' },
  },
  required: ['acceptedRisks', 'preFilteredFindings', 'summary'],
}

var VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    finding: { type: 'string' },
    outcome: {
      type: 'string',
      enum: ['Confirmed', 'Likely', 'Possible', 'Needs investigation', 'False positive', 'Unknown'],
    },
    reasoning: { type: 'string' },
    isReal: { type: 'boolean' },
  },
  required: ['finding', 'outcome', 'reasoning', 'isReal'],
}

// --- Phase 0: Pre-Hunt Sweeps ---

phase('Pre-Hunt Sweeps')

const preHunt = await agent(
  'Run the three Pre-Hunt Sweeps on this codebase:\n' +
  '1. govulncheck ./... — known CVEs in Go dependencies\n' +
  '2. Config drift — diff .env.example vs actual .env for DEBUG=true, ENVIRONMENT=development, default credentials\n' +
  '3. Supply-chain integrity — are CI actions SHA-pinned? Is go.sum committed?\n\n' +
  'Use ripgrep for the grep checks. Report each sweep result separately.\n' +
  'Do NOT skip govulncheck even if dependencies "look up to date."',
  { label: 'pre-hunt-sweeps', schema: PRE_HUNT_SCHEMA }
)

if (preHunt) {
  log(`govulncheck: ${preHunt.govulncheck.findings.length} findings`)
  log(`config drift flags: ${preHunt.configDrift.flags.join(', ') || 'none'}`)
  log(`supply-chain: SHA-pinned=${preHunt.supplyChain.actionsShaPinned}, go.sum=${preHunt.supplyChain.goSumPresent}`)
}

// --- Phase 1: Search Passes ---

phase('Search Passes')

var SEARCH_PASSES = [
  {
    name: 'url-path',
    pattern: 'url\\.Parse|path\\.Join|filepath\\.Join|path\\.Clean|fmt\\.Sprintf.*/%s|http\\.Redirect',
    label: 'URL and path manipulation',
  },
  {
    name: 'token-cookie-session',
    pattern: 'ParseWithClaims|jwt\\.Sign|jwt\\.NewWithClaims|jwt\\.Parse|SetCookie|cookie\\.Set|http\\.Cookie',
    label: 'Token, cookie, and session handling',
  },
  {
    name: 'parsing-deserialization',
    pattern: 'json\\.Unmarshal|xml\\.Unmarshal|gob\\.NewDecoder|\\.\\(\\w+\\)|fmt\\.Sscanf|strconv\\.Atoi|strconv\\.Parse|template\\.Must',
    label: 'Parsing and deserialization',
  },
  {
    name: 'crypto',
    pattern: 'md5\\.Sum|md5\\.New|sha1\\.Sum|sha1\\.New|crypto/aes|crypto/rsa|ecdsa\\.|hmac\\.|rand\\.Read|crypto/rand',
    label: 'Cryptographic operations',
  },
  {
    name: 'concurrency-race',
    pattern: 'go func|sync\\.Mutex|sync\\.RWMutex|sync\\.Map|chan\\b|<-chan|chan<-|chan\\)|chan\\{|sync\\.Once|sync\\.WaitGroup',
    label: 'Concurrency and potential races',
  },
  {
    name: 'dangerous-stdlib',
    pattern: 'exec\\.Command|os/exec|net/http\\.Get|reflect\\.|unsafe\\.',
    label: 'Dangerous standard library usage',
  },
  {
    name: 'websocket-sse',
    pattern: 'websocket|gorilla/websocket|nhooyr\\.io/websocket|sse|ServerSentEvent|EventSource',
    label: 'WebSocket and SSE real-time channels',
  },
]

// Run all 7 search passes in parallel
const searchResults = await parallel(
  SEARCH_PASSES.map(pass => () =>
    agent(
      `Search the codebase with ripgrep for this pattern:\n` +
      `  ${pass.pattern}\n\n` +
      `This is the "${pass.label}" pass of a security threat hunt.\n` +
      `For each hit, classify: needs-review (in a security boundary), likely-safe (test file, benchmark, non-security context), or unknown.\n\n` +
      `Minimum output: list every hit with file, line number, match text, and initial assessment.\n` +
      `A 3-line output is a FAILED pass — you are missing hits. Review ALL matches.`,
      { label: `search:${pass.name}`, schema: { type: 'object', properties: { hits: { type: 'array', items: SEARCH_HIT_SCHEMA } }, required: ['hits'] } }
    )
  )
)

// Batch all hits for deep audit
const allHits = searchResults.filter(Boolean).flatMap(r => r.hits)
const reviewHits = allHits.filter(h => h.initialAssessment !== 'likely-safe')

log(`${allHits.length} total hits, ${reviewHits.length} flagged for deep audit`)

// Step-completion enforcement: reject shallow passes
for (let i = 0; i < searchResults.length; i++) {
  const r = searchResults[i]
  if (r && r.hits.length < 3) {
    log(`WARN: ${SEARCH_PASSES[i].label} returned only ${r.hits.length} hits — may be incomplete`)
  }
}

// --- Phase 2: Deep Audit ---

phase('Deep Audit')

// Group hits by vulnerability class for focused deep-audit agents
var AUDIT_GROUPS = [
  {
    name: 'url-canonicalization',
    label: 'URL/path canonicalization and redirect safety',
    hitFilter: h => ['url-path'].includes(h.passName),
    prompt: 'Audit every URL/path hit for canonicalization vulnerabilities. For each input point, test against all 16 adversarial payloads from the threat hunt methodology (path traversal variants, open redirect forms, SSRF targets including DNS rebinding via nip.io). Classify each finding with severity and write a concrete exploit scenario.',
  },
  {
    name: 'header-trust-csp',
    label: 'Header trust, CSP, and redirect validation',
    hitFilter: h => ['url-path', 'token-cookie-session'].includes(h.passName),
    prompt: 'Audit header trust and redirect targets. For forwarded headers (X-Forwarded-For, X-Real-IP, etc.), verify they are not used in security decisions without explicit trust boundary documentation. Evaluate CSP against 3 questions (inline script? script-src origins? unsafe-eval?). Check every redirect_uri against an allowlist.',
  },
  {
    name: 'token-auth',
    label: 'Token, cookie, session, and auth boundaries',
    hitFilter: h => ['token-cookie-session', 'crypto', 'websocket-sse'].includes(h.passName),
    prompt: 'Audit token handling end-to-end. Verify JWT algorithm pinning (not header-controlled), cookie HttpOnly/Secure/SameSite flags, session ID randomness and regeneration on login. Check WebSocket/SSE auth boundaries: are upgrade requests authenticated? Are tokens validated per-message?',
  },
  {
    name: 'parser-dos-concurrency',
    label: 'Parser, DoS, panic, and concurrency boundaries',
    hitFilter: h => ['parsing-deserialization', 'concurrency-race', 'dangerous-stdlib'].includes(h.passName),
    prompt: 'Audit parsing and concurrency safety. Flag every io.ReadAll without size limit at a network boundary. Check json.NewDecoder usage without http.MaxBytesReader. Verify goroutines have cancellation paths. Check mutex defer-unlock patterns. Flag every user-controlled template.Execute.',
  },
]

// Run deep audits in parallel — each agent reads focused files, no cross-contamination
const auditResults = await parallel(
  AUDIT_GROUPS.map(group => () => {
    const groupHits = reviewHits.filter(group.hitFilter)
    if (groupHits.length === 0) {
      log(`No hits for ${group.name} — skipping`)
      return { findings: [] }
    }
    const hitList = groupHits.map(h => `${h.file}:${h.line} — ${h.match}`).join('\n')
    return agent(
      `${group.prompt}\n\n` +
      `Here are the grep hits to investigate:\n${hitList}\n\n` +
      `For each confirmed or likely finding, provide: title, severity (Critical/High/Medium/Low/Info), location (file:line), input vector, decision path, exploit scenario, current mitigation if any, and recommended fix.\n\n` +
      `Grep hits are clues, not conclusions — verify by reading the code. A hit may be safe. State why if you classify as false positive.`,
      { label: `audit:${group.name}`, schema: { type: 'object', properties: { findings: { type: 'array', items: DEEP_AUDIT_FINDING } }, required: ['findings'] } }
    )
  })
)

const allFindings = auditResults.filter(Boolean).flatMap(r => r.findings)
log(`${allFindings.length} findings from deep audit`)

// Step-completion enforcement
if (allFindings.length === 0 && reviewHits.length > 0) {
  log('WARN: deep audit produced zero findings from non-zero review hits — possible completeness gap')
}

// --- Phase 3: Adversarial Verify ---

phase('Adversarial Verify')

if (allFindings.length > 0) {
  // Scope Sweep gate — run first
  const scopeSweep = await agent(
    'Read the project\'s security documentation (docs/security.md, threat model if present, CLAUDE.md security boundaries, SECURITY.md).\n' +
    'For each finding listed below, check if the claimed vulnerability is already an accepted risk in these docs.\n' +
    'Flag any finding whose vulnerability is a documented accepted risk — we should not waste verification time on it.\n\n' +
    'Findings to sweep:\n' +
    allFindings.map((f, i) => `${i + 1}. [${f.severity}] ${f.title} — ${f.location}`).join('\n'),
    { label: 'scope-sweep', schema: SCOPE_SWEEP_SCHEMA }
  )

  // Remove pre-filtered findings
  var preFiltered = new Set(scopeSweep?.preFilteredFindings || [])
  var verifyFindings = allFindings.filter((_, i) => !preFiltered.has(`${i + 1}`))
  log(`Scope Sweep: ${preFiltered.size} findings pre-filtered (already accepted risks), ${verifyFindings.length} remaining for verification`)

  // 3-vote adversarial verify per finding
  const verified = await pipeline(
    verifyFindings,
    finding => {
      const findingText = `[${finding.severity}] ${finding.title}\n` +
        `Location: ${finding.location}\n` +
        `Input: ${finding.inputVector}\n` +
        `Decision path: ${finding.decisionPath}\n` +
        `Exploit scenario: ${finding.exploitScenario}`

      return parallel([
        // Skeptic 1: threat-model reader
        () => agent(
          `Read the project's security/threat-model documentation first, then evaluate this finding:\n\n${findingText}\n\n` +
          `Does this finding represent a real vulnerability given the project's stated threat model and security boundaries? Default to refuted (isReal=false) if the threat model already addresses this class of issue.`,
          { label: `verify:tm`, schema: VERDICT_SCHEMA }
        ),
        // Skeptic 2: exploit-chain tracer
        () => agent(
          `Trace the exploit chain from input to sink for this finding. Verify each hop:\n\n${findingText}\n\n` +
          `Can an attacker actually reach the sink from the input? Is there a missing validation at any hop? Is there a compensating control earlier in the chain? Default to refuted if any hop in the chain is not exploitable.`,
          { label: `verify:chain`, schema: VERDICT_SCHEMA }
        ),
        // Skeptic 3: fix-site checker
        () => agent(
          `Read the proposed fix site and check if the vulnerability is already mitigated elsewhere:\n\n${findingText}\n\n` +
          `Is there an existing mitigation (middleware, gateway, framework-level protection) that already covers this? Is the attack even possible given the deployment architecture? Default to refuted if already mitigated.`,
          { label: `verify:fix`, schema: VERDICT_SCHEMA }
        ),
      ])
    },
    // Kill if ≥2 refute
    votes => {
      const validVotes = votes.filter(Boolean)
      const refuteCount = validVotes.filter(v => !v.isReal).length
      const survived = refuteCount < 2
      return {
        finding: validVotes[0]?.finding,
        votes: validVotes.map(v => ({ outcome: v.outcome, reasoning: v.reasoning, isReal: v.isReal })),
        survived,
        refuteCount,
      }
    }
  )

  const confirmed = verified.filter(Boolean).filter(v => v.survived)
  const killed = verified.filter(Boolean).filter(v => !v.survived)

  log(`Verification complete: ${confirmed.length} survived, ${killed.length} killed (≥2 refute)`)
  log('')
  log('=== CONFIRMED FINDINGS ===')
  for (const c of confirmed) {
    log(`  ${c.finding} (${c.votes.filter(v => v.isReal).length}/3 confirmed)`)
  }
  if (killed.length > 0) {
    log('')
    log('=== KILLED FINDINGS (≥2 refute) ===')
    for (const k of killed) {
      log(`  ${k.finding} (${k.refuteCount}/3 refuted)`)
    }
  }
  log('')
  log('Manual steps remaining: Step 11 (report per-finding with 7-field template) and Step 12 (fix conservatively with regression tests).')
  log('Provider boundaries (Step 8) require manual judgment — OAuth, SAML, LDAP, KMS, DB.')
} else {
  log('No findings to verify.')
}

log('')
log('Threat hunt automated phases complete.')
log('Next: write the report (Step 11) and apply fixes with regression tests (Step 12).')
