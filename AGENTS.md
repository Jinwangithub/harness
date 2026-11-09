# Harness Engineering

This repository uses Harness Engineering. Route project work through `.harness/agents/orchestrator.md` and treat `.harness/` as the canonical source for workflow rules, skills, role prompts, change records, and validation.

## Harness Repository Maintenance Exception

When the task changes this Harness plugin itself (its source, rules, Skills, manifests, commands, or tools), edit the plugin directly. Do not run the consumer Harness workflow or create a `.harness/changes/` task record for plugin maintenance.

When this exception applies, ignore the session startup and flow steps below.

At session start:

1. Read `.harness/changes/INDEX.md` and resume the active change, if any.
2. Run `python3 .harness/tools/validate_change.py`.
3. Read the latest three entries in `.harness/memory/lessons-learned.md` and inspect `.harness/memory/known-issues.md` when relevant.
4. Classify new work using `.harness/rules/flow.md`; use the Lite or Standard workflow and gates defined under `.harness/rules/`.

Use the `harness` skill (`$harness`) for explicit entry. For Standard-flow, use the role prompts in `.harness/agents/` with Codex subagents when multi-agent support is enabled; if unavailable, stop before a phase that requires isolation and report the blocker. Keep change artifacts in this repository's `.harness/changes/` and run the validator before each approval gate and before declaring completion.

Do not commit, push, deploy, or publish unless the user explicitly asks.
