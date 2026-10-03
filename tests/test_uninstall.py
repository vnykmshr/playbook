"""uninstall.sh removes only the links install.sh made.

Runs the real script against a throwaway HOME, so nothing under the real
~/.claude is touched.
"""
import os
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def run_uninstall(home: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(REPO / "scripts" / "uninstall.sh")],
        env={**os.environ, "HOME": str(home)},
        capture_output=True,
        text=True,
    )


def test_uninstall_keeps_foreign_symlinks(tmp_path: Path):
    target = tmp_path / ".claude" / "commands"
    target.mkdir(parents=True)
    ours = target / "pb-commit.md"
    ours.symlink_to(REPO / "commands" / "development" / "pb-commit.md")
    foreign_src = tmp_path / "elsewhere" / "pb-review.md"
    foreign_src.parent.mkdir()
    _ = foreign_src.write_text("someone else's command\n")
    foreign = target / "pb-review.md"
    foreign.symlink_to(foreign_src)

    result = run_uninstall(tmp_path)

    assert result.returncode == 0, result.stderr
    assert not ours.is_symlink(), "a link into this repo should be removed"
    assert foreign.is_symlink(), "a same-named link pointing elsewhere must survive"
