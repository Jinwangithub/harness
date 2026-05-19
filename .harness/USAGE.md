# 实战操作指南

> 拿到一个需求后，Orchestrator 会先执行 Flow Classifier，自动选择 Standard-flow、Lite-flow 或 Mini-flow。

---

## 运行模式

### Standard-flow

用于高风险或不明确需求：新功能、跨模块、架构/数据/安全/权限/外部接口/迁移/性能/部署等。Phase 1-10 必须顺序推进，不跳 Phase、不合并 Mechanical Gate。确认策略为 `mandatory`，保持 CK1-CK9 阶段确认。

### Lite-flow

用于单模块/少量文件、明确低风险行为变化、简单 bugfix、简单测试补充。确认策略为 `batched`：需求+简化计划确认一次，最终验证/评审摘要确认一次；中间 Mechanical Gate 通过则继续。

### Mini-flow

用于 typo、注释、格式、纯文档、README 小修、无行为变化小配置。确认策略为 `exception-only`：仅分类不确定、门禁失败/阻塞、需要业务判断或最终摘要时确认。

### Standalone Skill Mode

用于用户明确只做单点任务，例如只做代码评审、只跑测试、只生成部署清单。此模式可以直接调用对应 Skill，但不得声明完整交付完成，也不得替代所选交付流程的阶段证据。

任何运行模式都不能绕过 Mechanical Gate、fresh verification evidence、Memory check、Stop-the-Line 或必要 Human Approval Gate。

---

## 第一步：告诉 Claude Code 启动 Harness 模式

每次开始新会话时，输入：

```text
我准备开发一个新需求，启动 Harness Engineering 模式。
```

Claude Code 会自动读取 `CLAUDE.md` → `.harness/AGENTS.md`，进入 Orchestrator 模式，检查 `.harness/changes/` 和 `.harness/memory/`，然后准备执行 Flow Classifier。

---

## 第二步：描述需求

直接说需求内容。比如：

```text
需求：用户下单后，需要发送订单确认通知。
通知方式支持短信和邮件，用户可以在个人中心选择偏好。
```

Orchestrator 会先执行 Flow Classifier，并在 `summary.md` 写入：

- Flow
- Selection basis
- Risk flags
- Confirmation policy
- Upgrade triggers

如果需求涉及高风险或不明确内容，会进入 Standard-flow；如果明确低风险，会自动进入 Lite-flow 或 Mini-flow。

---

## 第三步：按选定流程推进

### Standard-flow

你会在每个关键 Phase 做三件事中的一种：

- 回答“通过” — Human Approval Gate 通过，进入下一阶段。
- 回答“不通过，原因是...” — Orchestrator 回退到对应阶段修复。
- 回答边界问题（比如部署环境、参数配置等）。

每个阶段必须先满足 Mechanical Gate；Mechanical Gate 不通过时，Orchestrator 不会请求你人工放行。

```text
Phase 1: 需求分析
  → 产 understanding.md（不产 spec.md）
  → Mechanical Gate → CK1 用户确认

Phase 2: 需求评审
  → 产 spec.md（不含 tasks.md）
  → Mechanical Gate → CK2 用户确认

Phase 3: 任务规划
  → 首次创建 tasks.md
  → Mechanical Gate → CK3 用户确认

Phase 4: 编码实现
  → 编译验证（mvn clean compile，不运行测试）
  → Author/Self Review
  → Mechanical Gate → CK4 用户确认

Phase 5: 编码评审
  → code/security/performance 三轴隔离评审
  → Mechanical Gate → CK5 用户确认

Phase 6: 单元测试
  → mvn test + jacoco:report
  → Mechanical Gate → CK6 用户确认

Phase 7: 测试评审
  → 测试质量审查
  → Mechanical Gate → CK7 用户确认

Phase 8: CI 验证
  → mvn verify
  → Mechanical Gate

Phase 9: 部署验证
  → package、冒烟、回滚检查
  → Mechanical Gate → CK8 用户确认

Phase 10: 用户确认
  → 汇总交付物、质量门禁、memory
  → Mechanical Gate → CK9 最终确认
```

### Lite-flow

```text
L1: 需求确认+简化计划
  → 产 lite_spec.md + checklist.md
  → Mechanical Gate → batched 确认一次

L2: 实现
  → 按 checklist 修改
  → Mechanical Gate 通过则继续

L3: 验证/压缩评审
  → 产 verification_report.md + review_summary.md
  → Mechanical Gate 通过则继续

L4: 交付确认
  → 展示最终验证/评审摘要
  → batched 最终确认一次
```

### Mini-flow

```text
M1: 理解/分类
  → summary.md 记录 Flow Classification
M2: 修改
  → 仅无行为变化小改动
M3: 验证
  → 内容审查、一致性搜索或文件检查
M4: 记录/总结
  → Memory check + 最终摘要
```

---

## 任务示例表

