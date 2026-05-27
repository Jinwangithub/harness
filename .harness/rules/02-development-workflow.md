# 开发流程规范

本文件是 Flow Classifier、Lite/Standard-flow 顺序、Standard Phase Locks、Phase 4 隔离原则、升级/回退与检查时机的权威源。

详细门禁检查表见 `.harness/rules/04-quality-gates.md`；Skill Matrix 见 `.harness/skills/README.md`；Memory 模板与检查频率见 `.harness/memory/README.md`；变更目录模板见 `.harness/changes/README.md`。

## 核心原则

1. **先分类再执行**：新需求必须先执行 Flow Classifier。
2. **低风险降密度，高风险保完整**：Lite 只减少阶段和产物，不减少验证、证据、Memory、Stop-the-Line 或必要用户确认。
3. **先机械后人工**：每个 Phase / Flow step 先执行 Mechanical Gate，通过后再按 `confirmation_policy` 进入 Human Approval Gate。
4. **证据优先**：未列出 fresh verification evidence，不得声明完成、通过或交付。
5. **唯一 Orchestrator + 本地 Skills**：隔离上下文只能执行受限任务，不替代 Orchestrator 决策。
6. **单一权威源**：流程顺序与锁在本文件；Gate 规则、模板和 Skill Matrix 只引用各自权威源。

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
| `flow` | `Lite-flow` / `Standard-flow` |
| `selection_basis` | 选择依据，必须说明影响面、行为变化和风险判断 |
| `risk_flags` | `none` 或 `security`、`data`、`api`、`auth`、`payment`、`perf`、`migration`、`architecture`、`governance`、`deployment`、`unclear-requirement` |
| `confirmation_policy` | `batched` / `mandatory` |
| `upgrade_triggers` | 风险扩大、门禁失败/阻塞、证据不足、Memory 无法完整记录、需要业务判断等 |

### 强制 Standard-flow 排除法（命中任意一条 → 强制 Standard-flow，不得选 Lite）

- [ ] 涉及文件数 > 3
- [ ] 涉及数据库 schema 变更
- [ ] 涉及外部接口（新增或修改）
- [ ] 需求描述含以下任意关键词：权限、安全、迁移、部署、架构、支付、认证
- [ ] 需求描述含模糊词：大概、可能、看情况、不确定、待定
- [ ] 涉及治理规则/模板/Skill Matrix/Gate/Memory/changes 结构变更

以上全部为 NO → 可进入 Lite-flow 机械判定清单。

### 机械判定清单

Flow Classifier 必须逐项回答并写入 `summary.md` / `lite_spec.md`：

1. 影响面是否单模块/少量文件，或纯文档/格式/注释？
2. 是否修改治理规则、模板、流程、Skill Matrix、Gate、Memory 或 changes 结构？如是，默认 `Standard-flow`，或至少设置 `risk_flags: governance` / `architecture`，不得写 `risk_flags: none`。
3. 是否跨模块、跨目录边界或改变公共契约？
4. 是否涉及 API、DB/schema、auth、security、perf、migration、architecture、deployment 或 unclear requirement？
5. Lite-flow 是否有可机械复核的 `low_risk_proof`？没有则不得选择 Lite-flow。
6. 是否需要业务判断或用户确认未定义规则？如是，使用 `unclear-requirement` 并进入 Standard-flow。

### 自动选择规则

| Flow | 自动适用场景 | 强制升级条件 | confirmation_policy |
|------|--------------|--------------|---------------------|
| Lite-flow | typo、注释、格式、纯文档、README 小修、无行为变化小配置、单模块/少量文件、明确低风险行为变化、简单 bugfix、简单测试补充，且 `low_risk_proof` 可机械复核 | 跨模块、API/DB/schema/auth/payment/security/perf/migration/architecture/governance/deployment、治理规则/流程/模板/Skill Matrix/Gate/Memory/changes 结构变更、需求不清或需要业务判断 | `batched` |
| Standard-flow | 新功能、跨模块、架构/数据/安全/权限/外部接口/迁移/性能/部署、治理规则/流程/模板/Skill Matrix/Gate/Memory/changes 结构变更、需求不清 | N/A | `mandatory` |

### 强制升级规则

任一条件出现时，必须 Stop-the-Line，记录升级原因，更新 `summary.md`，并升级到 Standard-flow：

- Lite-flow 发现跨模块影响、接口/数据库/schema/auth/payment/security/perf/migration/architecture 变更。
- 需求不清、需要业务判断，或低风险假设无法机械证明。
- 任一流程的 Mechanical Gate 为 `fail|blocked` 且无法在当前流程步骤内修复。
- 验证证据不足以支撑当前完成声明。
- Memory 记录要求被触发但无法按完整模板记录。

## Flow 产物与执行顺序

### Lite-flow

适用：typo、注释、格式、纯文档、README 小修、无行为变化小配置、单模块/少量文件、明确低风险行为变化、简单 bugfix、简单测试补充。

必需产物：

