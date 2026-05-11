---
name: auto-check-and-optimize
description: 代码写好后自动自检优化技能。每次完成代码编写任务后自动触发，调用 code-review-and-quality 进行五轴审查，调用 code-simplification 进行代码简化，执行 mvn compile 编译验证。专为 Java DDD 四层架构项目设计，额外检查分层架构合规性。Make sure to use this skill after every code implementation task - it is not optional.
---

# Auto Check and Optimize

## Overview

代码写好后自动触发的自检优化流程。作为编排层调用现有 skill，同时保留 Java DDD 项目的特色检查。

**核心价值**：
1. 调用 `code-review-and-quality` 进行五轴代码审查
2. 调用 `code-simplification` 进行代码简化
3. 执行 `mvn compile` 编译验证
4. **独有**：DDD 分层架构合规性检查

## When to Use

- **自动触发**：在每次完成代码编写任务后自动执行
- **手动调用**：用户说"自检"、"检查代码"时
- **提交前**：确保代码质量

**强制要求**：每次 Task 完成后必须执行此检查流程，不可跳过。

## Self-Check Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    Self-Check Flow                           │
└─────────────────────────────────────────────────────────────┘

    Task Complete
         │
         ▼
┌─────────────────────────┐
│ 1. Identify Changed     │
│    Files                │  ← git diff 识别修改的文件
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 2. Call: code-review   │  ← 调用 code-review-and-quality
│    and-quality Skill    │    进行五轴审查
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 3. Call: code-         │  ← 调用 code-simplification
│    simplification      │    进行代码简化
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 4. DDD Architecture     │  ← 独有：分层架构检查
│    Check               │    (见下方详细说明)
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 5. Compile Verify      │  ← mvn compile 编译验证
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 6. Generate Report     │  ← 输出 Markdown 报告
└─────────────────────────┘
```

## Step Detail

### Step 1: Identify Changed Files

```bash
git diff --name-only HEAD
git status --porcelain | grep "^??"
```

### Step 2: Call code-review-and-quality

**调用方式**：读取 `code-review-and-quality` skill 的内容并执行其流程。

**执行五轴审查**：
1. **Correctness** - 代码逻辑、边界情况、错误处理
2. **Readability** - 命名、控制流、代码组织
3. **Architecture** - 模块边界、依赖方向
4. **Security** - 输入验证、SQL注入、敏感信息
5. **Performance** - N+1查询、无界循环

### Step 3: Call code-simplification

**调用方式**：读取 `code-simplification` skill 的内容并执行。

**简化检查**：
- 深度嵌套（3+ 层）→ 提取守卫条件
- 长函数（50+ 行）→ 职责拆分
- 命名不清 → 描述性名称
- 冗余代码 → 提取公共函数

### Step 4: DDD Architecture Check（特色内容）

⚠️ **这是本 skill 相对于 code-review-and-quality 的独特价值**

对 Java DDD 四层架构项目，额外检查：

| 规则 | 检查点 | 检查方法 |
|------|--------|----------|
| domain 不依赖 infrastructure | domain/model 无数据库注解 | 搜索 `@TableId`、`@TableName`、`@Entity` |
| interfaces 不直接调 infrastructure | interfaces 只调用 domain/service | 检查 imports |
| Repository 接口在 domain 层 | domain/repository/*.java | 检查文件路径 |
| Client 接口在 domain 层 | domain/client/*.java | 检查文件路径 |
| 实现类在 infrastructure 层 | infrastructure/*/adapter/*.java | 检查文件路径 |
| domain/service 是唯一出口 | interfaces 层通过 service 接口访问 | 检查方法调用链 |

**违规示例**：
```java
// ❌ domain/model/Notice.java - 错误：使用了 MyBatis-Plus 注解
@TableName("t_notice")
public class Notice {
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;
}

// ❌ interfaces/controller/XxxController.java - 错误：直接调用 infrastructure
@Autowired
private NoticeMapper noticeMapper;  // 应该调用 domain/service
```

### Step 5: Compile Verify

```bash
cd /path/to/project
mvn compile -q

if [ $? -eq 0 ]; then
  echo "✅ 编译成功"
else
  echo "❌ 编译失败，输出错误："
  mvn compile 2>&1 | tail -30
fi
```

**失败处理**：修复错误 → 重新编译 → 直至通过

### Step 6: Generate Report

```markdown
# Auto Check Report - 2024-01-01 12:00:00

## Files Changed
- `domain/service/NoticeService.java`
- `domain/service/impl/NoticeServiceImpl.java`
- `infrastructure/repository/adapter/NoticeRepositoryAdapter.java`

## Code Review (by code-review-and-quality)
- ✅ Correctness: 通过
- ✅ Readability: 通过
- ⚠️ Architecture: 发现 1 处问题（已修复）
- ✅ Security: 通过
- ✅ Performance: 通过

## Simplification (by code-simplification)
- ✅ 无需简化

## DDD Architecture Check
- ✅ domain/model 无框架注解
- ✅ Repository 接口在 domain 层
- ✅ 实现类在 infrastructure 层
- ✅ 依赖方向正确

## Compile Status
```
[INFO] BUILD SUCCESS
```

## Verdict
**✅ PASS** - 代码通过所有检查
```

## Integration with Existing Skills

本 skill 是编排层，依赖以下 skill 的深度能力：

| 被调用的 Skill | 职责 | 本 skill 的作用 |
|---------------|------|----------------|
| code-review-and-quality | 五轴详细审查 | 调用执行 |
| code-simplification | 代码简化 | 调用执行 |
| incremental-implementation | 增量实现流程 | 参考其验证步骤 |

**不重复造轮子**：详细的审查规则和简化模式由对应 skill 定义，本 skill 负责串联和 DDD 特有检查。

## Verification Checklist

- [ ] 识别了所有修改的文件
- [ ] 执行了 code-review-and-quality 五轴审查
- [ ] 执行了 code-simplification 简化检查
- [ ] 执行了 DDD 架构检查
- [ ] 执行了 `mvn compile` 并通过
- [ ] 生成了 Markdown 报告

## Anti-Patterns (避免)

- ❌ 跳过自检直接进入下一个任务
- ❌ 编译失败时忽略错误
- ❌ DDD 架构违规不修复
