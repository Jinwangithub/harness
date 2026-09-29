# Ingest and Maintenance

导入来源、执行 grounding/安全检查、操作 OpenViking 工具或审计维护知识库时读取本参考。
## 16. Grounding Checks

写入 wiki 前执行 locate-before-write：

- 数字、日期和直接引语必须能逐字定位到列出的 raw；
- 派生数值必须列出可定位的组成项和计算关系；
- 关键业务规则、接口行为、数据约束和运行步骤都要映射到来源；
- 找不到精确值时删除虚假精度或记录 Open question；
- raw 链接必须位于当前 knowledge-root/raw，不能引用其他项目或 wiki 自身；
- 搜索摘要只能用于发现，不能替代精确 raw 读取；
- 新来源与旧结论冲突时标记 Disputed；明确取代时标记 Outdated；
- 来源版本、采集时间和 dirty working tree 状态必须如实记录；
- 不能确认的信息写 Unknown，不得推定为最新、生产事实或团队标准；
- Inference 必须说明依据和推理，不能混入 Verified 结论。

## 17. 安全过滤

ingest 前检查：

- 密码、token、cookie、私钥和默认凭据；
- 个人数据、客户样本和受限业务数据；
- 生产地址、账号、内部访问入口和可用于攻击的配置；
- 日志、错误堆栈或示例中的敏感值。

疑似秘密不得进入 raw、wiki、index、log 或错误摘要。停止该来源的 ingest，记录不含具体值的排除类别并报告用户。可在用户授权范围内从原始材料生成脱敏副本后再 ingest，但不得修改已经保存的 raw 来“脱敏”。

日志只记录资源 URI、状态和脱敏摘要，不复制敏感正文。

## 18. Ingest 与 Compile 完整流程

1. 定位并验证 knowledge-root，确认项目身份，不猜造用户 ID 或覆盖其他项目。
2. 收集来源元数据，执行敏感信息检查，记录日期、revision 和工作区状态。
3. 按 requirements、product、technical、data 中唯一一个 raw 分类创建不可变来源文件。
4. 读取 wiki/index.md，沿一到两个相关分类 index 定位已有文章；只有索引缺失或主题不明时才聚焦搜索。
5. 从来源提取可复用知识单元；为每个单元写 Primary question、Answer、Scope、Evidence、Confidence 和 Related questions。
6. 使用 A 至 J 问题模型选择唯一主分类，并用边界矩阵做反证。
7. 依据相同主要问题与核心论点判定 New、Update、Disputed 或 No material。
8. 按一文一主要问题编译 wiki；独立次要问题拆分，必要上下文保留，其他内容省略。
9. 检查级联影响，更新依赖该结论的相关非归档文章；不把同一正文复制到多个分类。
10. 自下而上更新文章父 index 和全部祖先 index，直到 wiki/index.md。
11. 向 wiki/log.md 追加记录。
12. 重新读取受影响 raw、wiki、index 和 log；使用 list、tree 或 stat 核验路径、类型和直接文件布局。
13. 运行 grounding、分类、粒度、链接、状态和安全检查后，才记录 completed。

多来源研究可以并行收集来源，但 compile 必须逐个来源串行执行，因为文章、index 和 log 是共享状态。

## 19. OpenViking 写入约束

首次写入前验证当前部署能否：

- 按精确 URI 在同一目录创建、读取和更新多个普通文件；
- 把 index.md 和 log.md 作为普通文件保留；
- 对 log 执行 append；
- 通过 list、tree 或 stat 验证文件类型和路径。

canonical 写入规则：

- raw Markdown、代码、配置、SQL 快照使用精确文件写入，目标是 raw/category/source-slug.md；
- wiki 文章、index.md 和 log.md 使用精确文件 URI；
- 只有稳定分类路径使用目录创建；
- 不得创建 category/article-slug/，不得把 article-slug 当 parent；
- 同批次同分类的多篇文章分别写入，再统一更新 index；
- 更新 wiki 前先读取最新内容，避免覆盖并发变化；
- raw 已存在时换唯一文件名，不覆盖；
- log 首次 create，后续只 append。

add_resource 可能按文档名或标题生成资源目录、自动分段或把文件变为资源容器，因此不能用于 canonical raw、wiki、index 或 log。它只可用于用户明确接受的非 canonical 暂存树，且暂存内容不能直接作为 wiki 证据。

若只有 add_resource 而没有精确文件写入能力，本次 raw ingest 或 wiki compile 状态是 unavailable。不得接受目录变形，也不得把多个主题强行合并成一篇来规避能力缺口。

remember 属于个人或 Agent Memory，不是项目 raw/wiki 写入通道。不得绕过 MCP 调用原始 HTTP；正常流程不调用不可恢复的 forget。

创建后必须验证 raw 和 wiki 文章是分类目录下的直接普通文件。如果出现 model-routing/model-routing.md、Foo.java.md/Foo.java.md、标题派生目录或 _1.md、_2.md 分段文件，本次写入失败，应停止继续写入并报告结构问题。未经用户明确授权，不自动删除或迁移已有异常目录。

## 20. Maintenance Checks

