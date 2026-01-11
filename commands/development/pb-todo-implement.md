# Todo-Based Implementation Workflow

Structured implementation of individual todos with checkpoint-based approval. Transforms vague todos into concrete, tested features with full audit trail.

---

## Philosophy

### When to Use This

**Use `/pb-todo-implement` when:**
- You have a clearly scoped todo or task to implement
- You want structured checkpoint-based review (not just final review)
- You want codebase analysis before implementation
- You want full audit trail of completed work
- You're implementing on current branch (no feature branches)

**Use `/pb-plan` instead if:**
- Planning a multi-phase release with multiple focus areas
- Scope is still being clarified
- You need multi-perspective alignment before starting

**Use `/pb-cycle` instead if:**
- You're ready for full self-review + peer review
- Implementation is already complete, you need code review

---

## Workflow Phases

You MUST follow these phases in order: **INIT → SELECT → REFINE → IMPLEMENT → COMMIT**

At each STOP, you MUST get user confirmation or input before proceeding.

---

## Phase 1: INIT - Establish Context

### Goal
Ensure project context is clear and detect any orphaned work from previous sessions.

### Steps

**1. Load Project Context**

Check for `todos/project-description.md`:
- If exists: Read in full
- If missing: Use parallel Task agents to analyze:
  - Purpose, features, business value
  - Languages, frameworks, build tools (extract from package.json, Makefile, etc.)
  - Components and architecture
  - Key commands: build, test, lint, dev/run
  - Testing setup and how to add new tests

Then propose:
```markdown
# Project: [Name]
[1-2 sentence description]

## Features
[Key capabilities and purpose]

## Tech Stack
[Languages, frameworks, build/test/deploy tools]

## Structure
[Key directories, entry points, important files]

## Architecture
[How components interact, main modules]

## Commands
- Build: [command]
- Test: [command]
- Lint: [command]
- Dev/Run: [command]

## Testing
[How to create and run new tests]
```

**STOP → "Are there corrections to the project description? (y/n)"**
- If yes: Gather corrections
- If no: Proceed to detect orphans

**2. Detect Orphaned Work**

Check `todos/work/` for any tasks from interrupted sessions:

```bash
mkdir -p todos/work todos/done
for task_dir in todos/work/*/; do
  [ -f "$task_dir/task.md" ] || continue
  status=$(grep "^**Status:**" "$task_dir/task.md" | head -1)
  echo "$(basename "$task_dir"): $status"
done
```

If orphaned tasks exist:

**STOP → "Found incomplete tasks. Resume one? (number/name or 'skip')"**

If resuming:
- Read full `task.md` from selected task
- Continue to appropriate phase:
  - Status: `Refining` → Jump to Phase 2 (REFINE)
  - Status: `InProgress` → Jump to Phase 3 (IMPLEMENT)
  - Status: `AwaitingCommit` → Jump to Phase 4 (COMMIT)

If skipping: Continue to SELECT

---

## Phase 2: SELECT - Choose Todo

### Goal
Pick a todo from your backlog and create a task tracking document.

### Steps

**1. Read Todo List**

Read `todos/todos.md` in full. If missing, create it:

```markdown
# Project Todos

## Backlog

- [ ] [Todo 1 - one line summary]
- [ ] [Todo 2 - one line summary]
- [ ] [Todo 3 - one line summary]

## Completed

(Move items here after successful completion)
```

**2. Present Todos**

Show numbered list with one-line summaries:

```
1. [Todo 1 summary]
2. [Todo 2 summary]
3. [Todo 3 summary]
```

**STOP → "Which todo to implement? (enter number)"**

**3. Create Task Tracking**

Create task directory and initialize tracking file:

```bash
TASK_DIR="todos/work/$(date +%Y-%m-%d-%H-%M-%S)-[task-title-slug]/"
mkdir -p "$TASK_DIR"
```

Initialize `$TASK_DIR/task.md`:

```markdown
# [Task Title]

**Status**: Refining
**Created**: [YYYY-MM-DD HH:MM:SS]
**Effort**: [estimate: 30min / 1-2hrs / 2-4hrs / 4hrs+]
**Priority**: [P0/P1/P2]

## Original Todo
[Raw text from todos/todos.md]

## Description
[What we're building - write after REFINE phase]

## Implementation Plan
[How we're building it - write after REFINE phase]
- [ ] Code change with location(s) if applicable (file.ts:45-93)
- [ ] Automated test: [what to test]
- [ ] Manual verification: [user-facing steps]
- [ ] Update docs: [if applicable]

## Notes
[Implementation notes and discoveries]
```

**4. Update Todo List**

Remove the selected todo from `todos/todos.md` (move it to "In Progress" section).

**STOP → "Ready to refine this todo? (y/n)"**

---

## Phase 3: REFINE - Analyze and Plan

### Goal
Understand exactly what needs to change and how to implement it.

### Steps

**1. Codebase Analysis**

