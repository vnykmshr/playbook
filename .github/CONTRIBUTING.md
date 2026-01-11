# Contributing to Engineering Playbook

## How to Report Issues

Found a bug or have a suggestion? [Open an issue](https://github.com/vnykmshr/playbook/issues) with:
- Clear title describing the problem
- Steps to reproduce (if applicable)
- Expected vs. actual behavior

## How to Suggest Improvements

Have an idea for a new command or enhancement? [Start a discussion](https://github.com/vnykmshr/playbook/discussions) to:
- Describe the use case
- Explain why it's needed
- Discuss the approach before implementing

## How to Contribute Code

### Commands

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-command-name`
3. Create command file in appropriate `commands/` subdirectory
4. Follow existing command structure and documentation format
5. Test locally: verify the command works as documented
6. Submit a pull request with:
   - Clear description of what the command does
   - When to use it
   - How it integrates with other commands

### Documentation

1. Follow the same branch/PR process
2. Keep changes focused and atomic
3. Run local checks: `markdownlint docs/` (if linting tools are set up)
4. Verify all links work

### Process

- All PRs require review
- Keep changes focused (one feature/fix per PR)
- Reference any related issues
- Be responsive to feedback

## Code of Conduct

Be respectful and constructive. This is a collaborative project for teams to improve their development practices.

## Questions?

- Check [docs/](/docs/) for existing documentation
- See [docs/command-index.md](/docs/command-index.md) for command reference
- Open a [discussion](https://github.com/vnykmshr/playbook/discussions) for questions
