# Changes Index

恢复索引。会话开始时先读本文件，找到 `active` 变更后读其 `summary.md`。

## Registry

| Change | Status | Resume point | Notes |
|--------|--------|--------------|-------|
| chore-harness-operability-index-validation-20260526 | active | Phase 10 用户确认 | 等待用户确认 |
| fix-harness-executability-20260521 | abandoned | — | 被后续治理工作取代 |
| docs-harness-slimming-20260520 | abandoned | — | 被后续治理工作取代 |
| docs-flow-friction-reduction-20260519 | abandoned | — | summary 状态冲突，不自动恢复 |
| feat-harness-evaluation-20260514 | done | — | 历史归档 |

## 状态说明

| Status | 含义 |
|--------|------|
| `active` | 当前进行中，会话恢复自动加载；最多一个 |
| `done` | 已完成交付 |
| `abandoned` | 已放弃或被取代，不自动恢复 |

## 维护规则

1. 新建变更时新增一行，状态设为 `active`，同时将原 `active` 行改为 `done` 或 `abandoned`。
2. 任意时刻最多一个 `active`。
3. Registry 与 `summary.md` 冲突时 Stop-the-Line，不自行猜测。
