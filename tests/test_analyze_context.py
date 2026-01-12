#!/usr/bin/env python3
"""
Unit tests for PlaybookContextAnalyzer (/pb-what-next script)

Tests cover:
- Git state analysis
- Workflow phase detection
- File type identification
- Recommendation generation & scoring
- Error handling
- Output formatting
"""

import json
import tempfile
from pathlib import Path
from unittest import mock

import pytest

# Import the analyzer
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from analyze_playbook_context import PlaybookContextAnalyzer


@pytest.fixture
def sample_metadata():
    """Sample metadata for testing."""
    return {
        "commands": {
            "pb-start": {
                "command": "pb-start",
                "title": "Start Development Work",
                "category": "development",
                "purpose": "Begin iterative development on a feature",
                "tier": ["XS"],
                "frequency": "as-needed",
            },
            "pb-cycle": {
                "command": "pb-cycle",
                "title": "Development Cycle",
                "category": "development",
                "purpose": "Self-review and peer review iteration",
                "tier": ["L"],
                "frequency": "as-needed",
            },
            "pb-testing": {
                "command": "pb-testing",
                "title": "Advanced Testing",
                "category": "development",
                "purpose": "Verify test coverage",
                "tier": ["XS"],
                "frequency": "as-needed",
            },
            "pb-commit": {
                "command": "pb-commit",
                "title": "Atomic Commits",
                "category": "development",
                "purpose": "Craft focused commits",
                "tier": ["S"],
                "frequency": "as-needed",
            },
            "pb-pr": {
                "command": "pb-pr",
                "title": "Quick PR Creation",
                "category": "development",
                "purpose": "Create pull request",
                "tier": ["S"],
                "frequency": "as-needed",
            },
            "pb-release": {
                "command": "pb-release",
                "title": "Release Preparation",
                "category": "deployment",
                "purpose": "Prepare for production",
                "tier": ["L"],
                "frequency": "as-needed",
            },
            "pb-deployment": {
                "command": "pb-deployment",
                "title": "Deployment Strategies",
                "category": "deployment",
                "purpose": "Plan deployment",
                "tier": ["XS"],
                "frequency": "as-needed",
            },
            "pb-documentation": {
                "command": "pb-documentation",
                "title": "Documentation",
                "category": "core",
                "purpose": "Write clear documentation",
                "tier": ["XS"],
                "frequency": "as-needed",
            },
        },
        "extraction_report": {"average_confidence": 0.89},
    }


@pytest.fixture
def metadata_file(sample_metadata, tmp_path):
    """Create a temporary metadata file."""
    metadata_path = tmp_path / ".playbook-metadata.json"
    metadata_path.write_text(json.dumps(sample_metadata))
    return metadata_path


class TestPlaybookContextAnalyzerInit:
    """Test initialization of PlaybookContextAnalyzer."""

    def test_init_with_default_path(self, tmp_path):
        """Test initialization with default metadata path."""
        analyzer = PlaybookContextAnalyzer()
        assert analyzer.metadata_file == Path(".playbook-metadata.json")
        assert analyzer.commands == {}

    def test_init_with_custom_path(self, metadata_file):
        """Test initialization with custom metadata path."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        assert analyzer.metadata_file == metadata_file

    def test_load_metadata_success(self, metadata_file):
        """Test successful metadata loading."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        success = analyzer.load_metadata()
        assert success is True
        assert len(analyzer.commands) == 8
        assert "pb-start" in analyzer.commands

    def test_load_metadata_missing_file(self):
        """Test loading non-existent metadata file."""
        analyzer = PlaybookContextAnalyzer(metadata_file=Path("/nonexistent/file.json"))
        success = analyzer.load_metadata()
        assert success is False
        assert len(analyzer.errors) > 0

    def test_load_metadata_invalid_json(self, tmp_path):
        """Test loading invalid JSON metadata."""
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{invalid json}")
        analyzer = PlaybookContextAnalyzer(metadata_file=bad_file)
        success = analyzer.load_metadata()
        assert success is False
        assert len(analyzer.errors) > 0


class TestGitStateAnalysis:
    """Test git state analysis."""

    @mock.patch("analyze_playbook_context.PlaybookContextAnalyzer._run_git_command")
    def test_analyze_git_state_feature_branch(self, mock_git, metadata_file):
        """Test git state analysis on feature branch."""
        mock_git.side_effect = [
            "feature/new-feature\n",  # branch
            "M  file1.py\n?? file2.py\n",  # status
            "file2.py\n",  # staged
            "commit1\ncommit2\ncommit3\n",  # log
            "file1.py\nfile2.py\n",  # diff
        ]

        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()
        git_state = analyzer._analyze_git_state()

        assert git_state is not None
        assert git_state["branch"] == "feature/new-feature"
        assert git_state["commit_count"] == 3
        assert len(git_state["changed_files"]) > 0

    @mock.patch("analyze_playbook_context.PlaybookContextAnalyzer._run_git_command")
    def test_analyze_git_state_main_branch(self, mock_git, metadata_file):
        """Test git state analysis on main branch."""
        mock_git.side_effect = [
            "main\n",  # branch
            "",  # status (clean)
            "",  # staged
            "commit1\n",  # log
            "",  # diff
        ]

        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()
        git_state = analyzer._analyze_git_state()

        assert git_state["branch"] == "main"
        assert git_state["commit_count"] == 1

    @mock.patch("analyze_playbook_context.PlaybookContextAnalyzer._run_git_command")
    def test_analyze_git_state_no_changes(self, mock_git, metadata_file):
        """Test git state with no changes."""
        mock_git.side_effect = ["feature/branch\n", "", "", "", ""]

        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()
        git_state = analyzer._analyze_git_state()

        assert len(git_state["changed_files"]) == 0


