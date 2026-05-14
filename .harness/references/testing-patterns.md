# Testing Patterns

## JUnit 5 命名规范

- 测试类命名：`{ClassName}Test`。
- 测试方法命名建议：`should_{expectedBehavior}_when_{condition}` 或中文等价表达。
- 参数化测试命名应体现输入场景和期望结果。

## Arrange / Act / Assert

每个测试按三段组织：

```java
// Arrange: 构造输入、依赖和预期
// Act: 调用被测方法
// Assert: 断言结果和副作用
```

要求：
- Assert 阶段必须有明确断言。
- 单个测试只验证一个主要行为。
- 复杂输入应使用局部构造，不为一次性场景创建过度 helper。

## Mockito 使用规则

- 只 mock 外部依赖、网关、Repository、远程客户端等边界对象。
- 不 mock 被测类本身。
- 不 mock 值对象、DTO、简单实体。
- 使用 `verify` 检查关键副作用，避免验证无意义调用。
- 对未使用 stub 及时删除，避免测试噪声。

## 参数化测试

适用于：
- 多组等价输入验证同一行为。
- 边界值组合。
- 枚举状态转换。

JUnit 5 示例结构：

```java
@ParameterizedTest
@CsvSource({"0,false", "1,true"})
void should_returnExpectedResult_when_inputVaries(int input, boolean expected) {
    // Arrange / Act / Assert
}
```

## 边界值测试

至少覆盖：
- 空值 / 空集合 / 空字符串。
- 最小值 / 最大值。
- 阈值前后：`limit - 1`、`limit`、`limit + 1`。
- 重复元素、乱序输入、缺失字段。

## 异常测试

- 使用 `assertThrows` 验证异常类型。
- 对业务异常验证错误码或关键信息。
- 对外部依赖异常验证降级、回滚或错误传播行为。

## 反模式

- 无断言测试。
- 只测试 getter/setter。
- 过度 mock 导致没有真实行为被验证。
- 只验证方法被调用，不验证业务结果。
- 测试依赖执行顺序或共享全局状态。
- 为覆盖率编写无意义测试。

## Phase 6 测试报告字段要求

`test_report.md` 至少包含：

- 测试命令。
- 总测试数。
- 通过数 / 失败数 / 跳过数。
- 行覆盖率。
- 分支覆盖率。
- 覆盖率报告路径。
- 失败详情与修复状态。
- Mechanical Gate 状态：`pass|fail|blocked`。
