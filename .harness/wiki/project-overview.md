# Project Overview Template

当前仓库是 Harness Engineering 框架模板，不内置具体业务知识。

业务项目接入时，请实例化以下内容：

## 项目名称

- {填写项目名称}

## 技术栈

- 后端：{语言 / 框架 / 版本}
- 前端：{框架 / 构建工具 / 版本}
- 数据库：{数据库 / 版本}
- 中间件：{缓存 / 消息队列 / 搜索 / 其他}

## 模块边界

| 模块 | 职责 | 依赖 |
|------|------|------|
| {module} | {responsibility} | {dependencies} |

## 关键业务域

- {业务域 1}
- {业务域 2}

## 外部依赖

| 系统 | 用途 | 协议 | 负责人 |
|------|------|------|--------|
| {system} | {purpose} | {protocol} | {owner} |

## 构建命令

```bash
{build command}
{test command}
{package command}
```

## 环境说明

- 开发环境：{说明}
- 测试环境：{说明}
- 生产环境：{说明}

## 注意事项

- 不提交密钥、token、cookie 或个人路径。
- 未填写的信息应在 Phase 1 作为疑问点确认。
