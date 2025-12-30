---
name: airis-project-indexing
description: 项目索引和分析助手，使用 AIRIS Agent 进行仓库索引、代码生成和深度研究。适用于大型项目理解、代码库分析、自动化任务编排等场景。支持项目结构摘要、主题深度研究、基于上下文的代码生成。
---

# AIRIS Project Indexing & Analysis Helper

**MCP 服务器**: airis-agent
**复杂度**: medium
**预估行数**: 240

---

## 🎯 触发条件

### 何时使用这个 Skill

**主要场景**:
- **大型项目理解**: 快速理解陌生代码库的结构和架构
- **代码库分析**: 分析项目依赖、技术栈、代码组织
- **深度研究**: 对特定主题进行深入调研（架构、性能、安全）
- **代码生成**: 基于项目上下文生成符合规范的代码
- **自动化任务**: 编排复杂的多步骤开发任务

**关键词触发**:
- "索引项目"、"分析代码库"、"理解项目结构"
- "深度研究"、"代码生成"、"自动化任务"
- "AIRIS Agent"、"project indexing"

**典型用户请求**:
```
"索引这个项目并生成结构摘要"
"深入研究这个项目的架构设计模式"
"基于项目规范生成一个 API 端点"
"分析项目的性能瓶颈"
```

---

## 📋 三功能工作流

### 功能 1: 项目索引

**功能**: 索引项目代码库，生成结构摘要

**执行索引**:
```typescript
// Step 1: 索引项目
const index = await airis-exec({
  tool: "airis-agent:index_repo",
  arguments: {
    repo_path: "/home/user/project",
    max_files: 500,               // 最大文件数（避免超大项目）
    include_patterns: ["*.ts", "*.tsx", "*.js"],  // 包含的文件类型
    exclude_patterns: ["node_modules/**", "dist/**"]  // 排除目录
  }
});
```

**参数说明**:
- `repo_path` (必需) - 项目根目录绝对路径
- `max_files` - 最大索引文件数（默认 500）
- `include_patterns` - 包含的文件模式（可选）
- `exclude_patterns` - 排除的文件模式（可选）

**返回结果**:
```json
{
  "summary": {
    "total_files": 234,
    "languages": {
      "TypeScript": 180,
      "JavaScript": 40,
      "CSS": 14
    },
    "structure": {
      "src/": {
        "components/": 45,
        "services/": 12,
        "utils/": 8
      },
      "tests/": 35
    },
    "dependencies": {
      "react": "^18.2.0",
      "typescript": "^5.0.0"
    }
  },
  "indexed_at": "2025-12-30T15:00:00Z"
}
```

---

### 功能 2: 深度研究

**功能**: 对特定主题进行深入调研

**执行研究**:
```typescript
// Step 2: 深度研究
const research = await airis-exec({
  tool: "airis-agent:deep_research",
  arguments: {
    repo_path: "/home/user/project",
    topic: "authentication architecture and security patterns",
    depth: "comprehensive",      // quick | moderate | comprehensive
    focus_areas: ["security", "architecture", "best-practices"]
  }
});
```

**参数说明**:
- `repo_path` (必需) - 项目路径
- `topic` (必需) - 研究主题（自然语言描述）
- `depth` - 研究深度
  - `quick`: 快速概览（1-2 分钟）
  - `moderate`: 中等深度（3-5 分钟）
  - `comprehensive`: 全面分析（5-10 分钟）
- `focus_areas` - 关注领域（可选）

**返回结果**:
```json
{
  "topic": "authentication architecture",
  "findings": [
    {
      "category": "security",
      "title": "JWT Token Management",
      "description": "Project uses JWT for authentication with proper token rotation...",
      "files": ["src/services/auth.ts", "src/middleware/jwt.ts"],
      "recommendations": ["Consider adding refresh token mechanism", "Implement token blacklist"]
    }
  ],
  "summary": "The project implements secure authentication using JWT...",
  "confidence": 0.92
}
```

