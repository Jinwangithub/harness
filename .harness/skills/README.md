# Skills

本目录是 Skill 库。

本目录内容随 Harness 插件安装并由插件读取。文件中的 `.harness/...` 源路径都指插件包内部。消费项目只保存每项需求的 `docs/harness/{change-id}/` 产物。

- 所有 Skill 文件位于 `.harness/skills/{name}/SKILL.md`
- Skill 名称必须等于目录名：`{name}`
- Skill 内部补充 `.md` 默认不加载，仅在当前 Phase/Step 入口卡片、主 Skill、任务证据缺口或用户明确要求时读取
- Lite-flow Step 读取哪些 Skills、什么情况下补读、禁止事项和 Gate 提示见 `.harness/rules/flow-lite.md`
- Standard-flow Phase 读取哪些 Skills、什么情况下补读、禁止事项和 Gate 提示见 `.harness/rules/flow-standard.md`

## OpenViking Skills

- `project-knowledge-search`：只读召回。默认查询 OpenViking 项目知识根的 `wiki/`，仅在核验或知识缺口时回查 `raw/`；Lite L1、Standard Phase 1/2 按入口卡片加载。
- `project-knowledge`：用户显式请求时执行的长期知识编译。它不属于 Lite L3 或 Standard Phase 5 的自动步骤；执行时按 `raw ingest → wiki compile → index/log` 维护知识库，未经明确授权不得写入外部知识库。
- OpenViking 的查询与写入只由以上两个 Skill 定义，不再维护其他 Wiki/curation Skill。
