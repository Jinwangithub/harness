# Skills Registry — 按需加载策略

本文件是 Skill Registry、Standard-flow Phase Skill Matrix、Skill 角色术语、触发策略和 Harness Integration Override 的权威源。所有 Skill 文件位于 `.harness/skills/{name}/SKILL.md`，仓库内置，无需安装插件。

## Skill 角色术语

| 术语 | 含义 | Gate 影响 |
|------|------|-----------|
| Required Skill | 当前 Phase 必须读取/调用的 Skill | 未加载或无 Skill Load Record 时 Mechanical Gate=`blocked` |
| Support Skill | 阶段支持能力，按上下文需要加载 | 需要但未加载时记录原因；不默认阻塞 |
| Conditional Skill | 由 risk flag、任务类型、证据缺口或失败触发 | 触发条件成立但未加载时 Mechanical Gate=`blocked` |
| Forbidden/Deferred | 当前 Phase 不得执行的能力或动作，必须延后或回退 | 执行后 Gate=`fail` 或 `blocked` |

## Harness Integration Override

当通用 Skill 指南与 Harness 阶段边界冲突时，以 Harness 权威源为准：

- 流程顺序与 Phase Lock 以 `.harness/rules/02-development-workflow.md` 为准。
- Gate 语义与机械验证以 `.harness/rules/04-quality-gates.md` 为准。
- 产物模板与 Skill Load Record 以 `.harness/changes/README.md` 为准。
- Required Skill 原始输出须通过 `.harness/changes/README.md` 映射为 Harness artifact template。
- Standard-flow Skill Matrix 以本文为准。
- `auto-check-and-optimize` 在 Phase 4 只代表 Author/Self Review，不能替代 Phase 5 Independent Review。
- git 操作只在用户要求或对应发布/版本场景中执行。

## Skill Load Lifecycle

每个 Phase/Step 入口按以下顺序执行：

1. 评估当前 Phase/Step 的 Required Skills 与 Conditional Skills 触发条件。
2. Required Skill 必须先读取/调用，再产出本阶段 artifact。
3. Conditional Skill 触发时必须读取/调用；未触发也要记录 trigger evaluation。
4. 写入 Skill Load Record，字段和状态以 `.harness/changes/README.md` 为准。
5. Required Skill 未加载，或 Conditional Skill 触发但未加载时，Mechanical Gate=`blocked`。

## Raw Skill Template Suppression

| Skill | Harness Override |
|-------|------------------|
| `spec-driven-development` | Harness Phase 2 只输出 `request_analysis/spec.md`；禁止在 Phase 2 输出 plan/tasks/implement。 |
| `planning-and-task-breakdown` | Harness Phase 3 只输出 `request_analysis/tasks.md`；禁止 `# Implementation Plan` 和 `### Phase 1/2/3` 作为 Harness tasks 模板。 |
| `idea-refine` | Harness Phase 1 输出映射到 `request_analysis/understanding.md`；不默认写 `docs/ideas/`。 |
| `incremental-implementation` | Harness Phase 4 中 “commit” 解释为归档实现证据；除非用户明确要求，不执行 git commit。 |
| `auto-check-and-optimize` | 只作为 Phase 4 Author/Self Review；编译命令来自 `spec.md`，不硬编码 Maven；不替代 Phase 5。 |
| `documentation-and-adrs` | ADR 不替代 Harness Memory，也不替代 `delivery-summary.md`。 |
| `using-agent-skills` | 只作发现辅助，不覆盖本文 Harness Skill Matrix。 |

## Lite-flow Skill Mapping

Lite-flow 可借用 Skill 概念完成 lite spec、checklist、verification、review，但只能把必要字段抽取到 Lite artifacts。Lite-flow 不得输出 Standard artifacts（`spec.md`、`tasks.md`、`coding/`、`unit_test/`、`ci_result/`、`deployment/`、`delivery-summary.md`），除非升级 Standard-flow。

## Slash / Natural Language Command Boundaries

`/spec`、`/plan`、`/build`、`/review`、`/test`、`/ship` 和等价自然语言命令只是请求 Orchestrator 执行对应能力，不是绕过 Flow 的授权。

