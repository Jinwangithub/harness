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

## Standard-flow 产物模板

Standard-flow 各 Phase 产物模板在本文件维护；流程顺序、Phase Lock 和阶段边界以 `.harness/rules/02-development-workflow.md` 为准；Required Skill Matrix 以 `.harness/skills/README.md` 为准；Mechanical Gate 判定以 `.harness/rules/04-quality-gates.md` 为准。

模板内容对齐 `.harness/skills/README.md` 中对应 Phase 的 Required Skills。Skill 原始模板是内容来源；Harness artifact path 和 phase boundary 以 Harness 权威源为准。Skill 内部 “Phase” 术语不得覆盖 Harness Standard Phase 1-10。产物模板只提供归档字段，不复制完整 Gate 规则。

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

边界说明：Phase 1 不创建 `spec.md`、不创建 `tasks.md`、不实现代码。

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
- Other:

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

边界说明：Phase 2 只产 `spec.md`；不产 PLAN/TASKS/IMPLEMENT；`tasks.md` 由 Phase 3 首次创建。

### Phase 3 — request_analysis/tasks.md

Required Skill: `planning-and-task-breakdown`

```markdown
# Tasks

## Overview
- {任务拆解摘要和交付策略}

## Architecture Decisions
- {已确认的架构/设计决策；没有则写 none}

## Task Groups / Slices

### Task Group / Slice {N}: {名称}
- Description: {要完成的工作}
- Acceptance criteria:
  - {可验证条件}
- Verification:
  - {验证命令、检查或报告}
- Dependencies:
  - {依赖的任务、文件、外部条件或 none}
- Files likely touched:
  - `{path}`

## Checkpoints
- {阶段内检查点、回退点或确认点}

## Risks and Mitigations
- Risk: {风险}
  - Mitigation: {缓解措施}

## Open Questions
- {仍需确认的问题；没有则写 none}
```

边界说明：为避免混淆，不使用 `Phase 1/2/3` 表示实现步骤；统一使用 `Task Group`、`Slice` 或 `Checkpoint`。

### Phase 4 — coding/coding_report_v1.md

Required Skills: `incremental-implementation`, `auto-check-and-optimize`

```markdown
# Coding Report v1

## Implementation Scope
- {本次实现范围，必须对应 approved spec/tasks}

## Implementation Slices / Tasks
- {完成的 Task Group / Slice / task，含状态和证据}

## Changed Files
- `{path}`: {变更摘要}

## Compile / Build Evidence
- Command: {来自 `spec.md` 的项目命令}
- Result: {exit code / key output / artifact path}

## Author / Self Review
- {`auto-check-and-optimize` 自检结果、发现和处理}

## DDD / Architecture Check
- {领域/架构边界检查；不适用则写 N/A}

## Deferred Items
- {延期事项、原因和归属 Phase；没有则写 none}

## Verdict
- Status: {pass/fail/blocked}
- Reason: {结论依据}
```

边界说明：Phase 4 不执行 git commit，除非用户明确要求；不运行或冒充 Phase 6 单元测试/覆盖率职责；Phase 4 Author/Self Review 不替代 Phase 5 Independent Review；编译命令来自 `spec.md` 的项目命令，不硬编码 `mvn compile`。

### Phase 5 — coding/review/review_v1.md

Required Skill: `code-review-and-quality`

```markdown
# Code Review v1

## Context
- {评审输入、变更范围、spec/tasks 链接}

## Correctness
- {正确性审查结论}

## Readability / Maintainability
- {可读性、复杂度、可维护性审查结论}

## Architecture
- {架构边界、模块职责、耦合审查结论}

## Security
- {安全风险审查结论；不适用则写 N/A}

## Performance
- {性能风险审查结论；不适用则写 N/A}

## Verification
- {已审查的编译/验证证据}

## Findings by Severity

### Critical
- {item 或 none}

### Must Fix
- {item 或 none}

### Should Fix
- {item 或 none}

### Nice to Have
- {item 或 none}

## Verdict
- Status: {Approve / Request Changes / Blocked}
- Critical count: {0+}
- Must Fix count: {0+}
- Reason: {结论依据}
```

边界说明：Phase 5 不直接实现修复；Critical/Must Fix 回退 Phase 4。

### Phase 6 — unit_test/test_report.md

Required Skill: `test-driven-development`

