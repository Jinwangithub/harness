# 变更管理 — Audit Trail

本文件是变更目录结构、summary 模板、Skill Load Record 和产物模板的权威源。流程规则见 `.harness/rules/development-workflow.md`，门禁检查见 `.harness/rules/quality-gates.md`。

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

## Raw Skill Template Rule

Skill 只提供过程指导和内容素材，不能直接复制其原始模板作为 Harness artifact。artifact 路径、字段、Gate、Skill Load Record、Phase/Step 边界，以本文件和对应规则文件为准。

## Flow 产物结构

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
└── delivery-summary.md
```

## summary.md 模板

```markdown
# 变更摘要

## 基本信息
- **需求**: {需求名称}
- **类型**: {feat/fix/refactor/perf/test/docs/chore}
- **日期**: {YYYYMMDD}
- **状态**: {active/done/abandoned}
- **Flow**: {Lite-flow/Standard-flow}
- **Current step**: {Lite L1-L4 或 Standard Phase N}
- **Resume point**: {下一步恢复入口；没有则写 none}

## 阶段进度
{仅保留所选 Flow 的进度表}

## Memory status
- **Memory recorded**: {N} entries / none
- **Memory evidence**: {decisions.log / lessons-learned.md / known-issues.md / none}

## 回退/升级记录
- {如果有回退或流程升级，记录原因；没有则写 none}

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

`Role` 只能使用 `.harness/skills/README.md` 定义的角色术语：`Required Skill`、`Support Skill`、`Conditional Skill`、`Forbidden/Deferred`。`Status` 只能使用：`loaded`、`blocked`、`not-triggered`、`not-required-by-policy`。Required Skill 未加载，或 Conditional Skill 触发但未加载时，对应 Mechanical Gate 必须 `blocked`。

```markdown
## Skill Load Records

| Phase/Step | Skill | Role | Trigger evaluation | Status | Reason/Evidence |
|------------|-------|------|--------------------|--------|-----------------|
| {Phase 4} | `incremental-implementation` | Required Skill | required-by-phase | loaded | {读取路径} |
```

## Lite-flow 产物模板

### request_analysis/lite_spec.md

```markdown
# Lite Spec

## Request
- {用户需求}

## Scope
- In scope:
- Out of scope:

## Acceptance Criteria
- {可验证验收条件}

## Verification
- {验证命令或检查结果}

## Memory Check
- Memory recorded: {N} entries / none
```

### request_analysis/checklist.md

```markdown
# Lite-flow Checklist

- [ ] {任务 1}
  - Acceptance criteria: {可验证验收条件}
  - Verification: {命令、搜索或确认记录}

## Memory Check
- Memory recorded: {N} entries / none
```

### verification_report.md

```markdown
# Verification Report

## Commands / Checks
- {command or search}: {result}

## Verdict
- Status: {pass/fail}
- Memory recorded: {N} entries / none
```

### review_summary.md

```markdown
# Review Summary

## Verdict
- Status: {Approve / Request Changes}
- Critical: {0}
- Must Fix: {0}

## Review Notes
- {评审发现和处理}

## Memory Check
- Memory recorded: {N} entries / none
```

## Standard-flow 产物模板

### Phase 1 — request_analysis/understanding.md

Required Skill: `idea-refine`

```markdown
# Understanding

## Problem Statement
- {用户问题、现状、痛点和期望结果}

## Recommended Direction
- {推荐方向、取舍和理由}

## Key Assumptions
- {当前可继续推进所依赖的假设}

## MVP Scope
- In scope:
- Out of scope:

## Not Doing
- {明确不做的事项，防止范围扩张}

## Open Questions
- {仍需用户或业务知识确认的问题；没有则写 none}
```

边界：不创建 `spec.md`、`tasks.md`，不实现代码。

### Phase 2 — request_analysis/spec.md

Required Skill: `spec-driven-development`

```markdown
# Spec

## Objective
- {目标、业务价值和可验证结果}

## Tech Stack
- {相关语言、框架、依赖、平台或 none}

## Commands
- Build:
- Lint:
- Typecheck:
- Test:

## Project Structure
- {相关目录、模块和边界}

## Code Style
- {项目约定、格式、命名或引用路径}

## Testing Strategy
- {测试层级、覆盖重点、项目阈值或待确认项}

## Boundaries
- In scope:
- Out of scope:
- Forbidden / Deferred:

## Success Criteria
- {可机械验证或人工确认的验收标准}

## Open Questions
- {仍需确认的问题；没有则写 none}
```

边界：只产 `spec.md`；`tasks.md` 由 Phase 3 首次创建。

### Phase 3 — request_analysis/tasks.md

Required Skill: `planning-and-task-breakdown`

```markdown
# Tasks

## Overview
- {任务拆解摘要和交付策略}

## Spec Success Criteria Mapping
| Success Criteria from spec.md | Task Group / Slice | Verification |
|-------------------------------|--------------------|--------------|
| {spec.md Success Criteria item} | {Task Group / Slice N} | {验证命令、检查或报告} |

## Architecture Decisions
- {已确认的架构/设计决策；没有则写 none}

## Task Groups / Slices

### Task Group / Slice {N}: {名称}
- Spec success criteria mapping: {对应条目}
- Description: {要完成的工作}
- Acceptance criteria: {可验证条件}
- Verification: {验证命令、检查或报告}
- Dependencies: {依赖或 none}
- Files likely touched: `{path}`

## Risks and Mitigations
- Risk: {风险} / Mitigation: {缓解措施}

## Open Questions
- {仍需确认的问题；没有则写 none}
```

