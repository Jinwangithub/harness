---
title: {系统名称}
domain: {domain-name}
modules:
  - {src/path}
type: integration-fact
tags: [{tag1}, {tag2}]
updated: {YYYY-MM-DD}
---

# {系统名称}

## 接入用途

- {purpose}

## 协议

- 协议：{HTTP/gRPC/MQ/etc.}
- 数据格式：{JSON/Protobuf/XML/etc.}
- Endpoint / Topic：{非敏感地址或占位符}

## 鉴权

- 方式：{OAuth2/API Key/mTLS/etc.}
- 密钥存储：{配置中心/环境变量/密钥管理服务}
- 注意：不得提交真实 token、cookie、密钥。

## 超时

- 连接超时：{value}
- 读取超时：{value}
- 总超时：{value}

## 重试

- 重试次数：{count}
- 退避策略：{fixed/exponential/jitter}
- 幂等性要求：{description}

## 降级

- 触发条件：{condition}
- 降级行为：{behavior}
- 用户可见影响：{impact}

## 监控

- 成功率：{metric}
- 延迟：{metric}
- 错误码：{metric}
- 告警：{alert}

## 测试环境

- 测试 Endpoint：{placeholder, no secrets}
- 测试账号：{placeholder, no secrets}
- Mock / Sandbox：{description}
