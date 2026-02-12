#!/usr/bin/env python3
"""
Git History Signal Analyzer

Extracts adoption, churn, and pain point signals from git history to inform
quarterly evolution planning and ad-hoc investigation.

Usage:
    python scripts/git-signals.py
    python scripts/git-signals.py --since "3 months ago"
    python scripts/git-signals.py --output todos/git-signals/
    python scripts/git-signals.py --snapshot 2026-02-12
"""

import argparse
import json
import logging
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter

from playbook_utils import setup_logger


class GitSignalsAnalyzer:
    """Analyze git history for adoption, churn, and pain point signals."""

    def __init__(self, output_dir: Path = None, since: str = None, verbose: bool = False):
        """Initialize analyzer."""
        self.output_dir = output_dir or Path("todos/git-signals/latest")
        self.since = since or "1 year ago"
        self.logger = setup_logger("git-signals", verbose)

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Storage for analysis results
        self.commits: List[Dict[str, Any]] = []
        self.adoption_metrics: Dict[str, Any] = {}
        self.churn_analysis: Dict[str, Any] = {}
        self.pain_points: Dict[str, Any] = {}

    def analyze(self) -> bool:
        """Main analysis pipeline: parse -> extract metrics -> generate reports."""
        try:
            self.logger.info(f"Analyzing git history since: {self.since}")

            # Parse git log
            if not self._parse_commits():
                return False

            # Extract metrics
            self._extract_adoption_metrics()
            self._extract_churn_metrics()
            self._extract_pain_points()

            # Write outputs
            self._write_outputs()

            self.logger.info("Analysis complete")
            return True
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            return False

    def _parse_commits(self) -> bool:
        """Parse git log and extract commit metadata."""
        try:
            # Get full git log with all info we need
            command = (
                f'git log --format="%H|%an|%ae|%ad|%s|%b" '
                f'--date=short --since="{self.since}"'
            )
            output = self._run_git_command(command)

            if not output:
                self.logger.warning("No commits found in specified time range")
                return True  # Not an error, just empty result

            # Parse each commit
            # Note: We split on commit delimiter and parse carefully since body can have pipes
            commits_raw = self._run_git_command(
                f'git log --format="%H%n%an%n%ae%n%ad%n%s%n---END---" '
                f'--date=short --since="{self.since}"'
            )

            if not commits_raw:
                return True

            # Parse structured format
            current_commit = {}
            lines = commits_raw.split('\n')
            i = 0

            while i < len(lines):
                line = lines[i]

                if not line.strip():
                    i += 1
                    continue

                # Start of new commit (hash)
                if len(line) == 40 and all(c in '0123456789abcdef' for c in line):
                    if current_commit:
                        self.commits.append(current_commit)
                    current_commit = {
                        'hash': line,
                        'author': '',
                        'email': '',
                        'date': '',
                        'subject': '',
                        'body': '',
                    }
                elif current_commit:
                    # Fill in fields in order
                    if 'author' in current_commit and not current_commit['author']:
                        current_commit['author'] = line
                    elif 'email' in current_commit and not current_commit['email']:
                        current_commit['email'] = line
                    elif 'date' in current_commit and not current_commit['date']:
                        current_commit['date'] = line
                    elif 'subject' in current_commit and not current_commit['subject']:
                        current_commit['subject'] = line
                    elif line == '---END---':
                        # End of this commit
                        pass
                    else:
                        # Body content
                        if current_commit['body']:
                            current_commit['body'] += '\n' + line
                        else:
                            current_commit['body'] = line

                i += 1

            # Add last commit if exists
            if current_commit and current_commit.get('hash'):
                self.commits.append(current_commit)

            self.logger.info(f"Parsed {len(self.commits)} commits")
            return True

        except Exception as e:
            self.logger.error(f"Error parsing commits: {e}")
            return False

    def _extract_adoption_metrics(self) -> None:
        """Extract which files/commands are most touched."""
        try:
            # Get file changes by running git log with name-only
            command = f'git log --name-only --pretty="" --since="{self.since}"'
            output = self._run_git_command(command)

            if not output:
                self.adoption_metrics = {'commands_by_touch_frequency': [], 'files_by_change_frequency': []}
                return

            files = [f.strip() for f in output.split('\n') if f.strip() and f.startswith('commands/')]

            # Count file touches
            file_counts = Counter(files)

            # Extract commands from file paths
            command_counts = defaultdict(int)
            for file_path, count in file_counts.items():
                # Pattern: commands/category/pb-command-name.md
                match = re.match(r'commands/[^/]+/(pb-[^/]+)', file_path)
                if match:
                    cmd = match.group(1).replace('.md', '')
                    command_counts[cmd] += count

            # Count unique authors per command
            author_counts = defaultdict(set)
            for commit in self.commits:
                for file_path in self._get_commit_files(commit['hash']):
                    if file_path.startswith('commands/'):
                        match = re.match(r'commands/[^/]+/(pb-[^/]+)', file_path)
                        if match:
                            cmd = match.group(1).replace('.md', '')
                            author_counts[cmd].add(commit['author'])

            # Compile metrics
            self.adoption_metrics = {
                'commands_by_touch_frequency': sorted(
                    [{'command': cmd, 'touches': count}
                     for cmd, count in command_counts.items()],
                    key=lambda x: x['touches'],
                    reverse=True
                )[:20],  # Top 20
                'files_by_change_frequency': sorted(
                    [{'file': file, 'changes': count}
                     for file, count in file_counts.items()],
                    key=lambda x: x['changes'],
                    reverse=True
                )[:20],  # Top 20
                'authors_per_command': {
                    cmd: len(authors)
                    for cmd, authors in author_counts.items()
                },
                'least_active_commands': sorted(
                    [{'command': cmd, 'touches': count}
                     for cmd, count in command_counts.items()],
                    key=lambda x: x['touches']
                )[:10],  # Bottom 10 (candidates for review)
            }

            self.logger.info(f"Extracted adoption metrics for {len(command_counts)} commands")

        except Exception as e:
            self.logger.error(f"Error extracting adoption metrics: {e}")
            self.adoption_metrics = {'commands_by_touch_frequency': [], 'files_by_change_frequency': []}

    def _extract_churn_metrics(self) -> None:
        """Extract files with high change frequency (churn)."""
        try:
            # Get line changes using numstat
            command = f'git log --numstat --pretty="" --since="{self.since}"'
            output = self._run_git_command(command)

            if not output:
                self.churn_analysis = {'files_by_commit_frequency': [], 'files_by_line_changes': []}
                return

            # Parse numstat output (added\tdeleted\tfile)
            file_commits = defaultdict(int)
            file_changes = defaultdict(int)

            for line in output.split('\n'):
                line = line.strip()
                if not line or line == '-':
                    continue

                parts = line.split('\t')
                if len(parts) >= 3:
                    try:
                        added = int(parts[0]) if parts[0] != '-' else 0
                        deleted = int(parts[1]) if parts[1] != '-' else 0
                        file_path = parts[2]

                        if file_path and (added > 0 or deleted > 0):
                            file_commits[file_path] += 1
                            file_changes[file_path] += (added + deleted)
                    except (ValueError, IndexError):
                        continue

            # Identify high-churn areas
            high_churn = []
            for file_path, line_changes in sorted(
                file_changes.items(),
                key=lambda x: x[1],
                reverse=True
            )[:20]:
                high_churn.append({
                    'file': file_path,
                    'line_changes': line_changes,
                    'commits': file_commits[file_path],
                    'avg_change_per_commit': line_changes // file_commits[file_path] if file_commits[file_path] > 0 else 0,
                })

            self.churn_analysis = {
                'files_by_commit_frequency': sorted(
                    [{'file': file, 'commits': count}
                     for file, count in file_commits.items()],
                    key=lambda x: x['commits'],
                    reverse=True
                )[:20],
                'files_by_line_changes': sorted(
                    [{'file': file, 'line_changes': count}
                     for file, count in file_changes.items()],
                    key=lambda x: x['line_changes'],
                    reverse=True
                )[:20],
                'high_churn_areas': high_churn,
            }

            self.logger.info(f"Extracted churn metrics: {len(file_commits)} files analyzed")

        except Exception as e:
            self.logger.error(f"Error extracting churn metrics: {e}")
            self.churn_analysis = {'files_by_commit_frequency': [], 'files_by_line_changes': []}

    def _extract_pain_points(self) -> None:
        """Extract pain point signals from commit patterns."""
        try:
            reverts = []
            bug_fixes = []
            hotfixes = []

            for commit in self.commits:
                subject = commit.get('subject', '').lower()

                # Revert detection
                if 'revert' in subject:
                    reverts.append({
                        'hash': commit['hash'],
                        'subject': commit['subject'],
                        'date': commit['date'],
                        'author': commit['author'],
                    })

                # Bug fix detection
                if any(pattern in subject for pattern in ['fix:', 'bug:', 'fix bug', 'bugfix']):
                    bug_fixes.append({
                        'hash': commit['hash'],
                        'subject': commit['subject'],
                        'date': commit['date'],
                    })

                # Hotfix detection
                if any(pattern in subject for pattern in ['hotfix', 'urgent', 'critical', 'p0:', 'p1:']):
                    hotfixes.append({
                        'hash': commit['hash'],
                        'subject': commit['subject'],
                        'date': commit['date'],
                    })

            # Calculate pain score by file (frequency of fixes in specific areas)
            pain_by_file = defaultdict(int)
            for commit in self.commits:
                files = self._get_commit_files(commit['hash'])
                subject = commit['subject'].lower()

                # Increase pain score for files touched by fixes/reverts
                if any(p in subject for p in ['fix:', 'revert', 'bug:', 'hotfix']):
                    for file_path in files:
                        pain_by_file[file_path] += 1

            self.pain_points = {
                'reverted_commits': reverts[-10:],  # Last 10 reverts
                'bug_fix_patterns': bug_fixes[-10:],  # Last 10 bug fixes
                'hotfix_patterns': hotfixes[-10:],  # Last 10 hotfixes
                'pain_score_by_file': sorted(
                    [{'file': file, 'pain_score': score}
                     for file, score in pain_by_file.items()],
                    key=lambda x: x['pain_score'],
                    reverse=True
                )[:15],
                'summary': {
                    'total_reverts': len(reverts),
                    'total_bug_fixes': len(bug_fixes),
                    'total_hotfixes': len(hotfixes),
                }
            }

            self.logger.info(
                f"Extracted pain points: {len(reverts)} reverts, "
                f"{len(bug_fixes)} bug fixes, {len(hotfixes)} hotfixes"
            )

        except Exception as e:
            self.logger.error(f"Error extracting pain points: {e}")
            self.pain_points = {
                'reverted_commits': [],
                'bug_fix_patterns': [],
                'hotfix_patterns': [],
                'pain_score_by_file': [],
                'summary': {'total_reverts': 0, 'total_bug_fixes': 0, 'total_hotfixes': 0},
            }

    def _get_commit_files(self, commit_hash: str) -> List[str]:
        """Get list of files changed in a specific commit."""
        try:
            command = f'git show --name-only --pretty="" {commit_hash}'
            output = self._run_git_command(command)
            return [f.strip() for f in output.split('\n') if f.strip()]
        except Exception:
            return []

    def _run_git_command(self, command: str) -> str:
        """Run git command safely."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,  # Slightly longer for large history
            )
            return result.stdout
        except subprocess.TimeoutExpired:
            self.logger.warning(f"Git command timed out: {command}")
            return ""
        except Exception as e:
            self.logger.warning(f"Git command failed: {command} - {e}")
            return ""

    def _write_outputs(self) -> None:
        """Write analysis results to JSON and markdown files."""
        try:
            # Write adoption metrics
            adoption_file = self.output_dir / "adoption-metrics.json"
            with open(adoption_file, 'w') as f:
                json.dump(self.adoption_metrics, f, indent=2)
            self.logger.info(f"Wrote adoption metrics to {adoption_file}")

            # Write churn analysis
            churn_file = self.output_dir / "churn-analysis.json"
            with open(churn_file, 'w') as f:
                json.dump(self.churn_analysis, f, indent=2)
            self.logger.info(f"Wrote churn analysis to {churn_file}")

            # Write pain points
            pain_file = self.output_dir / "pain-points-report.json"
            with open(pain_file, 'w') as f:
                json.dump(self.pain_points, f, indent=2)
            self.logger.info(f"Wrote pain points to {pain_file}")

            # Write human-readable summary
            summary_file = self.output_dir / "signals-summary.md"
            self._write_summary_markdown(summary_file)
            self.logger.info(f"Wrote summary to {summary_file}")

        except Exception as e:
            self.logger.error(f"Error writing outputs: {e}")

    def _write_summary_markdown(self, filepath: Path) -> None:
        """Write human-readable markdown summary of signals."""
        summary = []
        summary.append("# Git Signals Summary\n")
        summary.append(f"**Generated:** {datetime.now().isoformat()}\n")
        summary.append(f"**Time period:** Since {self.since}\n")
        summary.append(f"**Commits analyzed:** {len(self.commits)}\n\n")

        # Adoption section
        summary.append("## Adoption Metrics\n")
        if self.adoption_metrics.get('commands_by_touch_frequency'):
            summary.append("**Most active commands:**\n")
            for item in self.adoption_metrics['commands_by_touch_frequency'][:5]:
                summary.append(f"- `{item['command']}`: {item['touches']} touches\n")

        if self.adoption_metrics.get('least_active_commands'):
            summary.append("\n**Least active commands (candidates for review):**\n")
            for item in self.adoption_metrics['least_active_commands'][:5]:
                summary.append(f"- `{item['command']}`: {item['touches']} touches\n")

        # Churn section
        summary.append("\n## High-Churn Areas\n")
        if self.adoption_metrics.get('high_churn_areas'):
            summary.append("**Files with most changes:**\n")
            for item in self.churn_analysis.get('high_churn_areas', [])[:5]:
                summary.append(
                    f"- `{item['file']}`: {item['line_changes']} lines "
                    f"across {item['commits']} commits\n"
                )

        # Pain points section
        summary.append("\n## Pain Point Signals\n")
        pain_summary = self.pain_points.get('summary', {})
        summary.append(f"- Reverts: {pain_summary.get('total_reverts', 0)}\n")
        summary.append(f"- Bug fixes: {pain_summary.get('total_bug_fixes', 0)}\n")
        summary.append(f"- Hotfixes: {pain_summary.get('total_hotfixes', 0)}\n")

        if self.pain_points.get('pain_score_by_file'):
            summary.append("\n**Top pain areas (most fixed):**\n")
            for item in self.pain_points['pain_score_by_file'][:5]:
                summary.append(f"- `{item['file']}`: pain score {item['pain_score']}\n")

        summary.append("\n---\n")
        summary.append("See JSON files for detailed data.\n")

        with open(filepath, 'w') as f:
            f.writelines(summary)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Extract git history signals for evolution planning"
    )
    parser.add_argument(
        "--since",
        type=str,
        default="1 year ago",
        help="Git time range (default: 1 year ago)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("todos/git-signals/latest"),
        help="Output directory for results",
    )
    parser.add_argument(
        "--snapshot",
        type=str,
        help="Create snapshot with this date (YYYY-MM-DD format)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose logging",
    )

    args = parser.parse_args()

    # Run analysis
    analyzer = GitSignalsAnalyzer(
        output_dir=args.output,
        since=args.since,
        verbose=args.verbose,
    )

    success = analyzer.analyze()

    # Create snapshot if requested
    if success and args.snapshot:
        try:
            snapshot_dir = Path(f"todos/git-signals/{args.snapshot}")
            snapshot_dir.mkdir(parents=True, exist_ok=True)

            # Copy outputs to snapshot directory
            import shutil
            for file in ["adoption-metrics.json", "churn-analysis.json", "pain-points-report.json"]:
                src = args.output / file
                dst = snapshot_dir / file
                if src.exists():
                    shutil.copy2(src, dst)

            print(f"Snapshot created at {snapshot_dir}")
        except Exception as e:
            print(f"Error creating snapshot: {e}", file=sys.stderr)
            sys.exit(1)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
