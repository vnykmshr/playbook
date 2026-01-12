#!/usr/bin/env python3
"""
Playbook Context Analyzer

Analyzes user's current situation (git state, file changes) and recommends
next playbook commands to run, in order, with time estimates and reasoning.

Usage:
    python scripts/analyze-playbook-context.py
    python scripts/analyze-playbook-context.py --verbose
    python scripts/analyze-playbook-context.py --metadata custom.json
"""

import argparse
import json
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import re


class PlaybookContextAnalyzer:
    """Analyze user context and recommend playbook commands."""

    def __init__(self, metadata_file: Path = None, verbose: bool = False):
        """Initialize analyzer."""
        self.metadata_file = metadata_file or Path(".playbook-metadata.json")
        self.logger = self._setup_logging(verbose)
        self.metadata = {}
        self.commands = {}
        self.recommendations: List[Dict[str, Any]] = []
        self.warnings: List[str] = []
        self.errors: List[str] = []

    def _setup_logging(self, verbose: bool) -> logging.Logger:
        """Setup logging."""
        logger = logging.getLogger("context-analyzer")
        logger.setLevel(logging.DEBUG if verbose else logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def analyze(self) -> str:
        """Main analysis pipeline: load -> analyze -> recommend -> format."""
        # Load metadata
        if not self.load_metadata():
            return self._format_error_state()

        # Analyze git state
        git_state = self._analyze_git_state()
        if not git_state:
            return self._format_error_state()

        # Detect workflow phase
        phase = self._detect_workflow_phase(git_state)

        # Identify changed file types
        file_types = self._identify_changed_file_types(git_state)

        # Generate and score recommendations
        recommendations = self._generate_recommendations(git_state, phase, file_types)
        self.recommendations = self._score_and_rank(recommendations, git_state)

        # Format and return output
        return self._format_output(git_state, phase, file_types)

    def load_metadata(self) -> bool:
        """Load extracted metadata from JSON file."""
        if not self.metadata_file.exists():
            self.errors.append(f"Metadata file not found: {self.metadata_file}")
            self.logger.error(f"Metadata file not found: {self.metadata_file}")
            return False

        try:
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
            self.commands = self.metadata.get("commands", {})
            self.logger.info(f"Loaded metadata for {len(self.commands)} commands")
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in metadata file: {e}")
            self.logger.error(f"Invalid JSON in metadata file: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Error loading metadata: {e}")
            self.logger.error(f"Error loading metadata: {e}")
            return False

    def _analyze_git_state(self) -> Optional[Dict[str, Any]]:
        """Analyze current git state."""
        try:
            # Get current branch
            branch = self._run_git_command("git branch --show-current").strip()
            if not branch:
                branch = "main"

            # Get changed files
            unstaged = self._run_git_command("git status --porcelain").strip()
            staged = self._run_git_command("git diff --cached --name-only").strip()
            changed_files_unstaged = [line.split(maxsplit=1)[1] for line in unstaged.split("\n") if line.strip()]
            changed_files_staged = staged.split("\n") if staged else []
            all_changed_files = list(set(changed_files_unstaged + changed_files_staged))

            # Get recent commits
            commits_output = self._run_git_command("git log --oneline -10").strip()
            commits = commits_output.split("\n") if commits_output else []
            commit_count = len([c for c in commits if c.strip()])

            # Get file diffs
            diff_files = self._run_git_command("git diff --name-only").strip()
            diff_files_list = [f for f in diff_files.split("\n") if f.strip()] if diff_files else []

            return {
                "branch": branch,
                "changed_files": all_changed_files,
                "unstaged_changes": len(changed_files_unstaged) > 0,
                "staged_changes": len(changed_files_staged) > 0,
                "commit_count": commit_count,
                "recent_commits": commits[:5],
                "diff_files": diff_files_list,
            }
        except Exception as e:
            self.errors.append(f"Error analyzing git state: {e}")
            self.logger.error(f"Error analyzing git state: {e}")
            return None

    def _run_git_command(self, command: str) -> str:
        """Run git command safely."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.stdout
        except subprocess.TimeoutExpired:
            self.logger.warning(f"Git command timed out: {command}")
            return ""
        except Exception as e:
            self.logger.warning(f"Git command failed: {command} - {e}")
            return ""

    def _detect_workflow_phase(self, git_state: Dict[str, Any]) -> str:
        """Detect current workflow phase based on git state."""
        branch = git_state.get("branch", "")
        commit_count = git_state.get("commit_count", 0)
        changed_files = git_state.get("changed_files", [])
        unstaged = git_state.get("unstaged_changes", False)
        staged = git_state.get("staged_changes", False)

        # On main branch
        if branch == "main" or branch == "master":
            return "RELEASE"

        # Feature/fix/refactor branch with no changes
        if commit_count == 0 and not unstaged and not staged:
            return "START"

        # Feature/fix/refactor with changes but < 5 commits
        if 0 < commit_count < 5 and (unstaged or staged or changed_files):
            return "DEVELOP"

        # 5+ commits or ready to finalize
        if commit_count >= 5 or (not unstaged and not staged and commit_count > 0):
            return "FINALIZE"

        # Default to develop
        return "DEVELOP"

    def _identify_changed_file_types(self, git_state: Dict[str, Any]) -> Dict[str, List[str]]:
        """Categorize changed files by type."""
        changed_files = git_state.get("changed_files", [])

        result = {
            "tests": [],
            "docs": [],
            "source": [],
            "config": [],
            "ci": [],
        }

        for file_path in changed_files:
            file_lower = file_path.lower()

            if "test" in file_lower or "spec" in file_lower:
                result["tests"].append(file_path)
            elif "docs/" in file_lower or ".md" in file_lower:
                result["docs"].append(file_path)
            elif ".github/workflows" in file_lower:
                result["ci"].append(file_path)
            elif any(
                file_path.endswith(ext)
                for ext in [".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs"]
            ):
                result["source"].append(file_path)
            elif any(
                file_path.endswith(name)
                for name in [
                    "Dockerfile",
                    "docker-compose.yml",
                    "package.json",
                    "pyproject.toml",
                    "setup.py",
                    "go.mod",
                ]
            ):
                result["config"].append(file_path)

        # Remove empty categories
        return {k: v for k, v in result.items() if v}

    def _generate_recommendations(
        self, git_state: Dict[str, Any], phase: str, file_types: Dict[str, List[str]]
    ) -> List[Dict[str, Any]]:
        """Generate command recommendations based on context."""
        recommendations = []

        # Phase-based recommendations
        if phase == "START":
            recommendations.extend(
                [
                    {
                        "command": "pb-start",
                        "reason": "Beginning feature work on new branch",
                        "confidence": 0.95,
                    },
                ]
            )
        elif phase == "DEVELOP":
            recommendations.extend(
                [
                    {
                        "command": "pb-cycle",
                        "reason": "Iterate on changes, get peer feedback",
                        "confidence": 0.90,
                    },
                    {
                        "command": "pb-testing",
                        "reason": "Verify test coverage matches code changes",
                        "confidence": 0.85,
                    },
                ]
            )
        elif phase == "FINALIZE":
            recommendations.extend(
                [
                    {
                        "command": "pb-commit",
                        "reason": "Organize work into logical commits",
                        "confidence": 0.90,
                    },
                    {
                        "command": "pb-pr",
                        "reason": "Create pull request for integration",
                        "confidence": 0.90,
                    },
                ]
            )
        elif phase == "REVIEW":
            recommendations.extend(
                [
                    {
                        "command": "pb-review-code",
                        "reason": "Review code logic and patterns",
                        "confidence": 0.95,
                    },
                    {
                        "command": "pb-review-tests",
                        "reason": "Verify test coverage and quality",
                        "confidence": 0.85,
                    },
                    {
                        "command": "pb-security",
                        "reason": "Check security implications",
                        "confidence": 0.75,
                    },
                ]
            )
        elif phase == "RELEASE":
            recommendations.extend(
                [
                    {
                        "command": "pb-release",
                        "reason": "Prepare for production release",
                        "confidence": 0.90,
                    },
                    {
                        "command": "pb-deployment",
                        "reason": "Plan deployment strategy",
                        "confidence": 0.80,
                    },
                ]
            )

        # File-type-based recommendations
        if file_types.get("tests"):
            if "pb-testing" not in [r["command"] for r in recommendations]:
                recommendations.append(
                    {
                        "command": "pb-testing",
                        "reason": "Test files changed, verify coverage",
                        "confidence": 0.88,
                    }
                )

        if file_types.get("docs"):
            recommendations.append(
                {
                    "command": "pb-documentation",
                    "reason": "Documentation changed, ensure clarity",
                    "confidence": 0.75,
                }
            )

        if file_types.get("ci"):
            recommendations.append(
                {
                    "command": "pb-deployment",
                    "reason": "CI/CD workflow modified",
                    "confidence": 0.70,
                }
            )

        # Deduplication: keep highest confidence for duplicate commands
        seen = {}
        for rec in recommendations:
            cmd = rec["command"]
            if cmd not in seen or rec["confidence"] > seen[cmd]["confidence"]:
                seen[cmd] = rec

        return list(seen.values())

    def _score_and_rank(
        self, recommendations: List[Dict[str, Any]], git_state: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Score and rank recommendations."""
        # Apply tier-based priority weighting
        for rec in recommendations:
            cmd = rec.get("command", "")
            if cmd in self.commands:
                meta = self.commands[cmd]
                tier = meta.get("tier")
                if isinstance(tier, list):
                    tier = tier[0] if tier else "M"

                # Tier-based priority: XS=5, S=4, M=3, L=2
                tier_priority = {"XS": 5, "S": 4, "M": 3, "L": 2}.get(tier, 3)
                rec["priority"] = tier_priority
            else:
                rec["priority"] = 3

        # Sort by priority (descending) then confidence (descending)
        recommendations.sort(
            key=lambda x: (x.get("priority", 3), x.get("confidence", 0.5)),
            reverse=True,
        )

        return recommendations

    def _format_output(
        self, git_state: Dict[str, Any], phase: str, file_types: Dict[str, List[str]]
    ) -> str:
        """Format output as markdown with recommendations."""
        lines = []

        # Current work state
        lines.append("# Current Work State")
        lines.append("━" * 50)
        lines.append("")
        lines.append(f"**Branch**: `{git_state.get('branch', 'unknown')}`")
        lines.append(f"**Phase**: {phase}")

        changed_count = len(git_state.get("changed_files", []))
        if changed_count > 0:
            file_type_summary = ", ".join(
                f"{k}/" for k in file_types.keys() if file_types[k]
            )
            lines.append(f"**Changes**: {changed_count} files changed ({file_type_summary})")
        else:
            lines.append("**Changes**: None (clean working directory)")

        commit_count = git_state.get("commit_count", 0)
        lines.append(f"**Commits**: {commit_count} recent commits")
        lines.append("")

        # Recommendations
        lines.append("# Recommended Next Steps")
        lines.append("━" * 50)
        lines.append("")

        if not self.recommendations:
            lines.append("No specific recommendations at this time.")
            lines.append("Status looks good for current phase!")
        else:
            for idx, rec in enumerate(self.recommendations, 1):
                cmd = rec.get("command", "")
                reason = rec.get("reason", "")
                confidence = rec.get("confidence", 0.5)

                # Get command title and timing if available
                cmd_meta = self.commands.get(cmd, {})
                title = cmd_meta.get("title", cmd)
                tier = cmd_meta.get("tier")
                if isinstance(tier, list):
                    tier = tier[0] if tier else "M"

                timing = self._get_tier_time(tier)

                lines.append(f"{idx}. **`/{cmd}`** — {title}")
                lines.append(f"   - {reason}")
                lines.append(f"   - Confidence: {confidence:.0%} | Time: {timing}")
                lines.append("")

        # Why these commands?
        if self.recommendations:
            lines.append("# Why These Commands?")
            lines.append("━" * 50)
            lines.append("")

            if file_types.get("tests") and file_types.get("source"):
                lines.append(
                    "• Both source and test files changed → Need full development cycle"
                )

            if commit_count >= 5:
                lines.append(
                    "• Multiple commits → Time to organize and prepare for integration"
                )

            if phase == "FINALIZE" and not git_state.get("unstaged_changes"):
                lines.append("• All changes committed → Ready to create PR")

            if file_types.get("docs"):
                lines.append("• Documentation updated → Ensure clarity and completeness")

            if file_types.get("ci"):
                lines.append("• CI/CD modified → Review deployment impacts")

            lines.append("")

        # Additional context
        lines.append("# Tips")
        lines.append("━" * 50)
        lines.append("")
        lines.append("- Run `/pb-what-next --verbose` for detailed analysis")
        lines.append("- Each command should take 5-60 minutes")
        lines.append("- Return here after each step for updated recommendations")
        lines.append("")

        return "\n".join(lines)

    def _get_tier_time(self, tier: Optional[str]) -> str:
        """Get estimated time for a tier."""
        if tier is None:
            return "varies"
        times = {"XS": "5 min", "S": "10 min", "M": "25 min", "L": "45 min"}
        return times.get(str(tier), "varies")

    def _format_error_state(self) -> str:
        """Format error state output."""
        lines = [
            "# Analysis Error",
            "━" * 50,
            "",
        ]

        if self.errors:
            lines.append("**Errors:**")
            for error in self.errors:
                lines.append(f"- {error}")
            lines.append("")

        lines.extend(
            [
                "**Troubleshooting:**",
                "- Ensure `.playbook-metadata.json` exists (run extraction first)",
                "- Ensure this is a git repository",
                "- Check that extraction was successful with 47+ commands",
                "",
                "**To regenerate metadata:**",
                "```bash",
                "python scripts/extract-playbook-metadata.py",
                "```",
            ]
        )

        return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze playbook context and recommend next commands"
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        default=Path(".playbook-metadata.json"),
        help="Path to metadata JSON file",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Analyze
    analyzer = PlaybookContextAnalyzer(metadata_file=args.metadata, verbose=args.verbose)
    output = analyzer.analyze()

    # Print output
    print(output)

    return 0 if not analyzer.errors else 1


if __name__ == "__main__":
    sys.exit(main())
