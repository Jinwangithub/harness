# Harness 项目评价与 Superpowers 对比分析

## 结论先行

当前 Harness 项目已经不是普通的“提示词集合”，而是一个 **项目内嵌式 AI 工程治理框架**。它的核心价值在于：

- 把 AI 编码从“会话型执行”拉回到“工程流程管理”；
- 用 `.harness/changes/` 做变更审计；
- 用 Mechanical Gate + Human Approval Gate 抑制“口头完成”；
- 用 `.harness/memory/` 做跨会话经验沉淀；
- 用 `.harness/wiki/` 抑制业务规则猜测；
- 用本地 Skills 保证团队 clone 即用。

如果和 Superpowers 比较：

> **Harness 更像企业级工程管控系统；Superpowers 更像高纪律、高效率的 AI 编码执行体系。**

两者不是谁替代谁的问题，而是偏重点不同。

---

## 一、当前 Harness 项目评价

### 1. 整体设计成熟度：较高

从 `.harness/AGENTS.md` 可以看到，项目已经定义了完整的十阶段工作流：

```text
需求分析 → 需求评审 → 任务规划 → 编码实现 → 编码评审 → 单元测试 → 测试评审 → CI验证 → 部署验证 → 用户确认
```

这说明 Harness 已经具备完整的软件交付生命周期，而不是只覆盖“写代码”阶段。

特别值得肯定的是：

- 入口地图清晰：`.harness/AGENTS.md`
- Orchestrator 唯一中枢明确：`.harness/agents/orchestrator.md`
- Skill 索引完整：`.harness/skills/README.md`
- 规则体系独立：`.harness/rules/`
- 质量门禁独立定义：`.harness/rules/04-quality-gates.md`
- Memory 系统独立存在：`.harness/memory/`
- Wiki 业务知识层独立存在：`.harness/wiki/`

这已经具备“框架化”的雏形。

### 2. 最大亮点：工程治理闭环

Harness 最有价值的不是 22 个 skills，而是以下闭环：

```text
需求 → 产物 → 门禁 → 验证证据 → 人工确认 → Memory 记录 → 下一阶段
```

尤其是 `.harness/rules/02-development-workflow.md` 明确规定每个 Phase 出口顺序：

1. Memory 检查；
2. Mechanical Gate；
3. fresh verification evidence；
4. 失败处理；
5. Human Approval Gate；
6. 用户确认后进入下一 Phase。

这比很多 AI 编码框架更工程化。

Superpowers 强在“个人执行纪律”，而 Harness 强在“团队交付治理”。

### 3. Memory 系统是原创优势

`.harness/agents/orchestrator.md` 要求每个 Phase 出口强制检查 Memory：

- 架构决策 → `decisions.log`
- Agent 错误/教训 → `lessons-learned.md`
- 技术限制 → `known-issues.md`

这点非常关键。

很多 AI workflow 最大的问题是：

> 每次会话都像失忆一样重新犯错。

Harness 的 Memory 系统试图把 AI 的一次性经验转化成项目资产，这是它区别于 Superpowers 的核心优势之一。

### 4. 当前主要问题：流程偏重，执行摩擦较高

Harness 目前的十阶段流程非常完整，但对于小改动可能显得重。

虽然已经有 Mini-flow / Lite-flow，但目前仍有几个问题：

1. 默认 Standard-flow 的心理成本较高；
2. Mini-flow / Lite-flow 的触发规则还不够自动化；
3. 每个 Phase 都要求 Human Approval Gate，容易造成频繁打断；
4. 文档产物较多，可能导致“为流程而流程”；
5. 对非 Java/Spring Boot 项目的适配还不够自然。

如果团队不能严格执行，Harness 可能从“质量保障”变成“文档负担”。

---

## 二、Harness vs Superpowers 对比

### 总体定位

| 维度 | Harness | Superpowers |
|---|---|---|
| 核心定位 | 工程治理框架 | AI 编码纪律体系 |
| 适合对象 | 团队、企业级项目、长期维护项目 | 个人开发者、高频编码、快速迭代 |
| 主要优势 | 可审计、可追溯、可恢复、可沉淀 | TDD 强、执行快、纪律硬、上下文隔离好 |
| 主要风险 | 流程重、摩擦高、泛化弱 | 缺少项目级治理、记忆弱、审计弱 |