```markdown
# Unit Test Report

## Test Scope
- {测试覆盖的功能、模块和边界}

## RED / GREEN / REFACTOR
- RED: {新增/失败测试或 N/A}
- GREEN: {通过证据}
- REFACTOR: {测试或实现整理；没有则写 none}

## Test Cases
- {测试用例、断言重点和对应 spec/tasks}

## Commands
- {测试命令、退出码、关键输出}

## Coverage
- {覆盖率结果、阈值、报告路径或 N/A}

## Skipped / Pending Tests
- {跳过/待补测试和原因；没有则写 none}

## Failures
- {失败、根因和回退目标；没有则写 none}
```

边界说明：如测试暴露实现缺陷，回退 Phase 4；不得在 Phase 6 静默修改需求/spec。

### Phase 7 — unit_test/review/test_review_v1.md

Required Skills: `code-review-and-quality`, `test-driven-development`

```markdown
# Test Review v1

## Test Adequacy
- {测试充分性审查}

## Spec Coverage
- {spec/tasks 覆盖映射和缺口}

## Skipped / Flaky / Brittle Tests
- {跳过、不稳定、脆弱测试审查；没有则写 none}

## Coverage Review
- {覆盖率结果、阈值和风险}

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

边界说明：测试缺口回退 Phase 6；实现或需求缺陷回退对应更早 Phase。

### Phase 8 — ci_result/ci_report.md

Required Skill: `ci-cd-and-automation`

```markdown
# CI Report

## Pipeline / Gate Results
- {CI pipeline 名称、运行链接/编号、状态或不可用原因}

## Checks
- Build: {pass/fail/blocked/N/A}
- Lint: {pass/fail/blocked/N/A}
- Typecheck: {pass/fail/blocked/N/A}
- Tests: {pass/fail/blocked/N/A}
- Security scan: {pass/fail/blocked/N/A}
- Other: {pass/fail/blocked/N/A}

## Local Equivalents
- {CI 不可用时的本地等价验证命令和结果；不适用则写 N/A}

## Failures
- {失败项、证据、根因和回退目标；没有则写 none}

## Feedback / Follow-up
- {CI 反馈、待办或改进；没有则写 none}

## Verdict
- Status: {pass/fail/blocked}
- Reason: {结论依据}
```

边界说明：CI 不可用时必须记录本地等价验证；不得绕过失败 CI。

### Phase 9 — deployment/deploy_report.md

Required Skill: `shipping-and-launch`

```markdown
# Deployment Report

## Pre-launch Checklist
- {发布前检查项和状态}

## Rollout / Staging / Deployment Evidence
- {部署/预发/灰度证据、命令、链接或 N/A}

## Rollback Plan
- {回滚方案、触发条件和负责人/执行方式}

## Monitoring / Smoke Evidence
- {监控、冒烟验证、关键指标和结果}

## Issues
- {部署问题、风险和处理；没有则写 none}

## Verdict
- Status: {pass/fail/blocked}
- Reason: {结论依据}
```

边界说明：部署验证不替代最终交付确认；部署风险回退 Phase 8/9。

### Phase 10 — delivery-summary.md

Required Skill: `documentation-and-adrs`

```markdown
# Delivery Summary

## Delivered Scope
- {已交付范围，对应 spec/tasks}

## Evidence Links
- {各 Phase artifact、Gate Record、验证报告链接}

## Gate Summary
- {CK1-CK9 / Mechanical Gate / Human Approval Gate 状态摘要}

## Documentation / ADR / Changelog
- {按需项目文档产物；没有则写 none}

## Known Gotchas / Limitations
- {已知限制、注意事项和后续建议；没有则写 none}

## Final User Confirmation
- Status: {pending-human/approved/rejected}
- Evidence: {用户确认记录或 pending reason}
```

边界说明：未经用户要求，不执行 git commit/push；不修改实现代码。ADR、README、Changelog 等是按需项目产物，`delivery-summary.md` 是 Harness 必需归档产物。

## 归档规则

1. 每个 Phase 或 Flow step 完成后立即归档对应产物。
2. 产物按需标记版本号（如 `review_v1` → `review_v2`）。
3. 回退或流程升级时记录 reason 到 `summary.md`。
4. 变更完成后，`summary.md` 标记为“已完成”。
5. 每个 Phase 或 Flow step 的 Mechanical Gate 与 Human Approval Gate 状态必须记录到 `summary.md`。
6. 根据 Flow Classification 仅保留对应流程进度表，不把未采用流程标记为“跳过”。
7. 新规则适用于新变更；历史 `.harness/changes/` 作为旧证据保留，不自动重写。
