---
name: airis-knowledge-mgmt
description: 知识图谱管理助手，使用 Memory MCP 创建实体和关系构建知识图谱，使用 Serena MCP 管理项目记忆文件。支持双路径知识管理：结构化知识图谱（实体-关系）和文档化项目记忆。适用于项目知识整理、概念关系梳理、会话记忆保存、技术文档管理等场景。
---

# AIRIS Knowledge Management Helper

**MCP 服务器**: memory, serena
**复杂度**: medium
**预估行数**: 260

---

## 🎯 触发条件

### 何时使用这个 Skill

**主要场景**:
- **知识图谱构建**: 创建概念、组件、人员、产品等实体及其关系
- **项目知识整理**: 保存架构决策、技术选型、最佳实践到项目记忆
- **概念关系梳理**: 理清复杂系统中的依赖关系、包含关系、实现关系
- **会话记忆保存**: 保存重要对话内容、决策过程到长期记忆
- **技术文档管理**: 系统化管理技术文档、学习笔记、研究报告

**关键词触发**:
- "创建知识图谱"、"建立关系"、"保存知识"
- "记录到记忆"、"保存笔记"、"整理文档"
- "创建实体"、"添加关系"、"查询知识"
- "项目记忆"、"长期记忆"

**典型用户请求**:
```
"创建一个知识图谱，记录微服务架构中的各个组件及其依赖关系"
"保存今天的架构决策讨论到项目记忆"
"建立 React 和 Next.js 的关系，Next.js 是基于 React 的框架"
"整理学习笔记，记录 TypeScript 的核心概念"
```

---

## 📋 双路径工作流

### 路径选择决策

```
用户需求
    │
    ├─ 需要结构化关系（实体-关系图谱）？
    │   YES → 路径 1: Memory MCP (知识图谱)
    │
    ├─ 需要文档化保存（长文本、笔记）？
    │   YES → 路径 2: Serena MCP (项目记忆)
    │
    └─ 两者都需要？
        → 组合使用：Memory 存关系 + Serena 存详细文档
```

---

## 📋 路径 1: 知识图谱（Memory MCP）

### Phase 1: 创建实体

**功能**: 创建知识图谱中的实体（概念、组件、人员等）

**⚠️ 关键陷阱：observations 字段必需**

```typescript
// ❌ 错误：缺少 observations
await airis-exec({
  tool: "memory:create_entities",
  arguments: {
    entities: [
      {
        name: "React",
        entityType: "Framework"
      }
    ]
  }
});
// Error: 'observations' is required

// ✅ 正确：包含 observations
await airis-exec({
  tool: "memory:create_entities",
  arguments: {
    entities: [
      {
        name: "React",
        entityType: "Framework",
        observations: [
          "React 是一个用于构建用户界面的 JavaScript 库",
          "由 Facebook 开发和维护",
          "使用虚拟 DOM 提升性能"
        ]
      }
    ]
  }
});
```

**参数说明**:
- `entities` (必需) - 实体数组
  - `name` (必需) - 实体名称（唯一标识）
  - `entityType` (必需) - 实体类型（Concept, Component, Person, Product 等）
  - `observations` (必需) - 观察/描述数组（至少 1 个）

**支持的实体类型**:
- `Concept` - 抽象概念（如"微服务架构"、"RESTful API"）
- `Component` - 系统组件（如"UserService"、"AuthModule"）
- `Person` - 人员（如"项目负责人"、"开发者"）
- `Product` - 产品/工具（如"React"、"TypeScript"）
- `Document` - 文档（如"架构设计文档"、"API 规范"）

**批量创建示例**:
```typescript
await airis-exec({
  tool: "memory:create_entities",
  arguments: {
    entities: [
      {
        name: "UserService",
        entityType: "Component",
        observations: [
          "负责用户认证和授权",
          "提供 REST API 接口",
          "使用 JWT 进行会话管理"
        ]
      },
      {
        name: "Database",
        entityType: "Component",
        observations: [
          "PostgreSQL 数据库",
          "存储用户信息和会话数据"
        ]
      }
    ]
  }
});
```

