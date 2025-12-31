# 🚀 Howie AIRIS Skills 快速入门指南

**5 分钟上手 AIRIS MCP Gateway 的 7 个核心操作**

---

## 📋 前置要求

1. ✅ **AIRIS MCP Gateway 已安装并运行**
   ```bash
   # 检查 Gateway 状态
   curl http://localhost:9400/api/tools/status
   ```

2. ✅ **Claude Code 已安装 howie_skills**
   ```bash
   # 检查安装
   ls ~/.claude/skills/ | grep airis
   ```

---

## 🎯 3 步快速验证

### Step 1: 测试 Web 研究

```typescript
// 在 Claude Code 中直接运行
用户: "帮我研究一下 React Server Components 的最新进展"

// howie_skills 会自动:
// 1. 使用 Tavily 搜索最新资讯
// 2. 使用 Fetch 提取详细内容
// 3. 使用 Serena 保存到 .serena/memories/
```

**预期结果**:
- ✅ 在 `.serena/memories/` 目录下生成研究报告
- ✅ Claude Code 显示结构化的研究摘要

---

### Step 2: 测试代码搜索

```typescript
用户: "找到项目中所有处理用户认证的代码"

// howie_skills 会:
// 1. 使用 MorphLLM 语义搜索代码库
// 2. 定位相关文件和函数
// 3. 保存搜索结果到 Serena
```

**预期结果**:
- ✅ 列出所有认证相关的文件和函数
- ✅ 提供代码片段和行号

---

### Step 3: 测试知识管理

```typescript
用户: "记录一下今天的架构决策：选择 PostgreSQL 作为主数据库"

// howie_skills 会:
// 1. 使用 Memory MCP 创建知识图谱实体
// 2. 使用 Serena 保存详细记录
// 3. 建立实体之间的关系
```

**预期结果**:
- ✅ 在 Memory 中创建 "PostgreSQL" 实体
- ✅ 在 Serena 中保存完整决策记录

---

## 📚 7 个 Skills 对照表

| 需求 | 使用的 Skill | 示例触发词 |
|------|-------------|-----------|
| **Web 研究** | airis-web-research | "研究 XXX", "查询 XXX 最新动态" |
| **代码搜索** | airis-code-search | "找到 XXX 的代码", "定位 XXX 函数" |
| **知识管理** | airis-knowledge-mgmt | "记录 XXX", "创建知识图谱" |
| **浏览器自动化** | airis-browser-automation | "打开 XXX 网站", "截图 XXX" |
| **库文档查询** | airis-library-docs | "查询 React 文档", "XXX API 怎么用" |
| **UI 组件生成** | airis-ui-generation | "生成一个 Modal 组件", "创建 XXX UI" |
| **项目索引** | airis-project-indexing | "分析项目结构", "索引代码库" |

---

## ⚠️ 常见陷阱和解决方案

### 陷阱 1: 参数命名错误

**错误示例**:
```typescript
// ❌ 错误：使用 filename
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    filename: "my-note.md",  // 错误！
    content: "..."
  }
});
```

**正确做法**:
```typescript
// ✅ 正确：使用 memory_file_name
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "my-note.md",  // 正确
    content: "..."
  }
});
```

**解决方法**: 查阅 `docs/MCP_PARAMETER_REFERENCE.md` 获取正确参数名

---

### 陷阱 2: 路径必须是绝对路径

**错误示例**:
```typescript
// ❌ 错误：相对路径
arguments: {
  absolutePathToCurrentFile: "./src/Modal.tsx"  // Magic 不接受相对路径
}
```

**正确做法**:
```typescript
// ✅ 正确：绝对路径
const path = require('path');
const absolutePath = path.resolve(process.cwd(), "./src/Modal.tsx");

arguments: {
  absolutePathToCurrentFile: absolutePath  // /home/user/project/src/Modal.tsx
}
```

---

### 陷阱 3: COLD 模式服务器首次启动慢

**现象**: 第一次调用某些 MCP 工具时，等待 5-10 秒

**原因**:
- Serena、Playwright、Tavily 等是 COLD 模式服务器
- 按需启动，首次调用需要初始化

