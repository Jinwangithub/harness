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
| Flow 分类与执行 | `.harness/rules/02-development-workflow.md` | Flow Classifier、Lite/Standard、十阶段、升级/回退 |
| 质量门禁 | `.harness/rules/04-quality-gates.md` | Mechanical Gate、Human Approval Gate、检查表 |
| 变更归档 | `.harness/changes/README.md` | 目录结构、产物模板、summary 模板 |
| Memory | `.harness/memory/README.md` | Memory 模板、检查频率、触发即记录 |
| Skill Registry | `.harness/skills/README.md` | Core/Conditional/Support 分层与按需加载 |
| 编码规范 | `.harness/rules/03-coding-standards.md` | 代码风格、约束 |
| 参考清单 | `.harness/references/` | 安全、性能、测试、可访问性审查清单 |
| 项目知识库 | `.harness/wiki/` | 业务领域、核心流程、外部集成 |
| 用户指南 | `.harness/USAGE.md` | 启动方式、确认点、FAQ |

## Flow 速查

| Flow | 场景 |
|------|------|
| Lite-flow | typo、注释、格式、纯文档、README 小修、小配置、简单 bugfix、简单测试补充、单模块/少量文件且明确低风险 |
| Standard-flow | 新功能、跨模块、架构/数据/安全/权限/外部接口/迁移/性能/部署、需求不清 |

完整 Flow Classifier、升级/回退规则见 `.harness/rules/02-development-workflow.md`。
