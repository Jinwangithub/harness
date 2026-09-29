# Technical Data and Operations Categories

选择 technical/data、technical/infrastructure、technical/operations 或 technical/standards 时读取本参考。
### 6.7 technical/data

**核心问题**

数据是什么、由谁拥有、在哪里、如何关联、流转、缓存、演化和保持一致？

**收录范围**

- 逻辑和物理数据模型、表和实体关系；
- 字段语义、主键、索引和约束；
- 数据归属、来源、去向和读写责任；
- 数据生命周期、状态、保留和删除语义；
- DB、MQ、ES、对象存储等之间的数据流转；
- 一致性、事务、同步、补偿和重放语义；
- 缓存的数据模型、Key 语义、TTL 的业务或一致性含义；
- 数据迁移、版本演化和兼容性。

**排除范围**

- Redis、MySQL、Kafka 集群如何安装、部署和配置，进入 technical/infrastructure；
- 数据库连接池耗尽、主从延迟告警和故障恢复，进入 technical/operations；
- 业务对象纯概念定义，进入 business/domain；
- 业务事件的端到端步骤，进入 business/processes；
- DAO、Repository、序列化类的实现细节，进入 technical/modules。

**判断规则**

满足以下条件时选择本分类：

1. Primary question 是“数据如何表达、存储、关联、移动或保证正确”；
2. 即使更换实现代码，数据语义和一致性问题仍需被理解；
3. 文章关注存储内容与数据行为，而不是承载它的集群或事故处理。

文章应优先包含：数据定义、所有者、来源、存储、关系、生命周期、读写路径、一致性策略、缓存语义、迁移约束和敏感性说明。

**典型文章**

- 订单与订单明细数据模型
- 预测记录与评估结果关系
- 订单数据从 DB 到 MQ 再到 ES 的流转
- 交易结果最终一致性
- Redis 中订单状态的缓存模型

**相邻分类区别**

- 与 infrastructure：data 回答 Redis 存什么以及如何保持正确；infrastructure 回答 Redis 集群怎样提供运行能力。
- 与 operations：data 描述正常的数据语义和一致性；operations 处理异常现象、诊断、恢复和验证。
- 与 domain：data 是技术表达；domain 是不依赖存储实现的业务含义。

### 6.8 technical/infrastructure

**核心问题**

系统依赖什么环境、网络、中间件和基础设施才能运行，这些依赖如何部署、配置和接入？

**收录范围**

- MySQL、Redis、Kafka、MQ、Nacos、ES、对象存储等基础设施依赖；
- 环境划分、部署环境和环境差异；
- 集群拓扑、网络、域名、专线和连通性要求；
- Topic、集群、命名空间、资源配额等基础设施配置；
- 配置来源、连接要求、容量规划和基础依赖版本；
- 基础设施高可用和备份能力的具体部署约束；
- 生产值以外的安全配置说明和占位符语义。

**排除范围**

- 中间件承载的业务数据模型，进入 technical/data；
- 中间件故障的排查、恢复和值班步骤，进入 technical/operations；
- 系统整体组件关系和系统级技术选择，进入 technical/architecture；
- 代码如何使用客户端和连接池，进入 technical/modules；
- 密码、token、真实生产账号、地址或其他可用于访问系统的敏感值。

**判断规则**

满足以下条件时选择本分类：

1. Primary question 是“系统需要哪些运行依赖、如何提供和配置这些依赖”；
2. 重点是正常运行前的环境能力和接入条件；
3. 文章不是在解释存储内容，也不是在处理已经发生的故障。

文章应优先包含：依赖用途、环境范围、拓扑、版本、配置来源、连接方式、容量和可用性要求、环境差异、安全注意事项和相关运维链接。

**典型文章**

- Redis 集群部署与连接要求
- MySQL 集群和读写节点
- Kafka Topic 基础设施配置
- 生产环境外部依赖
- 网络与专线依赖

**相邻分类区别**

