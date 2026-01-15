# 知识管理系统验证和使用指南

**版本**: 1.0.0
**日期**: 2025-01-15
**状态**: ✅ 完成

---

## 📊 执行摘要

本指南提供了 AIRIS Skills 知识管理系统的完整验证流程和使用方法，确保每次访问都能正常工作。

### 核心成果

**1. 三层记忆架构设计**
- ✅ 短期记忆（Memory MCP）- 会话级临时图谱
- ✅ 项目记忆（Serena）- 项目级文档管理
- ✅ 长期记忆（Mindbase）- 跨项目知识库 + 对话历史

**2. 更新的 Skills**
- ✅ `airis-knowledge-mgmt` v2.0.0 - 整合三层架构
- ✅ 移除错误的工具描述
- ✅ 添加 Mindbase 13 个工具支持
- ✅ 添加决策树和使用场景映射

**3. 完整文档**
- ✅ `MINDBASE_STANDARD_GUIDE.md` - Mindbase 完整指南（450+ 行）
- ✅ `KNOWLEDGE_ARCHITECTURE_DESIGN.md` - 架构设计文档（600+ 行）
- ✅ `SKILL_VALIDATION_CHECKLIST.md` - 本验证指南

---

## 🔧 验证检查清单

### Step 1: Gateway 健康检查

```bash
# 检查 Gateway 是否运行
curl http://localhost:9400/health

# 预期输出
# {"status": "healthy"}
```

**使用 AIRIS MCP Gateway 验证**:
```typescript
const health = await airis-exec({
  tool: "airis-mcp-gateway-control:gateway_health"
});

if (!health.ok) {
  throw new Error("Gateway 不可用");
}
```

### Step 2: 验证 Mindbase 工具

```typescript
// 1. 发现 Mindbase 工具
const mindbaseTools = await airis-find({ query: "mindbase" });

// 2. 检查工具数量
console.log("Mindbase 工具数量:", mindbaseTools.length);
// 预期: 13 个工具

// 3. 验证核心工具存在
const requiredTools = [
  "mindbase:memory_write",
  "mindbase:memory_search",
  "mindbase:conversation_save",
  "mindbase:session_create"
];

for (const tool of requiredTools) {
  if (!mindbaseTools.some(t => t.name === tool)) {
    throw new Error(`缺少必需工具: ${tool}`);
  }
}
```

### Step 3: 验证 Serena 工具

```typescript
// 1. 发现 Serena 工具
const serenaTools = await airis-find({ query: "serena" });

// 2. 验证核心工具
const coreSerenaTools = [
  "serena:write_memory",
  "serena:read_memory",
  "serena:list_memories"
];

for (const tool of coreSerenaTools) {
  if (!serenaTools.some(t => t.name === tool)) {
    console.warn(`Serena 工具不可用: ${tool}`);
  }
}
```

### Step 4: 验证 Memory MCP 工具（可选）

```typescript
// Memory MCP 可能在某些配置中不可用
const memoryTools = await airis-find({ query: "memory" });

const hasMemoryGraph = memoryTools.some(t =>
  t.name === "memory:create_entities"
);

if (hasMemoryGraph) {
  console.log("✅ Memory MCP 知识图谱工具可用");
} else {
  console.log("⚠️  Memory MCP 知识图谱工具不可用（这是正常的）");
}
```

### Step 5: 功能验证测试

```typescript
// 测试 Mindbase memory_write
try {
  await airis-exec({
    tool: "mindbase:memory_write",
    arguments: {
      name: "validation-test-" + Date.now(),
      content: "# Validation Test\n\nTesting Mindbase functionality.",
      category: "note"
    }
  });
  console.log("✅ Mindbase memory_write 工作正常");
} catch (error) {
  console.error("❌ Mindbase memory_write 失败:", error.message);
}

// 测试 Mindbase memory_search
try {
  const results = await airis-exec({
    tool: "mindbase:memory_search",
    arguments: {
      query: "validation test",
      limit: 1
    }
  });
  console.log("✅ Mindbase memory_search 工作正常");
} catch (error) {
  console.error("❌ Mindbase memory_search 失败:", error.message);
}

// 测试 Serena write_memory（如果可用）
try {
  await airis-exec({
    tool: "serena:write_memory",
    arguments: {
      memory_file_name: "validation-test.md",
      content: "# Validation Test\n\nTesting Serena functionality."
    }
  });
  console.log("✅ Serena write_memory 工作正常");
} catch (error) {
  console.warn("⚠️  Serena write_memory 不可用或失败:", error.message);
}
```

