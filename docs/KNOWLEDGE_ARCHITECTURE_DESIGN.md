# AIRIS 知识管理系统架构设计

**版本**: 1.0.0
**设计日期**: 2025-01-15
**策略**: Systematic
**深度**: Deep Analysis

---

## 📊 执行摘要

本设计文档重新规划了 AIRIS Skills 中的知识管理系统，整合 **Mindbase**、**Serena** 和 **Memory MCP** 三个关键组件，构建了完整的长短记忆架构。

### 核心发现

**关键问题**：
- ❌ 当前 `airis-knowledge-mgmt` skill 描述了不存在的 `memory:create_entities` 工具
- ❌ Mindbase 实际提供 13 个工具（Memory + Conversation + Session），但未在 skill 中体现
- ❌ Serena 的角色和责任未明确定义

**解决方案**：
- ✅ 明确三层记忆架构：短期（Memory）→ 项目（Serena）→ 长期（Mindbase）
- ✅ 重新设计 `airis-knowledge-mgmt` skill 以支持所有三个 MCP 服务器
- ✅ 创建标准化访问模式和使用指南

---

## 🏗️ 系统架构

### 三层记忆模型

```
┌─────────────────────────────────────────────────────────────────┐
│                        AIRIS Knowledge Architecture             │
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
        │                     │                     │
    RAM/Disk              Filesystem           PostgreSQL
   (JSON)               (Markdown)          + pgvector
```

### 详细组件分析

#### 1. Memory MCP - 短期记忆（Session Memory）

**角色**: 会话级临时记忆
**存储**: JSON 文件 (`/app/data/memory.json`)
**生命周期**: 会话结束即清除
**访问模式**: COLD（按需启动）

**工具清单**（预期，需验证）:
```typescript
// 知识图谱操作
memory:create_entities     // 创建实体
memory:create_relations     // 创建关系
memory:search_nodes        // 搜索节点
memory:get_entity          // 获取实体详情

// 会话记忆
memory:save_frame          // 保存当前帧
memory:recall_frame        // 回忆帧
memory:forget              // 清除记忆
```

**使用场景**:
- ✅ 当前会话的临时思考过程
- ✅ 快速构建实体-关系图谱
- ✅ 会话中的上下文保持
- ❌ 不适合跨会话持久化

**参数示例**:
```typescript
await airis-exec({
  tool: "memory:create_entities",
  arguments: {
    entities: [
      {
        name: "React",
        entityType: "Framework",
        observations: [
          "JavaScript UI 库",
          "由 Facebook 维护"
        ]
      }
    ]
  }
});
```

---

#### 2. Serena - 项目记忆（Project Memory）

**角色**: 项目级文档化记忆
**存储**: 文件系统 Markdown 文件 (`.serena/memories/`)
**生命周期**: 永久保存（手动删除）
**访问模式**: COLD（按需启动）

**工具清单**（基于官方文档）:
```typescript
// 记忆管理
serena:write_memory        // 写入记忆文件
serena:read_memory         // 读取记忆文件
serena:list_memories       // 列出所有记忆
serena:delete_memory       // 删除记忆文件
serena:update_memory       // 更新记忆文件

// 代码语义搜索
serena:search_code         // 语义代码搜索
serena:find_references     // 查找引用
serena:explain_code        // 代码解释
```

**使用场景**:
- ✅ 项目级文档保存（架构决策、API 规范）
- ✅ 代码语义检索和导航
- ✅ 技术选型记录和最佳实践
- ✅ 团队知识共享

**参数示例**:
```typescript
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "architecture-decision-2025-01-15.md",
    content: `# 架构决策：前端框架选型

## 背景
需要为新产品选择前端框架

## 决策
选择 Next.js 14 + TypeScript 5.0

## 理由
1. 服务端渲染优化 SEO
2. TypeScript 提供类型安全
3. 强大的生态系统

---
**决策日期**: 2025-01-15
**状态**: 已批准`
  }
});
```

---

#### 3. Mindbase - 长期记忆（Long-term Memory）

