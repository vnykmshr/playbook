"""scripts/feedback-harvest.py: extraction, keys, sources, exit codes, and what it must never open."""
import builtins
import os
import subprocess
from pathlib import Path

import pytest

import feedback_harvest as fh  # registered by conftest


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    _ = path.write_text(text)
    return path


def run(tmp_path: Path, *extra: str) -> int:
    args = [
        "--repos", str(tmp_path / "repos"), "--memory", str(tmp_path / "mem"),
        "--playbook", str(tmp_path / "pb"), "--ledger", str(tmp_path / "ledger.tsv"),
        "--out", str(tmp_path / "out"), *extra,
    ]
    return fh.main(args)


def digest(tmp_path: Path) -> str:
    return next((tmp_path / "out").glob("digest-*.md")).read_text()


def texts(md: str) -> list[str]:
    return [t for _, t in fh.extract(md)[0]]


def test_golden_key():
    """A normaliser change orphans every ledger row: it must fail here first."""
    assert fh.normalise("**Fix** `pb-pause` Step 6  (2026-10-14) [see](http://x)") == "fix pb-pause step 6 ( ) see"
    assert fh.item_key("**Fix** `pb-pause` Step 6  (2026-10-14) [see](http://x)") == "44a94ecdce0e"


@pytest.mark.parametrize("heading", [
    "Patterns / playbook feedback:",
    "**Patterns / playbook feedback:**",
    "**Playbook feedback.**",
    "**Playbook feedback:**",
    "Playbook feedback:",
    "### Patterns / playbook feedback",
    "**Process / playbook feedback.**",
])
def test_every_heading_shape(heading: str):
    assert texts(f"{heading}\n- one\n- two\n") == ["one", "two"]


def test_inline_item_after_the_heading():
    assert texts("**Playbook feedback:** `pb-handcraft` Lens 2 held.\n") == ["`pb-handcraft` Lens 2 held."]


def test_bullet_block_shape():
    md = (
        "Playbook feedback:\n\n"
        "- first\n  continued\n"
        "  - nested detail\n"
        "\n"
        "- second\n"
        "\n"
        "A paragraph ends the block.\n"
        "- not an item\n"
    )
    assert texts(md) == ["first continued - nested detail", "second"]


@pytest.mark.parametrize("stop", ["## Next", "**Key observations:**"])
def test_block_stops_at_a_heading_or_bold_label(stop: str):
    assert texts(f"Playbook feedback:\n- one\n{stop}\n- other\n") == ["one"]


def test_fenced_heading_and_template_placeholder_are_skipped():
    md = (
        "```markdown\nPatterns / playbook feedback:\n- fenced\n```\n"
        "Patterns / playbook feedback:\n- [pattern or playbook command that needs attention]\n"
    )
    items, empty = fh.extract(md)
    assert items == [] and empty == [5]


@pytest.mark.parametrize("prose", [
    "The pause asks for playbook feedback: see pb-pause.",
    "Playbook feedback harvesting runs before Step 1.",
    "playbook feedbackish",
    "## Playbook feedback loop",
])
def test_a_mention_in_prose_is_not_a_heading(prose: str):
    assert fh.extract(f"{prose}\n- not an item\n") == ([], [])


@pytest.mark.parametrize("heading", ["## Playbook Feedback (v2.1)", "**Playbook feedback**: inline"])
def test_heading_variants_still_match(heading: str):
    assert texts(f"{heading}\n- one\n")[-1] == "one"