---

## 三、Harness 的优点

### 1. 变更可审计

`.harness/AGENTS.md` 要求每次变更归档到：

```text
.harness/changes/{type}-{name}-{YYYYMMDD}/
```

每个阶段都有明确产物路径。这让 AI 编码过程可回溯、可检查。

Superpowers 更依赖当前会话和执行技能，不强制完整阶段归档。

### 2. 门禁模型更形式化

`.harness/rules/04-quality-gates.md` 定义了 Mechanical Gate，状态只能是：

```text
pass / fail / blocked
```

并且明确要求先 Mechanical Gate，再 Human Approval Gate。

这比“我觉得可以了”的 AI 输出可靠得多。

### 3. 更适合团队协作

Harness 的规则、Skills、Memory、Wiki 都在项目仓库里。

优点是：

- clone 即用；
- 团队规则一致；
- 版本随项目演进；
- 不依赖外部插件安装；
- 适合组织内沉淀标准流程。

Superpowers 的插件化更适合跨项目个人使用，但组织级约束相对弱。

### 4. 对 Java/Spring Boot 项目有深度适配

`.harness/AGENTS.md` 定义了分层架构规则：

```text
controller → service → repository
```

这类技术栈专项规则，是 Superpowers 这类通用框架通常不会内置的。

### 5. 失败处理更系统

`.harness/rules/02-development-workflow.md` 定义了 Failure Handling Protocol：

1. 停止进入下一阶段；
2. 记录失败证据；
3. 复现失败条件；
4. 定位根因；
5. 回退到对应 Phase；
6. 修复并重新验证；
7. 记录 lessons-learned。

这个很接近严肃工程组织的 Stop-the-Line 机制。

---

## 四、Harness 的缺点

### 1. 流程重

十阶段流程对以下任务过重：

- typo；
- 注释；
- 小配置；
- 单文件小修复；
- README 小改动；
- 简单测试补充。

虽然已有 Mini-flow / Lite-flow，但文档上仍强调默认 Standard-flow，实际使用中容易让用户觉得“太麻烦”。

### 2. Human Approval Gate 过于频繁

当前设计中多个阶段都需要用户确认：

- Phase 1 后确认需求；
- Phase 2 后确认 spec；
- Phase 3 后确认任务；
- Phase 4 后确认编码；
- Phase 5 后确认评审；
- Phase 6 后确认测试；
- Phase 7 后确认测试评审；
- Phase 9 前确认部署；
- Phase 10 最终确认。

这对高风险任务合理，但对低风险任务会降低流畅度。

建议区分：

- 强确认；
- 弱确认；
- 批量确认；
- 仅异常确认。

### 3. TDD 约束不如 Superpowers 硬

Harness 有 `test-driven-development` Skill，但流程上是 Phase 6 才正式测试。

当前职责划分是：

- Phase 4：编码实现，只做编译验证；
- Phase 6：单元测试。

这对于传统流程友好，但不是真正的 TDD。

Superpowers 的优势是强制 RED-GREEN-REFACTOR，能更有效抑制“先写实现、后补测试”的问题。

### 4. Skill 深度可能不如 Superpowers

从结构看，Harness 有 22 个 Skills，覆盖更广；Superpowers 的 Skills 数量少一些，但很多技能更像“强执行协议”，有更硬的行为约束。

Harness 当前部分 Skill 更像清单和流程说明，未来需要增强：

- 反模式识别；
- 必须停止条件；
- 错误示例；
- 自检表；
- 输出契约；
- 可机器检查字段。

### 5. 多平台适配较弱

Harness 当前明显以 Claude Code + 本地 `.harness/` 为中心。

优点是简单、可控、随项目版本化。

缺点是：

- 对 Cursor / Codex / Gemini CLI 等平台迁移不够直接；
- Slash command 体验不如 Superpowers；
- 插件生态分发能力弱。

---

## 五、Superpowers 的优点

### 1. 执行纪律强

Superpowers 的核心强项是 Iron Laws、verification-before-completion、TDD、two-stage review。

