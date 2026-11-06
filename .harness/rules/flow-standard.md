# Standard-flow 规范

> **TL;DR**: Standard-flow 用于新功能、跨模块、高风险或需求不清任务。任务规划作为 Phase 4 的首个子步骤，完成后直接进入实现；Phase 4/5 分别只在实现与独立评审完成后设置一次 Composite Gate 和用户确认。

本文件是 Standard-flow Phase 1/2、Phase 4-6、Phase 4/5 子步骤和隔离实现原则的权威源。原 Phase 3 任务规划已并入 Phase 4，不再设置独立 Gate 或确认点。恢复旧活动变更时，Phase 3 只作为兼容状态：核验既有 `tasks.md` 后直接归一到 Phase 4 / implementation；计划缺失或不符时归一到 Phase 4 / task-planning，不增加计划确认。
Flow 分类与路由见 `.harness/rules/flow.md`，Gate 判定见 `.harness/rules/gates.md`，失败处理和回退路径见 `.harness/rules/rollback.md`。

> **边界**：本文件只定义 Standard-flow 执行顺序、每个 Phase/子步骤的入口卡片、Phase 4/5 隔离实现原则和 Standard 特有禁止事项。Gate 判定见 `gates.md`，产物结构见 `changes/structure.md`，Skill 文件位于 `.harness/skills/{name}/SKILL.md`。

## Standard-flow

适用：新功能、跨模块、高风险、需求不清。依次执行 Phase 1、2、4、5、6；任务规划是 Phase 4 的首个子步骤，不单独设置 Gate 或用户确认。Phase 4/5 的所有子步骤完成后各设置一次用户确认。

| Phase | 目标 | 主要产物 | 确认点 |
|-------|------|----------|--------|
| 1 | 需求分析 | `request_analysis/understanding.md` | CK1 |
| 2 | 需求评审 | `request_analysis/spec.md` | CK2 |
| 4 | 任务规划 → 实现 → 独立代码评审（`task-planning` → `implementation` → `code-review`） | `request_analysis/tasks.md`, `coding/coding_report_v1.md`, `coding/review/*.md` | CK3 |
| 5 | 单元测试 + 独立测试评审（`unit-test` → `test-review`） | `unit_test/test_report.md`, `unit_test/review/test_review_v1.md` | CK4 |
| 6 | 用户确认和交付归档 | `delivery-summary.md` | CK5 |

**Phase 1/2/4/5 的推进条件**：Phase 1/2 出口经 Mechanical Gate=`pass` 且用户确认后推进。Phase 4 的 `task-planning` 完成并通过 Orchestrator 内部检查后，直接进入 `implementation`，不设置独立 Gate 或请求用户确认；Phase 4 的三个子步骤全部完成后才执行 Composite Mechanical Gate 并请求一次确认。Phase 5 两个子步骤全部完成后同样执行一次 Composite Gate 并请求一次确认。推进或恢复时立即更新 `summary.md` 的 `Current step`、`Substep` 和 `Resume point`。Phase 6 先以 final Gate=`pass` + Human Approval=`pending` 保持 summary / INDEX 为 `active` 请求最终确认；批准后更新 final Gate 为 `approved`、同步两处为 `done` 且 Resume point=`none`，随后重跑 validator。

关键边界：

- Phase 4 依次执行任务规划、实现和独立代码评审：Planner 基于 approved `spec.md` 生成 `tasks.md`；Orchestrator 检查任务映射和验收条件后直接派发 Implementer，不请求用户批准计划。实现子步骤只做编码、编译验证和 Author/Self Review；code-review 子步骤由 fresh Reviewer 只读评审，不能替代 Composite Gate。
- Phase 5 依次执行单元测试和独立测试评审：unit-test 子步骤创建/运行测试；test-review 子步骤由 fresh Reviewer 只读评审，不能修改测试。
- Phase 4/5 的实现、测试和评审报告保持独立；Phase 4 Composite Gate 还必须检查 `tasks.md`，Phase 5 Composite Gate 必须检查测试报告和对应评审报告。

Phase/Step 入口必须按本文件对应卡片输出入口状态卡；状态卡必须包含读取 Skills、按条件补读 Skills、失败时补读 Skills、禁止事项、产物提示和 Gate 提示。

## Phase Cards

### Phase 1 — 需求分析

- Agent: Planner (`.harness/agents/planner.md`)
- Phase 1 需要业务或项目上下文时，由 Orchestrator 加载 `project-knowledge-search`；Planner 记录精确 URI、采用规则、冲突和 Open Questions。
- 读取 Skills:
  - `idea-refine`
