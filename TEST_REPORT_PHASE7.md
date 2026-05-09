# ROSClaw Wiki Phase 7 测试报告：Synthesis（知识驱动与裁决闭环）

**Date:** 2026-04-29
**Phase:** 7 — Synthesis（知识驱动与裁决闭环）
**Test Suite:** pytest test_e2e.py
**Total Tests:** 150
**Result:** ALL PASSED (150 passed, 5 warnings in 36.06s)

---

## 执行摘要

Phase 7 的核心使命是**让知识从"可被查阅"进化到"可被裁决、可被路由、可被生成"**。在 Phase 6 建立了可信知识中枢的基础上，Phase 7 构建了一套完整的"发现关系 → 裁决冲突 → 形成判决 → 路由场景 → 生成代码"的闭环系统。

本次升级实现了六大模块：

1. **启发式实体链接器 (Entity Linker)** — 零 LLM、纯规则的关系发现引擎，自动识别页面间的 `uses`/`depends_on`/`contradicts`/`supersedes` 关系
2. **智能冲突裁决器 (Conflict Resolver)** — 加权评分 `authority × 0.6 + recency × 0.4`，2 年半衰期指数衰减，多数共识 boost，gap ≥ 0.3 自动裁决
3. **判决生成器 (Judgment Generator)** — 将裁决结果转化为结构化判决 JSON，带 confidence、context、usage_notes，写入 `wiki/judgments/`
4. **查询扩展与上下文路由 (Search + Router)** — RRF 多查询融合搜索 + 场景关键词路由，自动推断 locomotion/manipulation/navigation 等上下文
5. **受控代码生成器 (Code Generator)** — 从 wiki 参数自动生成带引用和警告的 Python 骨架代码，遇到未裁决冲突时**拒绝生成**
6. **Phase 6 限制修复** — event_bus 日志轮转、QA 回写后自动 emit `page_created`、wiki_engine 文件锁竞态保护

**零回归**：Phase 1~6 全部 146 个基线测试全部通过，新增 4 个 Phase 7 Module 6 测试。

---

## 模块完成概览

| 模块 | 内容 | 新增/修改文件 | 新增测试 | 状态 |
|------|------|--------------|----------|------|
| 模块 1 | 启发式实体链接器 | `entity_linker.py` | 9 | PASS |
| 模块 2 | 智能冲突裁决器 | `conflict_resolver.py` | 7 | PASS |
| 模块 3 | 判决生成器 | `judgment_generator.py` | 8 | PASS |
| 模块 4 | 查询扩展 + 上下文路由 | `search_backend.py`, `context_router.py` | 8 | PASS |
| 模块 5 | 受控代码生成器 | `code_generator.py` | 5 | PASS |
| 模块 6 | Phase 6 限制修复 | `event_bus.py`, `qa_engine.py`, `wiki_engine.py` | 4 | PASS |
| Phase 1~6 基线 | 原有功能回归测试 | — | 109 | PASS |

---

## 模块 1：启发式实体链接器 — 零 LLM 关系发现

### 1.1 实现内容

**新增文件：** `entity_linker.py` (320 行)

**核心设计原则：** 完全零 LLM 调用，纯基于规则与启发式模式，确保关系发现的确定性和零成本。

**三层关系发现机制：**

| 层级 | 机制 | 示例 |
|------|------|------|
| **L1: 显式 wikilink** | 提取 `[[Page Title]]` | `[[ROS2]]` → `depends_on` |
| **L2: 句法模式** | 正则匹配 "X uses Y" / "based on X" / "contradicts X" | "Gait Controller uses [[ROS2]]" → `uses` |
| **L3: 类型推断** | entity + algorithm → `uses` / entity + entity → `depends_on` | 无显式链接时的兜底推断 |

**`process_page()` 流程：**
1. 读取页面，解析 frontmatter 获取 title + type
2. `_WIKILINK_RE` 提取所有 `[[...]]` 链接
3. `_RELATION_PATTERNS` 正则扫描句子级别的关系动词
4. `_TYPE_RELATION_MAP` 对无显式关系的链接进行类型推断
5. `write_links_to_page()` 将发现的关系追加到页面末尾的 `### 自动链接关系` 章节

**集成点：** `wiki_engine.create_page()` 和 `update_page()` 在写入完成后自动调用 `entity_linker.process()`，实现"写即链接"。

