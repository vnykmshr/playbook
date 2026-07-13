---
name: pb-threat-hunt
description: 12-step executable security threat hunt with automated sweep→grep→audit→verify pipeline. Uses workflow automation for mechanical steps (Pre-Hunt Sweeps, search passes, 3-vote adversarial verify) and stops for manual judgment (scoping, provider boundaries, fix application). Go default + Python/Node appendices.
---

# Security Threat Hunt: Deep Audit Methodology

A 12-step executable security audit that treats every auth shortcut, redirect, token source, cookie, forwarded header, parser, cache, and cryptographic decision as a security boundary until proven otherwise. The default answer to "is this safe?" is "prove it."

**Mindset:** Apply `/pb-preamble` thinking (challenge every safety assumption) and `/pb-design-rules` thinking (fail noisily, distrust "one true way," recovery-oriented errors). The hunt is adversarial by design.

**Resource Hint:** opus - deep audit requires tracing decision paths end-to-end, evaluating cryptographic boundaries, and validating findings against exploit scenarios.

**Language:** This methodology targets **Go** projects by default. For Python equivalents, see `references/methodology.md` Appendix A. For Node, see Appendix B.

---

## When to Use This Command

- **Deep security audit** - full methodology, every step executed
- **Pre-release security gate** - for L-tier changes touching auth, crypto, or input parsing
- **Post-incident review** - hunt the vulnerability class that caused the incident across the codebase
- **Dependency boundary audit** - when integrating a new auth provider, payment processor, or identity system

For quick pre-release checks, use `/pb-security`. This command is the deep pass.

---

## Severity Rubric

| Level | Criteria |
|-------|----------|
| **Critical** | Remote code execution, authentication bypass, credential exfiltration, privilege escalation to admin |
| **High** | Data exfiltration (non-credential), token forgery, SSRF to internal services, broken access control on sensitive data |
| **Medium** | Information disclosure (non-sensitive), open redirect, DoS with restart requirement, debug info leak |
| **Low** | Configuration weakness (no direct exploit), missing security headers (defense-in-depth), verbose error messages |
| **Info** | Hardening opportunity (no vulnerability), code pattern that could become exploitable with future changes |

---

## How This Skill Runs

The hunt splits into workflow-automated phases and manual-judgment steps:

| Automated (workflow drives) | Manual (you decide) |
|-----------------------------|---------------------|
| Pre-Hunt Sweeps (govulncheck, config drift, supply-chain) | Step 1: Scope the hunt |
| Step 3: Targeted search passes (7 parallel greps) | Step 2: Map decision paths |
| Step 4: URL/path canonicalization (16 payloads) | Step 8: Provider and crypto boundaries |
| Step 5: Header trust + CSP audit | Step 11: Report writing |
| Step 6: Token/cookie/session audit | Step 12: Fix application |
| Step 7: Parser/DoS/panic boundaries | |
| Step 9: Concurrency and cache safety | |
| Step 10: 3-vote adversarial verify (with Scope Sweep gate) | |

Workflow phases run in sequence with step-completion enforcement: a phase producing shallow output is rejected, not passed. The 3-vote verify in Step 10 uses diverse skeptic prompts (threat-model reader, exploit-chain tracer, fix-site checker). Kill if ≥2 refute.

---

## 12-Step Summary

| # | Step | Mode |
|---|------|------|
| Pre | govulncheck, config drift, supply-chain integrity | Workflow |
| 1 | Scope the hunt | Manual |
| 2 | Map decision paths end-to-end | Manual |
| 3 | Targeted search passes (7 grep patterns) | Workflow |
| 4 | URL/path canonicalization (16 adversarial payloads) | Workflow |
| 5 | Redirect, header trust, CSP contextual audit | Workflow |
| 6 | Token, cookie, session security | Workflow |
| 7 | Parser, DoS, panic boundaries + race detector | Workflow |
| 8 | Provider and crypto boundaries | Manual |
| 9 | Concurrency and cache safety | Workflow |
| 10 | 3-vote adversarial verify with Scope Sweep gate | Workflow |
| 11 | Report per-finding (7-field template) | Manual |
| 12 | Fix conservatively with regression tests | Manual |

Full step details, payload tables, and language-specific search passes in `references/methodology.md`.

---

## Definition of Done

- [ ] Scope documented (what was hunted, what was out of bounds)
- [ ] Pre-Hunt Sweeps executed (govulncheck, config drift, supply-chain)
- [ ] All 7 search passes from Step 3 executed (no skipped passes)
- [ ] URL/path inputs tested against all 16 adversarial payloads
- [ ] Every finding classified into one of 6 validation outcomes
- [ ] ≥2 skeptics concur on each Confirmed/Likely (or `--quick` flag used)
- [ ] Every Confirmed finding has a fix with a regression test
- [ ] Provider boundaries checked (each present in this project)
- [ ] `go test -race ./...` passes (or explained if not run)

---

## File Structure

```
skills/pb-threat-hunt/
  SKILL.md                              ← You are here (~100 lines)
  references/
    methodology.md                       ← Full 12-step breakdown, payload tables, appendices
  workflows/
    threat-hunt.js                       ← Executable workflow template
```

Run `./scripts/install.sh` to install to `~/.claude/skills/pb-threat-hunt/`.

---

## Related Commands

- `/pb-security` - Quick pre-release security checklist (run first; use this for deep follow-up)
- `/pb-secrets` - Secrets management lifecycle
- `/pb-hardening` - Infrastructure hardening (servers, containers, networks)
- `/pb-incident` - Incident response when a finding becomes an active threat
- `/pb-debug` - Tracing exploit paths through code
