# Pattern Learning

**Purpose:** Extract reusable patterns from the current session — error resolutions, debugging techniques, workarounds, and project conventions.

**Mindset:** Design Rules say "measure before optimizing" — learn from what you measure, not what you assume. Capture knowledge that would help future you (or teammates) solve similar problems faster. Focus on patterns that are **reusable**, not one-time fixes.

**Resource Hint:** sonnet — pattern extraction and documentation

---

## When to Use

- After resolving a non-trivial bug worth documenting
- After discovering a debugging technique or library workaround
- After establishing a project convention that teammates should follow
- After a session where hard-won insights would otherwise be lost

---

## What to Capture

| Category | Good Candidate | Skip |
|----------|----------------|------|
| **Error Resolution** | "Type X error in library Y means Z" | Typo fixes |
| **Debugging Technique** | "To debug A, check B then C" | Obvious checks |
| **Workaround** | "Library X has quirk Y, work around with Z" | Version-specific issues that will be fixed soon |
| **Project Pattern** | "In this codebase, we handle X by doing Y" | One-off decisions |

**Rule of thumb:** If you'd explain this to a teammate joining the project, it's worth capturing.

---

## Pattern Template

```markdown
# [Pattern Name]

## Problem

[What situation triggers this pattern — be specific about symptoms]

## Solution

[What to do — concrete steps or code]

## Example

[Code or commands demonstrating the solution]

## Context

[When this applies, when it doesn't, prerequisites]

## Discovered

[Date, project, session context]
```

---

## Storage Locations

| Location | Use For | Command |
|----------|---------|---------|
| `.claude/patterns/` | Project-specific patterns, shareable with team | Default |
| `~/.claude/learned/` | Universal patterns, personal knowledge base | `--global` flag |

### Project Patterns (Default)

```
.claude/patterns/
├── error-axios-timeout-handling.md
├── debug-react-state-updates.md
└── workaround-jest-esm-modules.md
```

**Commit these** to share with your team. They become part of project knowledge.

### Global Patterns

```
~/.claude/learned/
├── debug-memory-leaks-node.md
├── workaround-docker-m1-networking.md
└── pattern-api-retry-logic.md
```

These follow you across all projects — personal knowledge base.

---

## Workflow

### Step 1: Identify the Pattern

After resolving an issue, ask yourself:

- Would this help me next time I hit this?
- Would this help a teammate?
- Is this specific enough to be actionable?
- Did this take significant time to figure out?

If yes to any, proceed.

### Step 2: Extract the Pattern

Review what happened:

1. **What was the symptom?** — Error message, unexpected behavior
2. **What was the root cause?** — Why it happened
3. **What was the solution?** — What fixed it
4. **What made this non-obvious?** — Why it took time to figure out

### Step 3: Document

Use the template above. Be specific:

| Bad | Good |
|-----|------|
| "Check the logs" | "When axios throws ECONNRESET, check if server timeout < client timeout" |
| "Fix the types" | "TypeScript 5.x with ESM requires .js extensions in imports even for .ts files" |
| "Handle the error" | "Prisma P2025 means record not found — check if ID exists before update" |

### Step 4: Store

```bash
# Project-local (default) — creates .claude/patterns/[name].md
mkdir -p .claude/patterns

# Global — creates ~/.claude/learned/[name].md
mkdir -p ~/.claude/learned
```

---

## Examples

### Error Resolution Pattern

```markdown
# TypeScript: Cannot find module with .js extension

## Problem

TypeScript compilation fails with "Cannot find module './foo.js'" even though
foo.ts exists. Happens after upgrading to TypeScript 5.x with ES modules.

## Solution

In tsconfig.json, set moduleResolution appropriately:
- For `Node16`/`NodeNext`: imports need .js extension even for .ts files
- For `bundler`: imports can omit extension

## Example

```json
{
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext"
  }
}
```

Then import with `.js`:
```typescript
import { helper } from './helper.js';  // Even though file is helper.ts
```

## Context

Applies to TypeScript 5.x with ES modules. Classic CommonJS projects
don't have this issue. If using a bundler (webpack, vite), use
`moduleResolution: "bundler"` instead.

## Discovered

2026-01-21, playbook project, debugging module resolution
```