# The contract: a line is a heading, a near miss (listed, no key), or silent because the
# words do not start it. A new shape is ruled against this table, not fixed in HEADING.
@pytest.mark.parametrize("line, outcome", [
    ("Playbook feedback:", "heading"),
    ("**Patterns / playbook feedback:**", "heading"),
    ("### Patterns / playbook feedback", "heading"),
    ("## Playbook Feedback (v2.1)", "heading"),
    ("**Playbook feedback**: inline", "heading"),
    ("**Playbook feedback**", "near"),
    ("Playbook feedback", "near"),
    ("Playbook feedback (pb-forge)", "near"),
    ("## Playbook feedback - 2026-11-03", "near"),
    ("### Playbook feedback for pb-forge", "near"),
    ("## Playbook feedback loop", "near"),
    ("- **Playbook feedback:**", "near"),
    ("  ## Playbook feedback", "near"),
    ("> Playbook feedback:", "near"),
    ("Playbook feedback harvesting runs before Step 1.", "near"),
    ("## Q4 playbook feedback", "silent"),
    ("Patterns and playbook feedback:", "silent"),
    ("playbook feedbackish", "silent"),
    ("The pause asks for playbook feedback: see pb-pause.", "silent"),
])
def test_every_line_is_a_heading_a_near_miss_or_silent(line: str, outcome: str):
    got = "heading" if fh.HEADING.match(line) else "near" if fh.near_misses(line) == [1] else "silent"
    assert got == outcome


def test_near_misses_skip_fences_and_never_change_the_exit(tmp_path: Path):
    assert fh.near_misses("```\nPlaybook feedback\n```\nPlaybook feedback\n---\n") == [4]
    repo_note(tmp_path, "o/r", "## 2026-10-01\n**Playbook feedback**\n- lost\n")
    assert run(tmp_path) == 2, "no repo heading at all: a regression or a wrong root, never a close"
    assert "pause-notes.md:2`" in digest(tmp_path).split("## Near-miss headings")[1]
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n\n**Playbook feedback**\n- lost\n")
    write(tmp_path / "ledger.tsv", f"key\tdisposition\tversion\tdate\n{fh.item_key('one')}\ttaken\tv1\t2026-11-04\n")
    assert run(tmp_path) == 0
    md = digest(tmp_path)
    assert "pause-notes.md:5`" in md.split("## Near-miss headings")[1] and "1 near misses" in md


def test_heading_date_skips_future_mentions():
    lines = ["## Pause: 2026-10-01", "### Shipped (v2 stays on 2099-01-01)", "Playbook feedback:"]
    assert fh.heading_date(lines, 2, "2026-11-04") == "2026-10-01"


def repo_note(tmp_path: Path, repo: str, text: str, name: str = "pause-notes.md") -> Path:
    return write(tmp_path / "repos" / repo / "todos" / name, text)


def test_exit_2_when_nothing_is_found(tmp_path: Path):
    (tmp_path / "repos").mkdir()
    assert run(tmp_path) == 2


@pytest.mark.parametrize("ledger", [
    "key\tdisposition\n",
    "key\tdisposition\tversion\tdate\nabc\ttaken\tv1\t2026-11-04\n",
    "key\tdisposition\tversion\tdate\n0123456789ab\tseen\tv1\t2026-11-04\n",
    "key\tdisposition\tversion\tdate\n0123456789ab\ttaken\tv1\n",
    "key\tdisposition\tversion\tdate\n0123456789ab\tdup-of:xyz\tv1\t2026-11-04\n",
    "key\tdisposition\tversion\tdate\n0123456789ab\ttaken\tv1\tsoon\n",
    "key\tdisposition\tversion\tdate\n0123456789ab\ttaken\tv1\t2026-11-04\n0123456789ab\trejected\t\t2026-11-05\n",
    "key\tdisposition\tversion\tdate\n0123456789ab\tdup-of:deadbeef0000\t\t2026-11-04\n",
    "key\tdisposition\tversion\tdate\n0123456789ab\tdup-of:deadbeef0000\t\t2026-11-04\n"
    "deadbeef0000\tdup-of:0123456789ab\t\t2026-11-04\n",
])
def test_exit_2_on_a_malformed_ledger(tmp_path: Path, ledger: str):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    write(tmp_path / "ledger.tsv", ledger)
    assert run(tmp_path) == 2


