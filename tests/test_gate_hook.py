"""hooks/external-action-gate.sh asks on known external-action shapes.

Each case pipes the PreToolUse JSON Claude Code sends and asserts the matched
label, so a hook that asks for another reason (jq missing) cannot pass a case.
KNOWN_MISSES is the hook's gap list: each asserts "ask" under xfail(strict=True),
so closing a gap fails until its entry is deleted. KNOWN_FALSE_POSITIVES is the
reverse, asserting silence. Both lists only shrink.
"""
import json
import shutil
import subprocess
from pathlib import Path
from typing import cast

import pytest

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "external-action-gate.sh"


def run_hook(command: str, env: dict[str, str] | None = None, payload: str | None = None) -> subprocess.CompletedProcess[str]:
    if payload is None:
        payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    return subprocess.run(
        ["/bin/bash", str(HOOK)], input=payload, capture_output=True, text=True, env=env
    )


PREFIX, SUFFIX = "external-action-gate: ", " -- needs your explicit go"


def labels(got: str) -> list[str]:
    assert got.startswith(PREFIX) and got.endswith(SUFFIX), got
    return got[len(PREFIX) : -len(SUFFIX)].split("; ")


def reason(result: subprocess.CompletedProcess[str]) -> str | None:
    """The ask reason, or None when the hook stayed silent."""
    assert result.returncode == 0, result.stderr
    if not result.stdout.strip():
        return None
    out = cast(dict[str, dict[str, str]], json.loads(result.stdout))["hookSpecificOutput"]
    assert out["permissionDecision"] == "ask"
    return out["permissionDecisionReason"]


ASKS = [
    ("git push origin main", "git push"),
    ("git -C /x push", "git push"),
    ("git -c core.x=y push", "git push"),
    ("git push --follow-tags origin main", "git push"),
    ("cd repo && git push", "git push"),
    ("echo 'then git push'", "git push"),
    ("git send-pack remote", "git send-pack"),
    ("git reset --hard HEAD~1", "git reset --hard"),
    ("git checkout -- .", "git checkout/restore ."),
    ("git checkout .", "git checkout/restore ."),
    ("git restore .", "git checkout/restore ."),
    ("git restore -- .", "git checkout/restore ."),
    ("git clean -fd", "git clean -f"),
    ("git clean --force", "git clean -f"),
    ("/usr/bin/git push", "git push"),
    ("GIT push", "git push"),
    ("git -P push", "git push"),
    ("git --git-dir .git push", "git push"),
    ("gh -R x/y pr merge 3", "gh pr/issue write"),
    ("gh -Rx/y pr merge 3", "gh pr/issue write"),
    ("gh --repo x/y release create v1", "gh release write"),
    ("gh issue delete 5", "gh pr/issue write"),
    ("gh issue transfer 5 x/z", "gh pr/issue write"),
    ("gh pr create --fill", "gh pr/issue write"),
    ("gh pr merge 3", "gh pr/issue write"),
    ("gh issue comment 4 -b x", "gh pr/issue write"),
    ("gh release create v1", "gh release write"),
    ("gh repo delete x/y", "gh repo write"),
    ("gh workflow run deploy.yml", "gh workflow run"),
    ("gh run rerun 12", "gh workflow run"),
    ("gh api -X DELETE repos/x/y", "gh api write method"),
    ("gh api repos/x/y/issues -f title=t", "gh api with fields (defaults to POST)"),
    ("npm publish", "publish"),
    ("pnpm publish", "publish"),
    ("yarn publish", "publish"),
    ("docker push img", "publish"),
    ("twine upload dist/*", "publish"),
    ("npx wrangler deploy", "worker deploy"),
    ("npm run worker:deploy", "worker deploy"),
    ("rm -rf build", "rm -r"),
    ("rm -r -f build", "rm -r"),
    ("rm -f -r build", "rm -r"),
    ("rm -Rf build", "rm -r"),
    ("rm -fR build", "rm -r"),
    ("rm --recursive --force build", "rm -r"),
    ("rm -r build", "rm -r"),
    ("rm --rec build", "rm -r"),
    ('rm -rf"" build', "rm -r"),
    (r"rm -r\f build", "rm -r"),
    # a quoted ; & or | stays inside its segment
    ("gh api repos/o/r/issues --jq '.number | tostring' -f title=t", "gh api with fields (defaults to POST)"),
    ("gh api graphql --jq '.data | .x' -f query=q", "gh api with fields (defaults to POST)"),
    ("gh api 'repos/o/r/issues?a=1&b=2' -X POST", "gh api write method"),
    ("gh api repos/o/r --jq '.[] | .x' --method POST", "gh api write method"),
    ("wrangler --config 'a|b' deploy", "worker deploy"),
    ("git clean -d -n -- 'x;y' -f", "git clean -f"),
    # normalised: one case, backslash-newline joined with a space
    ("GH pr merge 3", "gh pr/issue write"),
    ("RM -rf build", "rm -r"),
    ("NPM publish", "publish"),
    ("rm \\\n  -rf build", "rm -r"),
    ("gh api -X post repos/x/y", "gh api write method"),
    ("echo C:\\\\\nrm -rf build", "rm -r"),
]


