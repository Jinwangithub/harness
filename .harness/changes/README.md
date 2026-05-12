# 变更管理 — Audit Trail

## 目录结构

每个需求的变更归档在独立目录中：

```
.harness/changes/
└── {变更类型}-{需求名称}-{YYYYMMDD}/
    ├── summary.md                     # 全流程追溯摘要
    ├── request_analysis/
    │   ├── understanding.md           # Phase1: 需求理解笔记（idea-refine 产出）
    │   ├── spec.md                    # Phase2: 正式 PRD（spec-driven-development 产出）
    │   ├── tasks.md                   # Phase3: 任务拆分清单（planning-and-task-breakdown 产出）
    │   └── review/                    # 需求评审记录
    │       ├── review_v1.md
    │       └── review_v2.md           # 最多 3 轮
    ├── coding/
    │   ├── coding_report_v1.md        # Phase4: 编码报告（版本递增）
    │   └── review/
    │       ├── code_review_v1.md      # Phase5: 代码评审报告
    │       ├── security_report_v1.md  # Phase5: 安全审计报告
    │       └── perf_report_v1.md      # Phase5: 性能审查报告
    ├── unit_test/
    │   ├── test_report.md             # Phase6: 测试报告
    │   └── review/
    │       └── test_review_v1.md      # Phase7: 测试评审报告
    ├── ci_result/
    │   └── ci_report.md               # Phase8: CI 验证结果
    └── deployment/
        └── deploy_report.md           # Phase9: 部署验证报告
```

## 变更类型前缀

| 前缀 | 含义 |
|------|------|
| feat- | 新功能 |
| fix- | Bug 修复 |
| refactor- | 重构 |
| perf- | 性能优化 |
| test- | 测试 |
| docs- | 文档 |
| chore- | 工程维护 |

## summary.md 模板

```markdown
# 变更摘要

## 基本信息
- **需求**: {需求名称}
- **类型**: {feat/fix/refactor/...}
- **日期**: {YYYYMMDD}
- **状态**: {进行中/已完成/已回退}
- **负责人**: {orchestrator}

## 阶段进度
- [x] Phase 1: 需求分析 → {日期}
- [x] Phase 2: 需求评审 → {日期}
- [x] Phase 3: 任务规划 → {日期}
- [ ] Phase 4: 编码实现
- [ ] Phase 5: 编码评审
- [ ] Phase 6: 单元测试
- [ ] Phase 7: 测试评审
- [ ] Phase 8: CI验证
- [ ] Phase 9: 部署验证
- [ ] Phase 10: 用户确认

## 门禁状态
| Phase | Mechanical Gate | Evidence | Human Approval | Next/Rollback |
|-------|-----------------|----------|----------------|---------------|
| Phase 1 | pass/fail/blocked | request_analysis/understanding.md | pending-human/approved/rejected | P2/P1 |
| Phase 2 | pass/fail/blocked | request_analysis/spec.md | pending-human/approved/rejected | P3/P1 |
| Phase 3 | pass/fail/blocked | request_analysis/tasks.md | pending-human/approved/rejected | P4/P2 |
| Phase 4 | pass/fail/blocked | coding/coding_report_v1.md | pending-human/approved/rejected | P5/P4 |
| Phase 5 | pass/fail/blocked | coding/review/*.md | pending-human/approved/rejected | P6/P4 |
| Phase 6 | pass/fail/blocked | unit_test/test_report.md | pending-human/approved/rejected | P7/P6 |
| Phase 7 | pass/fail/blocked | unit_test/review/test_review_v1.md | pending-human/approved/rejected | P8/P6 |
| Phase 8 | pass/fail/blocked | ci_result/ci_report.md | pending-human/approved/rejected | P9/P6 |
| Phase 9 | pass/fail/blocked | deployment/deploy_report.md | pending-human/approved/rejected | P10/P8 |
| Phase 10 | pass/fail/blocked | delivery-summary.md | pending-human/approved/rejected | done/P9 |

## 回退记录
- {如果有回退，记录原因和时间}

## 最终交付物
- {产出的文件/功能清单}
```

## Phase 5 三份评审报告最小结构

`code_review_v1.md`、`security_report_v1.md`、`perf_report_v1.md` 均至少包含：

```markdown
# {Code Review / Security Report / Performance Report}

## Verdict
- Status: {Approve / Request Changes / Blocked}
- Critical: {0}
- Must Fix: {0}

## Scope
- Reviewed changes:
- Exclusions:

## Mechanical Checks
- [ ] Required files reviewed
- [ ] Relevant commands or static checks recorded
- [ ] Critical/Must Fix counts summarized

## Findings
| Severity | Area | Finding | Recommendation |
|----------|------|---------|----------------|

## Evidence
- Evidence paths:
- Command outputs:
- Logs/screenshots:

## Required Fixes
- {Required fixes before next Phase, or "None"}
```

## 归档规则

1. 每个 Phase 完成后立即归档对应产物
2. 产物标记版本号（如 review_v1 → review_v2）
3. 回退时记录 reason 到 summary.md
4. 变更完成后，summary.md 标记为"已完成"
5. 每个 Phase 的 Mechanical Gate 与 Human Approval Gate 状态必须记录到 summary.md