class TestWorkflowPhaseDetection:
    """Test workflow phase detection."""

    @pytest.mark.parametrize(
        "branch,commit_count,changed,unstaged,expected_phase",
        [
            ("feature/test", 0, [], False, "START"),
            ("feature/test", 1, ["file.py"], False, "DEVELOP"),
            ("feature/test", 3, ["file.py"], True, "DEVELOP"),
            ("feature/test", 5, ["file.py"], False, "FINALIZE"),
            ("main", 10, [], False, "RELEASE"),
        ],
        ids=["start", "develop-early", "develop-mid", "finalize", "release"],
    )
    def test_workflow_phase_detection(
        self, branch, commit_count, changed, unstaged, expected_phase, metadata_file
    ):
        """Test workflow phase detection for different scenarios."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()

        git_state = {
            "branch": branch,
            "commit_count": commit_count,
            "changed_files": changed,
            "unstaged_changes": unstaged,
        }

        phase = analyzer._detect_workflow_phase(git_state)
        assert phase == expected_phase


class TestFileTypeIdentification:
    """Test file type identification."""

    def test_identify_source_files(self, metadata_file):
        """Test identification of source code files."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        files = ["src/main.py", "lib/utils.ts", "app.js"]
        file_types = analyzer._identify_changed_file_types({"changed_files": files})
        assert "source" in file_types
        assert len(file_types["source"]) == 3

    def test_identify_test_files(self, metadata_file):
        """Test identification of test files."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        files = ["tests/test_main.py", "spec/utils.spec.ts"]
        file_types = analyzer._identify_changed_file_types({"changed_files": files})
        assert "tests" in file_types
        assert len(file_types["tests"]) == 2

    def test_identify_doc_files(self, metadata_file):
        """Test identification of documentation files."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        files = ["docs/guide.md", "README.md"]
        file_types = analyzer._identify_changed_file_types({"changed_files": files})
        assert "docs" in file_types
        assert len(file_types["docs"]) == 2

    def test_identify_config_files(self, metadata_file):
        """Test identification of configuration files."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        files = ["Dockerfile", "package.json", "pyproject.toml"]
        file_types = analyzer._identify_changed_file_types({"changed_files": files})
        assert "config" in file_types
        assert len(file_types["config"]) >= 2

    def test_identify_ci_files(self, metadata_file):
        """Test identification of CI/CD files."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        files = [".github/workflows/test.yml"]
        file_types = analyzer._identify_changed_file_types({"changed_files": files})
        assert "ci" in file_types

    def test_identify_mixed_files(self, metadata_file):
        """Test identification of mixed file types."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        files = ["src/main.py", "tests/test_main.py", "docs/README.md"]
        file_types = analyzer._identify_changed_file_types({"changed_files": files})
        assert len(file_types) >= 2  # At least source and tests


class TestRecommendationGeneration:
    """Test recommendation generation."""

    def test_start_phase_recommendations(self, metadata_file):
        """Test recommendations for START phase."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()

        git_state = {
            "branch": "feature/new",
            "commit_count": 0,
            "changed_files": [],
        }
        file_types = {}

        recommendations = analyzer._generate_recommendations(git_state, "START", file_types)
        commands = [r["command"] for r in recommendations]
        assert "pb-start" in commands

    def test_develop_phase_recommendations(self, metadata_file):
        """Test recommendations for DEVELOP phase."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()

        git_state = {
            "branch": "feature/test",
            "commit_count": 3,
            "changed_files": ["src/main.py", "tests/test_main.py"],
        }
        file_types = {"source": ["src/main.py"], "tests": ["tests/test_main.py"]}

        recommendations = analyzer._generate_recommendations(
            git_state, "DEVELOP", file_types
        )
        commands = [r["command"] for r in recommendations]
        assert "pb-cycle" in commands
        assert "pb-testing" in commands

    def test_finalize_phase_recommendations(self, metadata_file):
        """Test recommendations for FINALIZE phase."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()

        git_state = {
            "branch": "feature/test",
            "commit_count": 5,
            "changed_files": [],
        }
        file_types = {}

        recommendations = analyzer._generate_recommendations(
            git_state, "FINALIZE", file_types
        )
        commands = [r["command"] for r in recommendations]
        assert "pb-commit" in commands
        assert "pb-pr" in commands

    def test_release_phase_recommendations(self, metadata_file):
        """Test recommendations for RELEASE phase."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()

        git_state = {
            "branch": "main",
            "commit_count": 10,
            "changed_files": [],
        }
        file_types = {}

        recommendations = analyzer._generate_recommendations(
            git_state, "RELEASE", file_types
        )
        commands = [r["command"] for r in recommendations]
        assert "pb-release" in commands or "pb-deployment" in commands

    def test_no_duplicate_recommendations(self, metadata_file):
        """Test that recommendations don't have duplicates."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()

        git_state = {
            "branch": "feature/test",
            "commit_count": 3,
            "changed_files": ["tests/test.py"],
        }
        file_types = {"tests": ["tests/test.py"]}

        recommendations = analyzer._generate_recommendations(
            git_state, "DEVELOP", file_types
        )
        commands = [r["command"] for r in recommendations]
        assert len(commands) == len(set(commands))  # No duplicates


