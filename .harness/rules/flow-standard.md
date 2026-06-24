# Standard-flow 规范

> **TL;DR**: Standard-flow 用于新功能、跨模块、高风险或需求不清任务，完整执行 Phase 1-10；每个 Phase 完成后必须 Mechanical Gate=`pass` 且用户确认后才能进入下一 Phase。

本文件是 Standard-flow Phase 1-10、Phase Cards 和 Phase 4 隔离实现原则的权威源。
Flow 分类与路由见 `.harness/rules/flow.md`，Gate 判定见 `.harness/rules/gates.md`，失败处理和回退路径见 `.harness/rules/rollback.md`。

> **边界**：本文件只定义 Standard-flow 执行顺序、每个 Phase 的入口卡片、Phase 4 隔离实现原则和 Standard 特有禁止事项。Gate 判定见 `gates.md`，产物结构见 `changes/structure.md`，Skill 文件路径约定见 `.harness/skills/README.md`。

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
| 10 | 用户确认 | `delivery-summary.md`, `wiki/candidates.md` | CK10 |

**进入下一 Phase 的唯一条件**：当前 Phase Mechanical Gate=`pass` 且用户已确认。进入后立即更新 `summary.md` 的 `Current step` 和 `Resume point`。

关键边界：

- 各 Phase/Step 的读取 Skills、补读 Skills、禁止事项见本文件对应入口卡片。
- Phase 4 只做编码实现、编译验证和 Author/Self Review，不运行 Phase 6 测试职责。
- Phase 5 是 Independent Review，不替代 Phase 4 自检。

Phase/Step 入口必须按本文件对应卡片输出入口状态卡；状态卡必须包含读取 Skills、按条件补读 Skills、失败时补读 Skills、禁止事项、产物提示和 Gate 提示。

## Phase Cards

### Phase 1 — 需求分析

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
  - 不运行 Phase 6 测试职责
- 产物提示:
  - `request_analysis/tasks.md`
- Gate 提示:
  - `tasks.md` 存在
  - 每个任务有验收条件
  - Fresh evidence 四字段完整

### Phase 4 — 编码实现

- 读取 Skills:
  - `incremental-implementation`
- 按条件补读 Skills:
  - `api-and-interface-design`: 仅当涉及公共契约变化
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不推进 Phase
  - 不请求确认
  - 不判断 Gate
  - 不运行 Phase 6 测试职责
  - 不冒充 Phase 5
- 产物提示:
  - `coding/isolation/input_packet.md`
  - `coding/isolation/subagent_prompt.md`
  - `coding/isolation/subagent_output.md`
  - `coding/isolation/merge_report.md`
  - `coding/coding_report_v1.md`
- Gate 提示:
  - fresh subagent 隔离执行证据四件套存在
  - subagent status 已处理（DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT）
  - 边界检查通过（allowed files、禁止 Phase/Gate/确认/测试职责声明）
  - 编译证据存在
  - Author/Self Review 完成

### Phase 5 — 编码评审

- 读取 Skills:
  - `code-review-and-quality`
- 按条件补读 Skills:
  - `security-and-hardening`: 仅当 risk_flags 或评审发现涉及安全风险
  - `performance-optimization`: 仅当 risk_flags 或评审发现涉及性能风险
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不直接实现修复
  - Must Fix/Critical 回退 Phase 4
- 产物提示:
  - `coding/review/*.md`
- Gate 提示:
  - 独立评审报告存在
  - Critical=0
  - Must Fix=0
  - Fresh evidence 四字段完整

### Phase 6 — 单元测试

- 读取 Skills:
  - `test-driven-development`
- 按条件补读 Skills:
  - 无
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不改需求/spec
  - 实现缺陷回退 Phase 4
- 产物提示:
  - `unit_test/test_report.md`
- Gate 提示:
  - 测试通过
  - 测试数 > 0
  - 覆盖率符合项目阈值
  - Fresh evidence 四字段完整

### Phase 7 — 测试评审

