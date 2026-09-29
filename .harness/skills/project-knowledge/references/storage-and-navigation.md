# Storage and Navigation

首次初始化或写入 raw/wiki、处理 URI、文章模板、index 或 log 时读取本参考。
## 2. Directory Model

knowledge-root 是当前项目已经确认的 OpenViking Resource URI：

~~~text
<knowledge-root>/
├── raw/
│   ├── requirements/
│   ├── product/
│   ├── technical/
│   └── data/
└── wiki/
    ├── index.md
    ├── log.md
    ├── business/
    │   ├── index.md
    │   ├── domain/
    │   │   ├── index.md
    │   │   └── {concept}.md
    │   ├── rules/
    │   │   ├── index.md
    │   │   └── {rule-set}.md
    │   └── processes/
    │       ├── index.md
    │       └── {process}.md
    └── technical/
        ├── index.md
        ├── architecture/
        │   ├── index.md
        │   └── {architecture-topic}.md
        ├── interfaces/
        │   ├── index.md
        │   └── {interface-set}.md
        ├── modules/
        │   ├── index.md
        │   └── {module}.md
        ├── data/
        │   ├── index.md
        │   └── {data-topic}.md
        ├── infrastructure/
        │   ├── index.md
        │   └── {infrastructure-topic}.md
        ├── operations/
        │   ├── index.md
        │   └── {operational-topic}.md
        └── standards/
            ├── index.md
            └── {confirmed-standard}.md
~~~

目录是稳定分类容器，文章是目录中的普通 Markdown 文件。分类是可用路由，不代表必须提前创建所有空目录。首次 ingest 只创建当前需要的路径；但 wiki 根目录以及每个含文章或子目录的 wiki 目录都必须有 index.md。

创建 wiki/technical/modules/model-routing.md 时，需要同时存在：

- wiki/index.md
- wiki/technical/index.md
- wiki/technical/modules/index.md
- wiki/technical/modules/model-routing.md

index 只导航直接子目录和直接子文章，不复制文章正文。wiki/log.md 是 append-only 操作记录，由根索引链接，但不作为普通知识文章列入分类索引。

raw 是证据存档，不是导航式知识树，不要求每层都有 index.md。canonical raw 文件直接位于四个证据分类目录中，例如 raw/technical/src-deploy-model-route-service.java.md。来源的仓库相对路径、发布日期和 revision 放在 raw 元数据中，不通过复制代码目录制造 OpenViking 层级。

OpenViking 自动生成的 .abstract.md、.overview.md 或 .relations.json 是语义 sidecar，不手工创建，也不作为 raw 或 wiki 正文。

## 3. 目录与文件映射

同一分类目录可以保存多篇文章。典型叶子分类是 index.md 加若干互相关联的主题文章：

~~~text
wiki/technical/modules/
├── index.md
├── transaction-processing.md
├── model-routing.md
└── async-evaluation.md
~~~

禁止把文章误建成资源容器：

~~~text
wiki/technical/modules/
├── transaction-processing/
│   └── transaction-processing.md
└── model-routing/
    └── model-routing.md
~~~

默认目录深度是：

~~~text
wiki/<axis>/<category>/<article>.md
~~~

目录负责粗粒度路由，文章负责具体知识，See Also 负责文章之间的关系。

只有同时满足以下条件时才创建 category 下面的新子分类：

1. 已存在多个稳定主题，而不是只有一篇文章；
2. 这些主题形成独立且清楚的读者检索边界；
3. 有证据表明该主题集合会继续增长；
4. 新目录能显著降低检索成本，并能说明每一级目录的新增含义。

实践约束：

- 叶子分类通常包含 2 至 8 篇相互相关的文章；
- 只有一个主题且没有明确扩展计划时，放入已有分类，不创建单文件子目录；
- 分类下约有 12 篇以上文章，或读者任务、生命周期、维护责任明显分化时，才考虑拆分；
- 更深一级目录至少应有两个可导航子项；
- 禁止 foo/foo.md、module-a/index.md 之类包装单篇文章的结构；
- 空目录不创建。

canonical raw 同样使用“分类目录下直接文件”。如果出现 Foo.java.md/Foo.java.md、标题派生目录或自动生成的 _1.md、_2.md 分段文件，说明写入方式破坏了 canonical 布局。

## 4. raw 层路由

raw 的分类依据是**来源性质**，不是从来源中提炼出的知识类型。

| raw 分类 | 应收录 | 不应收录 |
|---|---|---|
| requirements | 用户需求、验收条件、需求变更、约束原文 | AI 改写后的业务规则总结 |
| product | 产品说明、交互稿说明、产品配置、业务资料和使用说明 | 代码实现摘要、数据库设计推断 |
| technical | 技术方案、架构/API/部署说明、代码或配置快照、技术调研原文 | 从技术资料综合出的 wiki 结论 |
| data | JSON、CSV、SQL、数据字典、样本和其他原始结构化数据 | 已整理的数据模型或一致性说明 |

raw 分类不需要与 wiki 对称。例如一份 API 设计原文进入 raw/technical，从中可以编译出 technical/interfaces、technical/modules 或 technical/standards，具体取决于每篇 wiki 文章的主要问题。

raw 文件名优先使用 YYYY-MM-DD-descriptive-slug.md，日期取来源发布日期；发布日期未知时省略日期前缀，并在元数据写 Published: Unknown。同名来源追加数字后缀。raw 文件创建后不可覆盖、追加或 edit；新版本写新文件。

