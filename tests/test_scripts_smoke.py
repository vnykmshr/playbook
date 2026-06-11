"""Smoke tests: the read-only tooling entry points run cleanly.

Catches the crash-on-fresh-checkout / missing-dependency class of bug that
pure-function unit tests miss, by invoking the real entry points via subprocess.
Read-only entry points only -- nothing here writes under todos/. As path-bug
fixes land (e.g. evolution-snapshot --list), their entry points join this list.
"""
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent

READ_ONLY_ENTRYPOINTS = [
    ["scripts/validate-conventions.py"],
    ["scripts/evolve.py", "--validate"],
]


@pytest.mark.parametrize(
    "argv", READ_ONLY_ENTRYPOINTS, ids=lambda a: Path(a[0]).name
)
def test_entrypoint_exits_clean(argv):
    result = subprocess.run(
        [sys.executable, *argv],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"{' '.join(argv)} exited {result.returncode}\n{result.stderr}"
    )
