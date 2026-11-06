#!/usr/bin/env python3
"""
Pins the repo's one-line self-description.

README line 3 opens with it; llms.txt, the reference site's intro page and
book.toml's description repeat it. The book site's subtitle is the book's title, a separate
artifact, and is not pinned here.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
SELF_DESCRIPTION = "Structured Markdown commands for AI-assisted development."


@pytest.mark.parametrize("relpath", ["README.md", "llms.txt", "mdbook/intro.md", "mdbook/book.toml"])
def test_file_carries_the_self_description(relpath):
    text = (ROOT / relpath).read_text()
    assert SELF_DESCRIPTION in text, (
        f"{relpath} no longer carries the self-description {SELF_DESCRIPTION!r}. "
        "Change it in README.md, llms.txt, mdbook/intro.md and mdbook/book.toml together, "
        "then update SELF_DESCRIPTION here."
    )


def test_readme_opens_with_the_self_description():
    assert (ROOT / "README.md").read_text().splitlines()[2].startswith(SELF_DESCRIPTION)
