# Security Checklist

## OWASP Top 10 快速清单

- Broken Access Control：越权、水平越权、对象级授权。
- Cryptographic Failures：敏感数据明文存储或传输。
- Injection：SQL、NoSQL、命令、表达式注入。
- Insecure Design：缺少安全边界、威胁建模不足。
- Security Misconfiguration：默认配置、调试开关、过宽 CORS。
- Vulnerable and Outdated Components：存在高危依赖。
- Identification and Authentication Failures：认证绕过、弱会话管理。
- Software and Data Integrity Failures：不可信更新、反序列化风险。
- Security Logging and Monitoring Failures：安全事件不可追溯。
- SSRF：服务端请求伪造。

## 输入校验

- 所有用户输入在系统边界校验。
- 使用白名单、长度限制、格式限制。
- 避免只在前端校验。
- 错误信息不得泄露内部实现。

## 认证鉴权

- 所有敏感接口必须校验认证状态。
- 数据读取和修改必须校验对象级授权。
- 管理接口必须有角色或权限检查。
- 禁止客户端传入角色或权限后直接信任。

## 敏感信息与日志脱敏

- 不记录 token、cookie、密码、密钥、身份证号、手机号全量等敏感信息。
- 配置文件不得提交真实密钥。
- 错误日志避免打印完整请求体中的敏感字段。

## SQL / 命令注入

- SQL 使用参数化查询或 ORM 安全绑定。
- 禁止拼接用户输入形成 SQL。
- 命令执行必须避免 shell 拼接；确需执行时使用参数数组和白名单。
- 文件路径参数必须限制在允许目录内。

## SSRF / 路径穿越

- 外部 URL 请求必须限制协议、域名/IP 范围和重定向行为。
- 禁止访问内网元数据地址和本地回环地址。
- 文件读取/写入必须规范化路径并校验根目录。

## 依赖与配置安全

- 检查依赖漏洞和许可证风险。
- 关闭生产调试端点。
- 设置合理 CORS、Cookie Secure/HttpOnly/SameSite。
- 外部服务调用设置超时、重试上限和降级。

## Phase 5 security_report 最小结构

`security_report_v1.md` 至少包含：

- Verdict。
- Scope。
- Mechanical Checks。
- OWASP Top 10 检查结果。
- Findings（Severity、Risk、Evidence、Fix）。
- Critical 计数。
- Must Fix 计数。
- Evidence 路径。
- Required Fixes。
