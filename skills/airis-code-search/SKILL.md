---
name: airis-code-search
description: 代码搜索和编辑助手，使用 MorphLLM 进行语义查询和占位符编辑，使用 Serena 进行符号级精确搜索。支持占位符编辑模式（// ... existing code ...），避免重写整个文件。适用于代码片段搜索、函数定位、变量查找、小范围代码编辑等场景。
---

# AIRIS Code Search & Edit Helper

**MCP 服务器**: morphllm, serena
**复杂度**: high
**预估行数**: 280

---

## 🎯 触发条件

### 何时使用这个 Skill

**主要场景**:
- **代码片段搜索**: 查找特定函数、类、变量的定义位置
- **语义搜索**: 基于自然语言描述查找相关代码
- **精确搜索**: 使用正则表达式查找代码模式
- **小范围编辑**: 修改函数、添加参数、更新逻辑（文件 < 2000 行）
- **代码理解**: 理解代码结构和依赖关系

**关键词触发**:
- "搜索代码"、"查找函数"、"定位变量"
- "编辑代码"、"修改函数"、"添加参数"
- "语义搜索"、"grep"、"查找模式"
- "占位符编辑"、"部分修改"

**典型用户请求**:
```
"查找项目中所有使用 useState 的地方"
"修改 UserService 类中的 login 函数，添加错误处理"
"搜索包含 'API endpoint' 注释的代码"
"编辑 config.ts 文件，更新 API_URL 配置"
```

---

## 📋 决策树：搜索 vs 编辑

### 决策点：用户意图分析

```
用户请求
    │
    ├─ 包含 "查找"、"搜索"、"定位" 关键词？
    │   YES → 搜索路径
    │   NO  → 继续判断
    │
    ├─ 包含 "编辑"、"修改"、"更新" 关键词？
    │   YES → 编辑路径
    │   NO  → 默认搜索路径
```

---

## 📋 工作流程

### 路径 A: 代码搜索

#### Phase 1: 语义搜索（MorphLLM）

**功能**: 使用自然语言描述查找相关代码

**执行搜索**:
```typescript
// Step 1: 语义查询
const semanticResults = await airis-exec({
  tool: "morphllm:semantic_query",
  arguments: {
    repo_path: "/path/to/project",  // 项目绝对路径
    query: "functions that handle user authentication",
    max_results: 10
  }
});
```

**参数说明**:
- `repo_path` (必需) - 项目根目录的**绝对路径**
- `query` (必需) - 自然语言查询描述
- `max_results` - 返回结果数量（默认 10）

**返回结果**:
```json
{
  "results": [
    {
      "file_path": "src/services/auth.ts",
      "line_number": 45,
      "code_snippet": "async function login(username, password) {...}",
      "score": 0.92
    }
  ]
}
```

---

#### Phase 2: 精确搜索（MorphLLM grep）

**功能**: 使用正则表达式查找代码模式

**执行搜索**:
```typescript
// Step 2: grep 精确搜索
const grepResults = await airis-exec({
  tool: "morphllm:grep_search",
  arguments: {
    repo_path: "/path/to/project",
    pattern: "useState\\(",           // 正则表达式
    file_pattern: "*.{ts,tsx}",       // 文件类型过滤
    case_sensitive: false
  }
});
```

**参数说明**:
- `repo_path` (必需) - 项目根目录绝对路径
- `pattern` (必需) - 正则表达式模式
- `file_pattern` - 文件类型过滤（如 `*.ts`, `*.{js,jsx}`）
- `case_sensitive` - 是否区分大小写（默认 false）

**返回结果**:
```json
{
  "matches": [
    {
      "file_path": "src/components/UserForm.tsx",
      "line_number": 12,
      "line_content": "const [username, setUsername] = useState('');"
    }
  ]
}
```

---

#### Phase 3: Serena 符号级搜索（可选）

**功能**: 基于 LSP 的符号级精确搜索

**执行搜索**:
```typescript
// Step 3: Serena 语义搜索（符号级）
const serenaResults = await airis-exec({
  tool: "serena:semantic_search",
  arguments: {
    query: "UserService login method",
    limit: 5
  }
});
```

