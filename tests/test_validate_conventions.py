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
