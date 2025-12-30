---
name: airis-web-research
description: 完整的 Web 研究流程助手，使用 Tavily 搜索最新信息、Fetch 提取网页内容、Serena 保存到项目记忆。适用于技术调研、API 文档查询、竞品分析、市场研究等需要系统整理在线信息的场景。自动处理搜索、提取、保存三个阶段，确保研究结果结构化存储。
---

# AIRIS Web Research Helper

**MCP 服务器**: tavily, fetch, serena
**复杂度**: medium
**预估行数**: 250

---

## 🎯 触发条件

### 何时使用这个 Skill

**主要场景**:
- **技术调研**: 查询最新技术文档、框架教程、最佳实践
- **API 文档查询**: 获取官方 API 文档、使用示例
- **竞品分析**: 研究竞品功能、技术栈、用户反馈
- **市场研究**: 收集行业动态、趋势分析、统计数据
- **学习笔记**: 整理在线学习资料并保存到项目记忆

**关键词触发**:
- "web 搜索"、"在线查询"、"网上找"
- "技术调研"、"研究"、"了解"
- "最新信息"、"官方文档"
- "保存到记忆"、"整理资料"

**典型用户请求**:
```
"帮我研究一下 React Server Components 的最新进展"
"查询 OpenAI API 的官方文档并保存"
"了解一下目前主流的前端框架有哪些"
"整理关于微服务架构的最佳实践"
```

---

## 📋 工作流程

### 三阶段 Web 研究流程

#### Phase 1: 搜索发现（Tavily）

**功能**: 使用 Tavily MCP 搜索最新信息

**第一步：发现工具**
```typescript
// Step 1.1: 查找 Tavily 搜索工具
const searchTools = await airis-find({
  query: "tavily search"
});
// 返回: tavily:search, tavily:extract
```

**第二步：执行搜索**
```typescript
// Step 1.2: 执行 Web 搜索
const searchResults = await airis-exec({
  tool: "tavily:search",
  arguments: {
    query: "React Server Components 2025",
    search_depth: "advanced",        // basic | advanced
    max_results: 5,                  // 1-20
    include_domains: [],             // 可选：限制域名
    exclude_domains: []              // 可选：排除域名
  }
});
```

**参数说明**:
- `query` (必需) - 搜索查询，建议包含年份获取最新信息
- `search_depth` - 搜索深度
  - `basic`: 快速搜索，返回摘要
  - `advanced`: 深度搜索，提取完整内容
- `max_results` - 返回结果数量（1-20）
- `include_domains` - 仅搜索指定域名（如 ["react.dev", "github.com"]）
- `exclude_domains` - 排除特定域名

**返回结果**:
```json
{
  "results": [
    {
      "title": "React Server Components - Official Docs",
      "url": "https://react.dev/reference/rsc/server-components",
      "content": "概要内容...",
      "score": 0.95
    }
  ]
}
```

---

#### Phase 2: 内容提取（Tavily/Fetch）

**功能**: 提取完整网页内容（两种方式）

**方式 A：使用 Tavily Extract（推荐）**
```typescript
// Step 2.1: 提取特定 URL 的内容
const extractedContent = await airis-exec({
  tool: "tavily:extract",
  arguments: {
    urls: [
      "https://react.dev/reference/rsc/server-components",
      "https://nextjs.org/docs/app/building-your-application/rendering/server-components"
    ]
  }
});
```

**方式 B：使用 Fetch MCP**
```typescript
// Step 2.2: 获取 Markdown 格式的网页内容
const pageContent = await airis-exec({
  tool: "fetch:fetch",
  arguments: {
    url: "https://react.dev/reference/rsc/server-components",
    max_length: 50000,              // 最大内容长度
    start_index: 0,                 // 起始位置（分页用）
    raw: false                      // false: Markdown, true: HTML
  }
});
```

**选择建议**:
- **Tavily Extract**: 适合批量提取多个 URL，自动去噪
- **Fetch**: 适合单个 URL，保留完整 Markdown 格式

---

#### Phase 3: 记忆保存（Serena）

**功能**: 将研究结果保存到项目记忆

**⚠️ 关键陷阱：参数名称**
```typescript
// ❌ 错误：使用 filename
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    filename: "react-rsc-research.md",  // 错误！
    content: "..."
  }
});

// ✅ 正确：使用 memory_file_name
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "react-rsc-research.md",  // 正确！
    content: "..."
  }
});
```

