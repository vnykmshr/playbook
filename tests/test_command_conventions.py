#!/usr/bin/env python3
"""
Convention validation tests for playbook command files.

Verifies all command files follow audit conventions established in v2.8.0:
- Resource Hint present with valid model tier
- When to Use section present (or recognized variant)
- Related Commands count within limits
- Expected command count
- Metadata model_hint matches body Resource Hint (consistency)
"""

import functools
import re
import subprocess
from pathlib import Path

import pytest
import yaml

COMMANDS_DIR = Path(__file__).parent.parent / "commands"
EXPECTED_COUNT = 116  # 118 - pb-guide-go, pb-guide-python

# Hub commands allowed to exceed the 5-link limit
HUB_COMMANDS = {"pb-patterns.md"}
RELATED_LIMIT = 5
HUB_RELATED_LIMIT = 10

VALID_MODELS = {"opus", "sonnet", "haiku"}

WHEN_TO_USE_VARIANTS = [
    "## when to use",
    "## when to read",
    "## when to write",
    "## when to deprecate",
    "## when to optimize",
    "## when to create",
    "### when to use",
    "**when to use",
]


def get_command_files():
    """Return sorted list of all command markdown files."""
    return sorted(COMMANDS_DIR.rglob("*.md"))


REPO_ROOT = COMMANDS_DIR.parent

# Substantive edits that predate this guard and never bumped their review date.
# These are real debt, not exemptions: the list must only ever shrink. Bumping a
# file's last_reviewed removes it here, and test_baseline_only_shrinks fails if
# an entry is fixed but left behind.
REVIEW_DATE_BASELINE = {
    "pb-adr.md",
    "pb-design-rules.md",
    "pb-performance.md",
    "pb-preamble.md",
    "pb-release.md",
    "pb-threat-hunt.md",
}


def git(*args: str) -> str:
    """Run git at the repo root.

    Raises if git is unavailable rather than skipping. A check that passes
    silently when it cannot run reports the same result for healthy and broken.
    """
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def split_front_matter(text: str) -> tuple[str, str]:
    """(front matter, body), split at the closing `---` by position.

    Position, not key shape: command bodies carry lines like `name: node1` inside
    YAML examples, and a key-prefix filter reads those as metadata. The closer
    may carry trailing whitespace (MD009 allows two spaces and skips front
    matter); matching it exactly would move the split to a body rule.
    """
    lines = text.split("\n")
    if lines and lines[0].rstrip() == "---":
        for i, line in enumerate(lines[1:], start=1):
            if re.fullmatch(r"---[ \t\r]*", line):
                return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return "", text


def body_lines(text: str) -> list[str]:
    """Non-blank body lines: what a substantive edit changes. A blank-line fix is not one."""
    return [line for line in split_front_matter(text)[1].splitlines() if line.strip()]


@functools.lru_cache(maxsize=None)
def parse_front_matter(text: str) -> dict:
    """The front matter as YAML. Raises on malformed YAML: a guard that cannot read metadata must not pass.

    A real parser, not a regex: a hand-written reader of quoted scalars stopped
    at the first escaped quote and truncated two commands' version_notes.
    BaseLoader keeps every scalar a string, so an unquoted `version: 1.10` is
    not read as the float 1.1.
    """
    data = yaml.load(split_front_matter(text)[0], Loader=yaml.BaseLoader)
    return data if isinstance(data, dict) else {}


def front_matter_field(text: str, field: str) -> str | None:
    """One front-matter value as text, from the YAML parse, never from a body example."""
    value = parse_front_matter(text).get(field)
    return None if value is None else str(value)


def read_front_matter_field(path: Path, field: str) -> str | None:
    """One front-matter value of a command file, as text."""
    return front_matter_field(path.read_text(), field)


@functools.lru_cache(maxsize=None)
def last_tag() -> str:
    """Newest tag reachable from HEAD. Raises with none: a release-window guard that cannot find its window must not pass."""
    return git("describe", "--tags", "--abbrev=0").strip()


@functools.lru_cache(maxsize=None)
def show_or_none(rev_path: str) -> str | None:
    """File text at `<rev>:<path>`, or None where it does not exist (added, deleted, renamed, root)."""
    try:
        return git("show", rev_path)
    except subprocess.CalledProcessError:
        return None


def metadata_changes(before: str | None, after: str | None) -> tuple[bool, bool]:
    """(version changed, version_notes changed) between two texts of one command, read from front matter only."""
    if after is None:
        return False, False
    if before is None:
        return True, True
    return tuple(
        front_matter_field(before, key) != front_matter_field(after, key) for key in ("version", "version_notes")
    )


@functools.lru_cache(maxsize=None)
def commit_metadata_changes(sha: str, rel_path: str) -> tuple[bool, bool]:
    return metadata_changes(show_or_none(f"{sha}^:{rel_path}"), show_or_none(f"{sha}:{rel_path}"))


@functools.lru_cache(maxsize=None)
def commit_changed_body(sha: str, rel_path: str) -> bool:
    """True if the commit changed this file's body (front matter and blank lines excluded).

    A bulk pass that only sets `version:` across the corpus is not a review, so
    its `last_reviewed` is correctly left alone. Only a substantive edit that
    also claims a version owes a review date. A file absent from the parent
    (added, renamed in, root commit) counts as changed.
    """
    before = show_or_none(f"{sha}^:{rel_path}")
    return before is None or body_lines(before) != body_lines(git("show", f"{sha}:{rel_path}"))


@functools.lru_cache(maxsize=None)
def last_substantive_version_bump(rel_path: str) -> str | None:
    """Date of the newest commit that bumped `version:` and changed the body.

    Cached: two tests call this across all 118 commands, and each call walks the
    file's history one `git show` at a time -- 537 subprocesses and ~10s per
    uncached pass. Git state does not change during a run.
    """
    for line in git("log", "--format=%H %cs", "--", rel_path).strip().splitlines():
        if not line.strip():
            continue
        sha, date = line.split()
        if commit_metadata_changes(sha, rel_path)[0]:
            return date if commit_changed_body(sha, rel_path) else None
    return None


