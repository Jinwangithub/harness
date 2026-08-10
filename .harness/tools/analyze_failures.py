#!/usr/bin/env python3
"""Analyze gate failure patterns across completed changes.

Scans done changes for recurring validator issue codes, groups them into
deterministic pattern signatures, and writes evolution candidates for human
review.

Usage:
  python3 .harness/tools/analyze_failures.py [--repo ROOT] [--min-occurrence N] [--dry-run]
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from collections import defaultdict
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
from typing import Optional

# Reuse primitives from validate_change
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_change import find_repo_root, INDEX_ROW_RE, Validator  # noqa: E402

# -- static mapping: validator code → (action_type, target_file) ----------
CODE_ACTION_MAP: dict[str, tuple[str, str]] = {
    "gate.evidence_missing": ("rule-update", "gates.md"),
    "gate.pass_without_evidence": ("rule-update", "gates.md"),
    "gate.artifact_missing": ("skill-update", "gates.md"),
    "gate.mechanical_invalid": ("rule-update", "gates.md"),
    "gate.final_mechanical_not_pass": ("validator-update", "validate_change.py"),
    "gate.final_approval_not_approved": ("rule-update", "orchestrator.md"),
    "summary.field_missing": ("rule-update", "templates.md"),
    "artifact.missing": ("skill-update", "templates.md"),
    "artifact.forbidden": ("skill-update", "templates.md"),
    "index.multiple_active": ("rule-update", "structure.md"),
    "wiki.candidates_missing": ("rule-update", "gates.md"),
}
# -------------------------------------------------------------------------

GATE_RECORD_RE = re.compile(
    r"^## Gate Record\s*[—\-]\s*(.+?)\s*$([\s\S]*?)(?=^##\s+|\Z)",
    re.MULTILINE,
)
SIGNATURE_RE = re.compile(r"### Candidate \d+: .+ — (.+)")
LOG_DECISION_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}\s*\|\s*(approved|rejected|deferred)\s*\|\s*(.+?)\s*$"
)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def compute_signature(issue_codes: list[str]) -> Optional[str]:
    """Deterministic pattern signature: sorted unique codes joined by '-'."""
    codes = sorted(set(issue_codes))
    if codes:
        return "-".join(codes)
    return None


def compute_fallback_signature(change_dir: Path) -> Optional[str]:
    """Fallback signature from Mechanical Gate + phase label when no codes."""
    summary_path = change_dir / "summary.md"
    if not summary_path.exists():
        return None

    text = summary_path.read_text(encoding="utf-8")
    for match in GATE_RECORD_RE.finditer(text):
        label = match.group(1).strip()
        body = match.group(2)
        mechanical = _extract_bullet(body, "Mechanical Gate")
        if mechanical in ("fail", "blocked"):
            return f"{mechanical}-{label}"
    return None


def _extract_bullet(text: str, name: str) -> Optional[str]:
    m = re.search(
        rf"^\s*-\s*{re.escape(name)}:\s*(.*?)\s*$", text, re.MULTILINE | re.IGNORECASE
    )
    return m.group(1).strip() if m else None


def parse_log_approved_signatures(log_path: Path) -> set[str]:
    """Return set of pattern signatures that have been approved in log.md."""
    approved: set[str] = set()
    if not log_path.exists():
        return approved
    for line in log_path.read_text(encoding="utf-8").splitlines():
        m = LOG_DECISION_RE.match(line.strip())
        if m and m.group(1) == "approved":
            approved.add(m.group(2).strip())
    return approved


def compute_severity(change_count: int, signature: str) -> str:
    if change_count >= 4:
        return "critical"
    if change_count >= 3:
        return "high"
    # medium when 2+ changes share exactly one code
    if change_count >= 2 and "-" not in signature:
        return "medium"
    return "low"


# ---------------------------------------------------------------------------
# core logic
# ---------------------------------------------------------------------------

def collect_issue_codes_for_change(
    repo_root: Path, change_id: str
) -> list[str]:
    """Run validator for a single change and return issue codes."""
    # suppress stdout from validate_change's print_report()
    with redirect_stdout(io.StringIO()):
        v = Validator(repo_root, include_done=True)
        v.validate(requested_change=change_id)
    return [issue.code for issue in v.issues if issue.level == "FAIL"]


def run(repo_root: Path, min_occurrence: int) -> dict:
    """Main analysis: returns analysis result dictionary."""
    harness_dir = repo_root / ".harness"
    changes_dir = harness_dir / "changes"
    index_path = changes_dir / "INDEX.md"
    evolution_dir = harness_dir / "evolution"
    log_path = evolution_dir / "log.md"

    # ---- 1. read done changes from INDEX --------------------------------
    if not index_path.exists():
        return {"status": "no_index", "patterns": []}

    done_changes: list[str] = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped or "Change" in stripped:
            continue
        m = INDEX_ROW_RE.match(stripped)
        if not m:
            continue
        change, status = [p.strip() for p in m.groups()[:2]]
        if status == "done":
            done_changes.append(change)

    if not done_changes:
        return {"status": "no_done_changes", "patterns": []}

    # ---- 2. scan each done change ---------------------------------------
    change_codes: dict[str, list[str]] = {}
    skipped: list[str] = []

    for change_id in done_changes:
        change_dir = changes_dir / change_id
        if not change_dir.exists():
            print(f"WARN: Change directory not found, skipping: {change_id}")
            skipped.append(change_id)
            continue

        try:
            codes = collect_issue_codes_for_change(repo_root, change_id)
        except Exception:
            print(f"WARN: Validator error for {change_id}, skipping.")
            skipped.append(change_id)
            continue

        if codes:
            change_codes[change_id] = codes

    if not change_codes:
        return {"status": "no_failures", "patterns": []}

    # ---- 3. group by pattern signature ----------------------------------
    change_signature: dict[str, str] = {}
    for cid, codes in change_codes.items():
        sig = compute_signature(codes)
        if not sig:
            # fallback
            sig = compute_fallback_signature(changes_dir / cid)
        if sig:
            change_signature[cid] = sig

    pattern_groups: dict[str, list[str]] = defaultdict(list)
    for cid, sig in change_signature.items():
        pattern_groups[sig].append(cid)

    # ---- 4. filter by occurrence threshold ------------------------------
    filtered = {
        sig: changes
        for sig, changes in pattern_groups.items()
        if len(changes) >= min_occurrence
    }

    if not filtered:
        return {"status": "below_threshold", "patterns": []}

    # ---- 5. exclude already-approved patterns ---------------------------
    approved_sigs = parse_log_approved_signatures(log_path)

    patterns = []
    for sig, changes in sorted(filtered.items()):
        if sig in approved_sigs:
            continue
        codes = sig.split("-")
        primary = codes[0]
        action_type, target_file = CODE_ACTION_MAP.get(
            primary, ("rule-update", "gates.md")
        )
        severity = compute_severity(len(changes), sig)

        patterns.append({
            "signature": sig,
            "severity": severity,
            "action_type": action_type,
            "target_file": target_file,
            "change_count": len(changes),
            "changes": sorted(changes),
            "codes": codes,
        })

    if not patterns:
        return {"status": "all_addressed", "patterns": []}

    return {
        "status": "patterns_found",
        "patterns": patterns,
        "total_scanned": len(done_changes) - len(skipped),
        "failed_count": len(change_codes),
    }


# ---------------------------------------------------------------------------
# output helpers
# ---------------------------------------------------------------------------

def _target_path(target_file: str) -> str:
    if target_file.endswith(".py"):
        return f".harness/tools/{target_file}"
    if target_file.endswith(".md"):
        return f".harness/rules/{target_file}"
    return f".harness/{target_file}"


def print_dry_run_result(result: dict) -> None:
    patterns = result.get("patterns", [])
    if patterns:
        print(
            f"WARN: Found {len(patterns)} candidate pattern(s) for "
            f"self-evolution:\n"
        )
    for i, c in enumerate(patterns, 1):
        print(f"  Candidate {i}: {c['severity']}  —  {c['signature']}")
        print(f"    Action: {c['action_type']}  →  {_target_path(c['target_file'])}")
        print(f"    Distinct changes: {c['change_count']} ({', '.join(c['changes'])})")
        print(f"    Codes: {', '.join(c['codes'])}")
        print()
    if patterns:
        print("WARN: Evolution analysis complete.")


def write_candidates_md(repo_root: Path, result: dict) -> None:
    """Write (merge-preserving) candidates.md."""
    evolution_dir = repo_root / ".harness" / "evolution"
    if not evolution_dir.exists():
        evolution_dir.mkdir(parents=True, exist_ok=True)

    candidates_path = evolution_dir / "candidates.md"
    patterns = result.get("patterns", [])
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # read existing pending signatures to preserve
    existing_pending: dict[str, str] = {}
    if candidates_path.exists():
        text = candidates_path.read_text(encoding="utf-8")
        cur_sig = None
        cur_block: list[str] = []
        in_candidate = False
        for line in text.splitlines():
            sig_m = SIGNATURE_RE.search(line)
            if sig_m:
                if cur_sig and cur_block:
                    existing_pending[cur_sig] = "\n".join(cur_block)
                cur_sig = sig_m.group(1)
                cur_block = [line]
                in_candidate = True
            elif in_candidate:
                cur_block.append(line)
        if cur_sig and cur_block:
            existing_pending[cur_sig] = "\n".join(cur_block)

    total_scanned = result.get("total_scanned", 0)
    failed_count = result.get("failed_count", 0)

    content = f"""# Self-Evolution Candidates