---

### Phase 2: 创建关系

**功能**: 建立实体之间的关系

**执行创建**:
```typescript
await airis-exec({
  tool: "memory:create_relations",
  arguments: {
    relations: [
      {
        from: "UserService",
        to: "Database",
        relationType: "dependsOn"
      },
      {
        from: "Next.js",
        to: "React",
        relationType: "uses"
      }
    ]
  }
});
```

**参数说明**:
- `relations` (必需) - 关系数组
  - `from` (必需) - 源实体名称
  - `to` (必需) - 目标实体名称
  - `relationType` (必需) - 关系类型

**支持的关系类型**:
- `dependsOn` - 依赖关系（A 依赖 B）
- `uses` - 使用关系（A 使用 B）
- `includes` - 包含关系（A 包含 B）
- `implements` - 实现关系（A 实现 B）
- `extends` - 继承关系（A 继承 B）
- `relatedTo` - 相关关系（A 与 B 相关）

---

### Phase 3: 查询知识图谱

**功能**: 搜索和浏览知识图谱

**搜索节点**:
```typescript
const searchResult = await airis-exec({
  tool: "memory:search_nodes",
  arguments: {
    query: "UserService",
    limit: 10
  }
});
```

**返回结果**:
```json
{
  "nodes": [
    {
      "name": "UserService",
      "entityType": "Component",
      "observations": [...],
      "relations": [
        {"to": "Database", "type": "dependsOn"}
      ]
    }
  ]
}
```

---

## 📋 路径 2: 项目记忆（Serena MCP）

### Phase 1: 写入记忆

**功能**: 保存文档化的项目知识

**⚠️ 关键陷阱：参数名称是 memory_file_name**

```typescript
// ❌ 错误：使用 filename
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    filename: "architecture-decision.md",  // 错误参数名
    content: "..."
  }
});

// ✅ 正确：使用 memory_file_name
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "architecture-decision.md",  // 正确参数名
    content: `# 架构决策记录

## 背景
我们需要选择前端框架...

## 决策
选择 Next.js 作为主要框架

## 理由
1. 服务端渲染支持
2. 优秀的开发体验
3. 强大的社区生态

---
**日期**: ${new Date().toISOString().split('T')[0]}
`
  }
});
```

**参数说明**:
- `memory_file_name` (必需) - 记忆文件名（会保存到 `.serena/memories/` 目录）
- `content` (必需) - Markdown 格式的内容

**记忆文件命名规范**:
- 使用语义化名称：`topic-subtopic-date.md`
- 使用小写字母和连字符
- 添加日期后缀便于追踪
- 示例：
  - `architecture-decision-2025-12-30.md`
  - `react-hooks-learning-notes.md`
  - `api-design-best-practices.md`

---

### Phase 2: 列出记忆

**功能**: 查看所有已保存的记忆文件

```typescript
const memoryList = await airis-exec({
  tool: "serena:list_memories",
  arguments: {}
});
```

**返回结果**:
```json
{
  "memories": [
    {
      "name": "architecture-decision.md",
      "path": ".serena/memories/architecture-decision.md",
      "size": 1024,
      "modified": "2025-12-30T10:30:00Z"
    }
  ]
}
```

---

### Phase 3: 读取记忆

**功能**: 读取特定的记忆文件内容

```typescript
const memoryContent = await airis-exec({
  tool: "serena:read_memory",
  arguments: {
    memory_file_name: "architecture-decision.md"
  }
});
```

**返回结果**:
```json
{
  "content": "# 架构决策记录\n\n..."
}
```

---

## 💻 完整示例

### 示例 1: 构建微服务知识图谱

**用户需求**:
```
"创建一个知识图谱，记录我们微服务架构中的 3 个核心服务及其依赖"
```

**执行步骤**:

