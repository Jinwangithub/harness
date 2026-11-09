# Harness Engineering

Harness 是面向 Claude Code 和 Codex 的工程工作流，提供共享规则、Skills、角色提示、变更记录和机械验证工具。权威实现保留在 `.harness/`，宿主适配文件只负责暴露入口。

## 在本仓库使用

在 Claude Code 或 Codex 中打开本仓库后，可直接描述任务，宿主入口会将工作交给 Harness Orchestrator：

- Claude Code：`CLAUDE.md`
- Codex：`AGENTS.md`
- 显式调用：Claude Code 使用 `/harness:start` 或 `/harness:harness`，Codex 使用 `$harness`

插件同时通过 `agents/` 和 `skills/` 暴露角色提示与 Skills；这两个目录链接到 `.harness/` 中的权威文件。

## 安装为 Claude Code 插件

在 Claude Code 中将本仓库添加为 Marketplace 并安装插件：

```text
/plugin marketplace add Jinwangithub/harness
/plugin install harness@harness
```

插件会发布 `/harness:start`、`/harness:spec`、`/harness:plan`、`/harness:build`、`/harness:review`、`/harness:test`、`/harness:ship` 命令，以及 `harness` Skill 和 `planner`、`implementer`、`reviewer` Agents。消费项目安装并调用插件即可使用，不需要复制项目级 `AGENTS.md`、`CLAUDE.md`，也不需要迁移插件的 `.harness/agents/`、`rules/`、`skills/` 或 `tools/`。插件只在消费项目需要记录需求时创建 `.harness/changes/{change-id}/`。

## 安装为 Codex 插件

本仓库在 `.agents/plugins/marketplace.json` 注册了工作区本地 Codex Marketplace。在 Codex 中打开本仓库，在 Plugins 中启用 `harness`，然后重启 Codex。使用 `$harness` 可显式进入工作流。

要在其他工作区使用，可将本仓库链接到 Codex 插件目录：

```bash
mkdir -p ~/plugins ~/.agents/plugins
ln -sfn /absolute/path/to/harness ~/plugins/harness
```

将插件条目合并到 `~/.agents/plugins/marketplace.json`；如果该文件已存在，请保留原有内容：

```json
{
  "name": "local",
  "interface": { "displayName": "Local Plugins" },
  "plugins": [
    {
      "name": "harness",
      "source": { "source": "local", "path": "./plugins/harness" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Developer Tools"
    }
  ]
}
```

重启 Codex 以加载本地 Marketplace。要使用隔离的 Planner、Implementer 和 Reviewer 调度，需要启用 Codex multi-agent：

```toml
[features]
multi_agent = true
```

将该配置写入用户级 Codex 配置（`~/.codex/config.toml`）后重启 Codex。未启用 multi-agent 时，依赖隔离调度的 Standard-flow 阶段会阻塞。消费项目无需迁移本仓库的 Harness 文件，也无需创建 INDEX 或 memory。插件会把每个需求的记录写到消费项目自己的 `.harness/changes/{change-id}/`。

## 目录结构

| 路径 | 用途 |
|------|---------|
| `.harness/agents/` | Orchestrator and constrained role prompts |
| `.harness/rules/` | Flow, gate, and rollback policy |
| `.harness/skills/` | Reusable workflow and domain skills |
| `.harness/changes/` | Plugin development records; consumers receive per-demand records here |
| `.harness/tools/validate_change.py` | Plugin-bundled mechanical artifact validator |
| `.claude-plugin/` | Claude Code plugin and marketplace manifests |
| `.codex-plugin/` | Codex plugin manifest |
| `.agents/plugins/` | Workspace-local Codex marketplace registration |

验证器从插件安装目录运行，并显式接收消费项目根目录；不要从消费项目查找或复制验证器：

```text
python3 <plugin-root>/.harness/tools/validate_change.py --repo <consumer-project-root>
python3 <plugin-root>/.harness/tools/validate_change.py --repo <consumer-project-root> --change <change-id>
```

## 开发检查

运行仓库检查：

```bash
python3 -m unittest discover -s .harness/tools/tests -v
python3 .harness/tools/validate_change.py
```

## 参考资料

- [Agent Skills](https://github.com/addyosmani/agent-skills/tree/main/skills)
- [Harness Engineering: how I raised AI coding to 90%](https://mp.weixin.qq.com/s/rlIyIIZOXFObNIXbPI7gDg)
