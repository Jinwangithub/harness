# 已知问题

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
