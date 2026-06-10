# Skill Matrix

> **TL;DR**: 本文件是 Skill 注册、角色术语、加载规则、Phase 调度和 Forbidden 约束的唯一权威源。Phase 入口必须读取本文件。

## Boundary

本文件只定义：

- Skill 注册和路径
- Skill 角色术语
- Skill 加载规则
- Lite-flow Skill Mapping
- Standard-flow Phase Skill Matrix
- Forbidden/Deferred 约束

Gate 判定见 `.harness/rules/gates.md`，产物结构见 `.harness/changes/structure.md`，产物模板见 `.harness/changes/templates.md`。

## Skill Role Terms

| 术语 | 含义 | Gate 影响 |
|------|------|-----------|
| Required Skill | 当前 Phase 主 Skill，必须读取/调用 | 未加载或无 Skill Load Record 时 Mechanical Gate=`blocked` |
| On-demand Skill | 由明确上下文需求、任务类型或 risk flag 触发 | 触发评估必须记录；触发成立但未加载且无理由 → Mechanical Gate=`blocked` |
| On-demand Domain Skill | API/security/performance 等领域参考 Skill | risk_flags 或评审发现触发；加载或不加载理由必须记录 |
| Failure-only Skill | 仅在 fail/blocked/异常行为时加载 | Failure Gate 缺少根因、回退或修复验证 → Mechanical Gate=`blocked` |
| Internal Reference | Skill 目录内补充资料 | 默认不加载；仅当主 Skill、任务或用户明确要求时读取 |
| Forbidden/Deferred | 当前 Phase 不得执行的能力或动作 | 执行后 Gate=`fail` 或 `blocked` |

## Loading Rules

- Required Skill 必须在对应 Phase 产出 artifact 前读取，并写入 Skill Load Record。
- On-demand Skill 必须记录 trigger evaluation。
- On-demand trigger 来源只能是：risk_flags、任务类型、证据缺口、评审发现、失败现象、用户明确要求。
- 未触发的 On-demand Skill 不默认加载。
- Failure-only Skill 只在 Mechanical Gate=`fail|blocked`、测试失败、CI 失败、部署失败或异常行为时加载。
- Skill 内部补充 `.md` 属于 Internal Reference，不默认加载。
- 多加载不算失败，但无理由加载大量 Skill 视为上下文污染，应在 Gate Record 中说明。

## Skill Registry

| Skill | 路径 | 角色 | 用途 |
|-------|------|------|------|
| `context-engineering` | `.harness/skills/context-engineering/SKILL.md` | On-demand Skill | 上下文压缩与恢复 |
| `debugging-and-error-recovery` | `.harness/skills/debugging-and-error-recovery/SKILL.md` | Failure-only Skill | Stop-the-Line、失败排查 |
| `idea-refine` | `.harness/skills/idea-refine/SKILL.md` | Required Skill | Phase 1 需求澄清、问题收敛 |
| `spec-driven-development` | `.harness/skills/spec-driven-development/SKILL.md` | Required Skill | Phase 2 spec 编写 |
| `planning-and-task-breakdown` | `.harness/skills/planning-and-task-breakdown/SKILL.md` | Required Skill | Phase 3 任务拆解、验收条件 |
| `incremental-implementation` | `.harness/skills/incremental-implementation/SKILL.md` | Required Skill | Phase 4 增量实现 |
| `code-review-and-quality` | `.harness/skills/code-review-and-quality/SKILL.md` | Required Skill | Phase 5/7 代码与测试质量评审 |
| `test-driven-development` | `.harness/skills/test-driven-development/SKILL.md` | Required Skill | Phase 6/7 测试编写、覆盖率验证 |
| `ci-cd-and-automation` | `.harness/skills/ci-cd-and-automation/SKILL.md` | Required Skill | Phase 8/9 CI 与部署验证 |
| `documentation-and-adrs` | `.harness/skills/documentation-and-adrs/SKILL.md` | Required Skill | Phase 10 交付摘要、ADR |
| `api-and-interface-design` | `.harness/skills/api-and-interface-design/SKILL.md` | On-demand Domain Skill | API、模块边界、接口契约 |
| `security-and-hardening` | `.harness/skills/security-and-hardening/SKILL.md` | On-demand Domain Skill | 安全、auth、权限、OWASP 风险 |
| `performance-optimization` | `.harness/skills/performance-optimization/SKILL.md` | On-demand Domain Skill | 性能风险、瓶颈分析 |

## Lite-flow Skill Mapping

| Step | Required Skills | On-demand / Failure-only | Forbidden |
|------|-----------------|--------------------------|-----------|
| L1 需求确认+计划 | `idea-refine` | `context-engineering` only if context restoration/compression is needed | 不创建 Standard-only 产物；不实现代码 |
| L2 实现 | `incremental-implementation` | domain skills only if risk expands; `debugging-and-error-recovery` only on fail/blocked | 不跳过验证；不引入风险扩大 |
| L3 验证+交付 | `code-review-and-quality`（压缩评审）、`documentation-and-adrs` | `debugging-and-error-recovery` only on fail/blocked | 不创建 Standard-only 产物 |

Lite-flow 不得输出 Standard artifacts（完整清单见 `.harness/changes/structure.md`），除非升级 Standard-flow。

## Standard-flow Phase Skill Matrix

| Phase | Required Skills | On-demand / Failure-only | Forbidden/Deferred |
|-------|-----------------|--------------------------|--------------------|
| 1 | `idea-refine` | `context-engineering` only if context restoration/compression is needed | 不创建 `spec.md`、`tasks.md`；不实现代码 |
| 2 | `spec-driven-development` | `api-and-interface-design` / `security-and-hardening` / `performance-optimization` only by risk_flags/task type | 不创建 `tasks.md`；不实现代码 |
| 3 | `planning-and-task-breakdown` | domain skills only by risk_flags/task type | 不实现代码；不运行 Phase 6 测试职责 |
| 4 | `incremental-implementation` | `api-and-interface-design` only for public contract changes; `debugging-and-error-recovery` only on fail/blocked | 不推进 Phase；不请求确认；不判断 Gate；不运行 Phase 6 测试职责；不冒充 Phase 5 |
| 5 | `code-review-and-quality` | security/performance domain skills only by risk_flags or review findings | 不直接实现修复；Must Fix/Critical 回退 Phase 4 |
| 6 | `test-driven-development` | `debugging-and-error-recovery` only on fail/blocked | 不改需求/spec；实现缺陷回退 Phase 4 |
| 7 | `code-review-and-quality`、`test-driven-development` | `debugging-and-error-recovery` only on fail/blocked | 不扩大测试范围为新需求；发现缺口回退 Phase 6 或更早 |
| 8 | `ci-cd-and-automation` | `debugging-and-error-recovery` only on fail/blocked | 不发布；不绕过失败 CI |
| 9 | `ci-cd-and-automation` | security/performance domain skills only by deployment risk; `debugging-and-error-recovery` only on fail/blocked | 不替代最终交付确认；部署风险回退 Phase 8/9 |
| 10 | `documentation-and-adrs` | none | 未经用户要求不执行 git 提交/推送；不改实现代码 |
