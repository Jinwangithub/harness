#!/usr/bin/env python3
"""Capture a deterministic, read-only filesystem manifest for Phase 4 slices."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path

SCHEMA_VERSION = "phase4-manifest-v2"


def normalized_relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def collect(repo: Path, output: Path) -> dict[str, object]:
    if not repo.is_dir():
        raise ValueError(f"repository is not a directory: {repo}")
    try:
        output_rel = output.relative_to(repo).as_posix()
    except ValueError as exc:
        raise ValueError("output must be inside --repo") from exc

    files: list[dict[str, object]] = []
    for current, directories, names in os.walk(repo, topdown=True, followlinks=False):
        current_path = Path(current)
        kept_dirs: list[str] = []
        for name in sorted(directories):
            child = current_path / name
            rel = normalized_relative(repo, child)
            mode = child.lstat().st_mode
            if rel == ".git":
                continue
            if stat.S_ISLNK(mode):
                raise ValueError(f"symlink is not supported: {rel}")
            if not stat.S_ISDIR(mode):
                raise ValueError(f"unsupported filesystem entry: {rel}")
            kept_dirs.append(name)
        directories[:] = kept_dirs
        for name in sorted(names):
            child = current_path / name
            rel = normalized_relative(repo, child)
            mode = child.lstat().st_mode
            if rel == output_rel:
                continue
            if stat.S_ISLNK(mode):
                raise ValueError(f"symlink is not supported: {rel}")
            if not stat.S_ISREG(mode):
                raise ValueError(f"unsupported filesystem entry: {rel}")
            files.append({"path": rel, "mode": format(stat.S_IMODE(mode), "04o"), "size": child.stat().st_size, "sha256": digest(child)})
    files.sort(key=lambda item: str(item["path"]))
    return {"schema_version": SCHEMA_VERSION, "files": files}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Capture deterministic Phase 4 filesystem manifest.")
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    output = args.output.resolve()
    try:
        manifest = collect(repo, output)
        payload = json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"FAIL: manifest.capture: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