@functools.lru_cache(maxsize=None)
def window_version_changes() -> tuple[tuple[str, frozenset[str], frozenset[str], frozenset[str]], ...]:
    """Per commit since the last tag: (sha, files touched, commands adding `version:`,
    commands adding `version_notes:`).

    One walk, shared by both release-window guards, so their detection cannot drift.
    """
    changes = []
    for sha in git("log", "--format=%H", f"{last_tag()}..HEAD").split():
        touched = frozenset(git("show", "--stat", "--format=", "--name-only", sha).split())
        bumped: set[str] = set()
        noted: set[str] = set()
        for f in touched:
            if f.startswith("commands/") and f.endswith(".md"):
                version_moved, notes_moved = commit_metadata_changes(sha, f)
                if version_moved:
                    bumped.add(f)
                if notes_moved:
                    noted.add(f)
        changes.append((sha[:7], touched, frozenset(bumped), frozenset(noted)))
    return tuple(changes)


def commands_changed_since_tag() -> list[tuple[str, str | None, str]]:
    """(path, text at the last tag or None if added, working-tree text) per command changed since the tag.

    Compares the tag with the working tree, so a pre-commit run sees the edit.
    Renames compare old path to new; deleted commands are skipped.
    """
    tag = last_tag()
    changed = []
    for row in git("diff", "-M", "--name-status", tag, "--", "commands/").splitlines():
        status, *paths = row.split("\t")
        if status[0] not in "AMR" or not paths[-1].endswith(".md"):
            continue
        old, new = paths[0], paths[-1]
        before = None if status[0] == "A" else git("show", f"{tag}:{old}")
        changed.append((new, before, (REPO_ROOT / new).read_text()))
    return changed


FENCE_OPEN = re.compile(r" {0,3}(`{3,}|~{3,})")


def fence_walk(body: str):
    """Yield (line, event, opener) per body line; event is prose, open, close or inside.

    A fence closes only on a bare run of its own character at least as long as
    the opener, as CommonMark renders it: a 4-backtick sample holding a
    ```bash block stays one fence. A plain open/close toggle reads the inner
    block's close as the end of the sample and counts the rest as prose. The
    prose and nesting guards read fences through this; the Related Commands
    counters still toggle (v2.34.0).
    """
    fence = None
    for line in body.split("\n"):
        if fence is None:
            if match := FENCE_OPEN.match(line):
                fence = match.group(1)
                yield line, "open", fence
            else:
                yield line, "prose", None
        elif re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{%d,}[ \t]*" % len(fence), line):
            yield line, "close", fence
            fence = None
        else:
            yield line, "inside", fence


def prose_lines(text: str) -> list[str]:
    """Body lines outside fenced blocks, as rendered."""
    return [line for line, event, _ in fence_walk(split_front_matter(text)[1]) if event == "prose"]


def fence_problems(text: str) -> list[str]:
    """Nested samples whose outer fence is too short, as far as syntax can prove.

    Inside a block, a fence line of the same character, at least the opener's
    length and carrying an info string, is content, and the inner block's bare
    close then ends the outer one. The rule is conservative: a sample showing
    a lone opener line as text trips it too, and lengthening its outer fence is
    harmless. A block still open at end of file also fails.

    Gaps, by design:
    1. A bare inner opener reads as the outer's close; nothing in the syntax
       says which was meant. Requiring an info string on every opener closes
       the gap.
    2. Fences in blockquotes, or in list items indented 4+ spaces, are not
       modelled.
    3. A backtick fence whose info string holds a backtick is not an opener in
       CommonMark; FENCE_OPEN reads it as one.
    """
    body = split_front_matter(text)[1]
    first = text.count("\n") - body.count("\n") + 1
    problems, opened, still_open = [], 0, False
    for i, (line, event, fence) in enumerate(fence_walk(body), first):
        if event == "open":
            opened, still_open = i, True
        elif event == "close":
            still_open = False
        elif event == "inside":
            match = FENCE_OPEN.match(line)
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                problems.append(f"line {i}: fence with an info string inside the block opened at line {opened}")
    if still_open:
        problems.append(f"line {opened}: block never closed")
    return problems


CODE_SPAN = re.compile(r"(?<![`\\])(`+)(?!`)(.+?)(?<!`)\1(?!`)")


def dash_count(text: str) -> int:
    """Spaced double hyphens (` -- `) in prose; fenced samples and code spans are exempt.

    Spans are matched per line, so one that crosses a line break is counted,
    and backslash escapes are not modelled beyond a lone escaped backtick.
    """
    return sum(CODE_SPAN.sub("", line).count(" -- ") for line in prose_lines(text))


def get_related_commands_count(content: str) -> int:
    """Count Related Commands links in standard section.

    Fenced lines are skipped, matching scripts/validate-conventions.py. Generator
    commands embed a sample Related Commands block inside ```; counting the
    sample's heading first ends the scan at the fence and returns 0, which
    `test_related_commands_within_limits` reads as "no section" and skips. The
    file then sits outside the ceiling entirely -- one rule, two implementations,
    and the blind one is the one CI runs.
    """
    in_section = False
    in_fence = False
    count = 0
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped.startswith("## Related Commands"):
            in_section = True
            continue
        if in_section:
            if line.startswith("## ") or line.startswith("---"):
                break
            if stripped.startswith("- `/pb-"):
                count += 1
    return count


