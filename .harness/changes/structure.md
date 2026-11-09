# 变更管理 — 目录结构和归档规则

> **TL;DR**: 消费项目只保存 `docs/harness/{type}-{name}-{YYYYMMDD}/` 任务产物；Harness 定义和工具由已安装插件提供。

本文件是变更目录结构、命名规范和归档规则的权威源。产物模板见 `.harness/changes/templates.md`。

> **边界**：本文件定义消费项目任务目录、命名与归档规则，并说明插件仓库开发用 INDEX。产物字段模板见 `templates.md`，Gate 判定见 `.harness/rules/gates.md`。

## 目录命名

```text
docs/harness/{type}-{name}-{YYYYMMDD}/
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

消费项目不需要创建全局 `INDEX.md`。Orchestrator 从消费项目的 `docs/harness/*/summary.md` 中定位活动任务；若存在多个活动任务且当前请求无法唯一匹配，询问用户选择。插件仓库自身可以保留 `.harness/changes/INDEX.md` 作为本插件的开发记录，但它不是消费项目产物。

变更状态只有三种：`active`（进行中）、`done`（已完成）、`abandoned`（已放弃/被取代）。每个任务的状态仅记录在该任务自己的 `summary.md`。

`INDEX.md` 是插件仓库维护用的可选文件，不由消费项目创建：

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

## 消费项目产物边界

- 插件定义只读来源：插件安装目录中的 `agents/`、`rules/`、`skills/`、`tools/` 和模板。
- 消费项目唯一 Harness 输出根：`docs/harness/`。
- 每个需求在该目录下创建自己的变更目录；不创建项目级 `.harness/`、INDEX、memory、rules、agents 或 skills 副本。
- `summary.md` 是单个需求的状态和恢复点来源。
```

## Flow 产物结构

### Lite-flow

```text
docs/harness/{type}-{name}-{YYYYMMDD}/
├── summary.md          （含 inline lite spec 和必要的上下文检索记录）
├── request_analysis/
│   └── checklist.md
└── verification_report.md  （含压缩评审）
```

Lite-flow 不创建 `spec.md`、`tasks.md`、`coding/`、`unit_test/`、`delivery-summary.md`，除非升级为 Standard-flow。

### Standard-flow

Phase 4 首先由 Planner 生成 `tasks.md`，随后依次执行 implementation 与独立 code-review；任务规划不单独设 Gate 或用户确认。Phase 4/5 保留各自独立报告路径，以区分实现/测试证据和 Reviewer 证据。

```text
docs/harness/{type}-{name}-{YYYYMMDD}/
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
5. 最终归档顺序必须为：final Gate Mechanical=`pass`、Human Approval=`pending` → 用户批准 → 更新 final Gate Human Approval=`approved` → 同步当前任务 `summary.md` 为 `done` 且 Resume point=`none` → 调用插件包内 validator 并传入消费项目根目录 → 仅 PASS 后声明完成。确认前 `summary.md` 保持 `active`。
