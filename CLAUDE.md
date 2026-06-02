# CLAUDE.md — Harness Engineering

> 本项目使用 Harness Engineering 工程框架。
> 启动时从 `.harness/agents/orchestrator.md` 进入，按 Session Startup 流程执行。

## 项目状态

| 模块 | 状态 |
|------|------|
| 规则体系（rules/） | 已可用 |
| 流程体系（Flow + Gate） | 已可用（Lite + Standard） |
| Memory 系统（memory/） | 已可用 |
| Skill 内容 | 框架完整，待项目适配填充 |
| Wiki 业务知识 | 未初始化，接入项目后必须填充 |
| 脚本化验证 | 未实现，当前依赖 Agent 自我报告 |

## 文件导航

| 文件 | 什么时候读 |
|------|-----------|
| `.harness/agents/orchestrator.md` | 每次启动必读 — Iron Laws、Session Startup、Dispatch Loop |
| `.harness/changes/INDEX.md` | 每次启动必读 — 恢复 active 变更 |
| `.harness/rules/flow.md` | 有新需求、分类、回退时读 |
| `.harness/rules/gates.md` | 每个 Phase 出口时读 |
| `.harness/skills/matrix.md` | 每个 Phase 入口时读 — Required/Forbidden |
| `.harness/skills/registry.md` | 需要查找 Skill 时读 |
| `.harness/changes/structure.md` | 创建新变更或归档时读 |
| `.harness/changes/templates.md` | 需要产物模板时读 |
| `.harness/memory/README.md` | 需要记录 memory 时读 |
| `.harness/memory/lessons-learned.md` | 开始新任务时读最近 3 条 |
| `.harness/memory/known-issues.md` | 遇到异常行为时读 |
| `.harness/references/checklists.md` | 安全/性能/测试/可访问性审查时按需读 |
| `.harness/wiki/README.md` | 遇到未知业务概念时读 |
| `.harness/USAGE.md` | 人类用户指南，Agent 不逐字加载 |
