# 开发流程规范

本文件是 Flow Classifier、Lite/Standard-flow 顺序、Phase 4 隔离原则和回退路径的权威源。

门禁检查表见 `.harness/rules/quality-gates.md`；Skill Matrix 见 `.harness/skills/README.md`；Memory 模板见 `.harness/memory/README.md`；变更目录模板见 `.harness/changes/README.md`。

## Flow Classifier

> **安全默认值**：任何时候不确定该选哪个 Flow → 一律选 Standard-flow。Lite-flow 仅用于你 100% 确定安全且完全满足所有 Lite 条件的场景。

收到新需求后，Orchestrator 必须先分类，并把结果写入 `.harness/changes/{id}/summary.md`。

| 字段 | 含义 |
|------|------|
| `flow` | `Lite-flow` / `Standard-flow` |
| `selection_basis` | 影响面、行为变化和风险判断 |
| `risk_flags` | `none` 或 `security`、`data`、`api`、`auth`、`payment`、`perf`、`migration`、`architecture`、`governance`、`deployment`、`unclear-requirement` |

### 强制 Standard-flow 排除法（命中任意一条 → 强制 Standard-flow）

- [ ] 涉及文件数 > 3（需求分析阶段无法确定时，在 Phase 1 完成后、进入 Phase 2 前重新判定）
- [ ] 涉及数据库 schema 变更
- [ ] 涉及外部接口（新增或修改）
- [ ] 需求含关键词：权限、安全、迁移、部署、架构、支付、认证
- [ ] 需求含模糊词：大概、可能、看情况、不确定、待定
- [ ] 涉及治理规则/模板/Skill Matrix/Gate/Memory/changes 结构变更

以上全部为 NO → 进入机械判定清单。

### 机械判定清单（逐项回答并写入 summary.md）

1. 影响面是否单模块/少量文件，或纯文档/格式/注释？
2. 是否修改治理规则、模板、流程、Gate、Memory 或 changes 结构？如是 → Standard-flow，`risk_flags` 不得为 `none`。
3. 是否跨模块、跨目录边界或改变公共契约？
4. 是否涉及 API、DB、auth、security、perf、migration、architecture 或 deployment？
5. 是否有可机械复核的 `low_risk_proof`？没有则不得选 Lite-flow。
6. 是否需要业务判断或用户确认未定义规则？如是 → `unclear-requirement`，进入 Standard-flow。

## Lite-flow

适用：typo、注释、格式、纯文档、小配置、简单 bugfix、简单测试补充，且 `low_risk_proof` 可机械复核。

必需产物：`summary.md`、`request_analysis/lite_spec.md`、`request_analysis/checklist.md`、`verification_report.md`、`review_summary.md`

执行顺序：

1. **L1** 需求确认+简化计划：写入三个 request_analysis 产物；Mechanical Gate=`pass` 后请求用户确认；未确认前不得进入 L2。
2. **L2** 实现：按 checklist 修改；风险扩大则 Stop-the-Line 并升级 Standard-flow。
3. **L3** 验证/压缩评审：生成 `verification_report.md` 和 `review_summary.md`，包含 fresh evidence 和 Memory check。
4. **L4** 交付：用户最终确认后标记 `已完成`；Mechanical Gate fail/blocked 时不得请求用户放行。

## Standard-flow

适用：新功能、跨模块、高风险、需求不清。完整 Phase 1-10，每 Phase 完成后必须用户确认才能进入下一 Phase。

| Phase | 目标 | 主要产物 | 确认点 |
|-------|------|----------|--------|
| 1 | 需求分析 | `request_analysis/understanding.md` | CK1 |
| 2 | 需求评审 | `request_analysis/spec.md` | CK2 |
| 3 | 任务规划 | `request_analysis/tasks.md` | CK3 |
| 4 | 编码实现 | `coding/coding_report_v1.md` | CK4 |
| 5 | 编码评审 | `coding/review/*.md` | CK5 |
| 6 | 单元测试 | `unit_test/test_report.md` | CK6 |
| 7 | 测试评审 | `unit_test/review/test_review_v1.md` | CK7 |
| 8 | CI 验证 | `ci_result/ci_report.md` | CK8 |
| 9 | 部署验证 | `deployment/deploy_report.md` | CK9 |
| 10 | 用户确认 | `delivery-summary.md` | CK10 |

**进入下一 Phase 的唯一条件**：当前 Phase Mechanical Gate=`pass` 且用户已确认。任一不满足则停止。进入后立即更新 `summary.md` 的 `Current step` 和 `Resume point`。

关键边界：

- Phase 1 只产 `understanding.md`，禁止提前创建 `spec.md` 或 `tasks.md`。
- Phase 2 只产 `spec.md`，禁止提前创建 `tasks.md`。
- Phase 4 只做编码实现、编译验证和 Author/Self Review，不运行 Phase 6 测试职责。
- Phase 5 是 Independent Review，不替代 Phase 4 自检。

## Phase 状态卡

每个 Standard Phase 入口，Orchestrator 必须输出以下状态卡，把当前 Phase 的关键约束集中呈现：

```
=== Phase N 入口状态卡 ===
当前 Phase: N — {Phase 名称}
前置确认: {已确认 / 未确认}
本 Phase 禁止: {直接从 Skill Matrix Forbidden 列复制，不得省略}
Required Skills: {列出，未加载则 Gate=blocked}
产物目标: {本 Phase 唯一产物文件名}
```

状态卡必须在 Phase 工作开始前输出。

## Phase 4 隔离实现原则

Orchestrator 责任：

1. 准备不可变输入包：需求、spec、tasks、相关代码路径、禁止范围、验收条件。
2. 调度隔离上下文执行受限实现任务。
3. 汇总变更，执行编译验证。
4. 调度或执行 Author/Self Review。
5. 归档隔离执行证据、编译证据、`coding_report_v1.md` 和 CK4 门禁状态。

隔离上下文不得：推进 Phase、请求用户确认、判断 Gate、修改无关文件、运行或冒充 Phase 6 测试职责。

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
