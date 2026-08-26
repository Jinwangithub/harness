#!/usr/bin/env python3
"""Create change-local Wiki discovery candidates, never formal Wiki pages."""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

EXCLUDE_DIRS = {".git", ".harness", ".idea", ".claude", ".vscode", "node_modules", "__pycache__", ".venv", "venv", "target", "build", "dist", "coverage"}
SOURCE_EXTS = {".java", ".kt", ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".rb", ".php"}
CHANGE_ID_RE = r"^(feat|fix|refactor|perf|test|docs|chore)-[a-z0-9][a-z0-9-]*-\d{8}$"


def find_repo_root(start):
    current = Path(start).resolve()
    for candidate in [current] + list(current.parents):
        if (candidate / ".harness" / "changes" / "INDEX.md").exists():
            return candidate
    return current


def detect_modules(repo_root):
    found = []
    for root, dirs, files in os.walk(str(repo_root)):
        dirs[:] = [item for item in dirs if item not in EXCLUDE_DIRS and not item.startswith(".")]
        rel = Path(root).relative_to(repo_root)
        if not rel.parts or len(rel.parts) > 3:
            continue
        count = sum(1 for name in files if Path(name).suffix in SOURCE_EXTS)
        if count:
            found.append((str(rel).replace("\\", "/"), count))
    return sorted(found)


def scaffold(repo_root, change_id, output, dry_run=False):
    import re
    if not re.fullmatch(CHANGE_ID_RE, change_id):
        raise ValueError("invalid change ID: %s" % change_id)
    changes = repo_root / ".harness" / "changes" / change_id
    if not changes.is_dir():
        raise ValueError("change directory does not exist: %s" % changes)
    target = (repo_root / output).resolve()
    if target != changes.resolve() and changes.resolve() not in target.parents:
        raise ValueError("output must be inside the requested change directory")
    if target.exists() and any(target.iterdir()):
        raise ValueError("refusing to overwrite non-empty output: %s" % target)
    modules = detect_modules(repo_root)
    lines = [
        "# Business Wiki Candidates", "", "## Source Change",
        "- Change id: `%s`" % change_id,
        "- Flow: {Lite-flow/Standard-flow}",
        "- Source artifacts:",
        "  - none (generated from repository module signals)", "",
        "## Extraction Summary", "",
        "- Status: candidates-found",
        "- Reason: repository source-directory signals require business evidence review.",
        "- Classification: New / Update / Disputed / No material (pending review)", "",
        "## Discovery Signals", "",
    ]
    if modules:
        lines.extend("- `%s` (%d source files)" % item for item in modules)
    else:
        lines.append("- none")
    lines += [
        "", "## Candidates", "",
        "- No formal candidate content is promoted by this scaffold.",
        "- Proposed targets require source evidence and human Wiki decision.", "",
        "## Human Wiki Approval", "",
        "- Status: pending",
        "- Decision evidence: none",
        "- Official Wiki updates: none",
        "- Wiki index regenerated (`generate_wiki_index.py`): not-applicable",
        "- Wiki log synchronized: no",
        "- Source evidence summary: none",
        "", "## Required review",
        "- Confirm module/domain/integration mapping from business evidence.",
        "- Do not copy inferred content into `.harness/wiki/` without a formal candidate decision.", "",
    ]
    content = "\n".join(lines)
    if not dry_run:
        target.mkdir(parents=True, exist_ok=False)
        (target / "candidates.md").write_text(content, encoding="utf-8")
    return {"output": str(target / "candidates.md"), "modules": modules, "dry_run": dry_run}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Write inferred Wiki candidates to a change-local path.")
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--change", required=True)
    parser.add_argument("--output", required=True, help="repo-relative directory inside .harness/changes/{change}; writes wiki/candidates.md")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    repo_root = args.repo.resolve() if args.repo else find_repo_root(Path.cwd())
    try:
        result = scaffold(repo_root, args.change, args.output, args.dry_run)
    except (OSError, ValueError) as error:
        print("REFUSED: %s" % error, file=sys.stderr)
        return 1
    print("Candidate output: %s%s" % (result["output"], " (dry-run)" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
