# Engineering Playbook

Structured development commands for engineers using agentic AI tools. Tool-agnostic at the core, Claude Code integration included.

[![CI](https://github.com/vnykmshr/playbook/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/vnykmshr/playbook/actions/workflows/deploy-docs.yml)
[![Latest Release](https://img.shields.io/github/v/release/vnykmshr/playbook)](https://github.com/vnykmshr/playbook/releases/latest)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## What this is

109 commands across 9 categories covering the SDLC from planning through production operations. Written for engineers who want repeatable structure without ceremony:

- Two foundations: [`/pb-preamble`](commands/core/pb-preamble.md) (how to collaborate) and [`/pb-design-rules`](commands/core/pb-design-rules.md) (what to build)
- A three-command daily ritual: `/pb-preferences --setup` → `/pb-start` → code → `/pb-review` → `/pb-pr`
- Self-evolving: quarterly cycles plus capability-triggered updates when Claude's model tier changes

Content is Markdown. Structure is enforced by lint and tests. Commands are versioned independently; no breaking changes without a major release.

## Who it's for

- Engineers using Claude Code who want a curated command library
- Teams adapting playbooks to other AI tools (read as Markdown, adapt prompts)
- Solo maintainers building personal workflows they can evolve

Not a framework to adopt wholesale. Start with the preamble, pick commands that fit, ignore the rest.

## Install

```bash
git clone https://github.com/vnykmshr/playbook.git
cd playbook
./scripts/install.sh
```

With Claude Code, `install.sh` symlinks `commands/` and helper scripts into `~/.claude/`. Without Claude Code, read the files directly -- each command is self-contained Markdown.

Uninstall: `./scripts/uninstall.sh`.

## Daily rhythm

```
/pb-preferences --setup     # one-time, 15 min
/pb-start "<description>"   # create branch, lock scope
  [code]
/pb-review                  # self-review + persona review + commit
/pb-pr                      # create PR when peer review needed
```

For deeper work: `/pb-plan` (architecture), `/pb-adr` (decision records), `/pb-security`, `/pb-performance`, `/pb-incident`. See the command index for the full list.

## Learn more

- **[Command index](https://vnykmshr.github.io/playbook/command-index/)** -- all 109 commands grouped by category
- **[Book site](https://playbook.1mb.dev)** -- distraction-free reading view
- **[Integration guide](docs/integration-guide.md)** -- how commands compose
- **[Using with other tools](docs/using-with-other-tools.md)** -- adapting the playbook outside Claude Code

## Meta

- [CONTRIBUTING](.github/CONTRIBUTING.md) -- local checks, PR expectations
- [SECURITY](.github/SECURITY.md) -- scope, reporting
- [CHANGELOG](CHANGELOG.md) -- release history
- MIT -- see [LICENSE](LICENSE)
