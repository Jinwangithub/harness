---
name: harness
description: Use when starting, resuming, or checking a software engineering change with the Harness workflow, including Lite or Standard flow classification, change artifacts, mechanical gates, and verification.
---

# Harness Workflow

Use this skill as the entry point for the Harness plugin.

## Source And Output Boundaries

- This skill and the bundled `agents/`, `rules/`, `skills/`, `changes/templates.md`, and `tools/` are read-only plugin sources. Resolve them from this loaded skill's installed plugin path; never look for their copies in the consumer project.
- Resolve symlinks before computing the plugin root. When the host does not provide a plugin root, walk the ancestors of this loaded Skill until finding `.harness/tools/validate_change.py`; use that directory as `<plugin-root>`.
- The consumer project is the current workspace. Harness output is limited to `docs/harness/{change-id}/` task artifacts. Do not create project-level `.harness/`, `INDEX.md`, `memory/`, `rules/`, `agents/`, `skills/`, `tools/`, `AGENTS.md`, or `CLAUDE.md` as a prerequisite.
- Keep workflow definitions, role prompts, and verification tools in the plugin. Keep task-specific summaries, plans, reports, and delivery records in the consumer project's `docs/harness/{change-id}/` directory.

## Startup

1. Resolve the installed plugin source path and read its `agents/orchestrator.md`.
2. Treat the current workspace as the consumer project root. Scan `docs/harness/*/summary.md` for matching active work; if multiple active tasks cannot be matched to the user's request, ask which task to resume.
3. For a new task, classify it using the plugin's `rules/flow.md` before writing project files.
4. If there is no existing task artifact, do not create project files until a task requires them.

## Host Adaptation

- In Claude Code, use the installed plugin's source path (or `CLAUDE_PLUGIN_ROOT` when available) for role prompts and tools.
- In Codex, use the source location of this loaded plugin Skill and resolve relative links from the plugin package. Do not derive plugin paths from the consumer workspace.
- For Standard-flow, dispatch the bundled role prompts with fresh subagents when multi-agent support is available. If it is unavailable, report the limitation before a phase that requires isolated dispatch.
- Run validation using the plugin-bundled tool and pass the consumer project explicitly: `python3 <plugin-root>/.harness/tools/validate_change.py --repo <project-root> --change <change-id>`. The validator reads artifacts from `<project-root>/docs/harness/`.
- A skill or plugin prompt does not grant approval to commit, push, deploy, or publish. Follow the user's authorization and workflow gates.

## Routing

- New requirements: read the plugin's `rules/flow.md`, then the selected `rules/flow-lite.md` or `rules/flow-standard.md`.
- Gate decisions: read the plugin's `rules/gates.md`.
- Failures, blocked work, or rollback: read the plugin's `rules/rollback.md`.
- Artifact templates and structure: read the plugin's `changes/templates.md` and `changes/structure.md`.
- Detailed commands and human-facing usage: read the plugin's `USAGE.md` when needed.

The plugin package is the authority for workflow definitions. Files with the same names in the consumer project are ordinary project content and do not override plugin rules.
