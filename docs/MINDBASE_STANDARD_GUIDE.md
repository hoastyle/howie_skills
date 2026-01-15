# Mindbase 知识图谱标准化使用指南

**版本**: 1.0.0
**最后更新**: 2025-01-15
**状态**: ✅ 已验证

---

## 🎯 概述

**Mindbase** 是 AIRIS MCP Gateway 提供的知识管理和会话持久化服务器，运行在 **Docker MCP Gateway (端口 9390)** 上。

### 核心功能

1. **Memory 管理** - Markdown 文档化记忆存储（类似 Serena）
2. **Conversation 管理** - AI 对话历史保存和语义搜索
3. **Session 管理** - 会话组织和上下文管理
4. **向量搜索** - 基于 PostgreSQL + pgvector 的语义搜索

---

## 📋 Mindbase 工具清单

### Memory 工具（5 个）

| 工具 | 功能 | 必需参数 |
|------|------|---------|
| `mindbase:memory_write` | 保存记忆到 Markdown + 数据库 | `name`, `content` |
| `mindbase:memory_read` | 读取指定记忆 | `name` |
| `mindbase:memory_list` | 列出所有记忆（可过滤） | 无 |
| `mindbase:memory_search` | 语义搜索记忆 | `query` |
| `mindbase:memory_delete` | 删除记忆 | `name` |

### Conversation 工具（4 个）

| 工具 | 功能 | 必需参数 |
|------|------|---------|
| `mindbase:conversation_save` | 保存对话历史 | `source`, `title`, `content` |
| `mindbase:conversation_search` | 语义搜索对话 | `query` |
| `mindbase:conversation_get` | 获取对话（可过滤） | 无 |
| `mindbase:conversation_delete` | 删除对话 | `id` |

### Session 工具（4 个）

| 工具 | 功能 | 必需参数 |
|------|------|---------|
| `mindbase:session_create` | 创建新会话 | `name` |
| `mindbase:session_list` | 列出最近会话 | 无 |
| `mindbase:session_start` | 启动/恢复会话 | 无 |
| `mindbase:session_delete` | 删除会话 | `id` |

---

## 🔧 AIRIS MCP Gateway 标准访问模式

### 三步标准化工作流

```typescript
// Step 1: 工具发现 (airis-find)
const mindbaseTools = await airis-find({
  query: "mindbase"
});
// 返回: 13 个工具

// Step 2: 参数验证 (airis-schema)
const schema = await airis-schema({
  tool: "mindbase:memory_write"
});
// 返回: 完整参数定义

// Step 3: 执行工具 (airis-exec)
const result = await airis-exec({
  tool: "mindbase:memory_write",
  arguments: {
    name: "architecture-decision",
    content: "# 架构决策\n...",
    category: "architecture",
    tags: ["nextjs", "typescript"]
  }
});
```

---

## 💻 使用示例

### 示例 1: 保存架构决策记忆

```typescript
await airis-exec({
  tool: "mindbase:memory_write",
  arguments: {
    name: "frontend-stack-2025-01-15",
    content: `# 前端技术栈选型

## 决策
- **框架**: Next.js 14
- **语言**: TypeScript 5.0
- **样式**: Tailwind CSS 3.4

## 理由
1. Next.js 提供服务端渲染和优秀的 SEO
2. TypeScript 提供类型安全
3. Tailwind CSS 加速开发流程

---
**决策日期**: 2025-01-15
**状态**: 已批准`,
    category: "decision",
    project: "my-project",
    tags: ["frontend", "nextjs", "tailwind"]
  }
});
```

### 示例 2: 语义搜索记忆

```typescript
const searchResults = await airis-exec({
  tool: "mindbase:memory_search",
  arguments: {
    query: "前端框架选型",
    threshold: 0.7,  // 相似度阈值 0-1
    limit: 5,
    category: "decision",
    project: "my-project"
  }
});
// 返回按相似度排序的记忆列表
```

