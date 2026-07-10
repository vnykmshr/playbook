#!/usr/bin/env python3
"""
Regression guard for the pb-handcraft <-> pb-voice delegation (handcraft v1.5.0 /
voice v2.3.0).

pb-voice is the single canonical prose-tell engine. pb-handcraft must fire it as a
required lens and must NOT re-list voice's prose-tell categories inline -- that
duplication is exactly what these tests exist to keep from growing back.
"""

from pathlib import Path

COMMANDS = Path(__file__).parent.parent / "commands"
HANDCRAFT = COMMANDS / "development" / "pb-handcraft.md"
VOICE = COMMANDS / "reviews" / "pb-voice.md"


def test_command_files_exist():
    assert HANDCRAFT.exists(), "pb-handcraft.md missing"
    assert VOICE.exists(), "pb-voice.md missing"


def test_handcraft_fires_voice_as_required_lens():
    """Lens 2 must delegate prose tells to the voice pass, unconditionally."""
    text = HANDCRAFT.read_text()
    assert "voice pass" in text.lower(), "handcraft must reference running the voice pass"
    assert "/pb-voice" in text, "handcraft must name /pb-voice as the prose engine"
    # The old conditional wording is what kept it from firing every time.
    assert "has been configured" not in text, (
        "voice pass must be a required lens, not conditional on configuration"
    )


def test_handcraft_does_not_relist_voice_categories():
    """The duplicated prose/structure/typography tell blocks must stay delegated."""
    text = HANDCRAFT.read_text()
    for banned in ("**Prose tells:**", "**Structure tells:**", "**Typography tells:**"):
        assert banned not in text, (
            f"{banned} belongs to pb-voice; handcraft must delegate, not re-list"
        )


def test_voice_carries_shapes_over_words_meta_principle():
    """The meta-principle is what makes a static word list safe to delegate to."""
    text = VOICE.read_text().lower()
    assert "rotate" in text and "blocklist" in text, (
        "voice must carry the shapes-over-words / words-rotate meta-principle"
    )


def test_bidirectional_related_links():
    """handcraft <-> voice must each name the other."""
    assert "pb-voice" in HANDCRAFT.read_text(), "handcraft must link pb-voice"
    assert "pb-handcraft" in VOICE.read_text(), "voice must link pb-handcraft"


def test_delegated_tells_exist_in_voice():
    """Tells handcraft cites as voice's must actually live in voice (guards the
    dedup's real failure mode: citing a category that lost/never-had the tell)."""
    handcraft = HANDCRAFT.read_text()
    voice = VOICE.read_text().lower()
    # Lens 3 delegates "repeated section anatomy" to voice Cat 2.
    if "section anatomy" in handcraft:
        assert "section anatomy" in voice, (
            "handcraft cites 'section anatomy' as voice's, but voice does not define it"
        )