FM = '---\nname: "pb-x"\nversion: "{v}"\nversion_notes: "{n}"\n---\n'
# (name, before, after, body changed, version moved, notes moved)
HOSTILE_FIXTURE = [
    ("removed-rule", FM.format(v="1.0.0", n="a") + "A\n\n----\nB\n", FM.format(v="1.0.0", n="a") + "A\n\nB\n", True, False, False),
    ("key-shaped-body-line", FM.format(v="1.0.0", n="a") + "name: node1\n", FM.format(v="1.0.0", n="a") + "name: node2\n", True, False, False),
    ("body-version-line", FM.format(v="1.0.0", n="a") + "x\n", FM.format(v="1.0.0", n="a") + 'x\nversion: "3.8"\n', True, False, False),
    ("closer-trailing-spaces", FM.format(v="1.0.0", n="a").replace("\n---\n", "\n---  \n") + "A\n----\nB\n",
     FM.format(v="1.1.0", n="b").replace("\n---\n", "\n---  \n") + "A\n----\nB\n", False, True, True),
    ("blank-lines-only", FM.format(v="1.0.0", n="a") + "A\nB\n", FM.format(v="1.0.0", n="a") + "A\n\nB\n\n", False, False, False),
    ("notes-amend-only", FM.format(v="1.1.0", n="a") + "A\n", FM.format(v="1.1.0", n="a b") + "A\n", False, False, True),
    ("notes-escaped-quote", FM.format(v="1.1.0", n='one \\"y\\" covers it') + "A\n",
     FM.format(v="1.1.0", n='one \\"y\\" covers it, amended') + "A\n", False, False, True),
    ("unquoted-version-1.10", FM.format(v="1.1", n="a").replace('version: "1.1"', "version: 1.1") + "A\n",
     FM.format(v="1.10", n="a").replace('version: "1.10"', "version: 1.10") + "A\n", False, True, False),
    ("added-file", None, FM.format(v="1.0.0", n="a") + "A\n", None, True, True),
    ("notes-folded-block", FM.format(v="1.0.0", n="a") + "A\n",
     '---\nname: "pb-x"\nversion: "1.1.0"\nversion_notes: >-\n  v1.1.0: one\n  line\n---\nA\n', False, True, True),
    ("notes-literal-block", FM.format(v="1.0.0", n="a") + "A\n",
     '---\nname: "pb-x"\nversion: "1.1.0"\nversion_notes: |\n  v1.1.0: one\n---\nA\n', False, True, True),
]

VERSION_MARKER = re.compile(r"(?<![\w.])v\d+\.\d+\.\d+:")


def notes_problem(text: str) -> str | None:
    """Why a bumped command's version_notes break the one-version rule, or None.

    The notes start with `v{version}:` and name no other version's marker:
    history lives in git and the CHANGELOG, not in a front-matter field that
    grows at every bump.
    """
    version, notes = front_matter_field(text, "version"), front_matter_field(text, "version_notes") or ""
    if not notes.startswith(f"v{version}: "):
        return f"does not start with 'v{version}: '"
    if len(VERSION_MARKER.findall(notes)) > 1:
        return f"names more than one version: {VERSION_MARKER.findall(notes)}"
    return None


NOTES_FIXTURE = [
    ("single-line", FM.format(v="1.1.0", n="v1.1.0: a"), None),
    ("cumulative", FM.format(v="1.1.0", n="v1.1.0: a. v1.0.0: b"), "more than one"),
    ("wrong-version", FM.format(v="1.1.0", n="v1.0.0: a"), "does not start"),
    ("no-marker", FM.format(v="1.1.0", n="v2.10.0 baseline"), "does not start"),
    ("prose-mentioning-a-playbook-tag", FM.format(v="2.0.0", n="v2.0.0: since playbook v2.31.0 ships"), None),
    ("folded-block-single", '---\nversion: "1.1.0"\nversion_notes: >-\n  v1.1.0: one\n  line\n---\n', None),
    ("literal-block-two-markers", '---\nversion: "1.1.0"\nversion_notes: |\n  v1.1.0: one\n  v1.0.0: two\n---\n', "more than one"),
]


class TestBodyChangeCarriesVersion:
    """A command whose body changed since the last tag must ship a new version.

    Compares the last tag with the working tree, so a pre-commit run catches the
    edit and CI (tree == HEAD) sees the same result. Resets at every tag; no
    baseline. Renames compare old path to new; added commands have nothing to
    compare. Gap: a second edit to a command already bumped in this window
    passes here -- its notes amendment is the changelog guard's job, and only
    when version_notes changes.
    """

    def test_body_change_carries_version_bump(self):
        tag = last_tag()
        offenders = []
        for new, before_text, after_text in commands_changed_since_tag():
            if before_text is None or body_lines(before_text) == body_lines(after_text):
                continue
            before, after = front_matter_field(before_text, "version"), front_matter_field(after_text, "version")
            if not (before and after):
                offenders.append(f"{new}: body changed since {tag}, version unreadable ({before!r} -> {after!r})")
            elif before == after:
                offenders.append(f"{new}: body changed since {tag}, still {after}")
        assert not offenders, (
            "Commands whose body changed without a version bump:\n  "
            + "\n  ".join(offenders)
            + "\nBump version (PATCH for a fix or clarification) with version_notes and a CHANGELOG line, in the same commit."
        )

    @pytest.mark.parametrize(
        "before, after, body_changed, version_moved, notes_moved",
        [row[1:] for row in HOSTILE_FIXTURE],
        ids=[row[0] for row in HOSTILE_FIXTURE],
    )
    def test_detectors_pass_the_hostile_fixture(self, before, after, body_changed, version_moved, notes_moved):
        """Every metadata and body detector, against inputs that fooled an earlier shape of them.

        No detector reads diff lines any more, so a diff header form (noprefix,
        custom src/dst prefixes) has nothing to fool.
        """
        if body_changed is not None:
            assert (body_lines(before) != body_lines(after)) is body_changed
        assert metadata_changes(before, after) == (version_moved, notes_moved)

    def test_every_command_splits_cleanly(self):
        """A split that landed in the body, an empty body or an unreadable version would make the guards pass by default."""
        broken = []
        for path in get_command_files():
            front, _body = split_front_matter(text := path.read_text())
            stray = [line for line in front.splitlines() if line.strip() and not re.match(r"[a-z_]+:|\s", line)]  # keys and indented YAML continuations
            try:
                readable = all(front_matter_field(text, key) for key in ("name", "version", "version_notes"))
            except yaml.YAMLError as error:
                broken.append(f"{path.name}: front matter is not YAML ({getattr(error, 'problem', None) or error})")
                continue
            if stray or not body_lines(text) or not readable:
                broken.append(f"{path.name}: {stray[:1] or 'no body, name, version or notes'}")
        assert not broken, "Front matter does not split cleanly:\n  " + "\n  ".join(broken)


class TestForgeFinderModes:
    def test_every_mode_forge_claims_for_a_finder_exists(self):
        """Forge's Find table names a finder's mode; a mode the finder's own file never defines is a promise nobody keeps."""
        forge = (COMMANDS_DIR / "development" / "pb-forge.md").read_text()
        find = forge.split("**Find.**", 1)[1].split("**Vet and fix.**", 1)[0]
        claims = re.findall(r"`/(pb-[a-z-]+) (--[a-z-]+)`", find)
        assert claims, "Forge's Find table names no finder mode -- did the table move?"
        missing = [
            f"/{cmd} {flag}" for cmd, flag in claims
            if flag not in next(COMMANDS_DIR.rglob(f"{cmd}.md")).read_text()
        ]
        assert not missing, f"Forge claims finder modes their commands do not define: {missing}"


