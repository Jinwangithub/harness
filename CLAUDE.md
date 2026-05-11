# CLAUDE.md — Harness Engineering 驱动开发

本项目使用 **Harness Engineering** 框架驱动 AI 编码，基于 `.harness/` 目录下的三层体系运行。

## 项目导航

- **入口地图**: `.harness/AGENTS.md` — 先读这里
- **角色定义**: `.harness/agents/` — Orchestrator / Reviewer / Test / Security
- **规则体系**: `.harness/rules/` — 工程结构、流程、编码、质量门禁
- **技能索引**: `.harness/skills/README.md` — agent-skills 映射表

## 开发工作流

按顺序执行：
```
需求 → /spec → /plan → /build → /review → /test → /ship
```

每个阶段结束后，Orchestrator 检查质量门禁，通过后进入下一阶段。

## Session 启动流程

1. 读取 `.harness/AGENTS.md` 获取项目上下文
2. 读取 `.harness/memory/` 获取历史经验和已知问题
3. 切换到 Orchestrator 模式推进开发

## 质量守则

- 绝不跳过阶段
- 绝不在没有验证的情况下声称"完成"
- 遇到失败优先回退到对应阶段修复，而非硬推

## 使用的 Plugin

- agent-skills (Addy Osmani) — 提供 20 个 Skill 工作流
- 技能路径: `~/.claude/plugins/cache/addy-agent-skills/agent-skills/1.0.0/skills/{name}/SKILL.md`