- 按条件补读 Skills:
  - `context-engineering`: 仅当需要上下文恢复/压缩
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不创建 `spec.md`
  - 不创建 `tasks.md`
  - 不实现代码
- 产物提示:
  - `request_analysis/understanding.md`
- Gate 提示:
  - `understanding.md` 存在
  - 禁止产物不存在
  - Fresh evidence 四字段完整

### Phase 2 — 需求评审

- Agent: Planner (`.harness/agents/planner.md`)
- Phase 2 需要项目规范或系统约束时，由 Orchestrator 查询并提供 context packet；Planner 将精确 URI、应用约束和冲突/过期信息写入 `spec.md`。
- 读取 Skills:
  - `spec-driven-development`
- 按条件补读 Skills:
  - `api-and-interface-design`: 仅当 risk_flags 或任务类型涉及 API/公共契约/模块边界
  - `security-and-hardening`: 仅当 risk_flags 或任务类型涉及 security/auth/permission
  - `performance-optimization`: 仅当 risk_flags 或任务类型涉及性能风险
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不创建 `tasks.md`
  - 不实现代码
- 产物提示:
  - `request_analysis/spec.md`
- Gate 提示:
  - `spec.md` 存在
  - 项目/系统上下文查询记录完整；业务和系统断言有实际读取的 `viking://` 来源，或标记 `open-question`
  - 禁止产物不存在
  - Fresh evidence 四字段完整

### Phase 4 — 实现 + 独立代码评审

#### Phase 4 / task-planning

- Agent: Planner (`.harness/agents/planner.md`)
- 输入：approved `request_analysis/spec.md`、项目目录结构、相关代码和依赖关系。
- 读取 Skills:
  - `planning-and-task-breakdown`
- 按条件补读 Skills:
  - `api-and-interface-design`: 仅当 risk_flags 或任务类型涉及 API/公共契约/模块边界
  - `security-and-hardening`: 仅当 risk_flags 或任务类型涉及 security/auth/permission
  - `performance-optimization`: 仅当 risk_flags 或任务类型涉及性能风险
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不实现或修改项目代码
  - 不请求独立计划批准、不判定 Phase 4 Gate
  - 不创建 Phase 4 implementation、review 或 Phase 5 产物
- 产物提示:
  - `request_analysis/tasks.md`
- 交接条件（非 Gate）:
  - 每个任务映射到 `spec.md` Success Criteria，并有验收条件、验证方式、依赖和可能修改文件
  - Orchestrator 检查任务计划没有超出 approved spec 后，更新 Resume point 为 `Phase 4 / implementation` 并直接派发实现
  - 若计划暴露 spec 缺口、范围变化或未决业务问题，停止派发并回到 Phase 2 或请求必要澄清

#### Phase 4 / implementation

- Agent: Implementer (`.harness/agents/implementer.md`)
- 读取 Skills:
  - `incremental-implementation`
- 按条件补读 Skills:
  - `api-and-interface-design`: 仅当涉及公共契约变化
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不推进 Phase、不请求确认、不判断 Gate
  - 不运行完整测试套件或声称单元测试完成
  - 不创建 `coding/review/` 评审产物
- 产物提示:
  - `coding/coding_report_v1.md`
- 子步骤完成条件:
  - 实现范围符合 approved spec 和当前 Phase 4 `tasks.md`
  - 编译/构建/typecheck 证据完整
  - Author/Self Review 完成

#### Phase 4 / code-review

- Agent: fresh Reviewer (`.harness/agents/reviewer.md`)
- 读取 Skills:
  - `code-review-and-quality`
- 按条件补读 Skills:
  - `security-and-hardening`: 仅当 risk_flags 或评审发现涉及安全风险
  - `performance-optimization`: 仅当 risk_flags 或评审发现涉及性能风险
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不修改实现代码
  - 不推进 Phase、不请求确认、不判断 Gate
  - Critical/Must Fix 由 Orchestrator 回退到 Phase 4 / implementation
- 产物提示:
  - `coding/review/*.md`
- Composite Gate 提示:
  - `tasks.md`、实现报告和独立评审报告均存在
  - 编译证据和独立评审证据完整
  - Critical=0、Must Fix=0
  - Fresh evidence 四字段完整

### Phase 5 — 单元测试 + 独立测试评审

#### Phase 5 / unit-test

- Agent: Implementer (`.harness/agents/implementer.md`)
- 读取 Skills:
  - `test-driven-development`
- 按条件补读 Skills:
  - 无
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不改需求/spec
  - 不修改非测试实现文件
  - 不创建 `unit_test/review/` 评审产物
  - 测试发现实现缺陷时回退 Phase 4 / implementation
