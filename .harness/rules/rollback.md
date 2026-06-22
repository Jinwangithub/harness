# 失败处理与回退路径

> **TL;DR**: 任意 fail/blocked 必须 Stop-the-Line，记录 failure evidence 和根因，按回退路径恢复到对应 Phase/Step，修复后重验证；风险扩大时重新执行 Flow Classifier。

本文件是失败处理与回退路径的权威源。
Flow 分类与路由见 `.harness/rules/flow.md`，Lite 执行见 `.harness/rules/flow-lite.md`，Standard 执行见 `.harness/rules/flow-standard.md`，Gate 判定见 `.harness/rules/gates.md`。

> **边界**：本文件只定义 fail/blocked/异常行为后的 Stop-the-Line、根因、恢复点、重验证、Memory 和回退目标。入口卡片见 `flow-lite.md` / `flow-standard.md`，Gate 检查表见 `gates.md`。

## 通用失败处理

Mechanical Gate=`fail|blocked`、执行异常、证据缺失或发现风险扩大时，必须按以下顺序处理：

1. **Stop-the-Line**：停止推进当前 Phase/Step；不得请求用户放行失败或跳过验证。
2. **记录 failure evidence**：记录失败命令、退出码、关键日志、缺失条件或异常行为。
3. **定位根因**：根因为空或“未定位”时保持 `blocked`，不得宣称修复完成。
4. **确定恢复点**：按本文件回退路径表选择 Phase 或 Flow step，并同步更新 `summary.md` 和 `INDEX.md`。
5. **修复并重验证**：修复后生成 fresh evidence；不得复用旧 evidence 作为通过依据。
6. **Memory**：命中 Memory 触发条件时立即记录；未触发也要在出口报告写 `Memory: none`。
7. **风险扩大重分类**：Lite-flow 中发现跨模块、公共契约、安全、数据、性能、迁移、架构、部署或治理风险时，重新执行 Flow Classifier；命中强制 Standard 条件则升级 Standard-flow。

## 回退路径

| 失败类型 | 回退到 |
|---------|--------|
| 需求不符 | Phase 1 |
| Spec 不符 | Phase 2 |
| 任务不可验收 | Phase 3 |
| 编译错误 | Phase 4 |
| 编码评审 Must Fix/Critical | Phase 4 |
| 测试失败 / 测试评审失败 / CI 失败 | Phase 6 |
| 部署验证失败 | Phase 8 或 Phase 9 |
| 评审超轮次 | 人工决策 |
