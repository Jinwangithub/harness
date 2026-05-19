# 质量门禁定义

## 门禁通用规则

- 每个 Phase 必须先执行 Mechanical Gate，再执行 Human Approval Gate。
- Mechanical Gate 必须机器可验证，或具备明确证据路径和判定规则。
- Human Approval Gate 只能在 Mechanical Gate 通过后询问用户。
- "感觉没问题" = 不通过。
- 必须提供证据（测试结果、日志、回包、报告路径等）。
- 事实判断优先于主观判断。
- 每个 Phase 必须立即可验证，不允许合 Phase 检查。
- Completion claim gate：未列出新鲜验证证据（命令、结果、报告路径或审查报告路径）时，不得声明完成、通过或交付。
- Mini-flow、Lite-flow、Standard-flow 都必须具备 Mechanical Gate、fresh verification evidence、Memory check 和必要 Human Approval Gate。
- Standard-flow 保持完整 10 阶段；Mini-flow/Lite-flow 只降低阶段密度，不取消验证、证据、Memory 或用户确认。

## 流程分级门禁

| 流程 | Mechanical Gate | 验证证据 | Memory check | 评审要求 |
|------|-----------------|----------|--------------|----------|
| Mini-flow | 必须，覆盖变更说明、验证结果、影响面 | 必须列出命令/结果/报告路径；纯文档可用审查报告路径 | 必须 | 可豁免独立评审，但必须记录豁免依据 |
| Lite-flow | 必须，覆盖 lite spec、任务清单、实现、验证/评审摘要 | 必须列出命令/结果/报告路径/审查摘要路径 | 必须 | 压缩版 Two-stage Review：实现后自检 + 独立/隔离评审摘要 |
| Standard-flow | 必须，按 Phase 1-10 完整执行 | 每个 Phase 出口都必须列出 fresh verification evidence | 必须 | Phase 4 自检 + Phase 5 独立评审 |

## 标准门禁模型

### Mechanical Gate

用于检查文件、状态、命令结果、报告字段、问题计数等可验证条件。状态只能是：

- `pass`: 证据完整且判定通过
- `fail`: 证据存在但判定失败
- `blocked`: 证据缺失、命令无法执行、环境不满足或条件无法判定

### Human Approval Gate

用于用户确认。只有 Mechanical Gate 为 `pass` 后才能进入，未确认时状态为 `pending-human`。

### 标准门禁 JSON 示例

```json
{
  "phase": "Phase 5",
  "name": "编码评审通过",
  "mechanical_gate": {
    "status": "pass|fail|blocked",
    "checks": [
      "code_review_v1.md exists",
      "security_report_v1.md exists",
      "perf_report_v1.md exists",
      "independent review lanes isolated",
      "review summary exists",
      "Critical == 0",
      "Must Fix == 0",
      "memory check completed"
    ],
    "evidence_paths": [
      ".harness/changes/{id}/coding/review/code_review_v1.md",
      ".harness/changes/{id}/coding/review/security_report_v1.md",
      ".harness/changes/{id}/coding/review/perf_report_v1.md",
      ".harness/changes/{id}/coding/review/review_summary.md"
    ],
    "fresh_verification_evidence": [
      "review input package hash or path",
      "independent review reports generated in this Phase",
      "review summary path"
    ]
  },
  "human_approval_gate": {
    "required": true,
    "prompt": "评审报告摘要如下（Verdict: Approve/Request Changes），请确认是否通过？",
    "approved_by": null,
    "approved_at": null
  },
  "next_phase": "Phase 6",
  "rollback_to": "Phase 4"
}
```

## 各阶段门禁

### Phase 1 门禁: 需求分析完成

```json
{
  "phase": "Phase 1",
  "name": "需求分析完成",
  "mechanical_gate": {
    "status": "pass|fail|blocked",
    "checks": ["understanding.md exists", "contains 需求复述", "contains 边界", "contains 疑问点", "memory check completed"],
    "evidence_paths": [".harness/changes/{id}/request_analysis/understanding.md"]
  },
  "human_approval_gate": {
    "required": true,
    "prompt": "以上理解是否正确？",
    "approved_by": null,
    "approved_at": null
  },
  "next_phase": "Phase 2",
  "rollback_to": "Phase 1"
}
```

### Phase 2 门禁: 需求评审通过

