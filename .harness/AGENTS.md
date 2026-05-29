# AGENTS.md — 导航地图

> 这里是地图，不是手册。它帮助大模型快速理解系统结构和找到权威源。完整规则在权威源中定义。

## 系统概述

Harness Engineering 是 AI 辅助软件开发的工程治理框架，围绕五个核心支柱：

| 支柱 | 做什么 | 去哪儿找 |
|------|--------|----------|
| **规则（Rules）** | 决定"什么流程"：Flow 分类（Lite/Standard）、10 阶段流程、Phase 4 隔离、回退路径 | `.harness/rules/development-workflow.md` |
| **门禁（Gates）** | 决定"怎么验证"：Mechanical Gate（机械检查）、Human Approval Gate（人工确认）、Gate Record 模板 | `.harness/rules/quality-gates.md` |
| **Skills** | 决定"怎么做"：22 个本地技能按 Phase 调度（Required/Support/Conditional/Forbidden） | `.harness/skills/README.md` |
| **变更（Changes）** | 决定"怎么记"：每个需求独立归档目录、产物模板、`INDEX.md` 做恢复索引 | `.harness/changes/` |
| **记忆（Memory）** | 决定"学什么"：架构决策、经验教训、已知债务，触发即记录 | `.harness/memory/` |

**核心流程**：启动 → 读 `INDEX.md` 找 active 变更 → 读 `summary.md` 确认当前 Phase → 按 Phase 加载 Skills → 执行 Gate → 用户确认 → 下一步。

## 项目信息

- **工程框架**: Harness Engineering（唯一 Orchestrator + 本地 Skills）
- **运行入口**: `CLAUDE.md` → `.harness/agents/orchestrator.md`

## 文件导航

| 文件 | 角色 | 什么时候读 |
|------|------|-----------|
| `.harness/agents/orchestrator.md` | 唯一 Agent：角色、Iron Laws、启动流程、Authority Map、Dispatch Loop | 每次启动必读 |
| `.harness/changes/INDEX.md` | 变更注册表：active/done/abandoned，恢复索引 | 每次启动必读 |
| `.harness/rules/development-workflow.md` | Flow Classifier、Lite/Standard Phase 定义、Phase 4 隔离、回退路径 | 有新需求、分类、回退时读 |
| `.harness/rules/quality-gates.md` | Mechanical Gate / Human Approval Gate / 检查表 / Gate Record 模板 | 每个 Phase 出口时读 |
| `.harness/changes/README.md` | 变更目录结构、产物模板、summary 模板 | 创建新变更或归档时读 |
| `.harness/skills/README.md` | Skill Registry + Phase Skill Matrix（Required/Support/Conditional/Forbidden） | 每个 Phase 入口时读 |
| `.harness/memory/README.md` | Memory 类型、记录格式、检查频率 | 需要记录 memory 时读 |
| `.harness/memory/lessons-learned.md` | 历史经验教训 | 开始新任务时读最近 3 条 |
| `.harness/memory/decisions.log` | 架构决策记录 | 做重大设计决策时读 |
| `.harness/memory/known-issues.md` | 已知技术债务 | 遇到异常行为时读 |
| `.harness/references/` | 安全/性能/测试/可访问性审查清单 | 按需查阅 |
| `.harness/wiki/` | 项目业务知识 | 遇到未知业务概念时读 |
| `.harness/USAGE.md` | 人类用户使用指南 | Agent 不逐字加载 |

## Flow 速查

| Flow | 场景 | 关键区别 |
|------|------|----------|
| Lite-flow | typo、注释、格式、纯文档、小配置、简单 bugfix、单模块且低风险 | 4 步（L1-L4），batched 确认，5 个产物 |
| Standard-flow | 新功能、跨模块、架构/数据/安全/权限/外部接口/迁移/性能/部署、需求不清 | 10 Phase，逐 Phase 确认，完整产物链 |

完整 Flow Classifier 见 `.harness/rules/development-workflow.md`。