- 读取 Skills:
  - `code-review-and-quality`
  - `test-driven-development`
- 按条件补读 Skills:
  - 无
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不扩大测试范围为新需求
  - 发现缺口回退 Phase 6 或更早
- 产物提示:
  - `unit_test/review/test_review_v1.md`
- Gate 提示:
  - 测试评审报告存在
  - Must Fix=0
  - Fresh evidence 四字段完整

### Phase 8 — CI 验证

- 读取 Skills:
  - `ci-cd-and-automation`
- 按条件补读 Skills:
  - 无
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不发布
  - 不绕过失败 CI
- 产物提示:
  - `ci_result/ci_report.md`
- Gate 提示:
  - CI 报告存在且成功
  - Fresh evidence 四字段完整

### Phase 9 — 部署验证

- 读取 Skills:
  - `ci-cd-and-automation`
- 按条件补读 Skills:
  - `security-and-hardening`: 仅当部署风险涉及安全/auth/permission
  - `performance-optimization`: 仅当部署风险涉及性能/容量
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不替代最终交付确认
  - 部署风险回退 Phase 8/9
- 产物提示:
  - `deployment/deploy_report.md`
- Gate 提示:
  - 部署报告存在
  - 冒烟/回滚检查完成
  - Fresh evidence 四字段完整

### Phase 10 — 用户确认

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
  - `INDEX.md` status 同步为 done
  - Human Approval=approved

## Phase 4 Subagent 隔离实现原则

Phase 4 采用 controller/subagent 协议：Orchestrator 是 controller，fresh subagent 是受限 implementer。subagent 不继承主会话历史；Orchestrator 必须构造自包含 prompt，把当前 slice 的完整任务文本和必要上下文直接放入 prompt，不得要求 subagent 自行读取完整计划或 Harness 流程文件。

### Orchestrator 责任

1. 从 approved `spec.md` / `tasks.md` 提取当前 Task Group / Slice 的完整文本、验收条件、相关代码路径、允许文件、禁止文件和 Phase 4 允许命令。
2. 归档 `coding/isolation/input_packet.md`。
3. 基于 input packet 构造实际发送给 subagent 的自包含 prompt，并归档 `coding/isolation/subagent_prompt.md`。
4. 使用 fresh subagent 执行实现；同一 slice 不复用历史 subagent 上下文。
5. 归档 subagent 返回为 `coding/isolation/subagent_output.md`。
6. 按 status 协议处理结果：
   - `DONE`：进入边界检查和编译验证。
   - `DONE_WITH_CONCERNS`：先处理 concerns；若影响范围、正确性或证据完整性，Gate 不得 pass。
   - `NEEDS_CONTEXT`：补充上下文后重新构造 prompt 并重新 dispatch。
   - `BLOCKED`：Stop-the-Line，记录 blocker、根因和回退/澄清路径。
7. 写入 `coding/isolation/merge_report.md`，检查 allowed files、禁止产物、禁止声明和 subagent status 处理结果。
8. 执行 Phase 4 compile/build/typecheck 或 approved narrow smoke check，归档编译证据、Author/Self Review、`coding_report_v1.md` 和 CK4 门禁状态。

### Subagent 约束

subagent 只执行 prompt 中指定的当前 slice。subagent 不得：推进 Phase、请求用户确认、判断 Gate、创建 Phase 5+ 产物、修改 forbidden files、运行或冒充 Phase 6 测试职责、提交/推送/部署、要求读取完整 `summary.md` / `tasks.md` / Harness 规则来重新解释任务。

### Subagent Prompt 必含字段

- Task description：当前 slice 完整文本，直接粘贴，不让 subagent 自行读取计划文件。
- Approved context：spec 摘要、相关代码路径、依赖、架构约束。
- Allowed files / forbidden files。
- Allowed commands / forbidden commands。
- Status protocol：`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`。
- Report format：status、what changed、files changed、commands run、exit codes、self-review、concerns、boundary compliance。
