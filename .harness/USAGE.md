# 实战操作指南

> 本文件面向人类用户。Agent 不应逐字加载此文件，应阅读 `.harness/agents/orchestrator.md` 和各权威源。
> 完整治理细节见 `.harness/rules/flow.md`、`.harness/rules/flow-lite.md`、`.harness/rules/flow-standard.md`、`.harness/rules/rollback.md` 和 `.harness/rules/gates.md`。

## 启动方式

新会话中输入：

```text
启动 Harness 模式
```

Claude Code 会从 `CLAUDE.md` → `.harness/agents/orchestrator.md` 启动，优先检查 `.harness/changes/INDEX.md` 恢复进行中的变更。

## 如何描述需求

直接描述目标、范围和约束。例如：

```text
需求：用户下单后发送订单确认通知，支持短信和邮件，用户可以选择偏好。
```

Orchestrator 会先执行 Flow Classifier，并在 `summary.md` 写入 Flow、Selection basis、Risk flags 等。

## 两种 Flow 简表

| Flow | 适用场景 | 用户会看到的确认点 | 必需产物 |
|------|----------|--------------------|----------|
| Lite-flow | typo、注释、格式、纯文档、README 小修、小配置、单模块/少量文件、明确低风险行为变化、简单 bugfix、简单测试补充 | batched：需求+计划一次，最终验证+交付一次 | `summary.md`（含 inline lite spec）、`request_analysis/checklist.md`、`verification_report.md`（含压缩评审） |
| Standard-flow | 新功能、跨模块、架构/数据/安全/权限/外部接口/迁移/性能/部署、需求不清 | mandatory：逐 Phase 确认 | 完整 Phase 1-10 产物 |

任何 Flow 都不能绕过 Mechanical Gate、fresh verification evidence、Memory check、Stop-the-Line 或必要 Human Approval Gate。

## 你会看到哪些确认点

- **Standard-flow**：mandatory，需求理解、spec、任务规划、编码、自检/评审、测试、CI/部署、最终交付等逐 Phase 确认。
- **Lite-flow**：batched，先确认需求+简化计划，再最终验证+交付确认。

Mechanical Gate 不通过时，Orchestrator 会先回退修复，不会请求你人工忽略失败。每个 Gate 请求你确认前，Orchestrator 应已运行 `.harness/tools/validate_change.sh --change {change-id}`；该命令失败时不得进入人工确认。shell 入口优先调用 Python full validator；如果 Python 不可用，会输出 `WARN: fallback.reduced` 并仅执行 reduced structural checks。

## 常用命令

| 你说 | 效果 |
|------|------|
| `启动 Harness 模式` | 读取入口地图并进入 Orchestrator 模式 |
| `新需求: ...` | 自动分类并创建变更归档 |
| `/spec` | 执行需求澄清/spec 相关流程 |
| `/plan` | 执行任务规划或 Lite checklist |
| `/build` | 按计划实现 |
| `/review` | 执行评审步骤或单点评审 |
| `/test` | 执行验证/测试步骤或单点测试 |
| `/ship` | 执行交付确认 |
| `恢复上次进度` | 从 `.harness/changes/INDEX.md` 和 `summary.md` 恢复 |
| `当前进度` | 查看当前 Phase / Flow step |
| `检查 Harness 结构` | 运行 `.harness/tools/validate_change.sh` 或指定 `--change {change-id}`；Python 不可用时会显示 `WARN: fallback.reduced` |

## 命令语义边界

| 命令 | Lite-flow | Standard-flow | 不能做什么 |
|------|-----------|---------------|------------|
| `/spec` | 产出/更新 L1 lite spec | Phase 1 understanding 或 Phase 2 spec | 不能跳过 Flow Classification 或 approval lock |
| `/plan` | 产出/更新 L1 checklist | Phase 3 tasks | 不能在 Phase 2 提前创建 tasks |
| `/build` | L2 实现 | Phase 4 实现 | 不能冒充 Phase 6 测试完成 |
| `/review` | L3 压缩评审 | Phase 5/7 评审 | 不能替代 Mechanical Gate |
| `/test` | L3 验证 | Phase 6 测试或阶段验证 | 不能单独声明交付完成 |
| `/ship` | L3 交付确认 | Phase 10 交付确认 | 不能在 pending-human 时标记已完成 |

## pending-human 时你需要做什么

当 Orchestrator 报告 `Human Approval Gate: pending-human`：

1. 查看交付摘要、验证证据和 Gate 状态。
2. 如果同意，明确回复 `approved` 或说明批准范围。
3. 如果不同意，回复 `rejected` 并说明问题；Orchestrator 应回退修复。
4. 在你确认前，`Completion lock` 必须保持 `locked`，变更不得标记为 `已完成`。

## 用户版验收简表

详细门禁见 `.harness/rules/gates.md`。用户验收时重点看：

```text
□ 选定 Flow 与任务风险匹配
□ Mechanical Gate 状态为 pass
□ validator 已通过，或只有明确可接受的 WARN
□ INDEX.md 与 summary.md 状态一致
□ fresh verification evidence 已列出
□ 必需产物已归档到 .harness/changes/{id}/
□ Memory recorded: {N} entries / none 已报告
□ 如有评审，Critical=0 且 Must Fix=0
□ 如有测试/CI/部署，结果和报告路径已列出
□ 需要你确认的 Human Approval Gate 已处理
```

## FAQ

**Q: 每次都要走十阶段吗？**
A: 不一定。Orchestrator 先分类；低风险任务走 Lite-flow，高风险或不明确需求走 Standard-flow。

**Q: 低风险/无行为变更小需求怎么处理？**
A: 也走 Lite-flow。内容可以更短，但仍保留统一产物、机械验证、Memory check 和必要确认。

**Q: Lite-flow 会生成 Standard-flow 的目录吗？**
A: 不会。Lite-flow 只生成 summary（含 inline lite spec）、checklist 和 verification report（含压缩评审）等三类产物。

**Q: 减少确认点是否等于取消 Human Approval Gate？**
A: 不是。确认点按风险分级减少，但不能绕过 Mechanical Gate、fresh evidence、Memory check 或 Stop-the-Line。

**Q: 只想评审或只想跑测试怎么办？**
A: 可以使用单点 Skill 任务，但它不等于完整交付流程完成。

**Q: 中途断开后如何继续？**
A: 输入 `启动 Harness 模式` 或 `恢复上次进度`，Orchestrator 会从 `INDEX.md` 和 `summary.md` 恢复上下文。