边界：禁止使用 `Phase 1/2/3` 作为实现步骤标题；每个 Task Group/Slice 必须映射到 `spec.md` Success Criteria。

### Phase 4 — coding/coding_report_v1.md

Required Skills: `incremental-implementation`, `auto-check-and-optimize`

```markdown
# Coding Report v1

## Implementation Scope
- {本次实现范围，必须对应 approved spec/tasks}

## Implementation Slices / Tasks
- {完成的 Task Group / Slice，含状态和证据}

## Changed Files
- `{path}`: {变更摘要}

## Compile / Build Evidence
- Command: {来自 spec.md 的项目命令}
- Result: {exit code / key output}

## Author / Self Review
- {auto-check-and-optimize 自检结果、发现和处理}

## DDD / Architecture Check
- {领域/架构边界检查；不适用则写 N/A}

## Deferred Items
- {延期事项、原因和归属 Phase；没有则写 none}

## Verdict
- Status: {pass/fail/blocked}
- Reason: {结论依据}
```

边界：不执行 git commit（除非用户明确要求）；不运行 Phase 6 单元测试；Author/Self Review 不替代 Phase 5 Independent Review。

### Phase 5 — coding/review/review_v1.md

Required Skill: `code-review-and-quality`

```markdown
# Code Review v1

## Context
- {评审输入、变更范围、spec/tasks 链接}

## Correctness
## Readability / Maintainability
## Architecture
## Security
## Performance

## Findings by Severity
### Critical
### Must Fix
### Should Fix
### Nice to Have

## Verdict
- Status: {Approve / Request Changes / Blocked}
- Critical count: {0+}
- Must Fix count: {0+}
- Reason: {结论依据}
```

边界：不直接实现修复；Critical/Must Fix 回退 Phase 4。

### Phase 6 — unit_test/test_report.md

Required Skill: `test-driven-development`

```markdown
# Unit Test Report

## Test Scope
- {测试覆盖的功能、模块和边界}

## RED / GREEN / REFACTOR
- RED: {新增/失败测试或 N/A}
- GREEN: {通过证据}
- REFACTOR: {整理；没有则写 none}

## Test Cases
- {测试用例、断言重点和对应 spec/tasks}

## Commands
- {测试命令、退出码、关键输出}

## Coverage
- {覆盖率结果、阈值或 N/A}

## Failures
- {失败、根因和回退目标；没有则写 none}
```

边界：测试暴露实现缺陷时回退 Phase 4；不得静默修改需求/spec。

### Phase 7 — unit_test/review/test_review_v1.md

Required Skills: `code-review-and-quality`, `test-driven-development`

```markdown
# Test Review v1

## Test Adequacy
## Spec Coverage
## Skipped / Flaky / Brittle Tests
## Coverage Review

## Findings by Severity
- Critical:
- Must Fix:
- Should Fix:
- Nice to Have:

## Verdict
- Status: {Approve / Request Changes / Blocked}
- Critical count: {0+}
- Must Fix count: {0+}
- Reason: {结论依据}
```

边界：测试缺口回退 Phase 6；实现或需求缺陷回退对应更早 Phase。

### Phase 8 — ci_result/ci_report.md

Required Skill: `ci-cd-and-automation`

```markdown
# CI Report

## Pipeline / Gate Results
- {CI pipeline 名称、运行链接/编号、状态或不可用原因}

## Checks
- Build / Lint / Typecheck / Tests / Security scan: {pass/fail/blocked/N/A}

## Local Equivalents
- {CI 不可用时的本地等价验证；不适用则写 N/A}

## Failures
- {失败项、根因和回退目标；没有则写 none}

## Verdict
- Status: {pass/fail/blocked}
- Reason: {结论依据}
```

边界：CI 不可用时必须记录本地等价验证；不得绕过失败 CI。

### Phase 9 — deployment/deploy_report.md

Required Skill: `shipping-and-launch`

```markdown
# Deployment Report

## Pre-launch Checklist
## Rollout / Staging / Deployment Evidence
## Rollback Plan
- {回滚方案、触发条件和执行方式}

## Monitoring / Smoke Evidence

## Issues
- {部署问题、风险和处理；没有则写 none}

## Verdict
- Status: {pass/fail/blocked}
- Reason: {结论依据}
```

### Phase 10 — delivery-summary.md

Required Skill: `documentation-and-adrs`

```markdown
# Delivery Summary

## Delivered Scope
- {已交付范围，对应 spec/tasks}

## Evidence Links
- {各 Phase artifact 和验证报告链接}

## Documentation / ADR / Changelog
- {按需项目文档产物；没有则写 none}

## Known Gotchas / Limitations
- {已知限制、注意事项；没有则写 none}

## User Confirmation
- Status: {pending / confirmed}
- Evidence: {用户确认记录或 pending reason}
```

边界：未经用户要求不执行 git commit/push；不修改实现代码。

## 归档规则

1. 每个 Phase 或 Flow step 完成后立即归档对应产物。
2. 产物按需标记版本号（如 `review_v1` → `review_v2`）。
3. 回退或流程升级时记录 reason 到 `summary.md`。
4. 用户确认后将 `summary.md` 状态改为 `done`，同步更新 `INDEX.md`。
