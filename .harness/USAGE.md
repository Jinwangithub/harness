# 实战操作指南

> 拿到一个需求后，按下面的步骤操作。

---

## 两种运行模式

### Full Delivery Mode

用于完整需求交付。Phase 1-10 必须顺序推进，不跳 Phase、不合并门禁。小需求可以压缩每阶段文档篇幅和交互轮次，但每个 Phase 的 Mechanical Gate 与 Human Approval Gate 仍必须独立完成。

### Standalone Skill Mode

用于用户明确只做单点任务，例如只做代码评审、只跑测试、只生成部署清单。此模式可以直接调用对应 Skill，但不得声明完整交付完成，也不得替代 Full Delivery Mode 的阶段证据。

---

## 第一步：告诉 Claude Code 启动 Harness 模式

每次开始新会话时，输入：

```
我准备开发一个新需求，启动 Harness Engineering 模式。
```

Claude Code 会自动读取 `CLAUDE.md` → `.harness/AGENTS.md`，进入 **Orchestrator 模式**，然后告诉你当前项目信息、准备进入 Phase 1。

---

## 第二步：描述需求

直接说需求内容。比如：

```
需求：用户下单后，需要发送订单确认通知。
通知方式支持短信和邮件，用户可以在个人中心选择偏好。
```

Orchestrator 会进入 Phase 1（需求分析），加载 `idea-refine` Skill，做以下事情：

1. **复述需求**让你确认理解是否正确（你必须回答"对"才能继续）
2. **追问边界问题**（比如：用什么短信服务商？邮件模板谁来出？）
3. 输出 `understanding.md`（需求理解笔记）到 `.harness/changes/{type}-{name}-{YYYYMMDD}/`

**你的操作**：确认需求理解是否正确，回答边界问题。Orchestrator 会**停下来等你回复**，你不说"通过"它不会自动进入下一阶段。

---

## 第三步：走完十阶段全流程

Orchestrator 会按以下顺序推进。每个阶段你做三件事中的一种：
- **回答"通过"** — Human Approval Gate 通过，进入下一阶段
- **回答"不通过，原因是..."** — Orchestrator 回退到对应阶段修复
- **回答边界问题**（比如部署环境、参数配置等）

每个阶段必须先满足 Mechanical Gate；Mechanical Gate 不通过时，Orchestrator 不会请求你人工放行。

```
Phase 1: 需求分析
  → 你: 描述需求 → Orchestrator 复述确认 → Mechanical Gate → 你确认 ✓
  → 产 understanding.md（不产 spec.md！Phase 1 不做详细设计）

Phase 2: 需求评审
  → Orchestrator 读取 understanding.md，加载 spec-driven-development Skill
  → 输出 spec.md（不含 tasks.md！那是 Phase 3 的职责）
  → Mechanical Gate → 你确认评审通过 ✓（最多3轮）

Phase 3: 任务规划
  → Orchestrator 读取 spec.md，首次创建 tasks.md
  → Mechanical Gate → 你确认任务拆分合理 ✓

Phase 4: 编码实现
  → Orchestrator 调度 incremental-implementation Skill，按增量切片实现
  → 进度: "Task 2/6 完成" — 每完成一个报告一次
  → 编译验证（mvn clean compile，不运行测试）
  → Mechanical Gate → 你确认编码完成 ✓

Phase 5: 编码评审
  → Orchestrator 并行调度 3 个本地 Skill:
    - .harness/skills/code-review-and-quality/SKILL.md
    - .harness/skills/security-and-hardening/SKILL.md
    - .harness/skills/performance-optimization/SKILL.md
  → 每个完成时报告: "Code Review 审查完成" / "Security Audit 审计完成" / "Performance Review 审查完成"
  → 汇总后三份报告齐备，Mechanical Gate → 一次展示结论并请求确认
  → 你: 看摘要，确认通过 ✓

Phase 6: 单元测试
  → 检查/添加 JaCoCo 插件，编写测试，运行 mvn test + jacoco:report
  → 产出 test_report.md（含行覆盖率和分支覆盖率）
  → Mechanical Gate → 你确认测试结果 ✓

Phase 7: 测试评审
  → 使用 code-review-and-quality 的测试审查标准，按需参考 test-driven-development
  → 产出 test_review_v1.md
  → Mechanical Gate → 你确认通过 ✓

Phase 8: CI 验证
  → mvn verify 运行
  → 产出 ci_report.md
  → Mechanical Gate → 你确认 CI 通过或按规则放行 ✓

Phase 9: 部署验证
  → mvn clean package -DskipTests → 冒烟测试 → 回滚检查
  → 产出 deploy_report.md
  → Mechanical Gate → 你确认部署参数和结果 ✓

Phase 10: 用户确认
  → 汇总交付物清单、质量门禁状态、所有归档文件，检查 memory 沉淀
  → Mechanical Gate → 你最终确认交付 ✓
```

