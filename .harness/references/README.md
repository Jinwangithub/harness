# 参考清单

本目录存放 Harness Engineering 的本地参考清单文件。
这些清单是仓库内置规范，不依赖外部插件缓存；团队 clone 仓库后即可直接使用。

## 清单列表

| 文件 | 用途 | 本地路径 |
|------|------|----------|
| `testing-patterns.md` | 测试结构、命名、Mock 模式、反模式 | references/testing-patterns.md |
| `security-checklist.md` | 安全检查清单、OWASP Top 10 | references/security-checklist.md |
| `performance-checklist.md` | Core Web Vitals、前后端性能清单 | references/performance-checklist.md |
| `accessibility-checklist.md` | 键盘导航、屏幕阅读器、ARIA | references/accessibility-checklist.md |
| `orchestration-patterns.md` | Orchestrator/Skill 编排模式目录 | references/orchestration-patterns.md |

## 使用方式

Orchestrator 在 Phase 5（编码评审）、Phase 6（测试编写）、Phase 7（测试评审）和按需专项检查时查阅对应的参考清单。不需要预加载，仅在需要时读取。

### 快速引用
- 安全审查 → `security-checklist.md`
- 性能审查 → `performance-checklist.md`
- 测试编写 → `testing-patterns.md`
- 无障碍审查 → `accessibility-checklist.md`
- 编排设计 → `orchestration-patterns.md`
