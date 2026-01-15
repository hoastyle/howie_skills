---
name: airis-knowledge-mgmt
description: 知识管理助手，整合 Mindbase（长期记忆）、Serena（项目记忆）和 Memory MCP（短期记忆）三层架构。支持结构化知识存储、语义搜索、会话管理和项目文档化。适用于跨项目知识库、对话历史持久化、会话管理等场景。
---

# AIRIS Knowledge Management Helper

**MCP 服务器**: mindbase, serena, memory
**复杂度**: medium
**预估行数**: 280

---

## 🎯 触发条件

### 何时使用这个 Skill

**主要场景**:
- **长期知识库**: 保存跨项目的架构模式、最佳实践（Mindbase）
- **对话历史**: 持久化 AI 对话历史，支持 PDCA 循环（Mindbase）
- **会话管理**: 组织和管理多轮对话会话（Mindbase）
- **项目记忆**: 保存项目级文档和架构决策（Serena）
- **临时思考**: 当前会话的快速知识图谱构建（Memory MCP）

**关键词触发**:
- "保存知识"、"长期记忆"、"跨项目知识"
- "对话历史"、"会话管理"
- "项目记忆"、"架构决策"
- "知识图谱"、"实体关系"

**典型用户请求**:
```
"保存这个架构决策到知识库"
"记录我们的对话历史以便后续参考"
"创建一个会话来跟踪这个项目"
"建立微服务组件的知识图谱"
```

---

## 📋 三层记忆架构

### 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                    AIRIS Knowledge Architecture                 │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Short-term   │    │  Mid-term     │    │  Long-term    │
│  Memory MCP   │    │  Serena       │    │  Mindbase     │
│  (Session)    │    │  (Project)    │    │  (Persistent) │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
    RAM/Disk              Filesystem           PostgreSQL
   (JSON)                (Markdown)          + pgvector
```

### 路径选择决策树

```
用户需求
    │
    ├─ 需要跨项目持久化？
    │   YES → Mindbase (长期知识库)
    │
    ├─ 需要项目级文档管理？
    │   YES → Serena (项目记忆)
    │
    ├─ 需要对话历史或会话管理？
    │   YES → Mindbase (Conversation/Session)
    │
    └─ 当前会话临时思考？
        → Memory MCP (短期图谱)
