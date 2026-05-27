# 质量门禁定义

本文件是 Mechanical Gate、Human Approval Gate、机械验证证据类型、Phase Gate 检查和失败门禁的权威源。流程选择和检查时机见 `.harness/rules/02-development-workflow.md`。

## 1. 通用规则

- 每个 Phase 或 Flow step 必须先执行 Mechanical Gate，再按 `confirmation_policy` 执行 Human Approval Gate。
- Mechanical Gate 必须严格机械判定：命令退出码、文件存在、确定性搜索、计数阈值、结构化字段、报告中的明确 `pass/fail/blocked`。
- 人工偏好、感觉、未定义标准的“审查通过”不能作为 Mechanical Gate。
- Human Approval Gate 只能在 Mechanical Gate 为 `pass` 后进入。
- Mechanical Gate 为 `fail|blocked` 时必须 Stop-the-Line，不得请求用户人工放行。
- 出口必须列出 fresh verification evidence：命令、结果、报告路径、审查报告路径或可复查的检查结果。
- Completion Claim Gate：summary 必填字段完整、final evidence 存在、Memory check 完成、Human Approval Gate 为 `approved` 或规则明确允许；否则不得声明完成、通过或交付。
- Lite-flow、Standard-flow 都必须具备 Mechanical Gate、fresh verification evidence、Memory check 和必要 Human Approval Gate。

## 2. Gate 状态定义

### Mechanical Gate

| 状态 | 含义 | 下一步 |
|------|------|--------|
| `pass` | 证据完整且机械判定通过 | 按 `confirmation_policy` 进入 Human Approval Gate 或继续 |
| `fail` | 证据存在但机械判定失败 | Stop-the-Line，回退修复 |
| `blocked` | 证据缺失、命令无法执行、环境不满足或无法机械判定 | Stop-the-Line，补证据或处理阻塞 |

### Human Approval Gate

只允许以下 canonical 状态：

| 状态 | 含义 |
|------|------|
| `pending-human` | Mechanical Gate 已通过，等待用户确认 |
| `approved` | 用户确认通过 |
| `rejected` | 用户不通过，必须回退处理 |
| `not-required-by-policy` | 当前 `confirmation_policy` 明确不要求此处确认，且 Mechanical Gate 已通过 |

非 canonical Human Approval 状态一律视为 Gate `blocked`。`not-required-by-policy` 不能代替 mandatory Phase approval 或 Lite L1/L4 approval。

## 3. Mechanical Evidence Types

| Evidence Type | 机械判定方式 | 示例 |
|---------------|--------------|------|
| Command | 命令退出码、stdout/stderr 中确定字段 | build/lint/test 命令 exit code 0 |
| File artifact | 文件或目录存在，路径确定，必要字段存在 | `summary.md`、`coding_report_v1.md` 存在 |
| Search/consistency check | 确定性搜索结果、匹配数、禁止词为 0 | 禁止提前创建文件、关键词一致性搜索 |
| Review report | 报告存在且结构化 verdict 明确，Critical/Must Fix 计数可判定 | `Critical=0`、`Must Fix=0` |
| Coverage/test | 测试命令、测试数、覆盖率阈值可判定 | tests passed、coverage >= threshold |
| Skill load | Required Skill Load Record 存在且 Status 可判定 | Required skill `loaded` 或 Gate `blocked` |
| Phase lock | Entry/Exit/Human/Failure Lock 状态字段可判定 | Entry Lock=`open`、Failure Lock=`closed` |
| Executable Harness validation | `harness-validate.sh` 输出 PASS/WARN/FAIL 和退出码 | `.harness/scripts/harness-validate.sh` |

## 3.1 Executable Gate Validation

`.harness/scripts/harness-validate.sh` 是 Harness 治理仓库的低复杂度 Mechanical Gate evidence source。

规则：

1. validator 只输出 `PASS` / `WARN` / `FAIL`，不得自动修改文件。
2. 仅 `FAIL` 返回非 0；legacy summary 不一致优先输出 `WARN`，新 summary 违反 canonical 状态或废弃字段输出 `FAIL`。
3. validator 可检查必需文件、`INDEX.md` 存在性、active auto-resume 唯一性、多个进行中 summary、canonical Human Approval 状态、deprecated `resume_from`、脚本自身可执行等确定性条件。
4. validator 不替代 Orchestrator Gate 判断；Orchestrator 必须结合 Flow、Phase artifact、fresh evidence、Memory 和 Human Approval Gate 做最终门禁记录。
5. 新 summary 中出现非 canonical Human Approval 状态时，对应 Mechanical Gate 必须为 `blocked`，不得请求人工放行。

