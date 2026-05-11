# Java 编码规范

## 通用规则

### 代码质量
- 遵循 "Rule of 500": 单文件不超过 500 行
- 方法不超过 50 行，一个方法只做一件事
- 类内字段不超过 15 个，超过考虑拆分
- 三个相似的代码片段比一个过早的抽象好
- 不要为假设的未来需求而构建

### 命名规范
| 类型 | 规范 | 示例 | 说明 |
|------|------|------|------|
| 类名 | PascalCase | `OrderService`, `UserController` | 名词/名词短语 |
| 接口 | PascalCase | `UserRepository`, `Serializable` | 形容词或名词 |
| 抽象类 | PascalCase + Abstract前缀 | `AbstractBaseService` | 表明抽象性质 |
| 方法 | camelCase | `findUserById()`, `saveOrder()` | 动词/动词短语 |
| 变量 | camelCase | `userName`, `orderList` | 名词 |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` | `static final` |
| 枚举 | PascalCase(类) + UPPER_SNAKE_CASE(值) | `OrderStatus.PENDING` | — |
| 包名 | 全小写 | `com.company.module.service` | 禁止下划线 |
| 泛型参数 | 单大写字母 | `<T>`, `<K,V>`, `<R extends Comparable>` | — |
- 禁止无上下文的名字: `temp`, `data`, `result`, `list`, `map`
- 布尔方法用 `is`/`has`/`can`/`should` 前缀: `isActive()`, `hasPermission()`

### 源文件组织（顺序）

```java
// 1. 版权声明（可选）
// 2. package 语句
package com.example.module.service;

// 3. import 语句（禁止通配符 import *）
import com.example.module.dto.OrderDTO;
import com.example.module.repository.OrderRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

// 4. 类/接口定义
@Slf4j
@Service
@RequiredArgsConstructor
public class OrderService {

    // 5. 静态变量: static final
    private static final int MAX_RETRY_COUNT = 3;

    // 6. 实例变量
    private final OrderRepository orderRepository;

    // 7. 构造方法（Lombok 可省略）
    // 8. 静态工厂方法
    // 9. 公共方法
    // 10. 私有方法
    // 11. getter/setter（Lombok @Data / @Getter / @Setter）
    // 12. equals/hashCode/toString（Lombok @EqualsAndHashCode / @ToString）
}
```

## Java 版本约束

- 项目最低 Java 版本: 按项目实际定义（推荐 Java 17+）
- 使用 `var` 仅在局部变量且类型从右侧显见时（禁止 `var` 用于返回值和参数）
- 优先使用 `record`（Java 16+）定义不可变数据传输对象
- 优先使用 `sealed class/interface`（Java 17+）限制继承

```java
// 推荐: 使用 record 定义 DTO
public record OrderDTO(String orderId, Long amount, OrderStatus status) {}

// 不推荐: 手写 getter/setter/toString 的 POJO
public class OrderDTO {
    private String orderId;
    private Long amount;
    // ... 大量样板代码
}
```

## 代码风格

### 格式
- 缩进: 4 空格（禁止 Tab）
- 左大括号: 同行（Egyptian brackets）
- 行宽: 120 字符
- 空行: 方法间 1 空行；逻辑块间可加空行分隔

```java
// 正确
@Service
public class OrderService {

    public OrderDTO findOrderById(String orderId) {
        if (orderId == null) {
            throw new IllegalArgumentException("orderId must not be null");
        }
        return orderRepository.findById(orderId)
                .map(this::toDTO)
                .orElseThrow(() -> new OrderNotFoundException(orderId));
    }
}

// 错误: 左大括号换行
public class OrderService
{
    public OrderDTO findOrderById(String orderId)
    {
        ...
    }
}
```

### 注解
- 注解在单独一行，与被注解元素之间有换行
- Spring 注解按顺序: `@Service/@Controller/@Repository` → `@RequiredArgsConstructor` → `@Slf4j`

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class OrderService {
    ...
}
```

### 枚举

```java
public enum OrderStatus {
    PENDING("待支付"),
    PAID("已支付"),
    SHIPPED("已发货"),
    COMPLETED("已完成"),
    CANCELLED("已取消");

    private final String description;

    OrderStatus(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }
}
```

## 异常处理

### 原则
- 优先使用自定义业务异常而非通用 `RuntimeException`
- 不要吞异常：`catch` 块必须处理、重新抛出或记录日志
- 异常分级: `BizException`(业务) → `SystemException`(系统) → `RemoteException`(外部)

```java
// 推荐
public class BizException extends RuntimeException {
    private final String errorCode;
    private final String message;

    public BizException(String errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }

    public String getErrorCode() {
        return errorCode;
    }
}

// 使用
if (order.getAmount() <= 0) {
    throw new BizException("INVALID_AMOUNT", "订单金额必须大于0");
}
```

### 禁止的模式
```java
// ❌ 吞异常
try {
    orderRepository.save(order);
} catch (Exception e) {
    // 什么也不做
}

// ❌ catch 了却继续抛 RuntimeException
try {
    orderRepository.save(order);
} catch (Exception e) {
    throw new RuntimeException("保存失败");
}

// ❌ 用异常控制流程
try {
    orderRepository.findById(orderId);
} catch (OrderNotFoundException e) {
    // 正常流程
}
```

## 安全约束
- 所有用户输入必须在 Controller 边界验证（`@Valid` / `@Validated`）
- 密钥/密码不得出现在代码、日志和版本控制中（使用环境变量或配置中心）
- 使用 `PreparedStatement` / 参数化查询，禁止字符串拼接 SQL
- 外部 API 数据视为不可信，必须在 Service 边界验证
- 外部服务调用必须设置超时和降级策略
- 敏感数据禁止 `System.out.println` 或 SLF4J 日志