**何时使用**:
- 需要查找函数定义、类定义、接口定义
- 需要查找符号引用（函数调用、变量使用）
- 跨文件的符号依赖分析

---

### 路径 B: 代码编辑（占位符模式）

#### Phase 1: 定位目标代码

**使用语义搜索或 grep 定位需要编辑的代码**:
```typescript
// Step 1: 定位目标函数
const target = await airis-exec({
  tool: "morphllm:semantic_query",
  arguments: {
    repo_path: "/path/to/project",
    query: "UserService login function"
  }
});

// 获取文件路径和行号
const filePath = target.results[0].file_path;
const lineNumber = target.results[0].line_number;
```

---

#### Phase 2: 占位符编辑（关键）

**功能**: 使用占位符模式编辑代码，避免重写整个文件

**⚠️ 核心原则: 使用占位符 `// ... existing code ...`**

**三种编辑操作**:

**1. REPLACE 操作（替换）**:
```typescript
await airis-exec({
  tool: "morphllm:morph_file",
  arguments: {
    repo_path: "/path/to/project",
    file_path: "src/services/UserService.ts",
    operation: "replace",
    old_code: `async login(username: string, password: string) {
  return await api.post('/login', { username, password });
}`,
    new_code: `async login(username: string, password: string) {
  try {
    return await api.post('/login', { username, password });
  } catch (error) {
    console.error('Login failed:', error);
    throw error;
  }
}`
  }
});
```

**2. INSERT 操作（插入）**:
```typescript
await airis-exec({
  tool: "morphllm:morph_file",
  arguments: {
    repo_path: "/path/to/project",
    file_path: "src/services/UserService.ts",
    operation: "insert",
    position: "after",              // before | after
    anchor_code: "class UserService {",
    new_code: `  private apiKey: string;

  constructor(apiKey: string) {
    this.apiKey = apiKey;
  }
  `
  }
});
```

**3. DELETE 操作（删除）**:
```typescript
await airis-exec({
  tool: "morphllm:morph_file",
  arguments: {
    repo_path: "/path/to/project",
    file_path: "src/services/UserService.ts",
    operation: "delete",
    target_code: `// Deprecated function
async oldLogin() {
  // ... old implementation ...
}`
  }
});
```

---

#### Phase 3: 占位符使用技巧

**✅ 正确使用占位符**:
```typescript
// 只修改函数体，保留类定义
new_code: `class UserService {
  // ... existing code ...

  async login(username: string, password: string) {
    // 新的实现
    try {
      return await api.post('/login', { username, password });
    } catch (error) {
      throw new AuthError(error);
    }
  }

  // ... existing code ...
}`
```

**❌ 错误做法：重写整个文件**:
```typescript
// 不要这样做！会覆盖整个文件
new_code: `import ...
import ...

class UserService {
  // 需要手动复制所有现有代码
  ...
}`
```

---

## 💻 完整示例

### 示例 1: 查找并修改函数

**用户需求**:
```
"查找 UserService 中的 login 函数，添加日志记录"
```

**执行步骤**:

```typescript
// Step 1: 语义搜索定位函数
const searchResult = await airis-exec({
  tool: "morphllm:semantic_query",
  arguments: {
    repo_path: "/home/user/project",
    query: "UserService login function implementation"
  }
});

const targetFile = searchResult.results[0].file_path;
// 结果: "src/services/UserService.ts"

// Step 2: 读取当前代码（可选，用于确认）
// 使用 Read tool 查看当前实现

// Step 3: 使用占位符模式编辑
await airis-exec({
  tool: "morphllm:morph_file",
  arguments: {
    repo_path: "/home/user/project",
    file_path: targetFile,
    operation: "replace",
    old_code: `async login(username: string, password: string) {
  return await api.post('/login', { username, password });
}`,
    new_code: `async login(username: string, password: string) {
  console.log('[UserService] Login attempt for:', username);
  try {
    const result = await api.post('/login', { username, password });
    console.log('[UserService] Login successful');
    return result;
  } catch (error) {
    console.error('[UserService] Login failed:', error);
    throw error;
  }
}`
  }
});
```

