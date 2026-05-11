# ROSClaw Wiki 前后端适配指南

> **版本**：v1.1  
> **面向**：前端开发人员（Vercel / Next.js）  
> **后端地址**：`https://api.rosclaw.io`  
> **前端地址**：`https://www.rosclaw.io`

---

## 一、架构总览

```
┌─────────────────┐      OAuth 登录       ┌─────────────────┐
│   Vercel 前端    │ ◄───────────────────► │ Google/GitHub   │
│  (Next.js)      │                       │   OAuth         │
└────────┬────────┘                       └─────────────────┘
         │
         │  1. POST /wiki/v1/auth/exchange   (传入 email)
         │  2. 获得 API Key，存入 localStorage
         │  3. 后续所有请求带 X-API-Key header
         ▼
┌─────────────────┐
│  api.rosclaw.io │  ← FastAPI + SeekDB (pyseekdb) + SQLite + Redis
│  (后端 API)      │
└─────────────────┘
```

**关键设计**：
- 前端 OAuth 只负责"身份确认"，真正的 API 认证使用后端颁发的 `X-API-Key`
- 搜索后端使用 **SeekDB**（pyseekdb），健康检查 `GET /v1/health` 会返回 `"backend": "seekdb"`
- SQLite (`seekdb_compat.db`) 只用于关系型查询（auth、usage、entity_graph）
- 多设备批量同步通过 `batch_sync.py` + R2 完成（见第七节）

---

## 二、认证流程

### Step 1: 用户 OAuth 登录

使用 NextAuth.js（Vercel 已配置 Google/GitHub OAuth）。登录成功后获取用户 `email`。

### Step 2: 换取 API Key

```typescript
// 登录成功后立即调用
const res = await fetch("https://api.rosclaw.io/wiki/v1/auth/exchange", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: user.email,      // 来自 NextAuth session
    name: user.name,        // 可选
    provider: "google",     // 可选
  }),
});

const data = await res.json();
if (data.api_key) {
  localStorage.setItem("rosclaw_api_key", data.api_key);
}
```

**说明**：
- 同一个 email 第二次调用会返回 `exists: true`，不会生成新 key
- 前端应始终优先使用 localStorage 中的 key，仅在首次登录时保存
- API Key 格式：`rw_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`（46 字符）

### Step 3: 所有 API 请求带 Key

```typescript
const API_KEY = localStorage.getItem("rosclaw_api_key");

const res = await fetch("https://api.rosclaw.io/wiki/v1/auth/me", {
  headers: { "X-API-Key": API_KEY },
});
```

---

## 三、端点速查表

