# Skills Registry — 按需加载策略

本文件是 Skill 分层、触发策略和加载边界的权威源。所有 Skill 文件位于 `.harness/skills/{name}/SKILL.md`，仓库内置，无需安装插件。

## Core-meta

| Skill | 路径 | 用途 |
|------|------|------|
| `using-agent-skills` | `.harness/skills/using-agent-skills/SKILL.md` | Skill 发现、路由和索引维护 |
| `context-engineering` | `.harness/skills/context-engineering/SKILL.md` | 新会话、任务切换、上下文压缩与恢复 |
| `debugging-and-error-recovery` | `.harness/skills/debugging-and-error-recovery/SKILL.md` | Stop-the-Line、构建/测试/门禁失败排查 |

## Core-flow

| Skill | 路径 | 主用途 |
|------|------|--------|
| `idea-refine` | `.harness/skills/idea-refine/SKILL.md` | 需求澄清、问题收敛 |
| `spec-driven-development` | `.harness/skills/spec-driven-development/SKILL.md` | PRD / spec 编写 |
| `planning-and-task-breakdown` | `.harness/skills/planning-and-task-breakdown/SKILL.md` | 任务拆解、验收条件 |
| `incremental-implementation` | `.harness/skills/incremental-implementation/SKILL.md` | 垂直切片增量实现 |
| `auto-check-and-optimize` | `.harness/skills/auto-check-and-optimize/SKILL.md` | Phase 4 出口 Author/Self Review；不替代 Phase 5 |
| `test-driven-development` | `.harness/skills/test-driven-development/SKILL.md` | 测试编写、覆盖率验证 |
| `code-review-and-quality` | `.harness/skills/code-review-and-quality/SKILL.md` | 代码/测试质量评审 |
| `ci-cd-and-automation` | `.harness/skills/ci-cd-and-automation/SKILL.md` | CI 验证与自动化 |
| `shipping-and-launch` | `.harness/skills/shipping-and-launch/SKILL.md` | 部署、冒烟、发布检查 |
| `documentation-and-adrs` | `.harness/skills/documentation-and-adrs/SKILL.md` | 交付摘要、ADR、文档沉淀 |

## Conditional-domain

| Skill | 路径 | 触发条件 |
|------|------|----------|
| `source-driven-development` | `.harness/skills/source-driven-development/SKILL.md` | 引入新框架、库、API 或需要官方文档依据 |
| `api-and-interface-design` | `.harness/skills/api-and-interface-design/SKILL.md` | 设计 API、模块边界、接口契约 |
| `frontend-ui-engineering` | `.harness/skills/frontend-ui-engineering/SKILL.md` | 前端 UI、组件、交互实现 |
| `browser-testing-with-devtools` | `.harness/skills/browser-testing-with-devtools/SKILL.md` | 浏览器端调试、页面行为验证 |
| `security-and-hardening` | `.harness/skills/security-and-hardening/SKILL.md` | 安全、auth、权限、输入边界、OWASP 风险 |
| `performance-optimization` | `.harness/skills/performance-optimization/SKILL.md` | 性能风险、瓶颈分析、容量或延迟目标 |
| `code-simplification` | `.harness/skills/code-simplification/SKILL.md` | 评审发现复杂、冗余、可简化代码 |
| `deprecation-and-migration` | `.harness/skills/deprecation-and-migration/SKILL.md` | 废弃旧功能、迁移接口、兼容策略 |

## Support-macro / Support-workflow

| Skill | 路径 | 触发条件 |
|------|------|----------|
| `git-workflow-and-versioning` | `.harness/skills/git-workflow-and-versioning/SKILL.md` | 用户要求提交、分支、版本或发布协作 |

## Flow-tiered 加载策略

| Flow | 默认策略 |
|------|----------|
| Mini-flow | 默认不加载阶段 Skill；除非需要内容审查、失败恢复或用户明确要求单点 Skill。 |
| Lite-flow | 只加载完成 lite spec、checklist、verification、review 所需的最少 Skill；按风险触发 Conditional-domain。 |
| Standard-flow | 按 Phase 主干加载 Core-flow；Conditional-domain 按风险触发；Core-meta 按上下文或失败触发。 |

## 加载边界

- `auto-check-and-optimize` 是 Phase 4 出口自检宏，只承载 Author/Self Review，不替代 Phase 5 Independent Review。
- `security-and-hardening` 不默认全文加载；安全、auth、权限、外部输入或风险标记触发时加载。
- `performance-optimization` 不默认全文加载；性能风险、容量/延迟目标或评审需要时加载。
- `source-driven-development` 不默认全文加载；新增或不熟悉依赖、框架、API 时加载。
- `browser-testing-with-devtools` 不默认全文加载；浏览器端行为验证或前端调试时加载。
- `git-workflow-and-versioning` 不默认全文加载；仅在用户要求 git 操作或流程进入提交/版本管理动作时加载。

## Standard-flow 主干映射

| Phase | 主 Skill | 条件 Skill |
|------|----------|------------|
| Phase 1 | `idea-refine` | `context-engineering` |
| Phase 2 | `spec-driven-development` | `source-driven-development` |
| Phase 3 | `planning-and-task-breakdown` | `api-and-interface-design` |
| Phase 4 | `incremental-implementation`、`auto-check-and-optimize` | `frontend-ui-engineering`、`source-driven-development`、`api-and-interface-design` |
| Phase 5 | `code-review-and-quality` | `security-and-hardening`、`performance-optimization`、`code-simplification` |
| Phase 6 | `test-driven-development` | `browser-testing-with-devtools` |
| Phase 7 | `code-review-and-quality` | `test-driven-development` |
| Phase 8 | `ci-cd-and-automation` | `git-workflow-and-versioning`、`debugging-and-error-recovery` |
| Phase 9 | `shipping-and-launch` | `performance-optimization`、`security-and-hardening` |
| Phase 10 | `documentation-and-adrs` | `deprecation-and-migration` |

任何 Flow 都不得通过“少加载 Skill”跳过 Mechanical Gate、fresh verification evidence、Memory check、Stop-the-Line 或必要 Human Approval Gate。
