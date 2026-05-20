# 开发流程规范

本文件是 Flow Classifier、Mini/Lite/Standard-flow、十阶段流程、升级/回退与检查时机的权威源。

详细门禁检查表见 `.harness/rules/04-quality-gates.md`；Memory 模板与检查频率见 `.harness/memory/README.md`；变更目录模板见 `.harness/changes/README.md`。

## 核心原则

1. **先分类再执行**：新需求必须先执行 Flow Classifier。
2. **低风险降密度，高风险保完整**：Mini/Lite 只减少阶段和产物，不减少验证、证据、Memory、Stop-the-Line 或必要用户确认。
3. **先机械后人工**：每个 Phase / Flow step 先执行 Mechanical Gate，通过后再按 `confirmation_policy` 进入 Human Approval Gate。
4. **证据优先**：未列出 fresh verification evidence，不得声明完成、通过或交付。
5. **唯一 Orchestrator + 本地 Skills**：隔离上下文只能执行受限任务，不替代 Orchestrator 决策。

## Harness Iron Laws

1. 未验证，不得声称完成、通过或交付。
2. 未读相关代码、规则或证据，不得提出修改方案或放行结论。
3. Mechanical Gate 失败或阻塞时，不得请求用户人工放行。
4. 任意失败必须 Stop-the-Line 定位根因，不得只修表象或跳过验证。
5. 业务规则未知时必须查 `.harness/wiki/` 或记录疑问，不得猜测。
6. 子代理/隔离上下文只能执行受限任务，不得替代 Orchestrator 决策。
7. 流程分级只能降低阶段密度，不能取消 Mechanical Gate、fresh verification evidence、Memory check、Stop-the-Line 或必要 Human Approval Gate。

## Flow Classifier

收到新需求后，Orchestrator 必须先分类，并把结果写入 `.harness/changes/{id}/summary.md` 的 `## Flow Classification`。

| 字段 | 含义 |
|------|------|
| `flow` | `Mini-flow` / `Lite-flow` / `Standard-flow` |
| `selection_basis` | 选择依据，必须说明影响面、行为变化和风险判断 |
| `risk_flags` | `none` 或 `security`、`data`、`api`、`auth`、`payment`、`perf`、`migration`、`architecture`、`deployment`、`unclear-requirement` |
| `confirmation_policy` | `exception-only` / `batched` / `mandatory` |
| `upgrade_triggers` | 风险扩大、门禁失败/阻塞、证据不足、Memory 无法完整记录、需要业务判断等 |

### 自动选择规则

| Flow | 自动适用场景 | 强制升级条件 | confirmation_policy |
|------|--------------|--------------|---------------------|
| Mini-flow | typo、注释、格式、纯文档、README 小修、无行为变化小配置 | 任何代码行为变化、需求不清、涉及安全/数据/API/部署 | `exception-only` |
| Lite-flow | 单模块/少量文件、明确低风险行为变化、简单 bugfix、简单测试补充 | 跨模块、API/DB/schema/auth/payment/security/perf/migration/architecture | `batched` |
| Standard-flow | 新功能、跨模块、架构/数据/安全/权限/外部接口/迁移/性能/部署、需求不清 | N/A | `mandatory` |

### 强制升级规则

任一条件出现时，必须 Stop-the-Line，记录升级原因，更新 `summary.md`，并升级到更高流程：

- Mini-flow 发现代码行为变化、业务规则不明确、需要用户业务判断，或需要独立评审。
- Lite-flow 发现跨模块影响、接口/数据库/schema/auth/payment/security/perf/migration/architecture 变更。
- 任一流程的 Mechanical Gate 为 `fail|blocked` 且无法在当前流程步骤内修复。
- 验证证据不足以支撑当前完成声明。
- Memory 记录要求被触发但无法按完整模板记录。

## Flow 产物与执行顺序

### Mini-flow

适用：typo、注释、格式、纯文档、README 小修、无行为变化小配置。

必需产物：

```text
summary.md
verification_report.md
```

执行顺序：

1. 理解/分类：执行 Flow Classifier，写入 `summary.md`。
2. 修改：仅进行无行为变化的小改动。
3. 验证：执行适配任务的最小验证；纯文档可用内容审查、一致性搜索、文件检查作为 fresh evidence。
4. 记录/总结：更新 `verification_report.md`，包含 Mechanical Gate、fresh evidence、Memory check、独立评审豁免依据和最终摘要。

Mini-flow 不强制 `review_summary.md`；如豁免独立评审，依据写入 `verification_report.md`。

### Lite-flow

适用：单模块/少量文件、明确低风险行为变化、简单 bugfix、简单测试补充。

必需产物：

```text
summary.md
request_analysis/lite_spec.md
request_analysis/checklist.md
verification_report.md
review_summary.md
```

执行顺序：

1. 需求确认+简化计划：写入 `summary.md`、`request_analysis/lite_spec.md`、`request_analysis/checklist.md`，进行一次 batched Human Approval Gate。
2. 实现：按 checklist 修改；若风险扩大则 Stop-the-Line 并升级。
3. 验证/压缩评审：生成 `verification_report.md` 和 `review_summary.md`，包含 fresh verification evidence 和压缩版 Two-stage Review。
4. 交付：最终验证/评审摘要确认一次；Mechanical Gate fail/blocked 时不得请求人工放行。

Lite-flow 不扩展成 Standard-flow 产物结构；只保留以上五类产物。

### Standard-flow

适用：高风险或不明确需求，保持完整 Phase 1-10、CK1-CK9 和逐 Phase Mechanical Gate。