### 示例 3: 保存对话历史

```typescript
await airis-exec({
  tool: "mindbase:conversation_save",
  arguments: {
    source: "claude-code",
    title: "实现用户认证功能",
    content: {
      messages: [
        { role: "user", content: "实现 JWT 认证" },
        { role: "assistant", content: "需要安装 jsonwebtoken 包..." }
      ],
      context: "添加登录和注册功能"
    },
    category: "task",
    priority: "high",
    sessionId: "session-123",
    metadata: {
      project: "my-project",
      tags: ["auth", "jwt"]
    }
  }
});
```

### 示例 4: 创建和管理会话

```typescript
// 创建会话
const session = await airis-exec({
  tool: "mindbase:session_create",
  arguments: {
    name: "sprint-1-development",
    description: "Sprint 1: 用户认证和授权功能开发",
    parentId: "parent-session-id"  // 可选：创建层级会话
  }
});

// 启动会话
await airis-exec({
  tool: "mindbase:session_start",
  arguments: {
    sessionId: session.id
  }
});

// 后续所有 conversation_save 可以关联到此会话
```

### 示例 5: 语义搜索对话

```typescript
const conversations = await airis-exec({
  tool: "mindbase:conversation_search",
  arguments: {
    query: "如何实现 JWT 认证",
    source: "claude-code",
    threshold: 0.6,
    limit: 3
  }
});
// 返回相关对话历史
```

---

## ⚠️ 常见错误和最佳实践

### 错误 1: 混淆 Memory MCP 和 Mindbase

**❌ 错误使用**（Memory MCP）:
```typescript
await airis-exec({
  tool: "memory:create_entities",  // ❌ 不存在于 AIRIS Gateway
  arguments: { entities: [...] }
});
```

**✅ 正确使用**（Mindbase）:
```typescript
await airis-exec({
  tool: "mindbase:memory_write",  // ✅ 正确
  arguments: { name: "...", content: "..." }
});
```

### 错误 2: 参数名称错误

**❌ 错误**:
```typescript
await airis-exec({
  tool: "mindbase:memory_write",
  arguments: {
    filename: "doc.md",  // ❌ 错误参数名
    body: "content"      // ❌ 错误参数名
  }
});
```

**✅ 正确**:
```typescript
await airis-exec({
  tool: "mindbase:memory_write",
  arguments: {
    name: "doc-name",    // ✅ 使用 name（不是 filename）
    content: "content"   // ✅ 使用 content（不是 body）
  }
});
```

### 最佳实践

1. **记忆命名**: 使用语义化名称，添加日期后缀
   ```typescript
   name: "architecture-decision-2025-01-15"
   name: "api-design-auth-endpoints"
   ```

2. **分类使用**: 始终指定 `category` 参数
   ```typescript
   category: "architecture"  // 架构设计
   category: "decision"      // 技术决策
   category: "pattern"       // 设计模式
   category: "guide"         // 使用指南
   category: "onboarding"    // 入门文档
   category: "note"          // 临时笔记
   ```

3. **项目隔离**: 使用 `project` 参数区分不同项目
   ```typescript
   project: "my-app"
   project: "my-docs"
   ```

4. **标签系统**: 使用 `tags` 参数增强检索
   ```typescript
   tags: ["react", "hooks", "frontend"]
   tags: ["api", "rest", "authentication"]
   ```

5. **会话管理**: 为长期项目创建会话
   ```typescript
   // 创建项目会话
   const session = await airis-exec({
     tool: "mindbase:session_create",
     arguments: {
       name: "project-x-development",
       description: "Project X - 全栈开发"
     }
   });

   // 所有对话关联到会话
   await airis-exec({
     tool: "mindbase:conversation_save",
     arguments: {
       source: "claude-code",
       title: "实现用户注册",
       content: { ... },
       sessionId: session.id
     }
   });
   ```

---