```typescript
// Step 1: 创建服务实体
await airis-exec({
  tool: "memory:create_entities",
  arguments: {
    entities: [
      {
        name: "UserService",
        entityType: "Component",
        observations: [
          "用户认证和授权服务",
          "提供 JWT 令牌生成",
          "端口: 3001"
        ]
      },
      {
        name: "OrderService",
        entityType: "Component",
        observations: [
          "订单管理服务",
          "处理订单创建、查询、更新",
          "端口: 3002"
        ]
      },
      {
        name: "PaymentService",
        entityType: "Component",
        observations: [
          "支付处理服务",
          "集成第三方支付网关",
          "端口: 3003"
        ]
      },
      {
        name: "PostgreSQL",
        entityType: "Component",
        observations: [
          "共享数据库",
          "存储用户、订单、支付数据"
        ]
      },
      {
        name: "Redis",
        entityType: "Component",
        observations: [
          "缓存服务",
          "存储会话和临时数据"
        ]
      }
    ]
  }
});

// Step 2: 创建依赖关系
await airis-exec({
  tool: "memory:create_relations",
  arguments: {
    relations: [
      {
        from: "UserService",
        to: "PostgreSQL",
        relationType: "dependsOn"
      },
      {
        from: "UserService",
        to: "Redis",
        relationType: "uses"
      },
      {
        from: "OrderService",
        to: "PostgreSQL",
        relationType: "dependsOn"
      },
      {
        from: "OrderService",
        to: "UserService",
        relationType: "dependsOn"
      },
      {
        from: "PaymentService",
        to: "PostgreSQL",
        relationType: "dependsOn"
      },
      {
        from: "PaymentService",
        to: "OrderService",
        relationType: "dependsOn"
      }
    ]
  }
});

// Step 3: 验证知识图谱
const graphCheck = await airis-exec({
  tool: "memory:search_nodes",
  arguments: {
    query: "Service",
    limit: 10
  }
});

console.log(`✅ 创建了 ${graphCheck.nodes.length} 个服务节点`);
```

**预期输出**:
```
✅ 知识图谱创建完成
- 5 个实体：3 个服务 + 2 个基础设施
- 6 个关系：依赖链清晰
```

---

### 示例 2: 组合使用 Memory + Serena

**用户需求**:
```
"记录今天的技术选型讨论，包括概念关系和详细文档"
```

**执行步骤**:

```typescript
// Step 1: 使用 Memory 创建技术栈实体和关系
await airis-exec({
  tool: "memory:create_entities",
  arguments: {
    entities: [
      {
        name: "Next.js",
        entityType: "Product",
        observations: ["React 框架", "SSR 支持", "v14"]
      },
      {
        name: "TypeScript",
        entityType: "Product",
        observations: ["类型安全", "v5.0"]
      },
      {
        name: "Tailwind CSS",
        entityType: "Product",
        observations: ["实用优先 CSS", "v3.4"]
      }
    ]
  }
});

await airis-exec({
  tool: "memory:create_relations",
  arguments: {
    relations: [
      { from: "Next.js", to: "React", relationType: "uses" },
      { from: "Next.js", to: "TypeScript", relationType: "uses" },
      { from: "Next.js", to: "Tailwind CSS", relationType: "uses" }
    ]
  }
});

// Step 2: 使用 Serena 保存详细决策文档
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "tech-stack-decision-2025-12-30.md",
    content: `# 技术栈选型决策

## 背景
为新项目选择前端技术栈

## 决策
- **框架**: Next.js 14
- **语言**: TypeScript 5.0
- **样式**: Tailwind CSS 3.4

## 理由

### Next.js
- 服务端渲染（SEO 优化）
- App Router（最新路由系统）
- 优秀的开发体验

### TypeScript
- 类型安全
- 更好的 IDE 支持
- 减少运行时错误

### Tailwind CSS
- 快速原型开发
- 一致的设计系统
- 优秀的性能

