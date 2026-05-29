# 已知问题

## 失败模式速查表

| 症状 | 根因 | 对应规则 |
|------|------|---------|
| Gate 状态无法确认 | 缺少 fresh evidence | `quality-gates.md` §Completion Claim Gate |
| 恢复后重复执行已完成 Phase | INDEX.md 未更新 resume point | `changes/README.md` §Registry |
| Lite-flow 后发现需要 Standard | Flow Classifier 误判 | `development-workflow.md` §强制升级规则 |
| Memory 记录不完整 | 字段缺失或未用完整模板 | `memory/README.md` §完整模板 |
| 多个 active auto-resume | INDEX 维护遗漏 | `changes/INDEX.md` §Maintenance Rules |
| Phase 产物边界混淆 | Work Lock 未执行 | `development-workflow.md` §Standard Phase Locks |
| Skill 加载错误或找不到 | Skill 目录与 README 不同步 | `skills/README.md` §Skill Registry |

## 格式

```
- [P{优先级}] {标题} ({发现日期})
  - 描述: {问题描述}
  - 影响范围: {哪些文件/功能受影响}
  - 临时方案: {短期规避方法}
  - 计划修复: {计划时间}
```

## 待办

- [P3] spec-driven-development Skill 默认行为包含 tasks.md 产出 (2026-05-07)
  - 描述: 该 Skill 默认同时产出 spec.md 和 tasks.md，需手动干预限制。
  - 影响范围: Phase 2 执行
  - 临时方案: 调用时显式指示「只写 spec.md，不写 tasks.md」
  - 计划修复: 需 agent-skills 插件支持 Skill 参数化

- [P3] JaCoCo 覆盖率门禁需手动读取报告 (2026-05-07)
  - 描述: 需解析 target/site/jacoco/index.html 获取覆盖率数据。
  - 影响范围: Phase 6 门禁验证
  - 临时方案: Orchestrator 手动读取报告文件解析覆盖率百分比
  - 计划修复: 添加 jacoco-check 自动门禁

- [P4] 子任务进度跟踪依赖手动管理 (2026-05-07)
  - 描述: incremental-implementation 无自动化进度 UI。
  - 影响范围: Phase 4 进度展示
  - 临时方案: Orchestrator 每次子任务完成后报告「Task i/N 已完成」
  - 计划修复: 依赖规范约束

## 2026-05-26 | 历史 summary 不完全符合新 schema

- 描述: 历史 changes summary 中存在非 canonical Human Approval wording、`resume_from`、缺失 `Completion lock`、`状态: 已完成` + `pending-human` 等与新 schema 不一致的问题。本次治理不批量重写历史归档，避免伪造或重塑审计链。
- 影响范围: `.harness/changes/docs-flow-friction-reduction-20260519/`、`.harness/changes/docs-harness-slimming-20260520/`、`.harness/changes/fix-harness-executability-20260521/` 等 legacy archive 的自动恢复和 validator 输出。
- 临时方案: 通过 `.harness/changes/INDEX.md` 标记 `legacy-unfinished`、`legacy-conflict`、`do-not-auto-resume`；validator 对 legacy debt 输出 WARN 而不是默认 FAIL。
- 计划修复: 仅在用户明确要求历史归档迁移时，按单独治理变更逐个迁移并保留原始 approval evidence，不自动改写历史 Human Approval。