**完整保存示例**:
```typescript
// Step 3: 保存研究结果到 Serena 记忆
const saveResult = await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "react-server-components-2025.md",
    content: `# React Server Components 研究

## 概述
${searchResults.results[0].content}

## 官方文档
${pageContent.content}

## 参考链接
${searchResults.results.map(r => `- [${r.title}](${r.url})`).join('\n')}

---
**研究日期**: ${new Date().toISOString().split('T')[0]}
**来源**: Tavily + Fetch
`
  }
});
```

---

## 💻 完整示例

### 示例 1: 技术框架调研

**用户需求**:
```
"帮我研究一下 Astro 框架，了解它的特点和使用场景，保存到项目记忆"
```

**执行步骤**:

```typescript
// Step 1: Tavily 搜索
const searchResults = await airis-exec({
  tool: "tavily:search",
  arguments: {
    query: "Astro framework features use cases 2025",
    search_depth: "advanced",
    max_results: 3
  }
});

// Step 2: 提取官网内容
const officialDocs = await airis-exec({
  tool: "fetch:fetch",
  arguments: {
    url: "https://astro.build",
    max_length: 30000,
    raw: false
  }
});

// Step 3: 整理并保存
const researchContent = `# Astro 框架研究

## 核心特点
${searchResults.results[0].content}

## 官方介绍
${officialDocs.content.substring(0, 5000)}

## 使用场景
${searchResults.results.map((r, i) => `### 场景 ${i+1}: ${r.title}\n${r.content}`).join('\n\n')}

## 参考资源
${searchResults.results.map(r => `- [${r.title}](${r.url})`).join('\n')}

---
**研究日期**: ${new Date().toISOString().split('T')[0]}
`;

await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "astro-framework-research.md",
    content: researchContent
  }
});
```

**预期输出**:
```
✅ 已保存研究结果到 .serena/memories/astro-framework-research.md
包含：
- Astro 核心特点
- 官方文档摘要
- 3 个使用场景
- 参考链接列表
```

---

### 示例 2: API 文档查询

**用户需求**:
```
"查询 Anthropic Claude API 的最新定价信息"
```

**执行步骤**:

```typescript
// Step 1: 精确搜索 Anthropic 官网
const pricingSearch = await airis-exec({
  tool: "tavily:search",
  arguments: {
    query: "Anthropic Claude API pricing 2025",
    include_domains: ["anthropic.com"],
    max_results: 2
  }
});

// Step 2: 提取定价页面
const pricingPage = await airis-exec({
  tool: "tavily:extract",
  arguments: {
    urls: [pricingSearch.results[0].url]
  }
});

// Step 3: 保存定价信息
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "claude-api-pricing-2025.md",
    content: `# Claude API 定价信息

${pricingPage.results[0].content}

**来源**: ${pricingSearch.results[0].url}
**更新日期**: ${new Date().toISOString().split('T')[0]}
`
  }
});
```

---

## ⚠️ 常见陷阱和解决方案

### 陷阱 1: Tavily API Key 未设置

**错误现象**:
```
Error: Tavily API key not found
```

**原因分析**:
Tavily MCP 需要在环境变量中设置 `TAVILY_API_KEY`

**解决方案**:
```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
export TAVILY_API_KEY="tvly-your-api-key-here"

# 或者在 MCP 配置文件中设置
# ~/.claude/mcp_servers/tavily.json
{
  "env": {
    "TAVILY_API_KEY": "tvly-your-api-key-here"
  }
}
```

---

### 陷阱 2: Serena 参数名称错误

**错误现象**:
```
Error: Unknown parameter 'filename'
```

**原因分析**:
Serena MCP 的参数名称与其他 MCP 服务器不同，使用 `memory_file_name` 而非 `filename`

**解决方案**:
```typescript
// ❌ 错误：使用 filename
{
  tool: "serena:write_memory",
  arguments: {
    filename: "research.md"  // 错误参数名
  }
}

// ✅ 正确：使用 memory_file_name
{
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "research.md"  // 正确参数名
  }
}
```

**验证方法**:
```typescript
// 使用 airis-schema 查看正确的参数名
const schema = await airis-schema({
  tool: "serena:write_memory"
});
console.log(schema.inputSchema);
```

---

### 陷阱 3: 内容过长超出 Serena 限制

**错误现象**:
```
Error: Content exceeds maximum length
```

**原因分析**:
单个记忆文件内容过长（通常 > 100KB）

