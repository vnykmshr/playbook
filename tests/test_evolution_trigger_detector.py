"""Regression tests for evolution-trigger-detector.py."""


def test_staleness_counts_unquoted_dates(tmp_path, load_script, make_command):
    """#4: a stale last_reviewed must be counted regardless of YAML quoting.

    The old regex matched double-quoted dates only, so unquoted/single-quoted
    entries were silently dropped -- deflating the count and able to suppress the
    >25% staleness trigger entirely.
    """
    commands = tmp_path / "commands" / "development"
    commands.mkdir(parents=True)
    make_command(commands, "pb-a", last_reviewed="2020-01-01")  # unquoted, stale
    make_command(commands, "pb-b", last_reviewed="2020-01-01")  # unquoted, stale

    det = load_script("evolution-trigger-detector.py")
    detector = det.EvolutionTriggerDetector()
    detector.commands_dir = tmp_path / "commands"

    result = detector.check_command_staleness()
    assert result is not None, "unquoted stale dates were not counted"
    assert result["stale_count"] == 2


def test_version_check_does_not_guess(tmp_path, monkeypatch, load_script):
    """#14: the version check must not turn document order into a recency claim.

    A CHANGELOG that mentions an older version before a newer one used to fire a
    (wrong) high-severity version_upgrade trigger reporting the older version.
    The honest check returns None.
    """
    (tmp_path / "CHANGELOG.md").write_text(
        "Migrated from Claude 4.5 to Claude 4.6 in this release.\n"
    )
    monkeypatch.chdir(tmp_path)

    det = load_script("evolution-trigger-detector.py")
    detector = det.EvolutionTriggerDetector()
    assert detector.check_claude_version_change() is None
