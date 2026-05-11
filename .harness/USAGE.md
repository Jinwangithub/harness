# 实战操作指南

> 拿到一个需求后，按下面的步骤操作。

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
- **回答"通过"** — 门禁通过，进入下一阶段
- **回答"不通过，原因是..."** — Orchestrator 回退到对应阶段修复
- **回答边界问题**（比如部署环境、参数配置等）

```
Phase 1: 需求分析
  → 你: 描述需求 → Orchestrator 复述确认 → 你确认 ✓
  → 产 understanding.md（不产 spec.md！Phase 1 不做详细设计）

Phase 2: 需求评审
  → Orchestrator 读取 understanding.md，加载 spec-driven-development Skill
  → 输出 spec.md（不含 tasks.md！那是 Phase 3 的职责）
  → 你: 确认评审通过 ✓（最多3轮）

Phase 3: 任务规划
  → Orchestrator 读取 spec.md，首次创建 tasks.md
  → 你: 确认任务拆分合理 ✓

Phase 4: 编码实现
  → Orchestrator 调用编码子 Agent，按增量切片实现
  → 进度: "Task 2/6 完成" — 每完成一个报告一次
  → 编译验证（mvn clean compile，不运行测试）
  → 你: 确认编码完成 ✓

Phase 5: 编码评审
  → 并行扇出 3 个审查 Agent，分别加载:
    - .harness/agents/code-reviewer.md（正确性+可读性+架构）
    - .harness/agents/security-auditor.md（安全）
    - .harness/agents/test-engineer.md（测试质量）
  → 每个完成时报告: "Code Reviewer 审查完成" / "Security Auditor 审计完成"
  → 汇总后一次展示结论，只问一次
  → 你: 看摘要，确认通过 ✓

Phase 6: 单元测试
  → 检查/添加 JaCoCo 插件，编写测试，运行 mvn test + jacoco:report
  → 产出 test_report.md（含行覆盖率和分支覆盖率）
  → 你: 确认测试结果 ✓

Phase 7: 测试评审
  → 加载 test-engineer.md 审查测试质量
  → 你: 确认通过 ✓

Phase 8: CI 验证
  → mvn verify 运行
  → 你: 确认 CI 通过 ✓

Phase 9: 部署验证
  → mvn clean package -DskipTests → 冒烟测试
  → 你: 确认部署参数 ✓

Phase 10: 用户确认
  → 汇总交付物清单、质量门禁状态、所有归档文件
  → 你: 最终确认交付 ✓
```

---

## 实际场景速查表

### 场景 1: 实现一个小功能

```
你: 在 UserController 里加一个根据手机号查询用户接口
Orchestrator: 好的，启动 Phase 1 需求分析...
```

因为需求很小，流程会自动压缩，但质量门禁不会跳过。

### 场景 2: 修复一个 Bug

```
你: 订单支付成功后没有回调通知，帮我查一下
Orchestrator: 启动 debugging-and-error-recovery Skill
```

会跳过 Phase 1-3，直接从 Phase 4 开始，但后续 Phase 5-10 照常执行。

### 场景 3: 重构已有代码

```
你: 把 OrderService 中的支付逻辑拆成单独的 PaymentService
Orchestrator: 启动 Phase 1 需求分析 + 加载 deprecation-and-migration Skill
```

会额外注入 `deprecation-and-migration` 和 `code-simplification` 技能。

### 场景 4: 评审已有代码（不写新代码）

```
你: /review
```

直接触发 Phase 5 编码评审，并行扇出 3 个 Agent，出评审报告。

### 场景 5: 我改主意了，要变更需求

```
你: 之前的需求变了，改成这样...
Orchestrator: 记录变更，回退到 Phase 1
```

回退到 Phase 1，但变更记录保留在 `.harness/changes/` 中。

---

## 常用命令速查

| 你说 | 效果 |
|------|------|
| `启动 Harness 模式` | 读取 AGENTS.md，进入 Orchestrator 模式 |
| `新需求: ...` | 开始 Phase 1 |
| `/spec` | 直接进 Phase 1-2（需求分析+评审） |
| `/plan` | 直接进 Phase 3（任务规划） |
| `/build` | 直接进 Phase 4（编码实现） |
| `/review` | 直接进 Phase 5（并行审查） |
| `/test` | 直接进 Phase 6-7（测试+评审） |
| `/ship` | 直接进 Phase 8-10（CI+部署+确认） |
| `回退到 Phase 3` | 手动指定回退 |
| `当前进度` | 查看当前在哪个 Phase |
| `看看 changes 目录` | 查看所有变更记录 |

---

## 验收标准检查清单

当你需要判断一个需求是否完成时，对照这个清单：

```
□ spec.md 中定义的所有功能都已实现
□ 所有测试通过（mvn test）
□ JaCoCo 覆盖率 >= 80%
□ 代码评审通过（Must Fix = 0）
□ 安全审计通过（Critical = 0）
□ CI 全绿
□ 预发布环境验证通过
□ .harness/changes/{type}-{name}-{YYYYMMDD}/ 已归档（含所有阶段产物）
```

---

## 常见问题

**Q: 每次都要走十阶段吗？太慢了怎么办？**
A: 小需求（比如改个字段名）Orchestrator 会自动压缩阶段，但质量门禁不会跳过。流程一致性比流程效率重要——防止"小改动大事故"。

**Q: Orchestrator 说"请确认"的时候我该怎么回应？**
A: 简单说"通过"或"不通过，原因是..."。如果不通过，Orchestrator 会自动回退到对应阶段。

**Q: 审查报告太长了，我只看摘要行吗？**
A: 可以。代码评审报告顶部有 **Verdict** 行，看 Approve/Request Changes 就行。想深入再看详细发现。

**Q: Phase 5 为什么有时候会问多次？**
A: 这是旧版本的问题。新规范已修复：所有审查 Agent 完成后统一汇总，**只问一次用户确认**。

**Q: 中途断电/断网，重新打开怎么办？**
A: 先输入 `启动 Harness 模式`，然后说 `恢复上次进度`。Orchestrator 会读取 `.harness/changes/` 和 `.harness/memory/` 恢复上下文。
