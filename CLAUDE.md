# CLAUDE.md — Harness Engineering 驱动开发

本项目使用 **Harness Engineering**：唯一 Orchestrator、规则权威源、本地 Skills、changes 归档和 memory 沉淀。

## 启动检查（每项必须明确完成才能继续）

- [ ] 已读 `.harness/AGENTS.md` → 知道 Authority Index 在哪
- [ ] 已读 `.harness/agents/orchestrator.md` → 知道当前 Dispatch Loop 规则
- [ ] 已读 `.harness/changes/INDEX.md` → 知道 active change 和 resume point
- [ ] 已读 `.harness/memory/lessons-learned.md` → 知道最近 3 条教训
- [ ] 遇到未知业务概念时查 `.harness/wiki/`，不猜测规则

## 权威源路径

| 主题 | 权威源 |
|------|--------|
| Orchestrator 调度 | `.harness/agents/orchestrator.md` |
| Flow Classifier、Lite/Standard、升级/回退 | `.harness/rules/02-development-workflow.md` |
| Mechanical Gate / Human Approval Gate / 检查表 | `.harness/rules/04-quality-gates.md` |
| Memory 模板与检查频率 | `.harness/memory/README.md` |
| 变更目录结构与产物模板 | `.harness/changes/README.md` |
| Skill 分层与触发策略 | `.harness/skills/README.md` |
| 用户操作方式 | `.harness/USAGE.md` |

## 不可违反原则摘要

- 未验证，不得声称完成、通过或交付。
- 未读相关代码、规则或证据，不得提出修改方案或放行结论。
- 先 Mechanical Gate，后 Human Approval Gate。
- Mechanical Gate `fail|blocked` 必须 Stop-the-Line，不得请求人工放行。
- 任意失败必须定位根因、回退修复并重新验证。
- 业务规则未知时必须查 `.harness/wiki/` 或记录疑问。
- Lite-flow 只降低阶段密度，不取消验证、fresh evidence、Memory、Stop-the-Line 或必要确认。
- Memory 触发即记录；完整模板见 `.harness/memory/README.md`。
- Skill 按 Core / Conditional / Support 分层按需加载；不默认全文展开。

## 基本工作流

```text
需求 → Flow Classifier → /spec → /plan → /build → /review → /test → /ship
```

实际步骤由 Flow Classifier 选择：Lite-flow 或 Standard-flow。完整定义见 `.harness/rules/02-development-workflow.md`。

## Skill 来源

所有 Skill 文件位于 `.harness/skills/{name}/SKILL.md`，已内置于项目仓库。加载策略以 `.harness/skills/README.md` 为准。
