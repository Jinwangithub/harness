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

每个阶段结束后，Orchestrator 先检查 Mechanical Gate，再请求 Human Approval Gate；未列出新鲜验证证据，不得声明完成、通过或交付。

## 全局纪律摘要

- Harness Iron Laws：未验证不宣称完成；未读证据不放行；Mechanical Gate 失败不得人工绕过；任意失败必须 Stop-the-Line 根因排查；业务规则未知必须查 wiki 或记录疑问；隔离上下文不能替代 Orchestrator 决策；流程分级不能取消验证、证据、Memory 和用户确认。
- Two-stage Review：Phase 4 编译后自检是 Author/Self Review；Phase 5 三轴隔离评审是 Independent Review。
- 流程分级：默认 Standard-flow 完整十阶段；Mini-flow/Lite-flow 仅用于低风险小变更，必须记录降级依据，且仍需 Mechanical Gate、fresh verification evidence、Memory check 和必要用户确认。

## Session 启动流程

1. 读取 `.harness/AGENTS.md` 获取项目上下文
2. 读取 `.harness/memory/` 获取历史经验和已知问题
3. 扫描 `.harness/changes/` 下最新变更目录的 `summary.md`：
   - 如 `状态: 进行中` 且存在未完成 Phase → 从中断处恢复，从第一个 `- [ ]` Phase 继续
   - 如 `状态: 已完成` 或无变更目录 → 准备新变更
4. 遇到未知业务概念时查阅 `.harness/wiki/`，不猜测规则
5. 切换到 Orchestrator 模式，按 Session 启动流程推进开发

## Session 结束检查

每个 Phase 出口必须确认 Memory 已完整记录。每个 Phase 出口和整个变更交付时，MUST record to `.harness/memory/` if applicable:
- 做了架构决策？ → 完整写入 `decisions.log`（背景、方案、备选、理由、后果、决定人，6 字段全部必填）
- 发现了 Agent 错误？ → 完整写入 `lessons-learned.md`（问题、根因、影响、修复、预防，5 字段全部必填）+ 修复 Harness 防止再犯
- 遇到已知限制？ → 完整写入 `known-issues.md`（描述、影响范围、临时方案、计划修复，4 字段全部必填）
每次记录必须按模板完整填写，禁止简化。Phase 出口必须明确报告 "Memory recorded: {N} entries / none"。

## 质量守则

- 绝不跳过阶段
- 绝不在没有验证的情况下声称"完成"
- 遇到失败优先回退到对应阶段修复，而非硬推
- 不猜测业务规则 — wiki/ 中有相关文档时必须查阅
- Skill 按需加载：11 个核心 Skill 每流程必用，其他为条件触发（参见 AGENTS.md 流程图）

## Skill 来源

所有 Skill 文件位于 `.harness/skills/{name}/SKILL.md`，已内置于项目仓库。
团队使用无需安装任何插件，clone 即用。
