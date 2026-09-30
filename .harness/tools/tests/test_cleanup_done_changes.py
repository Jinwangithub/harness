#!/usr/bin/env python3
"""Tests for cleanup_done_changes.py."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

TOOL_PATH = Path(__file__).resolve().parents[1] / "cleanup_done_changes.py"
SPEC = importlib.util.spec_from_file_location("cleanup_done_changes", TOOL_PATH)
assert SPEC and SPEC.loader
cleanup_tool = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = cleanup_tool
SPEC.loader.exec_module(cleanup_tool)


VERIFICATION_REPORT = """# Verification Report

## Commands / Checks
- python3 -m unittest: 0

## Compressed Review
- Status: Approve
- Critical: 0
- Must Fix: 0
- Review Notes: none

## Verdict
- Status: pass

## Memory Check
- Memory recorded: none
"""


class CleanupDoneChangesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.changes = self.root / ".harness" / "changes"
        self.tools = self.root / ".harness" / "tools"
        self.changes.mkdir(parents=True)
        self.tools.mkdir(parents=True)
        validator_source = TOOL_PATH.with_name("validate_change.py").read_text(encoding="utf-8")
        (self.tools / "validate_change.py").write_text(validator_source, encoding="utf-8")
        self.entries: list[tuple[str, str, str]] = []

    def tearDown(self) -> None:
        self.temp.cleanup()

    def change_id(self, number: int) -> str:
        return f"feat-retention-{number}-20260805"

    def add_change(self, number: int, status: str = "done", resume: str = "none") -> str:
        change_id = self.change_id(number)
        self.entries.append((change_id, status, resume))
        directory = self.changes / change_id
        directory.mkdir()
        (directory / "request_analysis").mkdir()
        (directory / "request_analysis" / "checklist.md").write_text("# Checklist\n", encoding="utf-8")
        (directory / "verification_report.md").write_text(VERIFICATION_REPORT, encoding="utf-8")
        (directory / "summary.md").write_text(
            "\n".join(
                [
                    "# Summary",
                    "- **需求**: retention",
                    "- **类型**: feat",
                    "- **日期**: 20260805",
                    f"- **状态**: {status}",
                    "- **Flow**: Lite-flow",
                    "- **Current step**: L3",
                    f"- **Resume point**: {resume}",
                    "",
                    "## Gate Record — L3",
                    "- Mechanical Gate: pass",
                    "- Human Approval: approved",
                    "- Command: python3 -m unittest",
                    "- Exit code: 0",
                    "- Output summary: tests completed with no failures",
                    "- Artifact path: verification_report.md",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return change_id

    def write_index(self) -> None:
        rows = ["# Changes Index\n\n", "| Change | Status | Resume point | Notes |\n", "|--------|--------|--------------|-------|\n"]
        rows.extend(f"| `{change}` | `{status}` | {resume} | test |\n" for change, status, resume in self.entries)
        (self.changes / "INDEX.md").write_text("".join(rows), encoding="utf-8")

    def snapshot(self, change_id: str) -> tuple[bytes, tuple[str, ...]]:
        return ((self.changes / "INDEX.md").read_bytes(), tuple(sorted(path.relative_to(self.changes).as_posix() for path in (self.changes / change_id).rglob("*"))))

    def test_refuses_when_done_count_is_exactly_five(self) -> None:
        target = self.add_change(1)
        for number in range(2, 6):
            self.add_change(number)
        self.write_index()
        before = self.snapshot(target)
        with self.assertRaises(cleanup_tool.CleanupError):
            cleanup_tool.cleanup(self.root, target)
        self.assertEqual(before, self.snapshot(target))

    def test_only_oldest_done_is_eligible_among_mixed_statuses(self) -> None:
        active = self.add_change(1, "active", "L2")
        oldest = self.add_change(2)
        abandoned = self.add_change(3, "abandoned", "none")
        later = [self.add_change(number) for number in range(4, 9)]
        self.write_index()
        before = self.snapshot(later[0])
        with self.assertRaises(cleanup_tool.CleanupError):
            cleanup_tool.cleanup(self.root, later[0])
        self.assertTrue((self.changes / active).is_dir())
        self.assertTrue((self.changes / abandoned).is_dir())
        self.assertEqual(before, self.snapshot(later[0]))
        cleanup_tool.cleanup(self.root, oldest)
        self.assertFalse((self.changes / oldest).exists())

    def test_success_deletes_only_one_change_and_index_row(self) -> None:
        oldest = self.add_change(1)
        remaining = [self.add_change(number) for number in range(2, 8)]
        self.write_index()
        cleanup_tool.cleanup(self.root, oldest)
        index = (self.changes / "INDEX.md").read_text(encoding="utf-8")
        self.assertNotIn(oldest, index)
        self.assertFalse((self.changes / oldest).exists())
        self.assertTrue(all((self.changes / change).exists() for change in remaining))
        self.assertEqual(index.count("| `feat-retention-"), 6)

    def test_rejects_invalid_selection_and_preserves_bytes(self) -> None:
        oldest = self.add_change(1)
        non_done = self.add_change(2, "active", "L2")
        for number in range(3, 8):
            self.add_change(number)
        self.write_index()
        for change in (non_done, self.change_id(99)):
            before = self.snapshot(oldest)
            with self.assertRaises(cleanup_tool.CleanupError):
                cleanup_tool.cleanup(self.root, change)
            self.assertEqual(before, self.snapshot(oldest))

    def test_rejects_summary_resume_mismatch_and_validator_failure(self) -> None:
        oldest = self.add_change(1)
        for number in range(2, 7):
            self.add_change(number)
        self.write_index()
        summary = self.changes / oldest / "summary.md"
        summary.write_text(summary.read_text(encoding="utf-8").replace("- **Resume point**: none", "- **Resume point**: L2"), encoding="utf-8")
        before = self.snapshot(oldest)
        with self.assertRaises(cleanup_tool.CleanupError):
            cleanup_tool.cleanup(self.root, oldest)
        self.assertEqual(before, self.snapshot(oldest))
        summary.write_text(summary.read_text(encoding="utf-8").replace("- **Resume point**: L2", "- **Resume point**: none"), encoding="utf-8")
        before_validator = self.snapshot(oldest)
        (self.changes / oldest / "request_analysis" / "checklist.md").unlink()
        with self.assertRaises(cleanup_tool.CleanupError):
            cleanup_tool.cleanup(self.root, oldest)
        self.assertFalse((self.changes / oldest / "request_analysis" / "checklist.md").exists())
        self.assertEqual((self.changes / "INDEX.md").read_bytes(), before_validator[0])

    def test_rejects_incomplete_delivery_evidence(self) -> None:
        oldest = self.add_change(1)
        for number in range(2, 7):
            self.add_change(number)
        self.write_index()
        (self.changes / oldest / "verification_report.md").unlink()
        before = self.snapshot(oldest)
        with self.assertRaises(cleanup_tool.CleanupError):
            cleanup_tool.cleanup(self.root, oldest)
        self.assertEqual(before, self.snapshot(oldest))

    def test_rejects_duplicate_id_and_missing_directory(self) -> None:
        oldest = self.add_change(1)
        for number in range(2, 7):
            self.add_change(number)
        self.write_index()
        index_path = self.changes / "INDEX.md"
        original_index = index_path.read_bytes()
        index_path.write_text(index_path.read_text(encoding="utf-8") + f"| `{oldest}` | `done` | none | duplicate |\n", encoding="utf-8")
        with self.assertRaises(cleanup_tool.CleanupError):
            cleanup_tool.cleanup(self.root, oldest)
        self.assertTrue((self.changes / oldest).is_dir())
        index_path.write_bytes(original_index)
        (self.changes / oldest).rename(self.changes / "feat-missing-dir-20260805")
        with self.assertRaises(cleanup_tool.CleanupError):
            cleanup_tool.cleanup(self.root, oldest)

    def test_no_wiki_candidate_still_cleans(self) -> None:
        oldest = self.add_change(1)
        for number in range(2, 7):
            self.add_change(number)
        self.write_index()
        self.assertFalse((self.changes / oldest / "wiki" / "candidates.md").exists())
        cleanup_tool.cleanup(self.root, oldest)
        self.assertFalse((self.changes / oldest).exists())

    def test_historical_wiki_candidate_does_not_block_cleanup(self) -> None:
        oldest = self.add_change(1)
        for number in range(2, 7):
            self.add_change(number)
        self.write_index()
        (self.changes / oldest / "wiki").mkdir()
        (self.changes / oldest / "wiki" / "candidates.md").write_text(
            "# Business Wiki Candidates\n## Human Wiki Approval\n- Status: approved\n", encoding="utf-8"
        )
        cleanup_tool.cleanup(self.root, oldest)
        self.assertFalse((self.changes / oldest).exists())


if __name__ == "__main__":
    unittest.main()
