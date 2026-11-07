---
name: harness
description: Use when starting, resuming, or checking a software engineering change that should follow this repository's Harness workflow, including Lite or Standard flow classification, change records, mechanical gates, and verification.
---

# Harness Workflow

Use this skill as the entry point for the Harness Engineering workflow in this repository.

## Startup

1. Read `../../agents/orchestrator.md` relative to this skill directory. Treat it as the orchestration contract.
2. Read `../../changes/INDEX.md`, then read the active change's `summary.md` if one exists.
3. Run `python3 .harness/tools/validate_change.py` from the repository root.
4. Read the latest three entries in `../../memory/lessons-learned.md`. Read `../../memory/known-issues.md` when an anomaly is relevant.
5. For new work, classify it using `../../rules/flow.md` before proposing or making changes.

## Host Adaptation

- Follow the shared workflow, artifacts, gates, and safety boundaries in `.harness/` on both Claude Code and Codex.
- In Claude Code, dispatch the role prompts in `../../agents/` with the Agent tool, using a fresh agent for each Standard-flow phase or substep.
- In Codex, dispatch the role prompts in `../../agents/` with Codex subagents when multi-agent support is enabled. If subagents are unavailable, do not run Standard-flow phases that require isolated dispatch; report the blocker and ask the user to enable multi-agent support or choose a workflow that does not require delegation.
- The current repository root is the project root. Store all change records under `.harness/changes/` and run validation with `python3 .harness/tools/validate_change.py --change <change-id>` before each approval gate and before completion.
- A skill or plugin prompt does not grant approval to modify, commit, push, deploy, or publish. Follow the user's authorization and the repository workflow.

## Routing

- New requirements: read `../../rules/flow.md`, then the selected `../../rules/flow-lite.md` or `../../rules/flow-standard.md`.
- Gate decisions: read `../../rules/gates.md`.
- Failures, blocked work, or rollback: read `../../rules/rollback.md`.
- Detailed commands and human-facing usage: read `../../USAGE.md` when needed.

The role prompts and domain skills in this plugin are supporting tools. The `.harness/rules/` and `.harness/changes/` files remain authoritative when instructions differ.
