#!/usr/bin/env python3
"""Harvest playbook feedback from every repo's todos/ and the Claude memory dirs.

Read-only on sources. Finds bullets under a "playbook feedback" heading in
<root>/<org>/<repo>/todos/**/*.md and one item per <memory>/*/memory/feedback_*.md,
keys each item on its normalised text, and writes a digest of the keys the
ledger has not dispositioned. Only intake (`/pb-evolve` Step 0) writes the ledger.

Conventions live here; this machine's specifics (roots, private orgs) live in the
untracked todos/evolve/harvest.toml, and flags override it.

Exit: 0 every key dispositioned, 1 undisposed keys or a taken key seen again, 2 instrument fault
(no repo heading found, a malformed ledger, a repo git cannot list, a path that cannot be read,
or any error). An incomplete harvest still writes its digest, so the paths to fix are in it.

Usage:
    python3 scripts/feedback-harvest.py --init     # writes the config once, with derived defaults
    python3 scripts/feedback-harvest.py
    python3 scripts/feedback-harvest.py --repos ~/src --out /tmp/digest
"""

import argparse
import functools
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
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
# A line that starts like a heading (list marker, quote, indent, `#`, emphasis allowed)
# but is not one. Listed in the digest so a shape HEADING drops is seen, never keyed.
NEAR_MISS = re.compile(
    r"^[ \t]{0,3}(?:>[ \t]*)*(?:(?:[-*+]|\d+[.)])[ \t]+)?(?:#{1,6}[ \t]+)?[*_]{0,2}"
    r"(?:[a-z]+[ \t]*/[ \t]*)?playbook[ \t-]+feedback(?![a-z0-9])",
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
    nested: bool = False  # inside a git repo nested under todos/: the owner's private companion


@dataclass
class Harvest:
    items: list[Item]
    empty: list[str]     # headings with no item, path:line
    near: list[str]      # near-miss headings, path:line
    unlisted: list[str]  # repos git could not list
    files: int           # files carrying a heading or a near miss
    unread: list[str] = field(default_factory=list)  # files and dirs that raised on read
    links: list[str] = field(default_factory=list)   # symlinks met and not followed


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


def near_misses(text: str) -> list[int]:
    """1-based numbers of unfenced lines that start like a heading and are not one."""
    lines = text.split("\n")
    return [
        n + 1 for n, (line, ok) in enumerate(zip(lines, unfenced(lines)))
        if ok and NEAR_MISS.match(line) and not HEADING.match(line)
    ]


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


def listing(path: Path, h: Harvest) -> list[os.DirEntry]:
    """The one way this script lists a dir: sorted entries, scratchpad names dropped first.

    A link is recorded and never followed: the scratchpad rule can only see a link's own name.
    A missing path or a file lists nothing; any other OSError is recorded as unread.
    """
    try:
        if path.is_symlink():
            h.links.append(str(path))
            return []
        with os.scandir(path) as it:
            entries = [e for e in it if not is_scratchpad(e.name)]
    except (FileNotFoundError, NotADirectoryError):
        return []
    except OSError:
        h.unread.append(str(path))
        return []
    return sorted(entries, key=lambda e: e.name)


def subdirs(path: Path, h: Harvest) -> list[os.DirEntry]:
    """Real (non-link) subdirs; links among them are recorded."""
    out = []
    for e in listing(path, h):
        if e.is_symlink():
            h.links.append(e.path)
        elif e.is_dir(follow_symlinks=False):
            out.append(e)
    return out


def todo_files(todos: Path, tracked: set[str], h: Harvest):
    """(path, inside a nested repo) per markdown file under todos/, files before subdirs.

    A dir holding .git starts a nested repo; the parent tracks none of its files, so none are
    filtered out as tracked.
    """
    def walk(d: Path, rel: Path, nested: bool):
        entries = listing(d, h)
        nested = nested or any(e.name == ".git" for e in entries)
        for e in entries:
            if e.is_symlink():
                h.links.append(e.path)
            elif e.name.endswith(".md") and e.is_file(follow_symlinks=False):
                if str(Path("todos") / rel / e.name) not in tracked:
                    yield Path(e.path), nested
        for e in entries:
            if e.is_symlink() or not e.is_dir(follow_symlinks=False) or e.name == ".git":
                continue
            if (rel == Path(".") and e.name == "evolve") or (rel == Path("inbox") and e.name.startswith("harvest-")):
                continue
            yield from walk(Path(e.path), rel / e.name, nested)

    yield from walk(todos, Path("."), False)


def todos_dir(repo: Path, h: Harvest) -> Path | None:
    """<repo>/todos when it is a real dir; a link is recorded, an unreadable repo is unread."""
    todos = repo / "todos"
    try:
        mode = todos.lstat().st_mode
    except (FileNotFoundError, NotADirectoryError):
        return None
    except OSError:
        h.unread.append(str(todos))
        return None
    if stat.S_ISLNK(mode):
        h.links.append(str(todos))
        return None
    return todos if stat.S_ISDIR(mode) else None


def harvest_repos(roots: tuple[Path, ...], h: Harvest) -> None:
    for root in (r.resolve() for r in roots):
        if is_scratchpad(str(root)):
            continue
        for org in subdirs(root, h):
            for repo_entry in subdirs(Path(org.path), h):
                repo = Path(repo_entry.path)
                if (todos := todos_dir(repo, h)) is None:
                    continue
                harvest_todos(todos, f"{org.name}/{repo.name}", h)


def harvest_todos(todos: Path, source: str, h: Harvest) -> None:
    repo = todos.parent
    tracked = tracked_todos(repo)
    if tracked is None:
        h.unlisted.append(str(repo))
        return
    for path, nested in todo_files(todos, tracked, h):
        try:
            text = path.read_text(errors="replace")
        except OSError:
            h.unread.append(str(path))
            continue
        found, none = extract(text)
        near = near_misses(text)
        if not found and not none and not near:
            continue
        h.files += 1
        lines = text.split("\n")
        h.empty += [f"{path}:{n}" for n in none]
        h.near += [f"{path}:{n}" for n in near]
        for n, t in found:
            when = heading_date(lines, n - 1, date.today().isoformat()) or mtime_date(path)
            h.items.append(Item(item_key(t), t, source, f"{path}:{n}", when, False, nested))


def memory_files(root: Path, h: Harvest):
    """feedback_*.md per project memory dir, through listing(): links recorded, never followed."""
    root = root.resolve()
    if is_scratchpad(str(root)):
        return
    for p in subdirs(root, h):
        for e in listing(Path(p.path) / "memory", h):
            if not (e.name.startswith("feedback_") and e.name.endswith(".md")):
                continue
            if e.is_symlink():
                h.links.append(e.path)
            elif e.is_file(follow_symlinks=False):
                yield Path(e.path)


def harvest_memory(root: Path, h: Harvest) -> tuple[list[Item], list[str]]:
    """(one item per feedback_*.md keyed on its description, files with no description).

    The description, not the body: bodies get edited, descriptions rarely. A project dir for a
    path under a todos/ (name has -todos- or ends -todos) is the owner's private companion.
    """
    items, skipped = [], []
    for path in memory_files(root, h):
        try:
            text = path.read_text(errors="replace")
        except OSError:
            h.unread.append(str(path))
            continue
        m = re.search(r"^description:[ \t]*(.+)$", text, re.MULTILINE)
        if not m:
            skipped.append(str(path))
            continue
        desc = m.group(1).strip().strip("\"'")
        d = path.parent.parent.name
        nested = "-todos-" in d.lower() or d.lower().endswith("-todos")
        items.append(Item(item_key(desc), desc, f"memory:{d}", f"{path}:1", mtime_date(path), True, nested))
    return items, skipped


@dataclass(frozen=True)
class Config:
    repos: tuple[Path, ...]
    memory: Path
    private: frozenset[str]  # lowercased org names
    note: str                # the digest says where private orgs came from, or that nothing was read

    @functools.cached_property
    def prefixes(self) -> tuple[str, ...]:
        """Memory dir prefixes for <root>/<org>, from both the absolute and the resolved root:
        Claude Code may record either, and an extra prefix can only add a private flag."""
        forms = {f for r in self.repos for f in (r.absolute(), r.resolve())}
        return tuple(sorted({project_dir(f / o).lower() for f in forms for o in self.private}))


def _strings(cfg: dict, key: str, path: Path) -> list[str]:
    v = cfg.get(key, [])
    if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
        raise InstrumentFault(f"{path}: {key} must be a list of strings")
    return v


def load_config(path: Path, repos: list[Path] | None, memory: Path | None) -> Config:
    """Flags win over the file; no root from either is a fault, never a guessed default."""
    cfg: dict = {}
    if path.exists():
        import tomllib
        try:
            cfg = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as e:
            raise InstrumentFault(f"{path}: {e}") from e
    if path.exists() and "private" not in cfg:
        raise InstrumentFault(f"{path}: private is required (an empty list is fine): leaving it out would flag nothing")
    roots = repos or [Path(r).expanduser() for r in _strings(cfg, "repos", path)]
    if not roots:
        raise InstrumentFault(f"no repos root: pass --repos, or run --init to write {path}")
    mem = memory or Path(cfg.get("memory", "~/.claude/projects")).expanduser()
    orgs = frozenset(o.strip().lower() for o in _strings(cfg, "private", path) if o.strip())
    note = f"private orgs: {len(orgs)} from {path}" if path.exists() else f"config missing ({path}): no source flagged by org"
    return Config(tuple(roots), mem, orgs, note)


def init_config(path: Path, playbook: Path) -> str:
    """Write the config once. The root is derived from the convention <root>/<org>/<playbook>."""
    if path.exists():
        raise InstrumentFault(f"{path} exists; edit it (--init never overwrites)")
    root = playbook.resolve().parent.parent
    home = Path.home().resolve()
    shown = f"~/{root.relative_to(home)}" if root.is_relative_to(home) else str(root)
    text = (
        f"repos = [{json.dumps(shown)}]   # roots holding <org>/<repo>/todos/\n"
        'memory = "~/.claude/projects"   # Claude Code\'s default\n'
        "private = []                    # orgs whose notes are flagged private\n"
    )
    import tomllib
    try:
        ok = tomllib.loads(text)["repos"] == [shown]
    except tomllib.TOMLDecodeError:
        ok = False
    if not ok:
        raise InstrumentFault(f"the root {shown!r} does not survive TOML quoting; write {path} by hand")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return text


def project_dir(path: Path) -> str:
    """Claude Code's memory dir name for a working directory: every non-alphanumeric becomes -."""
    return re.sub(r"[^A-Za-z0-9]", "-", str(path))


def is_private(source: str, cfg: Config) -> bool:
    """A private org's repo, or a memory dir for a path under <root>/<org>. Dir names encode
    / as -, so org `acme` also flags a sibling org `acme-labs`: the ambiguity errs private."""
    if not source.startswith("memory:"):
        return source.split("/", 1)[0].lower() in cfg.private
    d = source[len("memory:"):].lower()
    return any(d == p or d.startswith(p + "-") for p in cfg.prefixes)


Ledger = dict[str, tuple[str, str, str, int]]


def read_ledger(path: Path) -> Ledger:
    """key -> (disposition, version, date, line). Missing ledger is empty; malformed raises."""
    if not path.exists():
        return {}
    rows = path.read_text().split("\n")
    if rows[0].split("\t") != LEDGER_HEADER:
        raise InstrumentFault(f"{path}:1: header must be {' '.join(LEDGER_HEADER)} (tab-separated)")
    ledger: Ledger = {}
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
        if key in ledger:
            raise InstrumentFault(f"{path}:{n}: key {key} repeats line {ledger[key][3]}; edit that row instead")
        ledger[key] = (disp, version, when, n)
    for disp, _, _, n in ledger.values():
        target = ledger.get(disp[7:]) if disp.startswith("dup-of:") else None
        if disp.startswith("dup-of:") and (target is None or target[0].startswith("dup-of:")):
            raise InstrumentFault(f"{path}:{n}: {disp} names no key with its own disposition")
    return ledger


def ruling(ledger: Ledger, key: str) -> tuple[str, str] | None:
    """(disposition, date) for a key, read through dup-of to its representative."""
    row = ledger.get(key)
    if row and row[0].startswith("dup-of:"):
        row = ledger[row[0][7:]]
    return (row[0], row[2]) if row else None


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
    h: Harvest, skipped: list[str], ledger: Ledger, playbook: Path, cfg: Config,
) -> tuple[str, int, int]:
    """(digest markdown, undisposed keys, taken keys seen again)."""
    by_key: dict[str, list[Item]] = defaultdict(list)
    for it in h.items:
        by_key[it.key].append(it)

    def newest(occ: list[Item]) -> str:
        return max((o.when for o in occ), key=lambda w: w.lstrip("~"))

    def line(key: str, occ: list[Item]) -> list[str]:
        sources = sorted({o.source for o in occ})
        flags = []
        if any(o.nested or is_private(o.source, cfg) for o in occ):
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

    def seen_again(occ: list[Item], r: tuple[str, str] | None) -> bool:
        # Only a dated heading can recur: an mtime moves on any edit, so a memory file or an
        # undated note would read as new evidence every time it is touched.
        return bool(r) and r[0] == "taken" and any(not o.when.startswith("~") and o.when > r[1] for o in occ)

    undisposed = {k: v for k, v in by_key.items() if k not in ledger}
    repo_keys = sorted(((k, v) for k, v in undisposed.items() if not all(o.memory for o in v)), key=rank)
    mem_keys = sorted(((k, v) for k, v in undisposed.items() if all(o.memory for o in v)), key=rank)
    recurred = [(k, v) for k, v in by_key.items() if seen_again(v, ruling(ledger, k))]
    headings = len({o.where for o in h.items if not o.memory}) + len(h.empty)
    md = [
        f"# Feedback digest {date.today().isoformat()}",
        "",
        f"{headings} headings in {h.files} files; {len(h.items)} items, {len(by_key)} keys, "
        f"{len(undisposed)} undisposed, {len(recurred)} seen again, {len({o.source for o in h.items})} sources; "
        f"{len(h.near)} near misses, {len(h.unlisted)} repos unread, {len(h.unread)} paths unread, "
        f"{len(h.links)} links not followed. {cfg.note}.",
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
        *[f"- `{e}`" for e in h.empty],
        "",
        "## Near-miss headings (start like the heading, are not one; no key, no exit)",
        "",
        *[f"- `{n}`" for n in h.near],
        "",
        "## Memory files with no description",
        "",
        *[f"- `{s}`" for s in skipped],
        "",
        "## Repos unread: git could not list their tracked files",
        "",
        *[f"- `{u}`" for u in h.unlisted],
        "",
        "## Paths unread: raised on read",
        "",
        *[f"- `{u}`" for u in h.unread],
        "",
        "## Links not followed (no exit)",
        "",
        *[f"- `{x}`" for x in h.links],
        "",
    ]
    return "\n".join(md), len(undisposed), len(recurred)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Harvest playbook feedback into a digest of undisposed keys.")
    ap.add_argument("--repos", type=Path, action="append",
                    help="a root holding <org>/<repo>/todos; repeatable (default: repos in the config)")
    ap.add_argument("--memory", type=Path,
                    help="root holding <project>/memory/feedback_*.md (default: config, else ~/.claude/projects)")
    ap.add_argument("--playbook", type=Path, default=PLAYBOOK, help="playbook checkout, for command history")
    ap.add_argument("--config", type=Path, help="default <playbook>/todos/evolve/harvest.toml (untracked)")
    ap.add_argument("--ledger", type=Path, help="default <playbook>/todos/evolve/harvest-ledger.tsv")
    ap.add_argument("--out", type=Path, help="digest directory (default <playbook>/todos/evolve)")
    ap.add_argument("--init", action="store_true", help="write the config with derived defaults, then stop")
    args = ap.parse_args(argv)
    config = args.config or args.playbook / "todos" / "evolve" / "harvest.toml"
    if args.init:
        try:
            print(f"wrote {config}:\n{init_config(config, args.playbook)}add private orgs, if any, to `private`")
        except InstrumentFault as e:
            print(f"feedback-harvest: {e}", file=sys.stderr)
            return 2
        return 0
    ledger_path = args.ledger or args.playbook / "todos" / "evolve" / "harvest-ledger.tsv"
    out = args.out or args.playbook / "todos" / "evolve"
    try:
        if args.config is not None and not config.exists():
            raise InstrumentFault(f"{config}: --config names no file; a typo here would flag nothing")
        cfg = load_config(config, args.repos, args.memory)
        ledger = read_ledger(ledger_path)
        h = Harvest([], [], [], [], 0)
        harvest_repos(cfg.repos, h)
        memory, skipped = harvest_memory(cfg.memory, h)
        h.items += memory
        md, undisposed, again = render(h, skipped, ledger, args.playbook, cfg)
        out.mkdir(parents=True, exist_ok=True)
        digest = out / f"digest-{date.today().isoformat()}.md"
        digest.write_text(md)
    except InstrumentFault as e:
        print(f"feedback-harvest: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # exit 1 means "undisposed keys": a crash must not read as that
        print(f"feedback-harvest: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    print(f"{undisposed} undisposed, {again} seen again, of {len({i.key for i in h.items})} keys; "
          f"{len(h.near)} near misses; digest {digest}")
    # An incomplete harvest is never a close, whatever the ledger says: name each cause, exit 2.
    causes = [f"{r}: git cannot list its files; run `git -C {r} status`, fix, rerun" for r in h.unlisted]
    causes += [f"{u}: could not be read" for u in h.unread]
    if not any(not o.memory for o in h.items) and not h.empty:
        causes.append(f"no repo heading matched under {', '.join(map(str, cfg.repos))}; {len(h.near)} near misses listed: "
                      "is the root right, or did a heading shape change?")
    for c in causes:
        print(f"feedback-harvest: {c}", file=sys.stderr)
    return 2 if causes else 1 if undisposed or again else 0


if __name__ == "__main__":
    sys.exit(main())
