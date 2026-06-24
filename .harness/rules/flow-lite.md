# Lite-flow 规范

> **TL;DR**: Lite-flow 用于可机械证明低风险的小变更，按 L1 需求确认+计划 → L2 实现 → L3 验证+交付执行；Lite 只降低阶段密度，不取消 Gate、证据、Memory、Stop-the-Line 或必要确认。

本文件是 Lite-flow 执行顺序与 Lite Step Cards 的权威源。
Flow 分类与路由见 `.harness/rules/flow.md`，Gate 判定见 `.harness/rules/gates.md`，失败处理和回退路径见 `.harness/rules/rollback.md`。

> **边界**：本文件只定义 Lite-flow 执行顺序、每个 Step 的入口卡片和 Lite 特有禁止事项。Gate 判定见 `gates.md`，产物结构见 `changes/structure.md`，Skill 文件路径约定见 `.harness/skills/README.md`。

## Lite-flow

适用：typo、注释、格式、纯文档、小配置、简单 bugfix、简单测试补充，且 `low_risk_proof` 可机械复核。

必需产物：`summary.md`（含 inline lite spec）、`request_analysis/checklist.md`、`wiki/candidates.md`、`verification_report.md`（含压缩评审）

执行顺序：

1. **L1** 需求确认+计划：写入 `summary.md`（含 inline lite spec）和 `checklist.md`；Mechanical Gate=`pass` 后请求用户确认；未确认前不得进入 L2。
2. **L2** 实现：按 checklist 驱动修改，无独立文件；风险扩大则 Stop-the-Line 并升级 Standard-flow。
3. **L3** 验证+交付：生成 `verification_report.md`（含压缩评审：Critical/Must Fix 计数、评审结论），包含 fresh evidence 和 Memory check；用户最终确认后标记 `已完成`。

## Lite Step Cards

### L1 — 需求确认+计划

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

### L2 — 实现

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

### L3 — 验证+交付

- 读取 Skills:
  - `code-review-and-quality`
  - `documentation-and-adrs`
  - `business-wiki-curation`
- 按条件补读 Skills:
  - 无
- 失败时补读 Skills:
  - `debugging-and-error-recovery`
- 禁止事项:
  - 不创建 Standard-only 产物
  - 未完成验证和 Memory check 前不得标记完成
- 产物提示:
  - `verification_report.md`（含压缩评审）
  - `wiki/candidates.md`
- Gate 提示:
  - Critical=0
  - Must Fix=0
  - Memory check 完成
  - Business Wiki candidate check complete
  - `wiki/candidates.md` exists
  - formal Wiki is updated only with human approval
  - deferred/rejected/no-candidate decisions are recorded
  - `INDEX.md` status 同步为 done
  - Fresh evidence 四字段完整
