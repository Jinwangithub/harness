# 开发流程规范

> **TL;DR**: 收到需求 → Flow Classifier 分类（Lite/Standard）→ 按所选 Flow 路由到对应执行规范 → 每个 Phase/Step 出口过 Gate → 失败按回退路径处理。

本文件是 Flow Classifier 与 Flow 路由索引的权威源。
门禁检查表见 `.harness/rules/gates.md`，Lite-flow 执行见 `.harness/rules/flow-lite.md`，Standard-flow 执行见 `.harness/rules/flow-standard.md`，失败处理和回退路径见 `.harness/rules/rollback.md`，Memory 模板见 `.harness/memory/README.md`。

> **边界**：本文件只定义 Flow 分类、路由索引和 Phase/Step 入口卡片字段定义。Lite Step Cards 见 `flow-lite.md`，Standard Phase Cards 和 Phase 4 隔离原则见 `flow-standard.md`，回退路径见 `rollback.md`，Gate 判定见 `gates.md`，产物结构见 `changes/structure.md`，Skill 文件路径约定见 `.harness/skills/README.md`；本文件不定义 Skill role 或加载类型术语。

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

## Flow 路由索引

分类完成后，按 `summary.md` 中的 `flow` 读取对应执行规范：

| Flow | 读取文件 | 用途 |
|------|----------|------|
| `Lite-flow` | `.harness/rules/flow-lite.md` | Lite-flow 执行顺序、L1/L2/L3 Step Cards |
| `Standard-flow` | `.harness/rules/flow-standard.md` | Standard-flow Phase 1-10、Phase Cards、Phase 4 隔离原则 |
| `fail` / `blocked` / 风险扩大 / 需要回退 | `.harness/rules/rollback.md` | Stop-the-Line、failure evidence、根因、恢复点、重验证、回退路径 |

Gate 判定始终读取 `.harness/rules/gates.md`。

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
