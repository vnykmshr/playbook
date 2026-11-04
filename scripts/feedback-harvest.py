#!/usr/bin/env python3
"""Harvest playbook feedback from every repo's todos/ and the Claude memory dirs.

Read-only on sources. Finds bullets under a "playbook feedback" heading in
<repos>/*/*/todos/**/*.md and one item per <memory>/*/memory/feedback_*.md,
keys each item on its normalised text, and writes a digest of the keys the
ledger has not dispositioned. Only intake (`/pb-evolve` Step 0) writes the ledger.

Exit: 0 every key dispositioned, 1 undisposed keys or a taken key seen again, 2 instrument fault
(no feedback found at all, a malformed ledger, or any error).

Usage:
    python3 scripts/feedback-harvest.py
    python3 scripts/feedback-harvest.py --repos ~/workspace/github --out /tmp/digest
"""

import argparse
import functools
import hashlib
import os
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

PLAYBOOK = Path(__file__).resolve().parent.parent

# Optional `#`s or `**`, optional `<word> / ` prefix, "playbook feedback", optional
# "(...)", then `:` or `.` with a closing `**` on either side; the rest of the line is
# an inline item. A `#` heading may instead end there. Prose starting with the words
# ("Playbook feedback harvesting runs...") has neither, so it is not a heading.
HEADING = re.compile(
    r"^(?:(?P<h>#{1,6})[ \t]+)?(?:\*\*)?(?:[a-z]+[ \t]*/[ \t]*)?playbook feedback\b(?:[ \t]*\([^)]*\))?"
    r"(?:[ \t]*(?:\*\*[ \t]*)?[:.][ \t]*(?:\*\*)?[ \t]*(?P<rest>.*)|(?(h)[ \t]*(?:\*\*)?[ \t]*|(?!)))$",
    re.IGNORECASE,
)
BULLET = re.compile(r"^(?P<indent>[ \t]*)(?:[-*+]|\d+[.)])[ \t]+(?P<text>.*)$")
MD_HEADING = re.compile(r"^#{1,6}([ \t]|$)")
BOLD_LABEL = re.compile(r"^\*\*[^*]+\*\*")
FENCE = re.compile(r"^ {0,3}(?P<run>`{3,}|~{3,})(?P<info>.*)$")
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
PLACEHOLDER = re.compile(r"^\[[^\]]*\]$")
COMMAND = re.compile(r"\bpb-[a-z0-9]+(?:-[a-z0-9]+)*")
KEY = re.compile(r"^[0-9a-f]{12}$")
DISPOSITIONS = ("taken", "rejected", "deferred")
LEDGER_HEADER = ["key", "disposition", "version", "date"]


class InstrumentFault(Exception):
    """The harvester cannot give a trustworthy answer: exit 2, never 'new items'."""


@dataclass(frozen=True)
class Item:
    key: str
    text: str
    source: str      # org/repo, or memory:<project dir>
    where: str       # path:line
    when: str        # YYYY-MM-DD, prefixed "~" when it is the file's mtime
    memory: bool