---

### 功能 3: 代码生成

**功能**: 基于项目上下文生成代码

**执行生成**:
```typescript
// Step 3: 生成代码
const code = await airis-exec({
  tool: "airis-agent:generate_code",
  arguments: {
    repo_path: "/home/user/project",
    description: "Create a new API endpoint for user profile update following project conventions",
    target_path: "src/routes/user.ts",
    follow_conventions: true     // 遵循项目规范
  }
});
```

**参数说明**:
- `repo_path` (必需) - 项目路径
- `description` (必需) - 代码功能描述
- `target_path` (必需) - 目标文件路径
- `follow_conventions` - 是否遵循项目规范（默认 true）

**返回结果**:
```json
{
  "code": "import { Router } from 'express';\n...",
  "file_path": "src/routes/user.ts",
  "conventions_used": [
    "Express router pattern",
    "Async/await error handling",
    "TypeScript type annotations"
  ]
}
```

---

## 💻 完整示例

### 示例 1: 索引 + 研究 + 生成

**用户需求**:
```
"理解这个项目的架构，然后生成一个符合规范的新 API 端点"
```

**执行步骤**:

```typescript
// Step 1: 索引项目
const projectIndex = await airis-exec({
  tool: "airis-agent:index_repo",
  arguments: {
    repo_path: "/home/user/my-api-project",
    max_files: 300,
    exclude_patterns: ["node_modules/**", "dist/**", "*.test.ts"]
  }
});

console.log(`
📊 项目索引完成
- 总文件数: ${projectIndex.summary.total_files}
- 主要语言: ${Object.keys(projectIndex.summary.languages).join(', ')}
- 依赖: ${Object.keys(projectIndex.summary.dependencies).length} 个
`);

// Step 2: 研究 API 架构模式
const apiResearch = await airis-exec({
  tool: "airis-agent:deep_research",
  arguments: {
    repo_path: "/home/user/my-api-project",
    topic: "REST API endpoint patterns, authentication, error handling",
    depth: "moderate",
    focus_areas: ["architecture", "security"]
  }
});

console.log(`
🔍 API 架构研究
${apiResearch.summary}

关键发现:
${apiResearch.findings.map(f => `- ${f.title}: ${f.description}`).join('\n')}
`);

// Step 3: 生成新的 API 端点
const newEndpoint = await airis-exec({
  tool: "airis-agent:generate_code",
  arguments: {
    repo_path: "/home/user/my-api-project",
    description: "Create a POST /api/users endpoint for user registration with validation and error handling",
    target_path: "src/routes/users.ts",
    follow_conventions: true
  }
});

console.log(`
✅ API 端点已生成: ${newEndpoint.file_path}

遵循的规范:
${newEndpoint.conventions_used.map(c => `- ${c}`).join('\n')}
`);

// Step 4: 保存研究结果到 Serena
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "my-api-project-analysis.md",
    content: `# My API Project Analysis

## 项目结构
${JSON.stringify(projectIndex.summary, null, 2)}

## API 架构研究
${apiResearch.summary}

## 生成的代码
路径: ${newEndpoint.file_path}
规范: ${newEndpoint.conventions_used.join(', ')}

---
**分析日期**: ${new Date().toISOString().split('T')[0]}
`
  }
});
```

**预期输出**:
```
📊 项目索引完成
- 总文件数: 234
- 主要语言: TypeScript, JavaScript
- 依赖: 45 个

🔍 API 架构研究
The project follows RESTful conventions with Express.js...

关键发现:
- JWT Token Management: Proper token rotation implemented
- Error Handling: Centralized error middleware
- Validation: Using Joi for request validation

✅ API 端点已生成: src/routes/users.ts

遵循的规范:
- Express router pattern
- Async/await error handling
- Joi validation middleware
```

---

## ⚠️ 常见陷阱和解决方案

### 陷阱 1: 项目过大