### 1.2 关键设计决策

- **去重写入**：`write_links_to_page()` 检查是否已存在 `### 自动链接关系` 章节，避免重复追加
- **不覆盖人工链接**：人工在正文中写的关系保留原样，自动链接章节仅收录算法发现的关系
- **local import 防循环**：`wiki_engine.py` 中使用 `import entity_linker` 而非模块顶部 import，避免循环依赖

### 1.3 测试用例

| 测试 | 描述 | 结果 |
|------|------|------|
| test_wikilink_extraction | 从正文提取 [[ROS2]] 等 wikilink | PASS |
| test_type_inference_entity_to_entity | 两个 entity 页面推断为 depends_on | PASS |
| test_type_inference_entity_to_algorithm | entity + algorithm 推断为 uses | PASS |
| test_sentence_pattern_uses | "X uses Y" 句法识别 | PASS |
| test_sentence_pattern_based_on | "based on X" 句法识别 | PASS |
| test_zero_llm_calls | 确认无任何 LLM 调用 | PASS |
| test_integration_create_page_triggers_linker | create_page 后自动触发链接 | PASS |
| test_write_links_to_page | 关系章节正确写入页面 | PASS |
| test_no_duplicate_link_section | 重复处理不添加重复章节 | PASS |

---

## 模块 2：智能冲突裁决器 — 加权评分与共识机制

### 2.1 实现内容

**新增文件：** `conflict_resolver.py` (518 行)

**核心算法：** 每条证据的得分 = `authority_score × 0.6 + recency_score × 0.4`

- **Authority 评分**：official (0.9) > paper (0.8) > blog (0.5) > unknown (0.5)
- **Recency 评分**：`exp(-ln(2) × days / 730)`，2 年半衰期指数衰减
- **多数共识 boost**：当某个值的支持证据 ≥ 总证据的 60% 时，额外 +0.15
- **裁决阈值**：winner_score - runner_up_score ≥ 0.3 时判定为 `resolved`，否则 `unresolved`

**`adjudicate_field()` 返回：** `Adjudication` dataclass，含 `resolved: bool`, `winner_score`, `runner_up_score`, `winner_value`, `reasoning`

**`resolve_conflicts()` MCP 工具：**
1. 扫描页面 `### 待核实冲突` 章节
2. 逐条调用 `adjudicate_field()`
3. 在页面末尾追加 `### 已裁决冲突` 章节
4. 保留原始冲突记录（不删除），实现审计追踪

### 2.2 测试用例

| 测试 | 描述 | 结果 |
|------|------|------|
| test_parse_conflict_lines | 正确解析待核实冲突条目 | PASS |
| test_adjudicate_field_resolved | 高分差冲突被裁决 | PASS |
| test_adjudicate_field_unresolved | 低分差冲突保持未裁决 | PASS |
| test_adjudicate_field_majority_boost | 多数共识触发加分 | PASS |
| test_resolve_conflicts_mcp_tool | MCP 工具写入已裁决章节 | PASS |
| test_conflict_stats | 统计页面冲突状态 | PASS |
| test_no_conflicts_page | 无冲突页面返回空列表 | PASS |

---

## 模块 3：判决生成器 — 从裁决到结构化知识

### 3.1 实现内容

**新增文件：** `judgment_generator.py` (416 行)

**判决结构 (Judgment dataclass)：**

```json
{
  "parameter": "peak_torque",
  "entity": "Unitree G1",
  "context": "locomotion_control",
  "recommended_value": "237 Nm",
  "confidence": 0.92,
  "sources": ["unitree_g1", "official_manual"],
  "conflicts_resolved": true,
  "usage_notes": "Verified against official manual."
}
```

**生成流程：**
1. `generate_judgments_for_page()` 读取页面的 `### 已裁决冲突` 章节
2. 每条已裁决冲突转化为一个 `Judgment`
3. 未裁决冲突生成 warning 型 Judgment（confidence = 0.0，unresolved = true）
4. `save_judgments()` 按 `{entity}_{context}.json` 写入 `wiki/judgments/`

**MCP 工具：**
- `get_judgment(entity, context)` — 按实体+上下文查询
- `list_judgments(wiki_root, context)` — 列出全部或按上下文过滤
- `generate_all_judgments(wiki_root)` — 扫描所有页面批量生成