## 📊 数据模型

### Memory 结构

```typescript
interface Memory {
  name: string;              // 唯一标识符（成为文件名）
  content: string;           // Markdown 内容
  category?: 'architecture' | 'decision' | 'pattern' | 'guide' | 'onboarding' | 'note';
  project?: string;          // 项目标识符
  tags?: string[];           // 标签数组
  created_at: string;        // 创建时间（ISO 8601）
  updated_at: string;        // 更新时间（ISO 8601）
}
```

### Conversation 结构

```typescript
interface Conversation {
  id: string;                // 唯一 ID
  source: 'claude-code' | 'claude-desktop' | 'chatgpt' | 'cursor' | 'windsurf';
  title: string;             // 标题或摘要
  content: object;           // 对话内容（messages, context 等）
  category?: 'task' | 'decision' | 'progress' | 'note' | 'warning' | 'error';
  priority?: 'critical' | 'high' | 'normal' | 'low';
  sessionId?: string;        // 关联会话 ID
  channel?: string;          // 频道或工作区标识符
  metadata?: object;         // 额外元数据
  created_at: string;        // 创建时间
}
```

### Session 结构

```typescript
interface Session {
  id: string;                // 唯一 ID
  name: string;              // 会话名称
  description?: string;      // 会话描述
  parentId?: string;         // 父会话 ID（层级结构）
  created_at: string;        // 创建时间
  updated_at: string;        // 更新时间
}
```

---

## 🔌 技术架构

```
Mindbase 架构
├── Docker MCP Gateway (9390)
│   └── mindbase-mcp:latest Docker 镜像
│       └── Node.js MCP Server (dist/index.js)
│
├── PostgreSQL + pgvector
│   ├── memories 表（存储记忆）
│   ├── conversations 表（存储对话）
│   └── sessions 表（存储会话）
│   └── pgvector 扩展（向量相似度搜索）
│
└── Ollama Embedding
    └── nomic-embed-text 模型
    └── 生成文本向量用于语义搜索
```

---

## ✅ 验证检查清单

使用 Mindbase 前的验证步骤：

- [ ] Gateway 正在运行 (`docker ps` 查看 `airis-mcp-gateway-core`)
- [ ] Mindbase-postgres-dev 容器健康 (`docker ps` 查看状态)
- [ ] Ollama 服务可访问 (`curl http://localhost:11434/api/version`)
- [ ] nomic-embed-text 模型已下载 (`ollama list | grep nomic`)
- [ ] 使用 `airis-find query="mindbase"` 确认工具可用
- [ ] 使用 `airis-schema` 验证参数定义

---

## 🚀 快速开始

### 1. 启动 Gateway

```bash
cd /path/to/airis-mcp-gateway
docker compose up -d
```

### 2. 验证 Mindbase

```bash
# 检查容器状态
docker ps | grep mindbase

# 检查数据库连接
docker logs mindbase-postgres-dev | tail -10
```

### 3. 首次使用测试

```typescript
// 测试 memory_write
await airis-exec({
  tool: "mindbase:memory_write",
  arguments: {
    name: "test-memory",
    content: "# Test\nThis is a test memory."
  }
});

// 测试 memory_list
const memories = await airis-exec({
  tool: "mindbase:memory_list",
  arguments: {}
});

console.log("✅ Mindbase 工作正常！找到", memories.length, "个记忆");
```

---

## 📚 相关资源

**官方文档**:
- [AIRIS MCP Gateway README](https://github.com/agiletec-inc/airis-mcp-gateway)
- [Mindbase MCP Server](https://github.com/kazuph/mindbase)

**AIRIS Skills**:
- `airis-knowledge-mgmt` - 知识管理助手（需要更新以使用 Mindbase）
- `airis-web-research` - Web 研究和内容保存（可集成 Mindbase）

---

**版本**: 1.0.0
**作者**: Hao
**最后更新**: 2025-01-15
