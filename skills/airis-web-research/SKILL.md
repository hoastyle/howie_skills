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