### Debugging Technique Pattern

```markdown
# Debug React useEffect Running Twice

## Problem

useEffect cleanup and effect running twice in development, causing duplicate
API calls or unexpected state.

## Solution

This is intentional in React 18+ Strict Mode. It helps find bugs where:
- Cleanup doesn't properly reset state
- Effects have missing dependencies
- Effects aren't idempotent

To debug:
1. Check if cleanup function properly reverses the effect
2. Verify effect is idempotent (safe to run twice)
3. Use AbortController for fetch requests

## Example

```jsx
useEffect(() => {
  const controller = new AbortController();

  fetchData({ signal: controller.signal })
    .then(setData)
    .catch(err => {
      if (err.name !== 'AbortError') throw err;
    });

  return () => controller.abort();  // Proper cleanup
}, []);
```

## Context

React 18+ development mode only. Production runs effects once.
Don't disable Strict Mode — fix the underlying issue instead.

## Discovered

2026-01-21, investigating "duplicate API calls" issue
```

### Workaround Pattern

```markdown
# Jest ESM Modules: SyntaxError unexpected token export

## Problem

Jest fails with "SyntaxError: Unexpected token 'export'" when testing
code that imports from ESM-only packages (e.g., nanoid, chalk v5).

## Solution

Add the package to Jest's transformIgnorePatterns exception:

```javascript
// jest.config.js
module.exports = {
  transformIgnorePatterns: [
    'node_modules/(?!(nanoid|chalk)/)'
  ]
};
```

## Context

Needed for ESM-only packages in Jest with CommonJS setup.
Alternative: migrate project to native ESM or use vitest.

## Discovered

2026-01-21, adding nanoid to project
```

---

## When NOT to Use

Skip pattern extraction for:

- **Trivial fixes** — Typos, missing imports, syntax errors
- **Temporary workarounds** — Hacks you'll remove soon
- **Highly version-specific** — Library will fix in next release
- **Well-documented elsewhere** — Official docs cover it well
- **One-time decisions** — Choices that won't recur

---

## Pattern Quality Checklist

Before saving, verify:

- [ ] **Problem is specific** — Someone can recognize when they have this issue
- [ ] **Solution is actionable** — Steps are concrete, not vague
- [ ] **Example is included** — Shows actual code or commands
- [ ] **Context explains scope** — When it applies, when it doesn't
- [ ] **Not already documented** — Check project docs, official docs first

---

## Organizing Patterns

### Naming Convention

```
[category]-[topic]-[specifics].md

error-prisma-p2025-not-found.md
debug-react-hydration-mismatch.md
workaround-jest-esm-modules.md
pattern-api-retry-exponential.md
```

### Categories

| Prefix | Use For |
|--------|---------|
| `error-` | Error message resolutions |
| `debug-` | Debugging techniques |
| `workaround-` | Library/tool quirks |
| `pattern-` | Reusable code patterns |
| `setup-` | Environment/tooling setup |

---

## Integration

After resolving non-trivial issues in these workflows, consider capturing patterns:

- `/pb-debug` — After fixing a tricky bug, capture the resolution
- `/pb-cycle` — After discovering a better approach during iteration

---

## Related Commands

- `/pb-debug` — Debugging methodology (source of error/debug patterns)
- `/pb-cycle` — Development iteration (source of pattern discoveries)
- `/pb-resume` — Uses stored patterns for session continuity
- `/pb-documentation` — Writing clear documentation
- `/pb-standards` — Project conventions to document

---

*Patterns compound. Today's hard-won insight is tomorrow's instant recall.*
