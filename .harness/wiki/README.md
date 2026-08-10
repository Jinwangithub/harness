# 项目知识库

> Orchestrator L3 按需查询层 — 存储项目业务域名、术语、集成、模块映射等已获人工确认的正式知识。

## 目录结构

```text
.harness/wiki/
├── README.md                # 本文件：原则 + 实例化指南
├── index.md                 # 自动生成：Module→Wiki 映射 + 按域分类索引
├── log.md                   # Append-only：approved/rejected/deferred 决策记录
├── project/
│   └── overview.md          # 项目概览：技术栈 + 模块→域映射表 + 构建 + 环境
├── domains/
│   ├── _TEMPLATE.md         # 模板（_ 前缀不纳入 index）
│   └── {domain}.md          # 业务域知识：术语、实体、状态机、流程、异常规则
├── integrations/
│   ├── _TEMPLATE.md         # 模板
│   └── {system}.md          # 外部系统集成：协议、鉴权、超时、重试、降级
└── modules/
    ├── _TEMPLATE.md         # 模板
    └── {module}.md          # 模块级业务知识：输入输出约束、边界条件、非功能要求
```

- `_TEMPLATE.md` 文件不会被 `generate_wiki_index.py` 扫描入索引。
- 所有正式页面头部必须有 YAML frontmatter（见各模板）。

## Candidate-first 更新策略

1. 每个完成需求的业务知识先写入 `.harness/changes/{change-id}/wiki/candidates.md`（候选层，非 canonical）。
2. 未经明确人类批准，不得将候选内容写入 `.harness/wiki/`。
3. 批准后：更新正式 wiki 页面 → 运行 `python3 .harness/tools/generate_wiki_index.py` 重生成 `index.md` → append 到 `log.md`。
4. Rejected / deferred 的候选仅保留在 change artifact 中。

## 实例化指南

### 最小填充路径

1. 填写 `project/overview.md`：项目名、技术栈、**模块→域映射表**、构建命令。
2. 只填写已知事实，未知业务规则写 `{待确认}`。
3. 当前需求涉及某业务域时，才创建 `domains/{domain}.md`。
4. 当前需求涉及外部系统时，才创建 `integrations/{system}.md`。
5. 当前需求涉及某模块的特定业务约束时，才创建 `modules/{module}.md`。

### 原则

- 不得猜测：未知业务规则写 `{待确认}` 或记入 Phase 1 Open Questions。
- 模板文件以 `_TEMPLATE.md` 命名，正式页面按实际名称。
- `generate_wiki_index.py` 自动同步 `index.md`，不要手工编辑。

### Minimal Example

以下是 `project/overview.md` 的最小实例化形式：

```markdown
---
title: 示例订单服务
domain: order-management
updated: 2026-01-01
---

# 项目概览

## 项目
- 名称：示例订单服务
- 目的：演示 wiki 最小实例化。

## 技术栈
- Runtime: {待确认}
- Build: {待确认}
- Test: {待确认}

## 模块映射

| 代码路径 | 业务域 | 说明 |
|----------|--------|------|
| src/orders/ | order-management | 订单录入、状态流转 |
| src/notifications/ | notification | 通知偏好、消息发送 |

## 关键业务域
- order-management: 订单完整生命周期管理，精确状态和流转规则为 {待确认}。
- notification: 消息通知渠道规则为 {待确认}。

## 外部依赖
- 邮件服务：{待确认}
- 短信服务：{待确认}

## 构建命令
{待确认}

## 环境说明
- 开发：{待确认}
- 测试：{待确认}
- 生产：{待确认}
```

## Orchestrator 使用规则

- 遇到不清的业务概念时，先查 `index.md` 的 Module→Wiki 映射表找到对应域/模块页面。
- 若必要业务知识未实例化或标记 `{待确认}`，在 Phase 1 作为 Open Question 询问用户，不猜测。
