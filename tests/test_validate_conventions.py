"""Regression tests for validate-conventions.py."""


def test_non_command_markdown_excluded_from_count(tmp_path, monkeypatch, load_script, make_command):
    """A stray non-pb-*.md under commands/ must not inflate the command count.

    Before the fix run() globbed '*.md' (all markdown); a README.md dropped under
    commands/ would push the count past EXPECTED_COUNT and FAIL the validator --
    in the CI gate. The glob must match only command files (pb-*.md).
    """
    make_command(tmp_path, "pb-alpha")
    make_command(tmp_path, "pb-beta")
    (tmp_path / "README.md").write_text("# not a command\n")

    vc = load_script("validate-conventions.py")
    monkeypatch.setattr(vc, "COMMANDS_DIR", tmp_path)
    monkeypatch.setattr(vc, "EXPECTED_COUNT", 2)

    validator = vc.ConventionValidator()
    validator.run()

    count_errors = [e for e in validator.errors if "Expected" in e and "found" in e]
    assert count_errors == [], f"non-command markdown leaked into the count: {count_errors}"


def test_fenced_related_commands_template_ignored(tmp_path, load_script):
    """A generator command's fenced sample Related Commands must not shadow its own.

    pb-new-playbook embeds ``` fenced template blocks with placeholder links
    (- /pb-related-1, no backticks) BEFORE its real section. The scanner used to
    lock onto the first ## Related Commands heading -- the fenced template -- count
    zero real links, and warn "no standard Related Commands section" even though the
    command's own section (backtick links) sits at the end. Fenced lines are skipped.
    """
    content = (
        "# pb-generator\n\n"
        "Here is a template block:\n\n"
        "```markdown\n"
        "## Related Commands\n\n"
        "- /pb-related-1 - [Brief description]\n"
        "- /pb-related-2 - [Brief description]\n"
        "```\n\n"
        "## Related Commands\n\n"
        "- `/pb-evolve` -- Quarterly evolution cycles\n"
        "- `/pb-standards` -- Content quality standards\n"
    )
    path = tmp_path / "pb-generator.md"
    path.write_text(content)

    vc = load_script("validate-conventions.py")
    validator = vc.ConventionValidator()
    validator.validate_related_commands(path, content)

    no_section = [w for w in validator.warnings if "no standard Related Commands" in w]
    assert no_section == [], f"real section shadowed by fenced template: {no_section}"
    assert validator.passed == 1, "expected the real (unfenced) section to count 2 links"
