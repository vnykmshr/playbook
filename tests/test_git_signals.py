#!/usr/bin/env python3
"""
Tests for git-signals.py

Tests commit parsing, metrics extraction, and pain point detection.
Uses mocking to avoid real git calls.
"""

import json
import tempfile
from pathlib import Path
from unittest import mock

import pytest

# Import the analyzer class
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from git_signals import GitSignalsAnalyzer


@pytest.fixture
def temp_output_dir():
    """Create temporary output directory for test results."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_commits():
    """Mock git log output with sample commits."""
    return """abc1234
John Doe
john@example.com
2025-01-15
feat(commands): add new pb-example command
Initial implementation
---END---
def5678
Jane Smith
jane@example.com
2025-01-10
fix: resolve metadata validation issue
Fixed edge case in YAML parsing
---END---
ghi9012
John Doe
john@example.com
2025-01-05
Revert "feat: remove deprecated command"
This commit reverts a breaking change
---END---
jkl3456
Jane Smith
jane@example.com
2024-12-28
fix: handle null pointer in context analyzer
Added safety check for empty metadata
---END---
mno7890
John Doe
john@example.com
2024-12-20
hotfix: urgent performance regression
Critical fix for query timeout
---END---"""


@pytest.fixture
def mock_files():
    """Mock git show output (files per commit)."""
    return {
        'abc1234': 'commands/core/pb-example.md\ndocs/example.md\nREADME.md',
        'def5678': 'scripts/validate-conventions.py\ntests/test_validate.py',
        'ghi9012': 'commands/planning/pb-old-command.md',
        'jkl3456': 'scripts/analyze-playbook-context.py\ntests/test_analyze.py',
        'mno7890': 'commands/core/pb-core-command.md',
    }


@pytest.fixture
def mock_numstat():
    """Mock git log --numstat output."""
    return """10\t5\tcommands/core/pb-example.md
3\t1\tdocs/example.md
20\t15\tscripts/validate-conventions.py
5\t0\ttests/test_validate.py
10\t20\tscripts/analyze-playbook-context.py
2\t2\ttests/test_analyze.py
50\t30\tcommands/core/pb-core-command.md"""


@pytest.fixture
def mock_porcelain():
    """Mock git status --porcelain output."""
    return """M  commands/core/pb-example.md
