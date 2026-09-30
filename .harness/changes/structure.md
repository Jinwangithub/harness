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
1. 新建变更时新增一行，状态设为 `active`。不得为创建新变更而直接将旧 `active` 改为 `done`：旧 change 只有满足最终完成条件才可 `done`，否则改为 `abandoned` 并在 Notes 说明原因。
2. 任意时刻最多一个 `active`。
3. Registry 与 `summary.md` 的 Status，或任一非空 Resume point，出现冲突时均为 Stop-the-Line / validator FAIL；不得自行择一覆盖。
```

## Flow 产物结构

### Lite-flow

```text
.harness/changes/{type}-{name}-{YYYYMMDD}/
├── summary.md          （含 inline lite spec 和必要的上下文检索记录）
├── request_analysis/
│   └── checklist.md
└── verification_report.md  （含压缩评审）
```

Lite-flow 不创建 `spec.md`、`tasks.md`、`coding/`、`unit_test/`、`delivery-summary.md`，除非升级为 Standard-flow。

### Standard-flow

Phase 4/5 各包含 implementation 与独立 review 子步骤，但继续保留四个独立报告路径，以区分 Implementer 证据和 Reviewer 证据。

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
└── delivery-summary.md  （交付摘要与用户确认）
```

## 归档规则

1. 每个 Phase 或 Flow step 完成后立即归档对应产物。
2. 产物按需标记版本号（如 `review_v1` → `review_v2`）。
3. 回退或流程升级时记录 reason 到 `summary.md`。
4. Phase 1/L1 的上下文检索证据写入 `understanding.md` 或 Lite inline spec，Phase 2 的项目/系统检索证据写入 `spec.md`；不创建独立知识库 artifact。
5. 最终归档顺序必须为：final Gate Mechanical=`pass`、Human Approval=`pending` → 用户批准 → 更新 final Gate Human Approval=`approved` → 同步 `summary.md` / `INDEX.md` 为 `done` 且 Resume point=`none` → 运行 `python3 .harness/tools/validate_change.py --change {id}` → 仅 PASS 后声明完成。确认前两处均保持 `active`。

## 已完成变更保留

`changes/` 是保留最近交付证据的短期工作区，Git 保存工程历史。Registry 中 `done` 超过 5 时，按表内顺序审阅最旧的一项，一次只处理一项。

删除工具只在 change 已通过最终用户确认、状态和 Resume point 一致、validator 通过且属于最旧超额 `done` 时删除该目录及精确 Registry 行。`active`、`abandoned`、未登记路径以及任何证据不完整的 `done` 均不得删除。
