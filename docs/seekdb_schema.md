# SeekDB Schema Design

Schema definitions for Phase 11 SeekDB migration.

## Table 1: wiki_pages

Core wiki content table with fulltext and vector indexes.

```sql
CREATE TABLE wiki_pages (
    id VARCHAR(255) PRIMARY KEY,
    type VARCHAR(50),
    title TEXT,
    body TEXT,
    tags JSON,
    confidence FLOAT,
    created_at TIMESTAMP,
    last_reinforced TIMESTAMP,
    sources JSON,
    embedding VECTOR(384),
    wikilinks JSON,
    FULLTEXT INDEX body_ft (body),
    VECTOR INDEX embedding_idx (embedding)
);
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| id | VARCHAR(255) | Page slug (primary key) |
| type | VARCHAR(50) | entity / algorithm / concept / skill / episode |
| title | TEXT | Human-readable title |
| body | TEXT | Markdown body content |
| tags | JSON | Array of tag strings |
| confidence | FLOAT | 0.0-1.0 confidence score |
| created_at | TIMESTAMP | Creation time |
| last_reinforced | TIMESTAMP | Last update/reinforcement time |
| sources | JSON | Array of source references |
| embedding | VECTOR(384) | Sentence-transformer embedding |
| wikilinks | JSON | Outbound wikilink targets |

### Indexes

- `body_ft`: Fulltext index for keyword search
- `embedding_idx`: Vector index for semantic similarity search

## Table 2: judgments

Structured parameter judgments with conflict tracking.

```sql
CREATE TABLE judgments (
    id VARCHAR(255) PRIMARY KEY,
    entity VARCHAR(255),
    context VARCHAR(255),
    parameter VARCHAR(255),
    recommended_value TEXT,
    confidence FLOAT,
    sources JSON,
    conflicts_resolved BOOLEAN,
    resolved_at TIMESTAMP
);
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| id | VARCHAR(255) | Judgment UUID |
| entity | VARCHAR(255) | Target entity name |
| context | VARCHAR(255) | Usage context |
| parameter | VARCHAR(255) | Parameter name |
| recommended_value | TEXT | Suggested value |
| confidence | FLOAT | Judgment confidence |
| sources | JSON | Supporting sources |
| conflicts_resolved | BOOLEAN | Whether conflicts are resolved |
| resolved_at | TIMESTAMP | Resolution timestamp |

## Table 3: api_usage

Commercial API usage tracking for Phase 11 billing.

```sql
CREATE TABLE api_usage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    api_key VARCHAR(64),
    endpoint VARCHAR(255),
    tokens_used INT,
    latency_ms INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| id | INT | Auto-increment primary key |
| api_key | VARCHAR(64) | Client API key |
| endpoint | VARCHAR(255) | API endpoint accessed |
| tokens_used | INT | Token consumption |
| latency_ms | INT | Response latency |
| created_at | TIMESTAMP | Request timestamp |

## Migration Notes

1. **Vector dimension**: 384 matches `paraphrase-multilingual-MiniLM-L12-v2` embeddings.
2. **JSON fields**: Stored as JSON strings; SeekDB must support JSON type or TEXT with JSON functions.
3. **Primary keys**: `wiki_pages.id` maps to existing page slugs.
4. **Judgments FK**: Optional foreign key from `judgments.entity` to `wiki_pages.title` for referential integrity.
5. **Index strategy**: Hybrid search uses `FULLTEXT` for BM25 + `VECTOR` for semantic + application-level RRF fusion.
