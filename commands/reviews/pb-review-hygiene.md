## 🧹 **Periodic Project Hygiene Review**

You are performing a **periodic hygiene check** for this project.
Your goal is to **assess the project's overall health, completeness, and robustness** — not to make changes, but to identify what needs attention, what's working well, and what can be improved with minimal effort.

**Approach:** Hygiene reviews embody `/pb-preamble` thinking. Challenge hidden assumptions about what "health" means. Surface risks directly, don't soften findings to be diplomatic.

---

### **Roles & Perspectives**

Act as:

1. **Senior Engineer** – Assess technical soundness, codebase cleanliness, dependency health, CI/CD, and configuration hygiene.
2. **Technical Architect** – Evaluate system design, infrastructure readiness, scalability, and environment consistency.
3. **Product Manager** – Check that priorities, documentation, and outcomes align with product goals.
4. **Security & Reliability Reviewer** – Identify security, availability, or compliance gaps.
5. **DevOps / Operations Engineer** – Check automation, deployment, and observability coverage.

---

### **Review Objectives**

* **Completeness** – Are all key areas (code, tests, docs, infra, monitoring, security) reasonably covered?
* **Robustness** – Are there weak spots, outdated dependencies, or single points of failure?
* **Hygiene** – Are there stale files, unused configs, or missing metadata (README, LICENSE, CHANGELOG)?
* **Quick Wins** – Identify small, low-effort improvements that yield immediate stability, performance, or clarity benefits.
* **Consistency** – Ensure naming, conventions, environments, and workflows are uniform across modules.
* **Alignment** – Check that engineering direction aligns with current goals and priorities.

---

### **Checklist (Apply Selectively)**

#### 1. Codebase

* Clear, readable structure? No major dead code or unused modules?
* Dependencies up to date and pinned?
* Build scripts and Makefiles functional and minimal?
* Linting, formatting, and static checks passing?
* Sensitive info (API keys, creds) properly excluded?

#### 2. Tests & Quality Gates

* Unit/integration tests running in CI?
* Coverage reports available and meaningful?
* Flaky tests or false positives identified?
* Test data sane and isolated?

#### 3. Documentation & Metadata

* README covers setup, run, and contribution steps clearly?
* CHANGELOG and LICENSE present and current?
* Architecture or design overview updated with recent changes?
* Owner/maintainer info available?

#### 4. CI/CD & Infrastructure

* Pipelines consistent, reproducible, and passing?
* Deployments versioned and auditable?
* Monitoring, alerting, and rollback procedures exist?
* Environment variables, secrets, and infra configs clean and documented?

#### 5. Security & Compliance

* Dependencies scanned for vulnerabilities?
* Secrets properly stored (Vault, Secret Manager, etc.)?
* Logging and access controls verified?
* No unpatched services or public exposure risks?

#### 6. Operational Readiness

* Can a new engineer onboard easily?
* Recovery/runbooks available for production issues?
* Resource usage (CPU, memory, DB size) monitored and sane?
* Error budgets or SLAs being tracked?

#### 7. Quick Wins

* List small, immediate improvements (≤2 hours each) that improve clarity, performance, or safety.
  *(e.g., update README section, remove unused Docker image, add missing env var doc, enable dependabot, refresh lock file)*

---

### **Deliverables**

1. **Executive summary:** 3–5 bullet overview of overall health (Good / Needs Attention / At Risk).
2. **Key findings:** Grouped by category (Codebase, Docs, Infra, Security, etc.) with severity tags (Critical / Medium / Minor).
3. **Quick wins list:** Practical actions that can be completed fast, sorted by effort.
4. **Next review focus:** Areas that need deeper follow-up next cycle.
