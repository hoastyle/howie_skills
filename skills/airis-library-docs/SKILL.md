---
name: airis-library-docs
description: 库文档查询助手，使用 Context7 MCP 查询官方库文档（React、Vue、Tailwind 等 50+ 库）。支持库 ID 解析和智能文档检索。适用于 API 文档查询、框架学习、最佳实践查找等场景。简化两步流程：resolve-library-id → query-docs。
---

# AIRIS Library Docs Query Helper

**MCP 服务器**: context7
**复杂度**: simple
**预估行数**: 200

---

## 🎯 触发条件

### 何时使用这个 Skill

**主要场景**:
- **API 文档查询**: 快速查找框架/库的 API 文档
- **框架学习**: 学习 React、Vue、Angular 等框架的核心概念
- **最佳实践查找**: 查询官方推荐的最佳实践
- **配置参考**: 查找工具配置选项（Vite、Webpack、TypeScript）
- **版本差异**: 了解不同版本的 API 差异

**关键词触发**:
- "查询文档"、"官方文档"、"API 文档"
- "React 文档"、"Vue 文档"、"Tailwind 文档"
- "如何使用"、"配置方法"、"最佳实践"
- "Context7"、"library docs"

**典型用户请求**:
```
"查询 React Hooks 的官方文档"
"Vue 3 Composition API 怎么用？"
"Tailwind CSS v4 有什么新特性？"
"TypeScript 的 Utility Types 文档"
```

---

## 📋 两步工作流程

### Phase 1: 解析库 ID

**功能**: 将库名称转换为 Context7 的库 ID

**为什么需要这一步**:
Context7 使用内部库 ID 而非库名称，需要先解析

**执行解析**:
```typescript
// Step 1: 解析库 ID
const library = await airis-exec({
  tool: "context7:resolve-library-id",
  arguments: {
    library_name: "React"
  }
});

// 返回
// { library_id: "react", version: "18.2" }
```

**参数说明**:
- `library_name` (必需) - 库名称（不区分大小写）
  - 可以是: "React", "react", "REACT"
  - 支持简写: "TS" → "TypeScript"

**返回结果**:
```json
{
  "library_id": "react",
  "version": "18.2",
  "name": "React"
}
```

---

### Phase 2: 查询文档

**功能**: 使用库 ID 查询具体的文档内容

**执行查询**:
```typescript
// Step 2: 查询文档
const docs = await airis-exec({
  tool: "context7:query-docs",
  arguments: {
    library_id: "react",           // 使用 Step 1 的 library_id
    query: "useState hook usage"
  }
});
```

**参数说明**:
- `library_id` (必需) - 库 ID（来自 Step 1）
- `query` (必需) - 查询内容（自然语言）

**返回结果**:
```json
{
  "results": [
    {
      "title": "useState Hook",
      "url": "https://react.dev/reference/react/useState",
      "content": "useState is a React Hook that lets you add state to functional components...",
      "relevance": 0.95
    }
  ]
}
```

---

## 💻 完整示例

### 示例 1: 查询 React Hooks

**用户需求**:
```
"查询 React useEffect hook 的用法"
```

**执行步骤**:

```typescript
// Step 1: 解析 React 库 ID
const reactLibrary = await airis-exec({
  tool: "context7:resolve-library-id",
  arguments: {
    library_name: "React"
  }
});

// Step 2: 查询 useEffect 文档
const useEffectDocs = await airis-exec({
  tool: "context7:query-docs",
  arguments: {
    library_id: reactLibrary.library_id,
    query: "useEffect hook usage examples"
  }
});

// Step 3: 提取并展示结果
const mainDoc = useEffectDocs.results[0];

console.log(`
📚 ${mainDoc.title}

${mainDoc.content}

🔗 查看完整文档: ${mainDoc.url}
`);

// 可选：保存到 Serena 记忆
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "react-useeffect-notes.md",
    content: `# React useEffect Hook

## 概述
${mainDoc.content}

## 参考链接
${mainDoc.url}

---
**查询日期**: ${new Date().toISOString().split('T')[0]}
`
  }
});
```

**预期输出**:
```
📚 useEffect Hook

useEffect is a React Hook that lets you synchronize a component with an external system...

🔗 查看完整文档: https://react.dev/reference/react/useEffect
```

---