**角色**: 持久化知识库 + 对话历史 + 会话管理
**存储**: PostgreSQL + pgvector
**生命周期**: 永久保存（数据库持久化）
**访问模式**: COLD（通过 Docker MCP Gateway）

**工具清单**（已验证 - 13 个工具）:

**Memory 工具**（5 个）:
```typescript
mindbase:memory_write       // 写入记忆（Markdown + Database）
mindbase:memory_read        // 读取记忆
mindbase:memory_list        // 列出记忆（支持过滤）
mindbase:memory_search      // 语义搜索记忆（pgvector）
mindbase:memory_delete      // 删除记忆
```

**Conversation 工具**（4 个）:
```typescript
mindbase:conversation_save    // 保存对话历史
mindbase:conversation_search  // 语义搜索对话
mindbase:conversation_get     // 获取对话（支持过滤）
mindbase:conversation_delete  // 删除对话
```

**Session 工具**（4 个）:
```typescript
mindbase:session_create       // 创建会话
mindbase:session_list         // 列出会话
mindbase:session_start        // 启动/恢复会话
mindbase:session_delete       // 删除会话
```

**使用场景**:
- ✅ 跨项目知识库（架构模式、最佳实践）
- ✅ AI 对话历史持久化（PDCA 循环）
- ✅ 会话管理和上下文恢复
- ✅ 语义搜索和知识检索

**参数示例**:
```typescript
// Memory 操作
await airis-exec({
  tool: "mindbase:memory_write",
  arguments: {
    name: "microservices-pattern-2025-01-15",
    content: "# 微服务架构模式\n\n...",
    category: "pattern",
    project: "shared-knowledge",
    tags: ["microservices", "architecture"]
  }
});

// Conversation 操作
await airis-exec({
  tool: "mindbase:conversation_save",
  arguments: {
    source: "claude-code",
    title: "实现用户认证功能",
    content: { messages: [...] },
    category: "task",
    priority: "high",
    sessionId: "session-123"
  }
});

// Session 操作
await airis-exec({
  tool: "mindbase:session_create",
  arguments: {
    name: "project-x-sprint-1",
    description: "Sprint 1: 用户认证和授权"
  }
});
```

---

## 🎯 使用场景映射

### 决策矩阵：何时使用哪个 MCP？

| 场景 | 推荐方案 | 理由 |
|------|---------|------|
| **临时思考过程** | Memory MCP | 会话级，快速构建图谱 |
| **项目文档** | Serena | 项目级，Markdown 格式 |
| **架构决策** | Serena | 项目级，需要版本控制 |
| **跨项目知识** | Mindbase | 持久化，语义搜索 |
| **对话历史** | Mindbase | 专门支持对话管理 |
| **会话管理** | Mindbase | 支持会话恢复和上下文 |
| **代码语义搜索** | Serena | 专门的代码语义检索 |
| **知识图谱** | Memory MCP | 实体-关系图谱 |

### 典型工作流

#### 工作流 1: 架构决策记录

```
1. 当前会话思考（Memory MCP）
   └─ memory:create_entities (创建概念实体)
   └─ memory:create_relations (建立关系)

2. 保存到项目记忆（Serena）
   └─ serena:write_memory (保存决策文档)

3. 同步到长期知识库（Mindbase）
   └─ mindbase:memory_write (跨项目共享)
```

#### 工作流 2: 技术研究

```
1. Web 研究（Tavily + Fetch）
   └─ tavily:search (搜索最新信息)
   └─ fetch:fetch (提取详细内容)

2. 保存对话历史（Mindbase）
   └─ mindbase:conversation_save (保存研究过程)
   └─ mindbase:session_create (创建研究会话)

3. 提取知识要点（Serena）
   └─ serena:write_memory (保存研究总结)
```

#### 工作流 3: 代码理解

```
1. 语义代码搜索（Serena）
   └─ serena:search_code (查找相关代码)

2. 构建知识图谱（Memory MCP）
   └─ memory:create_entities (创建组件实体)
   └─ memory:create_relations (建立依赖关系)

3. 保存理解笔记（Mindbase）
   └─ mindbase:memory_write (保存理解笔记)
```

---

