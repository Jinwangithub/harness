#!/usr/bin/env python3
"""Validate Harness change registry and artifacts.

This checker intentionally validates only mechanical facts: file existence,
canonical statuses, required summary fields, Gate Record evidence fields, and
basic flow artifact boundaries. It does not judge business correctness.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


VALID_STATUSES = {"active", "done", "abandoned"}
VALID_FLOWS = {"Lite-flow", "Standard-flow"}
CHANGE_NAME_RE = re.compile(
    r"^(feat|fix|refactor|perf|test|docs|chore)-[a-z0-9][a-z0-9-]*-\d{8}$"
)
INDEX_ROW_RE = re.compile(
    r"^\|\s*`?([^`|]+?)`?\s*\|\s*`?([^`|]+?)`?\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*$"
)
SUMMARY_FIELD_RE = re.compile(r"^- \*\*(.+?)\*\*:\s*(.*?)\s*$", re.MULTILINE)
GATE_RECORD_RE = re.compile(
    r"^## Gate Record\s*[—-]\s*(.+?)\s*$([\s\S]*?)(?=^##\s+|\Z)",
    re.MULTILINE,
)

REQUIRED_SUMMARY_FIELDS = {
    "需求",
    "类型",
    "日期",
    "状态",
    "Flow",
    "Current step",
    "Resume point",
}

LITE_REQUIRED = [
    Path("summary.md"),
    Path("request_analysis/checklist.md"),
]
LITE_FINAL_REQUIRED = [Path("verification_report.md")]
LITE_FORBIDDEN = [
    Path("request_analysis/understanding.md"),
    Path("request_analysis/spec.md"),
    Path("request_analysis/tasks.md"),
    Path("coding"),
    Path("unit_test"),
    Path("ci_result"),
    Path("deployment"),
    Path("delivery-summary.md"),
]
STANDARD_PHASE_ARTIFACTS = {
    1: Path("request_analysis/understanding.md"),
    2: Path("request_analysis/spec.md"),
    3: Path("request_analysis/tasks.md"),
    4: Path("coding/coding_report_v1.md"),
    6: Path("unit_test/test_report.md"),
    7: Path("unit_test/review/test_review_v1.md"),
    8: Path("ci_result/ci_report.md"),
    9: Path("deployment/deploy_report.md"),
    10: Path("delivery-summary.md"),
}


@dataclass(frozen=True)
class Issue:
    level: str
    code: str
    message: str


@dataclass(frozen=True)
class IndexEntry:
    change: str
    status: str
    resume_point: str
    notes: str


class Validator:
    def __init__(self, repo_root: Path, include_done: bool) -> None:
        self.repo_root = repo_root
        self.harness_dir = repo_root / ".harness"
        self.changes_dir = self.harness_dir / "changes"
        self.index_path = self.changes_dir / "INDEX.md"
        self.include_done = include_done
        self.issues: list[Issue] = []

    def fail(self, code: str, message: str) -> None:
        self.issues.append(Issue("FAIL", code, message))

    def warn(self, code: str, message: str) -> None:
        self.issues.append(Issue("WARN", code, message))

    def validate(self, requested_change: str | None) -> int:
        entries = self.validate_index()
        if requested_change:
            matching = [entry for entry in entries if entry.change == requested_change]
            if not matching:
                self.fail("change.not_in_index", f"Change is not listed in INDEX.md: {requested_change}")
                change_dir = self.changes_dir / requested_change
                if change_dir.exists():
                    self.validate_change_dir(change_dir, None)
            else:
                self.validate_change_dir(self.changes_dir / requested_change, matching[0])
        else:
            targets = [entry for entry in entries if entry.status == "active"]
            if self.include_done:
                targets = entries
            if not targets:
                self.warn("index.no_active", "No active change in INDEX.md; registry is idle.")
            for entry in targets:
                self.validate_change_dir(self.changes_dir / entry.change, entry)

        self.print_report()
        return 1 if any(issue.level == "FAIL" for issue in self.issues) else 0

    def validate_index(self) -> list[IndexEntry]:
        if not self.index_path.exists():
            self.fail("index.missing", f"Missing registry: {self.index_path}")
            return []

        entries: list[IndexEntry] = []
        active_count = 0
        for line in self.index_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped.startswith("|") or "---" in stripped or "Change" in stripped:
                continue
            match = INDEX_ROW_RE.match(stripped)
            if not match:
                self.fail("index.row_malformed", f"Malformed INDEX row: {stripped}")
                continue
            change, status, resume_point, notes = [part.strip() for part in match.groups()]
            if status not in VALID_STATUSES:
                self.fail("index.status_invalid", f"{change}: invalid status `{status}`")
            if status == "active":
                active_count += 1
            if not CHANGE_NAME_RE.match(change):
                self.fail("change.name_invalid", f"{change}: expected {{type}}-{{name}}-YYYYMMDD")
            if not (self.changes_dir / change).exists():
                self.fail("change.dir_missing", f"{change}: directory listed in INDEX.md does not exist")
            entries.append(IndexEntry(change, status, resume_point, notes))

        if active_count > 1:
            self.fail("index.multiple_active", f"INDEX.md has {active_count} active changes; at most one is allowed")
        return entries

    def validate_change_dir(self, change_dir: Path, entry: IndexEntry | None) -> None:
        if not change_dir.exists():
            return
        if not CHANGE_NAME_RE.match(change_dir.name):
            self.fail("change.name_invalid", f"{change_dir.name}: expected {{type}}-{{name}}-YYYYMMDD")

        summary_path = change_dir / "summary.md"
        if not summary_path.exists():
            self.fail("summary.missing", f"{change_dir.name}: missing summary.md")
            return

        text = summary_path.read_text(encoding="utf-8")
        fields = self.parse_summary_fields(text)
        self.validate_summary_fields(change_dir, entry, fields, text)
        self.validate_flow_artifacts(change_dir, fields)
        self.validate_gate_records(change_dir, text, fields)

    def parse_summary_fields(self, text: str) -> dict[str, str]:
        return {key.strip(): value.strip() for key, value in SUMMARY_FIELD_RE.findall(text)}

    def validate_summary_fields(
        self, change_dir: Path, entry: IndexEntry | None, fields: dict[str, str], text: str
    ) -> None:
        missing = sorted(REQUIRED_SUMMARY_FIELDS - fields.keys())
        for field in missing:
            self.fail("summary.field_missing", f"{change_dir.name}: missing summary field `{field}`")

        status = fields.get("状态")
        flow = fields.get("Flow")
        change_type = fields.get("类型")
        date = fields.get("日期")

        if status and status not in VALID_STATUSES:
            self.fail("summary.status_invalid", f"{change_dir.name}: invalid summary status `{status}`")
        if flow and flow not in VALID_FLOWS:
            self.fail("summary.flow_invalid", f"{change_dir.name}: invalid Flow `{flow}`")
        if change_type and change_type not in {"feat", "fix", "refactor", "perf", "test", "docs", "chore"}:
            self.fail("summary.type_invalid", f"{change_dir.name}: invalid type `{change_type}`")
        if date and not re.fullmatch(r"\d{8}", date):
            self.fail("summary.date_invalid", f"{change_dir.name}: invalid date `{date}`")

        if entry:
            if status and status != entry.status:
                self.fail(
                    "summary.index_status_mismatch",
                    f"{change_dir.name}: summary status `{status}` differs from INDEX status `{entry.status}`",
                )
            resume = fields.get("Resume point")
            if resume and entry.resume_point and entry.resume_point != resume:
                self.warn(
                    "summary.index_resume_mismatch",
                    f"{change_dir.name}: summary Resume point `{resume}` differs from INDEX `{entry.resume_point}`",
                )

        if "resume_from" in text:
            self.warn("summary.legacy_field", f"{change_dir.name}: legacy field `resume_from` found")

        completion_lock = self.extract_named_value(text, "Completion lock")
        human_pending = re.search(r"Human Approval\s*:\s*\{?pending\}?", text, re.IGNORECASE)
        if human_pending and completion_lock and completion_lock.lower() != "locked":
            self.fail(
                "completion_lock.invalid",
                f"{change_dir.name}: Human Approval pending requires Completion lock locked",
            )
        if human_pending and status == "done":
            self.fail("completion.pending_done", f"{change_dir.name}: pending Human Approval cannot be done")

    def validate_flow_artifacts(self, change_dir: Path, fields: dict[str, str]) -> None:
        flow = fields.get("Flow")
        status = fields.get("状态")
        current_step = fields.get("Current step", "")

        if flow == "Lite-flow":
            for rel in LITE_REQUIRED:
                if not (change_dir / rel).exists():
                    self.fail("artifact.missing", f"{change_dir.name}: Lite-flow requires {rel}")
            if status == "done" or "L3" in current_step:
                for rel in LITE_FINAL_REQUIRED:
                    if not (change_dir / rel).exists():
                        self.fail("artifact.missing", f"{change_dir.name}: Lite-flow final delivery requires {rel}")
            for rel in LITE_FORBIDDEN:
                if (change_dir / rel).exists():
                    self.fail("artifact.forbidden", f"{change_dir.name}: Lite-flow must not contain {rel}")
        elif flow == "Standard-flow":
            phase = self.extract_phase(current_step)
            if phase is None and status == "done":
                phase = 10
            if phase:
                for number, rel in STANDARD_PHASE_ARTIFACTS.items():
                    if number <= phase and not (change_dir / rel).exists():
                        self.fail("artifact.missing", f"{change_dir.name}: Phase {number} requires {rel}")
                if phase >= 5 and not any((change_dir / "coding/review").glob("*.md")):
                    self.fail("artifact.missing", f"{change_dir.name}: Phase 5 requires coding/review/*.md")
            if status == "done" and not (change_dir / "delivery-summary.md").exists():
                self.fail("artifact.missing", f"{change_dir.name}: done Standard-flow requires delivery-summary.md")

    def validate_gate_records(self, change_dir: Path, text: str, fields: dict[str, str]) -> None:
        records = list(GATE_RECORD_RE.finditer(text))
        status = fields.get("状态")
        if not records:
            if status == "active":
                self.warn("gate.none", f"{change_dir.name}: no Gate Record found yet")
            elif status == "done":
                self.fail("gate.none", f"{change_dir.name}: done change requires at least one Gate Record")
            return

        for record in records:
            label = record.group(1).strip()
            body = record.group(2)
            mechanical = self.extract_bullet_value(body, "Mechanical Gate")
            human = self.extract_bullet_value(body, "Human Approval")
            command = self.extract_bullet_value(body, "Command")
            exit_code = self.extract_bullet_value(body, "Exit code")
            output = self.extract_bullet_value(body, "Output summary")
            artifact = self.extract_bullet_value(body, "Artifact path")

            if mechanical not in {"pass", "fail", "blocked"}:
                self.fail("gate.mechanical_invalid", f"{change_dir.name} {label}: invalid Mechanical Gate `{mechanical}`")
            if human not in {"approved", "rejected", "pending"}:
                self.fail("gate.human_invalid", f"{change_dir.name} {label}: invalid Human Approval `{human}`")

            evidence = {
                "Command": command,
                "Exit code": exit_code,
                "Output summary": output,
                "Artifact path": artifact,
            }
            for field, value in evidence.items():
                if self.is_placeholder_or_empty(value):
                    self.fail("gate.evidence_missing", f"{change_dir.name} {label}: missing {field}")
            if exit_code and not re.fullmatch(r"\d+", exit_code):
                self.fail("gate.exit_code_invalid", f"{change_dir.name} {label}: Exit code must be numeric")
            if output and output in {"成功", "已完成", "success", "done"}:
                self.fail("gate.output_too_vague", f"{change_dir.name} {label}: Output summary is too vague")
            if artifact and not self.is_placeholder_or_empty(artifact):
                artifact_path = (change_dir / artifact).resolve() if not Path(artifact).is_absolute() else Path(artifact)
                if not artifact_path.exists():
                    self.fail("gate.artifact_missing", f"{change_dir.name} {label}: Artifact path does not exist: {artifact}")
            if any(self.is_placeholder_or_empty(value) for value in evidence.values()) and mechanical == "pass":
                self.fail("gate.pass_without_evidence", f"{change_dir.name} {label}: pass requires complete fresh evidence")
            if human == "pending" and fields.get("状态") == "done":
                self.fail("gate.pending_done", f"{change_dir.name} {label}: pending Human Approval cannot be done")

    def extract_phase(self, current_step: str) -> int | None:
        match = re.search(r"Phase\s+(\d+)", current_step, re.IGNORECASE)
        if not match:
            return None
        phase = int(match.group(1))
        return phase if 1 <= phase <= 10 else None

    def extract_named_value(self, text: str, name: str) -> str | None:
        patterns = [
            rf"^- \*\*{re.escape(name)}\*\*:\s*(.*?)\s*$",
            rf"^- {re.escape(name)}:\s*(.*?)\s*$",
            rf"^{re.escape(name)}:\s*(.*?)\s*$",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
            if match:
                return self.clean_value(match.group(1))
        return None

    def extract_bullet_value(self, text: str, name: str) -> str | None:
        match = re.search(rf"^\s*-\s*{re.escape(name)}:\s*(.*?)\s*$", text, re.MULTILINE | re.IGNORECASE)
        if not match:
            return None
        return self.clean_value(match.group(1))

    def clean_value(self, value: str) -> str:
        value = value.strip()
        if value.startswith("{") and value.endswith("}"):
            return ""
        return value.strip("` ")

    def is_placeholder_or_empty(self, value: str | None) -> bool:
        if value is None:
            return True
        cleaned = value.strip()
        return not cleaned or (cleaned.startswith("{") and cleaned.endswith("}"))

    def print_report(self) -> None:
        if not self.issues:
            print("PASS: Harness changes validation passed.")
            return
        for issue in self.issues:
            print(f"{issue.level}: {issue.code}: {issue.message}")
        fail_count = sum(1 for issue in self.issues if issue.level == "FAIL")
        warn_count = sum(1 for issue in self.issues if issue.level == "WARN")
        status = "FAIL" if fail_count else "PASS"
        print(f"{status}: {fail_count} failure(s), {warn_count} warning(s).")


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".harness" / "changes" / "INDEX.md").exists():
            return candidate
    return current


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate Harness change registry and artifacts.")
    parser.add_argument("--repo", type=Path, default=None, help="Repository root. Defaults to nearest parent with .harness/changes/INDEX.md.")
    parser.add_argument("--change", help="Validate one change directory by name.")
    parser.add_argument("--all", action="store_true", help="Validate all INDEX.md entries, not only active changes.")
    args = parser.parse_args(argv)

    repo_root = args.repo.resolve() if args.repo else find_repo_root(Path.cwd())
    validator = Validator(repo_root, include_done=args.all)
    return validator.validate(args.change)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