**错误现象**:
```
Error: Too many files to index
Warning: Indexing may take a long time
```

**原因分析**:
项目文件数超过限制或包含大量无关文件

**解决方案**:
```typescript
// ❌ 不推荐：索引整个项目（包括 node_modules）
{
  repo_path: "/home/user/project"
}

// ✅ 推荐：排除无关目录
{
  repo_path: "/home/user/project",
  max_files: 500,
  exclude_patterns: [
    "node_modules/**",
    "dist/**",
    "build/**",
    "*.test.ts",
    "*.spec.ts"
  ]
}

// ✅ 推荐：只包含关键文件类型
{
  include_patterns: ["*.ts", "*.tsx", "*.js"],
  exclude_patterns: ["**/*.min.js", "**/*.d.ts"]
}
```

---

### 陷阱 2: Gateway 未运行

**错误现象**:
```
Error: AIRIS Agent not available
Error: Connection refused
```

**原因分析**:
AIRIS MCP Gateway 未启动或 AIRIS Agent 服务未运行

**解决方案**:
```bash
# 检查 Gateway 状态
curl http://localhost:9400/health

# 如果未运行，启动 Gateway
# （根据你的安装方式）
airis-gateway start

# 验证 AIRIS Agent 可用
airis-gateway list-servers
# 应显示 "airis-agent" 在列表中
```

---

## 🔌 AIRIS MCP Gateway 标准访问模式（完整版）

本章节展示完整的 AIRIS MCP Gateway 访问模式，确保工具使用的标准化和可靠性。

### 四步标准化工作流

#### Step 1: 工具发现 (airis-find)

使用 `airis-find` 发现 AIRIS Agent 提供的工具：

```typescript
// 发现 AIRIS Agent 工具
const airisTools = await airis-find({
  query: "airis-agent"
});
console.log("AIRIS Agent 工具:", airisTools.map(t => t.name));
// 输出: ["airis-agent:index_repo", "airis-agent:deep_research", "airis-agent:generate_code", ...]
```

**为什么需要这一步？**
- 发现 AIRIS Agent 的所有可用功能
- 确认工具名称拼写正确
- 验证 AIRIS Agent MCP 服务器已正确安装

---

#### Step 2: 参数验证 (airis-schema)

在执行前，使用 `airis-schema` 检查工具的参数要求：

```typescript
// 检查 index_repo 参数
const indexSchema = await airis-schema({
  tool: "airis-agent:index_repo"
});
console.log("必需参数:", indexSchema.inputSchema.required);
// 输出: ["repo_path"]
console.log("可选参数:", Object.keys(indexSchema.inputSchema.properties));
// 输出: ["repo_path", "max_files", "include_patterns", "exclude_patterns"]

// 检查 deep_research 参数
const researchSchema = await airis-schema({
  tool: "airis-agent:deep_research"
});
console.log("研究工具参数:", researchSchema.inputSchema.required);
// 输出: ["repo_path", "topic"]

// 检查 generate_code 参数
const generateSchema = await airis-schema({
  tool: "airis-agent:generate_code"
});
console.log("代码生成参数:", generateSchema.inputSchema.required);
// 输出: ["repo_path", "description", "target_path"]
```

**常见参数命名陷阱**（本 skill 涉及）:
- ⚠️ `repo_path` 必须是绝对路径（不能是相对路径）
- ⚠️ `max_files` 建议设置为 500 以下避免超时
- ⚠️ `exclude_patterns` 使用 glob 模式（如 `node_modules/**`）
- ⚠️ `depth` 参数影响研究耗时（quick < moderate < comprehensive）

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

// 验证 AIRIS Agent 已启动
const airisAgent = servers.find(s => s.name === "airis-agent");

if (!airisAgent) {
  throw new Error("AIRIS Agent 服务器未安装");
}