class TestCommandCount:
    def test_expected_command_count(self):
        files = get_command_files()
        assert len(files) == EXPECTED_COUNT, (
            f"Expected {EXPECTED_COUNT} commands, found {len(files)}"
        )


class TestReviewDateFreshness:
    """`last_reviewed` must not predate the file's most recent commit.

    A command edited without touching its review date claims a review that did
    not happen. This is the failure mode of changes authored in another
    project's session: the author has the evidence and not the conventions, so
    the body is sound and the metadata drifts. See /pb-review-incoming.
    """

    def _violations(self) -> dict[str, str]:
        found = {}
        for path in get_command_files():
            rel = str(path.relative_to(REPO_ROOT))
            bumped = last_substantive_version_bump(rel)
            declared = read_front_matter_field(path, "last_reviewed")
            if bumped and declared and declared < bumped:
                found[path.name] = f"last_reviewed={declared}, edited={bumped}"
        return found

    def test_no_new_stale_review_dates(self):
        new = {k: v for k, v in self._violations().items() if k not in REVIEW_DATE_BASELINE}
        assert not new, (
            "Commands whose body and version changed without bumping last_reviewed:\n  "
            + "\n  ".join(f"{k}: {v}" for k, v in sorted(new.items()))
            + "\nBump last_reviewed in the same commit as the change."
        )

    def test_baseline_only_shrinks(self):
        fixed = REVIEW_DATE_BASELINE - self._violations().keys()
        assert not fixed, (
            f"Fixed but still baselined: {sorted(fixed)}. "
            "Remove them from REVIEW_DATE_BASELINE -- the list is debt, not exemptions."
        )


class TestChangelogLandsWithChange:
    """A commit that bumps a command's version must carry its CHANGELOG line.

    Splitting them produces a commit documenting work its own tree does not
    contain, or shipping work its changelog does not mention. Both survive every
    other checker and make bisect lie. See /pb-review-incoming Step 0.

    A release window allows one bump per command (docs/command-versioning.md),
    so later commits amend version_notes instead -- those count as a change too.
    """

    def test_version_bumps_carry_their_changelog_line(self):
        offenders: list[str] = []
        for sha, touched, bumped, noted in window_version_changes():
            changed = sorted(bumped | noted)
            if changed and "CHANGELOG.md" not in touched:
                offenders.append(f"{sha}: bumped {', '.join(changed)} without a CHANGELOG line")
        assert not offenders, (
            "Version bumps missing their changelog entry:\n  "
            + "\n  ".join(offenders)
            + "\nThe changelog line belongs in the same commit as the change."
        )

    def test_one_version_bump_per_command_per_window(self):
        bumps: dict[str, list[str]] = {}
        for sha, _touched, bumped, _noted in window_version_changes():
            for f in bumped:
                bumps.setdefault(f, []).append(sha)
        repeated = {f: shas for f, shas in bumps.items() if len(shas) > 1}
        assert not repeated, (
            "Commands bumped more than once since the last tag:\n  "
            + "\n  ".join(f"{f}: {', '.join(s)}" for f, s in sorted(repeated.items()))
            + "\nAmend the unreleased version's version_notes instead of minting another."
        )


# Spaced double hyphens in prose, per command. Debt, not exemptions: an entry
# only ever goes down, and a command whose body changes since the last tag
# leaves it at 0. Each file's fix is its own commit; there is no sweep.
DASH_BASELINE = {
    "pb-alex-infra.md": 1,
    "pb-caveman.md": 17,
    "pb-claude-global.md": 3,
    "pb-claude-orchestration.md": 3,
    "pb-greenfield.md": 15,
    "pb-handcraft.md": 34,
    "pb-handoff.md": 20,
    "pb-huddle.md": 22,
    "pb-kai-reach.md": 3,
    "pb-linus-agent.md": 2,
    "pb-llm-guidelines.md": 3,
    "pb-pause.md": 7,
    "pb-plan.md": 1,
    "pb-preflight.md": 12,
    "pb-resume.md": 3,
    "pb-review-code.md": 1,
    "pb-review-hygiene.md": 3,
    "pb-review-incoming.md": 55,
    "pb-ship.md": 2,
    "pb-sketch.md": 11,
    "pb-spec.md": 5,
    "pb-storage.md": 19,
    "pb-threat-hunt.md": 1,
    "pb-todo-implement.md": 2,
    "pb-usability.md": 1,
    "pb-voice.md": 4,
}

PROSE_FIXTURE = [
    ("plain", "a -- b\n", 1),
    ("fenced", "```\na -- b\n```\n", 0),
    ("nested-sample", "````markdown\n```bash\nx -- y\n```\nz -- w\n````\nafter -- this\n", 1),
    ("info-string-does-not-close", "```bash\na -- b\n```text\nc -- d\n```\n", 0),
    ("shorter-run-does-not-close", "````\n```\na -- b\n````\n", 0),
    ("tilde", "~~~\na -- b\n~~~\nc -- d\n", 1),
    ("front-matter-exempt", '---\nname: "x -- y"\n---\nbody\n', 0),
    ("inline-code", "run `git checkout -- f` -- now\n", 1),
    ("double-backtick-span", "``a ` -- b`` -- c\n", 1),
    ("escaped-backtick", "\\`a -- b` x\n", 1),
]


class TestDashRatchet:
    @pytest.mark.parametrize("text, count", [row[1:] for row in PROSE_FIXTURE], ids=[row[0] for row in PROSE_FIXTURE])
    def test_counter_reads_fences_as_rendered(self, text, count):
        assert dash_count(text) == count

    def test_no_command_adds_dashes(self):
        over = {
            p.name: n for p in get_command_files()
            if (n := dash_count(p.read_text())) > DASH_BASELINE.get(p.name, 0)
        }
        assert not over, (
            f"Spaced double hyphens above baseline: {over}. "
            "Use a colon, comma, semicolon or parentheses."
        )

    def test_changed_command_reaches_zero(self):
        left = {
            Path(path).name: n for path, before, after in commands_changed_since_tag()
            if (before is None or body_lines(before) != body_lines(after)) and (n := dash_count(after))
        }
        assert not left, (
            f"Body changed since {last_tag()} with spaced double hyphens left: {left}. "
            "Fix them in their own commit, before or after the change."
        )

    def test_baseline_only_shrinks(self):
        current = {p.name: dash_count(p.read_text()) for p in get_command_files()}
        stale = {k: (v, current.get(k)) for k, v in DASH_BASELINE.items() if current.get(k) != v}
        assert not stale, (
            f"DASH_BASELINE entries that no longer match (baseline, now): {stale}. "
            "Lower the entry to the new count; remove it at 0 or when the command is gone."
        )


