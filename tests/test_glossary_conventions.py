#!/usr/bin/env python3
"""
Regression guard for docs/glossary.md.

The glossary rotted once, badly: a 23-row table restating command titles and
descriptions went stale everywhere at once, and one row published the wrong
description for /pb-review on the public site. A corpus-wide hygiene sweep
touched the file a day earlier and caught none of it -- because nothing in it
was checkable.

The page's rule is that every claim is either definitionally stable or
machine-checked. These tests are the "machine-checked" half. They do not
judge prose; they enforce that the categories of fact which cannot be verified
stay out of the file.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
GLOSSARY = ROOT / "docs" / "glossary.md"
COMMANDS = ROOT / "commands"


def _text():
    return GLOSSARY.read_text()


def test_glossary_exists():
    assert GLOSSARY.exists(), "docs/glossary.md missing"


def test_every_command_mention_resolves():
    """A bare /pb-name mention must name a command that exists.

    check-links.py only validates markdown hrefs in built HTML, so prose
    mentions like `/pb-review` are invisible to it. This closes that gap --
    it is the check that would have caught the /pb-review misroute.
    """
    known = {p.stem for p in COMMANDS.rglob("pb-*.md")}
    assert known, "no commands found -- test would pass vacuously"

    # Strip trailing hyphens left by prose wildcards (e.g. /pb-patterns-*).
    mentioned = {str(m).rstrip("-") for m in re.findall(r"/(pb-[a-z0-9-]+)", _text())}

    missing = sorted(m for m in mentioned if m not in known)
    assert not missing, (
        f"glossary names commands that do not exist: {missing}. "
        "Renames are the failure mode this file has already suffered."
    )


def test_no_command_title_table():
    """No table row may map a command to its title or description.

    This is the exact shape that rotted: `| /pb-x | Some Title | Purpose |`.
    Command titles live in each command's front matter and change on rename;
    a second copy here cannot be kept honest.
    """
    offenders = [
        line.strip()
        for line in _text().splitlines()
        if line.lstrip().startswith("|") and "/pb-" in line
    ]
    assert not offenders, (
        "glossary must not tabulate commands against titles or descriptions; "
        f"found {len(offenders)}: {offenders[:3]}"
    )


def test_no_version_numbers():
    """Version strings date the page the moment the next release ships."""
    versions = re.findall(r"\bv\d+\.\d+\.\d+\b", _text())
    assert not versions, (
        f"glossary must not cite version numbers: {sorted(set(versions))}"
    )


def test_no_command_or_corpus_counts():
    """Counts of commands, personas, or skills go stale on the next addition."""
    counts = re.findall(
        r"\b\d+\s+(?:commands?|personas?|skills?|categories)\b", _text(), re.I
    )
    assert not counts, f"glossary must not state corpus counts: {counts}"


def test_states_its_own_rule():
    """The rule is the mechanism; if it is deleted, the guard loses its anchor."""
    text = _text().lower()
    assert "machine-checked" in text, (
        "glossary must state the definitionally-stable-or-machine-checked rule"
    )