```text
summary.md
request_analysis/lite_spec.md
request_analysis/checklist.md
verification_report.md
review_summary.md
```

执行顺序：

1. L1 需求确认+简化计划：写入 `summary.md`、`request_analysis/lite_spec.md`、`request_analysis/checklist.md`；Mechanical Gate=`pass` 后请求一次 batched Human Approval Gate。未 `approved` 前不得进入 L2。
2. L2 实现：进入前必须 L1 Human Approval Gate=`approved`；按 checklist 修改；若风险扩大则 Stop-the-Line 并升级。
3. L3 验证/压缩评审：生成 `verification_report.md` 和 `review_summary.md`，包含 fresh verification evidence、Memory check 和压缩版 Two-stage Review。
4. L4 交付：最终验证/评审摘要确认一次；final approval=`approved` 且 Completion Claim Gate 通过前，不得把 `summary.md` 标为 `已完成`；Mechanical Gate fail/blocked 时不得请求人工放行。

Lite-flow 不扩展成 Standard-flow 产物结构；只保留以上五类产物。低风险小变更可填写较短内容，但不能省略机械验证、Memory check、Stop-the-Line 或必要确认。

### Standard-flow

适用：高风险或不明确需求，保持完整 Phase 1-10、CK1-CK9、逐 Phase Mechanical Gate 和逐 Phase Human Approval Gate。

| Phase | 目标 | 主要产物 | 确认点 |
|------|------|----------|--------|
| Phase 1 | 需求分析 | `request_analysis/understanding.md` | CK1 |
| Phase 2 | 需求评审 | `request_analysis/spec.md` | CK2 |
| Phase 3 | 任务规划 | `request_analysis/tasks.md` | CK3 |
| Phase 4 | 编码实现 | `coding/coding_report_v1.md` | CK4 |
| Phase 5 | 编码评审 | `coding/review/*.md` | CK5 |
| Phase 6 | 单元测试 | `unit_test/test_report.md` | CK6 |
| Phase 7 | 测试评审 | `unit_test/review/test_review_v1.md` | CK7 |
| Phase 8 | CI 验证 | `ci_result/ci_report.md` | 按 Standard 规则确认或记录自动放行依据 |
| Phase 9 | 部署验证 | `deployment/deploy_report.md` | CK8 |
| Phase 10 | 用户确认 | `delivery-summary.md` | CK9 |

Standard-flow 每个阶段必须加载 Required Skills；完整 Standard-flow Phase Skill Matrix 以 `.harness/skills/README.md` 为唯一权威源。主要产物路径在本表列出，具体 artifact template 以 `.harness/changes/README.md` 为准。

Standard-flow 关键边界：

- Phase 1 只产 `understanding.md`，不产 `spec.md` 或 `tasks.md`。
- Phase 2 只产 `spec.md`，不产 `tasks.md`。
- Phase 3 首次创建 `tasks.md`。
- Phase 4 只做编码实现、编译验证和 Author/Self Review，不运行 Phase 6 测试职责。
- Phase 5 是 Independent Review，不替代 Phase 4 自检。
- Phase 6 才运行测试和覆盖率验证。

## Standard Phase Locks

Standard-flow 使用强 Phase Lock。未满足当前锁，不得进入下一 Phase。

| Lock | 判定 |
|------|------|
| Entry Lock | 前一阶段 Mechanical Gate=`pass`、Human Approval=`approved` 或策略明确允许、产物已归档、Memory check 完成。Phase 1 Entry Lock 需完成 Flow Classification 和变更目录准备。 |
| Work Lock | 当前阶段只能执行本阶段允许动作，不得提前做后续阶段工作；发现需要后续阶段动作时记录并延后或回退。 |
| Exit Lock | 当前阶段产物、Required Skill Load Record、Mechanical Gate、fresh evidence、Memory check 完成。 |
| Human Approval Lock | Mechanical Gate=`pass` 后才能请求确认；用户 `approved` 前不能进入下一阶段。 |
| Failure Lock | Mechanical Gate=`fail|blocked` 时 Stop-the-Line，记录失败证据、回退目标和重新验证要求。 |

Phase Lock 状态模板见 `.harness/changes/README.md`；判定细则见 `.harness/rules/04-quality-gates.md`。

## Phase 4 隔离实现原则

Standard Phase 4 编码实现必须由 Orchestrator 调度隔离执行上下文/受限子上下文完成。

Orchestrator 责任：

1. 准备不可变输入包：需求、spec、tasks、相关代码路径、禁止范围、验收条件。
2. 调度隔离上下文执行受限实现任务。
3. 汇总变更，执行编译验证。
4. 调度或执行 Author/Self Review。
5. 归档隔离执行证据、编译证据、`coding_report_v1.md` 和 CK4 门禁状态。

隔离上下文限制：

- 不得推进 Phase。
- 不得请求用户确认。
- 不得判断 Gate。
- 不得修改无关文件。
- 不得运行或冒充 Phase 6 测试职责。
- 只能按不可变输入包执行受限编码任务并回传结果。

## Recovery Semantics

