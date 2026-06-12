# 变更管理 — 产物模板

> **TL;DR**: 所有产物的模板定义文件。Rule：Skill 只提供过程指导，模板以此文件为准。

> **边界**：本文件只定义产物字段模板。目录结构与归档规则见 `.harness/changes/structure.md`，Gate 判定见 `.harness/rules/gates.md`，Memory 字段见 `.harness/memory/README.md`；本文件引用其字段，不重述。

## Raw Skill Template Rule

Skill 只提供过程指导和内容素材，不能直接复制其原始模板作为 Harness artifact。artifact 路径、字段、Gate、Phase/Step 边界，以本文件和对应规则文件为准。

## summary.md 模板

```markdown
# 变更摘要

## 基本信息
- **需求**: {需求名称}
- **类型**: {feat/fix/refactor/perf/test/docs/chore}
- **日期**: {YYYYMMDD}
- **状态**: {active/done/abandoned}
- **Flow**: {Lite-flow/Standard-flow}
- **Current step**: {Standard Phase N 或 Lite L1-L3}
- **Resume point**: {下一步恢复入口；没有则写 none}

## Flow Classification
- **flow**: {Lite-flow/Standard-flow}
- **selection_basis**: {影响面、行为变化和风险判断}
- **risk_flags**: {none 或 security/data/api/auth/payment/perf/migration/architecture/governance/deployment/unclear-requirement}

## 阶段进度
{仅保留所选 Flow 的进度表}

## Memory status
- **Memory recorded**: {N} entries / none
- **Memory evidence**: {decisions.log / lessons-learned.md / known-issues.md / none}

## Lite Spec (Lite-flow 专用)
{以下内容仅在 Lite-flow 时填写，Standard-flow 不填写此节}

### Request
- {用户需求}

### Scope
- In scope:
- Out of scope:

### Acceptance Criteria
- {可验证验收条件}

### Verification
- {验证命令或检查结果}

## 回退/升级记录
- {如果有回退或流程升级，记录原因；没有则写 none}

## 最终交付物
- {产出的文件/功能清单}
```

### Lite-flow 阶段进度片段

```markdown
- [ ] L1: 需求确认+计划
- [ ] L2: 实现
- [ ] L3: 验证+交付
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

```markdown
## Skill Load Records

| Phase/Step | Skill | Action | Condition / Reason | Status | Evidence |
|------------|-------|--------|--------------------|--------|----------|
| Phase 4 | `incremental-implementation` | 读取 | 阶段入口必须读取 | loaded | `.harness/skills/incremental-implementation/SKILL.md` |
| Phase 4 | `api-and-interface-design` | 按条件补读 | 不涉及公共契约变化，not-needed | not-needed | spec/tasks 检查 |
```

字段含义：

- Action: `读取` / `按条件补读` / `失败时补读`
- Condition / Reason: 条件、判断结果或不需要读取的理由
- Status: `loaded` / `not-needed` / `blocked`

## Lite-flow 产物模板

### request_analysis/checklist.md

```markdown
# Lite-flow Checklist

- [ ] {任务 1}
  - Acceptance criteria: {可验证验收条件}
  - Verification: {命令、搜索或确认记录}

## Memory Check
（字段定义见 `.harness/memory/README.md` 的 Lite-flow 3 字段块，按其填写）
```

### verification_report.md（含压缩评审）

```markdown
# Verification Report

## Commands / Checks
- {command or search}: {result}

## Compressed Review
- Status: {Approve / Request Changes}
- Critical: {0}
- Must Fix: {0}
- Review Notes: {评审发现和处理}

## Verdict
- Status: {pass/fail}

## Memory Check
（字段见 `.harness/memory/README.md` 的 Lite-flow 3 字段块；出口报告另需 `Memory recorded: {N} entries / none`）
```

## Standard-flow 产物模板

### Phase 1 — request_analysis/understanding.md

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

### Phase 2 — request_analysis/spec.md

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

### Phase 3 — request_analysis/tasks.md

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
- {实现者自检结果、发现和处理；不得替代 Phase 5 code review}

## DDD / Architecture Check
- {领域/架构边界检查；不适用则写 N/A}

## Deferred Items
- {延期事项、原因和归属 Phase；没有则写 none}

## Verdict
- Status: {pass/fail/blocked}
- Reason: {结论依据}
```

### Phase 5 — coding/review/review_v1.md

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

### Phase 7 — unit_test/review/test_review_v1.md

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

### Phase 8 — ci_result/ci_report.md

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

### Phase 9 — deployment/deploy_report.md

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
