# Skills 索引 — agent-skills 映射表

本目录映射 agent-skills 插件的 20 个 Skill 到 Harness Engineering 十阶段工作流。

每个 Skill 的文件位于以下路径：
`~/.claude/plugins/cache/addy-agent-skills/agent-skills/1.0.0/skills/{name}/SKILL.md`

## 01-Define (需求定义)

| Phase | Skill | 源路径 | 使用时机 |
|-------|-------|--------|---------|
| P1: 需求分析 | idea-refine | `skills/idea-refine/SKILL.md` | 需求模糊时，用发散/收敛思维澄清。产出 understanding.md |
| P2: 需求评审 | spec-driven-development | `skills/spec-driven-development/SKILL.md` | 编写 PRD（spec.md）。不含 tasks.md |

## 02-Plan (任务规划)

| Phase | Skill | 源路径 | 使用时机 |
|-------|-------|--------|---------|
| P3: 任务规划 | planning-and-task-breakdown | `skills/planning-and-task-breakdown/SKILL.md` | 拆解 task，标注依赖和验收条件。首次创建 tasks.md |

## 03-Build (编码实现)

| Phase | Skill | 源路径 | 使用时机 |
|-------|-------|--------|---------|
| P4: 编码实现 | incremental-implementation | `skills/incremental-implementation/SKILL.md` | 按垂直切片增量实现。仅编译验证 |
| P4: 编码实现 | context-engineering | `skills/context-engineering/SKILL.md` | 启动 Session/切换任务时加载上下文 |
| P4: 编码实现 | source-driven-development | `skills/source-driven-development/SKILL.md` | 使用新框架/库时参考官方文档 |
| P4: 编码实现 | frontend-ui-engineering | `skills/frontend-ui-engineering/SKILL.md` | 构建 UI 组件 |
| P4: 编码实现 | api-and-interface-design | `skills/api-and-interface-design/SKILL.md` | 设计 API/模块边界 |

## 04-Verify (验证)

| Phase | Skill | 源路径 | 使用时机 |
|-------|-------|--------|---------|
| P6: 单元测试 | test-driven-development | `skills/test-driven-development/SKILL.md` | 编写/补全测试 + JaCoCo 覆盖率报告 |
| 跨阶段 | debugging-and-error-recovery | `skills/debugging-and-error-recovery/SKILL.md` | 构建/测试失败时 |
| 跨阶段 | browser-testing-with-devtools | `skills/browser-testing-with-devtools/SKILL.md` | 浏览器端调试 |

## 05-Review (审查)

| Phase | Skill | 源路径 | 使用时机 |
|-------|-------|--------|---------|
| P5: 编码评审 | code-review-and-quality | `skills/code-review-and-quality/SKILL.md` | 五轴代码审查（正确性/可读性/架构/安全/性能） |
| P5: 编码评审 | security-and-hardening | `skills/security-and-hardening/SKILL.md` | 安全审计（OWASP Top 10） |
| P5: 编码评审 | performance-optimization | `skills/performance-optimization/SKILL.md` | 性能审查 |
| P5: 编码评审 | code-simplification | `skills/code-simplification/SKILL.md` | 简化复杂代码 |
| P7: 测试评审 | code-review-and-quality | `skills/code-review-and-quality/SKILL.md` | 使用其测试审查标准评估测试质量 |

## 06-Ship (交付)

| Phase | Skill | 源路径 | 使用时机 |
|-------|-------|--------|---------|
| P8: CI验证 | ci-cd-and-automation | `skills/ci-cd-and-automation/SKILL.md` | CI 流水线设置 |
| P8: CI验证 | git-workflow-and-versioning | `skills/git-workflow-and-versioning/SKILL.md` | 提交/版本管理 |
| P9: 部署验证 | shipping-and-launch | `skills/shipping-and-launch/SKILL.md` | 预发布/投产检查 |
| P10: 交付 | documentation-and-adrs | `skills/documentation-and-adrs/SKILL.md` | 架构决策记录 |
| P10: 交付 | deprecation-and-migration | `skills/deprecation-and-migration/SKILL.md` | 废弃/迁移旧代码 |

## 使用方式

在 Claude Code 中通过 Skill tool 直接调用：
```
Skill name: spec-driven-development
Skill name: incremental-implementation
Skill name: code-review-and-quality
```

或通过 slash commands:
```
/spec → /plan → /build → /review → /test → /ship
```

## 重要提醒

| Phase | 常见误区 | 纠正 |
|-------|---------|------|
| P1 | 产出 spec.md | 产出 understanding.md，不做详细设计 |
| P2 | 产出 tasks.md | 只产 spec.md，tasks.md 是 P3 的职责 |
| P3 | 覆盖 tasks.md | 首次创建 tasks.md（P2 不产 tasks.md） |
| P4 | 运行 mvn test | 只做 mvn clean compile，测试是 P6 的职责 |
| P5 | 使用 agents/ 角色文件 | 直接使用 agent-skills 插件的 Skill，无独立 Agent |
| P6 | 不检查覆盖率 | 必须运行 JaCoCo 并产出覆盖率报告 |