?? .test-temp
"""


class TestGitSignalsAnalyzer:
    """Test suite for GitSignalsAnalyzer."""

    def test_initialization(self, temp_output_dir):
        """Test analyzer initialization."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)
        assert analyzer.output_dir == temp_output_dir
        assert analyzer.since == "1 year ago"
        assert analyzer.output_dir.exists()

    def test_initialization_with_custom_since(self, temp_output_dir):
        """Test initialization with custom time range."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir, since="3 months ago")
        assert analyzer.since == "3 months ago"

    def test_parse_commits_empty(self, temp_output_dir):
        """Test parsing with no commits."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)
        with mock.patch.object(analyzer, '_run_git_command', return_value=''):
            result = analyzer._parse_commits()
            assert result is True
            assert len(analyzer.commits) == 0

    def test_parse_commits_success(self, temp_output_dir, mock_commits):
        """Test successful commit parsing."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)
        with mock.patch.object(analyzer, '_run_git_command', return_value=mock_commits):
            result = analyzer._parse_commits()
            assert result is True
            assert len(analyzer.commits) == 5

            # Verify first commit
            first = analyzer.commits[0]
            assert first['hash'] == 'abc1234'
            assert first['author'] == 'John Doe'
            assert first['email'] == 'john@example.com'
            assert 'feat(commands):' in first['subject']

    def test_parse_commits_handles_error(self, temp_output_dir):
        """Test error handling in commit parsing."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)
        with mock.patch.object(analyzer, '_run_git_command', side_effect=Exception("git failed")):
            result = analyzer._parse_commits()
            assert result is False

    def test_extract_adoption_metrics(self, temp_output_dir, mock_commits):
        """Test extraction of adoption metrics."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)

        # Mock parse_commits
        with mock.patch.object(analyzer, '_run_git_command') as mock_run:
            mock_run.side_effect = [mock_commits, 'commands/core/pb-example.md\ncommands/core/pb-core-command.md\ncommands/core/pb-example.md']

            analyzer._parse_commits()

            # Mock _get_commit_files
            with mock.patch.object(analyzer, '_get_commit_files') as mock_files:
                mock_files.side_effect = [
                    ['commands/core/pb-example.md'],
                    ['commands/core/pb-example.md'],
                    ['commands/core/pb-old-command.md'],
                    ['commands/core/pb-core-command.md'],
                    ['commands/core/pb-core-command.md'],
                ]

                analyzer._extract_adoption_metrics()

                # Verify metrics were extracted
                assert 'commands_by_touch_frequency' in analyzer.adoption_metrics
                assert 'files_by_change_frequency' in analyzer.adoption_metrics

    def test_extract_churn_metrics(self, temp_output_dir, mock_numstat):
        """Test extraction of churn metrics."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)

        with mock.patch.object(analyzer, '_run_git_command', return_value=mock_numstat):
            analyzer._extract_churn_metrics()

            # Verify churn metrics
            assert 'files_by_commit_frequency' in analyzer.churn_analysis
            assert 'files_by_line_changes' in analyzer.churn_analysis
            assert 'high_churn_areas' in analyzer.churn_analysis

            # Verify high-churn area detected
            high_churn = analyzer.churn_analysis['high_churn_areas']
            assert len(high_churn) > 0
            assert high_churn[0]['line_changes'] >= high_churn[-1]['line_changes']

    def test_extract_pain_points(self, temp_output_dir, mock_commits):
        """Test extraction of pain point signals."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)

        with mock.patch.object(analyzer, '_run_git_command', return_value=mock_commits):
            analyzer._parse_commits()

            with mock.patch.object(analyzer, '_get_commit_files', return_value=['commands/core/test.md']):
                analyzer._extract_pain_points()

                # Verify pain points extracted
                assert 'reverted_commits' in analyzer.pain_points
                assert 'bug_fix_patterns' in analyzer.pain_points
                assert 'hotfix_patterns' in analyzer.pain_points
                assert 'summary' in analyzer.pain_points

                # Verify counts
                summary = analyzer.pain_points['summary']
                assert summary['total_reverts'] >= 1  # We have a revert
                assert summary['total_bug_fixes'] >= 2  # We have bug fixes
                assert summary['total_hotfixes'] >= 1  # We have a hotfix

    def test_pain_point_detection_accuracy(self, temp_output_dir):
        """Test accuracy of pain point pattern detection."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)

        # Create test commits with known patterns
        test_commits = [
            {'subject': 'Revert "feat: add feature"', 'hash': 'abc123', 'date': '2025-01-01', 'author': 'test', 'body': '', 'email': 'test@test.com'},
            {'subject': 'fix: resolve bug', 'hash': 'def456', 'date': '2025-01-02', 'author': 'test', 'body': '', 'email': 'test@test.com'},
            {'subject': 'hotfix: critical issue', 'hash': 'ghi789', 'date': '2025-01-03', 'author': 'test', 'body': '', 'email': 'test@test.com'},
            {'subject': 'bugfix: null pointer', 'hash': 'jkl012', 'date': '2025-01-04', 'author': 'test', 'body': '', 'email': 'test@test.com'},
            {'subject': 'docs: update guide', 'hash': 'mno345', 'date': '2025-01-05', 'author': 'test', 'body': '', 'email': 'test@test.com'},
        ]

        analyzer.commits = test_commits

        with mock.patch.object(analyzer, '_get_commit_files', return_value=['test.md']):
            analyzer._extract_pain_points()

            summary = analyzer.pain_points['summary']
            assert summary['total_reverts'] == 1
            assert summary['total_bug_fixes'] >= 2  # 'fix:' + 'bugfix:'
            assert summary['total_hotfixes'] >= 1

    def test_write_outputs(self, temp_output_dir):
        """Test writing outputs to files."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)
        analyzer.adoption_metrics = {'test': 'data'}
        analyzer.churn_analysis = {'test': 'churn'}
        analyzer.pain_points = {'test': 'pain'}

        analyzer._write_outputs()

        # Verify files created
        assert (temp_output_dir / 'adoption-metrics.json').exists()
        assert (temp_output_dir / 'churn-analysis.json').exists()
        assert (temp_output_dir / 'pain-points-report.json').exists()
        assert (temp_output_dir / 'signals-summary.md').exists()

    def test_write_outputs_creates_valid_json(self, temp_output_dir):
        """Test that output JSON files are valid."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)
        analyzer.adoption_metrics = {'commands': [{'name': 'pb-test', 'count': 5}]}
        analyzer.churn_analysis = {'files': [{'name': 'test.md', 'changes': 10}]}
        analyzer.pain_points = {'issues': [{'type': 'revert', 'count': 2}]}

        analyzer._write_outputs()

        # Verify JSON is valid and matches what we wrote
        with open(temp_output_dir / 'adoption-metrics.json') as f:
            data = json.load(f)
            assert 'commands' in data
            assert data['commands'][0]['name'] == 'pb-test'

        with open(temp_output_dir / 'churn-analysis.json') as f:
            data = json.load(f)
            assert 'files' in data

    def test_run_git_command_success(self, temp_output_dir):
        """Test successful git command execution."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)
        with mock.patch('subprocess.run') as mock_run:
            mock_run.return_value = mock.Mock(stdout='output', returncode=0)
            result = analyzer._run_git_command('git log')
            assert result == 'output'

    def test_run_git_command_timeout(self, temp_output_dir):
        """Test git command timeout handling."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)
        with mock.patch('subprocess.run', side_effect=TimeoutExpired('git log', 10)):
            result = analyzer._run_git_command('git log')
            assert result == ""

    def test_run_git_command_error(self, temp_output_dir):
        """Test git command error handling."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)
        with mock.patch('subprocess.run', side_effect=Exception("Command failed")):
            result = analyzer._run_git_command('git log')
            assert result == ""

    def test_analyze_full_pipeline(self, temp_output_dir, mock_commits, mock_numstat):
        """Test full analysis pipeline."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)

        with mock.patch.object(analyzer, '_run_git_command') as mock_run:
            # First call: parse_commits
            # Second call: adoption metrics files
            # Third call: churn metrics
            mock_run.side_effect = [
                mock_commits,  # parse_commits
                'commands/core/pb-test.md\ncommands/planning/pb-plan.md',  # adoption metrics
                mock_numstat,  # churn metrics
            ]

            with mock.patch.object(analyzer, '_get_commit_files', return_value=['test.md']):
                result = analyzer.analyze()

        assert result is True
        assert len(analyzer.commits) == 5
        assert 'commands_by_touch_frequency' in analyzer.adoption_metrics
        assert 'high_churn_areas' in analyzer.churn_analysis
        assert 'pain_score_by_file' in analyzer.pain_points

        # Verify output files created
        assert (temp_output_dir / 'adoption-metrics.json').exists()
        assert (temp_output_dir / 'churn-analysis.json').exists()
        assert (temp_output_dir / 'pain-points-report.json').exists()
        assert (temp_output_dir / 'signals-summary.md').exists()


