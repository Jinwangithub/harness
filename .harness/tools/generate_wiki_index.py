#!/usr/bin/env python3
"""Generate wiki/index.md from wiki/ page frontmatter.

Scans .harness/wiki/ for non-_ prefixed .md files, parses YAML frontmatter,
and writes a structured index.md with Module->Wiki mapping and per-domain sections.

Usage:
    python3 .harness/tools/generate_wiki_index.py
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".harness" / "changes" / "INDEX.md").exists():
            return candidate
    return current


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter block between --- markers."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_text = parts[1].strip()
    body = parts[2].strip()
    fm: dict[str, Any] = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if value.startswith("[") and value.endswith("]"):
                items = [v.strip().strip("'\"") for v in value[1:-1].split(",") if v.strip()]
                fm[key] = items
            elif value.startswith("{") and value.endswith("}"):
                items = [v.strip().strip("'\"") for v in value[1:-1].split(",") if v.strip()]
                fm[key] = items
            else:
                fm[key] = value.strip("'\"")
    return fm, body


def collect_wiki_pages(wiki_dir: Path) -> list[dict[str, Any]]:
    """Scan wiki/ for all non-_ prefixed .md files, return page info."""
    pages: list[dict[str, Any]] = []
    for md_file in sorted(wiki_dir.rglob("*.md")):
        rel = md_file.relative_to(wiki_dir)
        if rel.parts[0].startswith("_") or any(p.startswith("_") for p in rel.parts):
            continue
        if rel.name in ("README.md", "INDEX.md", "index.md", "log.md"):
            continue
        text = md_file.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        fm["_path"] = str(rel)
        pages.append(fm)
    return pages


def build_module_map(pages: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Build Module->Wiki mapping rows."""
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for page in pages:
        modules = page.get("modules", [])
        if isinstance(modules, str):
            modules = [modules]
        domain = page.get("domain", "unknown")
        path = page.get("_path", "")
        for mod in modules:
            key = (str(mod), str(domain), str(path))
            if key not in seen:
                seen.add(key)
                rows.append({"module": str(mod), "domain": str(domain), "page": str(path)})
    return rows


def group_by_domain(pages: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group pages by domain."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for page in pages:
        domain = page.get("domain", "unknown")
        groups[str(domain)].append(page)
    return dict(sorted(groups.items()))


def generate_index(wiki_dir: Path, index_path: Path) -> str:
    """Generate index.md content."""
    pages = collect_wiki_pages(wiki_dir)
    module_rows = build_module_map(pages)
    domain_groups = group_by_domain(pages)

    lines: list[str] = []
    lines.append("# Wiki Index")
    lines.append("")
    lines.append("> 由 `generate_wiki_index.py` 自动生成。不要手工编辑此文件。")
    lines.append("")

    # Module -> Wiki mapping
    lines.append("## Module → Wiki 映射")
    lines.append("")
    if module_rows:
        lines.append("| 代码模块 | 所属业务域 | 相关 Wiki 页面 |")
        lines.append("|----------|-----------|---------------|")
        for row in module_rows:
            lines.append(f"| {row['module']} | {row['domain']} | {row['page']} |")
    else:
        lines.append("| 代码模块 | 所属业务域 | 相关 Wiki 页面 |")
        lines.append("|----------|-----------|---------------|")
    lines.append("")

    # Per-domain sections
    lines.append("## 按业务域")
    lines.append("")
    if domain_groups:
        for domain, domain_pages in domain_groups.items():
            lines.append(f"### {domain}")
            lines.append("")
            lines.append("| 页面 | 类型 | 标题 |")
            lines.append("|------|------|------|")
            for page in domain_pages:
                title = page.get("title", page.get("_path", ""))
                ptype = page.get("type", "")
                ppath = page.get("_path", "")
                lines.append(f"| {ppath} | {ptype} | {title} |")
            lines.append("")
    else:
        lines.append("---")
        lines.append("")
        lines.append("_暂无已批准条目。运行 `python3 .harness/tools/generate_wiki_index.py` 生成索引。_")
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    repo_root = find_repo_root(Path.cwd())
    wiki_dir = repo_root / ".harness" / "wiki"
    index_path = wiki_dir / "index.md"

    if not wiki_dir.exists():
        print(f"ERROR: wiki directory not found: {wiki_dir}", file=sys.stderr)
        return 1

    content = generate_index(wiki_dir, index_path)
    index_path.write_text(content, encoding="utf-8")
    rel = index_path.relative_to(repo_root)
    print(f"Generated: {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
