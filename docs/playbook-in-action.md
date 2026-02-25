# Playbook in Action

The standard development cycle using playbook commands.

---

## Development Cycle

```
/pb-start "what you're building"
  → code
/pb-review
  → automatic quality gate, auto-commit
/pb-pr
  → peer review
```

## Command Quick Reference

| Scenario | Command |
|----------|---------|
| Start new feature | `/pb-start` |
| Finish and commit | `/pb-review` |
| Submit for review | `/pb-pr` |
| Deep architecture | `/pb-plan` |
| Test strategy | `/pb-testing` |
| Code standards | `/pb-standards` |
| Security check | `/pb-security` |
| Debug an issue | `/pb-debug` |

## Common Scenarios

### Adding a Feature

```bash
/pb-start "feat: add user profiles"
# write code, write tests
/pb-review
/pb-pr
```

### Fixing a Bug

```bash
/pb-start "fix: email validation"
# write failing test, fix code, verify test passes
/pb-review
/pb-pr
```

### Addressing Review Feedback

```bash
# make changes based on feedback
/pb-review
# auto-pushes to existing PR
```

---

See [`/pb-guide`](/commands/core/pb-guide.md) for the full SDLC framework.