**预期输出**:
```
✅ 成功修改 src/services/UserService.ts
- 添加了登录前日志
- 添加了成功/失败日志
- 添加了错误处理
```

---

### 示例 2: 批量搜索并保存结果

**用户需求**:
```
"查找所有使用 console.log 的地方，保存到记忆"
```

**执行步骤**:

```typescript
// Step 1: grep 搜索所有 console.log
const logUsages = await airis-exec({
  tool: "morphllm:grep_search",
  arguments: {
    repo_path: "/home/user/project",
    pattern: "console\\.log\\(",
    file_pattern: "*.{ts,tsx,js,jsx}"
  }
});

// Step 2: 整理搜索结果
const report = `# Console.log 使用情况

## 总计
找到 ${logUsages.matches.length} 处使用

## 详细列表
${logUsages.matches.map(m =>
  `- **${m.file_path}:${m.line_number}**\n  \`\`\`\n  ${m.line_content}\n  \`\`\``
).join('\n\n')}

---
**搜索日期**: ${new Date().toISOString().split('T')[0]}
`;

// Step 3: 保存到 Serena 记忆
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "console-log-audit.md",
    content: report
  }
});
```

---

## ⚠️ 常见陷阱和解决方案

### 陷阱 1: 不使用占位符，重写整个文件

**错误现象**:
编辑后文件丢失了其他函数或配置

**原因分析**:
直接提供完整文件内容会覆盖原文件，导致未包含的部分丢失

**解决方案**:
```typescript
// ❌ 错误：提供完整文件
new_code: `import React from 'react';

function UserForm() {
  // 只写了这一个组件，其他组件丢失了
  return <div>...</div>;
}

export default UserForm;`

// ✅ 正确：使用占位符
new_code: `// ... existing imports ...

function UserForm() {
  // 修改后的实现
  return <div>...</div>;
}

// ... existing code ...`
```

---

### 陷阱 2: 文件过大（> 2000 行）

**错误现象**:
```
Error: File too large for editing
```

**原因分析**:
MorphLLM 对单文件大小有限制（通常 < 2000 行），超过限制无法编辑

**解决方案**:

**策略 A：使用验证脚本**
```bash
# 使用 scripts/validate_file_size.py 检查
python scripts/validate_file_size.py src/services/LargeService.ts

# 输出：
# ✅ 文件大小: 1850 行 (可编辑)
# ❌ 文件大小: 2500 行 (超过限制，建议拆分)
```

**策略 B：拆分文件**
```typescript
// 如果文件过大，建议先拆分为多个模块
// 然后再编辑单个模块
```

**策略 C：使用传统编辑工具**
```typescript
// 对于超大文件，使用 Edit tool 进行编辑
// 而不是 MorphLLM
```

---

### 陷阱 3: repo_path 使用相对路径

**错误现象**:
```
Error: Repository not found
```

**原因分析**:
MorphLLM 要求使用绝对路径，相对路径会导致找不到仓库

**解决方案**:
```typescript
// ❌ 错误：相对路径
{
  repo_path: "./project"
}

// ❌ 错误：~/home 快捷方式
{
  repo_path: "~/project"
}

// ✅ 正确：绝对路径
{
  repo_path: "/home/user/project"
}

// ✅ 正确：使用 process.cwd()
{
  repo_path: process.cwd()  // 在当前工作目录
}
```

---

## 🔌 AIRIS MCP Gateway 标准访问模式（完整版）

本章节展示完整的 AIRIS MCP Gateway 访问模式，确保工具使用的标准化和可靠性。

### 四步标准化工作流

#### Step 1: 工具发现 (airis-find)

使用 `airis-find` 发现本 skill 使用的 MCP 工具：

```typescript
// 发现 MorphLLM 代码搜索和编辑工具
const morphllmTools = await airis-find({
  query: "morphllm"
});
console.log("MorphLLM 工具:", morphllmTools.map(t => t.name));
// 输出: ["morphllm:semantic_query", "morphllm:edit_code",
//        "morphllm:grep_search", ...]