Use parallel Task agents to analyze:
- Where in codebase changes are needed (specific files/lines)
- Existing patterns to follow (naming, structure, error handling)
- What related features/code already exist
- Dependencies and integration points
- Test structure for this area

Create `$TASK_DIR/analysis.md` with findings:

```markdown
# Codebase Analysis

## Files to Modify
- [file.ts:45-93] - Description of what needs to change
- [file.ts:120-150] - Description of what needs to change

## Existing Patterns
- [Pattern name] - How it's currently used in [file.ts:XX]
- [Pattern name] - Applicable pattern for this feature

## Related Code
- [Related feature 1] implemented in [file.ts:XX]
- [Related feature 2] implemented in [file.ts:XX]

## Dependencies
- [External API/service] - Used in [file.ts:XX]
- [Internal module] - Imported in [file.ts:XX]

## Test Structure
- Test file: [test-file.ts]
- How to add tests: [steps]
```

**2. Draft Description**

Based on analysis, propose:

```markdown
## Description

[Clear explanation of what we're building]
- What problem does this solve?
- Who benefits?
- What's the user-facing impact?
```

**STOP → "Use this description? (y/n)"**
- If no: Refine and re-present
- If yes: Add to task.md

**3. Draft Implementation Plan**

Based on analysis, propose:

```markdown
## Implementation Plan

[How we're building it]

### Checkpoints
- [ ] [Code change] - [file.ts:XX], [description]
- [ ] [Automated test] - [test case description]
- [ ] [Manual verification] - [steps to verify manually]
- [ ] [Docs update] - [if applicable]
```

**STOP → "Use this implementation plan? (y/n)"**
- If no: Refine and re-present
- If yes: Add to task.md

**4. Finalize**

Update `task.md`:
- Set `**Status**: InProgress`
- Add analysis results to Notes section
- Add final Description and Implementation Plan

**STOP → "Ready to implement? (y/n)"**

---

## Phase 4: IMPLEMENT - Execute Plan

### Goal
Execute the implementation plan checkpoint-by-checkpoint with user approval at each step.

### Steps

**1. Work Checkpoint-by-Checkpoint**

For each checkbox in implementation plan:

**A. Make the change**
- Code modifications
- New files
- Deletions
- Test additions

**B. Summarize**
Show what was changed, why, and how it aligns with the plan.

**C. Ask for approval**

**STOP → "Approve these changes? (y/n)"**
- If no: Refine or revert and re-propose
- If yes: Proceed to mark complete

**D. Mark complete and stage**
- Update checkbox in task.md: `- [x] [description]`
- Stage changes: `git add -A`

**2. Handle Unexpected Work**

If you discover work not in the plan:

**STOP → "Plan needs a new checkpoint: [description]. Add it? (y/n)"**
- If yes: Add checkbox to plan, proceed with work
- If no: Record in Notes as deferred, continue with plan

**3. Validation**

After all checkpoints complete, validate:

```bash
# Run tests
[TEST_COMMAND]

# Run lint
[LINT_COMMAND]

# Run build (if applicable)
[BUILD_COMMAND]
```

If validation fails:

**STOP → "Validation failed. Add these checkpoints to fix? [list]"**
- If yes: Add to plan and continue IMPLEMENT from step 1
- If no: Record in Notes and proceed (may need post-implementation follow-up)

**4. Manual Verification**

Present user test steps:

**STOP → "Do all manual verification steps pass? (y/n)"**
- If no: Gather details on what failed, return to step 1
- If yes: Proceed to COMMIT phase

**5. Update Project Description (if needed)**

If implementation changed structure, features, or commands:

**STOP → "Update project description with these changes? (y/n)"**
- If yes: Update `todos/project-description.md`
- If no: Record in Notes as doc debt

**6. Ready for Commit**

Update task.md: `**Status**: AwaitingCommit`

---

## Phase 5: COMMIT - Finalize Work

### Goal
Commit changes with full audit trail and move task to completed.

### Steps

**1. Present Summary**

Show what was accomplished:
```
## What Was Accomplished

- [Specific change 1]
- [Specific change 2]
- [Test added for X]
- [Docs updated for Y]

Files Changed:
- [file.ts:XX-YY]
- [new-file.ts]

Tests Added:
- [test case 1]
- [test case 2]
```

**STOP → "Ready to commit all changes? (y/n)"**

**2. Finalize Task Document**

Update task.md:
- Set `**Status**: Done`
- Add completion timestamp

**3. Move Task to Archive**

```bash
mv todos/work/[timestamp]-[task-slug]/task.md todos/done/[timestamp]-[task-slug].md
mv todos/work/[timestamp]-[task-slug]/analysis.md todos/done/[timestamp]-[task-slug]-analysis.md
rmdir todos/work/[timestamp]-[task-slug]/
```

**4. Create Atomic Commit**