# (name, text, problem substring or None)
FENCE_FIXTURE = [
    ("flat", "```bash\nx\n```\nprose\n", None),
    ("four-backtick-outer-info-inner", "````markdown\n# T\n```bash\nx\n```\nback\n````\n", None),
    ("four-backtick-outer-bare-inner", "````markdown\n```\nx\n```\nback\n````\n", None),
    ("three-backtick-outer-info-inner", "```markdown\n# T\n```bash\nx\n```\nback\n```\n", "line 3: fence with an info string"),
    ("gap-three-backtick-outer-bare-inner", "```markdown\n```\nx\n```\nback\n```\n", None),
    ("tilde-outer-backtick-inner", "~~~markdown\n```bash\nx\n```\n~~~\n", None),
    ("tilde-inside-tilde", "~~~markdown\n~~~bash\nx\n~~~\n~~~\n", "line 2: fence with an info string"),
    ("open-at-eof", "```\nx\n", "line 1: block never closed"),
    ("front-matter-offset", '---\nname: "x"\n---\n```markdown\n```bash\nx\n```\n```\n', "line 5: fence with an info string"),
]


class TestNestedSampleFences:
    """A sample holding a code block needs an outer fence longer than the inner.

    A 3-backtick outer fence closes at the inner block's close, and the rest of
    the page flips between prose and code: headings and Related Commands render
    as code on the site, and the other guards misread the file. See
    fence_problems for what syntax cannot prove.
    """

    @pytest.mark.parametrize("text, problem", [row[1:] for row in FENCE_FIXTURE], ids=[row[0] for row in FENCE_FIXTURE])
    def test_detector(self, text, problem):
        found = fence_problems(text)
        assert (not found) if problem is None else any(problem in f for f in found), found

    def test_every_command_closes_its_samples(self):
        bad = {p.name: probs[:3] for p in get_command_files() if (probs := fence_problems(p.read_text()))}
        assert not bad, (
            f"Fences a nested sample cannot close: {bad}. "
            "Give the outer fence more backticks than any fence inside it."
        )


LINE_BUDGET = 600
# Commands over LINE_BUDGET, at their current length, fence lines included.
# Debt, not exemptions: an entry only goes down, and is removed at or under 600.
LINE_BUDGET_BASELINE = {
    "pb-a11y.md": 932,
    "pb-adr.md": 691,
    "pb-alex-infra.md": 683,
    "pb-design-rules.md": 691,
    "pb-documentation.md": 828,
    "pb-dr.md": 728,
    "pb-git-signals.md": 910,
    "pb-guide.md": 666,
    "pb-hardening.md": 698,
    "pb-incident.md": 690,
    "pb-jordan-testing.md": 816,
    "pb-knowledge-transfer.md": 750,
    "pb-linus-agent.md": 614,
    "pb-observability.md": 837,
    "pb-performance.md": 653,
    "pb-preamble-decisions.md": 683,
    "pb-repo-docsite.md": 879,
    "pb-review-microservice.md": 841,
    "pb-sam-documentation.md": 711,
    "pb-secrets.md": 612,
    "pb-security.md": 739,
    "pb-ship.md": 730,
    "pb-sre-practices.md": 661,
    "pb-team.md": 663,
    "pb-testing.md": 716,
    "pb-think.md": 749,
    "pb-todo-implement.md": 616,
    "pb-zero-stack.md": 620,
}


class TestLineBudget:
    def test_no_command_over_its_budget(self):
        over = {
            p.name: (n, LINE_BUDGET_BASELINE.get(p.name, LINE_BUDGET)) for p in get_command_files()
            if (n := len(p.read_text().splitlines())) > LINE_BUDGET_BASELINE.get(p.name, LINE_BUDGET)
        }
        assert not over, (
            f"Commands over their line budget (lines, budget): {over}. "
            "Cut or move reference material out; the budget does not rise."
        )

    def test_baseline_only_shrinks(self):
        current = {p.name: len(p.read_text().splitlines()) for p in get_command_files()}
        stale = {
            k: (v, current.get(k)) for k, v in LINE_BUDGET_BASELINE.items()
            if v <= LINE_BUDGET or current.get(k) != v
        }
        assert not stale, (
            f"LINE_BUDGET_BASELINE entries that no longer match (baseline, now): {stale}. "
            f"Lower the entry to the new length; remove it at or under {LINE_BUDGET} or when the command is gone."
        )


class TestVersionNotesOneVersion:
    """A command bumped since the last tag carries notes for that version only.

    Resets at every tag, so commands not bumped since keep their old notes
    until their next bump rewrites them.
    """

    @pytest.mark.parametrize("text, problem", [row[1:] for row in NOTES_FIXTURE], ids=[row[0] for row in NOTES_FIXTURE])
    def test_detector(self, text, problem):
        found = notes_problem(text)
        assert (found is None) if problem is None else (found and problem in found), found

    def test_bumped_commands_name_one_version(self):
        bad = {
            path: problem for path, before, after in commands_changed_since_tag()
            if (before is None or front_matter_field(before, "version") != front_matter_field(after, "version"))
            and (problem := notes_problem(after))
        }
        assert not bad, (
            f"version_notes of commands bumped since {last_tag()}: {bad}. "
            "Rewrite them as one line starting 'v{version}: ' for the version being shipped."
        )