@pytest.mark.parametrize("command,label", ASKS)
def test_asks_with_the_matched_label(command: str, label: str):
    got = reason(run_hook(command))
    assert got is not None, f"{command!r} should ask"
    assert label in labels(got)


def test_chained_command_reports_every_label():
    got = reason(run_hook("git push origin a && gh release create v1"))
    assert got is not None
    assert labels(got) == ["git push", "gh release write"]


SILENT = [
    "git status",
    "git log --oneline -5",
    "gh pr view 3",
    "gh release list",
    "rm -f one-file",
    "rm one-file && ls -R",
    "rm -f old-report",
    "grep -n push notes.md",
    "git --no-pager log --oneline",
    "git restore --staged .",
    "rm -f out.txt\ngrep -rn foo .",
    "git clean -n && ls -lF",
    "git --no-pager grep -n push",
    "rm -f $(find . -name '*.pyc' -print)",
    "git clean -n && ls -lf",
    "git reset --soft HEAD~1 && grep --hard x",
]


@pytest.mark.parametrize("command", SILENT)
def test_read_only_commands_stay_silent(command: str):
    assert reason(run_hook(command)) is None


KNOWN_MISSES = [
    r"\git push",
    '"git" push',
    'g""it push',
    'eval "git push"',
    'sh -c "git push"',
    "bash -c 'git push'",
    "git -c alias.p=push p origin main",
    "curl -X POST https://api.github.com/repos/x/y/issues",
    "python3 -c 'import subprocess; subprocess.run([\"git\", \"push\"])'",
    "./scripts/release.sh",
    "make release",
    "npm run deploy",
    "gh secret set X",
    "gh pr ready 3",
    "gh repo sync",
    "gh gist create f",
    "gh api repos/x/y/issues -ftitle=t",
    'rm "-rf" build',
    "git restore --worktree .",
    "git checkout HEAD -- .",
    "rm $(echo x) -rf build",
    "git --attr-source HEAD push",
    # SEG approximates a shell segment: quotes must balance, a backslash escapes nothing,
    # $() and backticks do not nest, and the & of a redirection reads as a separator.
    # A rule's later word past such a spot is unseen; the pre-SEG `.*` asked on these.
    r'git reset \" --hard',
    r"git clean -e $'it\'s' -f",
    r"git clean -e 'a'\''b' -f",
    r"git reset a\;b --hard",
    "gh api $(echo repos/o/r | cat) -X POST",
    "gh api `echo repos/o/r | cat` -X POST",
    "git reset HEAD~1 2>&1 --hard",
    "git reset HEAD~1 &>/dev/null --hard",
]


@pytest.mark.xfail(strict=True, reason="known gap: delete the entry when the hook catches it")
@pytest.mark.parametrize("command", KNOWN_MISSES)
def test_known_miss(command: str):
    assert reason(run_hook(command)) is not None


KNOWN_FALSE_POSITIVES = [
    "git rm -r --cached build",
]


@pytest.mark.xfail(strict=True, reason="known false positive: delete the entry when the hook stays silent")
@pytest.mark.parametrize("command", KNOWN_FALSE_POSITIVES)
def test_known_false_positive(command: str):
    assert reason(run_hook(command)) is None


EVERY_COMMAND = [c for c, _ in ASKS] + SILENT + KNOWN_MISSES + KNOWN_FALSE_POSITIVES


