# 工程结构规则

## 目录组织

### Maven 项目（推荐）

```
项目根目录/
├── pom.xml                    # Maven 构建文件
├── src/
│   ├── main/
│   │   ├── java/              # Java 源代码
│   │   │   └── com/example/module/
│   │   │       ├── controller/     # Controller 层 (Layer 4)
│   │   │       ├── service/        # Service 层 (Layer 3)
│   │   │       ├── repository/     # Repository/DAO 层 (Layer 2)
│   │   │       ├── domain/         # 领域模型 (Layer 1)
│   │   │       ├── dto/            # 数据传输对象 (Layer 1)
│   │   │       ├── config/         # 配置类 (Layer 2)
│   │   │       ├── common/         # 公共工具/异常 (Layer 1)
│   │   │       └── util/           # 工具类 (Layer 0)
│   │   └── resources/               # 资源文件
│   │       ├── application.yml
│   │       ├── application-dev.yml
│   │       ├── mapper/             # MyBatis Mapper XML
│   │       └── db/migration/       # Flyway 迁移脚本
│   └── test/
│       └── java/                   # 测试代码
│           └── com/example/module/
│               ├── controller/
│               ├── service/
│               └── repository/
├── docs/                      # 文档
│   ├── ARCHITECTURE.md        # 架构总览
│   └── design-docs/           # 设计文档
├── scripts/                   # 构建/工具脚本
├── Dockerfile                 # 容器化
└── .harness/                  # Harness Engineering 工程目录
    ├── AGENTS.md              # Agent 导航地图
    ├── agents/                # Agent 角色定义
    ├── rules/                 # 规则体系
    ├── skills/                # 技能体系
    ├── changes/               # 变更管理
    ├── memory/                # 持久化记忆
    ├── wiki/                  # 项目知识库
    └── references/            # 参考清单
```

### Gradle 项目（备选）

```
项目根目录/
├── build.gradle               # Gradle 构建文件
├── settings.gradle
├── src/
│   ├── main/java/             # 同 Maven 结构
│   ├── main/resources/
│   ├── test/java/
│   └── test/resources/
├── ...
└── .harness/
```

### 多模块 Maven 项目

```
项目根目录/
├── pom.xml                    # 父 POM
├── module-common/             # 公共模块（工具类、DTO）
│   ├── pom.xml
│   └── src/main/java/...
├── module-domain/             # 领域模块（实体、领域服务）
│   ├── pom.xml
│   └── src/main/java/...
├── module-repository/         # 数据访问模块
│   ├── pom.xml
│   └── src/main/java/...
├── module-service/            # 业务服务模块
│   ├── pom.xml
│   └── src/main/java/...
├── module-web/                # Web 接口模块（Controller）
│   ├── pom.xml
│   └── src/main/java/...
└── .harness/
```

## 命名规范

| 类型 | 规范 | 示例 | 说明 |
|------|------|------|------|
| Java 类 | PascalCase | `OrderService`, `UserController` | 名词 |
| 接口 | PascalCase | `OrderRepository` | 名词/形容词 |
| 抽象类 | PascalCase + Abstract前缀 | `AbstractBaseService` | — |
| 方法 | camelCase | `findById()`, `createOrder()` | 动词 |
| 变量 | camelCase | `orderId`, `userName` | — |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` | `static final` |
| 枚举 | PascalCase(类型) + UPPER_SNAKE_CASE(值) | `OrderStatus.PENDING` | — |
| 包名 | 全小写 | `com.example.module.service` | 禁止下划线/大写 |
| 测试类 | {类名}Test | `OrderServiceTest` | JUnit 5 约定 |
| 资源文件 | kebab-case | `application-dev.yml` | — |
| XML Mapper | {接口名}.xml | `OrderMapper.xml` | MyBatis 约定 |

## 分层架构映射

| 层 | 对应目录 | Spring 注解 | 功能角色 |
|----|---------|------------|---------|
| Layer 4 — 接口层 | `controller/` | `@RestController` | 请求接收、参数校验、响应返回 |
| Layer 3 — 业务层 | `service/` | `@Service` | 业务逻辑编排、事务管理 |
| Layer 2 — 数据层 | `repository/` | `@Repository` / `@Mapper` | 数据访问、ORM 映射 |
| Layer 1 — 领域层 | `domain/`, `dto/`, `common/` | 无框架注解 | 领域模型、DTO、公共异常 |
| Layer 0 — 工具层 | `util/` | 无 | 纯工具类，无内部依赖 |

### 依赖方向
```
Layer 4 (controller) → Layer 3 (service) → Layer 2 (repository)
                               ↓
                    Layer 1 (domain/dto/common)
                               ↓
                    Layer 0 (util)
```
**禁止**: Service 依赖 Controller、循环依赖、双向依赖、下层反向依赖上层

## 文件大小约束
- 单 Java 文件不超过 500 行
- 超过 300 行考虑拆分
- 方法不超过 50 行，一个方法只做一件事
- Controller 方法不超过 20 行（只负责转发）
- 类内字段不超过 15 个，超过考虑拆分
