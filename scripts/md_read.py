"""Markdown as CommonMark renders it, for the convention guards and the validator.

Fences, code spans and sections come from markdown-it-py tokens. A reader that toggles on
fence markers cannot tell an inner fence that opens a block from one that closes it; only
a parser can. Line numbers are 0-based within the text passed in.
"""

import re

from markdown_it import MarkdownIt
from markdown_it.token import Token

_MD = MarkdownIt("commonmark")
_OPENER = re.compile(r" {0,3}(`{3,}|~{3,})(.*)")


def tokens(text: str) -> list[Token]:
    return _MD.parse(text)


def _plain(inline: Token) -> str:
    """An inline token's text with code spans and markup gone, line breaks kept."""
    out = []
    for c in inline.children or []:
        if c.type in ("text", "html_inline"):
            out.append(c.content)
        elif c.type in ("softbreak", "hardbreak"):
            out.append("\n")
    return "".join(out)


def prose_text(text: str) -> list[str]:
    """Rendered prose, one entry per source line: code blocks and code spans removed.

    Raw HTML blocks count as prose, as a line reader sees them.
    """
    out = []
    for t in tokens(text):
        if t.type == "inline":
            out += _plain(t).split("\n")
        elif t.type == "html_block":
            out += t.content.split("\n")
    return out


def fence_problems(text: str) -> list[tuple[int, int, str]]:
    """(line, opener line, "info" | "unclosed") for fenced samples their outer fence cannot hold.

    Inside a fence, a line of the same character, at least the opener's length and
    carrying an info string, is content, so the inner block's bare close ends the outer
    one. The rule is conservative: a sample showing a lone opener line as text trips it
    too, and lengthening its outer fence is harmless. A fence still open at end of text
    fails. Gap, by design: a bare inner opener reads as the outer's close, and nothing in
    the syntax says which was meant.
    """
    lines = text.split("\n")
    problems = []
    for t in tokens(text):
        if t.type != "fence" or not t.map:
            continue
        start, end = t.map
        run = t.markup
        for i, line in enumerate(t.content.split("\n")):
            m = _OPENER.fullmatch(line)
            if m and m.group(1)[0] == run[0] and len(m.group(1)) >= len(run) and m.group(2).strip():
                problems.append((start + 1 + i, start, "info"))
        close = re.compile(r"[ \t>]*" + re.escape(run[0]) + "{%d,}[ \t]*" % len(run))
        if end - 1 == start or not close.fullmatch(lines[end - 1]):
            problems.append((start, start, "unclosed"))
    return problems


def related_commands_count(text: str) -> int:
    """`- `/pb-...`` items under the `## Related Commands` heading, up to the next h1, h2 or rule."""
    toks = tokens(text)
    count, inside = 0, False
    for i, t in enumerate(toks):
        if t.type == "heading_open" and t.tag in ("h1", "h2"):
            inside = t.tag == "h2" and toks[i + 1].content.startswith("Related Commands")
        elif t.type == "hr":
            inside = False
        elif inside and t.type == "list_item_open" and t.markup == "-":
            first = next(x for x in toks[i + 1:] if x.type == "inline")
            count += first.content.startswith("`/pb-")
    return count