它更擅长约束 Agent 不要：

- 没验证就说完成；
- 跳过测试；
- 自我合理化；
- 修表象不修根因；
- 混淆 review 和 implementation。

Harness 已经吸收了部分思想，例如 verification-before-completion，但整体 TDD 执行强度仍弱于 Superpowers。

### 2. 灵活性更强

Superpowers 没有固定十阶段流程，更适合：

- 小任务；
- 快速迭代；
- 原型开发；
- 多语言项目；
- 个人项目；
- 非标准工程结构。

Harness 更适合“有流程、有门禁、有审计”的项目。

### 3. 子代理隔离更自然

Superpowers 强调 fresh context、subagent-driven development。

Harness 当前虽然定义了“隔离执行上下文”，但仍坚持唯一 Orchestrator。

这有利于统一决策，但也会带来一个问题：

> Orchestrator 上下文过长时，可能产生偏见、遗漏或污染。

Superpowers 的子代理隔离在审查、调试、并行任务上更有天然优势。

---

## 六、Superpowers 的缺点

### 1. 缺少 Harness 这样的项目级 Memory

Superpowers 没有原生等价于：

- `decisions.log`
- `lessons-learned.md`
- `known-issues.md`
- `wiki/`
- `changes/summary.md`

这意味着它更偏“当次执行质量”，而不是“项目长期记忆”。

### 2. 工程审计弱

Superpowers 可以写 plan、review、verification，但不强制每个阶段产物落盘，也不强制变更目录结构。

对企业团队来说，缺少：

- 谁确认了什么；
- 哪个阶段失败过；
- 为什么回退；
- 哪条决策影响了现在；
- 某个 bug 是否已有 lessons learned。

Harness 在这方面明显更强。

### 3. 技术栈深度不足

Superpowers 的技术栈无关是优点，也是缺点。

对 Java/Spring Boot 项目来说，Harness 可以沉淀：

- 分层架构规则；
- Controller/Service/Repository 边界；
- 事务规则；
- DTO 规则；
- 异常处理；
- 日志规范；
- JaCoCo 覆盖率门禁。

Superpowers 默认不会针对具体栈做这么深。

---

## 七、优化建议

### 建议 1：强化 Mini-flow / Lite-flow，让流程真正轻量化

当前已有流程分级，但建议进一步产品化：

```text
risk classifier → 自动建议 Standard / Lite / Mini
```

可以增加一份 `flow-selection.md`，用规则判断：

| 条件 | 推荐流程 |
|---|---|
| 纯文档、注释、typo | Mini |
| 单文件、无外部接口、无数据变更 | Lite |
| 涉及权限、安全、数据、接口、架构 | Standard |
| 需求不清晰 | Standard |
| 改动超过 N 个模块 | Standard |

重点是让 Orchestrator 不要默认把所有任务都拖进十阶段。

### 建议 2：减少低风险任务的人类确认次数

建议把 Human Approval Gate 分级：

| 类型 | 适用场景 | 行为 |
|---|---|---|
| mandatory | 高风险、架构、安全、数据、部署 | 必须停下确认 |
| batched | Lite-flow | 阶段组合后一次确认 |
| exception-only | Mini-flow | 仅失败或不确定时确认 |

例如 Mini-flow 可以变成：

```text
理解 → 修改 → 验证 → 总结确认
```

而不是每一步都要求确认。

### 建议 3：引入更硬的 TDD 策略

当前 Phase 6 才正式测试，建议按任务类型引入两种模式。

#### 对 bug fix

强制：

```text
先写失败测试 → 复现 bug → 修复 → 测试通过
```

#### 对新功能

至少要求：

```text
先定义验收测试或核心单元测试 → 再实现
```

可以在 `test-driven-development` Skill 中增加硬规则：

> 如果是 bug fix，没有失败测试或复现证据，不得进入实现修复。

这样可以吸收 Superpowers 最强的一点。

### 建议 4：增强 Skill 的“咬合力”

当前 Harness 的优势是覆盖广，下一步应该增强每个 Skill 的执行强度。

每个 Skill 建议统一增加：

