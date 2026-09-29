# Classification Routing

在提取知识单元、选择唯一主分类、处理跨分类内容或判断典型案例时读取本参考。
## 5. wiki 的统一问题路由模型

处理每个候选知识单元时，先写出一句完整的 Primary question，再按下表映射。来源文件类型不参与分类决策。

| 编号 | Primary question | 主分类 |
|---|---|---|
| A | 这是什么业务对象、概念、角色或术语，它们有什么业务关系？ | business/domain |
| B | 什么条件下允许、禁止、成功、失败或发生业务状态变化？ | business/rules |
| C | 一个业务事件从开始到结束是怎么发生的？ | business/processes |
| D | 系统由什么组成，各边界、组件和上下游是什么关系？ | technical/architecture |
| E | 某个代码模块负责什么，内部如何实现、协作和扩展？ | technical/modules |
| F | 外部调用方如何调用系统，并理解输入、输出、错误和兼容性？ | technical/interfaces |
| G | 数据是什么、在哪里、如何关联、流转、归属和保持一致？ | technical/data |
| H | 系统依赖什么环境、中间件、网络和基础设施才能运行？ | technical/infrastructure |
| I | 系统运行时如何发布、监控、告警、排障、恢复和验证？ | technical/operations |
| J | 项目或团队已确认统一采用什么工程规范？ | technical/standards |

### 5.1 机械决策树

对每个候选知识单元按顺序执行：

1. **它是来源还是结论？**
   - 来源原文、代码快照、SQL、文档和样本先进入 raw。
   - 由来源支持、可供以后复用的项目认识才成为 wiki 候选。
2. **它主要回答业务问题还是技术问题？**
   - 不依赖代码和部署也成立的业务含义，进入 A、B、C。
   - 关于系统结构、实现、契约、数据、环境、运行或工程约定，进入 D 至 J。
3. **把标题改写成一个问句。**
   - 若必须用“以及”连接两个独立问题，先拆分知识单元。
4. **在 A 至 J 中选择唯一一个最贴近的问句。**
   - 根据读者读完后能解决的首要问题选择，不根据文中出现了哪些名词选择。
5. **做相邻分类反证。**
   - 对照第 7 节边界矩阵，说明为什么不是最容易混淆的另一个分类。
6. **检查是否已有同一主要问题。**
   - 同一主要问题、相同核心论点：Update 原文章。
   - 主要问题不同：新建文章，即使来源相同。
7. **处理次要内容。**
   - 只是支撑主问题的必要上下文：保留在本文，但控制篇幅。
   - 能独立回答另一个问题：拆成另一篇文章，用 See Also 互链。
   - 不影响读者完成主任务：省略，读者需要时回到 raw。
8. **验证唯一性。**
   - 每篇文章只有一个 Primary question 和一个 Primary category。

### 5.2 选择主分类的优先原则

当一篇草稿看似符合多个分类时，依次判断：

1. 读者为何打开它？
2. 标题和结论直接回答什么？
3. 删除某部分后，文章的主要用途是否仍成立？
4. 哪个分类的收录条件全部满足，同时排除条件最少？

出现的组件、文件、协议或技术名词只构成内容，不自动决定分类。例如流程文章可以提到 API、Service、DB 和 MQ，但只要主要回答“业务怎么走”，主分类仍是 business/processes。

## 7. 相邻分类边界矩阵

混合内容先依据主要问题选择主分类，再把独立的次要问题拆分并用 See Also 连接。

| 边界 | 判断问题 | 左侧分类收录 | 右侧分类收录 | 混合内容处理 |
|---|---|---|---|---|
| domain vs rules | 重点是定义对象，还是判断条件？ | domain：对象、角色、术语、关系、状态含义 | rules：允许、禁止、成功、失败、转换条件 | 领域文章只概述有规则存在；详细条件独立成 rules |
| rules vs processes | 去掉时间顺序后文章是否仍完整？ | rules：决策条件、阈值、守卫、例外 | processes：触发、参与者、步骤、分支、结果 | 流程步骤引用规则文章；不要在流程中复制完整规则集 |
| architecture vs modules | 范围跨系统组件，还是深入一个代码单元？ | architecture：系统边界、组件关系、依赖方向 | modules：代码位置、内部协作、实现、扩展点 | 架构文章链接模块细节；模块文章只保留必要的系统上下文 |
| architecture vs interfaces | 重点是谁与谁连接，还是调用者怎样调用？ | architecture：关系、边界、链路、系统级选择 | interfaces：协议、字段、错误、超时、兼容性 | 架构写关系，接口写契约；同一调用链可分别形成两篇 |
| modules vs interfaces | 更换内部实现后文章是否仍成立？ | modules：内部类、方法、算法和协作 | interfaces：外部稳定契约 | 对外部分独立成 interfaces，内部实现留在 modules |
| data vs infrastructure | 重点是存什么，还是用什么平台承载？ | data：模型、关系、流转、一致性、缓存语义 | infrastructure：集群、版本、网络、配置和容量 | Redis 数据模型进 data；Redis 集群配置进 infrastructure |
| data vs operations | 重点是正常数据语义，还是异常恢复动作？ | data：正常模型、生命周期和一致性 | operations：积压、丢失、延迟等诊断、修复和验证 | 数据文章链接 Runbook；恢复步骤不塞入数据模型正文 |
| infrastructure vs operations | 重点是正常运行基线，还是运行时操作？ | infrastructure：部署、接入、依赖和配置 | operations：监控、发布、排障、恢复 | 基线和 Runbook 分篇，互相链接 |
| standards vs ordinary technical | 是否有证据证明是团队统一规则？ | standards：已确认、跨范围、可检查的约定 | 其他技术分类：具体事实、实现、契约、环境或经验 | 证据不足不得放 standards；先按具体主要问题分类并标注待确认 |

