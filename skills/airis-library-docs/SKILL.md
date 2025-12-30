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
