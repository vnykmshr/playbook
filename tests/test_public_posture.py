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
    assert not tracked_hits(str(Path.home())), "a home path in a tracked file names this machine"


def test_no_private_org_or_root_from_the_local_config_in_tracked_files():
    if not CONFIG.exists():
        pytest.skip(f"no {CONFIG.relative_to(REPO)}: the check runs where the config lives")
    cfg = fh.load_config(CONFIG, None, None)
    home = Path.home()
    roots = {str(r) for r in cfg.repos} | {f"~/{r.relative_to(home)}" for r in cfg.repos if r.is_relative_to(home)}
    hits = {o: tracked_hits(o, "-i", "-w") for o in cfg.private}
    hits |= {r: tracked_hits(r) for r in roots}
    assert not {k: v for k, v in hits.items() if v}