**解决方法**:
- ✅ **耐心等待** - 只有第一次慢，后续调用很快
- ✅ **批量操作** - 一次性完成多个操作，避免频繁启动

---

## 🔧 故障排查

### 问题 1: "Gateway 不可用"

**检查步骤**:
```bash
# 1. 检查 Gateway 是否运行
curl http://localhost:9400/api/tools/status

# 2. 查看 Docker 容器状态
docker ps | grep airis-mcp-gateway

# 3. 重启 Gateway
cd /path/to/airis-mcp-gateway
docker compose restart api
```

---

### 问题 2: "工具未找到"

**原因**: MCP 服务器未启用

**解决方法**:
```bash
# 检查 mcp-config.json
cat /path/to/airis-mcp-gateway/mcp-config.json | grep "enabled.*true"

# 启用所需的服务器
# 编辑 mcp-config.json，设置 "enabled": true
docker compose restart api
```

---

### 问题 3: "参数验证错误"

**解决方法**:
1. 查阅 `docs/MCP_PARAMETER_REFERENCE.md`
2. 使用三步工作流验证参数：
   ```typescript
   // Step 1: 发现工具
   airis-find({ query: "serena memory" })

   // Step 2: 查看参数
   airis-schema({ tool: "serena:write_memory" })

   // Step 3: 正确调用
   airis-exec({ tool: "serena:write_memory", arguments: {...} })
   ```

---

## 📖 进阶学习

### 完整文档索引

| 文档 | 用途 | 优先级 |
|------|------|--------|
| **README.md** | 项目总览和安装指南 | ⭐⭐⭐ |
| **docs/MCP_PARAMETER_REFERENCE.md** | 完整参数参考（1,162 行） | ⭐⭐⭐⭐ |
| **skills/*/SKILL.md** | 每个 Skill 的详细说明 | ⭐⭐⭐ |
| **docs/PARAMETER_VALIDATION_REPORT.md** | 参数验证报告 | ⭐ |

### 推荐学习路径

**初学者（第1天）**:
1. 阅读本文件（5 分钟）
2. 尝试 3 个快速验证示例（10 分钟）
3. 遇到问题查阅"常见陷阱"（5 分钟）

**进阶用户（第2-3天）**:
1. 阅读 `MCP_PARAMETER_REFERENCE.md` 高频陷阱 TOP 10（15 分钟）
2. 深入学习 2-3 个常用 Skills 的 SKILL.md（30 分钟）
3. 实践复杂工作流（1 小时）

**专家用户（长期）**:
1. 阅读所有 Skills 的完整文档
2. 贡献改进建议和 bug 报告
3. 创建自定义 Skills

---

## 💡 最佳实践

### 1. 先搜索，后调用

```typescript
// ✅ 推荐：先确认工具存在
const tools = await airis-find({ query: "memory" });
console.log("可用工具:", tools);

// 然后调用
await airis-exec({ tool: "memory:create_entities", ... });
```

### 2. 错误处理优先

```typescript
// ✅ 推荐：包裹错误处理
try {
  const result = await airis-exec({
    tool: "serena:write_memory",
    arguments: { ... }
  });
} catch (error) {
  if (error.message.includes("parameter")) {
    console.log("参数错误，请查阅 MCP_PARAMETER_REFERENCE.md");
  } else if (error.message.includes("timeout")) {
    console.log("COLD 模式服务器启动中，请重试");
  }
  throw error;
}
```

### 3. 批量操作复用连接

```typescript
// ✅ 高效：批量操作
for (const item of items) {
  // 第一次调用启动 Magic，后续调用复用连接
  await airis-exec({ tool: "magic:generate_ui", ... });
}
```

---

## 🎓 下一步

- ✅ 完成 3 个快速验证 → 基础掌握
- ✅ 阅读 MCP_PARAMETER_REFERENCE.md → 深入理解
- ✅ 实践复杂工作流 → 高级应用
- ✅ 贡献反馈和改进 → 社区贡献

---

**有问题？** 查看 `docs/MCP_PARAMETER_REFERENCE.md` 或创建 GitHub Issue

**最后更新**: 2025-12-31
**适用版本**: howie_skills v1.0.0