@pytest.mark.parametrize("command", EVERY_COMMAND)
def test_decision_survives_case_and_line_continuation(command: str):
    """Same decision upper-cased or split by backslash-newline (pinned ASKS cover what this cannot)."""
    asks = reason(run_hook(command)) is not None
    for variant in (command.upper(), command.replace(" ", " \\\n  ", 1)):
        assert (reason(run_hook(variant)) is not None) == asks, repr(variant)


def test_jq_missing_asks_on_everything(tmp_path: Path):
    got = reason(run_hook("git status", env={"PATH": str(tmp_path)}))
    assert got is not None and "jq missing" in got


def test_normalise_failure_asks(tmp_path: Path):
    jq = shutil.which("jq")
    assert jq, "jq is needed to reach the normalise step"
    (tmp_path / "jq").symlink_to(jq)
    got = reason(run_hook("git status", env={"PATH": str(tmp_path)}))
    assert got is not None and "normalise failed" in got


@pytest.mark.parametrize("payload", ["not json", "", '{"tool_input": {"cmd": "git push"}}'])
def test_unreadable_input_asks(payload: str):
    got = reason(run_hook("", payload=payload))
    assert got is not None and "input not parsed" in got


def run_install(home: Path, **env: str) -> subprocess.CompletedProcess[str]:
    script = HOOK.parent.parent / "scripts" / "install.sh"
    return subprocess.run(
        ["bash", str(script)], env={"PATH": "/usr/bin:/bin", "HOME": str(home), **env},
        capture_output=True, text=True,
    )


def oldest_committed_hook() -> bytes:
    repo = HOOK.parent.parent
    blobs = subprocess.run(
        ["git", "-C", str(repo), "log", "--format=", "--raw", "--no-abbrev", "--", "hooks/external-action-gate.sh"],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    blob = [b for b in blobs if len(b) == 40 and b.strip("0")][-1]
    return subprocess.run(["git", "-C", str(repo), "cat-file", "blob", blob], capture_output=True, check=True).stdout


def hook_dest(home: Path) -> Path:
    dest = home / ".claude" / "hooks" / "external-action-gate.sh"
    dest.parent.mkdir(parents=True, exist_ok=True)
    return dest


def test_install_copies_the_hook_and_keeps_a_changed_copy(tmp_path: Path):
    dest = tmp_path / ".claude" / "hooks" / "external-action-gate.sh"

    assert run_install(tmp_path).returncode == 0
    assert dest.is_file() and not dest.is_symlink(), "a link would follow the checkout"
    assert dest.read_bytes() == HOOK.read_bytes()

    _ = dest.write_text("# local edit\n")
    result = run_install(tmp_path)
    assert result.returncode == 0
    assert dest.read_text() == "# local edit\n", "a changed copy is the user's, not install's"
    assert "differs from hooks/" in result.stdout


def test_install_replaces_a_committed_older_copy(tmp_path: Path):
    old = oldest_committed_hook()
    assert old != HOOK.read_bytes()
    dest = hook_dest(tmp_path)
    _ = dest.write_bytes(old)
    result = run_install(tmp_path)
    assert result.returncode == 0, result.stderr
    assert dest.read_bytes() == HOOK.read_bytes(), "an unedited older install is replaced"


def test_install_replaces_a_symlinked_copy(tmp_path: Path):
    target = tmp_path / "elsewhere.sh"
    _ = target.write_text("# linked\n")
    dest = hook_dest(tmp_path)
    dest.symlink_to(target)
    assert run_install(tmp_path).returncode == 0
    assert dest.is_file() and not dest.is_symlink()
    assert dest.read_bytes() == HOOK.read_bytes()


@pytest.mark.parametrize("why", ["not a checkout", "git fails"])
def test_install_keeps_an_older_copy_when_git_cannot_say(tmp_path: Path, why: str):
    if why == "not a checkout":
        env = {"GIT_DIR": str(tmp_path / "none")}
    else:
        fake = tmp_path / "bin"
        fake.mkdir()
        _ = (fake / "git").write_text("#!/bin/sh\nexit 1\n")
        (fake / "git").chmod(0o755)
        env = {"PATH": f"{fake}:/usr/bin:/bin"}
    dest = hook_dest(tmp_path)
    _ = dest.write_bytes(oldest_committed_hook())
    result = run_install(tmp_path, **env)
    assert result.returncode == 0, result.stderr
    assert dest.read_bytes() == oldest_committed_hook(), "unverifiable, so kept"
    assert "differs from hooks/" in result.stdout
