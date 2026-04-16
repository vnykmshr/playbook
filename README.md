# Engineering Playbook

Structured Markdown commands for AI-assisted development. Covers the SDLC from planning to production operations. Tool-adaptable.

[![CI](https://github.com/vnykmshr/playbook/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/vnykmshr/playbook/actions/workflows/deploy-docs.yml)
[![Latest Release](https://img.shields.io/github/v/release/vnykmshr/playbook)](https://github.com/vnykmshr/playbook/releases/latest)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## What this is

Structured commands organized by SDLC phase, for engineers who want repeatable structure without ceremony:

- Two foundations: [`/pb-preamble`](commands/core/pb-preamble.md) (how to collaborate) and [`/pb-design-rules`](commands/core/pb-design-rules.md) (what to build)
- A three-command daily ritual: `/pb-preferences --setup` → `/pb-start` → code → `/pb-review` → `/pb-pr`
- Self-evolving: periodic cycles plus capability-triggered updates when the underlying model tier changes

Content is Markdown. Structure is enforced by lint and tests. Commands are versioned independently; no breaking changes without a major release.

## Who it's for

- Engineers who want a curated command library for AI-assisted development
- Teams adapting playbooks to different AI tools (read as Markdown, adapt prompts)
- Solo maintainers building personal workflows they can evolve

Not a framework to adopt wholesale. Start with the preamble, pick commands that fit, ignore the rest.

## Install

```bash
git clone https://github.com/vnykmshr/playbook.git
cd playbook
./scripts/install.sh
```

`install.sh` symlinks `commands/` and helper scripts to `~/.claude/`. Using a different toolchain? Read the files directly -- each command is self-contained Markdown.

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

- **[Command index](https://vnykmshr.github.io/playbook/command-index/)** -- complete catalog grouped by category
- **[Book site](https://playbook.1mb.dev)** -- distraction-free reading view
- **[Integration guide](docs/integration-guide.md)** -- how commands compose
- **[Using with other tools](docs/using-with-other-tools.md)** -- adapting the playbook outside the reference toolchain

## Meta

- [CONTRIBUTING](.github/CONTRIBUTING.md) -- local checks, PR expectations
- [SECURITY](.github/SECURITY.md) -- scope, reporting
- [CHANGELOG](CHANGELOG.md) -- release history
- MIT -- see [LICENSE](LICENSE)