---

## 📋 使用场景决策树

### 快速参考

```
用户需求
    │
    ├─ 跨项目知识？
    │   → Mindbase (memory_*)
    │
    ├─ 对话历史？
    │   → Mindbase (conversation_*)
    │
    ├─ 会话管理？
    │   → Mindbase (session_*)
    │
    ├─ 项目文档？
    │   → Serena (write_memory)
    │
    └─ 临时图谱？
        → Memory MCP (create_entities) [如果可用]
```

### 详细场景映射表

| 用户请求 | 推荐方案 | 工具 | 示例 |
|---------|---------|------|------|
| "保存架构模式" | Mindbase | `memory_write` | category: "pattern" |
| "搜索对话历史" | Mindbase | `conversation_search` | query: "..." |
| "创建项目会话" | Mindbase | `session_create` | name: "..." |
| "保存 ADR" | Serena | `write_memory` | memory_file_name: "adr-001.md" |
| "快速概念图" | Memory MCP | `create_entities` | entities: [...] |

---

## 🔌 标准化访问模式

### 四步工作流

```typescript
// Step 1: 工具发现
const tools = await airis-find({ query: "mindbase" });

// Step 2: 参数验证
const schema = await airis-schema({
  tool: "mindbase:memory_write"
});

// Step 3: 执行操作
const result = await airis-exec({
  tool: "mindbase:memory_write",
  arguments: { name: "...", content: "..." }
});

// Step 4: 错误处理
if (!result) {
  throw new Error("操作失败");
}
```

### 参数正确性验证

**Mindbase 参数**:
```typescript
// ✅ 正确
{
  name: "doc-name",
  content: "# Content",
  category: "pattern",
  tags: ["tag1", "tag2"]
}

// ❌ 错误
{
  filename: "doc.md",  // 错误：应该是 name
  body: "content"      // 错误：应该是 content
}
```

**Serena 参数**:
```typescript
// ✅ 正确
{
  memory_file_name: "doc.md",
  content: "# Content"
}

// ❌ 错误
{
  filename: "doc.md"  // 错误：应该是 memory_file_name
}
```

---

## 📊 性能基准

### 预期延迟

| 操作 | 预期延迟 | 备注 |
|------|---------|------|
| Mindbase memory_write | 500-1000ms | 首次调用可能更慢 |
| Mindbase memory_search | 500-1000ms | 向量搜索 |
| Mindbase conversation_save | 500-1000ms | 包含嵌入生成 |
| Serena write_memory | 200-500ms | 文件系统操作 |
| Memory MCP create_entities | <100ms | 内存操作 |

### 优化建议

1. **批量操作**: 一次调用处理多个项目
2. **异步处理**: 使用 `run_in_background` 处理大量数据
3. **缓存结果**: 缓存常用搜索结果
4. **定期清理**: 删除过时的记忆和对话

---

## 🚨 故障排查

### 问题 1: Mindbase 工具不可用

**症状**:
```
Error: Tool 'mindbase:memory_write' not found
```

**解决方案**:
```bash
# 1. 检查 Gateway 是否运行
docker ps | grep airis-mcp-gateway

# 2. 检查 Mindbase 容器
docker ps | grep mindbase

# 3. 检查配置
cat /path/to/airis-mcp-gateway/mcp-config.json | grep mindbase

# 4. 重启 Gateway
cd /path/to/airis-mcp-gateway
docker compose restart
```

### 问题 2: 向量搜索失败

**症状**:
```
Error: Failed to generate embeddings
```

**解决方案**:
```bash
# 1. 检查 Ollama 服务
curl http://localhost:11434/api/version

# 2. 检查模型是否已下载
ollama list | grep nomic

# 3. 下载模型（如果缺失）
ollama pull nomic-embed-text
```

### 问题 3: Serena 参数错误

**症状**:
```
Error: Unknown parameter 'filename'
```