> 本文件由 `analyze_failures.py` 自动生成和更新。每个 candidate 代表一个跨变更反复出现的 failure pattern。
> 人工审查后按 `.harness/rules/evolution.md` 处理。

## Analysis Metadata

- Last analysis: {now}
- Changes scanned: {total_scanned}
- Changes with failures: {failed_count}
- New patterns found: {len(patterns)}
- Existing patterns (still pending): 0

## Candidates

"""
    for i, c in enumerate(patterns, 1):
        sig = c["signature"]
        content += f"""### Candidate {i}: {c['severity']} — {c['signature']}
- Severity: {c['severity']}
- Action type: {c['action_type']}
- Target file: {_target_path(c['target_file'])}
- Distinct change count: {c['change_count']}
- Change IDs: {', '.join(c['changes'])}
- Pattern: Recurring failure with codes {', '.join(c['codes'])}
- Suggested fix: Review the rule, skill, or validator referenced by the action type and target file.

## Human Evolution Approval
- Status: pending
- Decision evidence: none
- Applied at: N/A
- Snapshot saved: N/A

"""

    candidates_path.write_text(content, encoding="utf-8")
    print(
        f"WARN: Wrote {len(patterns)} candidate pattern(s) to {candidates_path}"
    )


# ---------------------------------------------------------------------------
# cli
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Analyze gate failure patterns across completed changes."
    )
    parser.add_argument(
        "--repo", type=Path, default=None,
        help="Repository root. Defaults to nearest parent with .harness/changes/INDEX.md.",
    )
    parser.add_argument(
        "--min-occurrence", type=int, default=2,
        help="Minimum distinct changes for a pattern to be reported (default: 2).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Output to stdout only, do not write candidates.md.",
    )
    args = parser.parse_args(argv)

    repo_root = (
        args.repo.resolve() if args.repo else find_repo_root(Path.cwd())
    )

    try:
        result = run(repo_root, args.min_occurrence)
    except Exception as exc:
        print(f"ERROR: Analysis failed: {exc}", file=sys.stderr)
        return 1

    status = result["status"]

    if status == "no_index":
        print("WARN: No changes to analyze (INDEX.md not found).")
        return 0
    if status == "no_done_changes":
        print("PASS: No failure patterns to analyze (no done changes).")
        return 0
    if status == "no_failures":
        print("PASS: No failure patterns to analyze (no gate fail/blocked in done changes).")
        return 0
    if status == "below_threshold":
        print(
            f"WARN: No patterns meet minimum occurrence threshold "
            f"({args.min_occurrence})."
        )
        return 0
    if status == "all_addressed":
        print("PASS: All detected patterns are already addressed or pending approval.")
        return 0

    # patterns found
    if args.dry_run:
        print_dry_run_result(result)
    else:
        write_candidates_md(repo_root, result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
