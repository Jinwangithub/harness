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
    │   ├── tasks.md                   # Phase2: 任务拆分清单
    │   └── review/                    # 需求评审记录
    │       ├── review_v1.md
    │       └── review_v2.md           # 最多 3 轮
    ├── coding/
    │   ├── coding_report_v1.md        # 编码报告（版本递增）
    │   └── review/
    │       └── code_review_v1.md      # 代码评审报告
    ├── unit_test/
    │   ├── test_report.md             # 测试报告
    │   └── review/
    │       └── test_review_v1.md      # 测试评审报告
    ├── ci_result/
    │   └── ci_report.md               # CI 验证结果
    └── deployment/
        └── deploy_report.md           # 部署验证报告
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

## 回退记录
- {如果有回退，记录原因和时间}

## 最终交付物
- {产出的文件/功能清单}
```

## 归档规则

1. 每个 Phase 完成后立即归档对应产物
2. 产物标记版本号（如 review_v1 → review_v2）
3. 回退时记录 reason 到 summary.md
4. 变更完成后，summary.md 标记为"已完成"
