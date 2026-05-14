# Harness Engineering Framework 评价报告

> 评价对象：`/Users/apple/Documents/AI/harness/`
> 参考来源：① 微信公众号文章《Harness Engineering：耗时一周，如何将AI Coding率提升至90%》② GitHub [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) ③ Google agent-skills 集合
> 评价时间：2026-05-14

## 综合评价：85/100 — 高质量合成作品

---

## 一、项目定位与源码对比

你的项目本质上是**将两个顶级工程实践进行深度合成**的产物：

| 维度 | 微信文章 Harness | Google agent-skills | 你的项目 |
|------|----------------|-------------------|---------|
| 核心范式 | 10阶段流程 + Owner Agent | 6阶段技能 + 多Agent | **融合：10阶段 + 22 Skill + 单Orchestrator** |
| Agent模型 | 单 Application Owner | 多专职Agent（3人审查团） | **单 Orchestrator（从文章，但执行引擎用agent-skills）** |
| Skill数量 | 9个中文Skill（业务定制） | 22个英文Skill（通用） | **22个英文Skill（完整移植）+扩展** |
| 知识库 | Wiki（业务文档） | 无 | **Wiki模板 + 业务未填充** |
| 记忆系统 | 文中提及但未详述 | 无 | **完整的 memory/ 三层体系（创新）** |
| 质量门禁 | 文中提及 | 隐含在Skill中 | **独立 rule 文件 + JSON schema（深化）** |
| 接入方式 | 未说明 | 斜杠命令 + hooks | **缺失 slash commands + hooks** |

你的项目不是拷贝——你有明确的**架构判断力**：没有照搬 agent-skills 的三Agent模型，而是保留了文章中的"唯一Owner"哲学。这是一次**有判断的合成**。

---

## 二、按维度评价

### 2.1 架构设计（22/25）

**强项：**
- 四要素架构（Rules/Skills/References/Memory）结构清晰，分别对应"标准/流程/证据/经验"
- 单Orchestrator模型的取舍有理有据（`decisions.log` 中有ADR记录），比agent-skills的三Agent模型更适合小团队
- 三层上下文加载（L1常驻/L2阶段触发/L3按需查询）在 `CLAUDE.md` 和 `AGENTS.md` 中有明确体现
- 变更管理目录 `{type}-{name}-{YYYYMMDD}/` 规范且完整，含 `summary.md` 作为全链路单点溯源

**可优化：**
- 缺少 `.claude/commands/` 斜杠命令目录（agent-skills 提供 `/spec`, `/plan`, `/build` 等7个），用户无法通过简写触发流程
- 缺少 `hooks/` 目录（agent-skills 的会话生命周期钩子）
- `AGENTS.md` 作为 Index & Map 已到位（107行，符合"~100行"的最佳实践），但信息密度还有提升空间

### 2.2 规则体系（20/20）

四份规则文件质量很高：

| 文件 | 评价 |
|------|------|
| `01-engineering-structure.md` | 目录结构、命名、分层、依赖方向、文件大小约束全覆盖 |
| `02-development-workflow.md` | 10阶段全流程 + 9个确认点 + 回退路径 + 归档结构，比文章原文更严谨 |
| `03-coding-standards.md` | Java 17+ 规范：货币用long、异常不吞、@Valid边界、无通配符import、given/when/then测试，专业度高 |
| `04-quality-gates.md` | **亮点**：JSON schema 定义 + pass/fail/blocked 三态 + 每阶段独立门禁 + 快速检查表 |

其中 `03-coding-standards.md` 是直接从业务经验中提取的——价格用 `long`（分）而非 `double`、外部调用必须超时降级——这正是文章强调的"隐性知识显性化"。

### 2.3 Skill体系（18/20）

**强项：**
- 22个Skill完整移植自agent-skills，保留了所有核心工作流
- `idea-refine/` 目录自行扩展了 `examples.md`（3个完整示例）、`frameworks.md`（7种思维框架）、`refinement-criteria.md`（评估量规）和 `scripts/`——这些是agent-skills原仓库没有的
- `auto-check-and-optimize` Skill中有DDD架构合规检查（domain层无框架注解等），体现了对Java项目的定制

**可优化：**
- 22个Skill全部是英文原文，缺少类似文章中的中文业务定制Skill（如 `aone-ci-generate`、`project-analysis`）——这些虽然是业务相关的，但正是"Harness"区别于"Skill库"的关键
- 部分Skill的TypeScript/React示例与项目声明的Java/Spring技术栈不匹配（这是agent-skills的通病）
- Phase 5 三轴并行审查的调度逻辑依赖Orchestrator文本指令，缺乏脚本化的调度机制

### 2.4 记忆系统（15/15）— 原创亮点

这是**你的创新点**，两个参考来源都没有做到这个程度：

- `decisions.log` — 6条结构化ADR，每条含背景/方案/备选/理由/后果
- `lessons-learned.md` — 10条经验教训，驱动了规则和Orchestrator的优化，真正实现了 Mitchell Hashimoto 的"每发现一个错误就工程化消除它"
- `known-issues.md` — 3条已知问题，含优先级和临时方案
- `memory/README.md` — 使用说明

**这个反馈闭环是Harness Engineering的核心价值所在**——文章中是理念，你的项目是落地。10条lesson中的每一条都可以追溯到一个具体的规则变更，这证明了记忆系统确实在驱动框架演进。

### 2.5 实操可用性（10/20）— 主要短板