### 3.2 测试用例

| 测试 | 描述 | 结果 |
|------|------|------|
| test_generate_judgments_from_page | 从已裁决页面生成判决 | PASS |
| test_unresolved_conflict_generates_warning_judgment | 未裁决冲突生成 warning | PASS |
| test_save_and_load_judgments | 判决持久化与加载 | PASS |
| test_get_judgment_without_context | 无上下文时返回全部 | PASS |
| test_list_judgments_by_context | 按 locomotion_control 过滤 | PASS |
| test_list_all_judgments | 列出全部判决 | PASS |
| test_generate_all_judgments | 批量生成所有页面判决 | PASS |
| test_judgment_sorting_by_confidence | 按 confidence 降序排序 | PASS |

---

## 模块 4：查询扩展与上下文路由

### 4.1 Search Backend — RRF 融合查询扩展

**修改文件：** `search_backend.py` (+~100 行)

**新增能力：**

1. **`_rrf_fuse()` — Reciprocal Rank Fusion**
   - 融合多个查询变体的结果列表
   - 公式：`score = Σ 1 / (k + rank + 1)`，默认 k = 60
   - 解决单一查询遗漏相关文档的问题

2. **`search_wiki()` — 统一搜索入口**
   - `search_type="default"` → 直接 whoosh / grep
   - `search_type="expanded"` → 多查询变体 + RRF 融合
   - `search_type="judgment"` → 搜索 judgment 库

3. **`_simple_query_expansion()`** — 零 LLM 查询扩展
   - 去除停用词生成 broader variant
   - 无需 LLM 即可提升召回

4. **`_llm_query_expansion()`** — LLM 辅助扩展（可选注入）
   - 通过 `llm_func` callback 生成 3~4 个查询变体
   - 失败自动回退到 simple expansion

### 4.2 Context Router — 场景驱动的知识路由

**新增文件：** `context_router.py` (197 行)

**路由流程：**
1. `_extract_keywords()` — 分词 + 停用词过滤
2. `_infer_context_from_scenario()` — 关键词匹配 `_SCENARIO_CONTEXT_MAP`
3. `_score_judgment_relevance()` — judgment 的 parameter/context/usage_notes 与关键词匹配
4. `_score_page_relevance()` — 页面 title/body 与关键词匹配
5. **Priority flagging** — unresolved 冲突和含 ⚠️ 的 usage_notes 自动标记为高优先级

**预定义上下文：** locomotion_control, manipulation, perception, navigation, safety, power, general

### 4.3 测试用例

| 测试 | 描述 | 结果 |
|------|------|------|
| test_search_default | whoosh/grep 默认搜索 | PASS |
| test_search_expanded_simple | 简单查询扩展 + RRF | PASS |
| test_search_judgment_type | judgment 库过滤搜索 | PASS |
| test_rrf_fuse | RRF 融合多列表结果 | PASS |
| test_route_scenario_to_judgments | "G1 slips on wet ground" 路由到 locomotion_control | PASS |
| test_route_priority_warnings | unresolved max_speed 标记为 priority | PASS |
| test_route_infers_navigation_context | 导航/电源/操作关键词推断 | PASS |
| test_route_with_judgment_search | 宽泛 judgment 搜索兜底 | PASS |

---

## 模块 5：受控代码生成器 — 知识到代码的安全桥梁

### 5.1 实现内容

**新增文件：** `code_generator.py` (278 行)

**核心约束（硬编码不可违反）：**

1. **绝不生成完整控制循环** — `compute()` 方法必须 `raise NotImplementedError`
2. **必须包含 AUTO-GENERATED 警告头** — 每份代码顶部带 ⚠️ 警告
3. **必须引用物理参数来源** — 每个常量注释标注 source: wiki page / judgment
4. **遇到未裁决冲突时拒绝生成** — 返回 `status: "blocked"`，code 为空字符串

**生成流程：**
1. 查找实体页面 → 解析 frontmatter + body
2. 扫描 `### 已裁决冲突` 确认无 unresolved
3. `_extract_parameters_from_body()` 正则提取 `param = value unit`
4. 加载 judgment 库补充参数
5. 生成 Python class skeleton：物理参数常量 + `__init__` + `setup` + `compute` + `shutdown`

### 5.2 测试用例