### 示例 2: 查询 Tailwind CSS 配置

**用户需求**:
```
"Tailwind CSS 如何自定义主题颜色？"
```

**执行步骤**:

```typescript
// Step 1: 解析 Tailwind CSS 库 ID
const tailwindLibrary = await airis-exec({
  tool: "context7:resolve-library-id",
  arguments: {
    library_name: "Tailwind CSS"
  }
});

// Step 2: 查询主题配置文档
const themeDocs = await airis-exec({
  tool: "context7:query-docs",
  arguments: {
    library_id: tailwindLibrary.library_id,
    query: "customizing theme colors configuration"
  }
});

// Step 3: 提取配置示例
const configDoc = themeDocs.results[0];

console.log(`
🎨 Tailwind 主题颜色自定义

${configDoc.content}

💡 示例代码:
\`\`\`javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#FF6B6B',
        secondary: '#4ECDC4'
      }
    }
  }
}
\`\`\`

🔗 完整文档: ${configDoc.url}
`);
```

---

## ⚠️ 常见陷阱和解决方案

### 陷阱 1: 直接使用库名称而非库 ID

**错误现象**:
```
Error: Invalid library_id: "React"
```

**原因分析**:
`query-docs` 工具需要库 ID（如 "react"），而非库名称（"React"）

**解决方案**:
```typescript
// ❌ 错误：直接使用库名称
await context7:query-docs({
  library_id: "React",           // 错误！应该是 "react"
  query: "..."
});

// ✅ 正确：先解析库 ID
const lib = await context7:resolve-library-id({
  library_name: "React"
});

await context7:query-docs({
  library_id: lib.library_id,    // 正确！使用解析后的 ID
  query: "..."
});
```

---

### 陷阱 2: 查询过于宽泛

**错误现象**:
返回的文档不够具体或相关性低

**原因分析**:
查询关键词太宽泛，无法精确匹配

**解决方案**:
```typescript
// ❌ 不推荐：查询过于宽泛
{
  query: "React"                 // 太宽泛，返回大量无关内容
}

// ✅ 推荐：具体的查询
{
  query: "React useState hook with TypeScript"  // 具体明确
}

// ✅ 推荐：包含上下文
{
  query: "Vue 3 Composition API setup function lifecycle"
}
```

**查询技巧**:
- 包含具体的 API 名称（如 "useState", "useEffect"）
- 添加上下文关键词（如 "TypeScript", "best practices"）
- 使用官方术语（如 "Composition API" 而非 "composition"）

---

## 🔌 AIRIS MCP Gateway 标准访问模式（完整版）

本章节展示完整的 AIRIS MCP Gateway 访问模式，确保工具使用的标准化和可靠性。

### 四步标准化工作流

#### Step 1: 工具发现 (airis-find)

使用 `airis-find` 发现 Context7 提供的工具：

```typescript
// 发现 Context7 工具
const context7Tools = await airis-find({
  query: "context7"
});
console.log("Context7 工具:", context7Tools.map(t => t.name));
// 输出: ["context7:resolve-library-id", "context7:query-docs"]
```

**为什么需要这一步？**
- 发现 Context7 的可用工具
- 确认工具名称拼写正确
- 验证 Context7 MCP 服务器已正确安装

---

#### Step 2: 参数验证 (airis-schema)

在执行前，使用 `airis-schema` 检查工具的参数要求：

```typescript
// 检查 resolve-library-id 参数
const resolveSchema = await airis-schema({
  tool: "context7:resolve-library-id"
});
console.log("必需参数:", resolveSchema.inputSchema.required);
// 输出: ["library_name"]

// 检查 query-docs 参数
const querySchema = await airis-schema({
  tool: "context7:query-docs"
});
console.log("查询工具参数:", querySchema.inputSchema.required);
// 输出: ["library_id", "query"]
```

**常见参数命名陷阱**（本 skill 涉及）:
- ⚠️ `library_id` 必须先通过 `resolve-library-id` 获取（不能直接使用库名称）
- ⚠️ `library_name` 不区分大小写，但建议使用官方名称
- ⚠️ `query` 应该具体明确，避免过于宽泛

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

console.log("可用服务器:", servers.map(s => s.name));

// 验证 Context7 已安装
const context7 = servers.find(s => s.name === "context7");

if (!context7) {
  throw new Error("Context7 服务器未安装");
}

if (context7.mode === "COLD" && !context7.ready) {
  console.log("⏳ 等待 Context7 启动（COLD 模式，需要 2-5 秒）...");
  await sleep(3000);
}

console.log("✅ Context7 已就绪");
```

