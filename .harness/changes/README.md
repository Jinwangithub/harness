# 变更管理 — Audit Trail

## 目录结构

每个需求的变更归档在独立目录中。根据 `summary.md` 的 Flow Classification，只保留所选流程对应的进度表和产物结构，不把未采用流程标记为“跳过”。

### Standard-flow

```text
.harness/changes/
└── {变更类型}-{需求名称}-{YYYYMMDD}/
    ├── summary.md
    ├── request_analysis/
    │   ├── understanding.md
    │   ├── spec.md
    │   ├── tasks.md
    │   └── review/
    ├── coding/
    │   ├── coding_report_v1.md
    │   └── review/
    │       ├── code_review_v1.md
    │       ├── security_report_v1.md
    │       └── perf_report_v1.md
    ├── unit_test/
    │   ├── test_report.md
    │   └── review/
    │       └── test_review_v1.md
    ├── ci_result/
    │   └── ci_report.md
    └── deployment/
        └── deploy_report.md
```

### Lite-flow

```text
.harness/changes/
└── {变更类型}-{需求名称}-{YYYYMMDD}/
    ├── summary.md
    ├── request_analysis/
    │   ├── lite_spec.md
    │   └── checklist.md
    ├── verification_report.md
    └── review_summary.md
```

### Mini-flow

```text
.harness/changes/
└── {变更类型}-{需求名称}-{YYYYMMDD}/
    ├── summary.md
    ├── verification_report.md
    └── review_summary.md
```

## 变更类型前缀

| 前缀 | 含义 |
|------|------|
| feat- | 新功能 |
| fix- | Bug 修复 |
| refactor- | 重构 |
| perf- | 性能优化 |
| test- | 测试 |
| docs- | 文档 |
| chore- | 工程维护 |

## summary.md 模板

```markdown
# 变更摘要

## 基本信息
- **需求**: {需求名称}
- **类型**: {feat/fix/refactor/...}
- **日期**: {YYYYMMDD}
- **状态**: {进行中/已完成/已回退}
- **负责人**: {orchestrator}

## Flow Classification
- **Flow**: {Mini-flow/Lite-flow/Standard-flow}
- **Selection basis**: {选择依据，说明影响面、行为变化、风险判断}
- **Risk flags**: {none/security/data/api/auth/payment/perf/migration/architecture/deployment/unclear-requirement}
- **Confirmation policy**: {exception-only/batched/mandatory}
- **Upgrade triggers**: {风险扩大、门禁 fail|blocked、证据不足、Memory 无法完整记录、需要业务判断等}

## 阶段进度
{仅保留所选流程对应进度表}

### Standard-flow 阶段进度
- [x] Phase 1: 需求分析 → {日期}
- [x] Phase 2: 需求评审 → {日期}
- [x] Phase 3: 任务规划 → {日期}
- [ ] Phase 4: 编码实现
- [ ] Phase 5: 编码评审
- [ ] Phase 6: 单元测试
- [ ] Phase 7: 测试评审
- [ ] Phase 8: CI验证
- [ ] Phase 9: 部署验证
- [ ] Phase 10: 用户确认

### Lite-flow 阶段进度
- [ ] L1: 需求确认+简化计划
- [ ] L2: 实现
- [ ] L3: 验证/压缩评审
- [ ] L4: 交付确认

### Mini-flow 阶段进度
- [ ] M1: 理解/分类
- [ ] M2: 修改
- [ ] M3: 验证
- [ ] M4: 记录/总结

## 门禁状态
| Step/Phase | Mechanical Gate | Evidence | Human Approval | Next/Rollback |
|------------|-----------------|----------|----------------|---------------|
| {Step/Phase} | pass/fail/blocked | {evidence path} | pending-human/approved/rejected/not-required-by-policy | {next/rollback} |

## 回退/升级记录
- {如果有回退或流程升级，记录原因和时间}

## 最终交付物
- {产出的文件/功能清单}
```

## Mini-flow 压缩产物结构

### verification_report.md

```markdown
# Verification Report

## Scope
- Flow: Mini-flow
- Changed files:
- No behavior change basis:

## Mechanical Gate
- Status: {pass/fail/blocked}
- Checks:
  - [ ] Flow Classification exists
  - [ ] Scope remains Mini-flow
  - [ ] Fresh verification evidence listed
  - [ ] Memory check completed

## Fresh Verification Evidence
- {content review / consistency search / file check}

## Memory
- Memory recorded: {N} entries / none
```

### review_summary.md

```markdown
# Review Summary

## Verdict
- Status: {Approve / Request Changes / Blocked}
- Independent review waived: {yes/no}
- Waiver basis: {Mini-flow low-risk no behavior change basis}

## Findings
- {None or findings}

## Confirmation Policy
- Policy: exception-only
- Final summary confirmation: {pending-human/approved/not-required}
```

## Lite-flow 压缩产物结构

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

## Phase 5 三份评审报告最小结构

`code_review_v1.md`、`security_report_v1.md`、`perf_report_v1.md` 均至少包含：

```markdown
# {Code Review / Security Report / Performance Report}

## Verdict
- Status: {Approve / Request Changes / Blocked}
- Critical: {0}
- Must Fix: {0}

## Scope
- Reviewed changes:
- Exclusions:

## Mechanical Checks
- [ ] Required files reviewed
- [ ] Relevant commands or static checks recorded
- [ ] Critical/Must Fix counts summarized

## Findings
| Severity | Area | Finding | Recommendation |
|----------|------|---------|----------------|

## Evidence
- Evidence paths:
- Command outputs:
- Logs/screenshots:

## Required Fixes
- {Required fixes before next Phase, or "None"}
```

## 归档规则

1. 每个 Phase 或分级流程步骤完成后立即归档对应产物。
2. 产物标记版本号（如 review_v1 → review_v2）。
3. 回退或流程升级时记录 reason 到 summary.md。
4. 变更完成后，summary.md 标记为“已完成”。
5. 每个 Phase 或分级流程步骤的 Mechanical Gate 与 Human Approval Gate 状态必须记录到 summary.md。
6. 根据 Flow Classification 仅保留对应流程进度表，不把未采用流程标记为“跳过”。