class TestCommitParsing:
    """Additional tests for commit parsing edge cases."""

    def test_parse_commits_with_multiline_body(self, temp_output_dir):
        """Test parsing commits with multi-line bodies."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)
        commits_with_body = """abc1234
John Doe
john@example.com
2025-01-15
feat: add new feature
This is a longer commit body
with multiple lines
of description
---END---"""

        with mock.patch.object(analyzer, '_run_git_command', return_value=commits_with_body):
            analyzer._parse_commits()
            assert len(analyzer.commits) == 1
            assert 'multiple lines' in analyzer.commits[0]['body']

    def test_parse_commits_with_special_characters(self, temp_output_dir):
        """Test parsing commits with special characters in subjects."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)
        commits_special = """abc1234
John Doe
john@example.com
2025-01-15
feat(utils): add "special" & <characters> handling
---END---"""

        with mock.patch.object(analyzer, '_run_git_command', return_value=commits_special):
            analyzer._parse_commits()
            assert len(analyzer.commits) == 1
            assert '"special"' in analyzer.commits[0]['subject']
            assert '<characters>' in analyzer.commits[0]['subject']


class TestMetricsExtraction:
    """Additional tests for metrics extraction edge cases."""

    def test_adoption_metrics_with_no_commands_dir(self, temp_output_dir):
        """Test adoption metrics extraction when no commands/ files present."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)

        with mock.patch.object(analyzer, '_run_git_command', return_value='docs/file.md\nREADME.md'):
            analyzer._extract_adoption_metrics()

            # Should handle gracefully with empty results
            assert 'commands_by_touch_frequency' in analyzer.adoption_metrics

    def test_churn_metrics_with_invalid_numstat(self, temp_output_dir):
        """Test churn metrics extraction with malformed numstat."""
        analyzer = GitSignalsAnalyzer(output_dir=temp_output_dir)

        invalid_numstat = """-\t-\tfile.md
invalid line
10\tfile.md"""  # Missing column

        with mock.patch.object(analyzer, '_run_git_command', return_value=invalid_numstat):
            analyzer._extract_churn_metrics()

            # Should handle gracefully
            assert 'high_churn_areas' in analyzer.churn_analysis