**什么时候需要健康检查？**
- ✅ 首次使用 Context7（COLD 模式需要启动时间）
- ✅ 生产环境部署
- ✅ 批量查询多个库文档
- ⚠️ 单次快速查询时可以跳过（但要处理错误）

---

### 完整示例：端到端标准化工作流

```typescript
async function standardizedLibraryDocQuery(libraryName: string, query: string) {
  // Step 1: 健康检查
  const health = await airis-exec({
    tool: "gateway-control:health"
  });

  if (!health.ok) {
    throw new Error("Gateway 不可用");
  }

  // Step 2: 发现工具
  const tools = await airis-find({ query: "context7" });
  console.log(`发现 ${tools.length} 个 Context7 工具`);

  // Step 3: 验证参数
  const resolveSchema = await airis-schema({
    tool: "context7:resolve-library-id"
  });
  console.log("解析工具参数:", resolveSchema.inputSchema);

  // Step 4: 解析库 ID
  const library = await airis-exec({
    tool: "context7:resolve-library-id",
    arguments: {
      library_name: libraryName
    }
  });

  console.log(`库 ID 解析完成: ${library.library_id} (v${library.version})`);

  // Step 5: 查询文档
  const docs = await airis-exec({
    tool: "context7:query-docs",
    arguments: {
      library_id: library.library_id,
      query: query
    }
  });

  return { library, docs };
}
```

---

## ⚙️ 服务运行模式

### MCP 服务器特性

本 skill 使用的 Context7 为 **COLD 模式**：

| 服务器 | 工具数 | 运行模式 | 启动延迟 | 首次调用建议 |
|--------|--------|---------|---------|-------------|
| **context7** | 2 | COLD ❄️ | 2-5 秒 | 使用前检查健康状态 |

### COLD 模式说明

**COLD 模式服务器特点**:
- ❄️ 按需启动，首次调用需要 2-5 秒启动时间
- 💤 长时间不用会自动休眠
- 🔄 重新启动需要等待
- 📊 适合批量操作（复用已启动的服务）

**vs HOT 模式**（不适用于本 skill）:
- 🔥 常驻内存，即时响应
- ⚡ 无启动延迟
- 🎯 适合高频率调用

### 性能优化建议

#### 对于 COLD 模式服务器（Context7）:

1. **首次调用前执行健康检查**
   ```typescript
   const health = await airis-exec({ tool: "gateway-control:health" });
   ```

2. **预期并处理启动延迟**
   ```typescript
   // 首次调用可能需要等待
   try {
     const result = await airis-exec({
       tool: "context7:resolve-library-id",
       arguments: { library_name: "React" }
     });
   } catch (error) {
     if (error.message.includes("server not ready")) {
       console.log("Context7 正在启动，等待 3 秒后重试...");
       await sleep(3000);
       // 重试
       const result = await airis-exec({
         tool: "context7:resolve-library-id",
         arguments: { library_name: "React" }
       });
     }
   }
   ```

3. **实现重试机制**（推荐）
   ```typescript
   async function execWithRetry(tool, arguments, maxRetries = 3) {
     for (let i = 0; i < maxRetries; i++) {
       try {
         return await airis-exec({ tool, arguments });
       } catch (error) {
         if (i === maxRetries - 1) throw error;
         console.log(`重试 ${i + 1}/${maxRetries}...`);
         await sleep(2000);
       }
     }
   }
   ```

4. **批量查询时复用已启动的服务**
   ```typescript
   // ✅ 高效：批量查询复用 Context7 服务
   const libraries = ["React", "Vue", "Angular"];

   for (const libName of libraries) {
     // 首次调用后，Context7 已启动，后续调用无延迟
     const library = await airis-exec({
       tool: "context7:resolve-library-id",
       arguments: { library_name: libName }
     });

     const docs = await airis-exec({
       tool: "context7:query-docs",
       arguments: {
         library_id: library.library_id,
         query: "getting started"
       }
     });

     console.log(`${libName} 文档查询完成`);
   }
   ```

