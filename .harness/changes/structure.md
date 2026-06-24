# 变更管理 — 目录结构和归档规则

> **TL;DR**: 目录命名 `{type}-{name}-{YYYYMMDD}/`。任意时刻最多一个 `active`。INDEX.md 是唯一 registry。

本文件是变更目录结构、命名规范和归档规则的权威源。产物模板见 `.harness/changes/templates.md`。

> **边界**：本文件只定义目录结构、命名、INDEX 状态语义与归档规则。产物字段模板见 `templates.md`，Gate 判定见 `.harness/rules/gates.md`；本文件不重述。

## 目录命名

```text
.harness/changes/{type}-{name}-{YYYYMMDD}/
```

| 前缀 | 含义 |
|------|------|
| `feat-` | 新功能 |
| `fix-` | Bug 修复 |
| `refactor-` | 重构 |
| `perf-` | 性能优化 |
| `test-` | 测试 |
| `docs-` | 文档 |
| `chore-` | 工程维护 |

## Changes Registry — `INDEX.md`

`.harness/changes/INDEX.md` 是全局 changes registry / 恢复索引。会话恢复必须 registry-first：先读 `INDEX.md`，找到 `active` 变更后读其 `summary.md`。冲突时 Stop-the-Line，不自行猜测恢复对象。

变更状态只有三种：`active`（进行中）、`done`（已完成）、`abandoned`（已放弃/被取代）。任意时刻最多一个 `active`。

INDEX.md 格式：

```markdown
# Changes Index

| Change | Status | Resume point | Notes |
|--------|--------|--------------|-------|

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
```

## Flow 产物结构

### Lite-flow

```text
.harness/changes/{type}-{name}-{YYYYMMDD}/
├── summary.md          （含 inline lite spec）
├── request_analysis/
│   └── checklist.md
├── wiki/
│   └── candidates.md
└── verification_report.md  （含压缩评审）
```

Lite-flow 不创建 `spec.md`、`tasks.md`、`coding/`、`unit_test/`、`ci_result/`、`deployment/`、`delivery-summary.md`，除非升级为 Standard-flow。

### Standard-flow

```text
.harness/changes/{type}-{name}-{YYYYMMDD}/
├── summary.md
├── request_analysis/
│   ├── understanding.md
│   ├── spec.md
│   ├── tasks.md
│   └── review/
├── coding/
│   ├── coding_report_v1.md
│   └── review/
├── unit_test/
│   ├── test_report.md
│   └── review/
├── ci_result/
├── deployment/
├── wiki/
│   └── candidates.md
└── delivery-summary.md
```

## 归档规则

1. 每个 Phase 或 Flow step 完成后立即归档对应产物。
2. 产物按需标记版本号（如 `review_v1` → `review_v2`）。
3. 回退或流程升级时记录 reason 到 `summary.md`。
4. 每个完成需求必须归档 `wiki/candidates.md`；如果没有 durable business knowledge，也必须记录 `none` 和原因。
5. 正式 `.harness/wiki/` 更新必须获得明确人工批准；未批准、rejected 或 deferred candidates 只保留在 change artifact 中。
6. 用户确认后将 `summary.md` 状态改为 `done`，同步更新 `INDEX.md`。