**解决方案**:
```typescript
// 使用正确的参数名称
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "doc.md",  // ✅ 正确
    content: "..."
  }
});
```

---

## 📚 完整文档索引

### 核心文档

1. **[MINDBASE_STANDARD_GUIDE.md](MINDBASE_STANDARD_GUIDE.md)**
   - Mindbase 完整使用指南
   - 13 个工具详细说明
   - 参数参考和示例
   - 450+ 行

2. **[KNOWLEDGE_ARCHITECTURE_DESIGN.md](KNOWLEDGE_ARCHITECTURE_DESIGN.md)**
   - 三层记忆架构设计
   - MCP 服务器角色分析
   - 使用场景映射
   - 600+ 行

3. **[airis-knowledge-mgmt/SKILL.md](../skills/airis-knowledge-mgmt/SKILL.md)**
   - 更新后的 skill 定义
   - v2.0.0 三层架构版本
   - 完整示例和最佳实践
   - 775 行

### 快速参考

| 文档 | 用途 | 何时阅读 |
|------|------|---------|
| **MINDBASE_STANDARD_GUIDE.md** | Mindbase 工具详情 | 使用 Mindbase 前 |
| **KNOWLEDGE_ARCHITECTURE_DESIGN.md** | 架构理解和决策 | 系统设计时 |
| **SKILL_VALIDATION_CHECKLIST.md** | 验证和故障排查 | 部署和调试 |
| **airis-knowledge-mgmt/SKILL.md** | 使用示例和模式 | 日常开发 |

---

## ✅ 最终验证

### 完整验证脚本

```typescript
async function validateKnowledgeSystem() {
  console.log("开始验证知识管理系统...\n");

  // 1. Gateway 健康检查
  console.log("1. 检查 Gateway 状态...");
  const health = await airis-exec({
    tool: "airis-mcp-gateway-control:gateway_health"
  });
  if (!health.ok) throw new Error("Gateway 不可用");
  console.log("✅ Gateway 正常\n");

  // 2. 验证 Mindbase 工具
  console.log("2. 验证 Mindbase 工具...");
  const mindbaseTools = await airis-find({ query: "mindbase" });
  console.log(`✅ 找到 ${mindbaseTools.length} 个 Mindbase 工具\n`);

  // 3. 验证 Serena 工具
  console.log("3. 验证 Serena 工具...");
  const serenaTools = await airis-find({ query: "serena" });
  console.log(`✅ 找到 ${serenaTools.length} 个 Serena 工具\n`);

  // 4. 功能测试
  console.log("4. 运行功能测试...");

  // Mindbase 测试
  await airis-exec({
    tool: "mindbase:memory_write",
    arguments: {
      name: "validation-test-" + Date.now(),
      content: "# Validation Test",
      category: "note"
    }
  });
  console.log("✅ Mindbase memory_write 正常");

  const searchResults = await airis-exec({
    tool: "mindbase:memory_search",
    arguments: { query: "validation", limit: 1 }
  });
  console.log("✅ Mindbase memory_search 正常\n");

  // 5. 总结
  console.log("✅ 所有验证通过！");
  console.log(`- Mindbase 工具: ${mindbaseTools.length}`);
  console.log(`- Serena 工具: ${serenaTools.length}`);
  console.log(`- Gateway 状态: 健康`);
  console.log("\n知识管理系统已就绪。");
}

// 运行验证
await validateKnowledgeSystem();
```

---

## 🎯 下一步行动

### 立即行动

1. **运行验证脚本**: 确保所有工具可用
2. **阅读核心文档**: 理解三层记忆架构
3. **尝试示例代码**: 熟悉使用模式

### 短期目标（本周）

1. **更新现有 workflows**: 使用 Mindbase 替代临时存储
2. **建立会话管理**: 为长期项目创建会话
3. **迁移关键知识**: 将重要决策保存到 Mindbase

### 长期目标（本月）

1. **建立知识库**: 创建跨项目的共享知识
2. **优化搜索**: 使用语义搜索提高效率
3. **定期维护**: 清理过时的记忆和对话

---

**版本**: 1.0.0
**最后更新**: 2025-01-15
**维护者**: Hao
**状态**: ✅ 生产就绪