## 依赖关系
\`\`\`
Next.js
  ├─ uses → React
  ├─ uses → TypeScript
  └─ uses → Tailwind CSS
\`\`\`

## 参考资料
- [Next.js 官方文档](https://nextjs.org)
- [TypeScript 手册](https://www.typescriptlang.org)
- [Tailwind CSS 文档](https://tailwindcss.com)

---
**决策日期**: 2025-12-30
**参与人员**: 架构团队
**状态**: 已批准
`
  }
});
```

**预期输出**:
```
✅ 知识管理完成
- Memory: 创建了 3 个技术栈实体和 3 个关系
- Serena: 保存了详细决策文档到 tech-stack-decision-2025-12-30.md
```

---

## ⚠️ 常见陷阱和解决方案

### 陷阱 1: Memory 实体缺少 observations

**错误现象**:
```
Error: 'observations' is required for each entity
```

**原因分析**:
Memory MCP 要求每个实体必须有至少 1 个 observation（观察/描述）

**解决方案**:
```typescript
// ❌ 错误：缺少 observations
{
  name: "React",
  entityType: "Framework"
}

// ✅ 正确：包含 observations
{
  name: "React",
  entityType: "Framework",
  observations: [
    "JavaScript UI 库",
    "由 Facebook 维护"
  ]
}
```

---

### 陷阱 2: Serena 参数名称错误

**错误现象**:
```
Error: Unknown parameter 'filename'
```

**原因分析**:
Serena MCP 使用 `memory_file_name` 而非标准的 `filename`

**解决方案**:
```typescript
// ❌ 错误
{ filename: "notes.md" }

// ✅ 正确
{ memory_file_name: "notes.md" }
```

---

### 陷阱 3: 关系类型不明确

**错误现象**:
创建的关系无法准确表达实体间的关系

**原因分析**:
使用了过于宽泛的关系类型（如 `relatedTo`），无法清晰表达具体关系

**解决方案**:
```typescript
// ❌ 不推荐：关系不明确
{
  from: "UserService",
  to: "Database",
  relationType: "relatedTo"  // 太宽泛
}

// ✅ 推荐：明确的关系
{
  from: "UserService",
  to: "Database",
  relationType: "dependsOn"  // 清晰的依赖关系
}

// 选择合适的关系类型：
// - dependsOn: 强依赖（A 无 B 无法运行）
// - uses: 使用关系（A 调用 B 的功能）
// - includes: 包含关系（A 是 B 的容器）
// - implements: 实现关系（A 实现了 B 的接口）
// - extends: 继承关系（A 继承 B）
```

---

## 🔌 AIRIS MCP Gateway 标准访问模式（完整版）

本章节展示完整的 AIRIS MCP Gateway 访问模式，确保工具使用的标准化和可靠性。

### 四步标准化工作流

#### Step 1: 工具发现 (airis-find)

使用 `airis-find` 发现 Memory 和 Serena 提供的工具：

```typescript
// 发现 Memory 工具（知识图谱）
const memoryTools = await airis-find({
  query: "memory"
});
console.log("Memory 工具:", memoryTools.map(t => t.name));
// 输出: ["memory:create_entities", "memory:create_relations", "memory:search_nodes", ...]

// 发现 Serena 工具（项目记忆）
const serenaTools = await airis-find({
  query: "serena memory"
});
console.log("Serena 记忆工具:", serenaTools.map(t => t.name));
// 输出: ["serena:write_memory", "serena:read_memory", "serena:list_memories", ...]
```

**为什么需要这一步？**
- 发现 Memory 和 Serena 的可用工具
- 确认工具名称拼写正确
- 根据需求选择合适的 MCP 服务器

---

#### Step 2: 参数验证 (airis-schema)

在执行前，使用 `airis-schema` 检查工具的参数要求：

```typescript
// 检查 Memory create_entities 参数
const createEntitiesSchema = await airis-schema({
  tool: "memory:create_entities"
});
console.log("必需参数:", createEntitiesSchema.inputSchema.required);
// 输出: ["entities"]
// 注意：entities 数组中的每个对象必须包含 observations