```json
{
  "phase": "Phase 2",
  "name": "需求评审通过",
  "mechanical_gate": {
    "status": "pass|fail|blocked",
    "checks": ["spec.md exists", "tasks.md not created by Phase 2", "memory check completed"],
    "evidence_paths": [".harness/changes/{id}/request_analysis/spec.md"]
  },
  "human_approval_gate": {
    "required": true,
    "prompt": "spec 是否确认？",
    "approved_by": null,
    "approved_at": null
  },
  "next_phase": "Phase 3",
  "rollback_to": "Phase 1"
}
```

### Phase 3 门禁: 任务规划完成

```json
{
  "phase": "Phase 3",
  "name": "任务规划完成",
  "mechanical_gate": {
    "status": "pass|fail|blocked",
    "checks": ["tasks.md exists", "each task has acceptance criteria", "tasks are independently verifiable", "memory check completed"],
    "evidence_paths": [".harness/changes/{id}/request_analysis/tasks.md"]
  },
  "human_approval_gate": {
    "required": true,
    "prompt": "任务拆解是否合理？每一个都可独立验证？",
    "approved_by": null,
    "approved_at": null
  },
  "next_phase": "Phase 4",
  "rollback_to": "Phase 2"
}
```

### Phase 4 门禁: 编码完成

```json
{
  "phase": "Phase 4",
  "name": "编码完成",
  "mechanical_gate": {
    "status": "pass|fail|blocked",
    "checks": ["compile success", "coding_report_v1.md exists", "self review completed", "memory check completed"],
    "evidence_paths": [".harness/changes/{id}/coding/coding_report_v1.md", "build.log"],
    "fresh_verification_evidence": ["mvn clean compile result", "auto-check-and-optimize self review result", "coding_report_v1.md path"]
  },
  "human_approval_gate": {
    "required": true,
    "prompt": "编码完成，编译通过，请确认是否可以提交评审？",
    "approved_by": null,
    "approved_at": null
  },
  "next_phase": "Phase 5",
  "rollback_to": "Phase 4"
}
```

**注意**: Phase 4 不运行测试，测试是 Phase 6 的职责。

### Phase 5 门禁: 编码评审通过

```json
{
  "phase": "Phase 5",
  "name": "编码评审通过",
  "mechanical_gate": {
    "status": "pass|fail|blocked",
    "checks": [
      "code_review_v1.md exists",
      "security_report_v1.md exists",
      "perf_report_v1.md exists",
      "independent review lanes isolated",
      "review summary exists",
      "Critical == 0",
      "Must Fix == 0",
      "memory check completed"
    ],
    "evidence_paths": [
      ".harness/changes/{id}/coding/review/code_review_v1.md",
      ".harness/changes/{id}/coding/review/security_report_v1.md",
      ".harness/changes/{id}/coding/review/perf_report_v1.md",
      ".harness/changes/{id}/coding/review/review_summary.md"
    ],
    "fresh_verification_evidence": ["same immutable input package for all lanes", "independent reports generated", "review summary path"]
  },
  "human_approval_gate": {
    "required": true,
    "prompt": "评审报告摘要如下（Verdict: Approve/Request Changes），请确认是否通过？",
    "approved_by": null,
    "approved_at": null
  },
  "next_phase": "Phase 6",
  "rollback_to": "Phase 4"
}
```

### Phase 6 门禁: 单元测试通过

```json
{
  "phase": "Phase 6",
  "name": "单元测试通过",
  "mechanical_gate": {
    "status": "pass|fail|blocked",
    "checks": ["test command success", "total_tests > 0", "passed == total", "coverage >= threshold", "memory check completed"],
    "evidence_paths": [
      ".harness/changes/{id}/unit_test/test_report.md",
      "target/site/jacoco/index.html"
    ]
  },
  "human_approval_gate": {
    "required": true,
    "prompt": "测试已完成，请确认测试结果是否通过？",
    "approved_by": null,
    "approved_at": null
  },
  "next_phase": "Phase 7",
  "rollback_to": "Phase 6"
}
```

### Phase 7 门禁: 测试评审通过

```json
{
  "phase": "Phase 7",
  "name": "测试评审通过",
  "mechanical_gate": {
    "status": "pass|fail|blocked",
    "checks": ["test_review_v1.md exists", "Must Fix == 0", "memory check completed"],
    "evidence_paths": [".harness/changes/{id}/unit_test/review/test_review_v1.md"]
  },
  "human_approval_gate": {
    "required": true,
    "prompt": "测试评审完成，请确认是否通过？",
    "approved_by": null,
    "approved_at": null
  },
  "next_phase": "Phase 8",
  "rollback_to": "Phase 6"
}
```

