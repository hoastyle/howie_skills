# MCP 参数完整参考手册

**版本**: v1.0
**创建日期**: 2025-12-31
**目的**: 为 AIRIS Skills 提供 MCP 工具参数的权威参考

---

## 📋 目录

1. [高频参数陷阱 TOP 10](#高频参数陷阱-top-10)
2. [13 个 MCP 服务器完整参考](#mcp-服务器完整参考)
3. [参数命名模式总结](#参数命名模式总结)
4. [验证方法和最佳实践](#验证方法和最佳实践)

---

## 🎯 高频参数陷阱 TOP 10

> 基于 2025-12-31 验证报告，这些是最常见的参数错误（共 37 个错误中的典型代表）

### 1. ⚠️ Magic generate_ui - 缺少必需参数（19 次错误）

**错误示例**:
```typescript
// ❌ 严重错误：只有 1/3 必需参数
await airis-exec({
    tool: "magic:generate_ui",
    arguments: {
        absolutePathToCurrentFile: "/path/to/file.tsx"
        // 缺少 content 和 prompt！
    }
});
```

**正确用法**:
```typescript
// ✅ 完整的 3 个必需参数
await airis-exec({
    tool: "magic:generate_ui",
    arguments: {
        absolutePathToCurrentFile: "/home/user/project/src/App.tsx",  // 必须是绝对路径
        content: "import React from 'react'...",                       // 当前文件内容
        prompt: "创建一个登录表单组件"                                  // UI 生成提示
    }
});
```

**影响**: airis-ui-generation 的所有示例（准确性 -58.3%）

---

### 2. ❌ Serena write_memory - 错误的参数名（12 次错误）

**错误示例**:
```typescript
// ❌ 错误：使用直觉性参数名
await airis-exec({
    tool: "serena:write_memory",
    arguments: {
        filename: "react-rsc-research.md",  // 错误！应该是 memory_file_name
        text: "研究内容..."                  // 错误！应该是 content
    }
});
```

**正确用法**:
```typescript
// ✅ 正确：使用规范参数名
await airis-exec({
    tool: "serena:write_memory",
    arguments: {
        memory_file_name: "react-rsc-research.md",  // 正确参数名
        content: "研究内容..."                       // 正确参数名
    }
});
```

**影响**: airis-web-research (3次), airis-knowledge-mgmt (2次)

---

### 3. ❌ Serena find_symbol - 错误的参数名（6 次错误）

**错误示例**:
```typescript
// ❌ 错误：使用简单的参数名
await airis-exec({
    tool: "serena:find_symbol",
    arguments: {
        name: "MyClass"  // 错误！应该是 name_path_pattern
    }
});
```

**正确用法**:
```typescript
// ✅ 正确：使用完整的参数名
await airis-exec({
    tool: "serena:find_symbol",
    arguments: {
        name_path_pattern: "MyClass"  // 正确参数名
    }
});
```

**影响**: airis-code-search (6次，准确性 72.7%)

---

### 4. ⚠️ Playwright browser_navigate - 缺少必需参数（3 次错误）

**错误示例**:
```typescript
// ❌ 错误：缺少 url 参数
await airis-exec({
    tool: "playwright:browser_navigate",
    arguments: {}  // 空参数对象！
});
```

**正确用法**:
```typescript
// ✅ 正确：提供 url 参数
await airis-exec({
    tool: "playwright:browser_navigate",
    arguments: {
        url: "https://example.com"  // 必需参数
    }
});
```

**影响**: airis-browser-automation (3次，准确性 83.3%)

---

### 5. ❌ Serena read_memory - 混淆参数名

**常见错误组合**:
- `path` ❌ → `memory_file_name` ✅
- `name` ❌ → `memory_file_name` ✅
- `filename` ❌ → `memory_file_name` ✅

**正确用法**:
```typescript
await airis-exec({
    tool: "serena:read_memory",
    arguments: {
        memory_file_name: "project_overview"  // 唯一正确的参数名
    }
});
```

---

### 6. ❌ Magic generate_ui - 相对路径错误

**错误示例**:
```typescript
// ❌ 错误：使用相对路径
await airis-exec({
    tool: "magic:generate_ui",
    arguments: {
        absolutePathToCurrentFile: "src/App.tsx",  // 错误！必须是绝对路径
        content: "...",
        prompt: "..."
    }
});
```

**正确用法**:
```typescript
// ✅ 正确：使用绝对路径
await airis-exec({
    tool: "magic:generate_ui",
    arguments: {
        absolutePathToCurrentFile: "/home/user/project/src/App.tsx",  // 绝对路径
        content: "...",
        prompt: "..."
    }
});
```

---

### 7. ❌ MorphLLM query_codebase - 相对路径错误

**错误示例**:
```typescript
// ❌ 错误：使用相对路径或错误参数名
await airis-exec({
    tool: "morphllm:query_codebase",
    arguments: {
        path: ".",           // 错误参数名！
        project_path: "./",  // 错误参数名！
        query: "..."
    }
});
```

**正确用法**:
```typescript
// ✅ 正确：使用 repo_path 和绝对路径
await airis-exec({
    tool: "morphllm:query_codebase",
    arguments: {
        repo_path: "/home/user/my-project",  // 正确参数名 + 绝对路径
        query: "如何实现用户认证？"
    }
});
```

---

### 8. ❌ Serena find_file - 混淆参数组合

**错误示例**:
```typescript
// ❌ 错误：使用错误的参数组合
await airis-exec({
    tool: "serena:find_file",
    arguments: {
        filename: "*.md",  // 错误！应该是 file_mask
        path: "."          // 错误！应该是 relative_path
    }
});
```

**正确用法**:
```typescript
// ✅ 正确：使用正确的参数组合
await airis-exec({
    tool: "serena:find_file",
    arguments: {
        file_mask: "*.md",      // 文件名或通配符模式
        relative_path: "."       // 相对路径（"." 表示项目根目录）
    }
});
```

---

### 9. ❌ Memory remember - 字符串 vs 数组错误

**错误示例**:
```typescript
// ❌ 错误：使用字符串
await airis-exec({
    tool: "memory:remember",
    arguments: {
        observations: "用户偏好使用 TypeScript"  // 错误！必须是数组
    }
});
```

**正确用法**:
```typescript
// ✅ 正确：使用数组
await airis-exec({
    tool: "memory:remember",
    arguments: {
        observations: [
            "用户偏好使用 TypeScript",
            "项目使用 React 18"
        ]  // 正确：数组格式
    }
});
```

---

### 10. ⚠️ Playwright navigate - wait_until 严格值

**错误示例**:
```typescript
// ❌ 错误：使用不支持的值
await airis-exec({
    tool: "playwright:browser_navigate",
    arguments: {
        url: "https://example.com",
        wait_until: "complete"  // 错误！不支持的值
    }
});
```

**正确用法**:
```typescript
// ✅ 正确：使用支持的值
await airis-exec({
    tool: "playwright:browser_navigate",
    arguments: {
        url: "https://example.com",
        wait_until: "load"  // 支持的值："load", "domcontentloaded", "networkidle"
    }
});
```

---

## 📚 MCP 服务器完整参考

### Serena MCP 服务器 (HOT 模式)

**服务器**: `serena`
**模式**: HOT (常驻内存)
**主要功能**: 语义代码理解、项目记忆管理、符号搜索

---

#### read_memory

**用途**: 读取项目记忆文件

**必需参数**:
- `memory_file_name` (string) - 记忆文件名（不需要 .md 后缀）

**可选参数**:
- `max_answer_chars` (number) - 最大返回字符数

**示例**:
```typescript
await airis-exec({
    tool: "serena:read_memory",
    arguments: {
        memory_file_name: "project_overview"
    }
});
```

**常见错误**:
- ❌ `path`, `name`, `filename` → ✅ `memory_file_name`

---

#### write_memory

**用途**: 写入项目记忆文件

**必需参数**:
- `memory_file_name` (string) - 记忆文件名（不需要 .md 后缀）
- `content` (string) - 记忆内容（支持 Markdown）

**示例**:
```typescript
await airis-exec({
    tool: "serena:write_memory",
    arguments: {
        memory_file_name: "session_summary",
        content: "# 会话总结\n\n今天完成了..."
    }
});
```

**常见错误**:
- ❌ `filename`, `text`, `data` → ✅ `memory_file_name`, `content`

---

#### list_memories

**用途**: 列出所有可用的记忆文件

**必需参数**: 无

**示例**:
```typescript
await airis-exec({
    tool: "serena:list_memories",
    arguments: {}
});
```

---

#### find_file

**用途**: 在项目中搜索文件

**必需参数**:
- `file_mask` (string) - 文件名或通配符模式（如 "*.md", "config.json"）
- `relative_path` (string) - 相对路径（"." 表示项目根目录）

**示例**:
```typescript
// 查找所有 Markdown 文件
await airis-exec({
    tool: "serena:find_file",
    arguments: {
        file_mask: "*.md",
        relative_path: "."
    }
});

// 查找特定目录中的配置文件
await airis-exec({
    tool: "serena:find_file",
    arguments: {
        file_mask: "package.json",
        relative_path: "src"
    }
});
```

**常见错误**:
- ❌ `filename`, `path` → ✅ `file_mask`, `relative_path`

---

#### find_symbol

**用途**: 查找代码符号（类、函数、方法等）

**必需参数**:
- `name_path_pattern` (string) - 符号路径模式
  - 单个符号: `"MyClass"`
  - 类中的方法: `"MyClass/myMethod"`
  - 嵌套路径: `"Namespace/Class/Method"`

**可选参数**:
- `depth` (number) - 获取子符号的深度（默认 0）
- `relative_path` (string) - 限制搜索范围
- `include_body` (boolean) - 是否包含源代码（默认 false）

**示例**:
```typescript
// 查找类定义
await airis-exec({
    tool: "serena:find_symbol",
    arguments: {
        name_path_pattern: "UserService"
    }
});

// 查找类中的方法
await airis-exec({
    tool: "serena:find_symbol",
    arguments: {
        name_path_pattern: "UserService/authenticate",
        depth: 1,
        include_body: true
    }
});
```

**常见错误**:
- ❌ `name`, `symbol_name`, `class_name` → ✅ `name_path_pattern`

---

#### get_code_from_probable_symbol_file

**用途**: 根据符号名推断文件并获取代码

**必需参数**:
- `symbol_name` (string) - 符号名称

**可选参数**:
- `file_language` (string) - 文件语言（如 "typescript", "python"）

**示例**:
```typescript
await airis-exec({
    tool: "serena:get_code_from_probable_symbol_file",
    arguments: {
        symbol_name: "UserController",
        file_language: "typescript"
    }
});
```

---

### Magic MCP 服务器 (COLD 模式)

**服务器**: `magic`
**模式**: COLD (按需启动)
**主要功能**: AI 驱动的 UI 组件生成

---

#### generate_ui

**用途**: 根据提示生成 UI 组件代码

**必需参数**:
- `absolutePathToCurrentFile` (string) - **当前文件的绝对路径**
- `content` (string) - 当前文件内容
- `prompt` (string) - UI 生成提示

**示例**:
```typescript
await airis-exec({
    tool: "magic:generate_ui",
    arguments: {
        absolutePathToCurrentFile: "/home/user/project/src/components/LoginForm.tsx",
        content: "import React from 'react';\n\nexport const LoginForm = () => {\n  return <div></div>;\n};",
        prompt: "创建一个包含用户名、密码输入框和登录按钮的表单组件"
    }
});
```

**关键注意事项**:
- ⚠️ `absolutePathToCurrentFile` **必须是绝对路径**，相对路径会失败
- ⚠️ 所有 3 个参数都是必需的，缺一不可
- ⚠️ `content` 应该是当前文件的完整内容

**常见错误**:
- ❌ 使用相对路径: `"src/App.tsx"` → ✅ `"/home/user/project/src/App.tsx"`
- ❌ 只提供路径: 缺少 `content` 和 `prompt`
- ❌ 错误参数名: `path`, `file`, `currentFile` → ✅ `absolutePathToCurrentFile`

---

### MorphLLM MCP 服务器 (COLD 模式)

**服务器**: `morphllm`
**模式**: COLD (按需启动)
**主要功能**: 语义代码库查询、文件内容获取

---

#### query_codebase

**用途**: 使用自然语言查询代码库

**必需参数**:
- `repo_path` (string) - **仓库的绝对路径**
- `query` (string) - 查询问题

**示例**:
```typescript
await airis-exec({
    tool: "morphllm:query_codebase",
    arguments: {
        repo_path: "/home/user/my-project",
        query: "如何实现用户认证和授权？"
    }
});
```

**关键注意事项**:
- ⚠️ `repo_path` **必须是绝对路径**
- ⚠️ 查询应该是具体的问题，而非关键词

**常见错误**:
- ❌ 相对路径: `"."`, `"./"` → ✅ `"/home/user/my-project"`
- ❌ 错误参数名: `path`, `project_path`, `directory` → ✅ `repo_path`

---

#### get_file_content

**用途**: 获取指定文件的内容

**必需参数**:
- `repo_path` (string) - **仓库的绝对路径**
- `file_path` (string) - 文件相对路径

**限制**:
- 文件大小: < 2000 行

**示例**:
```typescript
await airis-exec({
    tool: "morphllm:get_file_content",
    arguments: {
        repo_path: "/home/user/my-project",
        file_path: "src/services/auth.ts"
    }
});
```

**常见错误**:
- ❌ `repo_path` 使用相对路径
- ❌ `file_path` 使用绝对路径（应该是相对于 repo_path 的路径）

---

### Memory MCP 服务器 (HOT 模式)

**服务器**: `memory`
**模式**: HOT (常驻内存)
**主要功能**: 知识图谱、实体记忆

---

#### remember (原 create_entities)

**用途**: 创建知识实体

**必需参数**:
- `observations` (array<string>) - 观察内容数组

**示例**:
```typescript
await airis-exec({
    tool: "memory:remember",
    arguments: {
        observations: [
            "用户偏好使用 TypeScript",
            "项目采用微服务架构",
            "数据库使用 PostgreSQL"
        ]
    }
});
```

**关键注意事项**:
- ⚠️ `observations` **必须是数组**，不能是字符串
- ⚠️ 数组中的每个元素应该是独立的观察陈述

**常见错误**:
- ❌ 字符串: `observations: "用户偏好..."` → ✅ `observations: ["用户偏好..."]`
- ❌ 错误参数名: `entities`, `facts`, `data` → ✅ `observations`

---

#### search (原 search_nodes)

**用途**: 搜索知识节点

**必需参数**:
- `query` (string) - 搜索查询

**示例**:
```typescript
await airis-exec({
    tool: "memory:search",
    arguments: {
        query: "TypeScript 配置"
    }
});
```

---

### Tavily MCP 服务器 (COLD 模式)

**服务器**: `tavily`
**模式**: COLD (按需启动)
**主要功能**: AI 驱动的 Web 搜索

---

#### search

**用途**: 搜索 Web 内容

**必需参数**:
- `query` (string) - 搜索查询

**可选参数**:
- `max_results` (number) - 最大结果数（默认 5）
- `search_depth` (string) - 搜索深度："basic" 或 "advanced"

**示例**:
```typescript
await airis-exec({
    tool: "tavily:search",
    arguments: {
        query: "React Server Components best practices",
        max_results: 10,
        search_depth: "advanced"
    }
});
```

---

#### extract

**用途**: 从 URL 提取内容

**必需参数**:
- `urls` (array<string>) - URL 数组

**示例**:
```typescript
await airis-exec({
    tool: "tavily:extract",
    arguments: {
        urls: [
            "https://react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023",
            "https://nextjs.org/docs/app/building-your-application/rendering/server-components"
        ]
    }
});
```

---

### Playwright MCP 服务器 (COLD 模式)

**服务器**: `playwright`
**模式**: COLD (按需启动)
**主要功能**: 浏览器自动化、Web 测试

---

#### browser_navigate

**用途**: 导航到指定 URL

**必需参数**:
- `url` (string) - 目标 URL

**可选参数**:
- `wait_until` (string) - 等待条件
  - 支持值: `"load"`, `"domcontentloaded"`, `"networkidle"`
- `timeout` (number) - 超时时间（毫秒）

**示例**:
```typescript
await airis-exec({
    tool: "playwright:browser_navigate",
    arguments: {
        url: "https://example.com",
        wait_until: "load"
    }
});
```

**常见错误**:
- ❌ 缺少 `url` 参数
- ❌ 错误的 `wait_until` 值: `"complete"`, `"ready"` → ✅ `"load"`, `"domcontentloaded"`, `"networkidle"`

---

#### snapshot

**用途**: 获取页面快照（HTML）

**必需参数**: 无

**示例**:
```typescript
await airis-exec({
    tool: "playwright:snapshot",
    arguments: {}
});
```

---

#### screenshot

**用途**: 截取页面截图

**可选参数**:
- `name` (string) - 截图文件名
- `width` (number) - 视口宽度
- `height` (number) - 视口高度

**示例**:
```typescript
await airis-exec({
    tool: "playwright:screenshot",
    arguments: {
        name: "homepage",
        width: 1920,
        height: 1080
    }
});
```

---

### Context7 MCP 服务器 (COLD 模式)

**服务器**: `context7`
**模式**: COLD (按需启动)
**主要功能**: 官方库文档查询

---

#### resolve-library-id

**用途**: 解析库 ID

**必需参数**:
- `library` (string) - 库名称（如 "react", "typescript"）

**示例**:
```typescript
await airis-exec({
    tool: "context7:resolve-library-id",
    arguments: {
        library: "react"
    }
});
```

---

#### query-docs

**用途**: 查询库文档

**必需参数**:
- `library_id` (string) - 库 ID（从 resolve-library-id 获取）
- `query` (string) - 查询问题

**示例**:
```typescript
// 步骤 1: 解析库 ID
const libResult = await airis-exec({
    tool: "context7:resolve-library-id",
    arguments: { library: "react" }
});

// 步骤 2: 查询文档
await airis-exec({
    tool: "context7:query-docs",
    arguments: {
        library_id: libResult.id,
        query: "How to use useEffect hook?"
    }
});
```

---

### AIRIS Agent MCP 服务器 (HOT 模式)

**服务器**: `airis-agent`
**模式**: HOT (常驻内存)
**主要功能**: 项目索引

---

#### index_repository

**用途**: 索引代码仓库

**必需参数**:
- `repo_path` (string) - **仓库的绝对路径**

**示例**:
```typescript
await airis-exec({
    tool: "airis-agent:index_repository",
    arguments: {
        repo_path: "/home/user/my-project"
    }
});
```

**常见错误**:
- ❌ 相对路径: `"."` → ✅ `"/home/user/my-project"`
- ❌ 错误参数名: `path`, `project_path` → ✅ `repo_path`

---

### Fetch MCP 服务器 (COLD 模式)

**服务器**: `fetch`
**模式**: COLD (按需启动)
**主要功能**: HTTP 请求

---

#### fetch

**用途**: 发送 HTTP 请求

**必需参数**:
- `url` (string) - 请求 URL

**可选参数**:
- `method` (string) - HTTP 方法（默认 "GET"）
- `headers` (object) - 请求头
- `body` (string) - 请求体

**示例**:
```typescript
// GET 请求
await airis-exec({
    tool: "fetch:fetch",
    arguments: {
        url: "https://api.example.com/users"
    }
});

// POST 请求
await airis-exec({
    tool: "fetch:fetch",
    arguments: {
        url: "https://api.example.com/users",
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name: "John" })
    }
});
```

---

### Chrome DevTools MCP 服务器 (COLD 模式)

**服务器**: `chrome-devtools`
**模式**: COLD (按需启动)
**主要功能**: Chrome 浏览器调试

---

#### navigate

**用途**: 导航到指定 URL

**必需参数**:
- `url` (string) - 目标 URL

**示例**:
```typescript
await airis-exec({
    tool: "chrome-devtools:navigate",
    arguments: {
        url: "https://example.com"
    }
});
```

---

### Sequential Thinking MCP 服务器 (COLD 模式)

**服务器**: `sequential-thinking`
**模式**: COLD (按需启动)
**主要功能**: 结构化多步推理

---

#### think

**用途**: 执行结构化思考

**必需参数**:
- `question` (string) - 需要思考的问题

**示例**:
```typescript
await airis-exec({
    tool: "sequential-thinking:think",
    arguments: {
        question: "如何设计一个可扩展的微服务架构？"
    }
});
```

---

### MindBase MCP 服务器 (Docker 模式)

**服务器**: `mindbase`
**模式**: Docker (需要显式启用)
**主要功能**: 会话记录持久化、对话语义搜索

#### conversation_save

**用途**: 保存会话记录到数据库

**必需参数**:
- `source` (string) - 来源平台
  - 支持值: `"claude-code"`, `"claude-desktop"`, `"chatgpt"`, `"cursor"`, `"windsurf"`
- `title` (string) - 会话标题或摘要
- `content` (object) - 会话内容（可包含任意结构化数据）

**可选参数**:
- `category` (string) - 会话类别
  - 支持值: `"task"`, `"decision"`, `"progress"`, `"note"`, `"warning"`, `"error"`
- `priority` (string) - 优先级
  - 支持值: `"critical"`, `"high"`, `"normal"`, `"low"`
- `channel` (string) - 频道或工作区标识符
- `sessionId` (string) - 会话 ID
- `metadata` (object) - 额外元数据

**示例**:
```typescript
await airis-exec({
  tool: "mindbase:conversation_save",
  arguments: {
    source: "claude-code",
    title: "Obsidian 知识库优化项目 - 会话记录",
    content: {
      summary: "基于 kepano 思想优化知识库",
      stage: "阶段一、二已完成",
      achievements: ["14 个模板", "25 个视图"],
      domains: ["机器人", "ML", "编程"]
    },
    category: "progress",
    priority: "high",
    channel: "notebook",
    metadata: {
      project: "obsidian-knowledge-base",
      date: "2026-01-15",
      reference: "kepano"
    },
    sessionId: "obsidian_optimization_2025_01_15"
  }
});
```

**关键注意事项**:
- ⚠️ **必须先启用服务器**: 使用 `gateway_enable_server` 启用 mindbase
- ⚠️ **错误工具不存在**: `mindbase:memory_write` 不存在，应使用 `conversation_save`
- ⚠️ `content` 参数应该是对象，包含结构化数据
- ⚠️ `source` 参数必须使用支持的枚举值

**常见错误**:
- ❌ 使用不存在的工具: `mindbase:memory_write` → ✅ `mindbase:conversation_save`
- ❌ 服务器未启用 → 先调用 `gateway_enable_server`
- ❌ `source` 参数值错误 → 必须使用支持的枚举值

---

### Time MCP 服务器 (Docker 模式)

**服务器**: `time`
**模式**: Docker (需要显式启用)
**主要功能**: 时区转换

#### convert_time

**用途**: 在不同时区间转换时间

**示例**:
```typescript
await airis-exec({
  tool: "time:convert_time",
  arguments: {
    // 具体参数请参考工具 schema
  }
});
```

---

## 🔍 参数命名模式总结

### 模式 1: 文件/路径相关

| 常见错误 | 正确参数 | MCP 服务器 |
|---------|---------|-----------|
| `path` | `memory_file_name` | Serena (read/write_memory) |
| `filename` | `file_mask` | Serena (find_file) |
| `path` | `relative_path` | Serena (find_file, find_symbol) |
| `path`, `project_path` | `repo_path` | MorphLLM, AIRIS Agent |
| `path`, `file` | `absolutePathToCurrentFile` | Magic |

**规律**:
- Serena 使用 `memory_file_name` （记忆文件）
- Serena 使用 `file_mask` + `relative_path` （文件搜索）
- MorphLLM 和 AIRIS Agent 使用 `repo_path` （仓库路径，必须绝对路径）
- Magic 使用冗长但明确的 `absolutePathToCurrentFile` （必须绝对路径）

---

### 模式 2: 内容相关

| 常见错误 | 正确参数 | MCP 服务器 |
|---------|---------|-----------|
| `text`, `data`, `message` | `content` | Serena (write_memory), Magic |
| `text`, `content` | `observations` (数组) | Memory |
| `search`, `keyword` | `query` | MorphLLM, Tavily, Context7 |

**规律**:
- 大部分使用 `content` （字符串）
- Memory 使用 `observations` （数组）
- 搜索类统一使用 `query`

---

### 模式 3: 符号/实体相关

| 常见错误 | 正确参数 | MCP 服务器 |
|---------|---------|-----------|
| `name`, `symbol_name`, `class_name` | `name_path_pattern` | Serena (find_symbol) |
| `name` | `symbol_name` | Serena (get_code_from_probable_symbol_file) |

**规律**:
- `find_symbol` 使用 `name_path_pattern` （支持路径语法）
- `get_code_from_probable_symbol_file` 使用简单的 `symbol_name`

---

### 模式 4: 绝对路径 vs 相对路径

**必须使用绝对路径**:
- `magic:generate_ui` → `absolutePathToCurrentFile`
- `morphllm:query_codebase` → `repo_path`
- `morphllm:get_file_content` → `repo_path`
- `airis-agent:index_repository` → `repo_path`

**使用相对路径**:
- `serena:find_file` → `relative_path` ("." 表示项目根目录)
- `serena:find_symbol` → `relative_path` (可选)
- `morphllm:get_file_content` → `file_path` (相对于 repo_path)

---

### 模式 5: 数组 vs 字符串

**必须使用数组**:
- `memory:remember` → `observations: ["观察1", "观察2"]`
- `tavily:extract` → `urls: ["url1", "url2"]`

**使用字符串**:
- 大部分其他参数

---

## ✅ 验证方法和最佳实践

### 实践 1: 总是先用 airis-schema 验证

在编写代码前，先查看工具的参数定义：

```typescript
// 步骤 1: 获取工具 schema
const schema = await airis-schema({
    tool: "serena:write_memory"
});

// 步骤 2: 检查必需参数
console.log("Required:", schema.inputSchema.required);
// 输出: ["memory_file_name", "content"]

// 步骤 3: 查看所有参数定义
console.log("Properties:", schema.inputSchema.properties);
```

---

### 实践 2: 维护个人参数映射表

创建一个快速参考表，记录常用工具的参数：

```markdown
| 工具 | 必需参数 | 关键注意 |
|------|---------|---------|
| serena:write_memory | memory_file_name, content | 不是 filename！ |
| magic:generate_ui | absolutePathToCurrentFile, content, prompt | 绝对路径 + 3 个必需 |
| morphllm:query_codebase | repo_path, query | repo_path 必须绝对路径 |
```

---

### 实践 3: 建立"三步工作流"习惯

```typescript
// 步骤 1: 发现工具
const tools = await airis-find({ query: "code search" });

// 步骤 2: 查看参数
const schema = await airis-schema({ tool: "serena:find_symbol" });

// 步骤 3: 执行工具
await airis-exec({
    tool: "serena:find_symbol",
    arguments: {
        name_path_pattern: "UserService"  // 基于 schema 使用正确参数
    }
});
```

---

### 实践 4: 三步工作流验证参数

推荐使用 AIRIS MCP Gateway 的三步工作流验证参数：

```typescript
// Step 1: 发现工具
const tools = await airis-find({ query: "serena memory" });
console.log("可用工具:", tools);

// Step 2: 查看参数签名（关键步骤！）
const schema = await airis-schema({ tool: "serena:write_memory" });
console.log("参数:", schema.inputSchema.properties);
console.log("必需:", schema.inputSchema.required);

// Step 3: 使用正确参数调用
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "my-note.md",  // 从 Step 2 确认的正确参数名
    content: "..."
  }
});
```

**为什么不使用自动化验证脚本？**
- 真实项目中所有代码已达 100% 参数准确性
- 三步工作流提供即时、准确的参数信息
- 避免静态分析的误报问题

---

### 实践 5: 遵循参数命名规律

**记住这些核心规律**:

1. **Serena 记忆**: `memory_file_name` + `content`
2. **Serena 文件**: `file_mask` + `relative_path`
3. **Serena 符号**: `name_path_pattern`
4. **Magic UI**: `absolutePathToCurrentFile` + `content` + `prompt` (绝对路径)
5. **MorphLLM**: `repo_path` + `query` (绝对路径)
6. **Memory**: `observations` (数组)
7. **绝对路径服务器**: Magic, MorphLLM, AIRIS Agent

---

### 实践 6: 错误处理模式

```typescript
try {
    await airis-exec({
        tool: "serena:find_symbol",
        arguments: {
            name_path_pattern: "MyClass"
        }
    });
} catch (error) {
    // 检查是否是参数验证错误
    if (error.message.includes("validation error")) {
        console.error("参数错误！请检查:");
        console.error("1. 参数名是否正确");
        console.error("2. 是否缺少必需参数");
        console.error("3. 参数类型是否正确（字符串 vs 数组）");

        // 使用 airis-schema 查看正确参数
        const schema = await airis-schema({ tool: "serena:find_symbol" });
        console.log("正确参数:", schema.inputSchema.required);
    }
    throw error;
}
```

---

## 📖 相关文档

- **ai_workflow PARAMETER_TRAPS.md** - 原始参数陷阱文档（627 行）
- **FINAL_VALIDATION_REPORT_P1.md** - P1 阶段验证报告（100% 质量确认）
- **GETTING_STARTED.md** - 快速入门指南（含参数验证最佳实践）

---

## 🚀 后续改进

- [x] 添加 MindBase MCP 服务器文档（conversation_save）
- [x] 添加 Time MCP 服务器文档（convert_time）
- [ ] 补充每个工具的返回值结构示例
- [ ] 添加常见错误的完整错误信息示例
- [ ] 创建交互式参数验证工具

---

**文档版本**: v1.1
**最后更新**: 2026-01-15
**维护**: Howie Skills Team
**更新内容**:
- ✅ 新增 MindBase MCP 服务器完整文档
- ✅ 新增 Time MCP 服务器基础文档
- ✅ 修正 MindBase 服务器启用说明
