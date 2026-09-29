# OpenViking Knowledge Model

本页是参考文档路由，不是完整规范。项目知识保留 \`raw/\` 原始证据与 \`wiki/\` 编译知识的双层模型；wiki 分类只按文章主要回答的问题选择，每篇文章只有一个主分类。根据当前工作加载下表所列参考，不要默认读取全部文件。

| 当前任务 | 读取参考 |
|---|---|
| 选择 wiki 分类、处理边界冲突或查看路由案例 | [classification.md](classification.md)，以及对应的分类定义文件 |
| 选择 \`business/domain\`、\`business/rules\`、\`business/processes\` | [business-categories.md](business-categories.md) |
| 选择 \`technical/architecture\`、\`technical/modules\`、\`technical/interfaces\` | [technical-system-categories.md](technical-system-categories.md) |
| 选择 \`technical/data\`、\`technical/infrastructure\`、\`technical/operations\`、\`technical/standards\` | [technical-data-operations-categories.md](technical-data-operations-categories.md) |
| 判断文章粒度、拆分/合并及 New/Update/Disputed/No material | [article-lifecycle.md](article-lifecycle.md) |
| 初始化目录或编写 raw/wiki、index、log | [storage-and-navigation.md](storage-and-navigation.md) |
| ingest、安全过滤、grounding、工具写入或知识库审计 | [ingest-and-maintenance.md](ingest-and-maintenance.md) |

## 共同约束

- raw 保存原始来源，固定使用 \`requirements/\`、\`product/\`、\`technical/\`、\`data/\` 四类；wiki 保存有证据支撑的长期项目认识。
- wiki 一级知识域和十个分类保持稳定，不按来源文件、代码包或技术名词机械分类。
- 每条 wiki 结论应能追溯到当前知识根下的精确 raw URI，并明确事实、推断、未知、冲突或过期状态。
- 目录只表达稳定分类，文章直接存放在分类目录中；默认路径为 \`wiki/<axis>/<category>/<article>.md\`。
- 每个含文章或子目录的 wiki 目录都需要 \`index.md\`；索引只列直接子项。每次 ingest 都向 \`wiki/log.md\` 追加记录。
- 分类、文章、URI、工具、索引和安全检查的详细规则只在上表对应参考中维护，避免跨文档重复。