if (airisAgent.mode === "HOT" && airisAgent.ready) {
  console.log("✅ AIRIS Agent 已就绪（HOT 模式，即时响应）");
} else {
  console.log("⏳ 等待 AIRIS Agent 启动...");
  await sleep(2000);
}
```

**什么时候需要健康检查？**
- ✅ 长时间运行的索引任务（如大型项目）
- ✅ 生产环境部署
- ✅ 首次使用 AIRIS Agent
- ⚠️ 快速原型开发时可以跳过（但要处理错误）

---

### 完整示例：端到端标准化工作流

```typescript
async function standardizedProjectAnalysis(repoPath: string, topic: string) {
  // Step 1: 健康检查
  const health = await airis-exec({
    tool: "gateway-control:health"
  });

  if (!health.ok) {
    throw new Error("Gateway 不可用");
  }

  // Step 2: 发现工具
  const tools = await airis-find({ query: "airis-agent" });
  console.log(`发现 ${tools.length} 个 AIRIS Agent 工具`);

  // Step 3: 验证参数
  const indexSchema = await airis-schema({ tool: "airis-agent:index_repo" });
  console.log("索引工具参数:", indexSchema.inputSchema);

  // Step 4: 执行索引
  const projectIndex = await airis-exec({
    tool: "airis-agent:index_repo",
    arguments: {
      repo_path: repoPath,
      max_files: 500,
      exclude_patterns: ["node_modules/**", "dist/**"]
    }
  });

  console.log(`索引完成: ${projectIndex.summary.total_files} 个文件`);

  // Step 5: 执行研究
  const research = await airis-exec({
    tool: "airis-agent:deep_research",
    arguments: {
      repo_path: repoPath,
      topic: topic,
      depth: "moderate"
    }
  });

  return { projectIndex, research };
}
```

---

## ⚙️ 服务运行模式

### MCP 服务器特性

本 skill 使用的 AIRIS Agent 为 **HOT 模式**：

| 服务器 | 工具数 | 运行模式 | 启动延迟 | 首次调用建议 |
|--------|--------|---------|---------|-------------|
| **airis-agent** | 15 | HOT 🔥 | 无延迟 | 即时可用，无需等待 |

### HOT 模式说明

**HOT 模式服务器特点**:
- 🔥 常驻内存，即时响应
- ⚡ 无启动延迟，首次调用即可使用
- 🎯 适合高频率调用和长时间运行的任务
- 💾 内存占用较高，但性能稳定

**vs COLD 模式**（不适用于本 skill）:
- ❄️ 按需启动，首次调用需要 2-5 秒
- 💤 长时间不用会自动休眠
- 🔄 重新启动需要等待

### 性能优化建议

#### 对于 HOT 模式服务器（AIRIS Agent）:

1. **可以直接调用，无需预热**
   ```typescript
   // ✅ 直接调用，无需等待
   const result = await airis-exec({
     tool: "airis-agent:index_repo",
     arguments: { repo_path: "..." }
   });
   ```

2. **适合高频率调用的场景**
   ```typescript
   // ✅ 高效：连续调用多个功能
   const index = await airis-exec({ tool: "airis-agent:index_repo", ... });
   const research = await airis-exec({ tool: "airis-agent:deep_research", ... });
   const code = await airis-exec({ tool: "airis-agent:generate_code", ... });
   // 所有调用都是即时响应
   ```

3. **响应时间稳定，适合生产环境**
   ```typescript
   // ✅ 生产环境部署推荐
   // HOT 模式确保稳定的响应时间
   const SLA = 100; // ms 响应时间目标
   const startTime = Date.now();
   const result = await airis-exec({ tool: "airis-agent:index_repo", ... });
   const responseTime = Date.now() - startTime;
   console.log(`响应时间: ${responseTime}ms`); // 通常 < 100ms
   ```

4. **长时间运行的任务无需担心服务休眠**
   ```typescript
   // ✅ 适合长时间运行的索引任务
   const largeProjectIndex = await airis-exec({
     tool: "airis-agent:index_repo",
     arguments: {
       repo_path: "/large/project",
       max_files: 5000 // 大型项目
     }
   });
   // HOT 模式确保任务不会因服务休眠而中断
   ```

### 服务可用性检查

```typescript
async function ensureAirisAgentAvailable() {
  const servers = await airis-exec({
    tool: "gateway-control:list-servers"
  });

  const airisAgent = servers.find(s => s.name === "airis-agent");

  if (!airisAgent) {
    throw new Error(`
      AIRIS Agent 服务器未安装

      请安装 AIRIS Agent：
      1. 检查 AIRIS MCP Gateway 配置
      2. 安装 AIRIS Agent MCP 服务器
      3. 重启 Gateway
    `);
  }

  if (!airisAgent.ready) {
    throw new Error("AIRIS Agent 未就绪，请检查服务状态");
  }

  console.log(`✅ AIRIS Agent 已就绪（HOT 模式，15 个工具可用）`);
  return airisAgent;
}

