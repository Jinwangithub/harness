# AGENTS.md — 导航地图

> 这里是地图，不是手册。完整规则在各权威源中定义。

## 项目信息

Harness Engineering 工程框架 — 唯一 Orchestrator + 本地 Skills。入口：`CLAUDE.md` → `.harness/agents/orchestrator.md`。

## 文件导航

| 文件 | 角色 | 什么时候读 |
|------|------|-----------|
| `.harness/agents/orchestrator.md` | Iron Laws（操作化）、Session Startup、Dispatch Loop、责任边界 | 每次启动必读 |
| `.harness/changes/INDEX.md` | 变更注册表：active/done/abandoned，恢复索引 | 每次启动必读 |
| `.harness/rules/development-workflow.md` | Flow Classifier、Lite/Standard Phase 定义、Phase 4 隔离、回退路径 | 有新需求、分类、回退时读 |
| `.harness/rules/quality-gates.md` | Mechanical Gate / Human Approval Gate / Gate Record 模板 | 每个 Phase 出口时读 |
| `.harness/changes/README.md` | 变更目录结构、产物模板、summary 模板 | 创建新变更或归档时读 |
| `.harness/skills/README.md` | Skill Registry + Phase Skill Matrix（Required/Support/Conditional/Forbidden） | 每个 Phase 入口时读 |
| `.harness/memory/README.md` | Memory 类型、记录格式、检查频率 | 需要记录 memory 时读 |
| `.harness/memory/lessons-learned.md` | 历史经验教训 | 开始新任务时读最近 3 条 |
| `.harness/memory/decisions.log` | 架构决策记录 | 做重大设计决策时读 |
| `.harness/memory/known-issues.md` | 已知技术债务 | 遇到异常行为时读 |
| `.harness/references/` | 安全/性能/测试/可访问性审查清单 | 按需查阅 |
| `.harness/wiki/` | 项目业务知识 | 遇到未知业务概念时读 |
| `.harness/USAGE.md` | 人类用户使用指南 | Agent 不逐字加载 |
