# Performance Checklist

## 后端性能

- N+1 查询：检查循环内数据库访问和 ORM 懒加载。
- 索引：高频过滤、排序、关联字段应有合适索引。
- 分页：列表接口必须分页或限制返回数量。
- 缓存：只缓存稳定、可失效的数据；记录失效策略。
- 连接池：数据库、HTTP、消息客户端连接池参数合理。
- 超时：外部调用必须设置连接超时和读取超时。
- 批处理：批量写入/读取避免逐条远程调用。
- 大对象：避免一次性加载大文件或大集合到内存。

## 前端性能

- Core Web Vitals：关注 LCP、INP、CLS。
- Bundle：检查过大依赖、重复依赖、未拆包页面。
- 图片：使用合适格式、尺寸、懒加载。
- 渲染：避免不必要 re-render，长列表使用虚拟滚动。
- 网络：避免瀑布请求，必要时合并或预取。
- 缓存：静态资源使用合理缓存头。

## 性能证据

性能结论必须说明：

- 基线：优化前指标或当前可接受阈值。
- 对比：优化后指标或评估结果。
- 采样方式：命令、工具、环境、数据量。
- 风险：未验证场景和潜在瓶颈。

## Phase 5 perf_report 最小结构

`perf_report_v1.md` 至少包含：

- Verdict。
- Scope。
- Mechanical Checks。
- Backend checklist。
- Frontend checklist（如适用）。
- Findings（Severity、Area、Evidence、Recommendation）。
- Must Fix 计数。
- Evidence 路径。
- Required Fixes。
