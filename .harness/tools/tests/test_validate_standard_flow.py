#!/usr/bin/env python3
"""Tests for Standard-flow validation boundaries."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

TOOL_PATH = Path(__file__).resolve().parents[1] / "validate_change.py"
SPEC = importlib.util.spec_from_file_location("validate_change_tests", TOOL_PATH)
assert SPEC and SPEC.loader
validator_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator_module
SPEC.loader.exec_module(validator_module)


class ValidateStandardFlowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.changes = self.root / ".harness" / "changes"
        self.change_id = "feat-six-phase-fixture-20260818"
        self.change_dir = self.changes / self.change_id
        self.change_dir.mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_change(self, phase: int, substep: str, artifacts: list[str], status: str = "active") -> None:
        resume = "none" if status == "done" else f"Phase {phase} / {substep}"
        (self.changes / "INDEX.md").write_text(
            "# Changes Index\n\n| Change | Status | Resume point | Notes |\n"
            "|---|---|---|---|\n"
            f"| {self.change_id} | {status} | {resume} | fixture |\n",
            encoding="utf-8",
        )
        gate = ""
        if status == "done":
            gate = """
## Gate Record — Phase 6
- Mechanical Gate: pass
- Human Approval: approved
- Command: fixture-check
- Exit code: 0
- Output summary: all six-phase artifacts verified
- Artifact path: delivery-summary.md
"""
        (self.change_dir / "summary.md").write_text(
            "# Summary\n"
            "- **需求**: fixture\n"
            "- **类型**: feat\n"
            "- **日期**: 20260818\n"
            f"- **状态**: {status}\n"
            "- **Flow**: Standard-flow\n"
            f"- **Current step**: Phase {phase}\n"
            f"- **Substep**: {substep}\n"
            f"- **Resume point**: {resume}\n"
            f"{gate}",
            encoding="utf-8",
        )
        for rel in artifacts:
            path = self.change_dir / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if rel == "wiki/candidates.md":
                content = "# Business Wiki Candidates\n## Source Change\n## Extraction Summary\n## Human Wiki Approval\n"
            else:
                content = "# Fixture\n"
            path.write_text(content, encoding="utf-8")

    def issues(self) -> list[validator_module.Issue]:
        validator = validator_module.Validator(self.root, include_done=False)
        validator.validate(self.change_id)
        return validator.issues

    @property
    def phase3_artifacts(self) -> list[str]:
        return [
            "request_analysis/understanding.md",
            "request_analysis/spec.md",
            "request_analysis/tasks.md",
        ]

    def test_phase4_implementation_does_not_require_review_yet(self) -> None:
        self.write_change(4, "implementation", self.phase3_artifacts + ["coding/coding_report_v1.md"])
        self.assertFalse(any(issue.level == "FAIL" for issue in self.issues()))

    def test_phase4_code_review_requires_review_artifact(self) -> None:
        self.write_change(4, "code-review", self.phase3_artifacts + ["coding/coding_report_v1.md"])
        self.assertTrue(any("Phase 4 requires coding/review/*.md" in issue.message for issue in self.issues()))

    def test_phase5_test_review_requires_both_test_artifacts(self) -> None:
        artifacts = self.phase3_artifacts + ["coding/coding_report_v1.md", "coding/review/review_v1.md", "unit_test/test_report.md"]
        self.write_change(5, "test-review", artifacts)
        self.assertTrue(any("Phase 5 requires unit_test/review/test_review_v1.md" in issue.message for issue in self.issues()))

    def test_invalid_substep_is_rejected(self) -> None:
        self.write_change(4, "unit-test", self.phase3_artifacts + ["coding/coding_report_v1.md"])
        self.assertTrue(any(issue.code == "summary.substep_invalid" for issue in self.issues()))

    def test_substep_resume_point_must_match(self) -> None:
        self.write_change(4, "code-review", self.phase3_artifacts + ["coding/coding_report_v1.md", "coding/review/review_v1.md"])
        summary = self.change_dir / "summary.md"
        summary.write_text(summary.read_text(encoding="utf-8").replace("Phase 4 / code-review", "Phase 4 / implementation", 1), encoding="utf-8")
        self.assertTrue(any(issue.code == "summary.substep_resume_mismatch" for issue in self.issues()))

    def test_phase7_is_not_a_valid_standard_phase(self) -> None:
        self.write_change(7, "none", self.phase3_artifacts)
        self.assertTrue(any(issue.code == "summary.phase_invalid" for issue in self.issues()))

    def test_done_standard_flow_requires_all_six_phase_artifacts(self) -> None:
        artifacts = self.phase3_artifacts + [
            "coding/coding_report_v1.md",
            "coding/review/review_v1.md",
            "unit_test/test_report.md",
            "unit_test/review/test_review_v1.md",
            "delivery-summary.md",
            "wiki/candidates.md",
        ]
        self.write_change(6, "none", artifacts, status="done")
        self.assertFalse(any(issue.level == "FAIL" for issue in self.issues()))


if __name__ == "__main__":
    unittest.main()
