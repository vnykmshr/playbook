"""uninstall.sh removes only the links install.sh made.

Runs the real script against a throwaway HOME, so nothing under the real
~/.claude is touched.
"""
import os
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def run_uninstall(home: Path, script_root: Path = REPO) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(script_root / "scripts" / "uninstall.sh")],
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
    assert "Skipped: 1" in result.stdout, "a link left installed must not be reported as not found"


def test_uninstall_owns_links_made_through_a_symlinked_repo_path(tmp_path: Path):
    alias = tmp_path / "alias"
    alias.symlink_to(REPO)
    target = tmp_path / ".claude" / "commands"
    target.mkdir(parents=True)
    link = target / "pb-commit.md"
    link.symlink_to(alias / "commands" / "development" / "pb-commit.md")

    result = run_uninstall(tmp_path)

    assert result.returncode == 0, result.stderr
    assert not link.is_symlink(), "installed via a symlinked path, still ours"


def test_uninstall_run_through_a_symlinked_repo_path(tmp_path: Path):
    alias = tmp_path / "alias"
    alias.symlink_to(REPO)
    target = tmp_path / ".claude" / "commands"
    target.mkdir(parents=True)
    link = target / "pb-commit.md"
    link.symlink_to(REPO / "commands" / "development" / "pb-commit.md")

    result = run_uninstall(tmp_path, script_root=alias)

    assert result.returncode == 0, result.stderr
    assert not link.is_symlink(), "uninstall run via a symlinked path, still ours"


def test_uninstall_survives_a_dangling_same_named_link(tmp_path: Path):
    target = tmp_path / ".claude" / "commands"
    target.mkdir(parents=True)
    dangling = target / "pb-review.md"
    dangling.symlink_to(tmp_path / "gone" / "pb-review.md")

    result = run_uninstall(tmp_path)

    assert result.returncode == 0, result.stderr
    assert dangling.is_symlink(), "a dangling link pointing elsewhere is not ours"


def test_uninstall_removes_a_link_into_a_moved_category(tmp_path: Path):
    target = tmp_path / ".claude" / "commands"
    target.mkdir(parents=True)
    link = target / "pb-commit.md"
    link.symlink_to(REPO / "commands" / "oldcat" / "pb-commit.md")

    result = run_uninstall(tmp_path)

    assert result.returncode == 0, result.stderr
    assert not link.is_symlink(), "a dangling link into this repo's commands/ is still ours"


def test_uninstall_removes_an_alias_link_into_a_moved_category(tmp_path: Path):
    alias = tmp_path / "alias"
    alias.symlink_to(REPO)
    target = tmp_path / ".claude" / "commands"
    target.mkdir(parents=True)
    link = target / "pb-commit.md"
    link.symlink_to(alias / "commands" / "oldcat" / "pb-commit.md")

    result = run_uninstall(tmp_path)

    assert result.returncode == 0, result.stderr
    assert not link.is_symlink(), "via an alias, a dangling link into commands/ is still ours"


def owned(link: Path, owner: Path, depth: int) -> bool:
    lib = REPO / "scripts" / "lib" / "link-owner.sh"
    script = 'source "$1"; link_owned_by "$2" "$(cd "$3" && pwd -P)" "$4"'
    return subprocess.run(
        ["bash", "-c", script, "_", str(lib), str(link), str(owner), str(depth)],
        capture_output=True,
    ).returncode == 0


def test_link_owner_predicate(tmp_path: Path):
    skills = REPO / "skills"
    cases = {
        "skill": (skills / "pb-threat-hunt", skills, 1, True),
        "retired skill": (skills / "pb-gone", skills, 1, True),
        "command": (REPO / "commands" / "development" / "pb-commit.md", REPO / "commands", 2, True),
        "foreign skill": (tmp_path / "pb-threat-hunt", skills, 1, False),
        "dangling elsewhere": (tmp_path / "gone" / "pb-commit.md", REPO / "commands", 2, False),
    }
    wrong = []
    for name, (dest, owner, depth, want) in cases.items():
        link = tmp_path / f"link-{name.replace(' ', '-')}"
        link.symlink_to(dest)
        if owned(link, owner, depth) is not want:
            wrong.append(name)
    assert not wrong, f"link_owned_by misjudged: {wrong}"
