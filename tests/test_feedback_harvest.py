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


HEADER = "key\tdisposition\tversion\tdate\ttext\n"


def row(note: str, disp: str, version: str = "v1", when: str = "2026-11-04") -> str:
    """One ledger row for a note, keyed and texted as the harvester computes them."""
    return f"{fh.item_key(note)}\t{disp}\t{version}\t{when}\t{fh.normalise(note)}\n"


def ledger(*rows: str) -> str:
    return HEADER + "".join(rows)


def texts(md: str) -> list[str]:
    return [t for _, t in fh.extract(md)[0]]


def test_golden_key():
    """A normaliser change orphans every ledger row: it must fail here first, and the ledger's
    text column is what a rekey recomputes from."""
    assert fh.normalise("**Fix** `pb-pause` Step 6  (2026-10-14) [see](http://x)") == "fix pb pause step 6 see"
    assert fh.item_key("**Fix** `pb-pause` Step 6  (2026-10-14) [see](http://x)") == "504571ef8b57"


@pytest.mark.parametrize("a, b, same", [
    ("rule holds — keep it", "rule holds, keep it", True),
    ("pb-pause: step 6.", "pb pause step 6", True),
    ("_emphasis_ and “quotes”", "emphasis and quotes", True),
    ("<= 5", "5", False),
    ("a → b", "a b", False),
    ("café", "caf", False),
    ("$x | y", "x y", False),
])
def test_punctuation_is_dropped_and_symbols_kept(a: str, b: str, same: bool):
    """A dash-to-comma voice pass must not re-present a ruled note; an operator must not merge two."""
    assert (fh.item_key(a) == fh.item_key(b)) is same


def test_normalise_is_idempotent_so_the_text_column_can_rekey():
    for note in ("**Fix** `pb-pause` (2026-10-14) [see](http://x) — done", "a ~~b~~ → c; d!"):
        assert fh.normalise(fh.normalise(note)) == fh.normalise(note)


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


def test_an_item_that_normalises_to_nothing_is_no_item():
    """Its key would be sha256("")[:12], which no ledger row can carry: exit 1 for good."""
    items, empty = fh.extract("Playbook feedback:\n- ...\n- \u2014\n- 2026-11-04\n")
    assert items == [] and empty == [1]
    items, _ = fh.extract("Playbook feedback:\n- ...\n- real\n")
    assert [t for _, t in items] == ["real"]


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
    write(tmp_path / "ledger.tsv", ledger(row("one", "taken")))
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


@pytest.mark.parametrize("text, says", [
    ("key\tdisposition\tversion\tdate\n", "header must be"),
    (ledger(row("one", "taken").replace("\t2026-11-04\tone", "\t2026-11-04")), "4 columns, want 5"),
    (ledger("abc\ttaken\tv1\t2026-11-04\tone\n"), "not 12 hex"),
    (ledger(row("one", "seen")), "disposition 'seen'"),
    (ledger(row("one", "dup-of:xyz")), "disposition 'dup-of:xyz'"),
    (ledger(row("one", "taken", when="soon")), "date 'soon'"),
    (ledger(row("one", "taken"), row("one", "rejected", "", "2026-11-05")), "repeats line 2"),
    (ledger(row("one", f"dup-of:{fh.item_key('gone')}", "")), "names no key"),
    (ledger(row("one", f"dup-of:{fh.item_key('two')}", ""), row("two", f"dup-of:{fh.item_key('one')}", "")), "names no key"),
    (ledger(f"{fh.item_key('one')}\ttaken\tv1\t2026-11-04\tone edited\n"), "text hashes to"),
    (ledger(f"{fh.item_key('one')}\ttaken\tv1\t2026-11-04\t\n"), "text hashes to"),
    (ledger(row("one", "deferred", "q1-2027")), "deferred to 'q1-2027'"),
    (ledger(row("one", "deferred", "2027-q5")), "deferred to '2027-q5'"),
    (ledger(row("one", "deferred", "v2.35.0")), "deferred to 'v2.35.0'"),
])
def test_exit_2_on_a_malformed_ledger(tmp_path: Path, capsys: pytest.CaptureFixture[str], text: str, says: str):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    write(tmp_path / "ledger.tsv", text)
    assert run(tmp_path) == 2
    assert says in capsys.readouterr().err


def test_any_error_exits_2_not_1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    monkeypatch.setenv("PATH", str(tmp_path / "no-bin"))
    write(tmp_path / "repos" / "o" / "r" / ".git" / "HEAD", "ref: refs/heads/main\n")
    assert run(tmp_path) == 2, "git missing"