def test_any_error_exits_2_not_1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    monkeypatch.setenv("PATH", str(tmp_path / "no-bin"))
    write(tmp_path / "repos" / "o" / "r" / ".git" / "HEAD", "ref: refs/heads/main\n")
    assert run(tmp_path) == 2, "git missing"


def test_a_repo_git_cannot_list_exits_2_and_is_named(tmp_path: Path):
    repo_note(tmp_path, "o/broken", "## 2026-10-01\nPlaybook feedback:\n- unvetted\n")
    write(tmp_path / "repos" / "o" / "broken" / ".git", "gitdir: /nowhere\n")
    repo_note(tmp_path, "o/plain", "## 2026-10-01\nPlaybook feedback:\n- kept\n")
    write(tmp_path / "ledger.tsv", f"key\tdisposition\tversion\tdate\n{fh.item_key('kept')}\ttaken\tv1\t2026-11-04\n")
    assert run(tmp_path) == 2, "every key dispositioned, but the harvest is incomplete"
    md = digest(tmp_path)
    assert "unvetted" not in md and "1 repos unread" in md
    assert "o/broken`" in md.split("## Repos unread")[1]


def test_a_crlf_note_is_harvested_with_its_date(tmp_path: Path):
    path = tmp_path / "repos" / "o" / "r" / "todos" / "pause-notes.md"
    path.parent.mkdir(parents=True)
    _ = path.write_bytes(b"## 2026-10-01\r\n## Playbook feedback\r\n- one\r\n- two\r\n")
    assert run(tmp_path) == 1
    md = digest(tmp_path)
    assert f"`{fh.item_key('one')}` 1 source(s), newest 2026-10-01" in md and "two" in md


def test_memory_cannot_mask_a_harvest_with_no_repo_heading(tmp_path: Path):
    write(tmp_path / "mem" / "p" / "memory" / "feedback_x.md", "---\ndescription: Kept\n---\n")
    write(tmp_path / "ledger.tsv", f"key\tdisposition\tversion\tdate\n{fh.item_key('Kept')}\ttaken\tv1\t2026-11-04\n")
    (tmp_path / "repos").mkdir()
    assert run(tmp_path) == 2
    assert digest(tmp_path), "the digest is still written"


def unreadable(monkeypatch: pytest.MonkeyPatch, suffix: str) -> None:
    """Make reads of paths ending in suffix raise, as chmod 000 would for a non-root user."""
    real_read, real_scandir = Path.read_text, os.scandir

    def read(self, *a, **k):
        if str(self).endswith(suffix):
            raise PermissionError(13, "denied", str(self))
        return real_read(self, *a, **k)

    def scandir(path=".", *a, **k):
        if str(path).endswith(suffix):
            raise PermissionError(13, "denied", str(path))
        return real_scandir(path, *a, **k)

    monkeypatch.setattr(Path, "read_text", read)
    monkeypatch.setattr(os, "scandir", scandir)


@pytest.mark.parametrize("suffix, where", [
    ("locked.md", "todos/locked.md"), ("archive", "todos/archive"), ("memory", "p/memory"),
])
def test_an_unreadable_path_exits_2_and_is_listed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, suffix: str, where: str):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- hidden\n", "locked.md")
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- hidden\n", "archive/a.md")
    write(tmp_path / "mem" / "p" / "memory" / "feedback_x.md", "---\ndescription: Mem\n---\n")
    unreadable(monkeypatch, suffix)
    assert run(tmp_path) == 2
    assert where in digest(tmp_path).split("## Paths unread")[1]


def test_a_symlinked_note_is_not_followed(tmp_path: Path):
    outside = write(tmp_path / "elsewhere" / "notes.md", "## 2026-10-01\nPlaybook feedback:\n- linked in\n")
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    (tmp_path / "repos" / "o" / "r" / "todos" / "link.md").symlink_to(outside)
    (tmp_path / "mem" / "p" / "memory").mkdir(parents=True)
    (tmp_path / "mem" / "p" / "memory" / "feedback_l.md").symlink_to(
        write(tmp_path / "elsewhere" / "m.md", "---\ndescription: Linked mem\n---\n"))
    assert run(tmp_path) == 1
    md = digest(tmp_path)
    assert "linked in" not in md and "Linked mem" not in md