```

### 使用场景映射表

| 场景 | 推荐方案 | 工具集 |
|------|---------|--------|
| **跨项目知识** | Mindbase | `memory_*` 工具 |
| **对话历史** | Mindbase | `conversation_*` 工具 |
| **会话管理** | Mindbase | `session_*` 工具 |
| **项目文档** | Serena | `write_memory`, `read_memory` |
| **临时图谱** | Memory MCP | `create_entities`, `create_relations` |

---

## 📋 Mindbase - 长期记忆（推荐）

### 核心功能

Mindbase 提供三个核心能力：
1. **Memory 管理** - 跨项目知识库
2. **Conversation 管理** - AI 对话历史
3. **Session 管理** - 会话组织和上下文

### Memory 工具（5 个）

#### 1. memory_write

**功能**: 保存知识到 Markdown 文件和 PostgreSQL 数据库

**参数**:
```typescript
{
  name: string;              // 必需：记忆名称（成为文件名）
  content: string;           // 必需：Markdown 内容
  category?: 'architecture' | 'decision' | 'pattern' | 'guide' | 'onboarding' | 'note';
  project?: string;          // 项目标识符
  tags?: string[];           // 标签数组
}
```

**示例**:
```typescript
await airis-exec({
  tool: "mindbase:memory_write",
  arguments: {
    name: "microservices-pattern-2025-01-15",
    content: `# 微服务架构模式

## 核心原则
- 服务独立性
- 去中心化数据管理
- API 网关统一入口`,
    category: "pattern",
    project: "shared-knowledge",
    tags: ["microservices", "architecture"]
  }
});
```

#### 2. memory_search

**功能**: 语义搜索记忆（使用 pgvector 向量相似度）

**参数**:
```typescript
{
  query: string;             // 必需：搜索查询
  threshold?: number;        // 相似度阈值 0-1（默认 0.7）
  limit?: number;            // 最大结果数（默认 10）
  category?: string;         // 按类别过滤
  project?: string;          // 按项目过滤
}
```

**示例**:
```typescript
const results = await airis-exec({
  tool: "mindbase:memory_search",
  arguments: {
    query: "微服务架构设计模式",
    threshold: 0.6,
    limit: 5,
    category: "pattern"
  }
});
// 返回按相似度排序的记忆列表
```

#### 3. memory_read

**功能**: 读取指定记忆

**参数**:
```typescript
{
  name: string;              // 必需：记忆名称
  project?: string;          // 项目标识符（可选）
}
```

#### 4. memory_list

**功能**: 列出所有记忆（支持过滤）

**参数**:
```typescript
{
  category?: string;         // 按类别过滤
  project?: string;          // 按项目过滤
  tags?: string[];           // 按标签过滤
}
```

#### 5. memory_delete

**功能**: 删除记忆（同时删除 Markdown 文件和数据库记录）

**参数**:
```typescript
{
  name: string;              // 必需：记忆名称
  project?: string;          // 项目标识符（可选）
}
```

---

### Conversation 工具（4 个）

#### 1. conversation_save

**功能**: 保存 AI 对话历史（自动生成向量用于语义搜索）

**参数**:
```typescript
{
  source: 'claude-code' | 'claude-desktop' | 'chatgpt' | 'cursor' | 'windsurf';
  title: string;             // 必需：对话标题或摘要
  content: object;           // 必需：对话内容（messages, context 等）
  category?: 'task' | 'decision' | 'progress' | 'note' | 'warning' | 'error';
  priority?: 'critical' | 'high' | 'normal' | 'low';
  sessionId?: string;        // 关联会话 ID
  channel?: string;          // 频道或工作区
  metadata?: object;         // 额外元数据
}
```

**示例**:
```typescript
await airis-exec({
  tool: "mindbase:conversation_save",
  arguments: {
    source: "claude-code",
    title: "实现用户认证功能",
    content: {
      messages: [
        { role: "user", content: "实现 JWT 认证" },
        { role: "assistant", content: "需要安装 jsonwebtoken..." }
      ],
      context: "添加登录和注册功能"
    },
    category: "task",
    priority: "high",
    metadata: {
      project: "my-app",
      tags: ["auth", "jwt"]
    }
  }
});
```

#### 2. conversation_search

**功能**: 语义搜索对话历史

**参数**:
```typescript
{
  query: string;             // 必需：搜索查询
  source?: string;           // 按来源平台过滤
  threshold?: number;        // 相似度阈值（默认 0.7）
  limit?: number;            // 最大结果数（默认 10）
}
```

#### 3. conversation_get

**功能**: 获取对话（支持详细过滤和分页）

**参数**:
```typescript
{
  id?: string;               // 获取特定对话
  sessionId?: string;        // 按会话过滤
  category?: string;         // 按类别过滤
  priority?: string;         // 按优先级过滤
  source?: string;           // 按来源过滤
  createdBefore?: string;    // ISO 8601 日期
  createdAfter?: string;     // ISO 8601 日期
  limit?: number;            // 最大结果数（默认 100）
  offset?: number;           // 分页偏移（默认 0）
}
```

#### 4. conversation_delete

**功能**: 删除对话

**参数**:
```typescript
{
  id: string;                // 必需：对话 ID
}
```

---

### Session 工具（4 个）

#### 1. session_create

**功能**: 创建新会话（用于组织对话）

**参数**:
```typescript
{
  name: string;              // 必需：会话名称
  description?: string;      // 会话描述
  parentId?: string;         // 父会话 ID（创建层级会话）
}
```

**示例**:
```typescript
const session = await airis-exec({
  tool: "mindbase:session_create",
  arguments: {
    name: "project-x-sprint-1",
    description: "Sprint 1: 用户认证和授权功能开发",
    parentId: "project-x-main"  // 创建子会话
  }
});
```

#### 2. session_start

**功能**: 启动或恢复会话（设置为当前上下文）

**参数**:
```typescript
{
  sessionId?: string;        // 现有会话 ID（恢复）
  name?: string;             // 新会话名称（创建新会话）
  description?: string;      // 新会话描述
}
```

#### 3. session_list

**功能**: 列出最近的会话

**参数**:
```typescript
{
  limit?: number;            // 最大结果数（默认 10）
}
```

#### 4. session_delete

**功能**: 删除会话（对话将保留但变为孤立）

**参数**:
```typescript
{
  id: string;                // 必需：会话 ID
}
```

---

## 📋 Serena - 项目记忆

### 核心功能

Serena 提供项目级文档化记忆管理，保存到 `.serena/memories/` 目录。

### 工具列表

#### 1. write_memory

**⚠️ 关键陷阱：参数名称是 `memory_file_name`**

```typescript
// ❌ 错误
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    filename: "doc.md",      // 错误参数名
    content: "..."
  }
});