用户要求 lint、审计或维护知识库时执行：

### 20.1 导航与结构

- 对比 wiki/index.md、各级 index 与实际文章；
- 缺失条目可以补齐，指向不存在文件的条目标记 MISSING，不静默删除；
- 所有包含文章或子目录的 wiki 目录都有 index.md；
- index 只列直接子项，从根索引能逐层到达每篇文章；
- 分类目录允许多篇直接文章，不存在 article/article.md 包装；
- canonical raw 不存在 source.md/source.md 或自动分段结构；
- 非 canonical 暂存资源有清楚标识，未被当作 raw 证据。

### 20.2 分类与粒度

- 每篇文章都有一个明确 Primary question 和唯一 Category；
- 文章路径与 A 至 J 路由一致；
- 对容易混淆的文章用边界矩阵复核；
- 同一主题未复制到多个分类；
- 多个独立问题已拆分并通过 See Also 关联；
- 不存在整个项目一篇或每个 Java 类一篇的极端粒度；
- 子目录符合稳定主题、独立边界、持续增长和降低检索成本四项条件。

### 20.3 standards 专项

- 每篇 standards 文章有项目确认依据；
- 能说明适用范围、强制性和例外；
- 通用经验、AI 建议和单点实现没有被误写成标准。

### 20.4 grounding 与状态

- 每篇非归档文章有当前知识根内可读取的 raw URI；
- 每条关键结论能映射到相应 raw；
- 冲突、过期、推断和未知已明确标记；
- 有 raw 但既未编译也未记录 No material 的积压被列出；
- 日期、数字、版本和直接引语没有无依据精确化。

### 20.5 可读性与安全

- 正文默认用简体中文解释，保留类名、表名、配置 key 和 API 字段原始标识符；
- 首次出现的缩写和内部术语有解释；
- 文章先给结论，再给关系、步骤、约束或实现；
- 流程确有先后时使用编号步骤或简短 Mermaid；
- 没有大段复制 raw，也没有逐文件清单冒充知识；
- wiki、raw、index、log 和诊断输出不含敏感值。

路径、index 和明确的分类一致性问题可以作为安全修复；事实、冲突状态、来源归属和 standards 确认状态只报告，未经证据核验不自动改写。lint 完成后向 wiki/log.md 追加脱敏摘要，不重写旧记录。

## 21. 禁止事项

禁止：

1. 为了目录看起来完整而增加大量分类或空目录；
2. 推翻 raw/wiki 双层模型或让两层内容混合；
3. 根据来源文件名、Java 包、类名或技术名词直接选择 wiki 分类；
4. 把每个 Java 类、SQL 文件或配置文件建立成一篇 wiki；
5. 把一个主题复制到多个分类；
6. 用 index 复制文章正文；
7. 把 AI 推测写成 Verified 项目事实；
8. 把通用技术经验写入 standards；
9. 把数据库、中间件、数据模型、部署和运维全部塞入 infrastructure；
10. 把业务流程和代码实现混成一篇全链路大文章；
11. 为单篇文章创建同名目录；
12. 用 add_resource 破坏 canonical 文件布局；
13. 为填模板而编造不存在的范围、证据、实现位置或规则；
14. 静默删除冲突、过期历史或旧日志；
15. 构造未经工具验证的 viking:// URI。

## 22. 完成验收

面对需求文档、产品文档、Java 代码、SQL、API 文档、架构图、部署文档或故障记录，执行者必须能够明确回答：

- 该资料是否值得进入 raw，进入哪个 raw 分类，为什么？
- 可以提炼出哪些长期知识单元？
- 每个知识单元的 Primary question 是 A 至 J 中哪一个？
- 唯一 wiki 主分类是什么，为什么不是相邻分类？
- 是创建新文章、更新旧文章、标记冲突，还是 No material？
- 是否需要拆分文章、添加 See Also 或创建子目录？
- 哪些 index 需要自下而上更新？
- log 应追加什么记录？
- 每条关键结论由哪个精确 raw URI 支持？
- 是否存在 Inference、Unknown、Disputed、Outdated 或敏感内容？
- 写入后的文件类型、路径、链接和导航是否已经验证？

若任一问题无法依据本规范得到明确答案，不应让 AI 猜目录；继续拆分主要问题、回查证据或把缺口记录为 Open question。

最终稳定流程是：

~~~text
资料
  ↓
判定 raw 来源分类
  ↓
提取长期知识单元
  ↓
写出唯一主要问题
  ↓
映射 A-J 分类
  ↓
用边界矩阵反证
  ↓
判断文章粒度与 New/Update/Disputed/No material
  ↓
写入或更新 wiki
  ↓
更新 index
  ↓
追加 log
  ↓
执行 grounding、结构、分类和安全验证
~~~

验收标准不是目录是否漂亮，而是不同 AI、不同时间、不同任务面对同一份资料时，能够依据相同问题和边界规则得到基本一致的分类结果。

设计参考：[Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki)。本规范保留 raw/wiki 编译、disposition、级联更新、index/log 和 grounding 原则，并将路径映射为 OpenViking URI。