恢复入口由 `.harness/changes/INDEX.md` registry-first 决定，再扫描各 `summary.md` 做一致性校验。

| 情况 | 处理 |
|------|------|
| INDEX 唯一声明 `active` + `auto-resume` | 按该 row 的 Current step / Resume point 恢复 |
| 多个 `状态: 进行中`，但 INDEX 将非 active 标为 `legacy-*` / `do-not-auto-resume` | 报告 WARN，按 active 恢复，不改写历史 |
| 多个 active auto-resume、INDEX 缺失或 INDEX 与 summary 冲突 | Stop-the-Line，报告候选目录和冲突字段，不猜测恢复对象 |
| `Human Approval Gate=pending-human` | 合法恢复入口；表示 Mechanical Gate 已通过、等待用户确认；Completion lock 必须为 `locked` |
| `状态: 已完成` + `pending-human` | 状态冲突；新 summary Gate=`blocked`，历史归档标记 `legacy-conflict` |
| governance/templates/gates/memory/changes/skills 变更 | 默认 Standard-flow 或 Governance-Standard，并设置 governance 相关 risk flags |

新 summary 必须使用 `Current step`、`Resume point`、`Completion lock`；`resume_from` 仅作为 legacy 字段保留，不得用于新变更。

## Confirmation Policy

| Policy | 默认 Flow | 行为 |
|--------|-----------|------|
| `mandatory` | Standard-flow | CK1-CK9 按 Phase 请求确认；用户确认前不得进入下一 Phase。 |
| `batched` | Lite-flow | 需求+简化计划确认一次，最终验证/评审摘要确认一次；中间 Mechanical Gate 通过则可继续。 |

Human Approval Gate 的时机可以按风险分级，但不能绕过 Mechanical Gate、fresh evidence、Memory check 或 Stop-the-Line。`pending-human` 是等待确认状态，不是完成状态。`not-required-by-policy` 只适用于策略明确定义的中间点，不能代替 Standard-flow mandatory Phase approval，也不能代替 Lite L1/L4 batched approval。非 canonical Human Approval 状态视为 Gate blocked。

## Memory 检查频率

- Standard-flow：每个 Phase 出口检查；触发即按 `.harness/memory/README.md` 记录。
- Lite-flow：计划确认后、最终验证/交付前检查；触发即记录。

workflow 只定义“何时检查”；Memory 模板和完整字段以 `.harness/memory/README.md` 为准。

## Phase / Flow 出口顺序

### Standard-flow

1. 验证 Entry Lock 与 Work Lock 未被破坏。
2. 执行本 Phase 产物归档。
3. 按本文件频率检查 Memory，触发即记录。

**Phase 出口 Memory 强制问答（必须逐项回答，有内容才记录）：**
- Q1: 本 Phase 是否做了任何非显而易见的技术或治理决策？→ 是则记入 `decisions.log`
- Q2: 本 Phase 是否遇到规则未覆盖的情况或已知限制？→ 是则记入 `known-issues.md`
- Q3: 本 Phase 是否有"下次应该更早做"的事？→ 是则记入 `lessons-learned.md`

4. 检查 Required Skill Load Record。
5. 执行 `.harness/rules/04-quality-gates.md` 对应 Mechanical Gate。
6. 出口报告列出 Mechanical Gate 状态、fresh verification evidence、`Memory recorded: {N} entries / none`。
7. Mechanical Gate 为 `fail|blocked` 时执行 Failure Handling Protocol，不得请求用户人工放行。
8. Mechanical Gate 为 `pass` 后按 `mandatory` 请求 Human Approval Gate。
9. Human Approval Gate 为 `approved` 前，下一 Phase Entry Lock 保持关闭。

### Lite-flow

按 `batched` 执行 Lite step locks：L1 需求+简化计划必须 Mechanical Gate=`pass` 后请求确认；L1 Human Approval Gate=`approved` 前不得进入 L2；L2 实现不得扩大风险；L3 必须具备 fresh evidence 和 Memory check；L4 final approval=`approved` 且 Completion Claim Gate 通过前，不得把 `summary.md` 标为 `已完成`。

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
| 编译错误 | Phase 4 或 Lite 实现步骤 |
| 编码评审 Must Fix/Critical | Phase 4 |
| 测试失败 | Phase 6 |
| 测试评审失败 | Phase 6 |
| CI 失败 | Phase 6 |
| 部署验证失败 | Phase 8 或 Phase 9 |
| 评审超轮次 | 人工决策 |

## 隔离执行上下文原则

隔离执行上下文是 Orchestrator 调度下的受限任务或审查泳道，不是新增 Agent 文件。

- 输入隔离：每个泳道收到同一份不可变输入包。
- 输出隔离：每个泳道只写自己的报告或返回自己的实现结果。
- 结论隔离：初次报告产出前不参考其他泳道结论。
- 权限隔离：隔离上下文不能推进 Phase、不能请求用户确认、不能修改无关文件。
- 汇总集中：只有 Orchestrator 能合并报告、判断 Mechanical Gate、请求 Human Approval Gate。