### 服务可用性检查

```typescript
async function ensureContext7Available() {
  const servers = await airis-exec({
    tool: "gateway-control:list-servers"
  });

  const context7 = servers.find(s => s.name === "context7");

  if (!context7) {
    throw new Error(`
      Context7 服务器未安装

      请安装 Context7：
      1. 检查 AIRIS MCP Gateway 配置
      2. 安装 Context7 MCP 服务器
      3. 重启 Gateway
    `);
  }

  if (context7.mode === "COLD" && !context7.ready) {
    console.log(`⏳ 等待 Context7 启动（COLD 模式）...`);
    await sleep(3000);

    // 验证服务器是否已就绪
    const updatedServers = await airis-exec({
      tool: "gateway-control:list-servers"
    });
    const updatedContext7 = updatedServers.find(s => s.name === "context7");

    if (!updatedContext7.ready) {
      throw new Error(`Context7 启动失败`);
    }
  }

  console.log(`✅ Context7 已就绪（2 个工具可用）`);
  return context7;
}

// 使用示例
await ensureContext7Available();
```

---

## 🔄 统一错误处理

### 错误分类体系

本 skill 的错误可分为 4 大类：

#### 1. 参数错误 → 使用 airis-schema 预验证

**典型错误**:
```
Error: Invalid library_id: "React"
Error: Required parameter 'library_name' is missing
Error: Library not found
```

**处理策略**:
```typescript
// ✅ 推荐：执行前验证
const resolveSchema = await airis-schema({
  tool: "context7:resolve-library-id"
});
const requiredParams = resolveSchema.inputSchema.required;

// 检查必需参数
if (!arguments.library_name) {
  throw new Error("缺少必需参数: library_name");
}

// 执行解析
const library = await airis-exec({
  tool: "context7:resolve-library-id",
  arguments: { library_name: arguments.library_name }
});

// 验证查询参数
if (!library.library_id) {
  throw new Error(`库 "${arguments.library_name}" 不在支持列表中`);
}
```

**预防措施**:
- 总是使用 `airis-schema` 查询正确的参数名
- 使用 `resolve-library-id` 而非直接使用库名称
- 参考支持的库列表（references/supported-libraries.md）
- 查询要具体明确

---

#### 2. Gateway 错误 → 检查健康状态

**典型错误**:
```
Error: Failed to connect to AIRIS MCP Gateway
Error: Context7 not found
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

  // 验证 Context7 可用
  const servers = await airis-exec({
    tool: "gateway-control:list-servers"
  });

  if (!servers.some(s => s.name === "context7")) {
    throw new Error("Context7 未安装");
  }

} catch (error) {
  console.error("Gateway 错误:", error.message);

  // 提供用户友好的错误信息
  throw new Error(`
    AIRIS MCP Gateway 不可用。请检查：
    1. Gateway 是否正在运行（http://localhost:9400/health）
    2. Context7 是否已安装
    3. 网络连接是否正常
  `);
}
```

**预防措施**:
- 工作流开始前执行健康检查
- 验证 Context7 在服务器列表中
- 提供清晰的错误提示和修复建议

---

#### 3. 工具执行错误 → 具体错误具体处理

**典型错误**:
```
Error: Library not found: "unknown-library"
Error: Query returned no results
Error: API rate limit exceeded
```

**处理策略**:

**库不存在（Library not found）**:
```typescript
try {
  const library = await airis-exec({
    tool: "context7:resolve-library-id",
    arguments: {
      library_name: "UnknownLibrary"
    }
  });
} catch (error) {
  if (error.message.includes("not found")) {
    console.log("库不在 Context7 支持列表中");

    throw new Error(`
      库 "UnknownLibrary" 不在 Context7 支持列表中

      Context7 支持 50+ 主流库，包括：
      - React, Vue, Angular, Svelte
      - Tailwind CSS, Material-UI
      - TypeScript, Vite, Webpack
      - 等等

      请使用 airis-web-research skill 查询非官方文档
    `);
  }
  throw error;
}
```

