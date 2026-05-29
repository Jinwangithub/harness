# 经验教训

> 每次发现 Agent 犯了错误，就花时间设计一个解决方案，使这个错误永远不再发生。
> 记录格式见 `.harness/memory/README.md`。

2026-05-07 | Phase 1 产出被 Phase 2 覆盖
- 问题: Orchestrator 在需求描述阶段写了 spec.md，然后 Phase 1 的 spec-driven-development Skill 又覆盖写了 spec.md，导致重复劳动。
- 根因: 流程没有明确区分需求澄清和详细设计的产出边界。
- 影响: understanding.md 缺失，spec.md 被写了两次。
- 修复: Phase 1 固定产 understanding.md，Phase 2 基于它产 spec.md。
- 预防: orchestrator.md 规则2（Phase 1/2 产物严格分离）。

2026-05-07 | 变更目录名不符合规范
- 问题: 变更目录被命名为 `001-skill-executor/`，而不是规范的 `feat-skill-executor-20260507/`。
- 根因: 命名规范未强制执行。
- 预防: orchestrator.md 规则5（Phase 1 第一步确定规范目录名）。

2026-05-07 | Phase 2 产 tasks.md 被 Phase 3 覆盖
- 问题: Phase 2 产出了 spec.md + tasks.md，Phase 3 又覆盖重写了 tasks.md。
- 根因: spec-driven-development 默认行为同时产出 spec 和 tasks，但流程上 tasks 应由 Phase 3 创建。
- 预防: orchestrator.md 规则3（Phase 3 首次创建 tasks.md）。

2026-05-07 | Phase 4 和 Phase 6 的测试职责重复
- 问题: Phase 4 运行了单元测试，Phase 6 又跑了一遍，且无覆盖率报告。
- 根因: 编码阶段"每片测试"的默认行为与 Phase 6 重复。
- 修复: Phase 4 仅编译验证，Phase 6 统一做完整测试 + JaCoCo。
- 预防: orchestrator.md 规则4。

2026-05-07 | Phase 5 并行审查无进度反馈 + 重复确认
- 问题: 用户看不到审查 Agent 进度，且被重复询问 3 次确认。
- 预防: Phase 5 逐 Agent 报告完成进度 + 汇总后只问一次。

2026-05-07 | agents/ 角色文件未使用
- 问题: code-reviewer.md、security-auditor.md、test-engineer.md 从未被加载。
- 预防: Phase 5 明确加载 3 个角色文件。

2026-05-07 | 缺少覆盖率报告
- 问题: Phase 6 无覆盖率数据，无法验证 80% 门禁。
- 预防: Phase 6 固定运行 JaCoCo。

2026-05-07 | 变更目录缺少阶段产物
- 问题: changes/ 下只有 3 个文件，缺评审/测试/CI/部署报告。
- 预防: orchestrator.md 规则6（每个 Phase 立即归档）。

2026-05-12 | Phase 5/7 引用了不存在的审查 Agent
- 问题: Phase 5/7 规范引用了 `.harness/agents/code-reviewer.md`、`.harness/agents/security-auditor.md`、`.harness/agents/test-engineer.md`，但当前架构实际只有 Orchestrator 一个 Agent。
- 根因: 历史决策试图用独立审查 Agent 承载评审职责，但文件结构和 Skill 索引已经演进为本地 Skills，文档未同步。
- 影响: 执行者会尝试加载不存在文件，导致 Phase 5/7 执行路径不一致，评审证据和职责边界混乱。
- 修复: 统一改为唯一 Orchestrator + 本地 Skills；Phase 5 并行调度 `code-review-and-quality`、`security-and-hardening`、`performance-optimization`，Phase 7 使用 `code-review-and-quality` 的测试审查标准。
- 预防: AGENTS、orchestrator、development-workflow、quality-gates 中明确 Phase 5/7 不加载独立审查 Agent 文件；references/orchestration-patterns 固化唯一 Orchestrator 模式。

2026-05-12 | "直接进入 Phase"破坏不跳阶段规则
- 问题: USAGE 中存在直接进入 Phase 4/5/6 等说法，与"完整交付不跳 Phase"的硬性规则冲突。
- 根因: 文档没有区分完整交付和单点 Skill 调用，把快捷命令和完整交付阶段混在一起描述。
- 影响: 小需求或快捷命令可能绕过 Phase 1-3、合并门禁或缺少阶段证据，导致交付链路不可追溯。
- 修复: 新增 Full Delivery Mode 与 Standalone Skill Mode；完整交付必须 Phase 1-10 顺序推进，单点 Skill 可直接调用但不得声明完整交付完成。
- 预防: USAGE 快捷命令表增加模式边界和前置条件；orchestrator 和 quality-gates 强化 Mechanical Gate 通过后才进入 Human Approval Gate。

2026-05-26 | 多个进行中变更导致恢复对象不确定
- 问题: `.harness/changes/` 中多个 summary 同时为 `状态: 进行中`，启动时只扫描最新或第一个未完成项会导致恢复目标不确定。
- 根因: changes 目录缺少全局 registry，恢复规则依赖分散 summary 的自然语言状态，无法表达 superseded、legacy、manual-only 等状态。
- 影响: Orchestrator 可能恢复错误变更、跳过当前用户需要确认的变更，或自行猜测恢复对象。
- 修复: 新增 `.harness/changes/INDEX.md`，并更新 AGENTS、orchestrator、workflow 和 changes README 为 registry-first 恢复。
- 预防: 新变更必须维护 INDEX；多个 active auto-resume 或 INDEX/summary 冲突时 Stop-the-Line。

2026-05-26 | completed 与 pending-human 冲突会伪装完成
- 问题: 历史 summary 存在 `状态: 已完成` 但最终 Human Approval Gate 仍为 `pending-human` 的冲突状态。
- 根因: Completion Claim Gate、Human Approval Gate 和 summary 状态之间缺少可执行一致性校验；`pending-human` 未被明确写成合法恢复状态而非完成状态。
- 影响: 后续执行者可能把未获用户确认的变更当作完成，破坏审计链和交付确认纪律。
- 修复: 在 workflow、quality gates、changes README、USAGE 和 INDEX 中明确 `pending-human` 必须保持 Completion lock locked，completed + pending-human 属于 conflict。
- 预防: validator 对历史冲突输出 WARN，对新 summary 中的 canonical 状态违规输出 FAIL。

2026-05-26 | summary 字段不一致降低恢复确定性
- 问题: 历史 summary 中同时出现 `resume_from`、缺失 `Current step` / `Resume point` / `Completion lock`、非 canonical approval wording 等字段差异。
- 根因: 归档模板演进后没有全局索引和 legacy 策略，新旧字段混用且缺少机械检查。
- 影响: 弱模型恢复时需要解释多套字段，容易误判当前步骤、门禁状态和是否能完成。
- 修复: 新 summary 统一使用 `Current step`、`Resume point`、`Completion lock`，历史字段作为 legacy evidence 保留。
- 预防: changes README 定义新模板，validator 对新 summary 废弃字段输出 FAIL，对历史废弃字段输出 WARN。
