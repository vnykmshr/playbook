"""Regression tests for evolution-log.py main() exit codes and arg handling.

Both bugs live in main()'s dispatch, so these drive the real entry point via
subprocess in an isolated cwd (the audit log is a cwd-relative path).
"""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "evolution-log.py"


def _run(args, cwd):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def test_failed_mutation_exits_nonzero(tmp_path):
    """#2: recording a change against a nonexistent cycle must exit non-zero,
    not print an error and exit 0 (which lets a chained workflow proceed past a
    write that never happened)."""
    result = _run(
        ["--record-change", "pb-x", "--cycle", "Nope", "--field", "f",
         "--before", "a", "--after", "b", "--rationale", "r"],
        cwd=tmp_path,
    )
    assert result.returncode == 1, result.stdout + result.stderr


def test_empty_before_is_accepted(tmp_path):
    """#11: an empty --before (recording a field that was previously unset) is a
    valid value, not a missing argument. It must clear the arg check and reach
    the cycle lookup."""
    result = _run(
        ["--record-change", "pb-x", "--cycle", "Nope", "--field", "f",
         "--before", "", "--after", "b", "--rationale", "r"],
        cwd=tmp_path,
    )
    assert "Missing required arguments" not in result.stdout, result.stdout
