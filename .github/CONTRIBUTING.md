# Contributing

Solo-curated playbook. PRs welcome -- open an issue first, it saves rework.

## Before you code

- Bugs: [issues](https://github.com/vnykmshr/playbook/issues). Ideas: [discussions](https://github.com/vnykmshr/playbook/discussions)
- New command: read `commands/core/pb-new-playbook.md`. Structure is enforced by lint and tests
- Existing command: metadata schema in `.playbook-metadata-schema.yaml` -- 14-field front-matter

## Local checks (all must pass)

```bash
python3 -m pytest tests/ -q
python3 scripts/validate-conventions.py
python3 scripts/check-links.py
npx markdownlint-cli --config .markdownlint.json 'commands/**/*.md'
./scripts/build-mdbook.sh
```

## PR expectations

- Atomic commits, conventional-commit format (`feat(scope): ...`)
- One concern per PR
- Touching a Related Commands list? Check all siblings for back-links
- Dependabot PRs: patch + security auto-merge after green CI, minor = check release notes, major = real review