- 产物提示:
  - `unit_test/test_report.md`
- 子步骤完成条件:
  - 测试通过、测试数 > 0
  - 覆盖率符合项目阈值
  - 测试证据完整

#### Phase 5 / test-review

- Agent: fresh Reviewer (`.harness/agents/reviewer.md`)
- 读取 Skills:
  - `code-review-and-quality`
  - `test-driven-development`
- 按条件补读 Skills:
  - 无
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不创建或修改测试代码
  - 不扩大测试范围为新需求
  - 不推进 Phase、不请求确认、不判断 Gate
  - Critical/Must Fix 由 Orchestrator 回退到 Phase 5 / unit-test
- 产物提示:
  - `unit_test/review/test_review_v1.md`
- Composite Gate 提示:
  - 两个 Phase 5 报告均存在
  - 测试通过、测试数 > 0、覆盖率达标
  - Critical=0、Must Fix=0
  - Fresh evidence 四字段完整

### Phase 6 — 用户确认和交付归档

- 读取 Skills:
  - `documentation-and-adrs`
- 按条件补读 Skills:
  - 无
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 未经用户要求不执行 git 提交/推送
  - 不改实现代码
- 产物提示:
  - `delivery-summary.md`
- Gate 提示:
  - delivery summary 存在
  - Memory 完整
  - 确认前：final Gate=`pass`、Human Approval=`pending`，summary / INDEX 均为 `active`
  - 用户批准后：final Gate Approval=`approved`，summary / INDEX 同步为 `done`、Resume point=`none`
  - 状态同步后 validator PASS
  - 不将 `done` 作为批准前 Gate 条件

## Agent 隔离实现原则

Standard-flow Phase 1/2/4/5 采用 controller/subagent 协议：Orchestrator 是 controller。Phase 4 依次 fresh 调度 Planner 生成任务、Implementer 实现、Reviewer 独立评审；Phase 5 依次 fresh 调度 Implementer 和 Reviewer；Phase 6 由 Orchestrator 自行处理。完整的隔离协议定义在 `.harness/agents/orchestrator.md` 的 Dispatch 步骤中。

Phase 4 的 Planner/Implementer/Reviewer 和 Phase 5 的 Implementer/Reviewer 定义见对应 Agent 文件。subagent 不继承主会话历史；Orchestrator 必须构造自包含 prompt，把当前子步骤完整任务文本、必要上下文和前一子步骤产物直接放入 prompt。

### Orchestrator 责任

1. 从 approved 产物中提取当前 Phase/子步骤的完整上下文、验收条件、相关代码路径、允许文件、禁止文件和允许命令。
2. Phase 4 implementation 必须消费同一 Phase 4 `task-planning` 产出的 `tasks.md`；Phase 4/5 的 review 子步骤必须读取对应实现/测试子步骤的报告、变更清单和验证证据。
3. 按 status 协议处理结果：
   - `DONE`：进入边界检查和验证。
   - `DONE_WITH_CONCERNS`：先处理 concerns；若影响范围、正确性或证据完整性，Gate 不得 pass。
   - `NEEDS_CONTEXT`：补充上下文后重新构造 prompt 并重新 dispatch。
   - `BLOCKED`：Stop-the-Line，记录 blocker、根因和回退/澄清路径。
4. 将 Agent 输出写入当前 Phase 最终产物，检查边界合规。
5. 执行当前 Phase 的验证步骤，归档证据和门禁状态。

### Subagent 约束（通用）

subagent 只执行 prompt 中指定的当前 task。subagent 不得：推进 Phase、请求用户确认、判断 Gate、创建非当前 Phase 产物、修改 forbidden files、提交/推送/部署、读取 `.harness/rules/` / `.harness/agents/` / `.harness/changes/INDEX.md` 等 Harness 元文件来重新解释任务。subagent 可以使用 Orchestrator 提供的 context packet、项目源码和已批准产物；上下文查询由 Orchestrator 在 Phase 1/2 完成。

Phase 专用约束见对应 Agent 文件的禁止操作节。

### Subagent Prompt 必含字段

- Task description：当前 Phase 完整任务文本，直接粘贴，不让 subagent 自行读取计划文件。
- Approved context：approved spec 摘要；Phase 4 implementation/review 另附当前 tasks 计划、相关代码路径、依赖和架构约束。
- Allowed files / forbidden files。
- Allowed commands / forbidden commands。
- Status protocol：`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`。
- Report format：按对应 Agent 文件 Report Format 节规定的结构。
