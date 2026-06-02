# 质量门禁定义

> **TL;DR**: 每个 Phase 出口先过 Mechanical Gate → 通过后请求用户确认。Gate 状态: pass/fail/blocked。Evidence 四字段（Command/Exit code/Output summary/Artifact path）任一为空 → blocked。Human Approval pending 时 Completion lock 必须 locked。

本文件是 Mechanical Gate、Human Approval Gate 和 Phase Gate 检查表的权威源。
Iron Laws 见 `.harness/agents/orchestrator.md`。

## 1. 通用规则

- 每个 Phase 或 Flow step 先执行 Mechanical Gate，通过后请求用户确认。
- Mechanical Gate 必须严格机械判定：命令退出码、文件存在、确定性搜索、计数阈值。
- 人工偏好、感觉、未定义标准的"审查通过"不能作为 Mechanical Gate。

## 2. Gate 状态

### Mechanical Gate

| 状态 | 含义 | 下一步 |
|------|------|--------|
| `pass` | 证据完整且机械判定通过 | 请求用户确认 |
| `fail` | 证据存在但判定失败 | Stop-the-Line，回退修复 |
| `blocked` | 证据缺失或无法机械判定 | Stop-the-Line，补证据 |

### Human Approval Gate

| 状态 | 含义 |
|------|------|
| `approved` | 用户确认通过，可进入下一 Phase |
| `rejected` | 用户不通过，回退处理 |
| `pending` | 等待用户确认（`Completion lock` 必须保持 `locked`） |

**硬约束**：`Human Approval = pending` 时 `Completion lock` 必须为 `locked`。`pending` + `已完成` = 冲突，不得声明完成。

## 3. Gate Record 模板

```markdown
## Gate Record — {Phase/Step}

- Mechanical Gate: {pass/fail/blocked}
- Checks:
  - [ ] {artifact exists / forbidden artifact absent / counts pass}
- Fresh verification evidence:
  - Command: {完整命令，不得为空}
  - Exit code: {数字，不得为空}
  - Output summary: {关键行，不得只写"成功"/"已完成"}
  - Artifact path: {文件路径，不得为空}
- Skill Load: {Skill 名} = {loaded / blocked + 原因}
- Memory: {N entries / none}
- Human Approval: {approved / rejected / pending}
```

**硬约束**：
- Fresh evidence 任意字段为空 → Mechanical Gate 自动 `blocked`。
- `Human Approval = pending` 且声明 `已完成` → Mechanical Gate 自动 `fail`。
- 出口报告缺少上述模板任一字段 → Mechanical Gate 自动 `blocked`。

## 4. Lite-flow Gate 表

| Step | Mechanical Gate 必查 | Fresh Evidence | Human Approval |
|------|----------------------|----------------|----------------|
| L1 需求确认+计划 | `summary.md`（含 inline lite spec）、`checklist.md` 存在；`INDEX.md` 标记为 active；有 `low_risk_proof`；无强制升级风险 | Command / Exit code / Output summary / Artifact path | 用户确认后进入 L2 |
| L2 实现 | 只修改 checklist 范围；未创建 Standard-only 产物；未引入风险扩大 | Command / Exit code / Output summary / Artifact path | 无需单独确认 |
| L3 验证+交付 | `verification_report.md`（含压缩评审）存在；Critical=0；Must Fix=0；Memory check 完成；`INDEX.md` status 同步为 done | Command / Exit code / Output summary / Artifact path | 用户最终确认后标记已完成 |

## 5. Standard Phase Gate 检查表

每个 Standard Phase 出口必须逐项填写：

```
Phase N Exit Checklist:
[ ] 本 Phase 产物文件已存在（文件名 + 路径）          yes/no
[ ] Required Skill 已加载（Skill 名 + loaded/blocked）  yes/no
[ ] Fresh evidence：Command + Exit code + Output + Artifact path  yes/no
[ ] Memory checkpoint 已填写                             yes/no
[ ] Mechanical Gate 状态已填写（pass/fail/blocked）     yes/no
```

**任意项为 no → Mechanical Gate=`blocked`，不得进入下一 Phase。**

| Phase | Mechanical Gate 必查 | Evidence | 确认点 |
|-------|----------------------|----------|--------|
| 1 | `understanding.md` 存在；禁止提前创建 `spec.md`/`tasks.md`（Forbidden 约束见 `.harness/skills/matrix.md`） | `request_analysis/understanding.md` | CK1 |
| 2 | `spec.md` 存在；禁止创建 `tasks.md` | `request_analysis/spec.md` | CK2 |
| 3 | `tasks.md` 存在，每个任务有验收条件；禁止实现代码 | `request_analysis/tasks.md` | CK3 |
| 4 | 隔离执行证据存在；编译成功；`coding_report_v1.md` 存在；Author/Self Review 完成 | 编译命令结果、`coding/coding_report_v1.md` | CK4 |
| 5 | 独立评审报告存在；Critical=0；Must Fix=0 | `coding/review/*.md` | CK5 |
| 6 | 测试通过；测试数 > 0；覆盖率符合项目阈值 | 测试命令结果、`unit_test/test_report.md` | CK6 |
| 7 | 测试评审报告存在；Must Fix=0 | `unit_test/review/test_review_v1.md` | CK7 |
| 8 | CI 报告存在且成功 | `ci_result/ci_report.md` | CK8 |
| 9 | 部署报告存在；冒烟/回滚检查完成 | `deployment/deploy_report.md` | CK9 |
| 10 | delivery summary 存在；Memory 完整；`INDEX.md` status 同步为 done | `delivery-summary.md` | CK10 |

## 6. Phase 4 附加要求

- 隔离执行证据：不可变输入包、子上下文输出或变更摘要存在。
- 编译证据：编译命令、退出码和结果存在。
- Author/Self Review 记录存在，不能记作 Independent Review（Phase 5）或测试（Phase 6）。

缺少任一项 → Mechanical Gate=`blocked`。

## 7. Failure Gate 记录

Mechanical Gate=`fail|blocked` 时，记录必须包含：

- 失败证据：失败命令、日志或缺失条件。
- 根因：已定位；未定位则保持 `blocked`。
- 回退目标：回退到的 Phase 或 Flow step（同步更新 `summary.md` 和 `INDEX.md`）。
- 修复验证：修复后的 fresh evidence。
- Memory 动作：写入了哪个 memory 文件，或 `none`。

## 8. 声明完成的条件

声明完成或标记 `已完成` 前，必须全部满足：

1. 所有产物存在且可复查。
2. final fresh evidence 存在。
3. Memory check 完成。
4. 用户已确认（`Human Approval = approved`）。
5. Mechanical Gate 无 `fail|blocked`。
6. `INDEX.md` status 已同步为 `done`。