| Phase | 目标 | 主 Skill | 主要产物 |
|------|------|----------|----------|
| 1 | 需求分析 | `idea-refine` | `request_analysis/understanding.md` |
| 2 | 需求评审 | `spec-driven-development` | `request_analysis/spec.md` |
| 3 | 任务规划 | `planning-and-task-breakdown` | `request_analysis/tasks.md` |
| 4 | 编码实现 | `incremental-implementation` + `auto-check-and-optimize` | `coding/coding_report_v1.md` |
| 5 | 编码评审 | `code-review-and-quality` + 条件安全/性能 Skill | `coding/review/*.md` |
| 6 | 单元测试 | `test-driven-development` | `unit_test/test_report.md` |
| 7 | 测试评审 | `code-review-and-quality` | `unit_test/review/test_review_v1.md` |
| 8 | CI 验证 | `ci-cd-and-automation` | `ci_result/ci_report.md` |
| 9 | 部署验证 | `shipping-and-launch` | `deployment/deploy_report.md` |
| 10 | 用户确认 | `documentation-and-adrs` | `delivery-summary.md` |

Standard-flow 关键边界：

- Phase 1 只产 `understanding.md`，不产 `spec.md`。
- Phase 2 只产 `spec.md`，不产 `tasks.md`。
- Phase 3 首次创建 `tasks.md`。
- Phase 4 只做编译验证和 Author/Self Review，不运行测试。
- Phase 5 是 Independent Review，不替代 Phase 4 自检。
- Phase 6 才运行测试和覆盖率验证。

## Confirmation Policy

| Policy | 默认 Flow | 行为 |
|--------|-----------|------|
| `mandatory` | Standard-flow | CK1-CK9 按 Phase 请求确认；用户确认前不得进入下一 Phase。 |
| `batched` | Lite-flow | 需求+简化计划确认一次，最终验证/评审摘要确认一次；中间 Mechanical Gate 通过则可继续。 |
| `exception-only` | Mini-flow | 分类不确定、门禁失败/阻塞、需要业务判断或最终摘要时确认。 |

Human Approval Gate 的时机可以按风险分级，但不能绕过 Mechanical Gate、fresh evidence、Memory check 或 Stop-the-Line。

## Memory 检查频率

- Standard-flow：每个 Phase 出口检查；触发即按 `.harness/memory/README.md` 记录。
- Lite-flow：计划确认后、最终验证/交付前检查；触发即记录。
- Mini-flow：最终 verification 阶段检查一次；触发即记录。

workflow 只定义“何时检查”；Memory 模板和完整字段以 `.harness/memory/README.md` 为准。

## Phase / Flow 出口顺序

### Standard-flow

1. 执行本 Phase 产物归档。
2. 按本文件频率检查 Memory，触发即记录。
3. 执行 `.harness/rules/04-quality-gates.md` 对应 Mechanical Gate。
4. 出口报告列出 Mechanical Gate 状态、fresh verification evidence、`Memory recorded: {N} entries / none`。
5. Mechanical Gate 为 `fail|blocked` 时执行 Failure Handling Protocol，不得请求用户人工放行。
6. Mechanical Gate 为 `pass` 后按 `mandatory` 请求 Human Approval Gate。

### Lite-flow

按 `batched` 执行：需求+简化计划出口确认一次；实现、验证/压缩评审的 Mechanical Gate 通过且证据完整时可继续；最终验证/评审摘要再确认一次。

### Mini-flow

按 `exception-only` 执行：分类不确定、门禁失败/阻塞、需要业务判断或最终摘要时确认；Mechanical Gate fail/blocked 不得请求人工放行。

## Failure Handling Protocol

任一 Mechanical Gate 状态为 `fail|blocked` 时，必须 Stop-the-Line：

1. 停止进入下一阶段或分级流程步骤，不请求 Human Approval Gate 放行。
2. 记录失败证据：失败命令、日志、报告路径、缺失条件或阻塞原因。
3. 复现或确认失败条件。
4. 定位根因，区分需求问题、实现问题、测试问题、环境问题或流程问题。
5. 回退到规则定义的 Phase 或当前分级流程对应步骤。
6. 修复并重新验证，生成新的 fresh verification evidence。
7. 如属于 Agent 错误或可复用教训，完整写入 `lessons-learned.md`。
8. 如风险扩大，更新 Flow Classification 并升级流程。

## 回退路径

| 失败类型 | 回退到 |
|---------|-------|
| 需求不符 | Phase 1 或当前 Flow 的需求/分类步骤 |
| Spec 不符 | Phase 2 |
| 任务不可验收 | Phase 3 |
| 编译错误 | Phase 4 或 Lite/Mini 修改步骤 |
| 编码评审 Must Fix/Critical | Phase 4 |
| 测试失败 | Phase 6 |
| 测试评审失败 | Phase 6 |
| CI 失败 | Phase 6 |
| 部署验证失败 | Phase 8 或 Phase 9 |
| 评审超轮次 | 人工决策 |

## 隔离执行上下文原则

隔离执行上下文是 Orchestrator 调度下的受限任务或审查泳道，不是新增 Agent 文件。

- 输入隔离：每个泳道收到同一份不可变输入包。
- 输出隔离：每个泳道只写自己的报告。
- 结论隔离：初次报告产出前不参考其他泳道结论。
- 权限隔离：隔离上下文不能推进 Phase、不能请求用户确认、不能修改无关文件。
- 汇总集中：只有 Orchestrator 能合并报告、判断 Mechanical Gate、请求 Human Approval Gate。
