# Daily Dashboard

## 手动视图（无插件）
- 打开 `01-Daily/` 目录，按文件名（日期）排序查看最近记录。
- 建议每周创建一条 `weekly-review` 总结。
- 最近日报：
  - [[01-Daily/2026-04-03]]
  - [[01-Daily/2026-04-02]]
  - [[01-Daily/2026-04-01]]
  - [[01-Daily/2026-03-31]]
  - [[01-Daily/2026-03-30]]
- 本周回顾：[[01-Daily/2026-W14-weekly-review]]

## Dataview 片段（可选）
```dataview
TABLE file.name as 日期, tags
FROM "01-Daily"
SORT file.name DESC
LIMIT 30
```
