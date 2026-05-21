# 实战操作指南

面向用户的 Harness 使用说明。完整治理细节见 `.harness/rules/02-development-workflow.md` 和 `.harness/rules/04-quality-gates.md`。

## 启动方式

新会话中输入：

```text
启动 Harness 模式
```

Claude Code 会读取 `CLAUDE.md`、`.harness/AGENTS.md` 和 Orchestrator 规则，检查 `.harness/changes/` 与 `.harness/memory/`，然后准备处理新需求或恢复进行中的变更。

## 如何描述需求

直接描述目标、范围和约束。例如：

```text
需求：用户下单后发送订单确认通知，支持短信和邮件，用户可以选择偏好。
```

Orchestrator 会先执行 Flow Classifier，并在 `summary.md` 写入：

- Flow
- Selection basis
- Risk flags
- Confirmation policy
- Upgrade triggers

## 两种 Flow 简表

| Flow | 适用场景 | 用户会看到的确认点 | 必需产物 |
|------|----------|--------------------|----------|
| Lite-flow | typo、注释、格式、纯文档、README 小修、小配置、单模块/少量文件、明确低风险行为变化、简单 bugfix、简单测试补充 | batched：需求+简化计划一次，最终验证/评审摘要一次 | `summary.md`、`request_analysis/lite_spec.md`、`request_analysis/checklist.md`、`verification_report.md`、`review_summary.md` |
| Standard-flow | 新功能、跨模块、架构/数据/安全/权限/外部接口/迁移/性能/部署、需求不清 | mandatory：逐 Phase 确认 | 完整 Phase 1-10 产物 |

任何 Flow 都不能绕过 Mechanical Gate、fresh verification evidence、Memory check、Stop-the-Line 或必要 Human Approval Gate。

## 你会看到哪些确认点

- **Standard-flow**：mandatory，需求理解、spec、任务规划、编码、自检/评审、测试、CI/部署、最终交付等逐 Phase 确认。
- **Lite-flow**：batched，先确认需求+简化计划，再确认最终验证/评审摘要。

Mechanical Gate 不通过时，Orchestrator 会先回退修复，不会请求你人工忽略失败。

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
| `恢复上次进度` | 从 `.harness/changes/` 最新未完成项恢复 |
| `当前进度` | 查看当前 Phase / Flow step |

## 用户版验收简表

详细门禁见 `.harness/rules/04-quality-gates.md`。用户验收时重点看：

```text
□ 选定 Flow 与任务风险匹配
□ Mechanical Gate 状态为 pass
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
A: 不会。Lite-flow 只生成 lite spec、checklist、verification report 和 review summary 等五类产物。

**Q: 减少确认点是否等于取消 Human Approval Gate？**
A: 不是。确认点按风险分级减少，但不能绕过 Mechanical Gate、fresh evidence、Memory check 或 Stop-the-Line。

**Q: 只想评审或只想跑测试怎么办？**
A: 可以使用单点 Skill 任务，但它不等于完整交付流程完成。

**Q: 中途断开后如何继续？**
A: 输入 `启动 Harness 模式` 或 `恢复上次进度`，Orchestrator 会读取 `.harness/changes/` 和 `.harness/memory/` 恢复上下文。