| 端点 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/v1/health` | GET | 无 | 健康检查（返回 `backend: "seekdb"` 表示正常） |
| `/wiki/v1/hub/stats` | GET | 无 | Wiki 总览 + 关键词图谱数据 |
| `/v1/search` | POST | X-API-Key | 搜索（支持 hybrid/semantic/keyword/judgment/expanded） |
| `/v1/search/hybrid` | POST | X-API-Key | 高精度混合搜索 |
| `/v1/judgments/{entity}` | GET | X-API-Key | 物理判据 |
| `/v1/insights` | GET | X-API-Key | 知识洞察 |
| `/wiki/v1/auth/exchange` | POST | 无 | OAuth email → API Key |
| `/wiki/v1/auth/me` | GET | X-API-Key | 用户信息 + 用量 |
| `/wiki/v1/usage?days=30` | GET | X-API-Key | 用量统计 |
| `/wiki/v1/upload/request` | POST | X-API-Key | 申请 R2 预签名上传 URL |
| `/wiki/v1/upload/complete` | POST | X-API-Key | 通知上传完成 |

> **注意**：所有 `/v1/...` 端点也支持 `/wiki/v1/...` 前缀（已配置别名）。前端统一用 `/wiki/v1/...` 即可。

---

## 四、端点详细说明

### 4.1 `GET /v1/health` — 健康检查

**无需认证**

**响应**：
```json
{
  "status": "ok",
  "backend": "seekdb",
  "wiki_pages": 804,
  "judgments": 1024
}
```

**前端展示建议**：
- 右上角显示一个小圆点：绿色 = `backend === "seekdb"`，红色/黄色 = 其他
- 悬浮提示显示 `wiki_pages` 和 `judgments` 数量
- **注意**：如果显示 `"backend": "sqlite_compat"`，说明 SeekDB 连接异常，应提示"搜索服务降级中"

---

### 4.2 `GET /wiki/v1/hub/stats` — Wiki 总览（公开）

**无需认证**

**响应**：
```json
{
  "status": "ok",
  "wiki_name": "ROSClaw Wiki",
  "description": "具身智能物理常识中枢...",
  "global_stats": {
    "total_pages": 804,
    "total_wikilinks": 7650,
    "total_judgments": 1024,
    "total_code_graph_nodes": 69668,
    "total_code_graph_edges": 672112,
    "robots_covered": 4,
    "entities_covered": 0,
    "causal_chains": 0,
    "last_updated": "2026-05-10 00:04:49"
  },
  "keywords": [...],
  "keyword_categories": { "entity": [...], "concept": [...], ... }
}
```

**实际数据说明**（截至 2026-05-11）：
| 字段 | 实际值 | 前端展示建议 |
|------|--------|-------------|
| total_pages | 804 | 正常展示 |
| total_wikilinks | 7650 | 正常展示 |
| total_judgments | 1024 | 正常展示 |
| total_code_graph_nodes | 69668 | ⚠️ 含 google-research 通用代码噪音，后续会过滤 |
| total_code_graph_edges | 672112 | ⚠️ 同上 |
| robots_covered | 4 | 正常展示 |
| entities_covered | 0 | **建议显示"待构建"而非 0**，因为 entity_graph 表尚未填充 |
| causal_chains | 0 | **建议显示"待构建"而非 0**，因为 physical_ontology.json 尚未填充 |

---

### 4.3 `POST /v1/search` — 搜索

**请求头**：`X-API-Key: rw_xxx`  
**请求体**：
```json
{
  "query": "unitree g1 humanoid",
  "search_type": "hybrid",
  "top_k": 5
}
```

**search_type 选项**：
| 类型 | 说明 | 适用场景 |
|------|------|---------|
| `keyword` | 关键词匹配（BM25） | 精确查找术语 |
| `semantic` | 语义向量搜索 | 同义词、概念相关 |
| `hybrid` | 关键词 + 语义混合（默认） | 通用搜索 |
| `expanded` | 混合 + LLM 查询扩展 | 需要深度理解时 |
| `judgment` | 判据搜索 | 查找物理参数建议 |

**响应**：
```json
{
  "status": "ok",
  "query": "unitree g1 humanoid",
  "results": [
    {
      "file_path": "unitree_g1",
      "title": "Unitree-G1",
      "snippet": "Humanoid robot by Unitree.\n\n## Parameters...",
      "score": 1.0
    }
  ],
  "count": 5
}
```

---

### 4.4 `POST /wiki/v1/auth/exchange` — 换取 API Key

**请求**：
```json
{
  "email": "user@example.com",
  "name": "Alice",
  "provider": "google"
}
```

**响应（首次）**：
```json
{
  "status": "ok",
  "exists": false,
  "api_key": "rw_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "tenant_id": "user@example.com",
  "plan": "free",
  "created_at": "2026-05-10T12:00:00"
}
```

**响应（已存在）**：
```json
{
  "status": "ok",
  "exists": true,
  "tenant_id": "user@example.com",
  "plan": "free",
  "message": "API key already exists."
}
```

---

### 4.5 `GET /wiki/v1/auth/me` — 用户信息

**请求头**：`X-API-Key: rw_xxx`

**响应**：
```json
{
  "status": "ok",
  "user": {
    "id": "user@example.com",
    "email": "user@example.com",
    "plan": "free",
    "created_at": "2026-05-10T12:00:00"
  },
  "api_key": "rw_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "api_key_masked": "rw_****...****abcd",
  "usage_today": 15,
  "daily_limit": 100
}
```

---

### 4.6 `POST /wiki/v1/upload/request` + `/wiki/v1/upload/complete` — 批量提交

用于多设备炼化结果的提交。设备端打包后上传到 R2，生产服务器合并。

**Step 1: 申请上传 URL**
```typescript
const res = await fetch("https://api.rosclaw.io/wiki/v1/upload/request", {
  method: "POST",
  headers: { "X-API-Key": API_KEY, "Content-Type": "application/json" },
  body: JSON.stringify({
    file_name: "batch_vln.tar.gz",
    file_size: 52428800,
    wiki_name: "batch_vln"
  }),
});
// { upload_id: "...", presigned_url: "...", expires_in: 3600 }
```

**Step 2: 直传 R2**
```typescript
await fetch(presigned_url, { method: "PUT", body: tarBlob });
```

**Step 3: 通知完成**
```typescript
await fetch("https://api.rosclaw.io/wiki/v1/upload/complete", {
  method: "POST",
  headers: { "X-API-Key": API_KEY, "Content-Type": "application/json" },
  body: JSON.stringify({ upload_id }),
});
```

---

## 五、错误处理

| HTTP 状态码 | 含义 | 前端处理 |
|------------|------|---------|
| 400 | 请求参数错误 | 提示用户检查输入 |
| 401 | API Key 无效或缺失 | 清除 localStorage，跳转登录 |
| 429 | 频率限制 | 显示"请求过于频繁，请稍后" |
| 500 | 服务器内部错误 | 显示"服务暂时不可用" |
| 502/503 | 后端服务未就绪 | 显示"服务启动中，请稍候"（常见于 seekdb 启动阶段） |

**通用错误响应格式**：
```json
{"detail": "错误描述"}
```

---

## 六、前端开发 Checklist

- [ ] OAuth 登录成功后调用 `/wiki/v1/auth/exchange`
- [ ] API Key 存入 localStorage（key: `rosclaw_api_key`）
- [ ] 封装 API client，自动带 `X-API-Key` header
- [ ] 401 时自动清除 key 并跳转登录
- [ ] Profile 页面：`/wiki/v1/auth/me` + Show/Copy Key
- [ ] Dashboard 页面：`/wiki/v1/usage?days=30` + 图表
- [ ] Hub 页面：`/wiki/v1/hub/stats` + 关键词图谱
- [ ] **Hub 页面：0 值字段显示"待构建"而非数字 0**
- [ ] **搜索页面：提供 search_type 选择器（keyword/semantic/hybrid/expanded/judgment）**
- [ ] **顶部状态栏：显示 `/v1/health` 的 backend 状态（seekdb = 绿点）**
- [ ] 所有 API 请求统一走 `https://api.rosclaw.io`

---

## 七、多设备批量同步（Batch Sync）

**背景**：多个设备可以在本地炼化知识库，通过 R2 提交到生产服务器合并。

**前端无需实现设备端逻辑**，但应在管理后台提供：
1. **提交记录列表**：显示各设备的 `batch_name`、`device_id`、`status`（pending/completed/merged）
2. **预览变更**：调用 `batch_sync.py production-merge --dry-run` 的结果
3. **一键合并**：触发生产服务器合并（管理员权限）

详见后端 `batch_sync.py` 和 SKILL.md。

---

## 八、本地开发

如需本地联调，在 `.env.local` 中：
```
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

后端 CORS 已配置允许 `http://localhost:3000` 和 `http://localhost:5173`。
