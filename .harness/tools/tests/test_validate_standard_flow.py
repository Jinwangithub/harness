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


UNDERSTANDING_CONTENT = """# Understanding

## Business Context
- Status: found
- Reason: relevant cancellation rule
- Knowledge root: viking://resources/acme/project-knowledge
- Search query: order cancellation business rules
- Layers searched: openviking
- Read resources: viking://resources/acme/project-knowledge/knowledge/business/rules/order-cancellation.md
- Applied business knowledge: cancellation requires refund authorization
- Conflicts / stale knowledge: none
- Missing knowledge: none
- Open Questions: none

## Problem Statement
- fixture
"""

SPEC_CONTENT = """# Spec

## Project / System Context
- Status: found
- Reason: applicable interface contract
- Knowledge root: viking://resources/acme/project-knowledge
- Search query: interface contracts
- Layers searched: openviking
- Read resources: viking://resources/acme/project-knowledge/knowledge/technical/standards/order-api.md; viking://resources/acme/project-knowledge/source/technical/order-api-spec.md
- Applied constraints: use repository pattern
- Conflicts / stale knowledge: none
- Open Questions: none

## Objective
- fixture
"""

DELIVERY_CONTENT = "# Delivery Summary\n"


class ValidateStandardFlowTests(unittest.TestCase):
    ARTIFACT_CONTENT = {
        "request_analysis/understanding.md": UNDERSTANDING_CONTENT,
        "request_analysis/spec.md": SPEC_CONTENT,
        "delivery-summary.md": DELIVERY_CONTENT,
    }

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
            path.write_text(self.ARTIFACT_CONTENT.get(rel, "# Fixture\n"), encoding="utf-8")

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

    @property
    def done_artifacts(self) -> list[str]:
        return self.phase3_artifacts + [
            "coding/coding_report_v1.md",
            "coding/review/review_v1.md",
            "unit_test/test_report.md",
            "unit_test/review/test_review_v1.md",
            "delivery-summary.md",
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
        self.write_change(6, "none", self.done_artifacts, status="done")
        self.assertFalse(any(issue.level == "FAIL" for issue in self.issues()))

    # -- OpenViking Phase 1/2 discovery evidence --------------------------

    def test_phase1_understanding_without_openviking_warns(self) -> None:
        self.write_change(1, "none", ["request_analysis/understanding.md"])
        (self.change_dir / "request_analysis" / "understanding.md").write_text(
            "# Understanding\n\n## Problem Statement\n- fixture\n", encoding="utf-8"
        )
        codes = {issue.code for issue in self.issues()}
        self.assertIn("context.discovery_missing", codes)

    def test_found_status_without_viking_uri_warns(self) -> None:
        self.write_change(1, "none", ["request_analysis/understanding.md"])
        (self.change_dir / "request_analysis" / "understanding.md").write_text(
            "# Understanding\n\n## Business Context\n- Status: found\n- Search query: x\n- Read resources: none\n",
            encoding="utf-8",
        )
        codes = {issue.code for issue in self.issues()}
        self.assertIn("context.discovery_uri_missing", codes)

    def test_phase2_spec_without_openviking_warns(self) -> None:
        self.write_change(2, "none", self.phase3_artifacts)
        (self.change_dir / "request_analysis" / "spec.md").write_text(
            "# Spec\n\n## Objective\n- fixture\n", encoding="utf-8"
        )
        codes = {issue.code for issue in self.issues()}
        self.assertIn("context.discovery_missing", codes)

    def test_not_needed_discovery_requires_reason(self) -> None:
        self.write_change(1, "none", ["request_analysis/understanding.md"])
        (self.change_dir / "request_analysis" / "understanding.md").write_text(
            "# Understanding\n\n## Business Context\n"
            "- Status: not-needed\n"
            "- Reason: none\n",
            encoding="utf-8",
        )
        codes = {issue.code for issue in self.issues()}
        self.assertIn("context.discovery_reason_missing", codes)

    def test_found_openviking_resource_counts_as_knowledge(self) -> None:
        self.write_change(1, "none", ["request_analysis/understanding.md"])
        (self.change_dir / "request_analysis" / "understanding.md").write_text(
            "# Understanding\n\n## Business Context\n"
            "- Status: found\n"
            "- Reason: raw source matched\n"
            "- Knowledge root: viking://resources/acme/project-knowledge\n"
            "- Search query: cancellation\n"
            "- Layers searched: openviking\n"
            "- Read resources: viking://resources/acme/project-knowledge/resources/source.md\n",
            encoding="utf-8",
        )
        codes = {issue.code for issue in self.issues()}
        self.assertNotIn("context.discovery_uri_missing", codes)


if __name__ == "__main__":
    unittest.main()
