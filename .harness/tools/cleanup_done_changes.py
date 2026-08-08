#!/usr/bin/env python3
"""Retire one excess completed Harness change after recorded Wiki synchronization."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

DONE_LIMIT = 5
INDEX_ROW_RE = re.compile(
    r"^\|\s*`?([^`|]+?)`?\s*\|\s*`?([^`|]+?)`?\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*$"
)
SUMMARY_FIELD_RE = re.compile(r"^- \*\*(.+?)\*\*:\s*(.*?)\s*$", re.MULTILINE)
APPROVAL_RE = re.compile(r"^## Human Wiki Approval\s*$([\s\S]*?)(?=^##\s+|\Z)", re.MULTILINE)
LOG_RECORD_RE = re.compile(r"^##\s+.*$[\s\S]*?(?=^##\s+|\Z)", re.MULTILINE)
PLACEHOLDER_RE = re.compile(r"^\{.*\}$")


@dataclass(frozen=True)
class IndexRow:
    line_number: int
    raw_line: str
    change: str
    status: str
    resume_point: str


class CleanupError(Exception):
    """A failed cleanup precondition."""


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".harness" / "changes" / "INDEX.md").exists():
            return candidate
    return current


def parse_index(index_path: Path) -> tuple[list[str], list[IndexRow]]:
    try:
        lines = index_path.read_text(encoding="utf-8").splitlines(keepends=True)
    except FileNotFoundError as error:
        raise CleanupError(f"Missing registry: {index_path}") from error

    rows: list[IndexRow] = []
    seen: set[str] = set()
    for number, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if not stripped.startswith("|") or "---" in stripped or "Change" in stripped:
            continue
        match = INDEX_ROW_RE.match(stripped)
        if not match:
            raise CleanupError(f"Malformed INDEX row at line {number}: {stripped}")
        change, status, resume_point, _notes = (part.strip() for part in match.groups())
        if change in seen:
            raise CleanupError(f"Duplicate change ID in INDEX.md: {change}")
        seen.add(change)
        rows.append(IndexRow(number, raw_line, change, status, resume_point))
    return lines, rows


def is_nonplaceholder(value: str | None) -> bool:
    return bool(value and value.strip() and not PLACEHOLDER_RE.fullmatch(value.strip()))


def parse_summary_fields(summary_path: Path) -> dict[str, str]:
    try:
        text = summary_path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise CleanupError(f"Missing summary: {summary_path}") from error
    return {key.strip(): value.strip() for key, value in SUMMARY_FIELD_RE.findall(text)}


def approval_fields(candidate_path: Path) -> tuple[dict[str, str], list[str]]:
    try:
        text = candidate_path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise CleanupError(f"Missing Wiki candidate: {candidate_path}") from error
    match = APPROVAL_RE.search(text)
    if not match:
        raise CleanupError("Candidate lacks Human Wiki Approval section")

    fields: dict[str, str] = {}
    official_paths: list[str] = []
    current_field: str | None = None
    for line in match.group(1).splitlines():
        field_match = re.match(r"^-\s+([A-Za-z ]+):\s*(.*?)\s*$", line)
        if field_match:
            current_field = field_match.group(1).strip().lower()
            fields[current_field] = field_match.group(2).strip().strip("`")
            continue
        path_match = re.match(r"^\s+-\s+`?([^`]+?)`?\s*$", line)
        if current_field == "official wiki updates" and path_match:
            official_path = path_match.group(1).strip()
            official_paths.append(official_path)
            if official_path.lower() == "none":
                fields[current_field] = "none"
    if fields.get("official wiki updates") and fields["official wiki updates"] != "none":
        official_paths.append(fields["official wiki updates"])
    return fields, [path for path in official_paths if path.lower() != "none"]


def matching_log_record(log_text: str, change_id: str) -> str | None:
    source = f"- Source change ID: `{change_id}`"
    for record in LOG_RECORD_RE.findall(log_text):
        if source in record:
            return record
    return None


def require_log_evidence(
    repo_root: Path, change_id: str, decision: str, wiki_paths: list[str], index_value: str
) -> None:
    log_path = repo_root / ".harness" / "wiki" / "log.md"
    try:
        record = matching_log_record(log_path.read_text(encoding="utf-8"), change_id)
    except FileNotFoundError as error:
        raise CleanupError(f"Missing Wiki log: {log_path}") from error
    if record is None:
        raise CleanupError(f"Wiki log has no record for source change ID `{change_id}`")
    if not is_nonplaceholder(re.search(r"^- Human approval evidence:\s*(.*?)\s*$", record, re.MULTILINE | re.IGNORECASE).group(1) if re.search(r"^- Human approval evidence:\s*(.*?)\s*$", record, re.MULTILINE | re.IGNORECASE) else None):
        raise CleanupError("Wiki log is missing human approval evidence")
    if f"- Cleanup disposition: retired-after-sync" not in record:
        raise CleanupError("Wiki log cleanup disposition is not retired-after-sync")
    if f"- Wiki index synchronized: {index_value}" not in record:
        raise CleanupError("Wiki log index synchronization does not match candidate")
    if decision == "not-requested":
        if "no-update" not in record.splitlines()[0]:
            raise CleanupError("not-requested cleanup requires a no-update Wiki log record")
        if not re.search(r"^\s*-\s+`?none`?\s*$", record, re.MULTILINE | re.IGNORECASE):
            raise CleanupError("no-update Wiki log record must list Updated Wiki paths as none")
    else:
        for wiki_path in wiki_paths:
            if wiki_path not in record:
                raise CleanupError(f"Wiki log does not list synchronized path: {wiki_path}")


def validate_wiki_sync(repo_root: Path, change_id: str, candidate_path: Path) -> None:
    try:
        candidate_text = candidate_path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise CleanupError(f"Missing Wiki candidate: {candidate_path}") from error
    if not re.search(rf"^- Change id:\s*`?{re.escape(change_id)}`?\s*$", candidate_text, re.MULTILINE):
        raise CleanupError("Candidate Source Change ID does not match requested change")
    fields, paths = approval_fields(candidate_path)
    status = fields.get("status")
    evidence = fields.get("decision evidence")
    source_summary = fields.get("source evidence summary")
    if not is_nonplaceholder(evidence):
        raise CleanupError("Candidate Decision evidence is missing or a placeholder")
    if not is_nonplaceholder(source_summary):
        raise CleanupError("Candidate Source evidence summary is missing or a placeholder")

    updates = fields.get("official wiki updates")
    index_sync = fields.get("wiki index synchronized")
    log_sync = fields.get("wiki log synchronized")
    if status == "approved":
        if not paths or updates == "none":
            raise CleanupError("approved candidate requires at least one official Wiki path")
        if index_sync != "yes" or log_sync != "yes":
            raise CleanupError("approved candidate requires synchronized Wiki index and log")
        index_path = repo_root / ".harness" / "wiki" / "index.md"
        try:
            index_text = index_path.read_text(encoding="utf-8")
        except FileNotFoundError as error:
            raise CleanupError(f"Missing Wiki index: {index_path}") from error
        candidate_reference = f".harness/changes/{change_id}/wiki/candidates.md"
        if candidate_reference in index_text:
            raise CleanupError("Wiki index retains a change-local candidate reference")
        for wiki_path in paths:
            if not wiki_path.startswith(".harness/wiki/"):
                raise CleanupError(f"Official Wiki path is not under .harness/wiki: {wiki_path}")
            page = repo_root / wiki_path
            if not page.is_file():
                raise CleanupError(f"Official Wiki page is missing: {wiki_path}")
            page_text = page.read_text(encoding="utf-8")
            if candidate_reference in page_text:
                raise CleanupError(f"Official Wiki page retains candidate reference: {wiki_path}")
            if wiki_path not in index_text:
                raise CleanupError(f"Wiki index does not list synchronized path: {wiki_path}")
        require_log_evidence(repo_root, change_id, status, paths, "yes")
    elif status == "not-requested":
        if updates != "none" or paths:
            raise CleanupError("not-requested candidate must have Official Wiki updates: none")
        if index_sync != "not-applicable" or log_sync != "yes":
            raise CleanupError("not-requested candidate has invalid synchronization fields")
        require_log_evidence(repo_root, change_id, status, [], "not-applicable")
    else:
        raise CleanupError(f"Candidate approval status is not eligible for cleanup: {status or 'missing'}")


def run_validator(repo_root: Path, change_id: str | None) -> None:
    command = [sys.executable, str(repo_root / ".harness" / "tools" / "validate_change.py"), "--repo", str(repo_root)]
    if change_id:
        command.extend(["--change", change_id])
    else:
        command.append("--all")
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        output = (result.stdout + result.stderr).strip()
        raise CleanupError(f"Validator precheck failed for {change_id or 'all changes'}:\n{output}")


def cleanup(repo_root: Path, change_id: str) -> None:
    index_path = repo_root / ".harness" / "changes" / "INDEX.md"
    lines, rows = parse_index(index_path)
    requested = [row for row in rows if row.change == change_id]
    if not requested:
        raise CleanupError(f"Change is not listed in INDEX.md: {change_id}")
    done_rows = [row for row in rows if row.status == "done"]
    if len(done_rows) <= DONE_LIMIT:
        raise CleanupError(f"Done retention limit not exceeded ({len(done_rows)} <= {DONE_LIMIT})")
    target = requested[0]
    if target.status != "done":
        raise CleanupError(f"Change is not done: {change_id}")
    if target != done_rows[0]:
        raise CleanupError(f"Change is not the oldest done Registry entry: {change_id}")
    if target.resume_point != "none":
        raise CleanupError(f"Done change Resume point must be none: {target.resume_point}")

    change_dir = repo_root / ".harness" / "changes" / change_id
    if not change_dir.is_dir():
        raise CleanupError(f"Change directory is missing: {change_dir}")
    summary = parse_summary_fields(change_dir / "summary.md")
    if summary.get("状态") != target.status:
        raise CleanupError("summary status does not match INDEX status")
    if summary.get("Resume point") != target.resume_point:
        raise CleanupError("summary Resume point does not match INDEX")

    validate_wiki_sync(repo_root, change_id, change_dir / "wiki" / "candidates.md")
    run_validator(repo_root, change_id)

    # All preconditions passed; now make the only two persistent cleanup changes.
    index_path.write_text("".join(line for line in lines if line != target.raw_line), encoding="utf-8")
    shutil.rmtree(change_dir)

    try:
        run_validator(repo_root, None)
    except CleanupError as error:
        raise CleanupError(f"Cleanup completed, but post-cleanup validation failed: {error}") from error


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Retire the oldest excess done Harness change.")
    parser.add_argument("--change", required=True, help="Done change ID to retire after Wiki synchronization.")
    args = parser.parse_args(argv)
    repo_root = find_repo_root(Path.cwd())
    try:
        cleanup(repo_root, args.change)
    except CleanupError as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 1
    print(f"PASS: Retired done change `{args.change}` after verified Wiki synchronization.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