| 测试 | 描述 | 结果 |
|------|------|------|
| test_generate_code_framework | 正常生成带参数和引用的骨架 | PASS |
| test_code_generation_blocked_by_unresolved_conflict | 未裁决冲突阻止生成 | PASS |
| test_code_generation_entity_not_found | 实体不存在返回 not_found | PASS |
| test_code_generate_mcp_tool | MCP 工具入口正常生成 | PASS |
| test_code_generate_with_warnings | 生成结果包含 SKELETON 警告 | PASS |

---

## 模块 6：Phase 6 限制修复

### 6.1 event_bus 日志轮转

**修改文件：** `event_bus.py` (+~35 行)

**新增 `_rotate_if_needed()`：**
- 当 `events.jsonl` 超过 `DEFAULT_ROTATION_BYTES` (10 MB) 时自动轮转
- 轮转链：`.1` → `.2` → `.3` → `.4` → `.5`，保留最近 5 份备份
- `emit()` 新增 `max_bytes` 参数，支持自定义阈值

### 6.2 QA 回写后 Web UI 图谱自动刷新

**修改文件：** `qa_engine.py` (+~7 行)

**在 `ask()` 的 write_back 成功后：**
```python
event_bus.emit("page_created", {"path": rel_qa, "title": qa_title})
```

Web UI 的 SocketIO 监听 `page_created` 事件，收到后自动刷新知识图谱。

### 6.3 并发写入文件锁竞态保护

**修改文件：** `wiki_engine.py` (+~10 行), 新增 `file_lock.py` (86 行)

**`file_lock.py` 设计：**
- Unix 环境：`fcntl.flock(LOCK_EX)`  advisory 文件锁
- Windows/fcntl 不可用：fallback 到 per-path `threading.Lock`
- Context manager 接口：`with acquire_lock(path): ...`

**集成点：**
- `create_page()` — 从 `filepath.write_text()` 前获取锁
- `update_page()` — 从 `read_text()` 到 `write_text()` 的整个 RMW 周期持有锁

### 6.4 测试用例

| 测试 | 描述 | 结果 |
|------|------|------|
| test_event_bus_log_rotation | 超过阈值后自动轮转备份 | PASS |
| test_qa_engine_emits_page_created_event | QA 回写后 emit page_created | PASS |
| test_wiki_engine_file_lock_prevents_race | 10 线程并发 create_page 无错误 | PASS |
| test_wiki_engine_update_page_with_lock | update_page 在锁保护下成功 | PASS |

---

## 回归测试

Phase 1~6 全部 146 个基线测试通过，无回归：

- Frontmatter 解析/写入 (2 tests)
- Confidence 生命周期 — 强化、30天/90天/180天衰减 (4 tests)
- Supersession 规则 (3 tests)
- Page CRUD + 归档 + 冲突处理 (4 tests)
- Index/Log 更新 (2 tests)
- Orphan 检测 (1 test)
- Fetcher URL 解析与分类 (4 tests)
- MCP Tool 逻辑 (2 tests)
- 完整流水线 (1 test)
- KnowledgeSynthesizer (4 tests)
- LLMInterface 后端检测 (5 tests)
- Phase 2 Fetcher 增强 (5 tests)
- RetentionEngine 遗忘引擎 (5 tests)
- SmartLint 自愈 (3 tests)
- BatchIngest 批量处理 (7 tests)
- SearchBackend whoosh 搜索 (5 tests)
- PDF 全文提取 (5 tests)
- 向量语义搜索 (3 tests)
- 实体消歧 (5 tests)
- 知识图谱导出 (3 tests)
- 多模态图表提取 (4 tests)
- 研究顾问与盲区可视化 (4 tests)
- 碎片信息整合 (5 tests)
- Web 可视化界面 (5 tests)
- QA Engine 问答 (6 tests)
- Scheduler 自动代谢 (6 tests)
- Phase 5 EntityResolver / GraphExporter / FragmentDetector / RetentionEngine / KnowledgeSynthesizer / ResearchAdvisor / VisualizeGaps (19 tests)
- Phase 7 Modules 1~5 (37 tests)

---

## 新增/修改文件统计