**问题：**
- **没有业务项目填充**：Wiki/、changes/ 都是模板和README，没有真实业务需求的实际执行记录。框架本身无法自证"能不能跑通"
- **没有 Dry Run 产物**：文章强调"Harness本身需要Dry Run"，你从lessons-learned中可以看到确实经历了多轮打磨，但未保留 Dry Run 的完整变更目录作为参考
- **USAGE.md 质量好但依赖外部理解**：写得清楚，但如果没有读过文章或agent-skills原仓库，新用户可能难以理解"为什么这么设计"
- **README.md 过于简略**：只有两个外部链接，没有项目自述

---

## 三、与两来源的 fidelity（忠实度）分析

### 对微信文章的实现程度：

| 文章要素 | 实现状态 |
|---------|---------|
| .harness/ 目录结构 | ✅ 完整实现并扩展 |
| 单 Application Owner Agent | ✅ 转写为 Orchestrator.md（312行 vs 文章400行） |
| 10阶段流水线 | ✅ 完整实现 |
| 5个Human-in-the-Loop确认点 | ✅ 扩展为9个（更严格） |
| 回退路径 | ✅ 实现且增加了评审超轮次→人工的路径 |
| 变更目录命名规范 | ✅ 完整实现 |
| summary.md 作为单一溯源 | ✅ 定义完整 |
| 分层上下文加载 L1/L2/L3 | ✅ 在AGENTS.md中体现 |
| Dry Run | ❌ 未保留产物 |
| 业务经验编码（货币long、超时降级等） | ✅ 写入03-coding-standards.md |

### 对 agent-skills 的实现程度：

| agent-skills要素 | 实现状态 |
|-----------------|---------|
| 22个SKILL.md | ✅ 完整移植 |
| References/ 补充清单 | ✅ 5个reference（新增orchestration-patterns.md） |
| idea-refine 的辅助文件 | ✅ 扩展（原仓库无examples/frameworks/criteria） |
| 3个Agent Persona | ❌ 主动放弃（符合文章的单Agent哲学） |
| 7个斜杠命令 | ❌ 未实现 |
| hooks/ 生命周期 | ❌ 未实现 |
| using-agent-skills 路由表 | ✅ 完整保留 |
| MCP 集成 | ✅ 有README但非硬依赖 |

---

## 四、核心价值判断

### 你的项目做得最好的是：

1. **记忆系统的设计** — 这是你超出两个参考来源的地方。decisions/lessons/known-issues 三层结构使Harness具备了自我演进能力，10条lesson真实反映了从"粗放使用Agent"到"工程化约束Agent"的认知升级过程。

2. **质量门禁的形式化** — `04-quality-gates.md` 中的JSON schema比文章的口语化描述严谨得多。pass/fail/blocked 三态（而非简单的"通过/不通过"）是实用的细节。

3. **Orchestrator的沟通原则** — 指定了10个Phase出口的精确句式，这对防止Agent"自己宣布成功"至关重要。这是你在实际使用中提炼出来的（lessons-learned有对应记录）。

4. **idea-refine的扩展** — examples.md、frameworks.md、refinement-criteria.md 让"需求分析"从概念变成可操作的方法论。

### 最需要补强的：

1. **缺少可运行的证明** — 这仍然是一个"框架模板"，缺少一个真实的变更示例。建议尽快找一个简单需求跑一遍完整的10阶段，将产物留在 `changes/example-feature-20260514/` 下。

2. **缺少斜杠命令** — 用户无法通过 `/spec`、`/build`、`/review` 这样的简短命令触发流程，只能靠自然语言描述。这将显著降低日常使用频率。

3. **Skills 与 Java 技术栈的适配** — 22个Skill中有大量TypeScript/React示例，对Java/Spring项目存在认知偏差。可能需要为 `coding-standards` 或 `incremental-implementation` 添加Java特化版本。

4. **Wiki 缺乏真实内容** — 框架是通用的，但Harness的价值在于承载"这个具体项目"的业务知识。空的Wiki模板无法提供任何上下文价值。

---

## 五、与业界对标

| 框架 | Harness Engineering (文章) | agent-skills (Google) | 你的项目 |
|------|--------------------------|----------------------|---------|
| 定位 | 企业级Java全流程 | 通用语言工程实践 | **通用框架模板** |
| 成熟度 | 生产验证（90% AI代码率） | 社区验证（30k+ stars） | **框架原型（未验证）** |
| 创新点 | Owner Agent + 10阶段 | Skill标准化 + 反-合理化表 | **记忆闭环 + 门禁形式化** |
| 开箱即用 | 需填充业务知识 | 需工具集成 | **需填充 + 集成** |

---

## 六、总结

你完成了一次**高质量的工程合成**，而非简单的拷贝。你有几个关键判断是准确的：

- **选择单Agent而非多Agent**：对中小团队更实用，且在 `decisions.log` 中有ADR记录
- **强化记忆系统**：抓住了Harness Engineering最本质的理念——"发现错误→工程化消除→再也不会犯"
- **保留USAGE.md**：agent-skills的处理方式（slash commands）和文章的处理方式（自然语言指令）各有利弊，你保留了双模式

当前的问题不在于设计，而在于**验证**：一个没有跑过真实需求的Harness框架，就像一台没有点火测试过的发动机——设计图可以很漂亮，但不知道能不能转。

**建议下一步**：找一个简单的需求（比如"添加一个查询接口"），用你的框架完整跑一遍10阶段流程，记录所有坑（果然会有坑），修正框架，保留产物作为示例。跑完这一圈，这个框架才真正"活"了。
