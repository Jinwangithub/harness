# CLAUDE.md — Harness Engineering

> 本项目使用 Harness Engineering 工程框架。
> 启动时从 `.harness/agents/orchestrator.md` 进入，按 Session Startup 流程执行。

## 文件导航

| 文件 | 什么时候读 |
|------|-----------|
| `.harness/agents/orchestrator.md` | 每次启动必读 — Iron Laws、Session Startup、Dispatch Loop |
| `.harness/changes/INDEX.md` | 每次启动必读 — 恢复 active 变更 |
| `.harness/rules/flow.md` | 有新需求、Flow Classifier、Flow 路由时读 |
| `.harness/rules/flow-lite.md` | Lite-flow Step 入口卡片和执行顺序时读 |
| `.harness/rules/flow-standard.md` | Standard-flow Phase 入口卡片、Phase 4 隔离原则时读 |
| `.harness/rules/rollback.md` | Gate fail/blocked、风险扩大或回退路径时读 |
| `.harness/rules/gates.md` | 每个 Phase/Step 出口时读 |
| `.harness/tools/validate_change.py` | Session Startup 后、每个 Gate 前、完成声明前运行 |
| `.harness/skills/README.md` | 需要确认 Skill 路径约定时读 |
| `.harness/changes/structure.md` | 创建新变更或归档时读 |
| `.harness/changes/templates.md` | 需要产物模板时读 |
| `.harness/memory/README.md` | 需要记录 memory 时读 |
| `.harness/memory/lessons-learned.md` | 开始新任务时读最近 3 条 |
| `.harness/memory/known-issues.md` | 遇到异常行为时读 |
| `.harness/wiki/README.md` | 遇到未知业务概念时读 |
| `.harness/USAGE.md` | 人类用户指南，Agent 不逐字加载 |
