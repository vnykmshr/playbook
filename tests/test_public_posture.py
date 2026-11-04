"""Tracked files carry conventions, never this machine's specifics.

The names to look for come from the untracked harvester config, read with the harvester's
own loader, so this file names nothing. Without that config (CI) the name check skips.
"""
import subprocess
from pathlib import Path

import pytest

import feedback_harvest as fh  # registered by conftest

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "todos" / "evolve" / "harvest.toml"


def tracked_hits(needle: str, *flags: str) -> list[str]:
    r = subprocess.run(
        ["git", "-C", str(REPO), "grep", "-n", "-I", "-F", *flags, "-e", needle, "--", "."],
        capture_output=True, text=True,
    )
    assert r.returncode in (0, 1), r.stderr
    return r.stdout.splitlines()


def test_no_home_path_in_tracked_files():
    home = Path.home()
    assert not tracked_hits(str(home)), "a home path in a tracked file names this machine"
    assert not tracked_hits(fh.project_dir(home) + "-"), "the same, in Claude Code's project-dir form"


def test_no_private_org_or_root_from_the_local_config_in_tracked_files():
    if not CONFIG.exists():
        pytest.skip(f"no {CONFIG.relative_to(REPO)}: the check runs where the config lives")
    cfg = fh.load_config(CONFIG, None, None)
    home = Path.home()
    roots = {str(r) for r in cfg.repos} | {f"~/{r.relative_to(home)}" for r in cfg.repos if r.is_relative_to(home)}
    hits = {o: tracked_hits(o, "-i", "-w") for o in cfg.private}
    if cfg.memory != home / ".claude" / "projects":
        roots.add(str(cfg.memory))
    hits |= {r: tracked_hits(r) for r in roots}
    assert not {k: v for k, v in hits.items() if v}


# Synthetic paths a test needs as input, by file:line text. Anything else shaped like a home
# path names a machine.
# Built from parts so this line is not a hit itself.
HOME_PATH_FIXTURES = {("tests/test_feedback_harvest.py", "/".join(["", "home", "a.b", ""]))}


def test_no_users_home_path_in_tracked_files():
    """Any user's home, not only this runner's: CI's HOME is not the author's."""
    r = subprocess.run(
        ["git", "-C", str(REPO), "grep", "-n", "-I", "-E", r"/(Users|home)/[A-Za-z0-9._-]+/", "--", "."],
        capture_output=True, text=True,
    )
    assert r.returncode in (0, 1), r.stderr
    hits = [h for h in r.stdout.splitlines()
            if not any(h.startswith(f"{path}:") and part in h for path, part in HOME_PATH_FIXTURES)]
    assert not hits, f"home paths in tracked files: {hits}"


BOOK_SCRIPT_HOSTS = {"static.cloudflareinsights.com"}


def test_book_pages_load_scripts_only_from_known_hosts():
    import re
    found = set()
    for page in (REPO / "book").glob("*.html"):
        for src in re.findall(r'<script[^>]*\bsrc="([^"]+)"', page.read_text()):
            if "://" in src:
                found.add(src.split("://", 1)[1].split("/", 1)[0])
    assert found <= BOOK_SCRIPT_HOSTS, f"third-party script hosts not on the list: {found - BOOK_SCRIPT_HOSTS}"