// ✅ 正确
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "architecture-decision-2025-01-15.md",  // 正确
    content: `# 架构决策

## 决策
选择 Next.js 作为前端框架

## 理由
1. 服务端渲染优化 SEO
2. 强大的生态系统

---
**日期**: 2025-01-15`
  }
});
```

**参数**:
- `memory_file_name` (必需) - 记忆文件名
- `content` (必需) - Markdown 内容

#### 2. read_memory

**功能**: 读取记忆文件

**参数**:
```typescript
{
  memory_file_name: string;  // 必需：文件名
}
```

#### 3. list_memories

**功能**: 列出所有记忆文件

**参数**: 无

#### 4. delete_memory

**功能**: 删除记忆文件

**参数**:
```typescript
{
  memory_file_name: string;  // 必需：文件名
}
```

---

## 📋 Memory MCP - 短期记忆（可选）

### 核心功能

Memory MCP 提供会话级临时记忆，用于快速构建实体-关系图谱。

**注意**: Memory MCP 工具可能在某些配置中不可用，使用前请通过 `airis-find` 验证。

### 预期工具（需验证）

```typescript
// 知识图谱操作
memory:create_entities     // 创建实体
memory:create_relations     // 创建关系
memory:search_nodes        // 搜索节点
memory:get_entity          // 获取实体详情
```

### 使用示例

```typescript
// 验证工具可用性
const memoryTools = await airis-find({ query: "memory" });

if (memoryTools.some(t => t.name === "memory:create_entities")) {
  // 创建实体
  await airis-exec({
    tool: "memory:create_entities",
    arguments: {
      entities: [
        {
          name: "UserService",
          entityType: "Component",
          observations: [
            "负责用户认证和授权",
            "提供 REST API 接口"
          ]
        }
      ]
    }
  });
}
```

---

## 💻 完整示例

### 示例 1: 跨项目知识库管理

**场景**: 保存可复用的架构模式到知识库

```typescript
// 1. 保存到 Mindbase（跨项目知识库）
await airis-exec({
  tool: "mindbase:memory_write",
  arguments: {
    name: "circuit-breaker-pattern-2025-01-15",
    content: `# 熔断器模式

## 描述
防止级联故障的弹性模式

## 实现
- 状态机：Closed → Open → Half-Open
- 超时设置
- 降级策略

## 最佳实践
1. 设置合理的超时时间
2. 实现降级逻辑
3. 监控和告警`,
    category: "pattern",
    project: "shared-knowledge",  // 跨项目共享
    tags: ["resilience", "microservices", "patterns"]
  }
});

// 2. 语义搜索相关模式
const patterns = await airis-exec({
  tool: "mindbase:memory_search",
  arguments: {
    query: "弹性模式 容错",
    category: "pattern",
    threshold: 0.6,
    limit: 5
  }
});

console.log(`找到 ${patterns.length} 个相关模式`);
```

### 示例 2: 对话历史和会话管理

**场景**: 追踪项目开发的完整对话历史

```typescript
// 1. 创建项目会话
const session = await airis-exec({
  tool: "mindbase:session_create",
  arguments: {
    name: "ecommerce-auth-implementation",
    description: "电商项目认证功能实现"
  }
});

console.log("会话 ID:", session.id);

// 2. 保存对话历史
await airis-exec({
  tool: "mindbase:conversation_save",
  arguments: {
    source: "claude-code",
    title: "实现 OAuth2 登录",
    content: {
      messages: [
        { role: "user", content: "如何实现 Google OAuth2 登录？" },
        { role: "assistant", content: "使用 passport-google-oauth20..." }
      ],
      context: "添加社交登录功能"
    },
    category: "task",
    priority: "high",
    sessionId: session.id,  // 关联到会话
    metadata: {
      project: "ecommerce",
      feature: "authentication"
    }
  }
});

// 3. 搜索相关对话
const conversations = await airis-exec({
  tool: "mindbase:conversation_search",
  arguments: {
    query: "OAuth 认证实现",
    sessionId: session.id,
    limit: 10
  }
});
```

### 示例 3: 项目文档管理

**场景**: 保存项目级架构决策

```typescript
// 保存到 Serena（项目记忆）
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "adr-001-database-selection-2025-01-15.md",
    content: `# ADR 001: 数据库选型

## 状态
已接受

## 背景
需要为新项目选择主数据库

## 决策
选择 PostgreSQL 15 作为主数据库

## 理由
1. ACID 事务支持
2. 丰富的数据类型（JSON, UUID）
3. pgvector 扩展支持向量搜索
4. 强大的生态系统

## 后果
- 使用 TypeScript + Prisma ORM
- 采用迁移管理数据库版本
- 定期备份策略

---
**决策日期**: 2025-01-15
**决策者**: 架构团队`
  }
});
```

### 示例 4: 组合使用三层架构

**场景**: 完整的知识管理流程

```typescript
// Step 1: 当前会话快速思考（Memory MCP）
if (hasMemoryTools) {
  await airis-exec({
    tool: "memory:create_entities",
    arguments: {
      entities: [
        { name: "AuthModule", entityType: "Component", observations: ["认证模块"] },
        { name: "JWT", entityType: "Concept", observations: ["JSON Web Token"] }
      ]
    }
  });
}