def normalise(text: str) -> str:
    """Lowercase; links to their text; dates, emphasis and code marks gone; whitespace collapsed."""
    t = text.lower()
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = ISO_DATE.sub(" ", t)
    t = re.sub(r"[*`]+|~~", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def item_key(text: str) -> str:
    return hashlib.sha256(normalise(text).encode()).hexdigest()[:12]


def unfenced(lines: list[str]) -> list[bool]:
    """Per line: True when it is outside a fenced block (fence lines themselves are False)."""
    out, opener = [], None
    for line in lines:
        m = FENCE.match(line)
        if opener is None:
            if m:
                opener = m.group("run")
                out.append(False)
                continue
            out.append(True)
        else:
            run = m.group("run") if m else ""
            if m and not m.group("info").strip() and run[0] == opener[0] and len(run) >= len(opener):
                opener = None
            out.append(False)
    return out


def extract(text: str) -> tuple[list[tuple[int, str]], list[int]]:
    """(items as (heading line no., text), heading line nos. that yielded no item). Line numbers 1-based."""
    lines = text.split("\n")
    open_ = unfenced(lines)
    items: list[tuple[int, str]] = []
    empty: list[int] = []
    i = 0
    while i < len(lines):
        m = HEADING.match(lines[i]) if open_[i] else None
        if not m:
            i += 1
            continue
        h, found = i, []
        rest = (m.group("rest") or "").strip()
        if rest and not PLACEHOLDER.match(rest):
            found.append(rest)
        cur, base, i = None, None, i + 1
        while i < len(lines) and open_[i]:
            line = lines[i]
            if not line.strip():
                j = next((k for k in range(i + 1, len(lines)) if lines[k].strip()), None)
                if j is None or not open_[j] or not BULLET.match(lines[j]):
                    break
                i += 1
                continue
            b = BULLET.match(line)
            if b and (base is None or len(b.group("indent")) <= base):
                base = len(b.group("indent")) if base is None else base
                if cur:
                    found.append(" ".join(cur))
                cur = [b.group("text").strip()]
            elif MD_HEADING.match(line) or BOLD_LABEL.match(line) or HEADING.match(line):
                break
            elif cur is not None:
                cur.append(line.strip())
            else:
                break
            i += 1
        if cur:
            found.append(" ".join(cur))
        found = [f for f in found if not PLACEHOLDER.match(f)]
        items += [(h + 1, f) for f in found]
        if not found:
            empty.append(h + 1)
    return items, empty


def heading_date(lines: list[str], upto: int, today: str) -> str | None:
    """Date on the nearest markdown heading at or above line `upto` (0-based).

    A date after today is a mention ("v2.1.0 stays on 2026-12-01"), not the entry's date.
    """
    for k in range(upto, -1, -1):
        if MD_HEADING.match(lines[k]):
            dates = [d for d in ISO_DATE.findall(lines[k]) if d <= today]
            if dates:
                return dates[0]
    return None


def mtime_date(path: Path) -> str:
    return "~" + date.fromtimestamp(path.stat().st_mtime).isoformat()


def is_scratchpad(name: str) -> bool:
    return "scratchpad" in name.lower()


def tracked_todos(repo: Path) -> set[str] | None:
    """Paths git tracks under todos/: they came from upstream, so they are untrusted input.

    None when the repo has a .git that git cannot list (dubious ownership, a broken checkout):
    its tracked files cannot be told apart, so the repo is skipped. No .git: nothing is tracked.
    """
    if not (repo / ".git").exists():
        return set()
    r = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-z", "--", "todos"], capture_output=True, text=True
    )
    return set(r.stdout.split("\0")) - {""} if r.returncode == 0 else None


def todo_files(todos: Path, tracked: set[str]):
    """Markdown files under todos/, pruning scratchpad dirs before they are listed."""
    for dirpath, dirnames, filenames in os.walk(todos):
        rel = Path(dirpath).relative_to(todos)
        dirnames[:] = sorted(
            d for d in dirnames
            if not is_scratchpad(d)
            and not (rel == Path(".") and d == "evolve")
            and not (rel == Path("inbox") and d.startswith("harvest-"))
        )
        for f in sorted(filenames):
            if f.endswith(".md") and not is_scratchpad(f):
                path = Path(dirpath) / f
                if str(Path("todos") / rel / f) not in tracked:
                    yield path


def harvest_repos(root: Path) -> tuple[list[Item], list[str], int, list[str]]:
    """(items, headings with no item as path:line, files carrying a heading, repos git could not list)."""
    items, empty, files, unlisted = [], [], 0, []
    for todos in sorted(root.glob("*/*/todos")):
        repo = todos.parent
        if is_scratchpad(str(todos)) or not todos.is_dir():
            continue
        source = f"{repo.parent.name}/{repo.name}"
        tracked = tracked_todos(repo)
        if tracked is None:
            unlisted.append(str(repo))
            continue
        for path in todo_files(todos, tracked):
            try:
                text = path.read_text(errors="replace")
            except OSError:
                continue
            found, none = extract(text)
            if not found and not none:
                continue
            files += 1
            lines = text.split("\n")
            empty += [f"{path}:{n}" for n in none]
            for n, t in found:
                when = heading_date(lines, n - 1, date.today().isoformat()) or mtime_date(path)
                items.append(Item(item_key(t), t, source, f"{path}:{n}", when, False))
    return items, empty, files, unlisted


def harvest_memory(root: Path) -> tuple[list[Item], list[str]]:
    """(one item per feedback_*.md keyed on its description, files with no description).

    The description, not the body: bodies get edited, descriptions rarely.
    """
    items, skipped = [], []
    projects = sorted(p for p in root.iterdir() if not is_scratchpad(p.name)) if root.is_dir() else []
    for path in (f for p in projects for f in sorted((p / "memory").glob("feedback_*.md"))):
        if is_scratchpad(path.name):
            continue
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        m = re.search(r"^description:[ \t]*(.+)$", text, re.MULTILINE)
        if not m:
            skipped.append(str(path))
            continue
        desc = m.group(1).strip().strip("\"'")
        source = f"memory:{path.parent.parent.name}"
        items.append(Item(item_key(desc), desc, source, f"{path}:1", mtime_date(path), True))
    return items, skipped


