# 持久化记忆

本文件是 Memory 类型、完整模板和检查频率的权威源。

> **边界**：本文件只定义 Memory 类型、Check 块字段与检查频率。Gate 判定见 `.harness/rules/gates.md`，产物模板见 `.harness/changes/templates.md`；其他文件引用本文件的字段定义，不重述。

## 文件说明

| 文件 | 用途 | 触发条件 |
|------|------|----------|
| `decisions.log` | 架构决策记录 | 做出架构、流程、治理或长期维护决策 |
| `lessons-learned.md` | 经验教训 | 发现 Agent 错误、流程缺陷、可复用失败模式 |
| `known-issues.md` | 已知问题 | 遇到暂未修复的技术限制、环境限制或治理债务 |

## 触发即记录

任何 Flow 中一旦出现以下情况，必须立即记录，不能等到最终交付再补：

- 做了架构或治理决策（规则、模板、Skill、Gate、Flow、changes 结构等）→ `decisions.log`
- 发现 Agent 错误、流程教训、模板误导或 Skill 冲突 → `lessons-learned.md`
- 遇到已知限制、暂无法修复的问题或治理债务 → `known-issues.md`

记录必须使用下方完整模板，禁止简化字段。历史旧格式可作为 legacy evidence 保留；新记录必须使用完整模板。

## 检查频率

| Flow | 检查时机 |
|------|----------|
| Standard-flow | 每个 Phase 出口；触发即记录 |
| Lite-flow | L1 后 + L3 后；触发即记录 |

每次出口报告必须包含 `Memory recorded: {N} entries / none`。

## Memory Check 块（Standard-flow — 6 字段）

每个 Standard Phase artifact 或 `summary.md` Gate Record 必须填写：

```markdown
## Memory Check
- Architecture/governance decision made: {yes/no; evidence}
- Agent/process lesson found: {yes/no; evidence}
- Known issue or governance debt found: {yes/no; evidence}
- Memory action: {decisions.log / lessons-learned.md / known-issues.md / none}
- Memory recorded: {N} entries / none
- Template completeness verified: {yes/no/N/A}
```

`Template completeness verified` 对触发记录的条目必须为 `yes`；否则当前 Gate=`blocked`。

## Memory Check 块（Lite-flow — 3 字段）

Lite-flow 出口 (L1 后、L3 后) 必须填写：

```markdown
## Memory Check
- Architecture/governance decision made: {yes/no; evidence}
- Agent/process lesson found: {yes/no; evidence}
- Known issue or governance debt found: {yes/no; evidence}
```

如有触发条目，必须写完整模板到对应 memory 文件。

验证或 Gate 输出 `fail`/`blocked` 时，必须判断是否触发对应 Memory 文件记录。

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

### lessons-learned.md

```markdown
## YYYY-MM-DD | {标题}

- 问题: {发生了什么错误或流程缺陷}
- 根因: {根本原因，不只描述表象}
- 影响: {影响范围、风险或损失}
- 修复: {已采取的修复动作}
- 预防: {如何防止再犯，必要时说明 Harness 规则或文档修复}
```

### known-issues.md

```markdown
## YYYY-MM-DD | {标题}

- 描述: {限制或问题是什么}
- 影响范围: {影响哪些流程、模块、用户或验证动作}
- 临时方案: {当前如何绕开或降低风险}
- 计划修复: {后续修复方向或决策条件}
```