| Command | Lite-flow meaning | Standard-flow meaning | Boundary |
|---------|-------------------|-----------------------|----------|
| `/spec` | L1 lite spec / requirement clarification | Phase 1 understanding or Phase 2 spec, depending on current lock | Cannot skip Flow Classification or pending approval |
| `/plan` | L1 checklist | Phase 3 tasks after approved spec | Cannot create `tasks.md` before Phase 3 |
| `/build` | L2 implementation | Phase 4 implementation after approved tasks | Cannot run Phase 6 tests as completion evidence |
| `/review` | L3 compressed review | Phase 5 independent review or Phase 7 test review | Cannot replace Mechanical Gate |
| `/test` | L3 verification | Phase 6 tests or Phase-specific validation | Cannot mark delivery complete by itself |
| `/ship` | L4 final confirmation | Phase 10 delivery confirmation | Requires Completion Claim Gate and Human Approval |

## Project-specific Skills

Project-specific Skills live under `.harness/skills/project/`. They may add local domain or project conventions, but cannot override Harness authority sources for workflow, gates, changes, memory, or Skill role semantics. If a project Skill conflicts with `.harness/rules/02-development-workflow.md`, `.harness/rules/04-quality-gates.md`, `.harness/changes/README.md`, `.harness/memory/README.md`, or this registry, Orchestrator must follow the authority source and record the conflict.

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
| Lite-flow | 只加载完成 lite spec、checklist、verification、review 所需的最少 Skill；按风险触发 Conditional-domain。 |
| Standard-flow | 按 Phase Skill Matrix 加载 Required Skills；Support/Conditional 按触发条件加载；Core-meta 按上下文或失败触发。 |

任何 Flow 都不得通过“少加载 Skill”跳过 Mechanical Gate、fresh verification evidence、Memory check、Stop-the-Line 或必要 Human Approval Gate。

## Standard-flow Phase Skill Matrix

| Phase | Required Skills | Support Skills | Conditional Skills | Forbidden/Deferred |
|------|-----------------|----------------|--------------------|--------------------|
| Phase 1 | `idea-refine` | `context-engineering` | none | 不创建 `spec.md`、`tasks.md`；不实现代码 |
| Phase 2 | `spec-driven-development` | none | `source-driven-development`、`api-and-interface-design`、`security-and-hardening`、`performance-optimization` | 不创建 `tasks.md`；不实现代码 |
| Phase 3 | `planning-and-task-breakdown` | `api-and-interface-design` | `security-and-hardening`、`deprecation-and-migration` | 不实现代码；不运行 Phase 6 测试职责 |
| Phase 4 | `incremental-implementation`、`auto-check-and-optimize` | none | `frontend-ui-engineering`、`source-driven-development`、`api-and-interface-design` | 不推进 Phase；不请求确认；不判断 Gate；不运行 Phase 6 测试职责；不冒充 Phase 5 Independent Review |
| Phase 5 | `code-review-and-quality` | none | `security-and-hardening`、`performance-optimization`、`code-simplification` | 不直接实现修复；Must Fix/Critical 回退 Phase 4 |
| Phase 6 | `test-driven-development` | none | `browser-testing-with-devtools`、`debugging-and-error-recovery` | 不改需求/spec；实现缺陷回退 Phase 4 |
| Phase 7 | `code-review-and-quality`、`test-driven-development` | none | none | 不扩大测试范围为新需求；发现缺口回退 Phase 6 或更早 |
| Phase 8 | `ci-cd-and-automation` | `debugging-and-error-recovery` | none | 不发布；不绕过失败 CI |
| Phase 9 | `shipping-and-launch` | none | `security-and-hardening`、`performance-optimization` | 不替代最终交付确认；部署风险回退 Phase 8/9 |
| Phase 10 | `documentation-and-adrs` | none | `git-workflow-and-versioning`、`deprecation-and-migration` | 未经用户要求不执行 git 提交/推送；不改实现代码 |

## 加载边界

- Required Skill 必须在对应 Phase 读取/调用，并写入 Skill Load Record。
- Conditional Skill 的触发依据必须来自 risk flag、任务类型、证据缺口、评审发现或失败现象。
- Support Skill 只在有明确支持需求时加载。
- `security-and-hardening` 不默认全文加载；安全、auth、权限、外部输入或风险标记触发时加载。
- `performance-optimization` 不默认全文加载；性能风险、容量/延迟目标或评审需要时加载。
- `source-driven-development` 不默认全文加载；新增或不熟悉依赖、框架、API 时加载。
- `browser-testing-with-devtools` 不默认全文加载；浏览器端行为验证或前端调试时加载。
- `git-workflow-and-versioning` 不默认全文加载；仅在用户要求 git 操作或流程进入提交/版本管理动作时加载。