// 发现 Serena 代码理解工具
const serenaTools = await airis-find({
  query: "serena symbol"
});
console.log("Serena 符号工具:", serenaTools.map(t => t.name));
// 输出: ["serena:find_symbol", "serena:find_referencing_symbols",
//        "serena:get_symbols_overview", ...]
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
// 检查 MorphLLM 语义查询参数
const semanticQuerySchema = await airis-schema({
  tool: "morphllm:semantic_query"
});
console.log("必需参数:", semanticQuerySchema.inputSchema.required);
// 输出: ["repo_path", "query"]
console.log("可选参数:", Object.keys(semanticQuerySchema.inputSchema.properties));
// 输出: ["repo_path", "query", "max_results"]

// 检查 Serena 符号搜索参数
const findSymbolSchema = await airis-schema({
  tool: "serena:find_symbol"
});
console.log("Serena 参数:", findSymbolSchema.inputSchema.required);
// 输出: ["name"]
```

**常见参数命名陷阱**（本 skill 涉及）:
- ⚠️ `repo_path` 必须是**绝对路径**（MorphLLM 和 Serena）
- ⚠️ MorphLLM `edit_code` 的 `file_path` 也必须是绝对路径
- ⚠️ Serena `name` vs `substring` - 精确匹配 vs 模糊匹配
- ⚠️ 文件大小限制：MorphLLM 编辑要求文件 < 2000 行

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
const requiredServers = ["morphllm", "serena"];
for (const serverName of requiredServers) {
  const server = servers.find(s => s.name === serverName);

  if (!server) {
    throw new Error(`服务器 ${serverName} 未安装`);
  }

  if (server.mode === "COLD" && !server.ready) {
    console.log(`⏳ 等待 ${serverName} 启动（COLD 模式，需要 3-5 秒）...`);
    await sleep(4000);
  }
}

console.log("✅ 所有必需的 MCP 服务器已就绪");
```

**什么时候需要健康检查？**
- ✅ 长时间运行的代码搜索任务
- ✅ 生产环境部署
- ✅ 首次使用 MorphLLM 或 Serena（项目初始化）
- ⚠️ 快速原型开发时可以跳过（但要处理错误）

---

### 完整示例：端到端标准化工作流

```typescript
async function standardizedCodeSearch(repoPath: string, query: string) {
  // Step 1: 健康检查
  const health = await airis-exec({
    tool: "gateway-control:health"
  });

  if (!health.ok) {
    throw new Error("Gateway 不可用");
  }

  // Step 2: 发现工具
  const tools = await airis-find({ query: "morphllm semantic" });
  const semanticTool = tools.find(t => t.name === "morphllm:semantic_query");

  if (!semanticTool) {
    throw new Error("MorphLLM 语义查询工具未找到");
  }

  // Step 3: 验证参数
  const schema = await airis-schema({ tool: semanticTool.name });
  console.log("工具参数:", schema.inputSchema);

  // 验证 repo_path 是绝对路径
  if (!repoPath.startsWith("/")) {
    throw new Error("repo_path 必须是绝对路径");
  }

  // Step 4: 执行语义搜索
  const semanticResults = await airis-exec({
    tool: "morphllm:semantic_query",
    arguments: {
      repo_path: repoPath,
      query: query,
      max_results: 10
    }
  });

  // Step 5: 使用 Serena 精确定位符号
  if (semanticResults.results.length > 0) {
    const topResult = semanticResults.results[0];

    const symbolDetails = await airis-exec({
      tool: "serena:find_symbol",
      arguments: {
        name: extractSymbolName(topResult.code_snippet),
        file: topResult.file_path
      }
    });

    return { semanticResults, symbolDetails };
  }

  return { semanticResults };
}
```

---

## ⚙️ 服务运行模式

### MCP 服务器特性

本 skill 使用的 2 个 MCP 服务器均为 **COLD 模式**：

