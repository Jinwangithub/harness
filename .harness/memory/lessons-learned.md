# 经验教训

> 每次发现 Agent 犯了错误，就花时间设计一个解决方案，使这个错误永远不再发生。
> 记录格式见 `.harness/memory/README.md`。

2026-05-07 | Phase 1 产出被 Phase 2 覆盖
- 问题: Orchestrator 在需求描述阶段写了 spec.md，然后 Phase 1 的 spec-driven-development Skill 又覆盖写了 spec.md，导致重复劳动。
- 根因: 流程没有明确区分需求澄清和详细设计的产出边界。
- 影响: understanding.md 缺失，spec.md 被写了两次。
- 修复: Phase 1 固定产 understanding.md，Phase 2 基于它产 spec.md。
- 预防: `.harness/rules/flow-standard.md` 的 Phase 1/2 入口卡片。

2026-05-07 | 变更目录名不符合规范
- 问题: 变更目录被命名为 `001-skill-executor/`，而不是规范的 `feat-skill-executor-20260507/`。
- 根因: 命名规范未强制执行。
- 预防: `.harness/changes/structure.md` 的目录命名规则。

2026-05-07 | Phase 2 产 tasks.md 被 Phase 3 覆盖
- 问题: Phase 2 产出了 spec.md + tasks.md，Phase 3 又覆盖重写了 tasks.md。
- 根因: spec-driven-development 默认行为同时产出 spec 和 tasks，但流程上 tasks 应由 Phase 3 创建。
- 预防: `.harness/rules/flow-standard.md` 的 Phase 2/3 入口卡片。

2026-05-07 | 实现、测试和交付职责重复
- 问题: 实现阶段运行了完整测试，后续阶段又重复执行，且交付阶段缺少独立验证边界。
- 根因: 编码阶段默认运行测试，流程没有明确实现与测试的职责边界。
- 修复: Phase 4 只做编译验证，Phase 5 统一执行测试和覆盖率检查，Phase 6 只做交付归档。
- 预防: `.harness/rules/flow-standard.md` 的 Phase 4-6 入口卡片。

2026-05-07 | 评审进度反馈和确认重复
- 问题: 用户看不到评审进度，且同一阶段被重复询问确认。
- 预防: Orchestrator 汇总评审结果后只请求一次阶段确认。

2026-05-07 | 缺少覆盖率报告
- 问题: 测试阶段无覆盖率数据，无法完成项目覆盖率门禁。
- 预防: Phase 5 固定记录项目覆盖率命令和报告路径。

2026-05-07 | 变更目录缺少阶段产物
- 问题: 变更目录缺少阶段报告，交付证据无法完整复查。
- 预防: 每个 Phase 或 Lite step 完成后立即归档对应产物，并由 Gate 检查路径。

2026-05-26 | 多个进行中变更导致恢复对象不确定
- 问题: `.harness/changes/` 中多个 summary 同时为 `状态: 进行中`，启动时只扫描最新或第一个未完成项会导致恢复目标不确定。
- 根因: 恢复规则依赖分散 summary 的自然语言状态，缺少全局 registry。
- 影响: Orchestrator 可能恢复错误变更、跳过当前用户需要确认的变更，或自行猜测恢复对象。
- 修复: 新增 `.harness/changes/INDEX.md`，并统一使用 registry-first 恢复。
- 预防: 新变更必须维护 INDEX；多个 active 或 INDEX/summary 冲突时 Stop-the-Line。

2026-05-26 | 最终确认与状态冲突会伪装完成
- 问题: 变更状态可能已经标记为 `done`，但最终 Human Approval 仍未批准。
- 根因: Gate、summary 和 INDEX 的状态同步缺少机械一致性检查。
- 影响: 后续执行者可能把未获用户确认的变更当作完成。
- 修复: 统一使用 `approved` / `rejected` / `pending`，并由 validator 检查最终状态组合。
- 预防: 只有 final Gate 批准、summary 和 INDEX 同步为 `done` 后才能声明完成。

2026-05-26 | summary 字段不一致降低恢复确定性
- 问题: summary 中的 `Current step`、`Resume point` 或审批状态不一致。
- 根因: 归档模板和 registry 缺少统一字段与机械检查。
- 影响: 弱模型恢复时需要解释多套字段，容易误判当前步骤、门禁状态和是否能完成。
- 修复: summary 和 INDEX 统一使用 `Current step`、`Resume point` 和 canonical approval 状态。
- 预防: changes 模板定义字段，validator 检查状态和恢复点一致性。
