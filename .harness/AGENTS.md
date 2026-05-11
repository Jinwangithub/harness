# AGENTS.md — Harness Engineering 导航地图

> 地图而非手册。此处仅做索引，具体内容在对应文件中。

## 项目信息

- **技术栈**: Java 17 / Spring Boot 3.x (参考规则)
- **架构风格**: 分层架构 (Controller → Service → Domain)
- **工程框架**: Harness Engineering + agent-skills

## 快速链接

| 资源 | 路径 | 说明 |
|------|------|------|
| 工程结构规则 | `.harness/rules/01-engineering-structure.md` | 目录、命名、分层 |
| 开发流程规范 | `.harness/rules/02-development-workflow.md` | 十阶段流程、门禁 |
| 编码规范 | `.harness/rules/03-coding-standards.md` | 代码风格、约束 |
| 质量门禁 | `.harness/rules/04-quality-gates.md` | 通过/回退条件 |
| Orchestrator | `.harness/agents/orchestrator.md` | 唯一的 Agent（编排中枢） |
| Skills 索引 | `.harness/skills/README.md` | 20 个 agent-skills 映射表 |

## 十阶段工作流速查

```
Phase 1:  需求分析   → idea-refine               产出: understanding.md
Phase 2:  需求评审   → spec-driven-development    产出: spec.md（不含 tasks.md）
Phase 3:  任务规划   → planning-and-task-breakdown 产出: tasks.md（首次创建）
Phase 4:  编码实现   → incremental-implementation  产出: 源码（编译验证，不做测试）
Phase 5:  编码评审   → 3 Skill 并行(code-review/security/perf)  产出: 三份评审报告
Phase 6:  单元测试   → test-driven-development     产出: 测试报告 + 覆盖率报告(JaCoCo)
Phase 7:  测试评审   → code-review-and-quality     产出: 测试评审报告
Phase 8:  CI验证     → ci-cd-and-automation        产出: CI报告
Phase 9:  部署验证   → shipping-and-launch          产出: 部署报告
Phase 10: 用户确认   → 人工                        产出: 最终确认
```

## 变更目录命名规范

每次变更归档到 `.harness/changes/{变更类型}-{需求名称}-{YYYYMMDD}/`：

| 前缀 | 含义 | 示例 |
|------|------|------|
| feat- | 新功能 | `feat-skill-executor-20260507/` |
| fix- | Bug 修复 | `fix-npe-order-20260507/` |
| refactor- | 重构 | `refactor-payment-20260507/` |
| perf- | 性能优化 | `perf-query-20260507/` |
| test- | 测试 | `test-coverage-20260507/` |
| docs- | 文档 | `docs-api-20260507/` |
| chore- | 工程维护 | `chore-upgrade-20260507/` |

## 回退规则

| 失败类型 | 回退到 |
|---------|-------|
| CI 失败 | Phase 6: 修复测试 |
| 编译错误 | Phase 4: 修复编码 |
| 需求不符 | Phase 1: 重新分析 |
| 评审超轮次 | 升级到人工决策 |

## 构建命令

```bash
# Maven 项目
mvn clean compile             # 编译
mvn test                      # 运行测试
mvn clean package -DskipTests # 打包
mvn verify                    # 完整验证（含集成测试）
mvn jacoco:report             # 生成覆盖率报告

# Gradle 项目
./gradlew build               # 构建
./gradlew test                # 运行测试
./gradlew check               # 代码质量检查
```

## 分层规则

```
controller/    → @RestController/@Controller, 接收转发 (Layer 4)
service/       → @Service, 业务逻辑 (Layer 3)
repository/    → @Repository, 数据访问 (Layer 2)
domain/dto/    → 领域模型/DTO (Layer 1)
util/          → 工具类 (Layer 0)
config/        → 配置类 (与 domain 同级)
exception/     → 异常定义 (与 domain 同级)

依赖方向: controller → service → repository
                      ↓
            config / domain / dto / exception / util
```

## 硬性约束

- 绝不跳过任何开发阶段
- Orchestrator 绝不自己写代码，只分派
- 每次变更必须归档到 `.harness/changes/{type}-{name}-{YYYYMMDD}/`
- 每个 Phase 完成后必须立即归档对应产物到变更目录
- 所有决策记录写入 `.harness/memory/decisions.log`
- 外部服务调用必须设置超时和降级
- 金额字段用 `long`(分), 禁用 `double/float`
- 每发现一个错误, 写入 `lessons-learned.md` 防止再犯
