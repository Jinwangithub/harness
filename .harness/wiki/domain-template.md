# Domain Template

用于业务域知识实例化。不要在模板中填写虚构业务内容。

## 业务域名称

- {domain name}

## 术语表

| 术语 | 定义 | 备注 |
|------|------|------|
| {term} | {definition} | {notes} |

## 核心实体

| 实体 | 关键字段 | 说明 |
|------|----------|------|
| {entity} | {fields} | {description} |

## 状态机

```text
{state A} -> {state B} -> {state C}
```

| 状态 | 含义 | 可进入条件 | 可退出条件 |
|------|------|------------|------------|
| {state} | {meaning} | {entry} | {exit} |

## 关键流程

1. {step 1}
2. {step 2}
3. {step 3}

## 异常规则

| 场景 | 规则 | 处理方式 |
|------|------|----------|
| {scenario} | {rule} | {handling} |

## 上下游依赖

| 上游/下游 | 系统 | 交互内容 | 风险 |
|-----------|------|----------|------|
| {direction} | {system} | {interaction} | {risk} |
