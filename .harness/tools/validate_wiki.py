#!/usr/bin/env python3
"""Fail-closed validation for formal Wiki pages and generated index."""

import argparse
import datetime
import re
import sys
from pathlib import Path

from generate_wiki_index import CANONICAL_DIRS, CANONICAL_KINDS, PLACEHOLDER_RE, collect_wiki_pages, generate_index, find_repo_root

REQUIRED = {"title", "kind", "domain", "status", "updated", "sources", "approval"}
VALID_STATUS = {"approved", "deprecated"}
RAW_DIR = "raw"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CANONICAL_RE = re.compile(r"^\.harness/wiki/(project|domains|modules|integrations)/[^/]+\.md$")


def canonical(repo_root, path):
    return ".harness/wiki/" + str(path.relative_to(repo_root / ".harness" / "wiki")).replace("\\", "/")


def validate_page(repo_root, page):
    issues = []
    text = page.read_text(encoding="utf-8")
    try:
        frontmatter, _ = __import__("generate_wiki_index").parse_frontmatter(text)
    except ValueError as error:
        return ["%s: %s" % (canonical(repo_root, page), error)]
    path = canonical(repo_root, page)
    missing = REQUIRED - set(frontmatter)
    issues.extend("%s: missing frontmatter `%s`" % (path, key) for key in sorted(missing))
    if frontmatter.get("kind") not in CANONICAL_KINDS:
        issues.append("%s: invalid kind" % path)
    if frontmatter.get("status") not in VALID_STATUS:
        issues.append("%s: invalid status" % path)
    updated = frontmatter.get("updated", "")
    if not DATE_RE.fullmatch(str(updated)):
        issues.append("%s: invalid updated date" % path)
    else:
        try:
            datetime.datetime.strptime(updated, "%Y-%m-%d")
        except ValueError:
            issues.append("%s: invalid calendar date" % path)
    if not isinstance(frontmatter.get("modules", []), list):
        issues.append("%s: modules must be a list" % path)
    sources = frontmatter.get("sources")
    if not isinstance(sources, list) or not sources or any(not isinstance(item, dict) or not item.get("change_id") or not item.get("evidence") for item in sources):
        issues.append("%s: sources must contain change_id and evidence" % path)
    approval = frontmatter.get("approval")
    if not isinstance(approval, dict) or not approval.get("log_ref"):
        issues.append("%s: approval.log_ref is required" % path)
    if PLACEHOLDER_RE.search(text):
        issues.append("%s: placeholder found" % path)
    if not page.name.startswith("_") and (page.parent.name not in CANONICAL_DIRS or page.parent.parent.name != "wiki"):
        issues.append("%s: non-canonical Wiki directory or nested page" % path)
    if page.parent.name in CANONICAL_DIRS and frontmatter.get("kind"):
        expected_kind = {"project": "project", "domains": "domain", "modules": "module", "integrations": "integration"}[page.parent.name]
        if frontmatter.get("kind") != expected_kind:
            issues.append("%s: kind does not match canonical directory" % path)
    return issues


def validate_index(repo_root, wiki_dir):
    expected = generate_index(wiki_dir, wiki_dir / "index.md")
    actual = (wiki_dir / "index.md").read_text(encoding="utf-8") if (wiki_dir / "index.md").exists() else ""
    return [] if actual == expected else ["index.md: stale; regenerate with generate_wiki_index.py"]


def validate_log(repo_root, pages):
    log = repo_root / ".harness" / "wiki" / "log.md"
    if not log.exists():
        return ["log.md: missing"]
    text = log.read_text(encoding="utf-8")
    issues = []
    for page in pages:
        approval = page.get("approval", {})
        ref = approval.get("log_ref", "") if isinstance(approval, dict) else ""
        if ref and ref not in text and ref.split("#", 1)[-1] not in text:
            issues.append("%s: approval log reference not found" % page["_path"])
    return issues