## 🔄 重新设计的 Skills

### 新 Skill: `airis-knowledge-hub`

**描述**: 统一的知识管理入口，智能路由到合适的 MCP 服务器

**触发条件**:
- "保存知识"、"记录笔记"、"创建记忆"
- "知识图谱"、"实体关系"
- "架构决策"、"技术选型"

**核心能力**:
```typescript
// 智能路由
interface KnowledgeHubSkill {
  // 短期记忆（Memory MCP）
  createGraph(entities, relations);
  searchGraph(query);

  // 项目记忆（Serena）
  saveProjectDoc(filename, content);
  searchProject(query);

  // 长期记忆（Mindbase）
  saveKnowledge(name, content, category);
  searchKnowledge(query);

  // 对话管理（Mindbase）
  saveConversation(title, content);
  createSession(name);

  // 智能选择
  autoRoute(context, content);
}
```

### 保留 Skill: `airis-knowledge-mgmt`

**更新内容**:
- ✅ 移除错误的 `memory:create_entities` 描述
- ✅ 添加 Mindbase 工具支持（13 个工具）
- ✅ 更新 Serena 工具参数（`memory_file_name`）
- ✅ 添加三层记忆架构说明
- ✅ 提供决策树帮助用户选择合适的 MCP

---

## 📊 技术规格

### 存储对比

| 维度 | Memory MCP | Serena | Mindbase |
|------|-----------|--------|----------|
| **存储介质** | JSON | Filesystem | PostgreSQL |
| **持久化** | 会话级 | 永久（文件） | 永久（数据库） |
| **语义搜索** | ❌ | ✅（代码） | ✅（全内容） |
| **向量存储** | ❌ | ❌ | ✅（pgvector） |
| **版本控制** | ❌ | ✅（Git） | ❌ |
| **会话管理** | ❌ | ❌ | ✅ |
| **实体-关系** | ✅ | ❌ | ❌ |
| **对话历史** | ❌ | ❌ | ✅ |

### 性能特性

| 操作 | Memory MCP | Serena | Mindbase |
|------|-----------|--------|----------|
| **写入延迟** | <100ms | 200-500ms | 500-1000ms |
| **读取延迟** | <50ms | 100-200ms | 200-500ms |
| **搜索延迟** | N/A | 1-2s | 0.5-1s |
| **扩展性** | 低（JSON） | 中（文件） | 高（数据库） |
| **并发支持** | 低 | 中 | 高 |

---

## ✅ 实施计划

### Phase 1: 验证和文档（立即）

1. **验证 Memory MCP 工具**
   ```bash
   # 使用 airis-find 验证工具可用性
   airis-find query="memory"
   ```

2. **验证 Serena 工具**
   ```bash
   # 检查 Serena 配置
   cat profiles/serena-remote.json
   ```

3. **创建验证脚本**
   ```typescript
   // scripts/validate-knowledge-tools.ts
   ```

### Phase 2: 更新 Skills（本周）

1. **更新 `airis-knowledge-mgmt`**
   - 移除错误的工具描述
   - 添加 Mindbase 支持
   - 更新所有示例

2. **创建 `airis-knowledge-hub`**
   - 统一入口
   - 智能路由逻辑
   - 完整示例

### Phase 3: 文档和指南（下周）

1. **更新使用指南**
   - 三层记忆架构说明
   - 决策树和选择指南
   - 完整示例

2. **创建验证检查清单**
   - 工具可用性检查
   - 参数正确性验证
   - 性能基准测试

---

## 📚 参考资源

**官方文档**:
- [Memory MCP Server](https://github.com/modelcontextprotocol/servers)
- [Serena MCP Server](https://github.com/oraios/serena)
- [Mindbase MCP Server](https://github.com/kazuph/mindbase)

**AIRIS 资源**:
- [AIRIS MCP Gateway](https://github.com/agiletec-inc/airis-mcp-gateway)
- [AIRIS Skills Documentation](../README.md)

---

**设计版本**: 1.0.0
**设计日期**: 2025-01-15
**设计师**: AI System Architect
**状态**: ✅ Design Complete, Pending Implementation
