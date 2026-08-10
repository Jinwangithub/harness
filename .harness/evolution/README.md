# Self-Evolution 自演化目录

> **TL;DR**: Harness 自动分析 gate fail/blocked 模式 → 生成演化候选 → 人工批准 → 打补丁到规则/技能/校验器。Candidate-first：批准前仅写 candidates.md，不修改规则。

## 目录结构

| 文件 | 用途 |
|------|------|
| `candidates.md` | 演化候选池：分析工具输出 + Human Evolution Approval |
| `log.md` | Append-only 演化决策日志：批准/拒绝/延期记录 |

## Candidate-first 策略

1. `analyze_failures.py` 扫描已完成变更的 Gate Record，按 validator issue code 分组识别失败模式
2. 新模式写入 `candidates.md`（增量合并，保留已有 Human Approval 决策）
3. 用户审查后批准 (approve)、拒绝 (reject) 或延期 (defer)
4. 批准后按建议的 action_type 打补丁到对应 target file
5. 记录到 `log.md`

## 触发条件

- 变更最终 Gate approved + validator PASS 后自动触发
- 无 gate fail/blocked 的变更可跳过
- 用户主动请求时触发
- Session Startup 检查 pending candidates

## 相关规则

- `.harness/rules/evolution.md` — 自演化协议规则
- `.harness/tools/analyze_failures.py` — 核心分析工具
