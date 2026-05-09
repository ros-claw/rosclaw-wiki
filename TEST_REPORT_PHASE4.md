# ROSClaw Wiki Phase 4 测试报告

**Date:** 2026-04-28
**Phase:** 4 — Cognition（认知升级）
**Test Suite:** pytest test_e2e.py
**Total Tests:** 69
**Result:** ALL PASSED (69 passed, 5 warnings in 14.64s)

---

## 执行摘要

Phase 4 将 ROSClaw Wiki 从"索引器"升级为"理解器"。本次升级实现了四大认知能力：

1. **PDF 全文提取** — 三层优先级提取（PaddleOCR API → PyMuPDF → pdfplumber），支持环境变量配置 API Token
2. **向量语义搜索** — 基于 all-MiniLM-L6-v2 的本地 Embedding，支持增量索引与 RRF 混合排序
3. **实体消歧** — whoosh 检索 + difflib 相似度计算，自动合并高相似度实体
4. **知识图谱导出** — 解析 [[wikilink]] 语法，输出 json / sigma / cytoscape 三种格式

**零回归**：Phase 1~3 全部 53 个基线测试全部通过。

---

## 模块完成概览

| 模块 | 内容 | 新增测试 | 状态 |
|------|------|----------|------|
| 模块 1 | PDF 全文提取器 (pdf_extractor.py) | 5 | PASS |
| 模块 2 | 向量语义搜索 (vector_index.py) | 3 | PASS |
| 模块 3 | 实体消歧器 (entity_resolver.py) | 5 | PASS |
| 模块 4 | 知识图谱导出 (graph_exporter.py) | 3 | PASS |
| Phase 1~3 基线 | 原有功能回归测试 | 53 | PASS |

---

## 模块 1：PDF 全文提取器

### 1.1 实现内容

**新增文件：** `pdf_extractor.py` (346 行)

三层优先级提取策略：

| 优先级 | 引擎 | 特点 | 触发条件 |
|--------|------|------|----------|
| 1 | PaddleOCR API | 版面感知，返回结构化 Markdown | `PADDLEOCR_API_TOKEN` 环境变量已设置 |
| 2 | PyMuPDF (fitz) | 本地快速提取 | 库已安装且 API 未配置/失败 |
| 3 | pdfplumber | 纯 Python，零依赖编译 | 前两者均失败时回退 |

**API 配置（环境变量）：**
```bash
export PADDLEOCR_API_URL="https://ucy1r2qeec5ey7ue.aistudio-app.com/layout-parsing"
export PADDLEOCR_API_TOKEN="your-token-here"
```

**Section 检测：**
- 正则匹配学术论文章节标题：`Abstract`, `Introduction`, `Methods`, `Experiments`, `Results`, `Conclusion`, `References`
- 支持多种格式：`I. INTRODUCTION`, `2 Methods`, `## Methods` (Markdown)
- 启发式过滤：要求标题前为换行或字符串开头，或为全大写，或带罗马数字前缀

**文本清洗：**
- 移除页码和重复的页眉/页脚
- 合并断行连字符（hyphenated line breaks）
- 合并段落内的换行，保留段落间空行

### 1.2 测试用例

| 测试 | 描述 | 结果 |
|------|------|------|
| test_extract_pdf_text | 使用 PyMuPDF 提取测试 PDF 全文 | PASS |
| test_extract_pdf_sections | Section 检测（Abstract / Methods / Conclusion） | PASS |
| test_extract_pdf_fallback_to_abstract | 无 Methods section 时回退到 abstract | PASS |
| test_read_source_text_fulltext | `read_source_text` 优先使用全文提取 | PASS |
| test_api_extractor_availability | API Token 配置检测 | PASS |

### 1.3 已知限制

- PaddleOCR API 对大型 PDF（>20MB）可能超时，建议分块上传或先用 PyMuPDF 处理
- API 返回 Markdown 格式的标题（`## Methods`），Section 检测正则已适配

---

## 模块 2：向量语义搜索

### 2.1 实现内容

**新增文件：** `vector_index.py` (235 行)

**Embedding 模型：**
- `sentence-transformers/all-MiniLM-L6-v2` (384 维)
- 本地运行，无需外部 API，零网络依赖
- 惰性单例加载（`_get_model()`），首次调用时初始化

**核心 API：**

| 函数 | 说明 |
|------|------|
| `build_vector_index(wiki_root)` | 全量重建索引，扫描所有 `.md` 文件 |
| `index_page(wiki_root, rel_path)` | 增量更新单页（删除+插入），无需重建全库 |
| `search_semantic(wiki_root, query, top_k)` | 纯语义搜索，余弦相似度排序 |
| `search_hybrid(wiki_root, query, top_k, k)` | RRF 混合搜索，融合 whoosh + semantic |

