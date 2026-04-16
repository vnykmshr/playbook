# Security

The playbook is markdown content, Python scripts, and a docsite build pipeline. Security scope is:

- Build/script vulnerabilities in `scripts/`, CI configs, deploy tooling
- Docsite vulnerabilities (XSS, injection in generated HTML)
- Supply-chain issues in pinned dependencies

Playbook *content* is advice, not executable. Argue with it, ignore it, adapt it -- that's not security scope.

## Reporting

Private disclosure via [GitHub Security Advisories](https://github.com/vnykmshr/playbook/security/advisories). Don't open public issues.

## Response

Solo maintainer, best effort -- no SLA. Typical rhythm: acknowledge within a few days, fix critical issues before the next release, non-critical batched into the next quarterly evolution cycle. Old releases are not patched -- update to current.