| 服务器 | 工具数 | 运行模式 | 启动延迟 | 首次调用建议 |
|--------|--------|---------|---------|-------------|
| **morphllm** | 4 | COLD ❄️ | 3-5 秒 | 项目索引检查 + 健康检查 |
| **serena** | 23 | COLD ❄️ | 2-5 秒 | 项目激活需要额外时间 |

### 双 COLD 模式说明

**双 COLD 模式服务器特点**:
- ❄️ 两个服务器都按需启动，首次调用需要等待
  - MorphLLM: 3-5 秒启动 + 项目索引加载
  - Serena: 2-5 秒启动 + 语言服务器初始化
- 💤 长时间不用会自动休眠
- 🔄 重新启动需要等待
- 📊 适合批量操作（复用已启动的服务）
- ⚡ 首次调用可能需要 6-10 秒总等待时间

**vs HOT 模式**（不适用于本 skill）:
- 🔥 常驻内存，即时响应
- ⚡ 无启动延迟
- 🎯 适合高频率调用

### 性能优化建议

#### 对于双 COLD 模式服务器（MorphLLM + Serena）:

1. **首次调用前执行健康检查**
   ```typescript
   const health = await airis-exec({ tool: "gateway-control:health" });
   ```

2. **预期并处理双启动延迟**
   ```typescript
   // 首次调用可能需要等待两个服务器启动
   try {
     const result = await airis-exec({
       tool: "morphllm:semantic_query",
       arguments: { repo_path: "...", query: "..." }
     });
   } catch (error) {
     if (error.message.includes("server not ready")) {
       console.log("MorphLLM 正在启动，等待 4 秒后重试...");
       await sleep(4000);
       // 重试
       const result = await airis-exec({
         tool: "morphllm:semantic_query",
         arguments: { repo_path: "...", query: "..." }
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
         await sleep(3000);
       }
     }
   }
   ```

4. **批量操作时复用已启动的服务**
   ```typescript
   // ✅ 高效：复用已启动的 MorphLLM 和 Serena 服务
   const queries = [
     "authentication functions",
     "database connection logic",
     "API endpoint handlers"
   ];

   for (const query of queries) {
     const results = await airis-exec({
       tool: "morphllm:semantic_query",
       arguments: { repo_path: "/project", query }
     });

     // 使用 Serena 进一步分析
     for (const result of results.results) {
       const symbols = await airis-exec({
         tool: "serena:find_symbol",
         arguments: { name: extractSymbolName(result.code_snippet) }
       });
     }
     // 后续调用无需启动延迟
   }

   // ❌ 低效：每次都可能触发启动
   // （如果在调用之间等待时间过长，服务器可能休眠）
   ```

5. **检查项目是否已索引（MorphLLM）**
   ```typescript
   // MorphLLM 需要项目索引才能工作
   try {
     await airis-exec({
       tool: "morphllm:semantic_query",
       arguments: { repo_path: "/project", query: "test" }
     });
   } catch (error) {
     if (error.message.includes("project not indexed") || error.message.includes("index")) {
       console.error(`
         ❌ 项目未索引。请先使用 airis-project-indexing skill 索引项目：

         await airis-exec({
           tool: "airis-agent:index_repository",
           arguments: { repo_path: "/project" }
         });
       `);
       throw new Error("项目未索引");
     }
   }
   ```

6. **检查项目是否激活（Serena）**
   ```typescript
   // Serena 需要激活项目才能使用
   try {
     await airis-exec({
       tool: "serena:find_symbol",
       arguments: { name: "MyClass" }
     });
   } catch (error) {
     if (error.message.includes("no active project") || error.message.includes("activate")) {
       console.error(`
         ❌ Serena 项目未激活。请先激活项目：

         await airis-exec({
           tool: "serena:activate_project",
           arguments: { name: "my-project" }
         });
       `);
       throw new Error("Serena 项目未激活");
     }
   }
   ```

### 服务可用性检查