---

## 实际场景速查表

### 场景 1: 实现一个小功能

```
你: 在 UserController 里加一个根据手机号查询用户接口
Orchestrator: 好的，启动 Phase 1 需求分析...
```

因为需求很小，流程会自动压缩文档篇幅和交互轮次，但不跳 Phase、不合并门禁。

### 场景 2: 修复一个 Bug

```
你: 订单支付成功后没有回调通知，帮我查一下
Orchestrator: 启动 Full Delivery Mode，从 Phase 1 明确问题、边界和验收标准。
```

如果你只要求定位原因或给出排查建议，可使用 Standalone Skill Mode 调用 `debugging-and-error-recovery`，但这不代表完整交付完成。

### 场景 3: 重构已有代码

```
你: 把 OrderService 中的支付逻辑拆成单独的 PaymentService
Orchestrator: 启动 Phase 1 需求分析 + 按需加载 deprecation-and-migration Skill
```

会按 Full Delivery Mode 顺序推进，并在相关阶段注入 `deprecation-and-migration` 和 `code-simplification` 技能。

### 场景 4: 评审已有代码（不写新代码）

```
你: /review
```

Standalone Skill Mode：只做评审，调度 `code-review-and-quality`、`security-and-hardening`、`performance-optimization` 并输出评审报告；不得声明完整交付完成。

Full Delivery Mode：当 Phase 1-4 证据已通过时，`/review` 执行 Phase 5。

### 场景 5: 我改主意了，要变更需求

```
你: 之前的需求变了，改成这样...
Orchestrator: 记录变更，回退到 Phase 1
```

回退到 Phase 1，但变更记录保留在 `.harness/changes/` 中。

---

## 常用命令速查

| 你说 | 模式与前置条件 | 效果 |
|------|----------------|------|
| `启动 Harness 模式` | 通用 | 读取 AGENTS.md，进入 Orchestrator 模式 |
| `新需求: ...` | Full Delivery Mode | 开始 Phase 1 |
| `/spec` | Full Delivery Mode；如缺 Phase 1 产物则先补 Phase 1 | 执行 Phase 1-2 |
| `/plan` | Full Delivery Mode；必须已有 Phase 2 spec | 执行 Phase 3 |
| `/build` | Full Delivery Mode；必须已有 Phase 3 tasks | 执行 Phase 4 |
| `/review` | Standalone Skill Mode 或 Full Delivery Mode Phase 5 | 单点评审，或在 Phase 4 通过后执行 Phase 5 |
| `/test` | Standalone Skill Mode 或 Full Delivery Mode Phase 6-7 | 单点测试，或在 Phase 5 通过后执行 Phase 6-7 |
| `/ship` | Full Delivery Mode；必须已有 Phase 7 通过证据 | 执行 Phase 8-10 |
| `回退到 Phase 3` | Full Delivery Mode | 手动指定回退 |
| `当前进度` | 通用 | 查看当前在哪个 Phase |
| `看看 changes 目录` | 通用 | 查看所有变更记录 |

---

## 验收标准检查清单

当你需要判断一个需求是否完成时，对照这个清单：

```
□ Phase 1-10 均有独立 Mechanical Gate 记录
□ spec.md 中定义的所有功能都已实现
□ 所有测试通过（mvn test）
□ JaCoCo 覆盖率 >= 80%
□ 代码评审通过（Must Fix = 0）
□ 安全审计通过（Critical = 0）
□ CI 全绿
□ 预发布环境验证通过
□ .harness/changes/{type}-{name}-{YYYYMMDD}/ 已归档（含所有阶段产物）
□ Phase 10 已完成 memory 检查和用户最终确认
```

---

## 常见问题

**Q: 每次都要走十阶段吗？**
A: 完整交付必须走十阶段。小需求只压缩文档篇幅和交互轮次，不跳 Phase、不合并门禁。

**Q: 只想评审或只想跑测试怎么办？**
A: 使用 Standalone Skill Mode。它可以直接调用评审或测试 Skill，但只能声明单点任务完成，不能声明完整交付完成。

**Q: Orchestrator 说"请确认"的时候我该怎么回应？**
A: 简单说"通过"或"不通过，原因是..."。如果不通过，Orchestrator 会自动回退到对应阶段。

**Q: 审查报告太长了，我只看摘要行吗？**
A: 可以。代码评审报告顶部有 **Verdict** 行，看 Approve/Request Changes 就行。想深入再看详细发现。

**Q: Phase 5 为什么有时候会问多次？**
A: 这是旧版本的问题。新规范已修复：所有审查 Skill 完成后统一汇总，**只问一次用户确认**。

**Q: 中途断电/断网，重新打开怎么办？**
A: 先输入 `启动 Harness 模式`，然后说 `恢复上次进度`。Orchestrator 会读取 `.harness/changes/` 和 `.harness/memory/` 恢复上下文。
