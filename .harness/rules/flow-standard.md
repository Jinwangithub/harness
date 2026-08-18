# Standard-flow 规范

> **TL;DR**: Standard-flow 用于新功能、跨模块、高风险或需求不清任务，完整执行 Phase 1-6；Phase 4/5 内保留实现与独立评审子步骤，每个 Phase 完成后必须 Mechanical Gate=`pass` 且用户确认后才能进入下一 Phase。

本文件是 Standard-flow Phase 1-6、Phase 4/5 子步骤和隔离实现原则的权威源。
Flow 分类与路由见 `.harness/rules/flow.md`，Gate 判定见 `.harness/rules/gates.md`，失败处理和回退路径见 `.harness/rules/rollback.md`。

> **边界**：本文件只定义 Standard-flow 执行顺序、每个 Phase/子步骤的入口卡片、Phase 4/5 隔离实现原则和 Standard 特有禁止事项。Gate 判定见 `gates.md`，产物结构见 `changes/structure.md`，Skill 文件路径约定见 `.harness/skills/README.md`。

## Standard-flow

适用：新功能、跨模块、高风险、需求不清。完整 Phase 1-6；Phase 4/5 内部依次执行实现与独立评审子步骤，每个 Phase 完成后必须用户确认才能进入下一 Phase。

| Phase | 目标 | 主要产物 | 确认点 |
|-------|------|----------|--------|
| 1 | 需求分析 | `request_analysis/understanding.md` | CK1 |
| 2 | 需求评审 | `request_analysis/spec.md` | CK2 |
| 3 | 任务规划 | `request_analysis/tasks.md` | CK3 |
| 4 | 实现 + 独立代码评审（`implementation` → `code-review`） | `coding/coding_report_v1.md`, `coding/review/*.md` | CK4 |
| 5 | 单元测试 + 独立测试评审（`unit-test` → `test-review`） | `unit_test/test_report.md`, `unit_test/review/test_review_v1.md` | CK5 |
| 6 | 用户确认 | `delivery-summary.md`, `wiki/candidates.md` | CK6 |

**进入下一 Phase 的唯一条件**：当前 Phase 的所有子步骤完成、Composite Mechanical Gate=`pass` 且用户已确认。进入后立即更新 `summary.md` 的 `Current step`、`Substep` 和 `Resume point`。Phase 6 是 finalization 例外：先以 final Gate=`pass` + Human Approval=`pending` 保持 summary / INDEX 为 `active` 请求最终确认；批准后才更新 final Gate 为 `approved`、同步两处为 `done` 且 Resume point=`none`，随后重跑 validator。

关键边界：

- Phase 4 依次执行实现和独立代码评审：实现子步骤只做编码、编译验证和 Author/Self Review；code-review 子步骤由 fresh Reviewer 只读评审，不能替代 Composite Gate。
- Phase 5 依次执行单元测试和独立测试评审：unit-test 子步骤创建/运行测试；test-review 子步骤由 fresh Reviewer 只读评审，不能修改测试。
- Phase 4/5 的四个报告保持独立，Composite Gate 必须同时检查实现/测试报告和对应评审报告。

Phase/Step 入口必须按本文件对应卡片输出入口状态卡；状态卡必须包含读取 Skills、按条件补读 Skills、失败时补读 Skills、禁止事项、产物提示和 Gate 提示。

## Phase Cards

### Phase 1 — 需求分析

- Agent: Planner (`.harness/agents/planner.md`)
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
  - 禁止产物不存在
  - Fresh evidence 四字段完整

### Phase 3 — 任务规划

- Agent: Planner (`.harness/agents/planner.md`)
- 读取 Skills:
  - `planning-and-task-breakdown`
- 按条件补读 Skills:
  - `api-and-interface-design`: 仅当 risk_flags 或任务类型涉及 API/公共契约/模块边界
  - `security-and-hardening`: 仅当 risk_flags 或任务类型涉及 security/auth/permission
  - `performance-optimization`: 仅当 risk_flags 或任务类型涉及性能风险
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不实现代码
  - 不运行 Phase 5 / unit-test 职责