def lint_report(repo_root, pages):
    """Report evidence, link, conflict, and orphan findings without mutation."""
    wiki_dir = repo_root / ".harness" / "wiki"
    indexed_paths = {page["_path"] for page in pages}
    for page in pages:
        text = page.get("_body", "")
        for target in re.findall(r"\]\(([^)#]+)(?:#[^)]+)?\)", text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            target_path = (wiki_dir / target).resolve()
            if not target_path.exists():
                print("WARN: broken Wiki link: %s -> %s" % (page["_path"], target))
        if re.search(r"\b(disputed|outdated|conflict)\b", text, re.IGNORECASE):
            print("WARN: conflict/outdated marker requires review: %s" % page["_path"])
        if not page.get("sources"):
            print("WARN: missing evidence source: %s" % page["_path"])
    for page in sorted(wiki_dir.rglob("*.md")):
        rel = page.relative_to(wiki_dir)
        if rel.parts and rel.parts[0] in CANONICAL_DIRS and not page.name.startswith("_"):
            path = ".harness/wiki/" + str(rel).replace("\\", "/")
            if path not in indexed_paths:
                print("WARN: canonical page is orphaned from generated index: %s" % path)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate formal Harness Wiki and generated index.")
    parser.add_argument("--repo", type=Path, default=None)
    args = parser.parse_args(argv)
    repo_root = args.repo.resolve() if args.repo else find_repo_root(Path.cwd())
    wiki_dir = repo_root / ".harness" / "wiki"
    issues = []
    raw_root = wiki_dir / RAW_DIR
    raw_dirs = sorted(path for path in raw_root.iterdir() if path.is_dir()) if raw_root.exists() else []
    for raw_dir in raw_dirs:
        content = raw_dir / "content.md"
        metadata = raw_dir / "metadata.yml"
        raw_path = ".harness/wiki/" + str(raw_dir.relative_to(wiki_dir)).replace("\\", "/")
        if not content.exists() or not metadata.exists():
            issues.append("%s: raw capture requires content.md and metadata.yml" % raw_path)
            continue
        raw_text = metadata.read_text(encoding="utf-8")
        required = {"source_id", "origin", "uri", "captured_at", "content_sha256", "provenance", "supersedes"}
        fields = {line.split(":", 1)[0].strip() for line in raw_text.splitlines() if ":" in line and not line.lstrip().startswith("#")}
        for field in sorted(required - fields):
            issues.append("%s/metadata.yml: raw metadata missing `%s`" % (raw_path, field))
        digest = re.search(r"^content_sha256:\s*([0-9a-f]{64})\s*$", raw_text, re.MULTILINE)
        import hashlib
        actual_digest = hashlib.sha256(content.read_bytes()).hexdigest()
        if not digest or digest.group(1) != actual_digest:
            issues.append("%s/metadata.yml: content_sha256 does not match content.md" % raw_path)

    for page in sorted(wiki_dir.rglob("*.md")):
        if page.name in {"README.md", "index.md", "log.md"} or page.name.startswith("_"):
            continue
        rel = page.relative_to(wiki_dir)
        if not rel.parts or rel.parts[0] == RAW_DIR:
            continue
        if rel.parts[0] not in CANONICAL_DIRS:
            print("WARN: non-canonical Wiki artifact retained outside index: %s" % canonical(repo_root, page))
            continue
        try:
            frontmatter, _ = __import__("generate_wiki_index").parse_frontmatter(page.read_text(encoding="utf-8"))
        except ValueError:
            issues.extend(validate_page(repo_root, page))
            continue
        if frontmatter.get("status") not in {"approved", "deprecated"}:
            print("WARN: non-formal Wiki page excluded from index: %s" % canonical(repo_root, page))
            continue
        issues.extend(validate_page(repo_root, page))
    try:
        pages = collect_wiki_pages(wiki_dir)
    except ValueError as error:
        issues.append(str(error))
        pages = []
    if not issues:
        issues.extend(validate_index(repo_root, wiki_dir))
    issues.extend(validate_log(repo_root, pages))
    lint_report(repo_root, pages)
    if issues:
        for issue in issues:
            print("FAIL: %s" % issue)
        return 1
    print("PASS: Wiki validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
