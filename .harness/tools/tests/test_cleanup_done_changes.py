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


class CleanupDoneChangesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.changes = self.root / ".harness" / "changes"
        self.wiki = self.root / ".harness" / "wiki"
        self.tools = self.root / ".harness" / "tools"
        self.changes.mkdir(parents=True)
        self.wiki.mkdir(parents=True)
        self.tools.mkdir(parents=True)
        (self.wiki / "index.md").write_text("# Business Wiki Index\n", encoding="utf-8")
        (self.wiki / "log.md").write_text("# Business Wiki Log\n", encoding="utf-8")
        validator_source = TOOL_PATH.with_name("validate_change.py").read_text(encoding="utf-8")
        (self.tools / "validate_change.py").write_text(validator_source, encoding="utf-8")
        self.entries: list[tuple[str, str, str]] = []

    def tearDown(self) -> None:
        self.temp.cleanup()

    def change_id(self, number: int) -> str:
        return f"feat-retention-{number}-20260805"

    def add_change(self, number: int, status: str = "done", resume: str = "none", approval: str = "approved") -> str:
        change_id = self.change_id(number)
        self.entries.append((change_id, status, resume))
        directory = self.changes / change_id
        directory.mkdir()
        (directory / "request_analysis").mkdir()
        (directory / "wiki").mkdir()
        (directory / "request_analysis" / "checklist.md").write_text("# Checklist\n", encoding="utf-8")
        (directory / "verification_report.md").write_text("# Verification\n", encoding="utf-8")
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
        self.write_candidate(change_id, directory, approval)
        return change_id

    def write_candidate(self, change_id: str, directory: Path, status: str) -> None:
        if status == "approved":
            body = """# Business Wiki Candidates

## Source Change
- Change id: {change_id}

## Extraction Summary
- Status: candidates-found

## Human Wiki Approval
- Status: approved
- Decision evidence: User approved formal Wiki update and deletion of this change.
- Official Wiki updates:
  - `.harness/wiki/retention.md`
- Wiki index synchronized: yes
- Wiki log synchronized: yes
- Source evidence summary: summary.md Gate Record and verification report
""".format(change_id=change_id)
        else:
            body = """# Business Wiki Candidates

## Source Change
- Change id: {change_id}

## Extraction Summary
- Status: none

## Human Wiki Approval
- Status: {status}
- Decision evidence: User decided no formal Wiki update and authorized deletion of this change.
- Official Wiki updates:
  - none
- Wiki index synchronized: not-applicable
- Wiki log synchronized: yes
- Source evidence summary: no durable business knowledge found
""".format(change_id=change_id, status=status)
        (directory / "wiki" / "candidates.md").write_text(body, encoding="utf-8")

    def write_index(self) -> None:
        rows = ["# Changes Index\n\n", "| Change | Status | Resume point | Notes |\n", "|--------|--------|--------------|-------|\n"]
        rows.extend(f"| `{change}` | `{status}` | {resume} | test |\n" for change, status, resume in self.entries)
        (self.changes / "INDEX.md").write_text("".join(rows), encoding="utf-8")

    def write_approved_wiki(self, change_id: str, include_index: bool = True, include_log: bool = True) -> None:
        (self.wiki / "retention.md").write_text(
            f"# Retention\n\n- Source change ID: `{change_id}`\n", encoding="utf-8"
        )
        if include_index:
            (self.wiki / "index.md").write_text(
                f"# Business Wiki Index\n\n- `Retention` — `.harness/wiki/retention.md`; Source change ID: `{change_id}`\n",
                encoding="utf-8",
            )
        if include_log:
            (self.wiki / "log.md").write_text(
                "\n".join(
                    [
                        "# Business Wiki Log",
                        "",
                        "## 2026-08-05 — update",
                        f"- Source change ID: `{change_id}`",
                        "- Human approval evidence: User approved formal Wiki update and deletion of this change.",
                        "- Source evidence summary: summary.md Gate Record and verification report",
                        "- Updated Wiki paths:",
                        "  - `.harness/wiki/retention.md`",
                        "- Wiki index synchronized: yes",
                        "- Cleanup disposition: retired-after-sync",
                        "- Notes: retained business rule",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

    def write_no_update_log(self, change_id: str) -> None:
        (self.wiki / "log.md").write_text(
            "\n".join(
                [
                    "# Business Wiki Log",
                    "",
                    "## 2026-08-05 — no-update",
                    f"- Source change ID: `{change_id}`",
                    "- Human approval evidence: User decided no formal Wiki update and authorized deletion of this change.",
                    "- Source evidence summary: no durable business knowledge found",
                    "- Updated Wiki paths:",
                    "  - none",
                    "- Wiki index synchronized: not-applicable",
                    "- Cleanup disposition: retired-after-sync",
                    "- Notes: no reusable knowledge",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def snapshot(self, change_id: str) -> tuple[bytes, tuple[str, ...]]:
        return ((self.changes / "INDEX.md").read_bytes(), tuple(sorted(path.relative_to(self.changes).as_posix() for path in (self.changes / change_id).rglob("*"))))

    def test_refuses_when_done_count_is_exactly_five(self) -> None:
        target = self.add_change(1)
        for number in range(2, 6):
            self.add_change(number)
        self.write_index()
        self.write_approved_wiki(target)
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
        self.write_approved_wiki(oldest)
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
        self.write_approved_wiki(oldest)
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
        self.write_approved_wiki(oldest)
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
        self.write_approved_wiki(oldest)
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

    def test_rejects_ineligible_or_incomplete_wiki_evidence(self) -> None:
        for status in ("pending", "rejected", "deferred", "partially-approved"):
            with self.subTest(status=status):
                self.tearDown()
                self.setUp()
                oldest = self.add_change(1, approval=status)
                for number in range(2, 7):
                    self.add_change(number)
                self.write_index()
                before = self.snapshot(oldest)
                with self.assertRaises(cleanup_tool.CleanupError):
                    cleanup_tool.cleanup(self.root, oldest)
                self.assertEqual(before, self.snapshot(oldest))

        self.tearDown()
        self.setUp()
        oldest = self.add_change(1)
        for number in range(2, 7):
            self.add_change(number)
        self.write_index()
        self.write_approved_wiki(oldest, include_index=False)
        before = self.snapshot(oldest)
        with self.assertRaises(cleanup_tool.CleanupError):
            cleanup_tool.cleanup(self.root, oldest)
        self.assertEqual(before, self.snapshot(oldest))

    def test_rejects_duplicate_id_missing_directory_and_candidate_source_mismatch(self) -> None:
        oldest = self.add_change(1)
        for number in range(2, 7):
            self.add_change(number)
        self.write_index()
        self.write_approved_wiki(oldest)
        index_path = self.changes / "INDEX.md"
        original_index = index_path.read_bytes()
        index_path.write_text(index_path.read_text(encoding="utf-8") + f"| `{oldest}` | `done` | none | duplicate |\n", encoding="utf-8")
        with self.assertRaises(cleanup_tool.CleanupError):
            cleanup_tool.cleanup(self.root, oldest)
        self.assertTrue((self.changes / oldest).is_dir())
        index_path.write_bytes(original_index)
        (self.changes / oldest / "wiki" / "candidates.md").write_text(
            (self.changes / oldest / "wiki" / "candidates.md").read_text(encoding="utf-8").replace(oldest, self.change_id(99)),
            encoding="utf-8",
        )
        with self.assertRaises(cleanup_tool.CleanupError):
            cleanup_tool.cleanup(self.root, oldest)
        self.assertTrue((self.changes / oldest).is_dir())
        (self.changes / oldest / "wiki" / "candidates.md").unlink()
        with self.assertRaises(cleanup_tool.CleanupError):
            cleanup_tool.cleanup(self.root, oldest)
        self.assertTrue((self.changes / oldest).is_dir())

    def test_approved_sync_and_not_requested_sync_succeed(self) -> None:
        oldest = self.add_change(1)
        for number in range(2, 7):
            self.add_change(number)
        self.write_index()
        self.write_approved_wiki(oldest)
        cleanup_tool.cleanup(self.root, oldest)
        self.assertFalse((self.changes / oldest).exists())
        self.assertNotIn(f".harness/changes/{oldest}/wiki/candidates.md", (self.wiki / "retention.md").read_text(encoding="utf-8"))

        self.tearDown()
        self.setUp()
        oldest = self.add_change(1, approval="not-requested")
        for number in range(2, 7):
            self.add_change(number)
        self.write_index()
        self.write_no_update_log(oldest)
        cleanup_tool.cleanup(self.root, oldest)
        self.assertFalse((self.changes / oldest).exists())


if __name__ == "__main__":
    unittest.main()