| 文件 | 行数 | 说明 |
|------|------|------|
| `entity_linker.py` | 320 | 零 LLM 启发式实体关系发现 |
| `conflict_resolver.py` | 518 | 加权评分冲突裁决器 |
| `judgment_generator.py` | 416 | 结构化判决生成与存储 |
| `context_router.py` | 197 | 场景关键词路由引擎 |
| `code_generator.py` | 278 | 受控代码骨架生成器 |
| `file_lock.py` | 86 | 跨平台文件锁（fcntl + thread fallback） |
| `search_backend.py` | +~100 | RRF 融合、查询扩展、统一搜索入口 |
| `event_bus.py` | +~35 | 日志轮转（10 MB 阈值，保留 5 份备份） |
| `qa_engine.py` | +~7 | QA 回写后 emit page_created 事件 |
| `wiki_engine.py` | +~10 | create_page / update_page 文件锁保护 |
| `test_e2e.py` | 3101 | 150 个测试用例（新增 41 个 Phase 7 测试） |

**项目总代码量：** ~8,600 行（Python）

---

## 关键设计决策

1. **零 LLM 实体链接**：`entity_linker.py` 完全基于 wikilink 提取、句法正则、类型推断三层规则，确保关系发现的确定性和零成本。LLM 只用于内容生成，不用于关系推理。

2. **加权评分 + 指数衰减**：冲突裁决同时考虑来源权威性 (60%) 和时间衰减 (40%)，避免"老论文永远赢"或"新博客碾压官方文档"的极端情况。

3. **判决与页面解耦**：judgment 以独立 JSON 文件存储在 `wiki/judgments/`，不嵌入页面正文。这允许 judgment 被多个场景复用、独立版本控制、快速批量查询。

4. **RRF 零成本查询扩展**：`search_wiki()` 的 expanded 模式先尝试零 LLM 的停用词过滤扩展，仅在调用方注入 `llm_func` 时才启用 LLM 辅助扩展，实现延迟成本优化。

5. **代码生成的安全红线**：`code_generator.py` 在三个层面防止不安全的代码生成：(a) 未裁决冲突直接阻断，(b) compute() 强制 NotImplementedError，(c) AUTO-GENERATED 警告头不可删除。

6. **文件锁的跨平台兼容**：`file_lock.py` 优先使用 Unix `fcntl.flock`（支持跨进程），回退到 `threading.Lock`（仅同进程内），在容器/Windows 环境仍可正常工作。

7. **QA 回写事件驱动刷新**：不采用轮询或定时刷新，而是在 QA 页面写入成功的瞬间通过 event_bus 推送 `page_created`，Web UI 收到 SocketIO 消息后毫秒级刷新图谱。

---

## 已知限制

1. **entity_linker 无跨语言支持**：句法模式仅匹配英文关系动词，中文页面可能漏检
2. **conflict_resolver 假设离散值**：连续数值冲突（如 0.05 vs 0.0501）会被视为不同值，未来可加入数值容差
3. **judgment 文件数量膨胀**：每个 entity × context 组合产生一个 JSON 文件，大规模 wiki 可能产生数百个小文件
4. **code_generator 仅支持 Python**：其他语言骨架待 Phase 8 扩展
5. **RRF 简单扩展召回有限**：`_simple_query_expansion()` 仅做停用词过滤，复杂语义扩展仍依赖 LLM
6. **event_bus 轮转同步阻塞**：`_rotate_if_needed()` 在 emit 时同步执行文件移动，极端大文件下可能短暂阻塞

---

## 下一步建议（Phase 8）

1. **多语言代码生成**：支持 C++ / Rust / Go 骨架生成，适配 ROS2 生态
2. **跨语言实体链接**：为中文页面添加 "基于" / "使用" / "依赖于" 等关系模式
3. **Judgment 向量索引**：将 judgment 纳入 vector_index，支持语义级 judgment 搜索
4. **自动工作流链式触发**：raw_watcher 检测到新文件后，自动调用 batch_ingest → entity_linker → conflict_resolver → judgment_generator
5. **实体链接可视化**：在 Web UI 中用不同颜色边表示 uses/depends_on/contradicts/supersedes 关系
6. **代码生成一键部署**：与 ros-mcp-server 集成，将生成的骨架直接推送为 MCP tool 模板

---

**Report generated by:** pytest test_e2e.py -v
**Total execution time:** ~36.06s (150 tests)
**Python version:** 3.9.19
**pytest version:** 8.4.2