def test_exit_1_then_0_once_every_key_is_dispositioned(tmp_path: Path):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n- two\n")
    assert run(tmp_path) == 1, "a missing ledger reads as empty"
    one, two = fh.item_key("one"), fh.item_key("two")
    write(tmp_path / "ledger.tsv", f"key\tdisposition\tversion\tdate\n{one}\ttaken\tv2.33.0\t2026-11-04\n")
    assert run(tmp_path) == 1
    write(tmp_path / "ledger.tsv", (
        f"key\tdisposition\tversion\tdate\n{one}\ttaken\tv2.33.0\t2026-11-04\n"
        f"{two}\tdup-of:{one}\tv2.33.0\t2026-11-04\n"
    ))
    assert run(tmp_path) == 0
    assert not (tmp_path / "pb").exists() or not any((tmp_path / "pb").rglob("*.tsv")), "never writes a ledger"


def test_sources_are_distinct_repos_and_private_orgs_are_flagged(tmp_path: Path):
    write(tmp_path / "pb" / "todos" / "evolve" / "private-orgs", "# one per line\nacme\n")
    repo_note(tmp_path, "o/a", "## 2026-10-01\nPlaybook feedback:\n- Same **thing**\n")
    repo_note(tmp_path, "o/a", "## 2026-10-02\nPlaybook feedback:\n- same thing\n", "done/lessons.md")
    repo_note(tmp_path, "acme/b", "## 2026-10-03\nPlaybook feedback:\n- same `thing`\n")
    write(tmp_path / "mem" / "-u-github-acme-c" / "memory" / "feedback_z.md", "---\ndescription: Mem note\n---\n")
    assert run(tmp_path) == 1
    md = digest(tmp_path)
    assert f"`{fh.item_key('same thing')}` 2 source(s), newest 2026-10-03 [private]" in md
    assert next(x for x in md.splitlines() if "Mem note" in x).count("[private]") == 1


@pytest.mark.parametrize("source, flagged", [
    ("acme/x", True), ("ACME/x", True), ("memory:-u-github-acme-x", True), ("memory:-u-github-acme", True),
    ("memory:-u-github-acme-labs-x", True), ("acme-labs/x", False), ("o/acme", False),
])
def test_private_org_match(source: str, flagged: bool):
    assert fh.is_private(source, frozenset({"acme"})) is flagged


def test_digest_says_whether_the_private_orgs_file_was_read(tmp_path: Path):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    assert run(tmp_path) == 1
    assert "private-orgs missing" in digest(tmp_path)
    write(tmp_path / "pb" / "todos" / "evolve" / "private-orgs", "Acme\n")
    assert run(tmp_path) == 1
    assert "private orgs: 1 from" in digest(tmp_path)


def test_a_note_in_a_repo_nested_under_todos_is_private(tmp_path: Path):
    repo_note(tmp_path, "o/pub", "## 2026-10-01\nPlaybook feedback:\n- public note\n")
    repo_note(tmp_path, "o/pub", "## 2026-10-01\nPlaybook feedback:\n- desk note\n", "desk/notes/a.md")
    repo_note(tmp_path, "o/pub", "## 2026-10-01\nPlaybook feedback:\n- git internals\n", "desk/.git/x.md")
    assert run(tmp_path) == 1
    md = digest(tmp_path)
    assert "[private]: desk note" in md and "[private]" not in next(x for x in md.splitlines() if "public note" in x)
    assert "git internals" not in md


