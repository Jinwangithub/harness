# Orchestration Patterns

本文件是非权威参考模式。具体规则以 `.harness/rules/02-development-workflow.md`、`.harness/rules/04-quality-gates.md`、`.harness/skills/README.md`、`.harness/changes/README.md` 为准。

## 唯一 Orchestrator 模式

- `.harness/agents/orchestrator.md` 是唯一 Agent。
- Orchestrator 负责阶段推进、证据检查、归档、回退和用户确认。
- 不新增 `code-reviewer.md`、`security-auditor.md`、`test-engineer.md` 等独立 Agent。

### 隔离执行上下文模式

- 隔离执行上下文是唯一 Orchestrator 调度下的受限任务或审查泳道，不是新增 Agent 文件。
- 输入隔离：每个泳道收到同一份不可变输入包。
- 输出隔离：每个泳道只写自己的报告或返回自己的实现结果。
- 结论隔离：初次报告产出前不参考其他泳道结论。
- 权限隔离：隔离上下文不能推进 Phase、不能请求用户确认、不能修改无关文件。
- 汇总集中：只有 Orchestrator 能合并报告、判断 Mechanical Gate、请求 Human Approval Gate。

## Flow Classifier Pattern

- 新需求输入后先执行 Flow Classifier，再选择 Lite-flow / Standard-flow。
- 分类结果必须写入 `summary.md` 的 `## Flow Classification`：`flow`、`selection_basis`、`risk_flags`、`confirmation_policy`、`upgrade_triggers`。
- Lite-flow 适用于 typo、注释、格式、纯文档、README 小修、无行为变化小配置、单模块/少量文件、明确低风险行为变化、简单 bugfix、简单测试补充。
- Standard-flow 适用于新功能、跨模块、架构/数据/安全/权限/外部接口/迁移/性能/部署、需求不清。
- 风险扩大时必须 Stop-the-Line，更新 Flow Classification 并升级流程。

## Confirmation Policy Pattern

- `mandatory`：Standard-flow 使用，保持 CK1-CK9 阶段确认。
- `batched`：Lite-flow 使用，需求+简化计划确认一次，最终验证/评审摘要确认一次；中间 Mechanical Gate 通过则继续。
- Human Approval Gate 的时机可以按风险分级，但不能绕过 Mechanical Gate、fresh verification evidence、Memory check 或 Stop-the-Line。

## Standard Phase Locks Pattern

Standard-flow 使用强 Phase Lock：

- Entry Lock：前一阶段 Mechanical Gate、Human Approval、产物归档、Memory check 满足后才打开。
- Work Lock：当前阶段只做当前阶段允许动作。
- Exit Lock：当前阶段产物、Required Skill Load Record、Mechanical Gate、fresh evidence、Memory check 完成。
- Human Approval Lock：Mechanical Gate 通过后才能请求确认，确认前不进入下一阶段。
- Failure Lock：Mechanical Gate fail/blocked 时 Stop-the-Line。

完整判定以 `.harness/rules/02-development-workflow.md` 和 `.harness/rules/04-quality-gates.md` 为准。

## Phase 4 Isolation Pattern

Standard Phase 4 编码实现参考模式：

1. Orchestrator 准备不可变输入包。
2. Orchestrator 调度受限子上下文执行实现。
3. 子上下文只返回实现结果和变更摘要。
4. Orchestrator 汇总、编译验证、执行 Author/Self Review 和 CK4。

子上下文不推进 Phase、不请求确认、不判断 Gate、不运行 Phase 6 测试职责。

## Skill 调度模式

- 工程能力由 `.harness/skills/{name}/SKILL.md` 提供。
- Orchestrator 在对应 Phase 读取 Required Skills，并按风险触发 Support/Conditional Skills。
- Skill 产物和 Skill Load Record 必须归档到 `.harness/changes/{id}/`。

## 并行评审模式

Phase 5 可按风险并行调度：

- `code-review-and-quality`
- `security-and-hardening`
- `performance-optimization`

每个泳道使用同一份不可变输入包，独立写自己的报告，初次结论产出前不互相影响；报告完成后才由 Orchestrator 汇总，一次请求用户确认。

## Two-stage Review 模式

- Stage 1: Author/Self Review，在 Phase 4 编译后执行，由 `auto-check-and-optimize` 产出自检结论。
- Stage 2: Independent Review，在 Phase 5 执行隔离评审，由 review 泳道独立产出报告。
- Stage 2 不替代 Stage 1；Stage 1 不替代 Stage 2。
- Lite-flow 可使用压缩版 Two-stage Review：实现后自检 + 独立/隔离评审摘要。

## Verification-before-completion 模式

- 未列出新鲜验证证据，不得声明完成、通过或交付。
- 每个 Phase 或分级流程出口必须列出 Mechanical Gate 状态、命令/结果/报告路径/审查报告路径、`Memory recorded: {N} entries / none`。
- Human Approval Gate 只能在 Mechanical Gate 为 pass 且证据完整后请求。

## Mechanical Gate + Human Approval Gate

- Mechanical Gate：机械可验证，状态为 `pass|fail|blocked`。
- Human Approval Gate：用户确认，Mechanical Gate 通过后才可进入，等待时状态为 `pending-human`。
- 不允许用人工确认绕过失败的 Mechanical Gate。

## Stop-the-Line debugging 模式

任一 Mechanical Gate 为 `fail|blocked` 时：

1. 停止进入下一阶段，不请求人工放行。
2. 记录 failure evidence。
3. 复现或确认失败条件。
4. 定位 root cause。
5. 回退到对应 Phase 或分级流程步骤。
6. 修复并重新验证。
7. 如属于 Agent 错误或可复用教训，完整写入 `lessons-learned.md`。

## 回退模式

- 编译失败：回退 Phase 4。
- 测试失败：回退 Phase 6。
- CI 失败：回退 Phase 6。
- 需求不符：回退 Phase 1。
- 评审超轮次：升级人工决策。

## 流程分级模式

- Standard-flow：完整 Phase 1-10，适用于新功能、跨模块、架构/数据/安全/性能相关变更。
- Lite-flow：需求确认 → 简化计划 → 实现 → 验证/评审 → 交付，适用于低风险、明确需求的小变更。
- 新需求先执行 Flow Classifier；高风险或不明确走 Standard-flow，明确低风险选择 Lite-flow。
- 流程分级只是门禁密度和确认策略不同，不允许跳过验证、fresh verification evidence、Memory check、Stop-the-Line 或必要用户确认。

## Standalone Skill Mode 限制

- 仅用于用户明确要求的单点任务。
- 可直接调用评审、测试、部署清单等 Skill。
- 不得声明完整交付完成。
- 不得替代 Full Delivery Mode 的阶段证据和门禁。
