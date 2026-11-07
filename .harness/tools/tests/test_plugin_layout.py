#!/usr/bin/env python3
"""Checks the Claude Code and Codex plugin entry points."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class PluginLayoutTests(unittest.TestCase):
    def load_json(self, relative_path: str) -> dict:
        with (ROOT / relative_path).open(encoding="utf-8") as manifest_file:
            return json.load(manifest_file)

    def test_claude_plugin_and_marketplace_point_to_this_repository(self) -> None:
        plugin = self.load_json(".claude-plugin/plugin.json")
        marketplace = self.load_json(".claude-plugin/marketplace.json")

        self.assertEqual(plugin["name"], "harness")
        self.assertTrue((ROOT / "skills" / "harness" / "SKILL.md").is_file())
        self.assertTrue((ROOT / "agents" / "orchestrator.md").is_file())
        self.assertTrue((ROOT / "commands" / "start.md").is_file())
        self.assertTrue((ROOT / "commands" / "harness.md").is_file())
        self.assertTrue((ROOT / "commands" / "spec.md").is_file())
        self.assertTrue((ROOT / "commands" / "plan.md").is_file())
        self.assertTrue((ROOT / "commands" / "build.md").is_file())
        self.assertTrue((ROOT / "commands" / "review.md").is_file())
        self.assertTrue((ROOT / "commands" / "test.md").is_file())
        self.assertTrue((ROOT / "commands" / "ship.md").is_file())
        self.assertEqual(marketplace["plugins"][0]["name"], plugin["name"])
        self.assertEqual(marketplace["plugins"][0]["source"]["url"], plugin["repository"] + ".git")

    def test_codex_plugin_exposes_the_shared_skills(self) -> None:
        plugin = self.load_json(".codex-plugin/plugin.json")
        marketplace = self.load_json(".agents/plugins/marketplace.json")
        skills_path = plugin["skills"].removeprefix("./")

        self.assertEqual(plugin["name"], "harness")
        self.assertTrue((ROOT / skills_path / "harness" / "SKILL.md").is_file())
        self.assertEqual(marketplace["plugins"][0]["name"], plugin["name"])
        self.assertEqual(marketplace["plugins"][0]["source"]["path"], ".")

    def test_host_skill_and_role_prompts_resolve_to_canonical_sources(self) -> None:
        self.assertTrue((ROOT / "skills").is_symlink())
        self.assertEqual((ROOT / "skills").resolve(), (ROOT / ".harness/skills").resolve())
        self.assertTrue((ROOT / "agents").is_symlink())
        self.assertEqual((ROOT / "agents").resolve(), (ROOT / ".harness/agents").resolve())


if __name__ == "__main__":
    unittest.main()