| 任务 | 推荐 Flow | 原因 |
|------|-----------|------|
| README typo | Mini-flow | 纯文档小修，无行为变化 |
| 注释措辞调整 | Mini-flow | 无运行时行为变化 |
| 单文件低风险 bugfix | Lite-flow | 有行为变化但影响面小、需求明确 |
| 简单测试补充 | Lite-flow | 低风险、验证目标明确 |
| 新增 API | Standard-flow | 涉及接口契约和外部调用面 |
| 修改数据库 schema | Standard-flow | 涉及数据和迁移风险 |
| 权限/认证逻辑调整 | Standard-flow | 涉及 auth/security 风险 |
| 支付链路改动 | Standard-flow | 涉及 payment/data consistency 风险 |
| 性能瓶颈治理 | Standard-flow | 涉及 perf 风险和验证复杂度 |
| 需求描述不清 | Standard-flow | 需要完整澄清和确认链路 |

---

## 常用命令速查

| 你说 | 模式与前置条件 | 效果 |
|------|----------------|------|
| `启动 Harness 模式` | 通用 | 读取 AGENTS.md，进入 Orchestrator 模式 |
| `新需求: ...` | 自动 Flow Classifier | 选择 Mini/Lite/Standard 并创建变更归档 |
| `/spec` | Standard-flow 或 Lite-flow 需求阶段 | Standard 执行 Phase 1-2；Lite 生成 lite_spec |
| `/plan` | Standard-flow 或 Lite-flow 规划阶段 | Standard 执行 Phase 3；Lite 生成 checklist |
| `/build` | 已有计划/清单 | 执行实现步骤 |
| `/review` | Standalone Skill Mode 或流程评审步骤 | 单点评审，或执行所选流程的评审步骤 |
| `/test` | Standalone Skill Mode 或流程验证步骤 | 单点测试，或执行所选流程的验证步骤 |
| `/ship` | 已有验证和评审证据 | 执行交付确认步骤 |
| `回退到 Phase 3` | Standard-flow | 手动指定回退 |
| `当前进度` | 通用 | 查看当前在哪个 Phase 或 Flow step |
| `看看 changes 目录` | 通用 | 查看所有变更记录 |

---

## 验收标准检查清单

### Standard-flow

```text
□ Phase 1-10 均有独立 Mechanical Gate 记录
□ spec.md 中定义的所有功能都已实现
□ 所有测试通过
□ 覆盖率达标
□ 代码评审通过（Must Fix = 0）
□ 安全审计通过（Critical = 0）
□ CI 全绿
□ 部署验证通过
□ .harness/changes/{type}-{name}-{YYYYMMDD}/ 已归档（含所有阶段产物）
□ Phase 10 已完成 memory 检查和用户最终确认
```

### Lite-flow

```text
□ Flow Classification 已记录
□ lite_spec.md 和 checklist.md 已归档
□ checklist 项均完成或明确延期
□ verification_report.md 列出 fresh verification evidence
□ review_summary.md 中 Critical=0、Must Fix=0
□ Memory check 完成
□ batched 确认点已按策略处理
```

### Mini-flow

```text
□ Flow Classification 已记录
□ 变更确认为无行为变化
□ verification_report.md 列出内容审查/一致性搜索/文件检查证据
□ Memory check 完成
□ exception-only 确认点已按策略处理
```

---

## 常见问题

**Q: 每次都要走十阶段吗？**
A: 不一定。Orchestrator 会先执行 Flow Classifier。高风险或完整需求走 Standard-flow；明确低风险任务走 Lite-flow 或 Mini-flow。

**Q: 减少确认点是否等于取消 Human Approval Gate？**
A: 不是。Human Approval Gate 的时机可以按风险分级，但不能绕过 Mechanical Gate、fresh evidence、Memory check 或 Stop-the-Line。

**Q: 只想评审或只想跑测试怎么办？**
A: 使用 Standalone Skill Mode。它可以直接调用评审或测试 Skill，但只能声明单点任务完成，不能声明完整交付完成。

**Q: Orchestrator 说“请确认”的时候我该怎么回应？**
A: 简单说“通过”或“不通过，原因是...”。如果不通过，Orchestrator 会回退到对应阶段或分级流程步骤。

**Q: 审查报告太长了，我只看摘要行吗？**
A: 可以。代码评审报告顶部有 Verdict 行，看 Approve/Request Changes 就行。想深入再看详细发现。

**Q: Phase 5 为什么有时候会问多次？**
A: Standard-flow 的 Phase 5 所有审查 Skill 完成后统一汇总，只问一次用户确认。Lite-flow 使用最终验证/评审摘要确认一次。

**Q: 中途断电/断网，重新打开怎么办？**
A: 先输入 `启动 Harness 模式`，然后说 `恢复上次进度`。Orchestrator 会读取 `.harness/changes/` 和 `.harness/memory/` 恢复上下文。