def private_orgs(playbook: Path) -> frozenset[str]:
    """Orgs listed one per line in <playbook>/todos/evolve/private-orgs: untracked, so no name ships."""
    path = playbook / "todos" / "evolve" / "private-orgs"
    if not path.exists():
        return frozenset()
    lines = (x.strip() for x in path.read_text().split("\n"))
    return frozenset(x for x in lines if x and not x.startswith("#"))


def is_private(source: str, orgs: frozenset[str]) -> bool:
    return any(source.startswith(f"{o}/") or f"-github-{o}-" in source for o in orgs)


def read_ledger(path: Path) -> dict[str, tuple[str, str, str]]:
    """key -> (disposition, version, date). Missing ledger is empty; malformed raises."""
    if not path.exists():
        return {}
    rows = path.read_text().split("\n")
    if rows[0].split("\t") != LEDGER_HEADER:
        raise InstrumentFault(f"{path}:1: header must be {' '.join(LEDGER_HEADER)} (tab-separated)")
    ledger: dict[str, tuple[str, str, str]] = {}
    seen: dict[str, int] = {}
    for n, row in enumerate(rows[1:], start=2):
        if not row.strip():
            continue
        cols = row.split("\t")
        if len(cols) != 4:
            raise InstrumentFault(f"{path}:{n}: {len(cols)} columns, want 4")
        key, disp, version, when = cols
        if not KEY.match(key):
            raise InstrumentFault(f"{path}:{n}: key {key!r} is not 12 hex characters")
        if disp not in DISPOSITIONS and not (disp.startswith("dup-of:") and KEY.match(disp[7:])):
            raise InstrumentFault(f"{path}:{n}: disposition {disp!r}: want {', '.join(DISPOSITIONS)} or dup-of:<key>")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", when):
            raise InstrumentFault(f"{path}:{n}: date {when!r} is not YYYY-MM-DD")
        if key in seen:
            raise InstrumentFault(f"{path}:{n}: key {key} repeats line {seen[key]}; edit that row instead")
        seen[key] = n
        ledger[key] = (disp, version, when)
    for key, (disp, _, _) in ledger.items():
        if disp.startswith("dup-of:") and ledger.get(disp[7:], ("dup-of:",))[0].startswith("dup-of:"):
            raise InstrumentFault(f"{path}:{seen[key]}: {disp} names no key with its own disposition")
    return ledger


