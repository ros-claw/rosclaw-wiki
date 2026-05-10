# ROSClaw Wiki 前后端适配指南

> **版本**：v1.0  
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
│  api.rosclaw.io │  ← FastAPI + SQLite/SeekDB + Redis
│  (后端 API)      │
└─────────────────┘
```

**关键设计**：前端 OAuth 只负责"身份确认"，真正的 API 认证使用后端颁发的 `X-API-Key`。这样前后端解耦，后端不依赖任何 OAuth provider。

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
- API Key 格式：`rw_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`（34 字符）

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
| `/wiki/v1/auth/exchange` | POST | 无 | OAuth email → API Key |
| `/wiki/v1/auth/me` | GET | X-API-Key | 用户信息 + 用量 |
| `/wiki/v1/usage?days=30` | GET | X-API-Key | 用量统计（含每日/端点 breakdown） |
| `/wiki/v1/hub/stats` | GET | 无 | Wiki 总览 + 关键词图谱 |
| `/v1/health` | GET | 无 | 健康检查 |
| `/v1/search` | POST | X-API-Key | 搜索 |
| `/v1/judgments/{entity}` | GET | X-API-Key | 物理判据 |
| `/v1/insights` | GET | X-API-Key | 知识洞察 |

> **注意**：所有 `/v1/...` 端点也支持 `/wiki/v1/...` 前缀（已配置别名）。前端统一用 `/wiki/v1/...` 即可。

---

## 四、端点详细说明

### 4.1 `POST /wiki/v1/auth/exchange` — 换取 API Key

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
  "api_key": "rw_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
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
  "created_at": "2026-05-10T12:00:00",
  "message": "API key already exists. Use the key stored in your browser."
}
```

### 4.2 `GET /wiki/v1/auth/me` — 用户信息

**请求头**：`X-API-Key: rw_sk_xxx`

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
  "api_key": "rw_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "api_key_masked": "rw_sk_****...****abcd",
  "usage_today": 15,
  "daily_limit": 100
}
```

**Profile 页面展示**：
- 顶部：邮箱 + 计划类型标签（free/pro/enterprise）
- API Key 行：默认展示 `api_key_masked`，点击 [👁 Show] 切换显示 `api_key`，点击 [📋 Copy] 复制
- 用量进度条：`usage_today / daily_limit`
- 下方附 cURL 示例：
  ```bash
  curl -H "X-API-Key: rw_sk_xxx" https://api.rosclaw.io/v1/search \
    -H "Content-Type: application/json" \
    -d '{"query": "G1 gait", "search_type": "hybrid"}'
  ```

### 4.3 `GET /wiki/v1/usage?days=30` — 用量统计

**请求头**：`X-API-Key: rw_sk_xxx`

**响应**：
```json
{
  "status": "ok",
  "usage": {
    "total_calls": 245,
    "total_tokens": 125000,
    "avg_latency_ms": 45.2,
    "period_days": 30,
    "by_endpoint": {
      "/v1/search": 120,
      "/v1/judgments": 45,
      "/v1/physics/impact": 30
    },
    "daily_breakdown": [
      {"date": "2026-05-10", "calls": 15},
      {"date": "2026-05-09", "calls": 42}
    ]
  }
}
```

**Dashboard 页面展示**：
- 顶部：API Key 组件（与 Profile 共享）
- 用量卡片：总调用次数、总 Token、平均延迟
- 端点分布图：饼图或柱状图（`by_endpoint`）
- 每日折线图：30 天趋势（`daily_breakdown`）
- 配额进度条

### 4.4 `GET /wiki/v1/hub/stats` — Wiki 总览（公开）

**无需认证**

**响应**：
```json
{
  "status": "ok",
  "wiki_name": "ROSClaw Wiki",
  "description": "具身智能物理常识中枢 —— 覆盖视觉语言导航、机器人控制...",
  "global_stats": {
    "total_pages": 804,
    "total_wikilinks": 9579,
    "total_judgments": 1024,
    "total_code_graph_nodes": 69668,
    "total_code_graph_edges": 672112,
    "robots_covered": 4,
    "entities_covered": 25,
    "causal_chains": 10,
    "last_updated": "2026-05-10T08:00:00"
  },
  "keywords": [
    {"name": "Visual Language Navigation", "weight": 1.0, "type": "concept", "pages": 1},
    {"name": "Unitree-G1", "weight": 0.92, "type": "entity", "pages": 1}
  ],
  "keyword_categories": {
    "entity": [...],
    "concept": [...],
    "property": [...],
    "algorithm": [...],
    "constraint": [...]
  }
}
```

**Hub 页面展示**：

**顶部 Hero**：
- 标题："ROSClaw Wiki —— 具身智能物理常识中枢"
- 副标题：`{total_pages} 页面 · {total_wikilinks} 连接 · {total_judgments} 判据 · {robots_covered} 机器人`

**中部关键词图谱**（核心视觉）：
- Canvas / D3.js 渲染节点-边
- 节点颜色按 `type`：
  - `entity`（机器人）：`#3b82f6` 蓝色
  - `property`（参数）：`#f59e0b` 琥珀色
  - `concept`（概念）：`#06b6d4` 青色
  - `algorithm`（算法）：`#10b981` 绿色
  - `constraint`（约束）：`#8b5cf6` 紫色
- 节点大小按 `weight` 缩放，`weight >= 0.8` 加粗边框
- 鼠标悬停：Tooltip 显示 `名称 · 类型 · {pages} 页面`

**底部统计卡片**（6 个）：
- 页面数 / 链接数 / 判据数 / 图谱节点 / 图谱边 / 机器人覆盖

---

## 五、错误处理

| HTTP 状态码 | 含义 | 前端处理 |
|------------|------|---------|
| 400 | 请求参数错误 | 提示用户检查输入 |
| 401 | API Key 无效或缺失 | 清除 localStorage，跳转登录 |
| 429 | 频率限制 | 显示"请求过于频繁，请稍后" |
| 500 | 服务器内部错误 | 显示"服务暂时不可用" |

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
- [ ] 所有 API 请求统一走 `https://api.rosclaw.io`

---

## 七、本地开发

如需本地联调，在 `.env.local` 中：
```
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

后端 CORS 已配置允许 `http://localhost:3000` 和 `http://localhost:5173`。
