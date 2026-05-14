# Integration Template

用于外部系统接入说明。不要在模板中填写虚构系统信息。

## 系统名称

- {system name}

## 接入用途

- {purpose}

## 协议

- 协议：{HTTP/gRPC/MQ/etc.}
- 数据格式：{JSON/Protobuf/XML/etc.}
- Endpoint / Topic：{非敏感地址或占位符}

## 鉴权

- 鉴权方式：{OAuth2/API Key/mTLS/etc.}
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

- 降级触发条件：{condition}
- 降级行为：{behavior}
- 用户可见影响：{impact}

## 监控

- 成功率：{metric}
- 延迟：{metric}
- 错误码：{metric}
- 告警规则：{alert}

## 测试环境

- 测试 Endpoint / Topic：{placeholder}
- 测试账号：{placeholder, no secrets}
- Mock / Sandbox：{description}
