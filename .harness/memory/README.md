# 持久化记忆

本文件是 Memory 类型、完整模板和检查频率的权威源。

## 用途

- 保存跨会话的关键决策、错误教训和已知限制。
- 减少重复排查和规则分叉。
- 使 Harness 能从过去的决策和错误中持续改进。

## 文件说明

| 文件 | 用途 | 触发条件 |
|------|------|----------|
| `decisions.log` | 架构决策记录 | 做出架构、流程、治理或长期维护决策 |
| `lessons-learned.md` | 经验教训 | 发现 Agent 错误、流程缺陷、可复用失败模式 |
| `known-issues.md` | 已知问题 | 遇到暂未修复的技术限制、环境限制或治理债务 |

## 触发即记录

任何 Flow 中一旦出现以下情况，必须立即记录，不能等到最终交付再补：

- 做了架构决策 → 写入 `decisions.log`。
- 做了治理规则、模板、Skill、Gate、Flow、changes 结构或长期维护决策 → 高概率写入 `decisions.log`。
- 发现 Agent 错误、流程教训、模板误导或 Skill 冲突 → 写入 `lessons-learned.md`。
- 遇到已知限制、暂无法修复的问题或治理债务 → 写入 `known-issues.md`。

记录必须使用下方完整模板，禁止简化字段。历史旧格式 Memory 可作为 legacy evidence 保留，不强制重写；新记录必须使用完整模板，不得复制旧的不完整条目格式。

## Memory 检查频率

| Flow | 检查频率 |
|------|----------|
| Standard-flow | 每个 Phase 出口检查；触发即记录 |
| Lite-flow | 计划确认后、最终验证/交付前检查；触发即记录 |

每次出口报告必须包含：`Memory recorded: {N} entries / none`。每个 Phase/Flow step artifact 或 `summary.md` Gate Record 必须引用或填写下方 Memory Check 块。

## Memory Check 块

```markdown
## Memory Check
- Architecture/governance decision made: {yes/no; evidence}
- Agent/process lesson found: {yes/no; evidence}
- Known issue or governance debt found: {yes/no; evidence}
- Memory action: {decisions.log / lessons-learned.md / known-issues.md / none}
- Memory recorded: {N} entries / none
- Template completeness verified: {yes/no/N/A}
```

`Template completeness verified` 对触发记录的条目必须为 `yes`；如无法完整记录则当前 Gate=`blocked`。

## Validator 与 Memory Check

`.harness/scripts/harness-validate.sh` 的输出可作为 Mechanical Gate evidence，但不替代 Memory Check。

- validator 输出 `FAIL` 且原因属于流程、模板、Gate、changes 或 Memory 规则缺陷时，必须判断是否触发 `lessons-learned.md` 或 `known-issues.md`。
- validator 输出 `WARN` 且确认是历史归档不一致、legacy summary 或暂不批量重写的治理债务时，必须判断是否触发 `known-issues.md`。
- 新增 changes index、validator、project Skill extension slot 等长期治理选择，必须记录 `decisions.log`。
- 多个 `状态: 进行中`、`已完成` + `pending-human`、summary 字段不一致导致恢复困难，属于流程教训，必须记录 `lessons-learned.md`。

## 完整模板

### decisions.log

```text
YYYY-MM-DD | {标题}
- 背景: {决策背景，为什么需要决定}
- 方案: {选择的方案}
- 备选: {考虑过但未选择的方案}
- 理由: {为什么选择该方案}
- 后果: {副作用、成本、后续影响}
- 决定人: {谁做的决定}
```

必填字段：背景、方案、备选、理由、后果、决定人。

### lessons-learned.md

```markdown
## YYYY-MM-DD | {标题}

- 问题: {发生了什么错误或流程缺陷}
- 根因: {根本原因，不只描述表象}
- 影响: {影响范围、风险或损失}
- 修复: {已采取的修复动作}
- 预防: {如何防止再犯，必要时说明 Harness 规则或文档修复}
```

必填字段：问题、根因、影响、修复、预防。

### known-issues.md

```markdown
## YYYY-MM-DD | {标题}

- 描述: {限制或问题是什么}
- 影响范围: {影响哪些流程、模块、用户或验证动作}
- 临时方案: {当前如何绕开或降低风险}
- 计划修复: {后续修复方向或决策条件}
```

必填字段：描述、影响范围、临时方案、计划修复。

## Phase 出口 Memory 强制问答（必须逐项回答，有内容才记录）

- Q1: 本 Phase 是否做了任何非显而易见的技术或治理决策？→ 是则记入 `decisions.log`
- Q2: 本 Phase 是否遇到规则未覆盖的情况或已知限制？→ 是则记入 `known-issues.md`
- Q3: 本 Phase 是否有"下次应该更早做"的事？→ 是则记入 `lessons-learned.md`

## 完整性检查

Memory check 必须回答：

1. 本阶段/步骤是否做出架构或治理决策？
2. 是否发现 Agent 错误、流程错误或可复用教训？
3. 是否遇到尚未修复的技术限制或治理债务？
4. 如触发记录，条目是否包含对应模板的全部字段？
5. 出口报告是否列出 `Memory recorded: {N} entries / none`？
