# 开发流程规范

> **TL;DR**: 收到需求 → Flow Classifier 分类（Lite/Standard）→ 按 Phase 执行 → 每个 Phase 出口过 Gate → 失败按回退路径处理。

本文件是 Flow Classifier、Lite/Standard-flow 执行顺序、Phase/Step 入口卡片、Phase 4 隔离原则和回退路径的权威源。
门禁检查表见 `.harness/rules/gates.md`，Memory 模板见 `.harness/memory/README.md`。

> **边界**：本文件只定义 Flow 分类、执行顺序、每个 Phase/Step 的入口卡片和回退路径。Gate 判定见 `gates.md`，产物结构见 `changes/structure.md`，Skill 文件路径约定见 `.harness/skills/README.md`；本文件不定义 Skill role 或加载类型术语。

## Flow Classifier

> **安全默认值**：任何不确定 → 一律选 Standard-flow。Lite-flow 仅用于 100% 确定安全且满足所有 Lite 条件的场景。

收到新需求后，必须先分类，并把结果写入 `.harness/changes/{id}/summary.md`。

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
- [ ] 涉及治理规则/模板/Flow Phase Cards/Gate/Memory/changes 结构变更

以上全部为 NO → 进入机械判定清单。

### 机械判定清单（逐项回答并写入 summary.md）

1. 影响面是否单模块/少量文件，或纯文档/格式/注释？
2. 是否修改治理规则、模板、流程、Gate、Memory 或 changes 结构？如是 → Standard-flow，`risk_flags` 不得为 `none`。
3. 是否跨模块、跨目录边界或改变公共契约？
4. 是否涉及 API、DB、auth、security、perf、migration、architecture 或 deployment？
5. 是否有可机械复核的 `low_risk_proof`？没有则不得选 Lite-flow。
6. 是否需要业务判断或用户确认未定义规则？如是 → `unclear-requirement`，进入 Standard-flow。

## Phase/Step 入口卡片

每个 Phase/Step 入口必须读取并输出当前卡片，只列当前 Phase/Step，不复制其他阶段内容。

卡片字段固定为：

- 读取 Skills：本阶段开始前必须读取的 Skill。
- 按条件补读 Skills：只有条件成立才读取；条件不成立时记录“不需要 + 原因”。
- 失败时补读 Skills：仅在 fail/blocked/异常行为时读取。
- 禁止事项：本阶段不得执行的动作或不得创建的产物。
- 产物提示：本阶段主要产物。
- Gate 提示：出口 Gate 重点，具体判定见 `gates.md`。

Skill 文件路径按 `.harness/skills/{name}/SKILL.md` 约定解析。

## Lite-flow

适用：typo、注释、格式、纯文档、小配置、简单 bugfix、简单测试补充，且 `low_risk_proof` 可机械复核。

必需产物：`summary.md`（含 inline lite spec）、`request_analysis/checklist.md`、`verification_report.md`（含压缩评审）

执行顺序：

1. **L1** 需求确认+计划：写入 `summary.md`（含 inline lite spec）和 `checklist.md`；Mechanical Gate=`pass` 后请求用户确认；未确认前不得进入 L2。
2. **L2** 实现：按 checklist 驱动修改，无独立文件；风险扩大则 Stop-the-Line 并升级 Standard-flow。
3. **L3** 验证+交付：生成 `verification_report.md`（含压缩评审：Critical/Must Fix 计数、评审结论），包含 fresh evidence 和 Memory check；用户最终确认后标记 `已完成`。

### Lite Step Cards

#### L1 — 需求确认+计划

- 读取 Skills:
  - `idea-refine`
- 按条件补读 Skills:
  - `context-engineering`: 仅当需要上下文恢复/压缩
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不创建 Standard-only 产物
  - 不实现代码
- 产物提示:
  - `summary.md`（含 inline lite spec）
  - `request_analysis/checklist.md`
- Gate 提示:
  - `low_risk_proof` 存在
  - `INDEX.md` 标记 active
  - Fresh evidence 四字段完整

#### L2 — 实现

- 读取 Skills:
  - `incremental-implementation`
- 按条件补读 Skills:
  - `api-and-interface-design`: 仅当风险扩大涉及公共契约变化
  - `security-and-hardening`: 仅当风险扩大涉及 security/auth/permission
  - `performance-optimization`: 仅当风险扩大涉及性能风险
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不跳过验证
  - 不引入风险扩大；一旦风险扩大必须 Stop-the-Line 并升级 Standard-flow
  - 不创建 Standard-only 产物
- 产物提示:
  - 按 `request_analysis/checklist.md` 执行修改，无独立阶段文件
- Gate 提示:
  - 只修改 checklist 范围
  - 未创建 Standard-only 产物
  - Fresh evidence 四字段完整

#### L3 — 验证+交付

- 读取 Skills:
  - `code-review-and-quality`
  - `documentation-and-adrs`
- 按条件补读 Skills:
  - 无
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不创建 Standard-only 产物
  - 未完成验证和 Memory check 前不得标记完成
- 产物提示:
  - `verification_report.md`（含压缩评审）
- Gate 提示:
  - Critical=0
  - Must Fix=0
  - Memory check 完成
  - `INDEX.md` status 同步为 done
  - Fresh evidence 四字段完整

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

**进入下一 Phase 的唯一条件**：当前 Phase Mechanical Gate=`pass` 且用户已确认。进入后立即更新 `summary.md` 的 `Current step` 和 `Resume point`。

关键边界：

- 各 Phase/Step 的读取 Skills、补读 Skills、禁止事项见本文件对应入口卡片。
- Phase 4 只做编码实现、编译验证和 Author/Self Review，不运行 Phase 6 测试职责。
- Phase 5 是 Independent Review，不替代 Phase 4 自检。

Phase/Step 入口必须按本文件对应卡片输出入口状态卡；状态卡必须包含读取 Skills、按条件补读 Skills、失败时补读 Skills、禁止事项、产物提示和 Gate 提示。

### Phase Cards

#### Phase 1 — 需求分析

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

#### Phase 2 — 需求评审

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

#### Phase 3 — 任务规划

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

#### Phase 4 — 编码实现

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
  - `coding/coding_report_v1.md`
- Gate 提示:
  - 隔离执行证据存在
  - 编译证据存在
  - Author/Self Review 完成

#### Phase 5 — 编码评审

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

#### Phase 6 — 单元测试

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

#### Phase 7 — 测试评审

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

#### Phase 8 — CI 验证

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

#### Phase 9 — 部署验证

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

#### Phase 10 — 用户确认

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
  - `INDEX.md` status 同步为 done
  - Human Approval=approved

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