// 检查 Serena write_memory 参数
const writeMemorySchema = await airis-schema({
  tool: "serena:write_memory"
});
console.log("Serena 参数:", writeMemorySchema.inputSchema.required);
// 输出: ["memory_file_name", "content"]
```

**常见参数命名陷阱**（本 skill 涉及）:
- ⚠️ Memory: `entities` 数组中每个实体必须包含 `observations` 字段
- ⚠️ Serena: 参数名是 `memory_file_name`（不是 `filename`）
- ⚠️ Memory: `entityType` 必须是标准类型（Concept, Component, Person, Product, Document）
- ⚠️ Memory: `relationType` 必须是标准类型（depends-on, part-of, related-to, uses, includes, implements）

通过 `airis-schema` 可以避免 90% 的参数错误！

---

#### Step 3: 执行工具 (airis-exec)

验证参数后，使用 `airis-exec` 执行工具（已在上面的工作流程中详细说明）。

---

#### Step 4: 健康检查 (gateway-control)

在执行工具前，检查 AIRIS MCP Gateway 状态：

```typescript
// 检查 Gateway 健康状态
const health = await airis-exec({
  tool: "gateway-control:health"
});

if (!health.ok) {
  throw new Error("AIRIS MCP Gateway 不可用，请检查 Gateway 是否正在运行");
}

// 列出可用的 MCP 服务器
const servers = await airis-exec({
  tool: "gateway-control:list-servers"
});

// 验证 Memory 和 Serena 已安装
const requiredServers = ["memory", "serena"];
for (const serverName of requiredServers) {
  const server = servers.find(s => s.name === serverName);

  if (!server) {
    throw new Error(`服务器 ${serverName} 未安装`);
  }

  if (server.mode === "HOT" && server.ready) {
    console.log(`✅ ${serverName} 已就绪（HOT 模式）`);
  } else if (server.mode === "COLD") {
    if (!server.ready) {
      console.log(`⏳ 等待 ${serverName} 启动（COLD 模式）...`);
      await sleep(3000);
    }
    console.log(`✅ ${serverName} 已就绪（COLD 模式）`);
  }
}
```

**什么时候需要健康检查？**
- ✅ 首次使用 Memory 或 Serena
- ✅ 批量创建实体和关系
- ✅ 生产环境部署
- ⚠️ 单次快速操作时可以跳过（但要处理错误）

---

### 完整示例：端到端标准化工作流

```typescript
async function standardizedKnowledgeManagement(
  entities: any[],
  memoryFileName: string,
  content: string
) {
  // Step 1: 健康检查
  const health = await airis-exec({
    tool: "gateway-control:health"
  });

  if (!health.ok) {
    throw new Error("Gateway 不可用");
  }

  // Step 2: 发现工具
  const memoryTools = await airis-find({ query: "memory" });
  const serenaTools = await airis-find({ query: "serena" });
  console.log(`Memory: ${memoryTools.length} 工具, Serena: ${serenaTools.length} 工具`);

  // Step 3: 验证参数
  const entitiesSchema = await airis-schema({
    tool: "memory:create_entities"
  });

  // Step 4: 创建知识图谱实体
  const createdEntities = await airis-exec({
    tool: "memory:create_entities",
    arguments: {
      entities: entities // 每个实体必须包含 observations
    }
  });

  console.log(`✅ 创建了 ${createdEntities.length} 个实体`);

  // Step 5: 保存详细文档到 Serena
  await airis-exec({
    tool: "serena:write_memory",
    arguments: {
      memory_file_name: memoryFileName,
      content: content
    }
  });

  console.log(`✅ 文档已保存: ${memoryFileName}`);

  return { entities: createdEntities };
}
```

---

## ⚙️ 服务运行模式

### MCP 服务器特性

本 skill 使用 2 个 MCP 服务器，运行模式不同：

| 服务器 | 工具数 | 运行模式 | 启动延迟 | 首次调用建议 |
|--------|--------|---------|---------|-------------|
| **memory** | 9 | HOT 🔥 | 无延迟 | 即时可用 |
| **serena** | 23 | COLD ❄️ | 2-5 秒 | 使用前检查健康状态 |

### 混合模式说明

**本 skill 的特殊性**:
- Memory (HOT) + Serena (COLD) 混合使用
- Memory 操作即时响应，Serena 首次调用需等待
- 建议先操作 Memory（无延迟），再操作 Serena（可能有延迟）

### 性能优化建议

#### 对于 HOT 模式服务器（Memory）:

1. **可以直接调用，无需预热**
   ```typescript
   // ✅ 直接调用 Memory，无需等待
   const entities = await airis-exec({
     tool: "memory:create_entities",
     arguments: { entities: [...] }
   });
   ```

2. **适合高频率调用**
   ```typescript
   // ✅ 批量创建实体，所有调用都是即时响应
   for (const entity of entities) {
     await airis-exec({
       tool: "memory:create_entities",
       arguments: { entities: [entity] }
     });
   }
   ```

#### 对于 COLD 模式服务器（Serena）:

1. **首次调用前预期延迟**
   ```typescript
   // 首次调用 Serena 可能需要等待
   try {
     const result = await airis-exec({
       tool: "serena:write_memory",
       arguments: { memory_file_name: "...", content: "..." }
     });
   } catch (error) {
     if (error.message.includes("server not ready")) {
       console.log("Serena 正在启动，等待 3 秒后重试...");
       await sleep(3000);
       // 重试
     }
   }
   ```

2. **批量操作时复用服务**
   ```typescript
   // ✅ 批量写入，首次调用后 Serena 已启动
   const files = ["doc1.md", "doc2.md", "doc3.md"];
   for (const file of files) {
     await airis-exec({
       tool: "serena:write_memory",
       arguments: {
         memory_file_name: file,
         content: generateContent(file)
       }
     });
   }
   ```

---

## 🔄 统一错误处理

### 错误分类体系

本 skill 的错误可分为 4 大类：

#### 1. 参数错误 → 使用 airis-schema 预验证

**典型错误**:
```
Error: 'observations' is required in entities
Error: Parameter 'filename' should be 'memory_file_name'
Error: Invalid entityType
Error: Invalid relationType
```

**处理策略**:
```typescript
// ✅ 推荐：执行前验证
const entitiesSchema = await airis-schema({
  tool: "memory:create_entities"
});