```bash
git add -A
git commit -m "[task-title]: [one-line summary]

[More detailed description if needed]

- Closes: [if applicable]
- Testing: [What was tested]"
```

**5. Update Todo List**

Move completed todo to "Completed" section in `todos/todos.md`:

```markdown
## Completed

- [x] [Todo that was just completed]
```

**6. Offer Next Step**

**STOP → "Continue with next todo? (y/n)"**
- If yes: Return to Phase 2 (SELECT)
- If no: Done for this session

---

## Checkpoints Summary

| Phase | Stop Points | Decision |
|-------|-------------|----------|
| INIT | 2 | Corrections? Resume orphan? |
| SELECT | 2 | Which todo? Ready to refine? |
| REFINE | 4 | Description? Plan? Ready to implement? |
| IMPLEMENT | Per checkpoint | Approve changes? New checkpoints needed? Tests pass? Docs updated? |
| COMMIT | 2 | Summary correct? Continue with next? |

---

## Integration with Playbook

### Workflow Integration

```
/pb-plan
  ↓ (after scope is locked)
/pb-todo-implement  ← YOU ARE HERE
  ↓ (when code is ready for review)
/pb-cycle (self-review + peer review)
  ↓ (when ready to finalize)
/pb-pr or /pb-commit (create PR or direct commit)
```

### Related Commands

- **Before this**: `/pb-plan` - Plan the focus area and phases
- **After implementation**: `/pb-cycle` - Self-review + peer review
- **Finalizing**: `/pb-pr` - Create pull request, `/pb-commit` - Direct commit
- **Code quality**: `/pb-review-code` - Code cleanup and review

### Directory Structure

```
todos/
├── todos.md                      # Your backlog
├── project-description.md        # Project context
├── work/
│   └── YYYY-MM-DD-HH-MM-SS-task-slug/
│       ├── task.md             # Current task being implemented
│       └── analysis.md          # Codebase analysis findings
└── done/
    ├── YYYY-MM-DD-HH-MM-SS-task-slug.md           # Completed task
    └── YYYY-MM-DD-HH-MM-SS-task-slug-analysis.md  # Analysis archive
```

---

## Best Practices

### Checkpoint Design

```
[NO] Too coarse: "[ ] Implement everything"
[YES] Right-sized: "[ ] Add validation to email input (user.ts:45-60)"

[NO] Too vague: "[ ] Fix the bugs"
[YES] Clear: "[ ] Fix password reset error when email has +address (fix in auth-service.ts:120)"

[NO] Too many: "[ ] Change 1 variable, [ ] Change 2 variables, [ ] Change 3 variables"
[YES] Grouped: "[ ] Update config variables in config.ts:10-30"
```

### Effort Estimation

```
Effort: 30min      - Trivial change, single file, no tests
Effort: 1-2hrs     - Simple change, 2-3 files, basic tests
Effort: 2-4hrs     - Moderate change, multiple files, comprehensive tests, docs
Effort: 4hrs+      - Large change, architectural impact, extensive testing
```

### Priority Levels

```
Priority: P0       - Critical bug, blocks other work, prod incident
Priority: P1       - Important feature, needed for release, high business value
Priority: P2       - Nice to have, can be deferred, lower priority
```

---

## Example: Adding a Feature

### Phase 1: INIT
→ Project context loaded, no orphans detected

### Phase 2: SELECT
→ Selected: "Add user profile endpoint"

### Phase 3: REFINE
→ Analysis: Need to modify `user-service.ts`, add tests to `user-service.test.ts`
→ Plan: Endpoint implementation, request validation, response serialization, tests, docs

### Phase 4: IMPLEMENT
→ Implement endpoint in user-service.ts
→ Add validation middleware
→ Create unit tests
→ Add integration test
→ Update API docs

### Phase 5: COMMIT
→ Commit: "user-service: add user profile endpoint"
→ Update todos.md: move to Completed

---

## Red Flags to Watch For

### Scope Creep
- "While I'm here, let me also..."
- "This would be easy to add..."

**Fix**: Record in Notes as future todo, stay focused on current task

### Missing Alignment
- Discovery reveals different solution needed
- Dependencies blocking implementation

**Fix**: STOP and discuss with user before proceeding

### Test Gaps
- Implementation complete but no tests
- Tests don't match stated acceptance criteria

**Fix**: Add test checkpoint, ensure coverage before COMMIT

### Incomplete Analysis
- Implementation reveals files/patterns we missed
- Integration complexity was underestimated

**Fix**: Update analysis.md, propose new checkpoints, adjust effort estimate

---

## Usage

Start implementing a todo:

```bash
/pb-todo-implement
```

The workflow will:
1. Load project context
2. Show your todos and let you pick one
3. Analyze the codebase thoroughly
4. Get your approval on description and plan
5. Walk through implementation checkpoint-by-checkpoint
6. Commit when complete with full audit trail
7. Offer to start next todo

---

*Created: 2026-01-11 | Category: Development | Tier: M*