**RRF 混合搜索（Reciprocal Rank Fusion）：**
```
score(doc) = sum_i( 1 / (k + rank_i(doc)) )
```
- `k=60`（默认常数）
- whoosh 全文排名 + semantic 向量排名 双路融合
- 解决"关键词匹配不到但语义相关"的问题

**存储格式：**
- `wiki/.vector_index/embeddings.npy` — NumPy 矩阵 (N x 384)
- `wiki/.vector_index/docs.json` — 文档元数据列表

### 2.2 测试用例

| 测试 | 描述 | 结果 |
|------|------|------|
| test_build_vector_index | 全量索引重建，验证 embeddings.npy 生成 | PASS |
| test_index_page_incremental | 增量索引单页后搜索 | PASS |
| test_search_hybrid_rrf | RRF 混合搜索排序正确性 | PASS |

### 2.3 MCP 集成

`mcp_wiki_server.py` 中 `search_wiki` 工具新增 `search_type` 参数：
- `"keyword"` — whoosh 全文搜索（默认）
- `"semantic"` — 纯向量语义搜索
- `"hybrid"` — RRF 混合排序

---

## 模块 3：实体消歧器

### 3.1 实现内容

**新增文件：** `entity_resolver.py` (176 行)

**消歧策略：**

| 相似度区间 | 动作 | 说明 |
|-----------|------|------|
| >= 0.9 | **自动合并** | 直接定位到已有页面，追加内容 |
| 0.6 ~ 0.9 | **LLM 审核** | 返回候选列表，由 LLM 判断是否同一实体 |
| < 0.6 | **创建新页** | 无匹配，全新创建 |

**实现细节：**
- 候选检索：whoosh 搜索（前 10 条）+ 全库文件名扫描（兜底）
- 相似度计算：`difflib.SequenceMatcher(None, name_a.lower(), name_b.lower()).ratio()`
- slug 精确匹配：若文件名相同，相似度强制提升至 0.95

**全局去重扫描：**
- `entity_dedup_report(wiki_root)` — O(N^2) 全对比较，输出潜在重复对
- `write_dedup_report()` — 生成 Markdown 报告到 `data/quality_reports/dedup_candidates.md`

### 3.2 与知识合成器集成

`knowledge_synthesizer.py` 的 `synthesize()` 方法在定位页面前先调用 `resolve_entity()`：
- 若 `action == "merge"`，直接定位到已有页面进行增量更新
- 若 `action == "llm_required"`，记录日志等待人工/LLM 审核
- 避免同一实体因来源不同而被重复创建

### 3.3 测试用例

| 测试 | 描述 | 结果 |
|------|------|------|
| test_find_candidate_entities_exact_match | whoosh + 文件名双路检索精确匹配 | PASS |
| test_resolve_entity_merge | 相似度 >0.9 时触发自动合并 | PASS |
| test_resolve_entity_create_new | 无匹配时返回 create_new | PASS |
| test_entity_dedup_report | 全库去重扫描生成报告 | PASS |
| test_knowledge_synthesizer_merge | 合成器自动调用消歧并合并实体 | PASS |

---

## 模块 4：知识图谱导出

### 4.1 实现内容

**新增文件：** `graph_exporter.py` (166 行)

**功能：** 解析所有 wiki 页面的 YAML frontmatter 和 `[[Page Name]]` wikilink，导出为三种图格式。

**支持的格式：**

| 格式 | 输出文件 | 用途 |
|------|----------|------|
| json | `nodes.json` + `edges.json` | 通用数据交换 |
| sigma | `sigma.json` | Sigma.js 可视化 |
| cytoscape | `cytoscape.json` | Cytoscape.js / Obsidian 插件 |

**节点属性：**
- `id`, `label`, `type`, `confidence`, `tags`, `path`

**边属性：**
- `source`, `target`, `type: "wikilink"`

**过滤：**
- 排除 `index.md`, `log.md`, `Admin_Dashboard.md`
- 跳过重复节点（基于 page_id）
- 跳过重复边（基于 (source, target) 元组）

### 4.2 测试用例

| 测试 | 描述 | 结果 |
|------|------|------|
| test_export_graph_json | 导出 json 格式，验证节点/边数量 | PASS |
| test_export_graph_sigma | 导出 sigma.js 格式，验证 key/attributes 结构 | PASS |
| test_export_graph_cytoscape | 导出 cytoscape 格式，验证 data 结构 | PASS |

### 4.3 MCP 集成