```typescript
async function ensureBothServersAvailable() {
  const servers = await airis-exec({
    tool: "gateway-control:list-servers"
  });

  const requiredServers = ["morphllm", "serena"];

  for (const serverName of requiredServers) {
    const server = servers.find(s => s.name === serverName);

    if (!server) {
      throw new Error(`服务器 ${serverName} 不存在或未安装`);
    }

    if (server.mode === "COLD" && !server.ready) {
      console.log(`⏳ 等待 ${serverName} 启动（COLD 模式）...`);
      await sleep(4000);

      // 验证服务器是否已就绪
      const updatedServers = await airis-exec({
        tool: "gateway-control:list-servers"
      });
      const updatedServer = updatedServers.find(s => s.name === serverName);

      if (!updatedServer.ready) {
        throw new Error(`服务器 ${serverName} 启动失败`);
      }
    }
  }

  console.log("✅ MorphLLM 和 Serena 服务器都已就绪");
}

// 使用示例
await ensureBothServersAvailable();
```

---

## 🔄 统一错误处理

### 错误分类体系

本 skill 的错误可分为 4 大类：

#### 1. 参数错误 → 使用 airis-schema 预验证

**典型错误**:
```
Error: repo_path must be absolute (got: ./project)
Error: File size exceeds 2000 lines limit
Error: Required parameter 'name' is missing
```

**处理策略**:
```typescript
// ✅ 推荐：执行前验证
const schema = await airis-schema({ tool: "morphllm:semantic_query" });
const requiredParams = schema.inputSchema.required;

// 检查必需参数
if (!arguments.repo_path) {
  throw new Error("缺少必需参数: repo_path");
}

// 检查 repo_path 是绝对路径
if (!arguments.repo_path.startsWith("/")) {
  throw new Error("repo_path 必须是绝对路径");
}

// 执行工具
await airis-exec({
  tool: "morphllm:semantic_query",
  arguments: { /* 验证后的参数 */ }
});
```

**预防措施**:
- 总是使用 `airis-schema` 查询正确的参数名
- 参考本文档的"常见陷阱"章节
- 验证文件大小（MorphLLM 编辑限制 < 2000 行）

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
Error: Project not indexed (MorphLLM)
Error: No active project (Serena)
Error: File size too large
Error: Symbol not found
```

**处理策略**:

**MorphLLM 项目未索引**:
```typescript
try {
  const result = await airis-exec({
    tool: "morphllm:semantic_query",
    arguments: { repo_path: "/project", query: "..." }
  });
} catch (error) {
  if (error.message.includes("not indexed") || error.message.includes("index")) {
    console.error(`
      ❌ 项目未索引。请先使用 airis-project-indexing skill 索引项目。
    `);
    throw new Error("项目未索引，无法进行语义搜索");
  }
  throw error;
}
```

**Serena 项目未激活**:
```typescript
try {
  const symbols = await airis-exec({
    tool: "serena:find_symbol",
    arguments: { name: "MyClass" }
  });
} catch (error) {
  if (error.message.includes("no active project") || error.message.includes("activate")) {
    console.log("Serena 项目未激活，正在激活...");

    // 自动激活项目
    await airis-exec({
      tool: "serena:activate_project",
      arguments: { name: extractProjectName(process.cwd()) }
    });

    // 重试
    return await airis-exec({
      tool: "serena:find_symbol",
      arguments: { name: "MyClass" }
    });
  }
  throw error;
}
```

**文件大小超限**:
```typescript
try {
  await airis-exec({
    tool: "morphllm:edit_code",
    arguments: {
      file_path: "/project/large_file.ts",
      operation: "replace",
      content: "..."
    }
  });
} catch (error) {
  if (error.message.includes("too large") || error.message.includes("2000")) {
    console.error(`
      ❌ 文件大小超过 2000 行限制。建议：
      1. 拆分文件为多个模块
      2. 使用传统 Edit tool 进行编辑
      3. 只编辑文件的一部分
    `);
    throw new Error("文件大小超限，无法使用 MorphLLM 编辑");
  }
  throw error;
}
```

**符号未找到**:
```typescript
try {
  const symbols = await airis-exec({
    tool: "serena:find_symbol",
    arguments: { name: "NonExistentClass" }
  });

  if (!symbols || symbols.length === 0) {
    console.warn("符号未找到，尝试模糊搜索...");

    // 使用 substring 模糊匹配
    const fuzzyResults = await airis-exec({
      tool: "serena:find_symbol",
      arguments: { substring: "NonExistent" }
    });

    return fuzzyResults;
  }
} catch (error) {
  if (error.message.includes("not found")) {
    console.log("符号未找到，可能需要重新启动语言服务器...");

    await airis-exec({
      tool: "serena:restart_language_server"
    });

    // 重试
    return await airis-exec({
      tool: "serena:find_symbol",
      arguments: { name: "NonExistentClass" }
    });
  }
  throw error;
}
```

---

#### 4. 服务不可用 → 重试或回退

**典型错误**:
```
Error: MorphLLM server not ready
Error: Serena server not ready
Error: Server startup timeout
```

**处理策略**:
```typescript
async function executeWithServerRetry(tool, arguments, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await airis-exec({ tool, arguments });
    } catch (error) {
      if (error.message.includes("not ready") || error.message.includes("starting")) {
        if (i === maxRetries - 1) {
          throw new Error(`服务器启动失败（已重试 ${maxRetries} 次）`);
        }

        const waitTime = (i + 1) * 3000;  // 递增等待时间
        console.log(`服务器正在启动，等待 ${waitTime/1000} 秒后重试...`);
        await sleep(waitTime);
        continue;
      }

      throw error;
    }
  }
}

