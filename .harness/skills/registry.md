# Skill Registry

> **TL;DR**: 所有 Skill 文件位于 `.harness/skills/{name}/SKILL.md`。按需加载。

本文件是 Skill 注册表和角色术语的权威源。Phase Skill Matrix（含 Required/Forbidden）见 `.harness/skills/matrix.md`。

## Skill 角色术语

| 术语 | 含义 | Gate 影响 |
|------|------|-----------|
| Required Skill | 当前 Phase 必须读取/调用的 Skill | 未加载或无 Skill Load Record 时 Mechanical Gate=`blocked` |
| Support Skill | 按上下文需要加载 | 需要但未加载时记录原因；不默认阻塞 |
| Conditional Skill | 由 risk flag、任务类型、证据缺口或失败触发 | 触发条件成立但未加载时 Mechanical Gate=`blocked` |
| Forbidden/Deferred | 当前 Phase 不得执行的能力或动作 | 执行后 Gate=`fail` 或 `blocked` |

## 加载规则

- Required Skill 必须在对应 Phase 产出 artifact 前读取，并写入 Skill Load Record。
- Conditional Skill 触发依据必须来自 risk flag、任务类型、证据缺口、评审发现或失败现象；未触发也要记录 trigger evaluation。
- **降级策略**：如果无法确定 Conditional Skill 是否触发 → 加载它。多加载不会 Gate 失败，漏加载会 blocked。
- Support Skill 只在有明确支持需求时加载。

## Core-meta

| Skill | 路径 | 用途 |
|-------|------|------|
| `using-agent-skills` | `.harness/skills/using-agent-skills/SKILL.md` | Skill 发现与路由 |
| `context-engineering` | `.harness/skills/context-engineering/SKILL.md` | 上下文压缩与恢复 |
| `debugging-and-error-recovery` | `.harness/skills/debugging-and-error-recovery/SKILL.md` | Stop-the-Line、失败排查 |

## Core-flow

| Skill | 路径 | 主用途 |
|-------|------|--------|
| `idea-refine` | `.harness/skills/idea-refine/SKILL.md` | 需求澄清、问题收敛 |
| `spec-driven-development` | `.harness/skills/spec-driven-development/SKILL.md` | spec 编写 |
| `planning-and-task-breakdown` | `.harness/skills/planning-and-task-breakdown/SKILL.md` | 任务拆解、验收条件 |
| `incremental-implementation` | `.harness/skills/incremental-implementation/SKILL.md` | 增量实现 |
| `auto-check-and-optimize` | `.harness/skills/auto-check-and-optimize/SKILL.md` | Phase 4 Author/Self Review；不替代 Phase 5 |
| `test-driven-development` | `.harness/skills/test-driven-development/SKILL.md` | 测试编写、覆盖率验证 |
| `code-review-and-quality` | `.harness/skills/code-review-and-quality/SKILL.md` | 代码/测试质量评审 |
| `ci-cd-and-automation` | `.harness/skills/ci-cd-and-automation/SKILL.md` | CI 验证与自动化 |
| `shipping-and-launch` | `.harness/skills/shipping-and-launch/SKILL.md` | 部署、冒烟、发布检查 |
| `documentation-and-adrs` | `.harness/skills/documentation-and-adrs/SKILL.md` | 交付摘要、ADR |

## Conditional-domain

| Skill | 路径 | 触发条件 |
|-------|------|----------|
| `source-driven-development` | `.harness/skills/source-driven-development/SKILL.md` | 引入新框架、库或 API |
| `api-and-interface-design` | `.harness/skills/api-and-interface-design/SKILL.md` | 设计 API、模块边界、接口契约 |
| `frontend-ui-engineering` | `.harness/skills/frontend-ui-engineering/SKILL.md` | 前端 UI、组件、交互实现 |
| `browser-testing-with-devtools` | `.harness/skills/browser-testing-with-devtools/SKILL.md` | 浏览器端调试、页面行为验证 |
| `security-and-hardening` | `.harness/skills/security-and-hardening/SKILL.md` | 安全、auth、权限、OWASP 风险 |
| `performance-optimization` | `.harness/skills/performance-optimization/SKILL.md` | 性能风险、瓶颈分析 |
| `code-simplification` | `.harness/skills/code-simplification/SKILL.md` | 评审发现复杂、冗余代码 |
| `deprecation-and-migration` | `.harness/skills/deprecation-and-migration/SKILL.md` | 废弃旧功能、迁移接口 |

## Support-macro

| Skill | 路径 | 触发条件 |
|-------|------|----------|
| `git-workflow-and-versioning` | `.harness/skills/git-workflow-and-versioning/SKILL.md` | 用户要求提交、分支或版本管理 |