```java
// 推荐: 参数化查询
@Query("SELECT o FROM Order o WHERE o.orderId = :orderId")
Optional<Order> findByOrderId(@Param("orderId") String orderId);

// ❌ 危险: 字符串拼接
@Query("SELECT o FROM Order o WHERE o.orderId = '" + orderId + "'")
```

## 金额与数值约束
- 金额字段用 `long` 类型（单位为分），禁止 `double/float`
- 提供工具方法在分和元之间转换

```java
public final class MoneyUtils {
    private MoneyUtils() {}

    public static long yuanToFen(BigDecimal yuan) {
        return yuan.multiply(new BigDecimal("100")).longValue();
    }

    public static BigDecimal fenToYuan(long fen) {
        return BigDecimal.valueOf(fen, 2);
    }
}
```

## 分层架构约束（Spring Boot 项目）

| 层 | 注解 | 职责 | 禁止 |
|----|------|------|------|
| Controller | `@RestController` / `@Controller` | 接收请求、参数校验、返回响应 | 不包含业务逻辑 |
| Service | `@Service` | 业务逻辑编排、事务管理 | 不直接操作数据库 |
| Repository/DAO | `@Repository` / `@Mapper` | 数据访问、ORM 映射 | 不包含业务逻辑 |
| Domain/Model | 无 | 核心领域模型、业务规则 | 不依赖框架注解 |

### 依赖方向
```
Controller → Service → Repository
                ↓
            Domain/Model
```

**禁止**: Service 依赖 Controller、循环依赖、双向依赖

### 分层代码示例

```java
// Controller 层: 只做接收和转发
@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;

    @GetMapping("/{orderId}")
    public ResponseEntity<OrderDTO> getOrder(@PathVariable String orderId) {
        return ResponseEntity.ok(orderService.findOrderById(orderId));
    }
}

// Service 层: 业务逻辑
@Service
@RequiredArgsConstructor
@Transactional
public class OrderService {

    private final OrderRepository orderRepository;

    public OrderDTO findOrderById(String orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException(orderId));
        return OrderAssembler.toDTO(order);
    }
}

// Repository 层: 数据访问
@Repository
public interface OrderRepository extends JpaRepository<Order, String> {
    List<Order> findByUserIdAndStatus(String userId, OrderStatus status);
}
```

## 测试规范（JUnit 5 + Mockito）

- 测试类命名: `{被测类名}Test`（如 `OrderServiceTest`）
- 测试方法命名: `{方法名}_{场景}_{期望结果}`（如 `findOrderById_当订单不存在时_抛出异常`）
- 使用测试金字塔: Unit 80% / Integration 15% / E2E 5%

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @InjectMocks
    private OrderService orderService;

    @Test
    void findOrderById_当订单存在时_返回订单DTO() {
        // given
        String orderId = "ORD-001";
        Order order = new Order(orderId, 1000L, OrderStatus.PAID);
        when(orderRepository.findById(orderId)).thenReturn(Optional.of(order));

        // when
        OrderDTO result = orderService.findOrderById(orderId);

        // then
        assertThat(result.orderId()).isEqualTo(orderId);
        assertThat(result.amount()).isEqualTo(1000L);
    }

    @Test
    void findOrderById_当订单不存在时_抛出异常() {
        // given
        String orderId = "NONEXIST";
        when(orderRepository.findById(orderId)).thenReturn(Optional.empty());

        // when & then
        assertThrows(OrderNotFoundException.class,
                () -> orderService.findOrderById(orderId));
    }
}
```

## 日志规范

- 使用 SLF4J + Logback（禁止 `System.out.println` 和 `System.err.println`）
- 配合 Lombok `@Slf4j` 注解

```java
@Slf4j
@Service
public class OrderService {

    public OrderDTO createOrder(CreateOrderRequest request) {
        log.info("开始创建订单, userId={}, amount={}", request.userId(), request.amount());

        try {
            Order order = orderRepository.save(buildOrder(request));
            log.info("订单创建成功, orderId={}", order.getOrderId());
            return OrderAssembler.toDTO(order);
        } catch (Exception e) {
            log.error("订单创建失败, userId={}, amount={}", request.userId(), request.amount(), e);
            throw new BizException("CREATE_ORDER_FAILED", "创建订单失败");
        }
    }
}
```

## 工具库规范

### 推荐工具
| 用途 | 推荐库 | 说明 |
|------|--------|------|
| 简化代码 | Lombok | `@Data`, `@Builder`, `@Slf4j` |
| 集合工具 | Apache Commons / Guava | `Lists`, `Maps`, `Strings` |
| JSON | Jackson | Spring Boot 默认 |
| 参数校验 | Jakarta Validation | `@Valid`, `@NotBlank`, `@Size` |
| 对象映射 | MapStruct | 编译期生成，性能优于 BeanUtils |

### Lombok 使用规范
```java
// 推荐组合
@Data                          // = @Getter + @Setter + @ToString + @EqualsAndHashCode
@Builder                       // Builder 模式
@NoArgsConstructor             // 无参构造
@AllArgsConstructor             // 全参构造
public class CreateOrderRequest {
    @NotBlank
    private String userId;

    @NotNull
    @Min(1)
    private Long amount;
}

// Service 层注入
@Service
@RequiredArgsConstructor       // final 字段的构造器注入
@Slf4j                         // log 对象
public class OrderService { ... }
```

## Maven/Gradle 规范
- 使用 dependency management 统一版本管理（`<dependencyManagement>` 或 BOM）
- 禁止在子模块写死版本号
- 定期更新依赖版本（mvn versions:display-dependency-updates）
- 禁止使用 SNAPSHOT 依赖（除非明确需要）
- 插件的版本也在 `<pluginManagement>` 中统一管理
