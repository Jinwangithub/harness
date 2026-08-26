#!/usr/bin/env python3
"""Generate the canonical business Wiki index from approved pages."""

import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

CANONICAL_KINDS = {"project", "domain", "module", "integration"}
CANONICAL_DIRS = {"project", "domains", "modules", "integrations"}
PLACEHOLDER_RE = re.compile(r"\{[^}\n]+\}")


def find_repo_root(start):
    current = Path(start).resolve()
    for candidate in [current] + list(current.parents):
        if (candidate / ".harness" / "changes" / "INDEX.md").exists():
            return candidate
    return current


def _scalar(value):
    value = value.strip()
    if value.startswith(("'", '"')) and value.endswith(value[0]):
        return value[1:-1]
    return value


def parse_frontmatter(text):
    """Parse the supported YAML subset, including source and approval mappings."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    raw = text[4:end]
    body = text[end + 4:].lstrip("\n")
    result = {}
    section = None
    item = None
    for number, line in enumerate(raw.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        if indent == 2 and stripped.startswith("- "):
            if section not in {"modules", "integrations", "tags", "sources"}:
                raise ValueError("line %d: list item without supported list key" % number)
            value = stripped[2:]
            if section == "sources":
                if ":" not in value:
                    raise ValueError("line %d: source item must be a mapping" % number)
                key, value = value.split(":", 1)
                item = {key.strip(): _scalar(value)}
                result[section].append(item)
            else:
                result[section].append(_scalar(value))
            continue
        if indent == 4 and section == "sources" and item is not None:
            if ":" not in stripped:
                raise ValueError("line %d: expected source field" % number)
            key, value = stripped.split(":", 1)
            item[key.strip()] = _scalar(value)
            continue
        if indent == 2 and section == "approval":
            if ":" not in stripped:
                raise ValueError("line %d: expected approval field" % number)
            key, value = stripped.split(":", 1)
            result[section][key.strip()] = _scalar(value)
            continue
        if indent != 0 or ":" not in line:
            raise ValueError("line %d: unsupported YAML structure" % number)
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError("line %d: empty key" % number)
        section = key
        item = None
        if value == "":
            if key in {"modules", "integrations", "tags", "sources"}:
                result[key] = []
            elif key == "approval":
                result[key] = {}
            else:
                result[key] = ""
        elif value.startswith("[") and value.endswith("]"):
            result[key] = [_scalar(part) for part in value[1:-1].split(",") if part.strip()]
        else:
            result[key] = _scalar(value)
    return result, body


def canonical_path(repo_root, page):
    return ".harness/wiki/" + str(page.relative_to(repo_root / ".harness" / "wiki")).replace("\\", "/")


def collect_wiki_pages(wiki_dir):
    pages = []
    for page in sorted(wiki_dir.rglob("*.md")):
        rel = page.relative_to(wiki_dir)
        if not rel.parts or rel.parts[0] not in CANONICAL_DIRS:
            continue
        if rel.name.startswith("_"):
            continue
        try:
            frontmatter, body = parse_frontmatter(page.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise ValueError("%s: %s" % (page, error))
        if frontmatter.get("status") != "approved":
            continue
        if PLACEHOLDER_RE.search(page.read_text(encoding="utf-8")):
            raise ValueError("approved page contains placeholder: %s" % canonical_path(wiki_dir.parent.parent, page))
        kind = frontmatter.get("kind")
        if kind not in CANONICAL_KINDS:
            raise ValueError("approved page has invalid kind: %s" % page)
        frontmatter["_path"] = canonical_path(wiki_dir.parent.parent, page)
        frontmatter["_body"] = body
        pages.append(frontmatter)
    return pages


def _items(page, key):
    value = page.get(key, [])
    return value if isinstance(value, list) else [value]


def _link(path):
    return "[{}]({})".format(path.rsplit("/", 1)[-1], path.split(".harness/wiki/", 1)[-1])


def generate_index(wiki_dir, index_path):
    pages = collect_wiki_pages(wiki_dir)
    module_map = defaultdict(list)
    domain_map = defaultdict(list)
    integration_map = defaultdict(list)
    tags = defaultdict(list)
    for page in pages:
        path = page["_path"]
        for module in _items(page, "modules"):
            module_map[str(module)].append(path)
        if page.get("domain"):
            domain_map[str(page["domain"])].append(path)
        for integration in _items(page, "integrations"):
            integration_map[str(integration)].append(path)
        for tag in _items(page, "tags"):
            tags[str(tag)].append(path)

    lines = ["# Wiki Index", "", "> 由 `generate_wiki_index.py` 自动生成。路径均为 canonical repo-relative path。", ""]
    lines += ["## Module → Wiki", "", "| Module | Pages |", "|---|---|"]
    for key in sorted(module_map):
        lines.append("| `{}` | {} |".format(key, ", ".join(_link(path) for path in sorted(set(module_map[key])))))
    lines += ["", "## Domain → Wiki", "", "| Domain | Pages |", "|---|---|"]
    for key in sorted(domain_map):
        lines.append("| `{}` | {} |".format(key, ", ".join(_link(path) for path in sorted(set(domain_map[key])))))
    lines += ["", "## Integration → Wiki", "", "| Integration | Pages |", "|---|---|"]
    for key in sorted(integration_map):
        lines.append("| `{}` | {} |".format(key, ", ".join(_link(path) for path in sorted(set(integration_map[key])))))
    lines += ["", "## Tags", "", "| Tag | Pages |", "|---|---|"]
    for key in sorted(tags):
        lines.append("| `{}` | {} |".format(key, ", ".join(_link(path) for path in sorted(set(tags[key])))))
    if not pages:
        lines += ["", "_暂无已批准正式页面。_", ""]
    return "\n".join(lines) + "\n"


def main(argv=None):
    repo_root = find_repo_root(Path.cwd())
    wiki_dir = repo_root / ".harness" / "wiki"
    try:
        content = generate_index(wiki_dir, wiki_dir / "index.md")
        (wiki_dir / "index.md").write_text(content, encoding="utf-8")
    except (OSError, ValueError) as error:
        print("ERROR: %s" % error, file=sys.stderr)
        return 1
    print("Generated: .harness/wiki/index.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
