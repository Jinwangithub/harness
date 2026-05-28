# CLAUDE.md — Harness Engineering 驱动开发

本项目使用 **Harness Engineering**：唯一 Orchestrator、规则权威源、本地 Skills、changes 归档和 memory 沉淀。

## 启动检查（每项必须明确完成才能继续）

**强制启动（每次必须）：**
- [ ] 已读 `.harness/agents/orchestrator.md` → 角色、Dispatch Loop、Iron Laws、Authority Map
- [ ] 已读 `.harness/changes/INDEX.md` → active change 和 resume point

**按需启动（有 active change 时才读）：**
- [ ] 已读 active change 的 `summary.md` → 当前状态和 resume point
- [ ] 已读 `.harness/memory/lessons-learned.md` → 最近 3 条教训（仅开始新任务时）

**`.harness/AGENTS.md` 仅在首次接触项目时作为导航地图读取，不是每次启动必读。**

- [ ] 遇到未知业务概念时查 `.harness/wiki/`，不猜测规则

## Skill 来源

所有 Skill 文件位于 `.harness/skills/{name}/SKILL.md`，已内置于项目仓库。加载策略以 `.harness/skills/README.md` 为准。
