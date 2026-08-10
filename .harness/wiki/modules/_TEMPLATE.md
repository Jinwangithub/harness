---
title: {模块名称}
domain: {domain-name}
modules:
  - {src/path}
type: operational-constraint
tags: [{tag1}, {tag2}]
updated: {YYYY-MM-DD}
---

# {模块名称}

## 关联业务域

- 所属域：{domain-name}（详见 `domains/{domain-name}.md`）
- 涉及的核心实体：{entity list}

## 输入约束

| 字段 | 约束 | 来源 |
|------|------|------|
| {field} | {validation/range/format} | {API/DB/upstream} |

## 输出约束

| 字段 | 约束 | 影响方 |
|------|------|--------|
| {field} | {format/guarantee} | {consumer} |

## 边界条件

- 最大值/最小值：{limits}
- 并发限制：{concurrency}
- 幂等性要求：{idempotency or N/A}

## 非功能要求

- 性能：{latency/throughput or 待确认}
- 可靠性：{SLA or 待确认}
- 安全：{authN/authZ/data classification or 待确认}

## 已知限制

- {limitation}: {impact and workaround}
