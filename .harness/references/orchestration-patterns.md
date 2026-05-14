# Orchestration Patterns

## 唯一 Orchestrator 模式

- `.harness/agents/orchestrator.md` 是唯一 Agent。
- Orchestrator 负责阶段推进、证据检查、归档、回退和用户确认。
- 不新增 `code-reviewer.md`、`security-auditor.md`、`test-engineer.md` 等独立 Agent。

## Skill 调度模式

- 工程能力由 `.harness/skills/{name}/SKILL.md` 提供。
- Orchestrator 在对应 Phase 读取 Skill 并按流程执行。
- Skill 产物必须归档到 `.harness/changes/{id}/`。

## 并行评审模式

Phase 5 并行调度：

- `code-review-and-quality`
- `security-and-hardening`
- `performance-optimization`

三份报告全部完成后再汇总，一次请求用户确认。

## Mechanical Gate + Human Approval Gate

- Mechanical Gate：机器可验证或有明确证据路径，状态为 `pass|fail|blocked`。
- Human Approval Gate：用户确认，Mechanical Gate 通过后才可进入，等待时状态为 `pending-human`。
- 不允许用人工确认绕过失败的 Mechanical Gate。

## 回退模式

- 编译失败：回退 Phase 4。
- 测试失败：回退 Phase 6。
- CI 失败：回退 Phase 6。
- 需求不符：回退 Phase 1。
- 评审超轮次：升级人工决策。

## Standalone Skill Mode 限制

- 仅用于用户明确要求的单点任务。
- 可直接调用评审、测试、部署清单等 Skill。
- 不得声明完整交付完成。
- 不得替代 Full Delivery Mode 的阶段证据和门禁。
