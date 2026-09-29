#!/usr/bin/env python3
"""Retire one excess completed Harness change after final Delivery Approval."""

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
    parser.add_argument("--change", required=True, help="Done change ID to retire after final Delivery Approval.")
    args = parser.parse_args(argv)
    repo_root = find_repo_root(Path.cwd())
    try:
        cleanup(repo_root, args.change)
    except CleanupError as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 1
    print(f"PASS: Retired done change `{args.change}` after verified final Delivery Approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