def _show(repo: Path, spec: str) -> str | None:
    r = subprocess.run(["git", "-C", str(repo), "show", spec], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def _split(text: str) -> tuple[dict[str, object], list[str]]:
    lines = text.split("\n")
    if lines and lines[0].rstrip() == "---":
        for i, line in enumerate(lines[1:], start=1):
            if re.fullmatch(r"---[ \t\r]*", line):
                import yaml  # here, so a missing PyYAML is a fault (exit 2), not an import crash (exit 1)
                fm = yaml.load("\n".join(lines[1:i]), Loader=yaml.BaseLoader)
                return (fm if isinstance(fm, dict) else {}), [x for x in lines[i + 1:] if x.strip()]
    return {}, [x for x in lines if x.strip()]


@functools.lru_cache(maxsize=None)
def last_bump(playbook: Path, command: str) -> tuple[str, str, str] | None:
    """(date, version, version_notes) of the newest commit that changed `version:` and the body."""
    found = None
    paths = sorted((playbook / "commands").glob(f"*/{command}.md"))
    if paths:
        rel = str(paths[0].relative_to(playbook))
        log = subprocess.run(
            ["git", "-C", str(playbook), "log", "--format=%H %cs", "--", rel], capture_output=True, text=True
        ).stdout.split("\n")
        for line in filter(None, log):
            sha, when = line.split()
            after = _show(playbook, f"{sha}:{rel}")
            if after is None:
                continue
            before = _show(playbook, f"{sha}^:{rel}")
            fa, ba = _split(after)
            fb, bb = _split(before) if before is not None else ({}, [])
            if fa.get("version") != fb.get("version") and ba != bb:
                found = (when, str(fa.get("version")), str(fa.get("version_notes", "")))
                break
    return found


def may_be_fixed(playbook: Path, text: str, newest: str) -> str | None:
    m = COMMAND.search(text)
    if not m or not (bump := last_bump(playbook, m.group(0))):
        return None
    when, version, notes = bump
    if newest.lstrip("~") >= when:
        return None
    notes = notes if len(notes) <= 100 else notes[:99] + "…"
    return f"{m.group(0)} v{version} bumped {when}: {notes}"


def render(
    items: list[Item], ledger: dict[str, tuple[str, str, str]], empty: list[str], skipped: list[str],
    playbook: Path, files: int, orgs: frozenset[str], unlisted: list[str],
) -> tuple[str, int]:
    """(digest markdown, undisposed keys, taken keys seen again)."""
    by_key: dict[str, list[Item]] = defaultdict(list)
    for it in items:
        by_key[it.key].append(it)

    def newest(occ: list[Item]) -> str:
        return max((o.when for o in occ), key=lambda w: w.lstrip("~"))

    def line(key: str, occ: list[Item]) -> list[str]:
        sources = sorted({o.source for o in occ})
        flags = []
        if any(is_private(s, orgs) for s in sources):
            flags.append("private")
        if fixed := may_be_fixed(playbook, occ[0].text, newest(occ)):
            flags.append(f"may be fixed: {fixed}")
        tag = f" [{'; '.join(flags)}]" if flags else ""
        out = [f"- `{key}` {len(sources)} source(s), newest {newest(occ)}{tag}: {occ[0].text}"]
        out += [f"  - {o.source} `{o.where}` {o.when}" for o in sorted(occ, key=lambda o: o.where)]
        return out

    def rank(kv):
        key, occ = kv
        return (-len({o.source for o in occ}), -int(newest(occ).lstrip("~").replace("-", "")), key)

    undisposed = {k: v for k, v in by_key.items() if k not in ledger}
    repo_keys = sorted(((k, v) for k, v in undisposed.items() if not all(o.memory for o in v)), key=rank)
    mem_keys = sorted(((k, v) for k, v in undisposed.items() if all(o.memory for o in v)), key=rank)
    # Only a dated heading can recur: an mtime moves on any edit, so a memory file or an
    # undated note would read as new evidence every time it is touched.
    recurred = [
        (k, v) for k, v in by_key.items()
        if k in ledger and ledger[k][0] == "taken"
        and any(not o.when.startswith("~") and o.when > ledger[k][2] for o in v)
    ]
    headings = len({o.where for o in items if not o.memory}) + len(empty)
    md = [
        f"# Feedback digest {date.today().isoformat()}",
        "",
        f"{headings} headings in {files} files; {len(items)} items, {len(by_key)} keys, "
        f"{len(undisposed)} undisposed, {len(recurred)} seen again, {len({o.source for o in items})} sources.",
        "",
        "## Undisposed: repo notes",
        "",
        *[x for kv in repo_keys for x in line(*kv)],
        "",
        "## Undisposed: memory",
        "",
        *[x for kv in mem_keys for x in line(*kv)],
        "",
        "## Taken, then seen again after the ledger date",
        "",
        *[x for kv in recurred for x in line(*kv)],
        "",
        "## Headings with no item",
        "",
        *[f"- `{e}`" for e in empty],
        "",
        "## Memory files with no description",
        "",
        *[f"- `{s}`" for s in skipped],
        "",
        "## Repos skipped: git could not list their tracked files",
        "",
        *[f"- `{u}`" for u in unlisted],
        "",
    ]
    return "\n".join(md), len(undisposed), len(recurred)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Harvest playbook feedback into a digest of undisposed keys.")
    ap.add_argument("--repos", type=Path, default=Path.home() / "workspace" / "github",
                    help="root holding <org>/<repo>/todos (default ~/workspace/github)")
    ap.add_argument("--memory", type=Path, default=Path.home() / ".claude" / "projects",
                    help="root holding <project>/memory/feedback_*.md (default ~/.claude/projects)")
    ap.add_argument("--playbook", type=Path, default=PLAYBOOK, help="playbook checkout, for command history")
    ap.add_argument("--ledger", type=Path, help="default <playbook>/todos/evolve/harvest-ledger.tsv")
    ap.add_argument("--out", type=Path, help="digest directory (default <playbook>/todos/evolve)")
    args = ap.parse_args(argv)
    ledger_path = args.ledger or args.playbook / "todos" / "evolve" / "harvest-ledger.tsv"
    out = args.out or args.playbook / "todos" / "evolve"
    try:
        ledger = read_ledger(ledger_path)
        items, empty, files, unlisted = harvest_repos(args.repos)
        memory, skipped = harvest_memory(args.memory)
        items += memory
        orgs = private_orgs(args.playbook)
        if not items and not empty:
            raise InstrumentFault(f"no feedback found under {args.repos} or {args.memory}: is the root right?")
        md, undisposed, again = render(items, ledger, empty, skipped, args.playbook, files, orgs, unlisted)
        out.mkdir(parents=True, exist_ok=True)
        digest = out / f"digest-{date.today().isoformat()}.md"
        digest.write_text(md)
    except InstrumentFault as e:
        print(f"feedback-harvest: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # exit 1 means "undisposed keys": a crash must not read as that
        print(f"feedback-harvest: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    print(f"{undisposed} undisposed, {again} seen again, of {len({i.key for i in items})} keys; digest {digest}")
    return 1 if undisposed or again else 0


if __name__ == "__main__":
    sys.exit(main())
