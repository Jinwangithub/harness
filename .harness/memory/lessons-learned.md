# 经验教训

> 每次发现 Agent 犯了错误，就花时间设计一个解决方案，使这个错误永远不再发生。

## 格式

```
YYYY-MM-DD | {标题}
- 问题: {错误描述}
- 根因: {为什么发生}
- 影响: {造成了什么后果}
- 修复: {如何修复}
- 预防: {如何防止再犯 — 规则/Skill/门禁变更}
```

## 记录

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

2026-05-12 | “直接进入 Phase”破坏不跳阶段规则
- 问题: USAGE 中存在直接进入 Phase 4/5/6 等说法，与“完整交付不跳 Phase”的硬性规则冲突。
- 根因: 文档没有区分完整交付和单点 Skill 调用，把快捷命令和完整交付阶段混在一起描述。
- 影响: 小需求或快捷命令可能绕过 Phase 1-3、合并门禁或缺少阶段证据，导致交付链路不可追溯。
- 修复: 新增 Full Delivery Mode 与 Standalone Skill Mode；完整交付必须 Phase 1-10 顺序推进，单点 Skill 可直接调用但不得声明完整交付完成。
- 预防: USAGE 快捷命令表增加模式边界和前置条件；orchestrator 和 quality-gates 强化 Mechanical Gate 通过后才进入 Human Approval Gate。