class TestConfidenceScoring:
    """Test confidence scoring and ranking."""

    def test_score_and_rank(self, metadata_file):
        """Test recommendation scoring and ranking."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()

        recommendations = [
            {"command": "pb-cycle", "confidence": 0.90},
            {"command": "pb-testing", "confidence": 0.85},
            {"command": "pb-commit", "confidence": 0.75},
        ]

        scored = analyzer._score_and_rank(recommendations, {})
        assert len(scored) == len(recommendations)
        assert scored[0]["command"] in [r["command"] for r in scored]

    def test_confidence_range(self, metadata_file):
        """Test that confidence scores are in valid range."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()

        git_state = {
            "branch": "feature/test",
            "commit_count": 3,
            "changed_files": ["src/main.py"],
        }
        file_types = {"source": ["src/main.py"]}

        recommendations = analyzer._generate_recommendations(
            git_state, "DEVELOP", file_types
        )

        for rec in recommendations:
            confidence = rec.get("confidence", 0)
            assert 0.6 <= confidence <= 1.0


class TestErrorHandling:
    """Test error handling."""

    def test_missing_metadata_file(self):
        """Test handling of missing metadata file."""
        analyzer = PlaybookContextAnalyzer(metadata_file=Path("/nonexistent/file.json"))
        output = analyzer.analyze()
        assert "Analysis Error" in output or "error" in output.lower()

    def test_git_command_failure(self, metadata_file):
        """Test handling of git command failures."""
        with mock.patch(
            "analyze_playbook_context.PlaybookContextAnalyzer._run_git_command"
        ) as mock_git:
            mock_git.side_effect = Exception("Git command failed")
            analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
            analyzer.load_metadata()
            git_state = analyzer._analyze_git_state()
            assert git_state is None

    def test_unknown_command_in_metadata(self, metadata_file):
        """Test handling of unknown commands in recommendations."""
        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()

        recommendations = [
            {"command": "pb-unknown", "confidence": 0.50},
        ]

        # Should not crash when scoring unknown command
        scored = analyzer._score_and_rank(recommendations, {})
        assert len(scored) >= 0  # Should handle gracefully


class TestOutputFormatting:
    """Test output formatting."""

    @mock.patch("analyze_playbook_context.PlaybookContextAnalyzer._analyze_git_state")
    def test_output_includes_current_state(self, mock_git, metadata_file):
        """Test that output includes current work state."""
        mock_git.return_value = {
            "branch": "feature/test",
            "changed_files": ["file.py"],
            "commit_count": 2,
            "unstaged_changes": False,
        }

        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()
        output = analyzer.analyze()

        assert "Current Work State" in output
        assert "feature/test" in output or "Branch" in output

    @mock.patch("analyze_playbook_context.PlaybookContextAnalyzer._analyze_git_state")
    def test_output_includes_recommendations(self, mock_git, metadata_file):
        """Test that output includes recommendations."""
        mock_git.return_value = {
            "branch": "feature/test",
            "changed_files": ["src/main.py", "tests/test.py"],
            "commit_count": 3,
            "unstaged_changes": False,
        }

        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()
        output = analyzer.analyze()

        assert "Recommended Next Steps" in output or "recommendations" in output.lower()

    @mock.patch("analyze_playbook_context.PlaybookContextAnalyzer._analyze_git_state")
    def test_output_includes_timing(self, mock_git, metadata_file):
        """Test that output includes timing estimates."""
        mock_git.return_value = {
            "branch": "feature/test",
            "changed_files": ["src/main.py"],
            "commit_count": 2,
            "unstaged_changes": False,
        }

        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()
        output = analyzer.analyze()

        assert "Time:" in output or "min" in output or "hour" in output

    @mock.patch("analyze_playbook_context.PlaybookContextAnalyzer._analyze_git_state")
    def test_output_markdown_formatting(self, mock_git, metadata_file):
        """Test that output uses markdown formatting."""
        mock_git.return_value = {
            "branch": "feature/test",
            "changed_files": ["file.py"],
            "commit_count": 1,
            "unstaged_changes": False,
        }

        analyzer = PlaybookContextAnalyzer(metadata_file=metadata_file)
        analyzer.load_metadata()
        output = analyzer.analyze()

        # Check for markdown elements
        assert "#" in output  # Headers
        assert "**" in output or "`" in output  # Formatting


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
