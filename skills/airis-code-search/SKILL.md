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