// 使用示例
await ensureAirisAgentAvailable();
```

---

## 🔄 统一错误处理

### 错误分类体系

本 skill 的错误可分为 4 大类：

#### 1. 参数错误 → 使用 airis-schema 预验证

**典型错误**:
```
Error: Invalid parameter 'repo_path' - must be absolute path
Error: Required parameter 'topic' is missing
Error: max_files exceeds limit
```

**处理策略**:
```typescript
// ✅ 推荐：执行前验证
const schema = await airis-schema({ tool: "airis-agent:index_repo" });
const requiredParams = schema.inputSchema.required;

// 检查必需参数
if (!arguments.repo_path) {
  throw new Error("缺少必需参数: repo_path");
}

// 检查路径是否为绝对路径
if (!path.isAbsolute(arguments.repo_path)) {
  throw new Error("repo_path 必须是绝对路径");
}

// 检查 max_files 限制
if (arguments.max_files && arguments.max_files > 1000) {
  console.warn("max_files 过大可能导致超时，建议 < 500");
}

// 执行工具
await airis-exec({
  tool: "airis-agent:index_repo",
  arguments: { /* 验证后的参数 */ }
});
```

**预防措施**:
- 总是使用绝对路径
- 使用 `airis-schema` 查询正确的参数名
- 限制 `max_files` 在合理范围（< 500）
- 提供有效的 `exclude_patterns` 排除无关文件

---

#### 2. Gateway 错误 → 检查健康状态

**典型错误**:
```
Error: Failed to connect to AIRIS MCP Gateway
Error: AIRIS Agent not found
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

  // 验证 AIRIS Agent 可用
  const servers = await airis-exec({
    tool: "gateway-control:list-servers"
  });

  if (!servers.some(s => s.name === "airis-agent")) {
    throw new Error("AIRIS Agent 未安装");
  }

} catch (error) {
  console.error("Gateway 错误:", error.message);

  // 提供用户友好的错误信息
  throw new Error(`
    AIRIS MCP Gateway 不可用。请检查：
    1. Gateway 是否正在运行（http://localhost:9400/health）
    2. AIRIS Agent 是否已安装
    3. 网络连接是否正常
  `);
}
```

**预防措施**:
- 工作流开始前执行健康检查
- 验证 AIRIS Agent 在服务器列表中
- 提供清晰的错误提示和修复建议

---

#### 3. 工具执行错误 → 具体错误具体处理

**典型错误**:
```
Error: Too many files to index
Error: Research timeout
Error: Code generation failed
```

**处理策略**:

**项目过大（Too many files）**:
```typescript
try {
  const result = await airis-exec({
    tool: "airis-agent:index_repo",
    arguments: {
      repo_path: "/large/project",
      max_files: 1000
    }
  });
} catch (error) {
  if (error.message.includes("too many files")) {
    console.log("项目文件过多，使用更严格的过滤...");

    // 重试：增加排除规则
    return await airis-exec({
      tool: "airis-agent:index_repo",
      arguments: {
        repo_path: "/large/project",
        max_files: 500,
        exclude_patterns: [
          "node_modules/**",
          "dist/**",
          "build/**",
          "*.test.ts",
          "*.spec.ts",
          "*.min.js",
          "*.d.ts"
        ]
      }
    });
  }
  throw error;
}
```

**研究超时（Research timeout）**:
```typescript
try {
  const research = await airis-exec({
    tool: "airis-agent:deep_research",
    arguments: {
      repo_path: "/project",
      topic: "complex topic",
      depth: "comprehensive" // 可能超时
    }
  });
} catch (error) {
  if (error.message.includes("timeout")) {
    console.log("研究超时，降低深度重试...");

    // 回退：使用更快的深度
    return await airis-exec({
      tool: "airis-agent:deep_research",
      arguments: {
        repo_path: "/project",
        topic: "complex topic",
        depth: "moderate" // 更快
      }
    });
  }
  throw error;
}
```

**代码生成失败（Generation failed）**:
```typescript
try {
  const code = await airis-exec({
    tool: "airis-agent:generate_code",
    arguments: {
      repo_path: "/project",
      description: "vague description",
      target_path: "src/new-file.ts"
    }
  });
} catch (error) {
  if (error.message.includes("generation failed")) {
    console.log("代码生成失败，可能是描述不够具体");

    throw new Error(`
      代码生成失败。请提供更具体的描述：
      - 明确功能需求
      - 指定输入输出
      - 说明错误处理
      - 提及需要遵循的规范

      示例描述：
      "Create a POST endpoint for user registration with email validation,
       password hashing, and error handling following Express.js patterns"
    `);
  }
  throw error;
}
```

---

#### 4. 服务不可用 → 验证安装

**典型错误**:
```
Error: Server 'airis-agent' not found
Error: AIRIS Agent not ready
```

**处理策略**:

**服务器未安装**:
```typescript
const servers = await airis-exec({
  tool: "gateway-control:list-servers"
});

