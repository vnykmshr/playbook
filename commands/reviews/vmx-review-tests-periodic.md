### 🧪 **Periodic Test Review Prompt (Unit + Integration Tests)**

You are performing a **comprehensive periodic review** of the project’s **unit and integration tests**.
Act as a **senior engineer and test architect** responsible for maintaining a test suite that is **lean, reliable, and genuinely useful**.

---

### **Your Review Goals**

1. **Prune Bloat**

   * Identify redundant, outdated, or overly defensive tests.
   * Remove or merge tests that don’t add new coverage or business value.
   * Flag duplicated logic or repetitive data setups.

2. **Evaluate Practicality**

   * Ensure tests validate meaningful behavior — not just implementation details.
   * Detect tests that are too brittle, rely on unstable mocks, or overfit specific code structures.
   * Check if test naming, descriptions, and organization remain clear and human-friendly.

3. **Assess Integration Depth**

   * For integration tests, confirm they test real system interactions (APIs, DB, queues, etc.), not what unit tests already cover.
   * Identify areas where integration tests have drifted toward slow, flaky, or unmaintainable behavior.

4. **Recommend Improvements**

   * Suggest refactoring, restructuring, or re-authoring tests for clarity and focus.
   * Propose new high-value tests for uncovered edge cases or new features.
   * Recommend better test data management or faster CI execution strategies.

---

### **Deliverables**

1. A **summary of key issues**: bloat, duplication, poor coverage, or misaligned focus.
2. **Concrete recommendations** — what to delete, merge, or rewrite, and why.
3. A **“next steps” plan** for restoring balance (e.g., split slow suites, remove mocks, improve naming).
4. Optionally: note **metrics to track** over time (e.g., test runtime, coverage %, flakiness, stability).
