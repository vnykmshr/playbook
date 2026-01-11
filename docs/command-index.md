# Command Index

Quick reference for all playbook commands.

## Development Workflow

| Command | When to Use |
|---------|-------------|
| `/pb-start` | Starting work on a feature branch |
| `/pb-cycle` | Each iteration (develop → review → commit) |
| `/pb-resume` | Resuming after a break |
| `/pb-pr` | Creating a pull request |

## Planning

| Command | When to Use |
|---------|-------------|
| `/pb-plan` | Planning a new feature/release |
| `/pb-adr` | Documenting architectural decisions |

## Release & Operations

| Command | When to Use |
|---------|-------------|
| `/pb-release` | Pre-release checks and deployment |
| `/pb-incident` | P0/P1 production incidents |

## Periodic Reviews

| Command | When to Use | Frequency |
|---------|-------------|-----------|
| `/pb-review` | Comprehensive multi-perspective | Monthly or pre-release |
| `/pb-review-code` | Code cleanup, repo health | Before new dev cycle |
| `/pb-review-prerelease` | Pre-release code review | Before each release |
| `/pb-review-tests` | Test suite quality | Monthly |
| `/pb-review-docs` | Documentation accuracy | Quarterly |
| `/pb-review-hygiene` | Multi-role health check | Quarterly |
| `/pb-review-product` | Technical + product review | Monthly |

## Reference Documents

| Command | Purpose |
|---------|---------|
| `/pb-guide` | Full SDLC guide with tiers, gates, checklists |
| `/pb-templates` | Templates for commits, phases, reviews |
| `/pb-standards` | Coding standards, quality principles |
| `/pb-context` | Project onboarding context template |

## Typical Workflow

```
1. Plan
   /pb-plan     → Lock scope, define phases

2. Develop (iterative)
   /pb-start    → Create branch, set rhythm
   /pb-cycle    → Develop → Review → Commit (repeat)
   /pb-resume   → Resume after breaks

3. PR
   /pb-pr       → Create with proper context

4. Release
   /pb-release  → Checks, deploy, verify

5. Maintain
   /pb-review-* → Periodic reviews as scheduled
```
