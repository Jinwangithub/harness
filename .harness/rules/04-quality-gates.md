# 质量门禁定义

## 门禁通用规则

- 每个门禁必须是**可程序化验证**的
- "感觉没问题" = 不通过
- 必须提供证据（测试结果、日志、回包等）
- 事实判断优先于主观判断
- 每个 Phase 必须立即可验证，不允许合 Phase 检查

## 各阶段门禁

### Phase 1 门禁: 需求分析完成
```json
{
  "condition": "需求复述通过 && 边界明确 && 疑问点已识别",
  "evidence": [".harness/changes/{id}/request_analysis/understanding.md"],
  "validation": "必须询问用户「以上理解是否正确？」，用户回答通过后才可继续"
}
```

### Phase 2 门禁: 需求评审通过
```json
{
  "condition": "spec.md 评审通过 && tasks.md 尚未创建（Phase 3 职责）",
  "evidence": [".harness/changes/{id}/request_analysis/spec.md"],
  "validation": "必须询问用户「spec 是否确认？」，用户确认后才进入 Phase 3。最多3轮"
}
```

### Phase 3 门禁: 任务规划完成
```json
{
  "condition": "所有任务有验收条件 && 依赖关系明确 && 优先级已标注",
  "evidence": [".harness/changes/{id}/request_analysis/tasks.md"],
  "validation": "每个任务可独立验证"
}
```

### Phase 4 门禁: 编码完成
```json
{
  "condition": "编译通过 && 增量可回退 && 无语法错误",
  "evidence": [".harness/changes/{id}/coding/coding_report_v1.md", "build.log"],
  "validation": "mvn clean compile 状态 == SUCCESS"
}
```
**注意**: Phase 4 不运行测试，测试是 Phase 6 的职责。

### Phase 5 门禁: 编码评审通过
```json
{
  "condition": "五轴审查通过 && Critical=0 && Must Fix=0",
  "evidence": [
    ".harness/changes/{id}/coding/review/code_review_v1.md",
    ".harness/changes/{id}/coding/review/security_report_v1.md",
    ".harness/changes/{id}/coding/review/perf_report_v1.md"
  ],
  "validation": "所有Must Fix问题已解决，最多2轮"
}
```
**注意**: 评审角色加载自 `.harness/agents/code-reviewer.md`、`.harness/agents/security-auditor.md`、`.harness/agents/test-engineer.md`。

### Phase 6 门禁: 单元测试通过
```json
{
  "condition": "测试全部通过 && 覆盖率 >= 80% && JaCoCo 报告已生成",
  "evidence": [
    ".harness/changes/{id}/unit_test/test_report.md",
    "target/site/jacoco/index.html"
  ],
  "validation": "mvn test 状态 == SUCCESS && total_tests > 0 && passed == total && JaCoCo 行覆盖率 >= 80%"
}
```

### Phase 7 门禁: 测试评审通过
```json
{
  "condition": "测试评审通过",
  "evidence": [".harness/changes/{id}/unit_test/review/test_review_v1.md"],
  "validation": "所有Review意见已处理，最多2轮"
}
```
**注意**: 评审角色加载自 `.harness/agents/test-engineer.md`。

### Phase 8 门禁: CI 验证通过
```json
{
  "condition": "CI 全绿 && 性能不退化",
  "evidence": [".harness/changes/{id}/ci_result/ci_report.md"],
  "validation": "mvn verify 状态为 SUCCESS"
}
```

### Phase 9 门禁: 部署验证通过
```json
{
  "condition": "预发布环境验证通过 && 回滚就绪",
  "evidence": [".harness/changes/{id}/deployment/deploy_report.md"],
  "validation": "冒烟测试通过，JAR 构建成功"
}
```

## 质量门禁快速检查表

| 门禁 | 条件 | 证据 | 最大轮次 |
|------|------|------|---------|
| 需求分析 | 复述通过 | understanding.md | 1 |
| 需求评审 | 评审通过 | spec.md | 3 |
| 任务规划 | 可验证 | tasks.md | 1 |
| 编码 | 编译通过 | coding_report.md | 1 |
| 编码评审 | Must Fix=0 | 3 份评审报告 | 2 |
| 单元测试 | 覆盖率≥80% | test_report.md + JaCoCo | 1 |
| 测试评审 | 评审通过 | test_review.md | 2 |
| CI | 全绿 | ci_report.md | 1 |
| 部署验证 | 预发布通过 | deploy_report.md | 1 |