- 与 data：infrastructure 描述承载平台；data 描述平台上存放的数据及正确性。
- 与 operations：infrastructure 描述正常运行基线；operations 描述运行后的观察、变更、故障和恢复。
- 与 architecture：infrastructure 给出实际环境和资源；architecture 给出系统边界、关系和系统级设计。

### 6.9 technical/operations

**核心问题**

系统运行过程中如何发布、监控、告警、执行日常任务、定位故障、恢复服务并验证结果？

**收录范围**

- 监控指标、日志观察点、告警和 SLO 运行视角；
- 发布、灰度、回滚和变更验证；
- 定时任务和日常运维动作；
- 故障现象、影响、排查路径和定位方法；
- 恢复、补偿、重放、应急处理和验证；
- Runbook、值班手册和已发生事故的可复用处置经验；
- 常见问题及其已经验证的解决方式。

**排除范围**

- 完整业务实现和内部算法，进入 technical/modules；
- 正常状态下的数据模型和一致性设计，进入 technical/data；
- 集群首次部署、环境和连接基线，进入 technical/infrastructure；
- 业务是否允许执行的规则，进入 business/rules；
- 没有项目证据支撑的通用排障清单。

**判断规则**

满足以下条件时选择本分类：

1. Primary question 是“运行中如何观察、操作，出问题如何恢复”；
2. 文章包含可执行的观察点、判断、动作和验证；
3. 场景发生在系统已部署运行之后。

故障和 Runbook 文章应优先包含：现象、影响、前置安全检查、排查路径、定位信号、恢复动作、回滚条件、验证方式和升级路径。

**典型文章**

- 数据库连接池耗尽排查
- 服务 CPU 飙高排查
- Kafka 消息堆积处理
- 应用发布与回滚
- 定时评估任务运行手册

**相邻分类区别**

- 与 infrastructure：operations 管理或修复正在运行的基础设施；infrastructure 定义正常部署和接入基线。
- 与 data：operations 处理数据异常和恢复操作；data 定义正常模型、流转和一致性语义。
- 与 modules：operations 面向值班和运行任务；modules 面向代码修改和扩展。

### 6.10 technical/standards

**核心问题**

项目或团队已经确认统一采用什么工程规则，适用于哪些范围，如何判断是否遵守？

**收录范围**

- 已确认的 API 设计规范；
- 日志、异常、测试、编码和命名规范；
- 工程目录、依赖管理和配置约定；
- Code Review、兼容性和版本管理约定；
- 有正式文档、配置、模板、自动化规则或一致代码事实支持的团队标准；
- 标准的适用范围、例外和检查方法。

**排除范围**

- AI 通用经验、行业最佳实践或个人偏好；
- 仅在单个模块中出现一次、无法证明是统一约定的实现方式；
- 某个具体 API 的实际契约，进入 technical/interfaces；
- 某个模块的内部实现，进入 technical/modules；
- 架构决策或基础设施事实本身，除非证据明确把它确认为统一工程规范。

**判断规则**

只有同时满足以下条件时选择本分类：

1. Primary question 是“团队统一应该怎么做”；
2. 存在项目确认依据，例如规范文档、ADR、构建规则、lint 配置、代码模板、评审约定或多处一致实践；
3. 能说明适用范围、约束强度和例外；
4. 不能仅凭 AI 认为“这样更好”。

证据不足时标记 Inference 或 Open question，并优先放回更具体的 ordinary technical 文章；不得把推测提升为项目标准。

文章应优先包含：规则、适用范围、确认依据、强制性、正例、反例、例外、自动检查方式和迁移说明。

**典型文章**

- HTTP API 错误响应规范
- 项目日志字段规范
- Java 异常处理约定
- 单元测试与集成测试边界
- Code Review 必查项

**相邻分类区别**

- 与 interfaces：standards 规定所有接口应该怎样设计；interfaces 描述一个真实接口怎样使用。
- 与 modules：standards 是跨模块约定；modules 是具体模块事实。
- 与 ordinary technical knowledge：只有已被项目确认并具有适用范围的约束才是 standard；事实、选择或经验本身不是标准。