## 4. Confirmation Policy

| Policy | 默认 Flow | Human Approval Gate 时机 | 不可绕过项 |
|--------|-----------|--------------------------|------------|
| `mandatory` | Standard-flow | CK1-CK9 按 Phase 请求确认 | Mechanical Gate、fresh evidence、Memory check、Stop-the-Line、Phase Lock |
| `batched` | Lite-flow | 需求+简化计划一次；最终验证/评审摘要一次 | Mechanical Gate fail/blocked、证据缺失、Memory 缺失 |

## 5. Flow-level 快速检查表

| Flow | Mechanical Gate 必查 | Evidence | Review | Memory | Human Approval |
|------|----------------------|----------|--------|--------|----------------|
| Lite-flow | lite spec 存在；checklist 存在且完成/延期明确；验证报告存在；评审摘要存在；Critical=0；Must Fix=0 | `summary.md`、`request_analysis/lite_spec.md`、`request_analysis/checklist.md`、`verification_report.md`、`review_summary.md` | 压缩版 Two-stage Review | 计划确认后、最终验证/交付前检查 | batched |
| Standard-flow | 对应 Phase 产物存在并符合 `.harness/changes/README.md` 对应模板结构；前置 Phase Lock 满足；Required Skill Load Record 存在；本 Phase 判定条件满足；fresh evidence 列出 | 对应 Phase 报告、命令结果、Skill Load Record、Phase Lock Record | Phase 4 自检 + Phase 5 独立评审 | 每个 Phase 出口检查 | mandatory |

## 6. Lite-flow L1-L4 Gate 表

| Step | Mechanical Gate 必查 | Fresh Evidence | Memory | Human Approval |
|------|----------------------|----------------|--------|----------------|
| L1 需求确认+简化计划 | `summary.md`、`lite_spec.md`、`checklist.md` 存在；Flow Classification 有 `low_risk_proof`；无 Standard 强制升级风险；Skill trigger evaluation 已记录 | artifact 路径、低风险证据、结构检查 | 计划确认后检查；触发即记录 | batched approval 必须 `approved` 后进入 L2 |
| L2 实现 | 只修改 checklist 允许范围；未创建 Standard-only 产物；未引入风险扩大 | 变更范围、文件清单、禁止文件搜索结果 | 如触发治理/教训/限制则立即记录 | `not-required-by-policy` 仅在 L1 已 approved 且无风险扩大时可用 |
| L3 验证/压缩评审 | `verification_report.md`、`review_summary.md` 存在；Critical=0；Must Fix=0；fresh evidence 当前有效；Memory check 完成 | 命令/搜索结果、报告路径、评审结论 | 最终验证/交付前检查；触发即记录 | `not-required-by-policy` 仅表示等待 L4 final approval 前无需中间确认 |
| L4 交付确认 | Completion Claim Gate 通过；summary completeness checklist 完成；Completion lock 可解锁 | final evidence、summary、approval evidence | Memory status 完整 | final approval 必须 `approved`，否则不得标记已完成 |

## 7. Standard Phase-level 快速检查表

每个 Standard Phase 都必须检查：

- Required Skill Load Record 存在，且 Required Skill 的 `Status` 为 `loaded` 或明确 `blocked`。
- Conditional Skill 触发但未加载时，Mechanical Gate 必须为 `blocked`。
- 前置 Phase Lock 状态符合 `.harness/rules/02-development-workflow.md`。
- 当前 Phase 没有执行 Forbidden/Deferred 动作。
- fresh verification evidence 为当前阶段新鲜证据。
- Memory check 完成。

