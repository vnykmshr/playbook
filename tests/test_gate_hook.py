"""hooks/external-action-gate.sh asks on known external-action shapes.

Each case pipes the PreToolUse JSON Claude Code sends and asserts the matched
label, so a hook that asks for another reason (jq missing) cannot pass a case.
KNOWN_MISSES is the hook's gap list: each asserts "ask" under xfail(strict=True),
so closing a gap fails until its entry is deleted. The list only shrinks.
"""
import json
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
]


@pytest.mark.xfail(strict=True, reason="known gap: delete the entry when the hook catches it")
@pytest.mark.parametrize("command", KNOWN_MISSES)
def test_known_miss(command: str):
    assert reason(run_hook(command)) is not None


def test_jq_missing_asks_on_everything(tmp_path: Path):
    got = reason(run_hook("git status", env={"PATH": str(tmp_path)}))
    assert got is not None and "jq missing" in got


@pytest.mark.parametrize("payload", ["not json", "", '{"tool_input": {"cmd": "git push"}}'])
def test_unreadable_input_asks(payload: str):
    got = reason(run_hook("", payload=payload))
    assert got is not None and "input not parsed" in got


def run_install(home: Path) -> subprocess.CompletedProcess[str]:
    script = HOOK.parent.parent / "scripts" / "install.sh"
    return subprocess.run(
        ["bash", str(script)], env={"PATH": "/usr/bin:/bin", "HOME": str(home)},
        capture_output=True, text=True,
    )


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