补充边界：

- architecture vs infrastructure：系统级逻辑边界、质量属性和组件关系属于 architecture；环境、集群、网络和中间件配置属于 infrastructure。
- processes vs operations：业务事件怎么完成属于 processes；系统异常后人员或自动化如何处置属于 operations。
- rules vs interfaces：业务资格和状态条件属于 rules；参数合法性、协议错误和调用限制属于 interfaces。若接口错误直接暴露业务拒绝，可在接口文章引用对应 rule。

## 8. 分类冲突与典型案例

### 8.1 订单创建流程

内容可能包含 API、Service、DB 和 MQ，但主要回答“订单从提交到创建完成如何发生”。

- Primary question：C
- 主分类：business/processes
- 处理：接口字段、代码实现和数据模型只保留理解流程所需摘要，并分别 See Also 到 interfaces、modules、data。

### 8.2 订单创建接口

主要回答“调用方如何创建订单并处理结果”。

- Primary question：F
- 主分类：technical/interfaces
- 处理：请求、响应、错误、幂等和版本是主体；Controller 和 Service 实现不展开。

### 8.3 订单服务实现

主要回答“Java 代码如何实现订单创建和扩展”。

- Primary question：E
- 主分类：technical/modules
- 处理：说明代码入口、内部协作和扩展点；业务规则与接口契约用链接引用。

### 8.4 订单数据模型

主要回答“订单数据如何存储、关联和保持一致”。

- Primary question：G
- 主分类：technical/data
- 处理：表、字段、关系、状态数据和一致性是主体；不展开集群部署。

### 8.5 订单 Redis 集群部署

主要回答“Redis 运行依赖如何部署和接入”。

- Primary question：H
- 主分类：technical/infrastructure
- 处理：拓扑、版本、连接、容量和环境差异是主体；Redis 中存放的订单结构链接 data。

### 8.6 订单 Redis 故障排查

主要回答“Redis 故障后如何定位、恢复和验证”。

- Primary question：I
- 主分类：technical/operations
- 处理：现象、影响、排查、恢复和验证是主体；正常集群基线链接 infrastructure。

### 8.7 订单状态转换

按文章重点决定：

- “哪些条件允许 PAID 转为 REFUNDING” → business/rules；
- “退款业务从申请到完成经过哪些状态” → business/processes；
- “状态字段如何持久化和同步” → technical/data；
- “状态机代码由哪些类实现” → technical/modules。

“状态转换”这个名词本身不能决定目录。

### 8.8 服务调用关系

按文章重点决定：

- “订单服务、支付服务、库存服务的系统关系” → technical/architecture；
- “订单服务如何调用支付 RPC” → technical/interfaces；
- “PaymentClient 和重试拦截器如何实现” → technical/modules；
- “调用失败后如何告警和恢复” → technical/operations。

### 8.9 Kafka Topic

按文章重点决定：

- Topic 中事件字段、版本和消费者契约 → technical/interfaces；
- 事件从 DB 到 Topic 再到下游的数据流和一致性 → technical/data；
- Topic 分区、保留期、集群和环境配置 → technical/infrastructure；
- 消息堆积、消费延迟和重放步骤 → technical/operations。

### 8.10 API 规范

- 某个 createTransaction API 的真实请求和响应 → technical/interfaces；
- 项目所有 HTTP API 必须采用的错误格式，且有确认依据 → technical/standards；
- AI 建议统一错误格式，但项目没有证据 → 不能写入 standards，可记录 Open question。