| Phase | Mechanical Gate 必查 | Evidence | Human Approval |
|------|----------------------|----------|----------------|
| Phase 1 需求分析 | `understanding.md` 存在，包含需求复述、边界、疑问点；禁止提前创建 `spec.md`/`tasks.md`；Memory check 完成 | `request_analysis/understanding.md`、禁止文件搜索结果 | CK1 |
| Phase 2 需求评审 | `spec.md` 存在；禁止创建 `tasks.md`；Memory check 完成 | `request_analysis/spec.md`、禁止文件搜索结果 | CK2 |
| Phase 3 任务规划 | `tasks.md` 存在，每个任务有验收条件且可独立验证；禁止实现代码；Memory check 完成 | `request_analysis/tasks.md`、变更范围检查 | CK3 |
| Phase 4 编码实现 | 隔离执行证据存在；编译成功；`coding_report_v1.md` 存在；Author/Self Review 完成；未冒充 Phase 5/6；Memory check 完成 | 隔离上下文记录、编译命令结果、`coding/coding_report_v1.md`、Author/Self Review | CK4 |
| Phase 5 编码评审 | 独立评审报告存在，隔离审查完成，Critical=0，Must Fix=0，Memory check 完成 | `coding/review/*.md`、评审摘要 | CK5 |
| Phase 6 单元测试 | 测试通过，测试数>0，覆盖率符合项目阈值，Memory check 完成 | 测试命令结果、`unit_test/test_report.md`、覆盖率报告 | CK6 |
| Phase 7 测试评审 | 测试评审报告存在，Must Fix=0，Memory check 完成 | `unit_test/review/test_review_v1.md` | CK7 |
| Phase 8 CI 验证 | CI 报告存在且成功，Memory check 完成 | `ci_result/ci_report.md` | 按 Standard 规则确认或记录自动放行依据 |
| Phase 9 部署验证 | 部署报告存在，冒烟/回滚检查完成，Memory check 完成 | `deployment/deploy_report.md` | CK8 |
| Phase 10 用户确认 | delivery summary 存在，summary 状态更新，Memory 完整性验证完成 | `delivery-summary.md`、`summary.md`、Memory 记录 | CK9 |

## 7. Phase 4 Gate 附加要求

Phase 4 Mechanical Gate 必须机械验证以下内容：

- 隔离执行证据：不可变输入包、受限任务说明、子上下文输出或变更摘要存在。
- 编译证据：编译命令、退出码和结果存在。
- Author/Self Review：`auto-check-and-optimize` 作为 Phase 4 自检记录存在。
- 未冒充 Phase 5：不能把 Author/Self Review 记作 Independent Review。
- 未冒充 Phase 6：不能把编译验证记作单元测试/覆盖率验证。

缺少任一项时 Mechanical Gate=`blocked`。

## 8. Failure gate 检查

任一 Mechanical Gate 为 `fail|blocked` 时，门禁记录必须包含：

- `failure_evidence`：失败命令、日志、报告路径、缺失条件或阻塞原因。
- `root_cause`：已定位根因；未定位时保持 `blocked`，不得进入 Human Approval Gate。
- `rollback_target`：回退到的 Phase 或 Flow step。
- `regression_verification`：修复后的 fresh verification evidence。
- `memory_action`：是否写入 `lessons-learned.md` / `known-issues.md` / `decisions.log`；如无则说明 `none`。

## 9. Canonical Markdown Gate Record 模板

```markdown
## Gate Record — {Step/Phase}

- Mechanical Gate: {pass/fail/blocked}
- Checks:
  - [ ] {mechanical check item}
  - [ ] {artifact exists / forbidden artifact absent / status canonical / counts pass}
- Fresh verification evidence:
  - {command + exit code, search result, report path, review path}
- Skill Load Record:
  - Required: {loaded/blocked/not-required-by-policy + evidence}
  - Conditional trigger evaluation: {triggered/not-triggered + evidence}
- Memory Check:
  - Status: {completed/pending/blocked}
  - Memory recorded: {N} entries / none
  - Evidence: {memory path or none}
- Human Approval Gate: {pending-human/approved/rejected/not-required-by-policy}
- Approval evidence: {user confirmation record or policy reason}
- Rollback target: {Phase/Step or none}
```

## 10. Completion Claim Gate

声明完成、通过、交付，或把 `summary.md` 状态改为 `已完成` 前，必须全部满足：

1. `summary.md` 必填字段完整：Flow Classification、Current step、Resume point、Gate、Skill Load Records、Memory status、Completion lock。
2. final fresh evidence 存在且可复查。
3. Memory check 完成；触发项已按完整模板记录。
4. Human Approval Gate 为 `approved`，或当前点被规则明确允许 `not-required-by-policy`。
5. Mechanical Gate 无 `fail|blocked`。
6. Human Approval Gate 状态为 canonical 值。

任一不满足时 Completion Claim Gate=`blocked`，不得声明完成/通过/交付。
