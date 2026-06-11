"""Regression tests for evolution-snapshot.py."""
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "evolution-snapshot.py"


def test_list_runs_on_fresh_checkout(tmp_path):
    """#9: --list must work in a tree with no todos/ (a fresh clone -- todos/ is
    gitignored). The constructor used to mkdir without parents=True and crash."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--list"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "todos" / "evolution-snapshots").is_dir()


def test_cleanup_is_dispatched(tmp_path, monkeypatch, load_script):
    """#10: --cleanup N must actually invoke cleanup, not silently fall through
    to listing snapshots (the flag was defined but never dispatched)."""
    monkeypatch.chdir(tmp_path)
    es = load_script("evolution-snapshot.py")

    calls = []
    monkeypatch.setattr(
        es.EvolutionSnapshot, "cleanup_old_snapshots",
        lambda self, keep: calls.append(keep),
    )
    monkeypatch.setattr(sys, "argv", ["evolution-snapshot.py", "--cleanup", "3"])

    with pytest.raises(SystemExit) as exc:
        es.main()
    assert exc.value.code == 0
    assert calls == [3]
