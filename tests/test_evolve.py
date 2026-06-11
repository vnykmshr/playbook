"""Regression tests for evolve.py metadata-validation robustness."""


def test_validate_tolerates_yaml_native_date_and_bad_related(
    tmp_path, load_script, make_command
):
    """#3: an unquoted YAML date parses to a datetime.date and must not crash the
    validator. #5: a null or string related_commands must be flagged as not-a-list
    -- never crash on, nor false-positive against, the self-reference check."""
    commands = tmp_path / "commands" / "development"
    commands.mkdir(parents=True)

    make_command(commands, "pb-unquoted-date", last_reviewed="2026-06-10")  # unquoted
    make_command(commands, "pb-null-related", related_commands="")           # YAML null
    make_command(commands, "pb-str-related", related_commands='"see pb-str-related docs"')

    evolve = load_script("evolve.py")
    engine = evolve.PlaybookEvolutionEngine(root_dir=str(tmp_path))
    engine.load_all_commands()

    issues = engine.validate_metadata()  # must not raise

    # #3: unquoted date accepted, not flagged as a bad format
    assert not any("last_reviewed date format" in i for i in issues["pb-unquoted-date.md"])
    # #5a: null reported as not-a-list (and did not crash)
    assert any("must be a list" in i for i in issues["pb-null-related.md"])
    # #5b: a string is not-a-list, NOT a false CIRCULAR
    str_issues = issues["pb-str-related.md"]
    assert any("must be a list" in i for i in str_issues)
    assert not any("CIRCULAR" in i for i in str_issues)
