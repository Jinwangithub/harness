# Harness Tools

`tools/` 只放 Harness 自身需要执行的机械工具，不承载业务逻辑或知识库写回。

| 工具 | 用途 | 频率 |
|---|---|---|
| `validate_change.py` | 从插件执行，校验传入消费项目的需求目录、产物边界、Gate 证据和状态一致性 | 每个 Gate、完成前 |
| `tests/` | 上述工具的离线单元测试 | 修改工具后 |

消费项目无需复制此目录。验证时显式传入项目根目录；若项目没有 `changes/INDEX.md`，工具会扫描 `.harness/changes/*/summary.md`。

工具失败时停止当前流程并定位根因，不通过增加旁路脚本绕过门禁。