### Phase 8 门禁: CI 验证通过

```json
{
  "phase": "Phase 8",
  "name": "CI 验证通过",
  "mechanical_gate": {
    "status": "pass|fail|blocked",
    "checks": ["ci_report.md exists", "CI status == success", "memory check completed"],
    "evidence_paths": [".harness/changes/{id}/ci_result/ci_report.md"]
  },
  "human_approval_gate": {
    "required": true,
    "prompt": "CI 验证完成，请确认是否通过？",
    "approved_by": null,
    "approved_at": null
  },
  "next_phase": "Phase 9",
  "rollback_to": "Phase 6"
}
```

### Phase 9 门禁: 部署验证通过

```json
{
  "phase": "Phase 9",
  "name": "部署验证通过",
  "mechanical_gate": {
    "status": "pass|fail|blocked",
    "checks": ["deploy_report.md exists", "smoke check completed", "rollback check completed", "memory check completed"],
    "evidence_paths": [".harness/changes/{id}/deployment/deploy_report.md"]
  },
  "human_approval_gate": {
    "required": true,
    "prompt": "部署验证完成，请确认是否通过？",
    "approved_by": null,
    "approved_at": null
  },
  "next_phase": "Phase 10",
  "rollback_to": "Phase 8"
}
```

### Phase 10 门禁: 最终交付确认

```json
{
  "phase": "Phase 10",
  "name": "最终交付确认",
  "mechanical_gate": {
    "status": "pass|fail|blocked",
    "checks": ["delivery-summary.md exists", "summary.md status updated", "memory completeness verified"],
    "evidence_paths": [
      ".harness/changes/{id}/delivery-summary.md",
      ".harness/changes/{id}/summary.md",
      ".harness/memory/decisions.log",
      ".harness/memory/lessons-learned.md"
    ]
  },
  "human_approval_gate": {
    "required": true,
    "prompt": "交付完成，请最终确认。",
    "approved_by": null,
    "approved_at": null
  },
  "next_phase": null,
  "rollback_to": "Phase 9"
}
```

## 失败门禁规则

任一 Mechanical Gate 为 `fail|blocked` 时，门禁记录必须包含：

- `failure_evidence`: 失败命令、日志、报告路径、缺失条件或阻塞原因。
- `root_cause`: 已定位根因；未定位时保持 blocked，不得进入 Human Approval Gate。
- `rollback_target`: 回退到的 Phase 或分级流程步骤。
- `regression_verification`: 修复后的新鲜验证证据。
- `memory_action`: 是否写入 `lessons-learned.md` / `known-issues.md` / `decisions.log`，如无则说明 none。

## 质量门禁快速检查表

| 门禁 | Mechanical Gate | Human Approval Gate | 证据 | 最大轮次 |
|------|-----------------|---------------------|------|---------|
| 需求分析 | understanding.md 存在且包含关键字段 + memory check | 用户确认理解 | understanding.md | 1 |
| 需求评审 | spec.md 存在且 Phase 2 不产 tasks.md + memory check | 用户确认 spec | spec.md | 3 |
| 任务规划 | tasks.md 存在且任务可验收 + memory check | 用户确认任务规划 | tasks.md | 1 |
| 编码 | 编译成功且报告存在 + memory check | 用户确认提交评审 | coding_report.md | 1 |
| 编码评审 | 三份报告存在，Critical=0，Must Fix=0 + memory check | 用户确认评审摘要 | 3 份评审报告 | 2 |
| 单元测试 | 测试通过、测试数>0、覆盖率达标 + memory check | 用户确认测试结果 | test_report.md + JaCoCo | 1 |
| 测试评审 | test_review 存在，Must Fix=0 + memory check | 用户确认测试评审 | test_review.md | 2 |
| CI | ci_report 存在且成功 + memory check | 用户确认或规则放行 | ci_report.md | 1 |
| 部署验证 | deploy_report 存在，冒烟/回滚检查完成 + memory check | 用户确认部署验证 | deploy_report.md | 1 |
| 最终交付 | delivery-summary、summary、memory 完整性验证完成 | 用户最终确认 | delivery-summary.md | 1 |