class TestTemplateCurrency:
    """The CLAUDE.md generator templates carry no model version strings.

    Their output is loaded into every session and cannot be corrected
    mid-session; a stale model name there tells the running model it is a
    different model. Front-matter version_notes are history and are exempt.
    """

    TEMPLATES = ["templates/pb-claude-global.md", "templates/pb-claude-project.md"]
    MODEL_VERSION = re.compile(r"\b(?:Opus|Sonnet|Haiku|Fable|Claude)[ -]?\d")

    @pytest.mark.parametrize("rel", TEMPLATES)
    def test_template_body_names_no_model_version(self, rel):
        text = (COMMANDS_DIR / rel).read_text()
        body = text.split("\n---\n", 1)[1]  # past the front-matter close
        hits = [
            f"{rel}:{n}: {line.strip()}"
            for n, line in enumerate(body.splitlines(), start=text[: len(text) - len(body)].count("\n") + 1)
            if self.MODEL_VERSION.search(line)
        ]
        assert not hits, "Model version in a generator template:\n  " + "\n  ".join(hits)


class TestResourceHint:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.files = get_command_files()

    def test_all_commands_have_resource_hint(self):
        missing = []
        for path in self.files:
            content = path.read_text()
            if "**Resource Hint:**" not in content:
                missing.append(path.name)
        assert not missing, f"Missing Resource Hint: {missing}"

    def test_resource_hints_have_valid_model(self):
        invalid = []
        for path in self.files:
            content = path.read_text()
            for line in content.splitlines():
                if "**Resource Hint:**" in line:
                    line_lower = line.lower()
                    if not any(m in line_lower for m in VALID_MODELS):
                        invalid.append(path.name)
                    break
        assert not invalid, f"Invalid model in Resource Hint: {invalid}"


class TestWhenToUse:
    def test_all_commands_have_when_to_use(self):
        missing = []
        for path in get_command_files():
            content_lower = path.read_text().lower()
            if not any(v in content_lower for v in WHEN_TO_USE_VARIANTS):
                missing.append(path.name)
        assert not missing, f"Missing When to Use: {missing}"


class TestRelatedCommands:
    def test_related_commands_within_limits(self):
        over_limit = []
        for path in get_command_files():
            content = path.read_text()
            count = get_related_commands_count(content)
            if count == 0:
                continue
            is_hub = path.name in HUB_COMMANDS
            limit = HUB_RELATED_LIMIT if is_hub else RELATED_LIMIT
            if count > limit:
                over_limit.append(f"{path.name} ({count}/{limit})")
        assert not over_limit, f"Over Related Commands limit: {over_limit}"

    def test_fenced_sample_blocks_are_not_counted(self):
        """A sample block inside ``` must not be mistaken for the file's own section.

        Counting the sample's heading ends the scan at the fence and returns 0,
        which test_related_commands_within_limits reads as "no section" and
        skips -- so the file leaves the ceiling check silently. pb-new-playbook
        hit exactly this: the test counted 0 where the validator counted 4.
        """
        content = (
            "## Related Commands\n\n"
            "- `/pb-alpha` - one\n"
            "- `/pb-beta` - two\n\n"
            "---\n\n"
            "## Template\n\n"
            "```markdown\n"
            "## Related Commands\n\n"
            "- `/pb-sample-a` - not this file's\n"
            "- `/pb-sample-b` - nor this\n"
            "```\n"
        )
        assert get_related_commands_count(content) == 2

        fenced_first = (
            "## Template\n\n"
            "```markdown\n"
            "## Related Commands\n\n"
            "- `/pb-sample-a` - sample\n"
            "```\n\n"
            "## Related Commands\n\n"
            "- `/pb-alpha` - one\n"
            "- `/pb-beta` - two\n"
            "- `/pb-gamma` - three\n"
        )
        assert get_related_commands_count(fenced_first) == 3, (
            "A fenced sample appearing before the real section must not consume it"
        )

    def test_front_matter_related_commands_within_limits(self):
        """The limit applies to both lists; until now only one was counted.

        get_related_commands_count parses the `## Related Commands` body
        section, so the front-matter field could grow past the ceiling with
        every gate green -- which it did, reaching 7 against a limit of 5.
        """
        over_limit = []
        for path in get_command_files():
            match = re.search(
                r"^related_commands:\s*\[(.*?)\]", path.read_text(), re.MULTILINE | re.DOTALL
            )
            if not match:
                continue
            count = len(re.findall(r"'([^']*)'", match.group(1)))
            limit = HUB_RELATED_LIMIT if path.name in HUB_COMMANDS else RELATED_LIMIT
            if count > limit:
                over_limit.append(f"{path.name} ({count}/{limit})")
        assert not over_limit, (
            "Over front-matter related_commands limit: "
            + ", ".join(over_limit)
            + "\nThe body section is counted separately; both lists share the limit."
        )

    def test_patterns_hub_names_every_family(self):
        """The hub's selection tree and Related list each name every pb-patterns-* child.

        A child missing from either is unreachable from the hub; one named but
        gone is a dead link.
        """
        family = {p.stem for p in (COMMANDS_DIR / "planning").glob("pb-patterns-*.md")}
        sections = {
            s.split("\n", 1)[0]: s
            for s in (COMMANDS_DIR / "planning" / "pb-patterns.md").read_text().split("\n## ")
        }
        tree = set(re.findall(r"→ /(pb-patterns-[a-z]+)", sections["Pattern Selection Workflow"]))
        related = set(re.findall(r"^- `/(pb-patterns-[a-z]+)`", sections["Related Commands"], re.M))
        assert tree == family, f"selection tree: missing {family - tree}, extra {tree - family}"
        assert related == family, f"Related: missing {family - related}, extra {related - family}"


SCHEMA_FIELDS = frozenset(
    yaml.safe_load((REPO_ROOT / ".playbook-metadata-schema.yaml").read_text())["fields"]
)


def unknown_front_matter_keys(text: str) -> set[str]:
    return set(parse_front_matter(text)) - SCHEMA_FIELDS


class TestFrontMatterKeys:
    """Every front-matter key is a field in .playbook-metadata-schema.yaml: a retired or misspelt key fails."""

    def test_every_key_is_a_schema_field(self):
        unknown = {p.name: sorted(k) for p in get_command_files() if (k := unknown_front_matter_keys(p.read_text()))}
        assert not unknown, f"Front-matter keys not in the schema's fields: {unknown}"

    def test_a_retired_key_fails(self, tmp_path, make_command):
        good = make_command(tmp_path, "pb-good").read_text()
        bad = make_command(tmp_path, "pb-bad", last_evolved='"2026-06-10"').read_text()
        assert unknown_front_matter_keys(good) == set()
        assert unknown_front_matter_keys(bad) == {"last_evolved"}