// Step 2: 保存到项目记忆（Serena）
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "auth-module-design.md",
    content: generateAuthDesignDoc()
  }
});

// Step 3: 同步到长期知识库（Mindbase）
await airis-exec({
  tool: "mindbase:memory_write",
  arguments: {
    name: "jwt-authentication-pattern",
    content: generateAuthPatternDoc(),
    category: "pattern",
    project: "shared-knowledge"
  }
});

// Step 4: 记录对话历史（Mindbase）
await airis-exec({
  tool: "mindbase:conversation_save",
  arguments: {
    source: "claude-code",
    title: "设计认证模块架构",
    content: { messages: conversationHistory },
    category: "decision"
  }
});
```

---

## ⚠️ 常见陷阱和解决方案

### 陷阱 1: 参数名称错误

**Serena 使用 `memory_file_name` 而非 `filename`**
```typescript
// ❌ 错误
{ filename: "doc.md" }

// ✅ 正确
{ memory_file_name: "doc.md" }
```

### 陷阱 2: Mindbase vs Memory MCP 混淆

```typescript
// ❌ 错误：使用不存在的 Memory MCP 工具
await airis-exec({ tool: "memory:create_entities" });

// ✅ 正确：使用 Mindbase 工具
await airis-exec({ tool: "mindbase:memory_write" });
```

### 陷阱 3: 工具可用性未验证

**解决方案**: 使用前始终验证
```typescript
// 1. 发现工具
const tools = await airis-find({ query: "mindbase" });

// 2. 检查工具是否存在
if (tools.some(t => t.name === "mindbase:memory_write")) {
  // 3. 验证参数
  const schema = await airis-schema({ tool: "mindbase:memory_write" });

  // 4. 执行操作
  await airis-exec({
    tool: "mindbase:memory_write",
    arguments: { name: "...", content: "..." }
  });
}
```

---

## 🔌 AIRIS MCP Gateway 标准访问模式

### 四步标准化工作流

```typescript
// Step 1: 工具发现
const mindbaseTools = await airis-find({ query: "mindbase" });
const serenaTools = await airis-find({ query: "serena" });

// Step 2: 参数验证
const schema = await airis-schema({ tool: "mindbase:memory_write" });

// Step 3: 执行工具
await airis-exec({
  tool: "mindbase:memory_write",
  arguments: { name: "...", content: "..." }
});

// Step 4: 健康检查（可选）
const health = await airis-exec({ tool: "gateway-control:health" });
```

---

## 📚 参考文档

### 详细指南

- **[Mindbase 标准指南](../../docs/MINDBASE_STANDARD_GUIDE.md)** - Mindbase 完整使用指南
- **[知识架构设计](../../docs/KNOWLEDGE_ARCHITECTURE_DESIGN.md)** - 三层记忆架构设计
- **[MCP 参数参考](../../docs/MCP_PARAMETER_REFERENCE.md)** - 完整参数文档

### MCP 服务器文档

- [Mindbase GitHub](https://github.com/kazuph/mindbase)
- [Serena GitHub](https://github.com/oraios/serena)
- [Memory MCP](https://github.com/modelcontextprotocol/servers)

---

## 📊 性能和限制

| 操作 | Mindbase | Serena | Memory MCP |
|------|----------|--------|------------|
| **写入延迟** | 500-1000ms | 200-500ms | <100ms |
| **读取延迟** | 200-500ms | 100-200ms | <50ms |
| **搜索延迟** | 0.5-1s | 1-2s | N/A |
| **扩展性** | 高（数据库） | 中（文件） | 低（JSON） |
| **持久化** | ✅ 永久 | ✅ 永久 | ❌ 会话级 |

**最佳实践**:
- 批量操作：一次调用处理多个项目
- 语义命名：使用清晰的名称和标签
- 定期清理：删除过时的记忆和对话
- 分类管理：使用 category 和 project 组织内容

---

**版本**: 2.0.0
**最后更新**: 2025-01-15
**作者**: Hao
**状态**: ✅ 已更新为三层架构