**解决方案**:

**策略 A：分段保存**
```typescript
// 将长内容分成多个记忆文件
const sections = splitContentIntoSections(longContent, 50000);

for (const [index, section] of sections.entries()) {
  await airis-exec({
    tool: "serena:write_memory",
    arguments: {
      memory_file_name: `research-part-${index + 1}.md`,
      content: section
    }
  });
}
```

**策略 B：使用摘要**
```typescript
// 只保存关键信息和摘要
const summary = extractKeyPoints(longContent);

await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "research-summary.md",
    content: `# 研究摘要

${summary}

## 完整内容链接
${originalUrl}
`
  }
});
```

---

## 🔌 AIRIS MCP Gateway 标准访问模式（完整版）

本章节展示完整的 AIRIS MCP Gateway 访问模式，确保工具使用的标准化和可靠性。

### 四步标准化工作流

#### Step 1: 工具发现 (airis-find)

使用 `airis-find` 发现本 skill 使用的 MCP 工具：

```typescript
// 发现 Tavily 搜索工具
const tavilyTools = await airis-find({
  query: "tavily"
});
console.log("Tavily 工具:", tavilyTools.map(t => t.name));
// 输出: ["tavily:search", "tavily:extract"]

// 发现 Fetch 提取工具
const fetchTools = await airis-find({
  query: "fetch"
});
console.log("Fetch 工具:", fetchTools.map(t => t.name));
// 输出: ["fetch:fetch"]

// 发现 Serena 记忆工具
const serenaTools = await airis-find({
  query: "serena memory"
});
console.log("Serena 记忆工具:", serenaTools.map(t => t.name));
// 输出: ["serena:write_memory", "serena:read_memory", "serena:list_memories", ...]
```

**为什么需要这一步？**
- 发现新工具和功能
- 确认工具名称拼写
- 了解服务器提供的所有能力
- 验证 MCP 服务器已正确安装

---

#### Step 2: 参数验证 (airis-schema)

在执行前，使用 `airis-schema` 检查工具的参数要求：

```typescript
// 检查 Tavily 搜索参数
const tavilySearchSchema = await airis-schema({
  tool: "tavily:search"
});
console.log("必需参数:", tavilySearchSchema.inputSchema.required);
// 输出: ["query"]
console.log("可选参数:", Object.keys(tavilySearchSchema.inputSchema.properties));
// 输出: ["query", "search_depth", "max_results", "include_domains", "exclude_domains"]

// 检查 Serena 保存参数
const serenaWriteSchema = await airis-schema({
  tool: "serena:write_memory"
});
console.log("Serena 参数:", serenaWriteSchema.inputSchema.required);
// 输出: ["memory_file_name", "content"]
```

**常见参数命名陷阱**（本 skill 涉及）:
- ⚠️ `filename` ❌ vs `memory_file_name` ✅ (Serena)
- ⚠️ Tavily `query` 建议包含年份（如 "React 2025"）获取最新信息
- ⚠️ Tavily `search_depth` 影响响应时间（basic < 2s，advanced 2-5s）

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

// 验证本 skill 需要的服务器已启动
const requiredServers = ["tavily", "fetch", "serena"];
for (const serverName of requiredServers) {
  const server = servers.find(s => s.name === serverName);

  if (!server) {
    throw new Error(`服务器 ${serverName} 未安装`);
  }

  if (server.mode === "COLD" && !server.ready) {
    console.log(`⏳ 等待 ${serverName} 启动（COLD 模式，需要 2-5 秒）...`);
    await sleep(3000);
  }
}