class TestMetadataConsistency:
    """Verify metadata front-matter matches body Resource Hint.

    This prevents regressions where bulk metadata generation overwrites
    carefully audited Resource Hints from v2.8.0 audit.
    """

    @staticmethod
    def extract_body_resource_hint(content: str) -> str | None:
        """Extract model from body Resource Hint line."""
        match = re.search(r'\*\*Resource Hint:\*\*\s+(sonnet|opus|haiku)', content)
        return match.group(1) if match else None

    @staticmethod
    def extract_metadata_model_hint(content: str) -> str | None:
        """Extract model_hint from YAML front-matter."""
        match = re.search(r'^model_hint:\s*"([^"]+)"', content, re.MULTILINE)
        return match.group(1) if match else None

    def test_metadata_matches_body_resource_hint(self):
        """All commands must have consistent model_hint in metadata and body."""
        conflicts = []
        for path in get_command_files():
            content = path.read_text()
            body_hint = self.extract_body_resource_hint(content)
            meta_hint = self.extract_metadata_model_hint(content)

            if body_hint and meta_hint and body_hint != meta_hint:
                conflicts.append(
                    f"{path.name}: body={body_hint}, metadata={meta_hint}"
                )

        assert not conflicts, f"Metadata-body conflicts:\n" + "\n".join(
            f"  {c}" for c in conflicts
        )


class TestPersonaIntegrity:
    """Validate persona agent structure and consistency."""

    # Persona agents (9): original 5 + kai-reach + elena/travis/clara (added 2026-07-13)
    PERSONA_COMMANDS = {
        "pb-linus-agent.md": {"model": "opus", "category": "reviews", "difficulty": "advanced"},
        "pb-alex-infra.md": {"model": "opus", "category": "deployment", "difficulty": "advanced"},
        "pb-maya-product.md": {"model": "sonnet", "category": "planning", "difficulty": "intermediate"},
        "pb-sam-documentation.md": {"model": "sonnet", "category": "core", "difficulty": "intermediate"},
        "pb-jordan-testing.md": {"model": "opus", "category": "development", "difficulty": "advanced"},
        "pb-kai-reach.md": {"model": "sonnet", "category": "planning", "difficulty": "intermediate"},
        "pb-elena-design.md": {"model": "opus", "category": "reviews", "difficulty": "advanced"},
        "pb-travis-security.md": {"model": "opus", "category": "reviews", "difficulty": "advanced"},
        "pb-clara-curator.md": {"model": "opus", "category": "core", "difficulty": "advanced"},
    }

    def test_persona_agents_exist(self):
        """Ensure all 9 persona agents are present."""
        files = get_command_files()
        file_names = {f.name for f in files}
        missing = []
        for persona_name in self.PERSONA_COMMANDS:
            if persona_name not in file_names:
                missing.append(persona_name)
        assert not missing, f"Missing persona agents: {missing}"

    def test_persona_metadata_correct(self):
        """Verify persona metadata matches expected values."""
        files = get_command_files()
        errors = []
        for path in files:
            if path.name not in self.PERSONA_COMMANDS:
                continue
            content = path.read_text()
            expected = self.PERSONA_COMMANDS[path.name]

            # Each field: a missing or unquoted value fails, not silently skips.
            for field, expected_val in (
                ("model_hint", expected["model"]),
                ("category", expected["category"]),
                ("difficulty", expected["difficulty"]),
            ):
                m = re.search(rf'^{field}:\s*"([^"]+)"', content, re.MULTILINE)
                actual = m.group(1) if m else None
                if actual != expected_val:
                    errors.append(
                        f"{path.name}: {field}={actual}, expected {expected_val}"
                    )

        assert not errors, f"Persona metadata mismatches:\n" + "\n".join(f"  {e}" for e in errors)

    def test_persona_agents_have_decision_framework(self):
        """Ensure persona agents have structured decision/review framework."""
        files = get_command_files()
        missing_framework = []
        for path in files:
            if path.name not in self.PERSONA_COMMANDS:
                continue
            content = path.read_text().lower()

            # Personas must have either: "decision", "framework", "review", or "criteria"
            if not any(keyword in content for keyword in ["decision", "framework", "review criteria", "red flags"]):
                missing_framework.append(path.name)

        assert not missing_framework, f"Persona agents missing decision framework: {missing_framework}"

    def test_personas_have_boundary_section(self):
        """Every persona must carry a Boundary & Authority section (sharpen pass, 2026-07-13).

        The block is what makes a boundary legible: the lane, the routes out, the
        collision-pair callout, and the domain authority. Applied inconsistently across
        nine files, the sharpening silently rots -- this guard is the belt for that.
        """
        files = get_command_files()
        missing = []
        for path in files:
            if path.name not in self.PERSONA_COMMANDS:
                continue
            if "## Boundary & Authority" not in path.read_text():
                missing.append(path.name)
        assert not missing, f"Personas missing Boundary & Authority: {missing}"

    def test_huddle_registers_all_personas(self):
        """pb-huddle's roster line must list every persona (roster drift guard).

        Checks the explicit "**Roster (N):**" line, not the whole file: an incidental
        mention (a collision-line cross-reference, a related_commands entry) must not
        satisfy the guard. A persona in PERSONA_COMMANDS but absent from the roster is
        the "forgot to seat it" drift this catches.
        """
        huddle = None
        for path in get_command_files():
            if path.name == "pb-huddle.md":
                huddle = path.read_text()
                break
        assert huddle is not None, "pb-huddle.md not found"
        roster_match = re.search(r"^\*\*Roster \(\d+\):\*\*(.+)$", huddle, re.MULTILINE)
        assert roster_match, "pb-huddle.md has no '**Roster (N):**' line"
        roster = roster_match.group(1)
        missing = [
            name for name in self.PERSONA_COMMANDS if f"/{name[:-3]}" not in roster
        ]
        assert not missing, f"Personas absent from the pb-huddle roster line: {missing}"

    def test_multi_perspective_reviews_exist(self):
        """Ensure multi-perspective review commands exist (Phase 2)."""
        multi_reviews = {"pb-review-backend.md", "pb-review-frontend.md", "pb-review-infrastructure.md"}
        files = get_command_files()
        file_names = {f.name for f in files}
        missing = multi_reviews - file_names
        assert not missing, f"Missing multi-perspective reviews: {missing}"

    def test_persona_no_hardcoded_security_flaws(self):
        """Check persona agents for common security anti-patterns."""
        # Specifically validates pb-linus-agent.md for password hashing security
        files = get_command_files()
        security_issues = []
        for path in files:
            if path.name == "pb-linus-agent.md":
                content = path.read_text()
                # Should not have hardcoded salt in password examples
                if "b'salt'" in content:
                    security_issues.append(f"{path.name}: Contains hardcoded salt in password example")
                # Should use bcrypt, not pbkdf2 with hardcoded salt
                if re.search(r"pbkdf2_hmac.*b'salt'", content):
                    security_issues.append(f"{path.name}: Uses pbkdf2 with hardcoded salt")

        assert not security_issues, f"Security issues in persona agents:\n" + "\n".join(
            f"  {issue}" for issue in security_issues
        )