## 10. raw → wiki 可追溯体系

完整链路是：

~~~text
source
  ↓
canonical raw file
  ↓
wiki conclusion
  ↓
exact raw URI + location hint
  ↓
grounding check
~~~

每篇非归档 wiki 文章必须回答：

- 这条知识来自哪些 raw？
- 哪个 raw 片段支持哪个结论？
- 适用于哪个版本、环境或业务范围？
- 是 Verified、Inference、Unknown、Disputed 还是 Outdated？
- 新资料到来时应更新哪篇文章？

wiki 自身、index、搜索摘要和 OpenViking sidecar 不能作为原始证据。

## 11. Raw Template

~~~markdown
# {Title}

> Source: {URL or origin description}
> Collected: {YYYY-MM-DD}
> Published: {YYYY-MM-DD or Unknown}
> Project: {stable project identity}
> Revision: {release / commit / document version / Unknown}
> Workspace: {clean / dirty snapshot / not applicable}

{Preserved source content. Clean formatting noise only; do not alter meaning.}
~~~

## 12. Wiki Article Template

~~~markdown
# {Concept Title}

> Purpose: {读者看完能理解或完成什么}
> Primary question: {A-J + 完整问句}
> Category: {唯一 wiki 分类}
> Confidence: {Verified / Inference / Mixed / Unknown}
> Conflict: {None / Disputed / Outdated}
> Updated: {YYYY-MM-DD}
> Basis: {source date + release/commit/revision; dirty working tree 时明确写 snapshot}

## 结论

{直接回答 Primary question，说明用途、范围和最重要结论。未经验证的部分就地标记。}

## 适用范围

{系统、模块、业务、环境、版本、前置条件和明确不适用范围。}

## {分类相关主体}

{根据分类写定义与关系、规则与例外、流程步骤、架构关系、模块实现、接口契约、数据模型、基础设施基线、Runbook 或已确认标准。只保留回答主要问题所需内容。}

## 实现或定位

{按需写仓库相对路径、类/方法、表、接口、配置 key、指标或运维入口。没有时省略，不为填模板而编造。}

## 来源与依据

| 支持的结论 | Raw 来源 | 定位与备注 |
|---|---|---|
| {结论或段落主题} | [{source title}]({exact viking:// raw URI}) | {章节、文件、类、方法、行或字段等定位线索} |

> **Status: Outdated** (YYYY-MM-DD)
> {被什么新证据替代、当前理解是什么。保留有历史价值的旧结论。}

> **Status: Disputed**
> {逐项列出冲突说法、各自来源和缺少的裁决证据。}

> **Open question**
> {缺少的证据、影响和待回答问题。}

## See Also

- [{Related concept}]({exact viking:// wiki URI}) — {它回答的另一个问题}
~~~

正文标题可按分类调整，但必须保留：

- 先结论后细节；
- Primary question 和唯一 Category；
- 适用范围；
- 可追溯来源；
- 状态清晰；
- 必要时通过 See Also 关联其他分类。

每个关键结论都要映射到支持它的 raw，而不是只在文末堆没有对应关系的来源清单。

## 14. Global Index

每个 index.md 只列当前目录的直接子项，不递归复制整棵树。

根 wiki/index.md 应给出：

- 稳定项目身份；
- 精确 knowledge-root URI；
- 项目简介和知识适用范围；
- business、technical 等直接子目录入口；
- wiki/log.md 入口；
- 少量高频主题快捷入口，可选。

根索引示例：

~~~markdown
# Project Knowledge Index

> Project: {stable project identity}
> Knowledge root: {exact viking:// URI}

## 阅读入口

| 目录 | 主要问题 |
|---|---|
| [{Category}/]({exact viking:// wiki URI}) | {进入该分类能回答什么} |

## 操作记录

- [Knowledge log]({exact viking:// log URI})
~~~

分类索引必须说明收录与排除边界，并列直接子项：

~~~markdown
# {Category} Index

> Core question: {A-J 对应问题}
> Includes: {收录范围摘要}
> Excludes: {最容易误入本分类的内容及正确去向}

## 子目录

| Directory | 用途 |
|---|---|
| [{child}/]({exact viking:// wiki URI}) | {何时进入该目录} |

## 本目录文章

| Article | Primary question | Updated |
|---|---|---|
| [{Title}]({exact viking:// wiki URI}) | {文章主要回答的问题} | {YYYY-MM-DD} |
~~~

每篇文章只在直接父索引出现一次；更高层索引链接分类或子目录。快捷入口不能代替分类索引。

index 的 Updated 只在知识内容或导航目标改变时更新；文章的 Updated 只随知识内容变化，不因纯排版变化更新。

## 15. Append-Only Log

wiki/log.md 只允许追加：

~~~markdown
## [YYYY-MM-DD] ingest | {primary article or no material: raw URI}
- Disposition: {New; Update; Disputed; No material}
- Primary question: {A-J + question / none}
- Primary category: {wiki category / none}
- Raw: {exact viking:// raw URI}
- Wiki: {exact viking:// wiki URI or none}
- Updated: {cascade-updated wiki URI; omit when none}
~~~

New、Update 和 Disputed 可以组合；No material 独占。不得修改旧日志来伪装历史。