- 产物提示:
  - `request_analysis/tasks.md`
- Gate 提示:
  - `tasks.md` 存在
  - 每个任务有验收条件
  - Fresh evidence 四字段完整

### Phase 4 — 实现 + 独立代码评审

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
  - 实现范围符合 approved spec/tasks
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
  - 两个 Phase 4 报告均存在
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

### Phase 6 — 用户确认

- 读取 Skills:
  - `documentation-and-adrs`
  - `business-wiki-curation`
- 按条件补读 Skills:
  - 无
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 未经用户要求不执行 git 提交/推送
  - 不改实现代码
- 产物提示:
  - `delivery-summary.md`
  - `wiki/candidates.md`
- Gate 提示:
  - delivery summary 存在
  - Business Wiki candidate check complete
  - human Wiki approval status recorded
  - if approved, `.harness/wiki/index.md` and `.harness/wiki/log.md` are synchronized
  - if rejected/deferred, reason is recorded in candidate artifact and delivery summary
  - Memory 完整
  - 确认前：final Gate=`pass`、Human Approval=`pending`，summary / INDEX 均为 `active`
  - 用户批准后：final Gate Approval=`approved`，summary / INDEX 同步为 `done`、Resume point=`none`
  - 状态同步后 validator PASS
  - 不将 `done` 作为批准前 Gate 条件

## Agent 隔离实现原则

Standard-flow Phase 1-5 采用 controller/subagent 协议：Orchestrator 是 controller。Phase 4 和 Phase 5 各自按 implementation → review 子步骤顺序调度两个 fresh subagent；Phase 6 由 Orchestrator 自行处理。完整的隔离协议定义在 `.harness/agents/orchestrator.md` 的 Dispatch 步骤中。

Phase 4 的 Implementer/Reviewer 和 Phase 5 的 Implementer/Reviewer 定义见 `.harness/agents/implementer.md` 与 `.harness/agents/reviewer.md`。subagent 不继承主会话历史；Orchestrator 必须构造自包含 prompt，把当前子步骤完整任务文本、必要上下文和前一子步骤产物直接放入 prompt。

### Orchestrator 责任

1. 从 approved 产物中提取当前 Phase/子步骤的完整上下文、验收条件、相关代码路径、允许文件、禁止文件和允许命令。
2. Phase 4/5 的 review 子步骤必须读取对应 implementation 子步骤的报告、变更清单和验证证据。
3. 按 status 协议处理结果：
   - `DONE`：进入边界检查和验证。
   - `DONE_WITH_CONCERNS`：先处理 concerns；若影响范围、正确性或证据完整性，Gate 不得 pass。
   - `NEEDS_CONTEXT`：补充上下文后重新构造 prompt 并重新 dispatch。
   - `BLOCKED`：Stop-the-Line，记录 blocker、根因和回退/澄清路径。
4. 将 Agent 输出写入当前 Phase 最终产物，检查边界合规。
5. 执行当前 Phase 的验证步骤，归档证据和门禁状态。

### Subagent 约束（通用）

subagent 只执行 prompt 中指定的当前 task。subagent 不得：推进 Phase、请求用户确认、判断 Gate、创建非当前 Phase 产物、修改 forbidden files、提交/推送/部署、读取 `.harness/rules/` / `.harness/agents/` / `.harness/changes/INDEX.md` 等 Harness 元文件来重新解释任务。subagent 可以读取 `.harness/wiki/`（业务知识）、项目源码和已批准产物。

Phase 专用约束见对应 Agent 文件的禁止操作节。

### Subagent Prompt 必含字段

- Task description：当前 Phase 完整任务文本，直接粘贴，不让 subagent 自行读取计划文件。
- Approved context：spec/tasks 摘要、相关代码路径、依赖、架构约束。
- Allowed files / forbidden files。
- Allowed commands / forbidden commands。
- Status protocol：`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`。
- Report format：按对应 Agent 文件 Report Format 节规定的结构。
