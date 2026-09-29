# Technical System Categories

选择 technical/architecture、technical/modules 或 technical/interfaces 时读取本参考。
### 6.4 technical/architecture

**核心问题**

系统由什么组成，边界在哪里，各组件、服务和上下游之间是什么关系，为什么采用这些系统级选择？

**收录范围**

- 系统上下文、系统边界和责任边界；
- 服务、组件和子系统关系；
- 上游、下游、同步与异步调用关系；
- 系统级调用链和关键依赖方向；
- 部署拓扑、高可用、容灾和多活架构；
- 系统级技术选择、架构约束和质量属性；
- 跨模块数据流概览，但不展开数据结构细节。

**排除范围**

- 请求字段、响应结构、错误码和调用限制，进入 technical/interfaces；
- Java 类、方法、包和模块内部实现，进入 technical/modules；
- 表、索引、缓存数据结构和一致性细节，进入 technical/data；
- Redis、MySQL、Kafka 的具体集群配置，进入 technical/infrastructure；
- 告警、发布、排障和恢复步骤，进入 technical/operations。

**判断规则**

满足以下条件时选择本分类：

1. Primary question 是“系统整体由哪些部分组成、边界和关系是什么”；
2. 结论跨越多个代码模块或部署单元；
3. 文章关注结构与依赖方向，而不是某个调用者的使用契约或某个模块的内部算法。

文章应优先包含：系统上下文、边界、组件职责摘要、关系图、关键链路、架构约束、质量属性、系统级决策和相关详细文章链接。

**典型文章**

- 交易平台系统上下文与边界
- 订单域服务组件关系
- 同步交易与异步评估架构
- 多可用区高可用架构
- 灾备切换与数据恢复总体架构

**相邻分类区别**

- 与 modules：architecture 看系统级组成和跨模块关系；modules 看一个代码模块的内部职责和实现。
- 与 interfaces：architecture 解释谁调用谁以及为什么；interfaces 解释调用方具体怎样调用。
- 与 infrastructure：architecture 可描述部署拓扑和系统级容灾；infrastructure 记录实际环境、中间件、网络和配置依赖。

### 6.5 technical/modules

**核心问题**

某个代码模块负责什么，代码在哪里，内部如何协作、实现和扩展？

**收录范围**

- 稳定代码模块的职责和边界；
- 仓库相对位置、核心包、类、方法和入口；
- 模块内部协作、执行流和依赖；
- 核心算法、重要实现策略和技术行为；
- 扩展点、插件点、策略实现和可替换组件；
- 模块输入输出的内部语义，但不复制对外契约；
- 对 AI Coding 有用的修改位置、影响面和测试定位。

**排除范围**

- 整个系统的服务边界和组件拓扑，进入 technical/architecture；
- 外部调用方可见的协议、字段、错误和版本，进入 technical/interfaces；
- 数据表、索引、数据生命周期和一致性，进入 technical/data；
- 完整业务流程和业务规则正文，进入 business/processes 或 business/rules；
- 每个类一篇、逐文件说明或无稳定职责的工具类清单。

**判断规则**

满足以下条件时选择本分类：

1. Primary question 是“修改或扩展这个代码能力时，需要理解哪些职责和实现”；
2. 文章范围能对应一个稳定模块或内聚能力，而不是单个偶然类；
3. 代码位置、内部协作和实现逻辑是文章核心。

文章应优先包含：模块职责、边界、代码位置、入口、内部流程、依赖、关键实现、扩展点、失败行为和相关测试。

**典型文章**

- 交易处理模块
- 基金筛选模块
- 风险检查模块
- 异步评估模块
- 模型路由模块

**相邻分类区别**

- 与 architecture：modules 深入一个实现单元；architecture 连接多个系统级单元。
- 与 interfaces：modules 面向维护者解释内部实现；interfaces 面向调用者解释稳定契约。
- 与 data：modules 可说明读写动作；data 负责数据结构、归属、流转和一致性本身。

### 6.6 technical/interfaces

**核心问题**

系统边界外的调用方如何调用能力，并正确理解输入、输出、错误、超时、幂等、版本和兼容性？

**收录范围**

- HTTP API、RPC、MQ/Event、Webhook 和 CLI 契约；
- 调用者、用途、协议和入口；
- 请求参数、响应结构和字段语义；
- 错误语义、错误码和可重试性；
- 超时、幂等、限流、鉴权和调用限制；
- 版本、兼容性、废弃策略和示例；
- 事件生产与消费的外部可见约定。

**排除范围**

- Controller、Service、Client 等内部实现，进入 technical/modules；
- 服务间为什么形成当前依赖，进入 technical/architecture；
- 表结构、消息落库和一致性实现，进入 technical/data；
- 接口设计应该普遍遵循什么规则，且已获确认的内容，进入 technical/standards；
- 只在内部方法间使用、对模块外不构成稳定契约的参数。

**判断规则**

满足以下条件时选择本分类：

1. Primary question 是“作为调用方，我要发送什么、会收到什么、失败时如何处理”；
2. 文章可独立供模块外、服务外或系统外消费者使用；
3. 内部实现替换后，只要契约不变，文章主体仍成立。

文章应优先包含：调用场景、协议、地址或逻辑名称、请求、响应、错误、超时、幂等、版本、兼容性、调用示例和来源。

**典型文章**

- 创建交易 HTTP API
- 基金查询 RPC 契约
- transaction-created 事件契约
- 批量评估 CLI
- 账户状态 Webhook

**相邻分类区别**

- 与 architecture：interfaces 说明怎么调用；architecture 说明系统为何连接、边界如何划分。
- 与 modules：interfaces 是调用方可见契约；modules 是实现者可见内部逻辑。
- 与 standards：interfaces 记录某个真实接口或接口集合；standards 记录所有接口应遵循的已确认规则。

