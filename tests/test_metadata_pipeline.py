"""Guards for the metadata extraction pipeline.

The pipeline (extract-playbook-metadata.py -> .playbook-metadata.json ->
validate-extracted-metadata.py) feeds /pb-what-next. Its output is gitignored,
so nothing in the repo records whether it still works; before these tests it ran
in no CI job and had no coverage, and a category allow-list inside it had drifted
to reject all 7 commands under commands/utilities/.
"""
import json
from pathlib import Path

import pytest

from playbook_utils import VALID_CATEGORIES

REPO_ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIR = REPO_ROOT / "commands"


def test_valid_categories_matches_directories():
    """The allow-list is a claim about the filesystem; check it against the filesystem.

    Four copies of this list existed and two were wrong -- including the one in
    playbook_utils, which had no consumers and so drifted unnoticed.
    """
    on_disk = {d.name for d in COMMANDS_DIR.iterdir() if d.is_dir()}
    assert VALID_CATEGORIES == on_disk, (
        f"VALID_CATEGORIES vs commands/ dirs: "
        f"only in constant={sorted(VALID_CATEGORIES - on_disk)}, "
        f"only on disk={sorted(on_disk - VALID_CATEGORIES)}"
    )


@pytest.fixture(scope="module")
def extracted(load_script):
    extractor = load_script("extract-playbook-metadata.py")
    return extractor.PlaybookMetadataExtractor(repo_root=REPO_ROOT).extract_all()


def test_extraction_covers_every_command(extracted):
    """Invariant 1: a record per command file, or the artifact silently under-reports."""
    on_disk = {p.stem for p in COMMANDS_DIR.rglob("pb-*.md")}
    extracted_names = set(extracted["commands"])
    assert extracted_names == on_disk, (
        f"missing from extraction={sorted(on_disk - extracted_names)}, "
        f"extra={sorted(extracted_names - on_disk)}"
    )
    assert extracted["total_commands"] == len(on_disk)


def test_validator_accepts_the_real_corpus(extracted, load_script):
    """The corpus is the input the pipeline actually runs on; it must pass cleanly."""
    validator = load_script("validate-extracted-metadata.py")
    checker = validator.MetadataValidator()
    assert checker.validate(extracted) is True, f"critical errors: {checker.errors}"


def test_validator_rejects_a_malformed_record(extracted, load_script):
    """Invariant 2: a validator that cannot fail is not a validator.

    Without this, test_validator_accepts_the_real_corpus passes just as happily
    against a validator whose checks have been gutted.
    """
    validator = load_script("validate-extracted-metadata.py")
    name = next(iter(extracted["commands"]))

    for field, bad_value in (
        ("category", "no-such-category"),
        ("title", ""),
    ):
        corrupt = json.loads(json.dumps(extracted))
        corrupt["commands"][name][field] = bad_value
        checker = validator.MetadataValidator()
        assert checker.validate(corrupt) is False, f"accepted a bad {field}"
        assert any(e["command"] == name for e in checker.errors)