class TestRegisterRuleReference:
    """Verify artifact-producing commands reference the global GitHub Artifact Register rule.

    Introduced in v2.22.0 Register Rollout. Prevents future commands from
    drifting back to local restatements or silent omissions of the rule.
    Maintainers adding a new artifact-producing command must extend the
    ARTIFACT_PRODUCING_COMMANDS set.
    """

    # Commands that produce GitHub artifacts (commits, PRs, issues, PR/review comments).
    # Each must reference the global rule defined in ~/.claude/CLAUDE.md
    # (template: commands/templates/pb-claude-global.md).
    ARTIFACT_PRODUCING_COMMANDS = {
        # Commit + PR producers
        "pb-commit.md",
        "pb-cycle.md",
        "pb-forge.md",
        "pb-handcraft.md",
        "pb-pr.md",
        "pb-review.md",
        "pb-ship.md",
        # Direct review-comment producers
        "pb-review-code.md",
        "pb-review-comprehensive.md",
        "pb-review-hygiene.md",
        "pb-review-tests.md",
        "pb-review-backend.md",
        "pb-review-frontend.md",
        "pb-review-infrastructure.md",
        "pb-review-microservice.md",
        "pb-review-product.md",
        "pb-review-docs.md",
        "pb-review-playbook.md",
        "pb-security.md",
        "pb-linus-agent.md",
        "pb-jordan-testing.md",
        # Persona reviewers + design lenses
        "pb-maya-product.md",
        "pb-kai-reach.md",
        "pb-sam-documentation.md",
        "pb-alex-infra.md",
        "pb-a11y.md",
        "pb-calm-design.md",
        "pb-logging.md",
        "pb-usability.md",
        "pb-voice.md",
    }

    REGISTER_REFERENCE = "GitHub Artifact Register"

    def test_artifact_producing_commands_reference_register_rule(self):
        """Every artifact-producing command must reference the global Register rule."""
        files = get_command_files()
        file_names = {f.name for f in files}

        missing_files = self.ARTIFACT_PRODUCING_COMMANDS - file_names
        assert not missing_files, (
            f"Expected artifact-producing commands not found: {missing_files}"
        )

        no_reference = []
        for path in files:
            if path.name not in self.ARTIFACT_PRODUCING_COMMANDS:
                continue
            content = path.read_text()
            if self.REGISTER_REFERENCE not in content:
                no_reference.append(path.name)

        assert not no_reference, (
            f"Commands missing '{self.REGISTER_REFERENCE}' reference:\n"
            + "\n".join(f"  {c}" for c in no_reference)
        )


class TestRecapArchiveCoherence:
    """The pause/resume pair writes and re-reads one recap archive.

    Three version bumps shipped a divergence here -- pb-resume's dedup check
    named `todos/done/lessons.md` while its own archive step told a project with
    an existing `memory/lessons.md` to keep using that -- so the check read a
    file the write never touched and a recap could be archived twice. Every
    other test in this file guards metadata shape; none could see a
    contradiction between two steps of one command.
    """

    PAIR = ("pb-resume.md", "pb-pause.md")

    def test_no_command_hardcodes_a_migration_away_from_an_existing_archive(self):
        """A fixed destination for an *existing* archive is the fork this rule caused.

        `todos/done/lessons.md` may still appear as the default for a project
        that has no archive yet. What must not come back is an instruction to
        keep writing somewhere other than where a project's recaps already go.
        """
        offenders = []
        for name in self.PAIR:
            path = COMMANDS_DIR / "development" / name
            body = path.read_text().split("---", 2)[-1]
            for marker in ("pre-v1.6.0 path", "leave it where it is and open the new file"):
                if marker in body:
                    offenders.append(f"{name}: reintroduces the fork-and-point-back rule ({marker!r})")

        assert not offenders, (
            "Recap archive must be the project's existing archive:\n  "
            + "\n  ".join(offenders)
            + "\nA second location forks the record whether or not a pointer connects them."
        )

    def test_pause_and_resume_agree_on_the_default_archive(self):
        """Both halves of the loop must name the same default, or a first archive splits."""
        default = "todos/done/lessons.md"
        missing = [
            name for name in self.PAIR
            if default not in (COMMANDS_DIR / "development" / name).read_text()
        ]
        assert not missing, (
            f"These commands no longer name the default archive {default!r}: {missing}\n"
            "pb-pause writes the recap and pb-resume re-reads it; a project with no "
            "archive yet needs both to start it in the same place."
        )

    def test_pause_and_resume_find_the_working_context_by_glob(self):
        """/pb-context names two common filenames; a hardcoded one reports the other as missing."""
        glob, fixed = "todos/*working-context*.md", "todos/1-working-context.md"
        wrong = [
            name for name in self.PAIR
            if glob not in (text := (COMMANDS_DIR / "development" / name).read_text()) or fixed in text
        ]
        assert not wrong, f"These commands do not find the working context by {glob!r}: {wrong}"

    def test_forge_and_resume_share_shipped_stage(self):
        """Resume flags finished arcs by the stage name forge writes, and both archive to one path; a rename on one side orphans cursors."""
        for needle in ("`SHIPPED`", "`todos/done/forge-<slug>.md`"):
            missing = [
                name for name in ("pb-forge.md", "pb-resume.md")
                if needle not in (COMMANDS_DIR / "development" / name).read_text()
            ]
            assert not missing, f"{needle} is not named in: {missing}"
