# 变更管理 — Audit Trail

本文件是变更目录结构、summary 模板、Skill Load Record、Phase Lock 状态模板和产物模板的权威源。流程规则见 `.harness/rules/02-development-workflow.md`，门禁检查见 `.harness/rules/04-quality-gates.md`。

## 目录命名

每个需求归档到独立目录：

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

## Flow 产物结构

根据 `summary.md` 的 Flow Classification，只保留所选 Flow 的进度表和产物结构，不展开未采用流程。

### Lite-flow

```text
.harness/changes/{type}-{name}-{YYYYMMDD}/
├── summary.md
├── request_analysis/
│   ├── lite_spec.md
│   └── checklist.md
├── verification_report.md
└── review_summary.md
```

Lite-flow 不扩展成 Standard-flow 产物结构。

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
└── delivery-summary.md
```

## summary.md 模板

只展示所选 Flow 的进度，不同时展开多套流程。

```markdown
# 变更摘要

## 基本信息
- **需求**: {需求名称}
- **类型**: {feat/fix/refactor/perf/test/docs/chore}
- **日期**: {YYYYMMDD}
- **状态**: {进行中/已完成/已回退}
- **负责人**: Orchestrator

## Flow Classification
- **Flow**: {Lite-flow/Standard-flow}
- **Selection basis**: {选择依据，说明影响面、行为变化、风险判断}
- **Risk flags**: {none/security/data/api/auth/payment/perf/migration/architecture/deployment/unclear-requirement}
- **Confirmation policy**: {batched/mandatory}
- **Upgrade triggers**: {风险扩大、门禁 fail|blocked、证据不足、Memory 无法完整记录、需要业务判断等}

## 阶段进度
{仅保留所选 Flow 的进度表}

## 门禁状态
| Step/Phase | Mechanical Gate | Evidence | Human Approval | Next/Rollback |
|------------|-----------------|----------|----------------|---------------|
| {Step/Phase} | pass/fail/blocked | {evidence path} | pending-human/approved/rejected/not-required-by-policy | {next/rollback} |

## Skill Load Records
{Standard-flow 每个 Phase 必填；Lite-flow 按需记录}

## Standard Phase Locks
{仅 Standard-flow 使用；模板见下方}

## 回退/升级记录
- {如果有回退或流程升级，记录原因和时间；没有则写 none}

## 最终交付物
- {产出的文件/功能清单}
```

### Lite-flow 阶段进度片段

```markdown
- [ ] L1: 需求确认+简化计划
- [ ] L2: 实现
- [ ] L3: 验证/压缩评审
- [ ] L4: 交付确认
```

### Standard-flow 阶段进度片段

```markdown
- [ ] Phase 1: 需求分析
- [ ] Phase 2: 需求评审
- [ ] Phase 3: 任务规划
- [ ] Phase 4: 编码实现
- [ ] Phase 5: 编码评审
- [ ] Phase 6: 单元测试
- [ ] Phase 7: 测试评审
- [ ] Phase 8: CI验证
- [ ] Phase 9: 部署验证
- [ ] Phase 10: 用户确认
```

## Skill Load Record 模板

Standard-flow 每个 Phase 必须记录 Required Skills；Support/Conditional Skills 在加载或触发时记录。

```markdown
## Skill Load Records

| Phase/Step | Skill | Role | Status | Reason/Evidence |
|------------|-------|------|--------|-----------------|
| {Phase 4} | `incremental-implementation` | Required | loaded/blocked/not-triggered | {读取路径、触发原因、阻塞原因或证据路径} |
| {Phase 4} | `auto-check-and-optimize` | Required | loaded/blocked/not-triggered | {读取路径、Author/Self Review 证据路径} |
```

`Role` 取值以 `.harness/skills/README.md` 为准；Required Skill 未加载时对应 Mechanical Gate 必须 `blocked`。

## Standard Phase Locks 状态模板

```markdown
## Standard Phase Locks

| Phase | Entry Lock | Work Lock | Exit Lock | Human Approval Lock | Failure Lock | Evidence |
|-------|------------|-----------|-----------|---------------------|--------------|----------|
| Phase {N} | open/closed/blocked | respected/violated | open/closed/blocked | pending-human/approved/rejected/not-required-by-policy | none/active/resolved | {gate record, artifact paths, memory check, approval evidence} |
```

Phase Lock 判定规则见 `.harness/rules/02-development-workflow.md`；机械检查要求见 `.harness/rules/04-quality-gates.md`。

## Lite-flow 产物模板

### request_analysis/lite_spec.md

```markdown
# Lite Spec

## Request
- {用户需求}

## Scope
- In scope:
- Out of scope:

## Flow Classification
- Flow: Lite-flow
- Selection basis:
- Risk flags:
- Confirmation policy: batched
- Upgrade triggers:

## Acceptance Criteria
- {可验证验收条件}
```

### request_analysis/checklist.md

```markdown
# Lite-flow Checklist

- [ ] {任务 1，含验收条件}
- [ ] {任务 2，含验收条件}

## Mechanical Gate
- [ ] checklist items are independently verifiable
- [ ] no Standard-flow risk flags introduced
```

### verification_report.md

```markdown
# Verification Report

## Commands / Checks
- {command or search}: {result}

## Mechanical Gate
- Status: {pass/fail/blocked}
- Fresh verification evidence:
- Memory recorded: {N} entries / none
```

### review_summary.md

```markdown
# Review Summary

## Verdict
- Status: {Approve / Request Changes / Blocked}
- Critical: {0}
- Must Fix: {0}

## Compressed Two-stage Review
- Author/Self Review:
- Independent/Isolated Review Summary:

## Confirmation Policy
- Policy: batched
- Requirements + simplified plan approval:
- Final verification/review approval:
```

## Standard-flow 产物说明

Standard-flow 目录结构完整模板在本文件维护；具体 Gate 检查不复制到产物模板中，统一引用 `.harness/rules/04-quality-gates.md`。

推荐每个 Phase 报告包含：

```markdown
# {Phase} Report

## Scope
- {本 Phase 范围}

## Skill Load Record
- {引用 summary.md 或复制本 Phase 的记录}

## Artifacts
- {产物路径}

## Fresh Verification Evidence
- {命令/检查/报告路径}

## Mechanical Gate
- Status: {pass/fail/blocked}
- Gate rules: `.harness/rules/04-quality-gates.md`

## Memory
- Memory recorded: {N} entries / none
```

## 归档规则

1. 每个 Phase 或 Flow step 完成后立即归档对应产物。
2. 产物按需标记版本号（如 `review_v1` → `review_v2`）。
3. 回退或流程升级时记录 reason 到 `summary.md`。
4. 变更完成后，`summary.md` 标记为“已完成”。
5. 每个 Phase 或 Flow step 的 Mechanical Gate 与 Human Approval Gate 状态必须记录到 `summary.md`。
6. 根据 Flow Classification 仅保留对应流程进度表，不把未采用流程标记为“跳过”。
7. 新规则适用于新变更；历史 `.harness/changes/` 作为旧证据保留，不自动重写。