**查询无结果（No results）**:
```typescript
const docs = await airis-exec({
  tool: "context7:query-docs",
  arguments: {
    library_id: "react",
    query: "vague query"
  }
});

if (!docs.results || docs.results.length === 0) {
  console.log("查询无结果，尝试更具体的查询...");

  // 建议更具体的查询
  throw new Error(`
    未找到相关文档。请尝试：
    1. 使用更具体的 API 名称（如 "useState" 而非 "state"）
    2. 添加上下文关键词（如 "TypeScript", "best practices"）
    3. 使用官方术语（如 "Composition API" 而非 "composition"）

    示例查询：
    - "React useState hook with TypeScript"
    - "Vue 3 Composition API setup function"
    - "Tailwind CSS responsive design utilities"
  `);
}
```

**API 速率限制（Rate limit）**:
```typescript
try {
  const docs = await airis-exec({
    tool: "context7:query-docs",
    arguments: { library_id: "react", query: "..." }
  });
} catch (error) {
  if (error.message.includes("rate limit")) {
    console.log("Context7 API 速率限制，等待 60 秒...");
    await sleep(60000);
    // 重试
    return await airis-exec({
      tool: "context7:query-docs",
      arguments: { library_id: "react", query: "..." }
    });
  }
  throw error;
}
```

---

#### 4. 服务不可用 → 重试或回退

**典型错误**:
```
Error: Server 'context7' not found
Error: Server 'context7' not ready
```

**处理策略**:

**服务器未安装**:
```typescript
const servers = await airis-exec({
  tool: "gateway-control:list-servers"
});

const context7 = servers.find(s => s.name === "context7");

if (!context7) {
  throw new Error(`
    Context7 服务器未安装

    请按以下步骤安装：
    1. 检查 AIRIS MCP Gateway 配置文件
    2. 添加 Context7 服务器配置
    3. 配置 Context7 API Key（如需要）
    4. 重启 AIRIS MCP Gateway
    5. 验证安装：airis-gateway list-servers

    配置示例：
    {
      "mcpServers": {
        "context7": {
          "command": "context7-mcp",
          "env": {
            "CONTEXT7_API_KEY": "your-api-key"
          }
        }
      }
    }
  `);
}
```

**服务器未就绪（COLD 模式）**:
```typescript
async function waitForContext7Ready(maxWaitTime = 10000) {
  const startTime = Date.now();

  while (Date.now() - startTime < maxWaitTime) {
    const servers = await airis-exec({
      tool: "gateway-control:list-servers"
    });

    const context7 = servers.find(s => s.name === "context7");

    if (context7 && context7.ready) {
      return true;
    }

    console.log(`⏳ 等待 Context7 就绪...`);
    await sleep(2000);
  }

  return false;
}

// 使用示例
const ready = await waitForContext7Ready();
if (!ready) {
  throw new Error("Context7 服务器启动超时");
}
```

**回退方案**:
```typescript
// 主方案：使用 Context7 查询官方文档
try {
  const library = await airis-exec({
    tool: "context7:resolve-library-id",
    arguments: { library_name: "React" }
  });

  const docs = await airis-exec({
    tool: "context7:query-docs",
    arguments: {
      library_id: library.library_id,
      query: "useState"
    }
  });
} catch (error) {
  console.log("Context7 不可用，回退到 Web 搜索...");

  // 回退方案：使用 Tavily Web 搜索
  const searchResults = await airis-exec({
    tool: "tavily:search",
    arguments: {
      query: "React useState official documentation",
      include_domains: ["react.dev"]
    }
  });

  console.log("使用 Web 搜索结果作为替代");
  return searchResults;
}
```

---

### 完整错误处理示例

