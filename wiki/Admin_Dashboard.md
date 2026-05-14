---
id: admin_dashboard
type: index
tags: [admin, dashboard, monitoring]
confidence: 1.0
created_at: "2026-04-27"
last_reinforced: "2026-04-27"
---

# ROSClaw Wiki 管理看板

> 本文件专为 Obsidian Dataview 插件设计。启用 Dataview 后，以下查询块将自动渲染为实时列表。

---

## 低置信度知识（需复核）

```dataview
LIST FROM "wiki"
WHERE confidence < 0.5
SORT confidence ASC
```

---

## 过期知识（超过30天未强化）

```dataview
LIST FROM "wiki"
WHERE date("now") - date(last_reinforced) > dur(30 days)
SORT last_reinforced ASC
```

---

## 孤立页面（未被引用）

```dataview
LIST FROM "wiki"
WHERE length(file.inlinks) = 0
  AND file.name != "index"
  AND file.name != "log"
  AND file.name != "Admin_Dashboard"
```

---

## 知识库统计快照

| 指标 | 说明 |
|------|------|
| 总页面数 | 使用 Dataview `length(file.inlinks)` 观察 |
| 平均置信度 | 低置信度页面优先复核 |
| 最近摄入 | 查看 `wiki/log.md` |
| 待核实冲突 | 搜索包含 `### 待核实冲突` 的页面 |

---

## 维护清单

- [ ] 低置信度页面已复核
- [ ] 过期知识已更新或标记
- [ ] 孤立页面已补充 `wikilink ⚠️`
- [ ] `index.md` 与目录结构同步
- [ ] `log.md` 无异常报错