const airisAgent = servers.find(s => s.name === "airis-agent");

if (!airisAgent) {
  throw new Error(`
    AIRIS Agent 服务器未安装

    请按以下步骤安装：
    1. 检查 AIRIS MCP Gateway 配置文件
    2. 添加 AIRIS Agent 服务器配置
    3. 重启 AIRIS MCP Gateway
    4. 验证安装：airis-gateway list-servers

    配置示例：
    {
      "mcpServers": {
        "airis-agent": {
          "command": "airis-agent",
          "args": ["start"],
          "mode": "HOT"
        }
      }
    }
  `);
}
```

**服务器未就绪（HOT 模式通常不会发生）**:
```typescript
const airisAgent = servers.find(s => s.name === "airis-agent");

if (!airisAgent.ready) {
  console.log("⏳ AIRIS Agent 未就绪，等待启动...");

  // HOT 模式通常立即就绪，但仍需检查
  await sleep(2000);

  const updatedServers = await airis-exec({
    tool: "gateway-control:list-servers"
  });

  const updatedAgent = updatedServers.find(s => s.name === "airis-agent");

  if (!updatedAgent.ready) {
    throw new Error("AIRIS Agent 启动失败，请检查日志");
  }
}
```

---

### 完整错误处理示例

```typescript
async function robustProjectAnalysis(repoPath: string, topic: string) {
  try {
    // 1. 健康检查
    const health = await airis-exec({
      tool: "gateway-control:health"
    });

    if (!health.ok) {
      throw new Error("GATEWAY_UNHEALTHY");
    }

    // 2. 验证 AIRIS Agent 可用性
    await ensureAirisAgentAvailable();

    // 3. 参数验证
    if (!path.isAbsolute(repoPath)) {
      throw new Error("repo_path 必须是绝对路径");
    }

    // 4. 执行索引（带错误处理）
    let projectIndex;
    try {
      projectIndex = await airis-exec({
        tool: "airis-agent:index_repo",
        arguments: {
          repo_path: repoPath,
          max_files: 500,
          exclude_patterns: [
            "node_modules/**",
            "dist/**",
            "*.test.ts"
          ]
        }
      });
    } catch (error) {
      if (error.message.includes("too many files")) {
        // 回退：更严格的过滤
        projectIndex = await airis-exec({
          tool: "airis-agent:index_repo",
          arguments: {
            repo_path: repoPath,
            max_files: 300,
            exclude_patterns: [
              "node_modules/**",
              "dist/**",
              "build/**",
              "*.test.ts",
              "*.spec.ts",
              "*.min.js"
            ]
          }
        });
      } else {
        throw error;
      }
    }

    // 5. 执行研究（带超时处理）
    let research;
    try {
      research = await airis-exec({
        tool: "airis-agent:deep_research",
        arguments: {
          repo_path: repoPath,
          topic: topic,
          depth: "moderate"
        }
      });
    } catch (error) {
      if (error.message.includes("timeout")) {
        // 回退：使用快速模式
        research = await airis-exec({
          tool: "airis-agent:deep_research",
          arguments: {
            repo_path: repoPath,
            topic: topic,
            depth: "quick"
          }
        });
      } else {
        throw error;
      }
    }

    return { projectIndex, research };

  } catch (error) {
    // 统一错误处理
    console.error("项目分析失败:", error);

    if (error.message === "GATEWAY_UNHEALTHY") {
      throw new Error("AIRIS MCP Gateway 不可用，请检查服务状态");
    } else if (error.message.includes("not found")) {
      throw new Error("AIRIS Agent 未安装，请先安装该服务器");
    } else if (error.message.includes("absolute path")) {
      throw new Error(`repo_path 必须是绝对路径，当前: ${repoPath}`);
    } else {
      throw new Error(`分析失败: ${error.message}`);
    }
  }
}
```

---

## 📚 参考文档

### References 文件

本 skill 包含以下参考文档（在 `references/` 目录中）:

- **indexing-strategies.md** (~80 行) - 索引策略详解
  - 内容: 增量索引、全量索引、排除规则、性能优化
  - 何时阅读: 处理大型项目或需要优化索引性能时

- **research-templates.md** (~70 行) - 研究主题模板
  - 内容: 架构研究、性能研究、安全研究、代码质量研究模板
  - 何时阅读: 需要进行系统性研究时

---

## 🔗 相关资源

**MCP 服务器文档**:
- [AIRIS Agent] - 项目索引和分析（文档待补充）

**AIRIS MCP Gateway**:
- [完整指南](../../ai_workflow/docs/airis-mcp-gateway/README.md)
- [工具索引](../../ai_workflow/docs/airis-mcp-gateway/TOOL_INDEX.md)

**相关 Skills**:
- airis-code-search - 代码搜索和编辑
- airis-knowledge-mgmt - 知识整理（保存研究结果）

---

## 📊 性能和限制

**性能考虑**:
- 项目索引: ~10-60 秒（取决于项目大小）
- 深度研究: ~1-10 分钟（取决于 depth 参数）
- 代码生成: ~5-15 秒
- **总耗时**: 约 1-15 分钟/完整流程

**限制条件**:
- 文件数限制: 建议 < 500 个文件
- 项目大小: 建议 < 100MB
- 研究深度: comprehensive 模式可能较慢
- Gateway 依赖: 需要 AIRIS MCP Gateway 运行

**最佳实践**:
- 首次使用先用 `max_files: 100` 测试
- 排除测试文件、构建产物、依赖目录
- 使用 `quick` depth 进行初步探索
- 研究主题要具体明确
- 定期更新项目索引（代码变更后）
- 将研究结果保存到 Serena 记忆供后续参考
- 大型项目考虑分模块索引

---

**版本**: 1.0.0
**最后更新**: 2025-12-30
**作者**: Hao
