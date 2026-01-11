# Command Index

Quick reference for all available commands.

## Development Workflow

| Command | When to Use |
|---------|-------------|
| `/vmx-start-dev` | Starting work on a feature branch |
| `/vmx-dev-cycle` | Each iteration (develop → review → commit) |
| `/vmx-resume-work` | Resuming after a break |
| `/vmx-quick-pr` | Creating a pull request |

## Planning

| Command | When to Use |
|---------|-------------|
| `/vmx-new-focus-area-generic` | Planning a new feature/release |
| `/vmx-adr` | Documenting architectural decisions |

## Release & Operations

| Command | When to Use |
|---------|-------------|
| `/vmx-make-release` | Pre-release checks and deployment |
| `/vmx-incident-response` | P0/P1 production incidents |

## Periodic Reviews

| Command | When to Use | Frequency |
|---------|-------------|-----------|
| `/vmx-project-review-periodic` | Comprehensive multi-perspective | Monthly or pre-release |
| `/vmx-review-engineer-periodic` | Code cleanup, repo health | Before new dev cycle |
| `/vmx-review-engineer-release` | Pre-release code review | Before each release |
| `/vmx-review-tests-periodic` | Test suite quality | Monthly |
| `/vmx-review-docs-periodic` | Documentation accuracy | Quarterly |
| `/vmx-review-hygiene-periodic` | Multi-role health check | Quarterly |
| `/vmx-review-tech-prod-periodic` | Technical + Product review | Monthly |

## Reference Documents

| Command | Purpose |
|---------|---------|
| `/vmx-engineering-playbook` | Full SDLC guide with tiers, gates, checklists |
| `/vmx-sdlc-template` | Templates for commits, phases, reviews |
| `/vmx-project-guidelines` | Coding standards, quality principles |
| `/vmx-working-context-template` | Project onboarding context template |

## Typical Workflow

```
1. Plan
   /vmx-new-focus-area-generic → Lock scope, define phases

2. Develop (iterative)
   /vmx-start-dev              → Create branch, set rhythm
   /vmx-dev-cycle              → Develop → Review → Commit (repeat)
   /vmx-resume-work            → Resume after breaks

3. PR
   /vmx-quick-pr               → Create with proper context

4. Release
   /vmx-make-release           → Checks, deploy, verify

5. Maintain
   /vmx-review-*               → Periodic reviews as scheduled
```
