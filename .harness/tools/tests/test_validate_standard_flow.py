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

## OpenViking Business Knowledge
- Status: found
- Reason: relevant cancellation rule
- Knowledge root: viking://resources/acme/project-knowledge
- Search query: order cancellation business rules
- Layers searched: wiki
- Read resources: viking://resources/acme/project-knowledge/wiki/business/rules/order-cancellation.md
- Applied business knowledge: cancellation requires refund authorization
- Conflicts / stale knowledge: none
- Missing knowledge: none
- Open Questions: none

## Problem Statement
- fixture
"""

SPEC_CONTENT = """# Spec

## Project / System Knowledge
- Status: found
- Reason: applicable interface contract
- Knowledge root: viking://resources/acme/project-knowledge
- Search query: interface contracts
- Layers searched: wiki+raw
- Read resources: viking://resources/acme/project-knowledge/wiki/technical/standards/order-api.md; viking://resources/acme/project-knowledge/raw/technical/order-api-spec.md
- Applied constraints: use repository pattern
- Conflicts / stale knowledge: none
- Open Questions: none

## Objective
- fixture
"""

DELIVERY_CONTENT = """# Delivery Summary

## OpenViking Knowledge Update
- Durable knowledge: yes; Reason: reusable cancellation rule
- Required for delivery: no; Reason: knowledge persistence is best effort
- Knowledge root: viking://resources/acme/project-knowledge
- Source artifact: delivery-summary.md
- Disposition: Update
- Status: completed
- Raw URI(s): viking://resources/acme/project-knowledge/raw/requirements/2026-08-18-order-cancellation.md
- Wiki URI(s): viking://resources/acme/project-knowledge/wiki/business/rules/order-cancellation.md
- Index/log result: wiki/index.md updated; wiki/log.md appended
- Operation ID: task-123
- Operation result: task completed
- Retry note: none
"""


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
        self.assertIn("knowledge.discovery_missing", codes)

    def test_found_status_without_viking_uri_warns(self) -> None:
        self.write_change(1, "none", ["request_analysis/understanding.md"])
        (self.change_dir / "request_analysis" / "understanding.md").write_text(
            "# Understanding\n\n## OpenViking Business Knowledge\n- Status: found\n- Search query: x\n- Read resources: none\n",
            encoding="utf-8",
        )
        codes = {issue.code for issue in self.issues()}
        self.assertIn("knowledge.discovery_uri_missing", codes)

    def test_phase2_spec_without_openviking_warns(self) -> None:
        self.write_change(2, "none", self.phase3_artifacts)
        (self.change_dir / "request_analysis" / "spec.md").write_text(
            "# Spec\n\n## Objective\n- fixture\n", encoding="utf-8"
        )
        codes = {issue.code for issue in self.issues()}
        self.assertIn("knowledge.discovery_missing", codes)

    # -- OpenViking final knowledge update status -------------------------

    def _done_update_codes(self, delivery_content: str) -> set[str]:
        self.write_change(6, "none", self.done_artifacts, status="done")
        (self.change_dir / "delivery-summary.md").write_text(delivery_content, encoding="utf-8")
        return {issue.code for issue in self.issues()}

    def test_done_update_missing_status_fails(self) -> None:
        codes = self._done_update_codes("# Delivery Summary\n")
        self.assertIn("knowledge.update_missing", codes)

    def test_done_update_completed_requires_raw_uri(self) -> None:
        codes = self._done_update_codes(
            "# Delivery Summary\n\n## OpenViking Knowledge Update\n"
            "- Durable knowledge: yes; Reason: reusable rule\n"
            "- Required for delivery: no; Reason: best effort\n"
            "- Knowledge root: viking://resources/acme/project-knowledge\n"
            "- Disposition: Update\n"
            "- Status: completed\n"
            "- Raw URI(s): none\n"
            "- Wiki URI(s): viking://resources/acme/project-knowledge/wiki/business/rules/rule.md\n"
            "- Index/log result: wiki/index.md updated; wiki/log.md appended\n"
        )
        self.assertIn("knowledge.raw_uri_missing", codes)

    def test_done_compiled_update_requires_wiki_uri(self) -> None:
        codes = self._done_update_codes(
            "# Delivery Summary\n\n## OpenViking Knowledge Update\n"
            "- Durable knowledge: yes; Reason: reusable rule\n"
            "- Required for delivery: no; Reason: best effort\n"
            "- Knowledge root: viking://resources/acme/project-knowledge\n"
            "- Disposition: New\n"
            "- Status: completed\n"
            "- Raw URI(s): viking://resources/acme/project-knowledge/raw/requirements/source.md\n"
            "- Wiki URI(s): none\n"
            "- Index/log result: wiki/index.md updated; wiki/log.md appended\n"
        )
        self.assertIn("knowledge.wiki_uri_missing", codes)

    def test_done_no_material_requires_raw_and_log_but_no_wiki(self) -> None:
        self.write_change(6, "none", self.done_artifacts, status="done")
        (self.change_dir / "delivery-summary.md").write_text(
            "# Delivery Summary\n\n## OpenViking Knowledge Update\n"
            "- Durable knowledge: yes; Reason: source retained for traceability\n"
            "- Required for delivery: no; Reason: best effort\n"
            "- Knowledge root: viking://resources/acme/project-knowledge\n"
            "- Disposition: No material\n"
            "- Status: completed\n"
            "- Raw URI(s): viking://resources/acme/project-knowledge/raw/technical/source.md\n"
            "- Wiki URI(s): none\n"
            "- Index/log result: wiki/log.md appended; index unchanged\n",
            encoding="utf-8",
        )
        self.assertFalse(any(issue.level == "FAIL" for issue in self.issues()))

    def test_done_no_material_rejects_wiki_article(self) -> None:
        content = (
            "# Delivery Summary\n\n## OpenViking Knowledge Update\n"
            "- Durable knowledge: yes; Reason: source retained for traceability\n"
            "- Required for delivery: no; Reason: best effort\n"
            "- Knowledge root: viking://resources/acme/project-knowledge\n"
            "- Disposition: No material\n"
            "- Status: completed\n"
            "- Raw URI(s): viking://resources/acme/project-knowledge/raw/technical/source.md\n"
            "- Wiki URI(s): viking://resources/acme/project-knowledge/wiki/technical/modules/source.md\n"
            "- Index/log result: wiki/log.md appended; index unchanged\n"
        )
        self.assertIn("knowledge.no_material_has_wiki", self._done_update_codes(content))

    def test_done_update_rejects_uri_outside_knowledge_root(self) -> None:
        codes = self._done_update_codes(
            DELIVERY_CONTENT.replace(
                "viking://resources/acme/project-knowledge/raw/requirements/2026-08-18-order-cancellation.md",
                "viking://resources/other-project/raw/requirements/source.md",
            )
        )
        self.assertIn("knowledge.raw_uri_outside_root", codes)

    def test_done_update_rejects_invalid_disposition(self) -> None:
        codes = self._done_update_codes(
            DELIVERY_CONTENT.replace("- Disposition: Update", "- Disposition: No material; Update")
        )
        self.assertIn("knowledge.disposition_invalid", codes)

    def test_done_update_not_needed_requires_reason(self) -> None:
        codes = self._done_update_codes(
            "# Delivery Summary\n\n## OpenViking Knowledge Update\n"
            "- Durable knowledge: no; Reason: none\n"
            "- Required for delivery: no; Reason: best effort\n"
            "- Status: not-needed\n"
        )
        self.assertIn("knowledge.reason_missing", codes)

    def test_done_update_required_failed_status_fails(self) -> None:
        codes = self._done_update_codes(
            "# Delivery Summary\n\n## OpenViking Knowledge Update\n"
            "- Durable knowledge: yes; Reason: required project contract\n"
            "- Required for delivery: yes; Reason: approved spec requires persistence\n"
            "- Status: failed\n"
            "- Operation result: service rejected write\n"
            "- Retry note: restore service and retry once\n"
        )
        self.assertIn("openviking.write_failed", codes)

    def test_done_update_nonblocking_failed_status_warns(self) -> None:
        self.write_change(6, "none", self.done_artifacts, status="done")
        (self.change_dir / "delivery-summary.md").write_text(
            "# Delivery Summary\n\n## OpenViking Knowledge Update\n"
            "- Durable knowledge: yes; Reason: reusable project convention\n"
            "- Required for delivery: no; Reason: best effort\n"
            "- Status: failed\n"
            "- Operation result: service rejected write\n"
            "- Retry note: retry after service recovery\n",
            encoding="utf-8",
        )
        issues = self.issues()
        self.assertFalse(any(issue.level == "FAIL" for issue in issues))
        self.assertTrue(any(issue.code == "openviking.write_failed" for issue in issues))

    def test_done_update_failure_requires_retry_note(self) -> None:
        codes = self._done_update_codes(
            "# Delivery Summary\n\n## OpenViking Knowledge Update\n"
            "- Durable knowledge: yes; Reason: reusable project convention\n"
            "- Required for delivery: no; Reason: best effort\n"
            "- Status: unavailable\n"
            "- Operation result: service unavailable\n"
            "- Retry note: none\n"
        )
        self.assertIn("knowledge.retry_note_missing", codes)

    def test_done_update_invalid_status_fails(self) -> None:
        codes = self._done_update_codes(
            "# Delivery Summary\n\n## OpenViking Knowledge Update\n- Status: banana\n"
        )
        self.assertIn("knowledge.update_invalid", codes)

    def test_done_update_not_needed_with_reason_passes(self) -> None:
        self.write_change(6, "none", self.done_artifacts, status="done")
        (self.change_dir / "delivery-summary.md").write_text(
            "# Delivery Summary\n\n## OpenViking Knowledge Update\n"
            "- Durable knowledge: no; Reason: no reusable knowledge\n"
            "- Required for delivery: no; Reason: no knowledge operation\n"
            "- Status: not-needed\n"
            "- Operation result: none\n",
            encoding="utf-8",
        )
        self.assertFalse(any(issue.level == "FAIL" for issue in self.issues()))

    def test_active_phase6_allows_pending_update(self) -> None:
        self.write_change(6, "none", self.done_artifacts, status="active")
        (self.change_dir / "delivery-summary.md").write_text(
            "# Delivery Summary\n\n## OpenViking Knowledge Update\n"
            "- Durable knowledge: yes; Reason: reusable project convention\n"
            "- Required for delivery: no; Reason: best effort\n"
            "- Knowledge root: viking://resources/acme/project-knowledge\n"
            "- Source artifact: delivery-summary.md\n"
            "- Disposition: Update\n"
            "- Status: pending\n"
            "- Raw URI(s): none\n"
            "- Wiki URI(s): none\n"
            "- Index/log result: pending\n"
            "- Operation ID: none\n"
            "- Operation result: awaiting final approval\n"
            "- Retry note: none\n",
            encoding="utf-8",
        )
        self.assertFalse(any(issue.level == "FAIL" for issue in self.issues()))

    def test_done_update_cannot_remain_pending(self) -> None:
        codes = self._done_update_codes(
            "# Delivery Summary\n\n## OpenViking Knowledge Update\n"
            "- Durable knowledge: yes; Reason: reusable project convention\n"
            "- Required for delivery: no; Reason: best effort\n"
            "- Status: pending\n"
        )
        self.assertIn("knowledge.update_pending", codes)

    def test_not_needed_discovery_requires_reason(self) -> None:
        self.write_change(1, "none", ["request_analysis/understanding.md"])
        (self.change_dir / "request_analysis" / "understanding.md").write_text(
            "# Understanding\n\n## OpenViking Business Knowledge\n"
            "- Status: not-needed\n"
            "- Reason: none\n",
            encoding="utf-8",
        )
        codes = {issue.code for issue in self.issues()}
        self.assertIn("knowledge.discovery_reason_missing", codes)

    def test_found_raw_only_does_not_count_as_compiled_knowledge(self) -> None:
        self.write_change(1, "none", ["request_analysis/understanding.md"])
        (self.change_dir / "request_analysis" / "understanding.md").write_text(
            "# Understanding\n\n## OpenViking Business Knowledge\n"
            "- Status: found\n"
            "- Reason: raw source matched\n"
            "- Knowledge root: viking://resources/acme/project-knowledge\n"
            "- Search query: cancellation\n"
            "- Layers searched: wiki+raw\n"
            "- Read resources: viking://resources/acme/project-knowledge/raw/requirements/source.md\n",
            encoding="utf-8",
        )
        codes = {issue.code for issue in self.issues()}
        self.assertIn("knowledge.discovery_uri_missing", codes)


if __name__ == "__main__":
    unittest.main()