```text
## When to use
## Inputs required
## Procedure
## Stop conditions
## Anti-patterns
## Required output schema
## Mechanical gate checks
## Examples
```

尤其是这些 Skill：

- `debugging-and-error-recovery`
- `test-driven-development`
- `code-review-and-quality`
- `security-and-hardening`
- `incremental-implementation`

应该加入更强的“不允许继续”的条件。

### 建议 5：给隔离执行上下文加标准输入包

Phase 5 已定义并行评审，但建议固化一个 review input package：

```text
.review-input/
├── diff.patch
├── spec.md
├── tasks.md
├── coding_report_v1.md
├── build.log
├── changed_files.txt
└── constraints.md
```

然后 code/security/performance 三个泳道只能基于这个包审查。

这样可以真正做到：

- 输入隔离；
- 审查可复现；
- 结论可对比；
- 避免审查上下文漂移。

### 建议 6：补足 Wiki，不要只保留模板

`.harness/wiki/` 是 Harness 的关键设计，但如果长期只是模板，价值会大幅下降。

建议至少补：

```text
wiki/project-overview.md
wiki/domain/{核心领域}.md
wiki/integration/{外部系统}.md
wiki/business-rules/{关键规则}.md
```

尤其是：

- 状态机；
- 权限规则；
- 金额/结算规则；
- 幂等规则；
- 外部接口 SLA；
- 数据一致性约束。

这是 Harness 能超越 Superpowers 的关键资产。

### 建议 7：把 Memory 从“记录”升级为“检索前置”

现在 Memory 主要是 Phase 出口记录。

建议增加一条强规则：

> Phase 1 和 Phase 4 开始前，必须检索 Memory 中是否存在相关 lessons、known issues、decisions。

也就是从：

```text
事后记录
```

升级为：

```text
事前检索 + 事后记录
```

否则 Memory 容易变成“写了但不用”的归档。

### 建议 8：建立 Harness 自身的质量评估指标

建议增加框架自身指标：

| 指标 | 说明 |
|---|---|
| Phase rollback rate | 哪些阶段最常回退 |
| Repeated lesson count | 同类错误是否重复发生 |
| Gate failure distribution | 哪类门禁最常失败 |
| Flow downgrade ratio | Mini/Lite/Standard 使用比例 |
| Verification freshness rate | 是否每次都有新鲜证据 |
| Human approval wait count | 用户确认摩擦度 |

这些指标可以帮助判断 Harness 是提高质量，还是只是增加流程负担。

---

## 八、最终建议路线

如果要继续优化当前 Harness，我建议路线是：

### 第一优先级：降摩擦

- 强化 Mini-flow / Lite-flow 自动选择；
- 减少低风险任务确认点；
- 明确哪些任务不需要完整十阶段。

### 第二优先级：增强执行纪律

- 对 bug fix 强制失败测试；
- 引入 Superpowers 式 anti-rationalization；
- 每个 Skill 增加 stop conditions；
- 把 verification-before-completion 作为所有流程出口硬门禁。

### 第三优先级：增强知识资产

- 填充 wiki；
- Memory 检索前置；
- 建立 repeated mistake 检查；
- 把 lessons learned 反馈到 rules 或 skills。

### 第四优先级：增强隔离审查

- 标准化 review input package；
- Phase 5 三泳道独立执行；
- 汇总时明确冲突处理规则。

---

## 九、总评

当前 Harness 的方向是对的，而且比普通 AI 编码提示词体系更接近真实工程框架。

它最强的是：

> 可审计、可恢复、可沉淀、可治理。

它最弱的是：

> 执行摩擦偏高、TDD 不够硬、Skill 执行约束不够锋利、轻量任务体验还需优化。

和 Superpowers 相比：

- 如果目标是 **个人高效编码、强 TDD、快速迭代**，Superpowers 更顺手。
- 如果目标是 **团队协作、企业级交付、长期项目治理、可审计 AI 编码流程**，Harness 更有潜力。

最理想的方向不是二选一，而是：

> 保留 Harness 的工程治理、Memory、Wiki、门禁和审计能力，同时吸收 Superpowers 的 TDD、fresh context、verification discipline 和强执行型 Skill 设计。
