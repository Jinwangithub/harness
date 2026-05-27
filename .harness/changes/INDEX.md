# Changes Index

This file is the registry-first recovery index for `.harness/changes/`. It records the active resume target and marks legacy conflicts without rewriting historical evidence.

## Active Resolution
- Active change: `.harness/changes/chore-harness-operability-index-validation-20260526/`
- Resume point: Phase 10 用户确认
- Human Approval Gate: pending-human
- Completion lock: locked
- Last verified: 2026-05-26

## Registry

| Change | Lifecycle | Resume policy | Current step | Resume point | Mechanical Gate | Human Approval Gate | Completion lock | Notes |
|--------|-----------|---------------|--------------|--------------|-----------------|---------------------|-----------------|-------|
| chore-harness-operability-index-validation-20260526 | active | auto-resume | Phase 10 | Phase 10 用户确认 | pass | pending-human | locked | current active governance change |
| fix-harness-executability-20260521 | legacy-unfinished | do-not-auto-resume | Phase 10 | Phase 10 用户确认 | pass | pending-human | locked | superseded by operability index/validation governance work; do not mark completed without user approval |
| docs-harness-slimming-20260520 | legacy-unfinished | do-not-auto-resume | L4 | L4 交付确认 | pass | pending-human | locked | superseded/continued by later governance work |
| docs-flow-friction-reduction-20260519 | legacy-conflict | do-not-auto-resume | L4 | status-conflict-review | pass | pending-human | locked | summary says completed while final Human Approval is pending-human |
| feat-harness-evaluation-20260514 | historical | manual-only | unknown | manual review required | unknown | unknown | locked | legacy pre-index archive |

## Lifecycle Semantics

| Lifecycle | Meaning | Auto-resume |
|-----------|---------|-------------|
| `active` | Current change selected by Orchestrator for automatic recovery | yes, only one allowed |
| `legacy-unfinished` | Historical change still marked unfinished or pending human approval | no |
| `legacy-conflict` | Historical summary has contradictory state or non-canonical approval evidence | no |
| `historical` | Older archive kept as evidence | no |
| `superseded` | Replaced by a later governance change | no |
| `manual-only` | Requires explicit user selection before resume | no |

## Maintenance Rules

1. New changes must update this index when created and when reaching delivery.
2. Exactly one row may have `Lifecycle=active` and `Resume policy=auto-resume`.
3. If `Human Approval Gate=pending-human`, `Completion lock` must be `locked`.
4. `状态: 已完成` with `Human Approval Gate=pending-human` is a conflict and must not be auto-resumed as completed.
5. Historical summaries are legacy evidence. Do not rewrite historical approval state to make the index look cleaner.
6. Registry and latest summary conflict must Stop-the-Line; Orchestrator must report candidates and ask for explicit resolution instead of guessing.
7. 超过 90 天且 Lifecycle != `active` 的行，自动降级为 `archived`，不再参与恢复逻辑。
8. `archived` 行移入本文件底部独立 `## Archive` 区块，不影响主 Registry 表扫描。
