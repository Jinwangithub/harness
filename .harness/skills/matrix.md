# Phase Skill Matrix

> **TL;DR**: 每个 Phase 加载对应 Required Skills。Forbidden 约束必须遵守。Phase 入口从此文件复制 Forbidden 约束。

本文件是 Phase Skill 调度矩阵的唯一权威源。

## Lite-flow Skill Mapping

| Step | Skills | Forbidden |
|------|--------|-----------|
| L1 需求确认+计划 | `idea-refine` | 不创建 Standard-only 产物；不实现代码 |
| L2 实现 | `incremental-implementation`、`auto-check-and-optimize` | 不跳过验证；不引入风险扩大 |
| L3 验证+交付 | `code-review-and-quality`（压缩评审）、`documentation-and-adrs` | 不创建 Standard-only 产物 |

Lite-flow 不得输出 Standard artifacts（`spec.md`、`tasks.md`、`coding/`、`unit_test/`、`ci_result/`、`deployment/`、`delivery-summary.md`），除非升级 Standard-flow。

## Standard-flow Phase Skill Matrix

| Phase | Required Skills | Support Skills | Conditional Skills | Forbidden/Deferred |
|-------|-----------------|----------------|--------------------|--------------------|
| 1 | `idea-refine` | `context-engineering` | none | 不创建 `spec.md`、`tasks.md`；不实现代码 |
| 2 | `spec-driven-development` | none | `source-driven-development`、`api-and-interface-design`、`security-and-hardening`、`performance-optimization` | 不创建 `tasks.md`；不实现代码 |
| 3 | `planning-and-task-breakdown` | `api-and-interface-design` | `security-and-hardening`、`deprecation-and-migration` | 不实现代码；不运行 Phase 6 测试职责 |
| 4 | `incremental-implementation`、`auto-check-and-optimize` | none | `frontend-ui-engineering`、`source-driven-development`、`api-and-interface-design` | 不推进 Phase；不请求确认；不判断 Gate；不运行 Phase 6 测试职责；不冒充 Phase 5 |
| 5 | `code-review-and-quality` | none | `security-and-hardening`、`performance-optimization`、`code-simplification` | 不直接实现修复；Must Fix/Critical 回退 Phase 4 |
| 6 | `test-driven-development` | none | `browser-testing-with-devtools`、`debugging-and-error-recovery` | 不改需求/spec；实现缺陷回退 Phase 4 |
| 7 | `code-review-and-quality`、`test-driven-development` | none | none | 不扩大测试范围为新需求；发现缺口回退 Phase 6 或更早 |
| 8 | `ci-cd-and-automation` | `debugging-and-error-recovery` | none | 不发布；不绕过失败 CI |
| 9 | `shipping-and-launch` | none | `security-and-hardening`、`performance-optimization` | 不替代最终交付确认；部署风险回退 Phase 8/9 |
| 10 | `documentation-and-adrs` | none | `git-workflow-and-versioning`、`deprecation-and-migration` | 未经用户要求不执行 git 提交/推送；不改实现代码 |