@pytest.mark.parametrize("project", ["-u-o-r-todos", "-u-o-r-todos-desk"])
def test_memory_for_a_path_under_todos_is_private(tmp_path: Path, project: str):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    write(tmp_path / "mem" / project / "memory" / "feedback_x.md", "---\ndescription: Desk mem\n---\n")
    assert run(tmp_path) == 1
    assert "[private]: Desk mem" in digest(tmp_path)


def test_skips_tracked_files_and_its_own_output(tmp_path: Path):
    repo = tmp_path / "repos" / "o" / "r"
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- from upstream\n", "tracked.md")
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- digest echo\n", "evolve/digest-x.md")
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- raw sweep\n", "inbox/harvest-1/a.md")
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- kept\n")
    _ = subprocess.run(["git", "init", "-q", str(repo)], check=True)
    _ = subprocess.run(["git", "-C", str(repo), "add", "todos/tracked.md"], check=True)
    assert run(tmp_path) == 1
    md = digest(tmp_path)
    assert "kept" in md
    for gone in ("from upstream", "digest echo", "raw sweep"):
        assert gone not in md


def test_never_opens_a_private_notes_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    for rel in ("scratchpad/a.md", ".scratchpad.md", "Old-Scratchpad/b.md", "notes/scratchpad-2/c.md"):
        repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- hidden-item\n", rel)
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- visible-item\n")
    for rel in ("-x-scratchpad-y/memory/feedback_a.md", "p/memory/feedback_scratchpad.md"):
        write(tmp_path / "mem" / rel, "---\ndescription: hidden-memory\n---\n")
    touched: list[str] = []
    real_open, real_scandir, real_read = builtins.open, os.scandir, Path.read_text

    def spy(path) -> None:
        if "scratchpad" in str(path).lower():
            touched.append(str(path))

    def spy_open(file, *a, **k):
        spy(file)
        return real_open(file, *a, **k)

    def spy_scandir(path=".", *a, **k):
        spy(path)
        return real_scandir(path, *a, **k)

    def spy_read(self, *a, **k):
        spy(self)
        return real_read(self, *a, **k)

    monkeypatch.setattr(builtins, "open", spy_open)
    monkeypatch.setattr(os, "scandir", spy_scandir)
    monkeypatch.setattr(Path, "read_text", spy_read)
    assert run(tmp_path) == 1
    assert touched == []
    md = digest(tmp_path)
    assert "visible-item" in md and "hidden-item" not in md and "hidden-memory" not in md


def test_memory_items_key_on_description_and_list_files_without_one(tmp_path: Path):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    write(tmp_path / "mem" / ".DS_Store", "not a project\n")
    write(tmp_path / "mem" / "q" / "memory", "a file, not a dir\n")
    write(tmp_path / "mem" / "p" / "memory" / "feedback_x.md", "---\nname: x\ndescription: Say the no first\n---\nbody\n")
    write(tmp_path / "mem" / "p" / "memory" / "feedback_y.md", "no front matter\n")
    assert run(tmp_path) == 1
    md = digest(tmp_path)
    memory = md.split("## Undisposed: memory")[1].split("##")[0]
    assert f"`{fh.item_key('Say the no first')}` 1 source(s), newest ~" in memory
    assert "feedback_y.md" in md.split("## Memory files with no description")[1]


def git(repo: Path, *args: str, when: str = "2026-10-01T12:00:00") -> None:
    env = {**os.environ, "GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when}
    _ = subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
        check=True, capture_output=True, env=env,
    )


def command(version: str, body: str) -> str:
    return f'---\nname: "pb-x"\nversion: "{version}"\nversion_notes: "v{version}: {body}"\n---\n\n# pb-x\n\n{body}\n'


