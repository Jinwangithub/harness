# CLAUDE.md — Harness Engineering 驱动开发

本项目使用 **Harness Engineering** 框架驱动 AI 编码，基于 `.harness/` 目录下的三层体系运行。

## 项目导航

- **入口地图**: `.harness/AGENTS.md` — 先读这里
- **角色定义**: `.harness/agents/orchestrator.md` — 唯一的 Agent（编排中枢）
- **规则体系**: `.harness/rules/` — 工程结构、流程、编码、质量门禁
- **技能索引**: `.harness/skills/README.md` — 22 个本地 Skill 映射表
- **参考清单**: `.harness/references/` — 安全/性能/测试/可访问性审查清单
- **项目知识库**: `.harness/wiki/` — 业务领域、核心流程、外部集成（L3 按需查询）

## 开发工作流

按顺序执行：
```
需求 → /spec → /plan → /build → /review → /test → /ship
```

每个阶段结束后，Orchestrator 检查质量门禁，通过后进入下一阶段。

## Session 启动流程

1. 读取 `.harness/AGENTS.md` 获取项目上下文
2. 读取 `.harness/memory/` 获取历史经验和已知问题
3. 遇到未知业务概念时查阅 `.harness/wiki/`，不猜测规则
4. 切换到 Orchestrator 模式推进开发

## Session 结束检查

每个 Phase 出口和整个变更交付时，检查是否有需要记入 `.harness/memory/` 的内容：
- 做了架构决策？ → `decisions.log`
- 发现了 Agent 错误？ → `lessons-learned.md` + 修复 Harness 防止再犯
- 遇到已知限制？ → `known-issues.md`

## 质量守则

- 绝不跳过阶段
- 绝不在没有验证的情况下声称"完成"
- 遇到失败优先回退到对应阶段修复，而非硬推
- 不猜测业务规则 — wiki/ 中有相关文档时必须查阅
- Skill 按需加载：11 个核心 Skill 每流程必用，其他为条件触发（参见 AGENTS.md 流程图）

## Skill 来源

所有 Skill 文件位于 `.harness/skills/{name}/SKILL.md`，已内置于项目仓库。
团队使用无需安装任何插件，clone 即用。
