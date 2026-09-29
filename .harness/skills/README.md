# Skills

本目录是 Skill 库。

- 所有 Skill 文件位于 `.harness/skills/{name}/SKILL.md`
- Skill 名称必须等于目录名：`{name}`
- Skill 内部补充 `.md` 默认不加载，仅在当前 Phase/Step 入口卡片、主 Skill、任务证据缺口或用户明确要求时读取
- Lite-flow Step 读取哪些 Skills、什么情况下补读、禁止事项和 Gate 提示见 `.harness/rules/flow-lite.md`
- Standard-flow Phase 读取哪些 Skills、什么情况下补读、禁止事项和 Gate 提示见 `.harness/rules/flow-standard.md`

## OpenViking Skills

- `project-knowledge-search`：只读召回。默认查询 OpenViking 项目知识根的 `wiki/`，仅在核验或知识缺口时回查 `raw/`；Lite L1、Standard Phase 1/2 按入口卡片加载。
- `project-knowledge`：长期知识编译。Lite L3、Standard Phase 6 在最终批准后执行 `raw ingest → wiki compile → index/log`；批准前不得写入外部知识库。
- OpenViking 的查询与写入只由以上两个 Skill 定义，不再维护其他 Wiki/curation Skill。