def test_may_be_fixed_reads_the_newest_bump_that_changed_the_body(tmp_path: Path):
    pb = tmp_path / "pb"
    path = write(pb / "commands" / "core" / "pb-x.md", command("1.0.0", "first"))
    _ = subprocess.run(["git", "init", "-q", str(pb)], check=True)
    git(pb, "add", ".")
    git(pb, "commit", "-qm", "a", when="2026-09-01T12:00:00")
    _ = path.write_text(command("1.1.0", "fixed"))
    git(pb, "commit", "-qam", "b", when="2026-10-15T12:00:00")
    _ = path.write_text(command("1.1.0", "fixed more"))  # body edit, no bump
    git(pb, "commit", "-qam", "c", when="2026-10-20T12:00:00")
    _ = path.write_text(command("1.2.0", "fixed more"))  # bump, body unchanged
    git(pb, "commit", "-qam", "d", when="2026-10-25T12:00:00")

    repo_note(tmp_path, "o/old", "## 2026-10-01\nPlaybook feedback:\n- pb-x was wrong\n")
    repo_note(tmp_path, "o/new", "## 2026-10-18\nPlaybook feedback:\n- pb-x still wrong\n")
    assert run(tmp_path) == 1
    md = digest(tmp_path)
    old = next(line for line in md.splitlines() if "pb-x was wrong" in line)
    new = next(line for line in md.splitlines() if "pb-x still wrong" in line)
    assert "[may be fixed: pb-x v1.1.0 bumped 2026-10-15: v1.1.0: fixed]" in old
    assert "may be fixed" not in new


def test_a_taken_key_seen_again_later_holds_exit_1_until_re_ruled(tmp_path: Path):
    repo_note(tmp_path, "o/r", "## 2026-11-01\nPlaybook feedback:\n- recurring\n")
    row = f"key\tdisposition\tversion\tdate\n{fh.item_key('recurring')}\ttaken\tv1\t"
    write(tmp_path / "ledger.tsv", row + "2026-10-01\n")
    assert run(tmp_path) == 1
    assert "recurring" in digest(tmp_path).split("## Taken, then seen again")[1].split("##")[0]
    write(tmp_path / "ledger.tsv", row + "2026-11-02\n")
    assert run(tmp_path) == 0


def test_a_dup_of_member_seen_again_reads_its_representatives_ruling(tmp_path: Path):
    repo_note(tmp_path, "o/r", "## 2026-11-01\nPlaybook feedback:\n- member wording\n")
    rep, member = fh.item_key("rep wording"), fh.item_key("member wording")
    ledger = f"key\tdisposition\tversion\tdate\n{rep}\ttaken\tv1\t2026-10-01\n{member}\tdup-of:{rep}\t\t"
    write(tmp_path / "ledger.tsv", ledger + "2026-11-04\n")
    assert run(tmp_path) == 1
    assert "member wording" in digest(tmp_path).split("## Taken, then seen again")[1].split("##")[0]


def test_an_mtime_dated_item_never_recurs(tmp_path: Path):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    write(tmp_path / "mem" / "p" / "memory" / "feedback_x.md", "---\ndescription: Edited later\n---\n")
    write(tmp_path / "ledger.tsv", (
        f"key\tdisposition\tversion\tdate\n{fh.item_key('Edited later')}\ttaken\tv1\t2026-01-01\n"
        f"{fh.item_key('one')}\ttaken\tv1\t2026-11-04\n"
    ))
    assert run(tmp_path) == 0
    assert "Edited later" not in digest(tmp_path).split("## Taken, then seen again")[1].split("##")[0]


def test_pb_pause_template_heading_feeds_the_harvester():
    """Renaming the heading pb-pause asks for would silently starve the loop."""
    pause = Path(__file__).resolve().parent.parent / "commands" / "development" / "pb-pause.md"
    lines = pause.read_text().split("\n")
    hits = [n for n, line in enumerate(lines) if fh.HEADING.match(line)]
    assert len(hits) == 1, f"pb-pause lines matching the harvester heading: {[lines[n] for n in hits]}"
    n = hits[0]
    assert lines[n] == "Patterns / playbook feedback:"
    assert fh.PLACEHOLDER.match(fh.BULLET.match(lines[n + 1]).group("text")), "the template's placeholder bullet follows it"