console.log("✅ 所有必需的 MCP 服务器已就绪");
```

**什么时候需要健康检查？**
- ✅ 长时间运行的 workflow（如批量研究任务）
- ✅ 生产环境部署
- ✅ 首次使用 COLD 模式服务器
- ⚠️ 快速原型开发时可以跳过（但要处理错误）

---

### 完整示例：端到端标准化工作流

```typescript
async function standardizedWebResearch(topic: string) {
  // Step 1: 健康检查
  const health = await airis-exec({
    tool: "gateway-control:health"
  });

  if (!health.ok) {
    throw new Error("Gateway 不可用");
  }

  // Step 2: 发现工具
  const tools = await airis-find({ query: "tavily search" });
  const searchTool = tools.find(t => t.name === "tavily:search");

  if (!searchTool) {
    throw new Error("Tavily 搜索工具未找到");
  }

  // Step 3: 验证参数
  const schema = await airis-schema({ tool: searchTool.name });
  console.log("工具参数:", schema.inputSchema);

  // Step 4: 执行搜索
  const results = await airis-exec({
    tool: "tavily:search",
    arguments: {
      query: `${topic} 2025`,
      search_depth: "advanced",
      max_results: 5
    }
  });

  // Step 5: 保存到记忆
  await airis-exec({
    tool: "serena:write_memory",
    arguments: {
      memory_file_name: `research-${topic.toLowerCase().replace(/\s+/g, "-")}.md`,
      content: formatResearchResults(results)
    }
  });

  return results;
}
```

---

## ⚙️ 服务运行模式

### MCP 服务器特性

本 skill 使用的 3 个 MCP 服务器均为 **COLD 模式**：

| 服务器 | 工具数 | 运行模式 | 启动延迟 | 首次调用建议 |
|--------|--------|---------|---------|-------------|
| **tavily** | 4 | COLD ❄️ | 2-5 秒 | 使用前检查健康状态 |
| **fetch** | 1 | COLD ❄️ | 2-5 秒 | 首次调用可能失败，需重试 |
| **serena** | 23 | COLD ❄️ | 2-5 秒 | 项目激活需要额外时间 |

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

#### 对于 COLD 模式服务器（本 skill 使用的所有服务器）:

1. **首次调用前执行健康检查**
   ```typescript
   const health = await airis-exec({ tool: "gateway-control:health" });
   ```

2. **预期并处理启动延迟**
   ```typescript
   // 首次调用可能需要等待
   try {
     const result = await airis-exec({
       tool: "tavily:search",
       arguments: { query: "..." }
     });
   } catch (error) {
     if (error.message.includes("server not ready")) {
       console.log("服务器正在启动，等待 3 秒后重试...");
       await sleep(3000);
       // 重试
       const result = await airis-exec({
         tool: "tavily:search",
         arguments: { query: "..." }
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

4. **批量操作时复用已启动的服务**
   ```typescript
   // ✅ 高效：复用已启动的 Tavily 服务
   const topics = ["React", "Vue", "Angular"];
   for (const topic of topics) {
     await airis-exec({
       tool: "tavily:search",
       arguments: { query: topic }
     });
     // 后续调用无需启动延迟
   }

   // ❌ 低效：每次都可能触发启动
   // （如果服务器在调用之间休眠）
   ```

### 服务可用性检查

```typescript
async function ensureServerAvailable(serverName: string) {
  const servers = await airis-exec({
    tool: "gateway-control:list-servers"
  });

  const server = servers.find(s => s.name === serverName);

  if (!server) {
    throw new Error(`服务器 ${serverName} 不存在或未安装`);
  }

  if (server.mode === "COLD" && !server.ready) {
    console.log(`⏳ 等待 ${serverName} 启动（COLD 模式）...`);
    await sleep(3000);

    // 验证服务器是否已就绪
    const updatedServers = await airis-exec({
      tool: "gateway-control:list-servers"
    });
    const updatedServer = updatedServers.find(s => s.name === serverName);

    if (!updatedServer.ready) {
      throw new Error(`服务器 ${serverName} 启动失败`);
    }
  }

  return server;
}

// 使用示例
await ensureServerAvailable("tavily");
await ensureServerAvailable("serena");
```

---

## 🔄 统一错误处理

### 错误分类体系

本 skill 的错误可分为 4 大类：

#### 1. 参数错误 → 使用 airis-schema 预验证

**典型错误**:
```
Error: Invalid parameter 'filename'
Error: Required parameter 'memory_file_name' is missing
```

**处理策略**:
```typescript
// ✅ 推荐：执行前验证
const schema = await airis-schema({ tool: "serena:write_memory" });
const requiredParams = schema.inputSchema.required;

// 检查必需参数
if (!arguments.memory_file_name) {
  throw new Error(`缺少必需参数: memory_file_name`);
}

// 执行工具
await airis-exec({
  tool: "serena:write_memory",
  arguments: { /* 验证后的参数 */ }
});
```

**预防措施**:
- 总是使用 `airis-schema` 查询正确的参数名
- 参考本文档的"常见陷阱"章节
- 使用 TypeScript 类型定义（如果可用）

---

#### 2. Gateway 错误 → 检查健康状态

**典型错误**:
```
Error: Failed to connect to AIRIS MCP Gateway
Error: Gateway timeout
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
} catch (error) {
  console.error("Gateway 错误:", error.message);

  // 提供用户友好的错误信息
  throw new Error(`
    AIRIS MCP Gateway 不可用。请检查：
    1. Gateway 是否正在运行（http://localhost:9400/health）
    2. 网络连接是否正常
    3. 防火墙设置是否阻止连接
  `);
}
```

**预防措施**:
- 工作流开始前执行健康检查
- 实现重试机制（最多 3 次，间隔 2 秒）
- 提供清晰的错误提示和修复建议

---

#### 3. 工具执行错误 → 具体错误具体处理

**典型错误**:
```
Error: Tavily API rate limit exceeded
Error: Serena content too large
Error: Fetch timeout
```

**处理策略**:

**Tavily 速率限制**:
```typescript
try {
  const result = await airis-exec({
    tool: "tavily:search",
    arguments: { query: "..." }
  });
} catch (error) {
  if (error.message.includes("rate limit")) {
    console.log("Tavily API 速率限制，等待 60 秒...");
    await sleep(60000);
    // 重试
    return await airis-exec({
      tool: "tavily:search",
      arguments: { query: "..." }
    });
  }
  throw error;
}
```

**Serena 内容过大**:
```typescript
try {
  await airis-exec({
    tool: "serena:write_memory",
    arguments: {
      memory_file_name: "research.md",
      content: largeContent
    }
  });
} catch (error) {
  if (error.message.includes("too large") || error.message.includes("exceeds maximum")) {
    // 分段保存
    const chunks = splitContent(largeContent, 50000);
    for (const [i, chunk] of chunks.entries()) {
      await airis-exec({
        tool: "serena:write_memory",
        arguments: {
          memory_file_name: `research-part-${i + 1}.md`,
          content: chunk
        }
      });
    }
  } else {
    throw error;
  }
}
```

**Fetch 超时**:
```typescript
const timeout = 30000; // 30 秒

try {
  const result = await Promise.race([
    airis-exec({
      tool: "fetch:fetch",
      arguments: { url: "..." }
    }),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error("Fetch timeout")), timeout)
    )
  ]);
} catch (error) {
  if (error.message.includes("timeout")) {
    console.log("Fetch 超时，尝试使用 Tavily Extract...");
    // 回退方案
    return await airis-exec({
      tool: "tavily:extract",
      arguments: { urls: ["..."] }
    });
  }
  throw error;
}
```

---

#### 4. 服务不可用 → 重试或回退

**典型错误**:
```
Error: Server 'tavily' not found
Error: Server 'serena' not ready
```

**处理策略**:

**服务器未安装**:
```typescript
const servers = await airis-exec({
  tool: "gateway-control:list-servers"
});

const requiredServers = ["tavily", "fetch", "serena"];
const missingServers = requiredServers.filter(
  name => !servers.find(s => s.name === name)
);

if (missingServers.length > 0) {
  throw new Error(`
    缺少必需的 MCP 服务器: ${missingServers.join(", ")}

    请安装缺少的服务器：
    1. 检查 AIRIS MCP Gateway 配置
    2. 安装缺少的 MCP 服务器
    3. 重启 Gateway
  `);
}
```

**服务器未就绪（COLD 模式）**:
```typescript
async function waitForServerReady(serverName, maxWaitTime = 10000) {
  const startTime = Date.now();

  while (Date.now() - startTime < maxWaitTime) {
    const servers = await airis-exec({
      tool: "gateway-control:list-servers"
    });

    const server = servers.find(s => s.name === serverName);

    if (server && server.ready) {
      return true;
    }

    console.log(`⏳ 等待 ${serverName} 就绪...`);
    await sleep(2000);
  }

  return false;
}

// 使用示例
const ready = await waitForServerReady("tavily");
if (!ready) {
  throw new Error("Tavily 服务器启动超时");
}
```

**回退方案**:
```typescript
// 主方案：使用 Tavily Extract
try {
  const content = await airis-exec({
    tool: "tavily:extract",
    arguments: { urls: [url] }
  });
} catch (error) {
  console.log("Tavily Extract 失败，回退到 Fetch...");

  // 回退方案：使用 Fetch
  try {
    const content = await airis-exec({
      tool: "fetch:fetch",
      arguments: { url: url }
    });
  } catch (fetchError) {
    console.log("Fetch 也失败，提取内容不可用");
    // 使用搜索结果的摘要内容
    return searchResult.content;
  }
}
```

---

### 完整错误处理示例

```typescript
async function robustWebResearch(topic: string) {
  try {
    // 1. 健康检查
    const health = await airis-exec({
      tool: "gateway-control:health"
    });

    if (!health.ok) {
      throw new Error("GATEWAY_UNHEALTHY");
    }

    // 2. 验证服务器可用性
    await ensureServerAvailable("tavily");
    await ensureServerAvailable("serena");

    // 3. 执行搜索（带重试）
    const results = await execWithRetry(
      "tavily:search",
      {
        query: `${topic} 2025`,
        search_depth: "advanced",
        max_results: 5
      },
      3
    );

    // 4. 保存结果（处理内容过大）
    const content = formatResearchResults(results);

    if (content.length > 50000) {
      // 分段保存
      const chunks = splitContent(content, 50000);
      for (const [i, chunk] of chunks.entries()) {
        await airis-exec({
          tool: "serena:write_memory",
          arguments: {
            memory_file_name: `${topic}-part-${i + 1}.md`,
            content: chunk
          }
        });
      }
    } else {
      await airis-exec({
        tool: "serena:write_memory",
        arguments: {
          memory_file_name: `${topic}.md`,
          content: content
        }
      });
    }

    return results;

  } catch (error) {
    // 统一错误处理
    console.error("Web 研究失败:", error);

    if (error.message === "GATEWAY_UNHEALTHY") {
      throw new Error("AIRIS MCP Gateway 不可用，请检查服务状态");
    } else if (error.message.includes("rate limit")) {
      throw new Error("API 速率限制，请稍后重试");
    } else if (error.message.includes("not found")) {
      throw new Error("必需的 MCP 服务器未安装");
    } else {
      throw new Error(`研究失败: ${error.message}`);
    }
  }
}
```

---

## 📚 参考文档

### References 文件

本 skill 包含以下参考文档（在 `references/` 目录中）:

- **tavily-advanced.md** (~100 行) - Tavily MCP 高级功能
  - 内容: 高级搜索参数、过滤选项、audience_extract 用法、批量提取技巧
  - 何时阅读: 需要精确控制搜索结果或批量处理多个 URL 时

- **serena-memory-patterns.md** (~50 行) - Serena 记忆管理最佳实践
  - 内容: 记忆文件命名规范、内容组织模式、分类策略、版本控制
  - 何时阅读: 需要建立系统化的项目知识库时

---

## 🔗 相关资源

**MCP 服务器文档**:
- [Tavily MCP](../../ai_workflow/docs/airis-mcp-gateway/servers/TAVILY.md) - Web 搜索和内容提取
- [Fetch MCP](../../ai_workflow/docs/airis-mcp-gateway/servers/FETCH.md) - 网页抓取
- [Serena MCP](../../ai_workflow/docs/airis-mcp-gateway/servers/SERENA.md) - 项目记忆管理

**AIRIS MCP Gateway**:
- [完整指南](../../ai_workflow/docs/airis-mcp-gateway/README.md)
- [快速参考](../../ai_workflow/docs/airis-mcp-gateway/QUICK_REFERENCE.md)
- [工具索引](../../ai_workflow/docs/airis-mcp-gateway/TOOL_INDEX.md)

**相关 Skills**:
- airis-knowledge-mgmt - 知识图谱管理（Memory + Serena 双路径）
- airis-project-indexing - 项目深度研究（AIRIS Agent）

---

## 📊 性能和限制

**性能考虑**:
- Tavily 搜索: ~2-5 秒/查询
- Fetch 提取: ~1-3 秒/URL
- Serena 保存: ~0.5-1 秒/文件
- **总耗时**: 约 5-10 秒/完整流程

**限制条件**:
- Tavily API 速率限制: 通常 60 requests/minute（根据计划不同）
- Fetch 单页内容: 建议 < 100KB
- Serena 记忆文件: 建议 < 50KB/文件

**最佳实践**:
- 使用 `search_depth: "basic"` 进行快速探索，`"advanced"` 进行深度研究
- 批量提取时使用 `tavily:extract` 而非多次 `fetch`
- 记忆文件使用语义化命名（如 `topic-subtopic-date.md`）
- 定期清理过时的记忆文件（使用 `serena:list_memories` 查看）

---

**版本**: 1.0.0
**最后更新**: 2025-12-30
**作者**: Hao