def test_a_repo_git_cannot_list_exits_2_and_is_named(tmp_path: Path):
    repo_note(tmp_path, "o/broken", "## 2026-10-01\nPlaybook feedback:\n- unvetted\n")
    write(tmp_path / "repos" / "o" / "broken" / ".git", "gitdir: /nowhere\n")
    repo_note(tmp_path, "o/plain", "## 2026-10-01\nPlaybook feedback:\n- kept\n")
    write(tmp_path / "ledger.tsv", ledger(row("kept", "taken")))
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
    write(tmp_path / "ledger.tsv", ledger(row("Kept", "taken")))
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


def every_level(tmp_path: Path) -> None:
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- in sub\n", "sub/a.md")
    write(tmp_path / "mem" / "p" / "memory" / "feedback_x.md", "---\ndescription: Mem\n---\n")


@pytest.mark.parametrize("suffix", ["repos/o", "repos/o/r/todos", "todos/sub", "repos/o/r/todos/sub/a.md", "mem", "p/memory"])
def test_an_unreadable_dir_or_file_at_any_level_exits_2(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, suffix: str):
    every_level(tmp_path)
    unreadable(monkeypatch, suffix)
    assert run(tmp_path) == 2
    assert any(x.endswith(suffix + "`") for x in digest(tmp_path).split("## Paths unread")[1].split("##")[0].splitlines())


@pytest.mark.parametrize("link, target", [
    ("repos/l", "repos/o"),
    ("repos/o/l", "repos/o/r"),
    ("repos/o/s/todos", "elsewhere/scratchpad"),
    ("repos/o/r/todos/linked", "elsewhere/scratchpad"),
    ("mem/l", "mem/p"),
    ("mem/q/memory", "mem/p/memory"),
])
def test_a_link_at_any_level_is_listed_and_never_followed(tmp_path: Path, link: str, target: str):
    every_level(tmp_path)
    write(tmp_path / "elsewhere" / "scratchpad" / "notes.md", "## 2026-10-01\nPlaybook feedback:\n- secret scratch\n")
    (tmp_path / link).parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / link).symlink_to(tmp_path / target, target_is_directory=True)
    assert run(tmp_path) == 1, "a link is listed, not an exit"
    md = digest(tmp_path)
    assert "secret scratch" not in md and md.count("Mem\n") <= 1
    assert f"{tmp_path / link}`" in md.split("## Links not followed")[1]


def test_a_symlinked_root_is_resolved_and_harvested(tmp_path: Path):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- via link\n")
    (tmp_path / "rootlink").symlink_to(tmp_path / "repos", target_is_directory=True)
    args = ["--repos", str(tmp_path / "rootlink"), "--memory", str(tmp_path / "mem"), "--playbook", str(tmp_path / "pb"),
            "--ledger", str(tmp_path / "ledger.tsv"), "--out", str(tmp_path / "out")]
    assert fh.main(args) == 1
    assert "via link" in digest(tmp_path)