`mcp_wiki_server.py` 新增 `wiki_export_graph(fmt)` 工具，支持通过 MCP 调用导出图谱。

---

## Phase 4 核心验证：全文 vs 摘要知识提取

使用论文 `2602.19308` (WildOS) 进行定量对比：

| 指标 | 摘要提取 | 全文提取 | 增益 |
|------|----------|----------|------|
| 实体数 | 8 | 20 | **2.5x** |
| 参数数 | 9 | 40 | **4.4x** |
| 能力数 | 16 | 33 | 2.1x |
| 关系数 | 16 | 37 | 2.3x |

**结论：** PDF 全文提取是深度知识抽取的必需能力。Phase 4 的三层提取策略确保了在不同环境下的可用性。

详细报告：`data/quality_reports/fulltext_vs_abstract.md`

---

## 回归测试

Phase 1~3 全部 53 个基线测试通过，无回归：

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
- Phase 2 Fetcher 增强 (4 tests)
- RetentionEngine 遗忘引擎 (5 tests)
- SmartLint 自愈 (3 tests)
- BatchIngest 批量处理 (3 tests)
- SearchBackend whoosh 搜索 (5 tests)

---

## 新增/修改文件统计

| 文件 | 行数 | 说明 |
|------|------|------|
| `pdf_extractor.py` | 346 | PDF 全文提取（三层引擎 + Section 检测 + 文本清洗） |
| `vector_index.py` | 235 | 向量语义搜索（all-MiniLM-L6-v2 + RRF 混合） |
| `entity_resolver.py` | 176 | 实体消歧（whoosh + difflib + 三级阈值） |
| `graph_exporter.py` | 166 | 知识图谱导出（json / sigma / cytoscape） |
| `compare_fulltext_abstract.py` | 275 | 全文 vs 摘要对比验证工具 |
| `mcp_wiki_server.py` | 764 | MCP 服务端（新增 semantic/hybrid 搜索、图谱导出） |
| `knowledge_synthesizer.py` | 314 | 知识合成器（集成 resolve_entity 自动合并） |
| `test_e2e.py` | 1,162 | 69 个测试用例（新增 16 个 Phase 4 测试） |
| `wiki_engine.py` | 473 | 核心引擎 |
| `search_backend.py` | 177 | whoosh 全文搜索 |
| `retention_engine.py` | 175 | 置信度衰减 |
| `batch_ingest.py` | 390 | 批量摄取 |
| `llm_interface.py` | 184 | LLM 抽象层 |
| `rosclaw_fetch.py` | 514 | 资源抓取器 |

**项目总代码量：** ~5,351 行（Python）

---

## 关键设计决策

1. **三层 PDF 提取优先级**：PaddleOCR API（最佳质量）→ PyMuPDF（本地快速）→ pdfplumber（零编译依赖）。确保在任何环境下至少有一种提取方式可用。
2. **本地 Embedding 模型**：使用 `all-MiniLM-L6-v2` 而非外部 API，零网络依赖、零 Token 成本、384 维轻量模型。
3. **RRF 混合搜索**：结合 whoosh 的关键词精确匹配与向量的语义匹配，解决"同义词不匹配"和"字面匹配但语义无关"两类问题。
4. **三级实体消歧**：>0.9 自动合并、0.6~0.9 LLM 审核、<0.6 新建。避免重复页面同时减少误合并。
5. **增量向量索引**：`index_page()` 使用删除+插入策略，无需每次写入后重建全库索引。

---

## 已知限制

1. **PaddleOCR API 大文件超时**：>20MB 的 PDF 在 base64 编码后 payload 过大，建议分块或预处理压缩
2. **whoosh 单进程限制**：不适合高并发写入，当前为单机 Obsidian 兼容 wiki，足够
3. **向量索引存储**：embeddings.npy 为二进制 NumPy 格式，跨 Python 版本兼容性良好但不支持外部工具直接读取
4. **实体消歧 O(N^2)**：全局去重扫描在页面数 >1000 时会变慢，建议定期而非实时运行

---

## 下一步建议（Phase 5）

1. **Web UI**：基于 llmwiki 或 llm_wiki 参考项目，构建前端界面展示知识图谱
2. **多模态提取**：从 PDF 中提取图片、表格，生成结构化数据（依赖 PaddleOCR API 的 chartRecognition）
3. **增量 PDF 处理**：大文件分块上传 API，支持断点续传
4. **自动化工作流**：基于 retention_engine 的置信度衰减，自动触发 LLM 审核低置信度页面

---

**Report generated by:** pytest test_e2e.py -v
**Total execution time:** ~14.64s (69 tests)
**Python version:** 3.9.19
**pytest version:** 8.4.2
