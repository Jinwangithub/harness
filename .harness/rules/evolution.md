# Self-Evolution 自演化协议

> **TL;DR**: 变更最终交付后，自动分析 gate fail/blocked 模式 → 写入 candidates.md → 人工批准 → 打补丁到规则/技能/校验器。分析失败不阻断变更完成。

本文件是 Harness 自我进化闭环的权威协议。目录结构见 `.harness/evolution/README.md`，分析工具见 `.harness/tools/analyze_failures.py`。

> **边界**：本文件只定义触发条件、分析范围、批准路径和安全检查。Gate 判定见 `.harness/rules/gates.md`，回退路径见 `.harness/rules/rollback.md`。

## 核心原则

1. **Candidate-first**：进化建议先写入 `candidates.md`，仅经人工批准后才合并到规则/技能/校验器。
2. **Deterministic**：分析使用精确的 validator issue code 匹配和计数，不使用 LLM 做"理解"。
3. **Non-blocking**：演化分析失败绝不阻断正常变更流程（输出 WARN 而非 FAIL）。
4. **Backward compatible**：旧变更的 Gate Record 无需修改即可被分析。

## 触发条件

| 时机 | 动作 |
|------|------|
| 变更最终 Gate approved + validator 重验 PASS 后 | Orchestrator 运行 `analyze_failures.py` |
| 无 gate fail/blocked 的变更 | 可跳过 Evolution 步骤 |
| 用户主动请求 | 下一次 Orchestrator 入口执行 |
| Session Startup | 检查 `evolution/candidates.md` 是否有 pending candidates，向用户报告 |

## 分析范围

- **扫描对象**：`INDEX.md` 中状态为 `done` 的所有变更
- **分析字段**：`summary.md` 中 Gate Record 的 Mechanical Gate、Evidence 字段
- **分组维度**：validator issue code（FAIL 级别）
- **模式签名**：排序后的 issue codes 用 `-` 连接
- **最小出现次数**：默认 2 个 distinct changes（可通过 `--min-occurrence` 调整）

## 批准路径

### 审批工作流

```
candidates.md (pending)
  ├── approve → 打补丁到 target file → 保存 snapshot → 追加 log.md
  ├── reject  → 追加 log.md（记录原因）
  └── defer   → 保留候选，标记重新考虑时间
```

### approve 执行步骤

1. 用户明确批准某个 candidate
2. 按 `action_type` 和 `target_file` 打补丁
3. 保存当前 target file 的 snapshot 到 `.harness/evolution/snapshots/{file}_{YYYYMMDD_HHMM}.bak`
4. 追加一行 decision entry 到 `.harness/evolution/log.md`
5. 重新运行 `validate_change.py --all` 验证无回归
6. 记录到 `lessons-learned.md`

### reject/defer 执行步骤

1. 用户明确拒绝或延期
2. 追加一行 decision entry 到 `.harness/evolution/log.md`（含原因）
3. 拒绝的 pattern 不再在后续分析中作为新候选出现

## 安全检查

- 补丁前必须保存 snapshot
- 补丁后必须运行 `validate_change.py --all` 验证
- 不得修改 `.harness/evolution/` 目录以外的文件打补丁时的路径检查
- 一次只能 apply 一个 candidate

## 分析工具 CLI

```bash
python3 .harness/tools/analyze_failures.py \
    [--repo ROOT] \
    [--min-occurrence 2] \
    [--dry-run]
```

- `--dry-run`: 仅输出到 stdout，不写 candidates.md
- Exit code 0 始终（即使发现 patterns），仅工具自身错误时 exit 1
- 发现 patterns 输出 WARN 级别