// 使用示例
const result = await executeWithServerRetry(
  "morphllm:semantic_query",
  { repo_path: "/project", query: "auth functions" }
);
```

**回退方案**:
```typescript
try {
  // 尝试使用 MorphLLM 语义搜索
  const semanticResults = await airis-exec({
    tool: "morphllm:semantic_query",
    arguments: { repo_path: "/project", query: "..." }
  });
} catch (error) {
  if (error.message.includes("not available") || error.message.includes("not indexed")) {
    console.warn("⚠️ MorphLLM 不可用，回退到 MorphLLM grep_search...");

    // 回退：使用 grep 搜索
    const grepResults = await airis-exec({
      tool: "morphllm:grep_search",
      arguments: {
        repo_path: "/project",
        pattern: "auth.*function"  // 正则表达式
      }
    });

    console.log("✅ 已使用 grep 搜索（无语义理解）");
    return { results: grepResults, fallback: true };
  }

  throw error;
}
```

**双服务器协同回退**:
```typescript
async function searchWithFallback(repoPath: string, query: string) {
  try {
    // 优先：MorphLLM 语义搜索
    return await airis-exec({
      tool: "morphllm:semantic_query",
      arguments: { repo_path: repoPath, query }
    });
  } catch (morphError) {
    console.warn("MorphLLM 失败，尝试 Serena 符号搜索...");

    try {
      // 回退 1：Serena 符号搜索
      return await airis-exec({
        tool: "serena:find_symbol",
        arguments: { substring: extractKeywords(query) }
      });
    } catch (serenaError) {
      console.warn("Serena 也失败，使用 grep 搜索...");

      // 回退 2：MorphLLM grep
      return await airis-exec({
        tool: "morphllm:grep_search",
        arguments: {
          repo_path: repoPath,
          pattern: convertToRegex(query)
        }
      });
    }
  }
}
```

---

### 完整错误处理示例（端到端）

```typescript
async function robustCodeSearch(repoPath: string, query: string) {
  // Step 1: Gateway 健康检查（错误类型 2）
  try {
    const health = await airis-exec({ tool: "gateway-control:health" });
    if (!health.ok) {
      throw new Error("Gateway 不健康");
    }
  } catch (error) {
    throw new Error(`Gateway 不可用: ${error.message}`);
  }

  // Step 2: 确保双服务器可用（错误类型 4）
  await ensureBothServersAvailable();

  // Step 3: 参数验证（错误类型 1）
  if (!repoPath.startsWith("/")) {
    throw new Error("repo_path 必须是绝对路径");
  }

  // Step 4: MorphLLM 语义搜索（错误类型 3 - 项目未索引）
  let semanticResults;
  try {
    semanticResults = await airis-exec({
      tool: "morphllm:semantic_query",
      arguments: { repo_path: repoPath, query, max_results: 10 }
    });
  } catch (error) {
    if (error.message.includes("not indexed")) {
      throw new Error("项目未索引，请先使用 airis-project-indexing skill 索引项目");
    }
    // 回退到 grep 搜索
    console.warn("语义搜索失败，使用 grep 搜索...");
    semanticResults = await airis-exec({
      tool: "morphllm:grep_search",
      arguments: { repo_path: repoPath, pattern: query }
    });
  }

  // Step 5: Serena 符号分析（错误类型 3 - 项目未激活）
  let symbolDetails;
  if (semanticResults.results.length > 0) {
    try {
      const topResult = semanticResults.results[0];
      symbolDetails = await airis-exec({
        tool: "serena:find_symbol",
        arguments: { name: extractSymbolName(topResult.code_snippet) }
      });
    } catch (error) {
      if (error.message.includes("no active project")) {
        console.log("激活 Serena 项目...");
        await airis-exec({
          tool: "serena:activate_project",
          arguments: { name: extractProjectName(repoPath) }
        });
        // 重试
        symbolDetails = await airis-exec({
          tool: "serena:find_symbol",
          arguments: { name: extractSymbolName(semanticResults.results[0].code_snippet) }
        });
      } else {
        console.warn("Serena 分析失败，跳过符号详情...");
        symbolDetails = null;
      }
    }
  }

  return { semanticResults, symbolDetails };
}
```

---

## 📚 参考文档

### References 文件

本 skill 包含以下参考文档（在 `references/` 目录中）:

- **morphllm-operations.md** (~120 行) - MorphLLM 三种操作详解
  - 内容: replace/insert/delete 操作类型、参数说明、边界条件、高级用法
  - 何时阅读: 需要执行复杂代码编辑时

- **placeholder-patterns.md** (~80 行) - 占位符最佳实践
  - 内容: 占位符语法、常见模式、错误示例、修复方案
  - 何时阅读: 遇到占位符相关错误时

### Scripts 文件

- **validate_file_size.py** (~50 行) - 文件大小验证工具
  - 功能: 检查文件是否适合 MorphLLM 编辑（< 2000 行）
  - 用法: `python scripts/validate_file_size.py <file_path>`

---

## 🔗 相关资源

**MCP 服务器文档**:
- [MorphLLM MCP](../../ai_workflow/docs/airis-mcp-gateway/servers/MORPHLLM.md) - 代码编辑和搜索
- [Serena MCP](../../ai_workflow/docs/airis-mcp-gateway/servers/SERENA.md) - 语义搜索和记忆管理

**AIRIS MCP Gateway**:
- [完整指南](../../ai_workflow/docs/airis-mcp-gateway/README.md)
- [工具索引](../../ai_workflow/docs/airis-mcp-gateway/TOOL_INDEX.md)

**相关 Skills**:
- airis-web-research - Web 研究和内容保存
- airis-project-indexing - 项目索引和深度分析

---

## 📊 性能和限制

**性能考虑**:
- 语义搜索: ~3-5 秒/查询
- Grep 搜索: ~1-2 秒/查询
- 文件编辑: ~2-4 秒/操作
- **总耗时**: 约 5-10 秒/完整流程

**限制条件**:
- 文件大小: < 2000 行（MorphLLM 限制）
- 仓库大小: 建议 < 100MB（搜索性能）
- 编辑操作: 一次建议编辑 < 5 个位置

**最佳实践**:
- 对于大文件，优先使用 grep 精确定位，减少语义搜索范围
- 编辑前使用 `validate_file_size.py` 检查文件大小
- 使用占位符模式，一次只编辑需要修改的部分
- 批量编辑时，先测试一个文件，确认无误后再批量操作
- 使用 Serena 保存搜索结果，避免重复搜索

---

**版本**: 1.0.0
**最后更新**: 2025-12-30
**作者**: Hao