// 检查 observations 字段
for (const entity of entities) {
  if (!entity.observations || entity.observations.length === 0) {
    throw new Error(`实体 "${entity.name}" 缺少 observations 字段`);
  }
}

// 检查 entityType
const validEntityTypes = ["Concept", "Component", "Person", "Product", "Document"];
for (const entity of entities) {
  if (!validEntityTypes.includes(entity.entityType)) {
    throw new Error(`无效的 entityType: ${entity.entityType}`);
  }
}

// 执行创建
await airis-exec({
  tool: "memory:create_entities",
  arguments: { entities: entities }
});
```

**预防措施**:
- Memory: 总是为实体提供 `observations` 数组
- Serena: 使用 `memory_file_name` 而非 `filename`
- Memory: 使用标准的 `entityType` 和 `relationType`
- 使用 `airis-schema` 验证参数结构

---

#### 2. Gateway 错误 → 检查健康状态

**典型错误**:
```
Error: Failed to connect to AIRIS MCP Gateway
Error: Memory/Serena not found
```

**处理策略**:
```typescript
try {
  const health = await airis-exec({
    tool: "gateway-control:health"
  });

  if (!health.ok) {
    throw new Error("Gateway 不健康");
  }

  // 验证 Memory 和 Serena 可用
  const servers = await airis-exec({
    tool: "gateway-control:list-servers"
  });

  const requiredServers = ["memory", "serena"];
  const missingServers = requiredServers.filter(
    name => !servers.find(s => s.name === name)
  );

  if (missingServers.length > 0) {
    throw new Error(`缺少服务器: ${missingServers.join(", ")}`);
  }

} catch (error) {
  console.error("Gateway 错误:", error.message);

  throw new Error(`
    AIRIS MCP Gateway 不可用。请检查：
    1. Gateway 是否正在运行
    2. Memory 和 Serena 是否已安装
    3. 网络连接是否正常
  `);
}
```

---

#### 3. 工具执行错误 → 具体错误具体处理

**典型错误**:
```
Error: Entity already exists
Error: Relation target not found
Error: Memory file too large
```

**处理策略**:

**实体已存在**:
```typescript
try {
  await airis-exec({
    tool: "memory:create_entities",
    arguments: {
      entities: [{ name: "React", entityType: "Framework", observations: ["..."] }]
    }
  });
} catch (error) {
  if (error.message.includes("already exists")) {
    console.log("实体已存在，跳过创建");
    // 或者更新实体
  } else {
    throw error;
  }
}
```

**关系目标未找到**:
```typescript
try {
  await airis-exec({
    tool: "memory:create_relations",
    arguments: {
      relations: [
        { from: "React", to: "Unknown", relationType: "depends-on" }
      ]
    }
  });
} catch (error) {
  if (error.message.includes("not found")) {
    console.log("目标实体不存在，先创建实体");
    // 先创建目标实体，再创建关系
  } else {
    throw error;
  }
}
```

**Serena 内容过大**:
```typescript
try {
  await airis-exec({
    tool: "serena:write_memory",
    arguments: {
      memory_file_name: "large-doc.md",
      content: largeContent
    }
  });
} catch (error) {
  if (error.message.includes("too large")) {
    // 分段保存
    const chunks = splitContent(largeContent, 50000);
    for (const [i, chunk] of chunks.entries()) {
      await airis-exec({
        tool: "serena:write_memory",
        arguments: {
          memory_file_name: `large-doc-part-${i + 1}.md`,
          content: chunk
        }
      });
    }
  } else {
    throw error;
  }
}
```

---

#### 4. 服务不可用 → 验证安装和重试

**典型错误**:
```
Error: Server 'memory' not found
Error: Server 'serena' not ready
```

**处理策略**:

**服务器未安装**:
```typescript
const servers = await airis-exec({
  tool: "gateway-control:list-servers"
});