```typescript
async function robustLibraryDocQuery(libraryName: string, query: string) {
  try {
    // 1. 健康检查
    const health = await airis-exec({
      tool: "gateway-control:health"
    });

    if (!health.ok) {
      throw new Error("GATEWAY_UNHEALTHY");
    }

    // 2. 验证 Context7 可用性
    await ensureContext7Available();

    // 3. 解析库 ID（带错误处理）
    let library;
    try {
      library = await execWithRetry(
        "context7:resolve-library-id",
        { library_name: libraryName },
        3
      );
    } catch (error) {
      if (error.message.includes("not found")) {
        throw new Error(`库 "${libraryName}" 不在 Context7 支持列表中，请使用 airis-web-research`);
      }
      throw error;
    }

    console.log(`库 ID: ${library.library_id} (v${library.version})`);

    // 4. 查询文档（带错误处理）
    let docs;
    try {
      docs = await execWithRetry(
        "context7:query-docs",
        {
          library_id: library.library_id,
          query: query
        },
        3
      );
    } catch (error) {
      if (error.message.includes("rate limit")) {
        console.log("API 速率限制，等待后重试...");
        await sleep(60000);
        docs = await airis-exec({
          tool: "context7:query-docs",
          arguments: {
            library_id: library.library_id,
            query: query
          }
        });
      } else {
        throw error;
      }
    }

    // 5. 验证结果
    if (!docs.results || docs.results.length === 0) {
      throw new Error(`未找到相关文档。请使用更具体的查询关键词`);
    }

    return { library, docs };

  } catch (error) {
    // 统一错误处理
    console.error("文档查询失败:", error);

    if (error.message === "GATEWAY_UNHEALTHY") {
      throw new Error("AIRIS MCP Gateway 不可用，请检查服务状态");
    } else if (error.message.includes("not found")) {
      throw new Error(`库不在支持列表中，建议使用 airis-web-research`);
    } else if (error.message.includes("rate limit")) {
      throw new Error("API 速率限制，请稍后重试");
    } else {
      throw new Error(`查询失败: ${error.message}`);
    }
  }
}
```

---

## 📚 支持的库列表

Context7 支持 50+ 主流前端库和工具：

### 前端框架
- **React** (react) - v18.2+
- **Vue** (vue) - v3.3+
- **Angular** (angular) - v16+
- **Svelte** (svelte) - v4+
- **Next.js** (nextjs) - v14+
- **Nuxt** (nuxt) - v3+

### UI 框架
- **Tailwind CSS** (tailwindcss) - v3.4+
- **Material-UI** (mui) - v5+
- **Ant Design** (antd) - v5+
- **Chakra UI** (chakraui) - v2+

### 工具库
- **TypeScript** (typescript) - v5+
- **Vite** (vite) - v5+
- **Webpack** (webpack) - v5+
- **ESLint** (eslint) - v8+
- **Prettier** (prettier) - v3+

### 状态管理
- **Redux** (redux) - v5+
- **Zustand** (zustand) - v4+
- **Pinia** (pinia) - v2+
- **Jotai** (jotai) - v2+

**完整列表**: 查看 `references/supported-libraries.md`

---

## 📚 参考文档

### References 文件

本 skill 包含以下参考文档（在 `references/` 目录中）:

- **supported-libraries.md** (~120 行) - 支持的库完整列表
  - 内容: 50+ 库列表、库 ID 映射、版本信息、官网链接
  - 何时阅读: 查找支持的库或确认库 ID

- **query-patterns.md** (~80 行) - 高效查询模式
  - 内容: 查询技巧、关键词选择、精确 vs 宽泛查询对比、常见查询示例
  - 何时阅读: 查询结果不理想时

---

## 🔗 相关资源

**MCP 服务器文档**:
- [Context7 MCP](../../ai_workflow/docs/airis-mcp-gateway/servers/CONTEXT7.md) - 库文档查询详细文档

**AIRIS MCP Gateway**:
- [完整指南](../../ai_workflow/docs/airis-mcp-gateway/README.md)
- [工具索引](../../ai_workflow/docs/airis-mcp-gateway/TOOL_INDEX.md)

**相关 Skills**:
- airis-web-research - Web 研究（用于非官方文档）
- airis-knowledge-mgmt - 知识整理（保存学习笔记）

---

## 📊 性能和限制

**性能考虑**:
- 解析库 ID: ~0.5-1 秒
- 查询文档: ~1-2 秒
- **总耗时**: 约 2-3 秒/完整查询

**限制条件**:
- 支持的库: ~50+ 个主流库
- 查询结果: 通常返回 1-5 个最相关结果
- 内容长度: 每个结果 ~500-2000 字符
- API 限制: 通常 60 requests/minute（根据配置不同）

**最佳实践**:
- 缓存库 ID（同一个库多次查询时复用）
- 使用具体的查询关键词提高准确性
- 结合 Serena 保存常用文档引用
- 对于不支持的库，使用 airis-web-research 查询
- 查询前先确认库是否在支持列表中

---

**版本**: 1.0.0
**最后更新**: 2025-12-30
**作者**: Hao
