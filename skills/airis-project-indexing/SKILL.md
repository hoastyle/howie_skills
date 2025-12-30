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