def test_a_repo_whose_todos_cannot_be_stat_exits_2(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    every_level(tmp_path)
    real = Path.lstat

    def lstat(self, *a, **k):
        if str(self).endswith("repos/o/r/todos"):
            raise PermissionError(13, "denied", str(self))
        return real(self, *a, **k)

    monkeypatch.setattr(Path, "lstat", lstat)
    assert run(tmp_path) == 2
    assert "repos/o/r/todos`" in digest(tmp_path).split("## Paths unread")[1]


def test_exit_1_then_0_once_every_key_is_dispositioned(tmp_path: Path):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n- two\n")
    assert run(tmp_path) == 1, "a missing ledger reads as empty"
    write(tmp_path / "ledger.tsv", ledger(row("one", "taken", "v2.33.0")))
    assert run(tmp_path) == 1
    write(tmp_path / "ledger.tsv", ledger(row("one", "taken", "v2.33.0"), row("two", f"dup-of:{fh.item_key('one')}", "v2.33.0")))
    assert run(tmp_path) == 0
    assert not (tmp_path / "pb").exists() or not any((tmp_path / "pb").rglob("*.tsv")), "never writes a ledger"


def test_sources_are_distinct_repos_and_private_orgs_are_flagged(tmp_path: Path):
    write(tmp_path / "pb" / "todos" / "evolve" / "harvest.toml", 'private = ["acme"]\n')
    repo_note(tmp_path, "o/a", "## 2026-10-01\nPlaybook feedback:\n- Same **thing**\n")
    repo_note(tmp_path, "o/a", "## 2026-10-02\nPlaybook feedback:\n- same thing\n", "done/lessons.md")
    repo_note(tmp_path, "acme/b", "## 2026-10-03\nPlaybook feedback:\n- same `thing`\n")
    write(tmp_path / "mem" / f"{fh.project_dir(tmp_path / 'repos' / 'acme')}-c" / "memory" / "feedback_z.md",
          "---\ndescription: Mem note\n---\n")
    assert run(tmp_path) == 1
    md = digest(tmp_path)
    assert f"`{fh.item_key('same thing')}` 2 source(s), newest 2026-10-03 [private]" in md
    assert next(x for x in md.splitlines() if "Mem note" in x).count("[private]") == 1


@pytest.mark.parametrize("source, flagged", [
    ("acme/x", True), ("ACME/x", True), ("memory:-src-acme-x", True), ("memory:-src-acme", True),
    ("memory:-SRC-Acme-x-todos", True), ("memory:-src-acme-labs-x", True),
    ("acme-labs/x", False), ("o/acme", False), ("memory:-other-acme-x", False), ("memory:-src-acmex", False),
])
def test_private_org_match(source: str, flagged: bool):
    cfg = fh.Config((Path("/src"),), Path("/m"), frozenset({"acme"}), "")
    assert fh.is_private(source, cfg) is flagged


def test_config_supplies_roots_and_its_absence_is_a_fault(tmp_path: Path):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    base = ["--memory", str(tmp_path / "mem"), "--playbook", str(tmp_path / "pb"),
            "--ledger", str(tmp_path / "ledger.tsv"), "--out", str(tmp_path / "out")]
    assert fh.main(base) == 2, "no --repos and no config: never a guessed default"
    write(tmp_path / "pb" / "todos" / "evolve" / "harvest.toml", f'repos = ["{tmp_path / "repos"}"]\nprivate = []\n')
    assert fh.main(base) == 1
    write(tmp_path / "pb" / "todos" / "evolve" / "harvest.toml", f'repos = ["{tmp_path / "repos"}"]\n')
    assert fh.main(base) == 2, "private left out would silently flag nothing"
    write(tmp_path / "pb" / "todos" / "evolve" / "harvest.toml", 'repos = "not-a-list"\nprivate = []\n')
    assert fh.main(base) == 2


def test_an_explicit_config_that_does_not_exist_is_a_fault(tmp_path: Path):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    assert run(tmp_path, "--config", str(tmp_path / "typo.toml")) == 2


def test_a_relative_or_linked_root_still_flags_private_memory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    (tmp_path / "real" / "acme").mkdir(parents=True)
    (tmp_path / "link").symlink_to(tmp_path / "real", target_is_directory=True)
    monkeypatch.chdir(tmp_path)
    for root in (Path("real"), Path("link")):
        cfg = fh.Config((root,), Path("/m"), frozenset({"acme"}), "")
        for form in (tmp_path / "real", tmp_path / root):
            assert fh.is_private(f"memory:{fh.project_dir(form / 'acme')}-x", cfg), (root, form)


def test_init_refuses_a_root_toml_cannot_carry(tmp_path: Path):
    pb = tmp_path / "w\U0001F600" / "org" / "playbook"
    pb.mkdir(parents=True)
    assert fh.main(["--init", "--playbook", str(pb)]) == 2, "json quoting gives surrogates, which TOML rejects"
    assert not (pb / "todos" / "evolve" / "harvest.toml").exists()


def test_init_derives_the_root_and_never_overwrites(tmp_path: Path):
    pb = tmp_path / "root" / "org" / "playbook"
    pb.mkdir(parents=True)
    config = pb / "todos" / "evolve" / "harvest.toml"
    assert fh.main(["--init", "--playbook", str(pb)]) == 0
    cfg = fh.load_config(config, None, None)
    assert cfg.repos == ((tmp_path / "root").resolve(),) and cfg.private == frozenset()
    assert fh.main(["--init", "--playbook", str(pb)]) == 2, "never overwrites"


@pytest.mark.parametrize("root, org, project", [
    ("/home/a.b/src_x", "my-org", "-home-a-b-src-x-my-org-repo"),
    ("/src", "acme", "-src-acme"),
])
def test_project_dir_matches_claude_codes_encoding(root: str, org: str, project: str):
    cfg = fh.Config((Path(root),), Path("/m"), frozenset({org}), "")
    assert project.startswith(fh.project_dir(Path(root) / org))
    assert fh.is_private(f"memory:{project}", cfg)


def test_digest_says_whether_the_config_was_read(tmp_path: Path):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    assert run(tmp_path) == 1
    assert "config missing" in digest(tmp_path)
    write(tmp_path / "pb" / "todos" / "evolve" / "harvest.toml", f'repos = ["{tmp_path / "repos"}"]\nprivate = ["Acme"]\n')
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
    write(tmp_path / "mem" / "p" / "memory" / "feedback_z.md", "---\nname: z\ndescription: \"...\"\n---\nbody\n")
    assert run(tmp_path) == 1
    md = digest(tmp_path)
    memory = md.split("## Undisposed: memory")[1].split("##")[0]
    assert f"`{fh.item_key('Say the no first')}` 1 source(s), newest ~" in memory
    no_desc = md.split("## Memory files with no description")[1]
    assert "feedback_y.md" in no_desc and "feedback_z.md" in no_desc


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
    write(tmp_path / "ledger.tsv", ledger(row("recurring", "taken", when="2026-10-01")))
    assert run(tmp_path) == 1
    assert "recurring" in digest(tmp_path).split("## Taken, then seen again")[1].split("##")[0]
    write(tmp_path / "ledger.tsv", ledger(row("recurring", "taken", when="2026-11-02")))
    assert run(tmp_path) == 0


def test_a_dup_of_member_seen_again_reads_its_representatives_ruling(tmp_path: Path):
    repo_note(tmp_path, "o/r", "## 2026-11-01\nPlaybook feedback:\n- member wording\n")
    write(tmp_path / "ledger.tsv", ledger(
        row("rep wording", "taken", when="2026-10-01"), row("member wording", f"dup-of:{fh.item_key('rep wording')}", "")))
    assert run(tmp_path) == 1
    assert "member wording" in digest(tmp_path).split("## Taken, then seen again")[1].split("##")[0]


def test_an_mtime_dated_item_never_recurs(tmp_path: Path):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    write(tmp_path / "mem" / "p" / "memory" / "feedback_x.md", "---\ndescription: Edited later\n---\n")
    write(tmp_path / "ledger.tsv", ledger(row("Edited later", "taken", when="2026-01-01"), row("one", "taken")))
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


@pytest.mark.parametrize("q, first", [("1", "01"), ("2", "04"), ("3", "07"), ("4", "10")])
def test_quarter_start_is_the_quarters_first_day(q: str, first: str):
    assert fh.quarter_start(f"2027-q{q}") == f"2027-{first}-01"


@pytest.mark.parametrize("today, code", [("2027-03-31", 0), ("2027-04-01", 1)])
def test_a_q2_deferral_comes_due_on_april_first(tmp_path: Path, today: str, code: int):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    write(tmp_path / "ledger.tsv", ledger(row("one", "deferred", "2027-q2")))
    assert run(tmp_path, "--today", today) == code


@pytest.mark.parametrize("today, code", [("2026-12-31", 0), ("2027-01-01", 1), ("2027-03-31", 1)])
def test_a_deferred_row_comes_due_on_its_quarters_first_day(tmp_path: Path, today: str, code: int):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n- two\n")
    write(tmp_path / "ledger.tsv", ledger(
        row("one", "deferred", "2027-q1"), row("two", f"dup-of:{fh.item_key('one')}", "")))
    assert run(tmp_path, "--today", today) == code
    md = digest(tmp_path)
    assert md.startswith(f"# Feedback digest {today}") and f"(today {today})" in md
    due = md.split("## Deferred, now due")[1].split("\n## ")[0]
    assert (f"`{fh.item_key('one')}` 2027-q1, ruled 2026-11-04 (+1 dup-of): one" in due) is bool(code)
    assert f"`{fh.item_key('one')}` 2027-q1" in md.split("## Deferred backlog")[1]


def test_a_due_deferred_row_holds_exit_1_after_its_note_is_deleted(tmp_path: Path):
    """The backlog lives in the ledger: discarding the note never closes the deferral."""
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- kept\n")
    write(tmp_path / "ledger.tsv", ledger(row("kept", "taken"), row("Gone — deleted note", "deferred", "2027-q1")))
    assert run(tmp_path, "--today", "2027-01-01") == 1
    assert "gone deleted note" in digest(tmp_path).split("## Deferred, now due")[1]
    write(tmp_path / "ledger.tsv", ledger(row("kept", "taken"), row("Gone — deleted note", "deferred", "2027-q2")))
    assert run(tmp_path, "--today", "2027-01-01") == 0


@pytest.mark.parametrize("today", ["2027-1-1", "tomorrow", "2027-02-30"])
def test_a_malformed_today_exits_2(tmp_path: Path, today: str):
    repo_note(tmp_path, "o/r", "## 2026-10-01\nPlaybook feedback:\n- one\n")
    assert run(tmp_path, "--today", today) == 2
