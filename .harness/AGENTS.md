# AGENTS.md — Harness Engineering 导航地图

> 这里是地图，不是手册。完整规则只在权威源中定义，入口文件只保留摘要和链接。

## 项目信息

- **工程框架**: Harness Engineering（唯一 Orchestrator + 本地 Skills）
- **运行入口**: `CLAUDE.md` → `.harness/AGENTS.md` → `.harness/agents/orchestrator.md`
- **治理原则**: 地图薄、规则清、按需加载、证据足够

## Authority Index

| 主题 | 权威源 | 说明 |
|------|--------|------|
| Orchestrator 角色与调度 | `.harness/agents/orchestrator.md` | 唯一 Agent、Dispatch Loop、出口协议 |
| Flow 分类与执行 | `.harness/rules/02-development-workflow.md` | Flow Classifier、Mini/Lite/Standard、十阶段、升级/回退 |
| 质量门禁 | `.harness/rules/04-quality-gates.md` | Mechanical Gate、Human Approval Gate、检查表 |
| 变更归档 | `.harness/changes/README.md` | 目录结构、产物模板、summary 模板 |
| Memory | `.harness/memory/README.md` | Memory 模板、检查频率、触发即记录 |
| Skill Registry | `.harness/skills/README.md` | Core/Conditional/Support 分层与按需加载 |
| 工程结构 | `.harness/rules/01-engineering-structure.md` | 目录、命名、分层 |
| 编码规范 | `.harness/rules/03-coding-standards.md` | 代码风格、约束 |
| 参考清单 | `.harness/references/` | 安全、性能、测试、可访问性审查清单 |
| 项目知识库 | `.harness/wiki/` | 业务领域、核心流程、外部集成 |
| 用户指南 | `.harness/USAGE.md` | 启动方式、确认点、FAQ |

## Flow 速查

| Flow | 场景 | 产物 |
|------|------|------|
| Mini-flow | typo、注释、格式、纯文档、README 小修、无行为变化小配置 | `summary.md`、`verification_report.md` |
| Lite-flow | 单模块/少量文件、明确低风险行为变化、简单 bugfix、简单测试补充 | `summary.md`、`request_analysis/lite_spec.md`、`request_analysis/checklist.md`、`verification_report.md`、`review_summary.md` |
| Standard-flow | 新功能、跨模块、架构/数据/安全/权限/外部接口/迁移/性能/部署、需求不清 | 完整 Phase 1-10 产物 |

完整 Flow Classifier、Confirmation Policy、升级/回退规则见 `.harness/rules/02-development-workflow.md`。

## 启动与恢复

1. 读取本地图和 `.harness/agents/orchestrator.md`。
2. 按 `.harness/memory/README.md` 检查历史 Memory。
3. 扫描 `.harness/changes/` 最新 `summary.md`：
   - `状态: 进行中` → 从第一个未完成 Phase / Flow step 恢复。
   - `状态: 已完成` 或无变更目录 → 准备新变更。
4. 新需求先执行 Flow Classifier。

## 不可违反摘要

- 先 Mechanical Gate，后 Human Approval Gate。
- 未列出 fresh verification evidence，不得声明完成、通过或交付。
- Mechanical Gate `fail|blocked` 必须 Stop-the-Line，不得请求人工放行。
- 未知业务规则必须查 `.harness/wiki/` 或记录疑问。
- Memory 触发即记录，模板见 `.harness/memory/README.md`。
- Skill 按 `.harness/skills/README.md` 分层按需加载，不默认全文展开。