const requiredServers = ["memory", "serena"];
const missingServers = requiredServers.filter(
  name => !servers.find(s => s.name === name)
);

if (missingServers.length > 0) {
  throw new Error(`
    缺少必需的 MCP 服务器: ${missingServers.join(", ")}

    请安装：
    1. 检查 AIRIS MCP Gateway 配置
    2. 安装 Memory 和 Serena MCP 服务器
    3. 重启 Gateway
  `);
}
```

**Serena 未就绪（COLD 模式）**:
```typescript
async function waitForSerenaReady(maxWaitTime = 10000) {
  const startTime = Date.now();

  while (Date.now() - startTime < maxWaitTime) {
    const servers = await airis-exec({
      tool: "gateway-control:list-servers"
    });

    const serena = servers.find(s => s.name === "serena");

    if (serena && serena.ready) {
      return true;
    }

    console.log(`⏳ 等待 Serena 就绪...`);
    await sleep(2000);
  }

  return false;
}

// 使用示例
const ready = await waitForSerenaReady();
if (!ready) {
  throw new Error("Serena 服务器启动超时");
}
```

---

### 完整错误处理示例

```typescript
async function robustKnowledgeManagement(
  entities: any[],
  relations: any[],
  memoryFile: string,
  content: string
) {
  try {
    // 1. 健康检查
    const health = await airis-exec({
      tool: "gateway-control:health"
    });

    if (!health.ok) {
      throw new Error("GATEWAY_UNHEALTHY");
    }

    // 2. 验证 Memory 和 Serena 可用性
    const servers = await airis-exec({
      tool: "gateway-control:list-servers"
    });

    const memory = servers.find(s => s.name === "memory");
    const serena = servers.find(s => s.name === "serena");

    if (!memory || !serena) {
      throw new Error("SERVERS_MISSING");
    }

    // 3. 参数验证
    for (const entity of entities) {
      if (!entity.observations || entity.observations.length === 0) {
        throw new Error(`实体 "${entity.name}" 缺少 observations`);
      }
    }

    // 4. 创建实体（带重试）
    let createdEntities;
    try {
      createdEntities = await execWithRetry(
        "memory:create_entities",
        { entities: entities },
        3
      );
    } catch (error) {
      if (error.message.includes("already exists")) {
        console.log("部分实体已存在，继续...");
      } else {
        throw error;
      }
    }

    // 5. 创建关系（带重试）
    if (relations.length > 0) {
      await execWithRetry(
        "memory:create_relations",
        { relations: relations },
        3
      );
    }

    // 6. 保存到 Serena（带重试和分段处理）
    if (content.length > 50000) {
      const chunks = splitContent(content, 50000);
      for (const [i, chunk] of chunks.entries()) {
        await airis-exec({
          tool: "serena:write_memory",
          arguments: {
            memory_file_name: `${memoryFile}-part-${i + 1}.md`,
            content: chunk
          }
        });
      }
    } else {
      await airis-exec({
        tool: "serena:write_memory",
        arguments: {
          memory_file_name: memoryFile,
          content: content
        }
      });
    }

    return { entities: createdEntities, relations: relations.length };

  } catch (error) {
    // 统一错误处理
    console.error("知识管理失败:", error);

    if (error.message === "GATEWAY_UNHEALTHY") {
      throw new Error("AIRIS MCP Gateway 不可用");
    } else if (error.message === "SERVERS_MISSING") {
      throw new Error("Memory 或 Serena 未安装");
    } else if (error.message.includes("observations")) {
      throw new Error("实体缺少必需的 observations 字段");
    } else {
      throw new Error(`操作失败: ${error.message}`);
    }
  }
}
```

---

## 📚 参考文档

### References 文件

本 skill 包含以下参考文档（在 `references/` 目录中）:

- **entity-types.md** (~60 行) - 实体类型详解
  - 内容: 5 种实体类型（Concept, Component, Person, Product, Document）、使用场景、命名规范
  - 何时阅读: 不确定应该使用哪种实体类型时

- **relation-patterns.md** (~60 行) - 关系模式最佳实践
  - 内容: 6 种关系类型详解、使用场景、示例模式、常见错误
  - 何时阅读: 需要建立复杂关系网络时

---

## 🔗 相关资源

**MCP 服务器文档**:
- [Memory MCP](../../ai_workflow/docs/airis-mcp-gateway/servers/MEMORY.md) - 知识图谱管理
- [Serena MCP](../../ai_workflow/docs/airis-mcp-gateway/servers/SERENA.md) - 项目记忆管理

**AIRIS MCP Gateway**:
- [完整指南](../../ai_workflow/docs/airis-mcp-gateway/README.md)
- [快速参考](../../ai_workflow/docs/airis-mcp-gateway/QUICK_REFERENCE.md)

**相关 Skills**:
- airis-web-research - Web 研究和内容保存（Serena 记忆）
- airis-project-indexing - 项目索引和分析

---

## 📊 性能和限制

**性能考虑**:
- 创建实体: ~1-2 秒/批次（批量创建更快）
- 创建关系: ~1-2 秒/批次
- 搜索节点: ~2-3 秒/查询
- Serena 写入: ~0.5-1 秒/文件
- **总耗时**: 约 3-8 秒/完整流程

**限制条件**:
- Memory 实体名称: 建议 < 100 字符
- Memory observations: 建议每个实体 1-10 个观察
- Serena 记忆文件: 建议 < 50KB/文件
- 知识图谱规模: 建议 < 1000 个实体（性能考虑）

**最佳实践**:
- 批量创建实体（一次调用创建多个）而非逐个创建
- 使用语义化的实体命名（易于搜索和理解）
- 定期清理过时的知识图谱节点
- Serena 记忆文件使用日期后缀便于版本追踪
- 组合使用 Memory（结构化）+ Serena（文档化）获得最佳效果

---

**版本**: 1.0.0
**最后更新**: 2025-12-30
**作者**: Hao
