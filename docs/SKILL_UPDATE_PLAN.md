# airis-knowledge-mgmt SKILL 更新计划

**创建日期**: 2026-01-15
**状态**: 待实施
**优先级**: P0（高）

---

## 📋 执行摘要

基于 2026-01-15 的实验验证，`airis-knowledge-mgmt` SKILL 需要进行以下关键更新：

1. ✅ 修正 COLD 模式服务器启动方法
2. ✅ 添加 Serena 项目激活步骤
3. ✅ 更新 Memory MCP 工具清单（从"预期"变为"已验证"）
4. ✅ 添加完整的参数说明和错误处理
5. ✅ 更新所有代码示例使用正确的工作流程

---

## 🔧 具体更新项

### 1. 添加"标准化工作流程"章节

**位置**: 在"三层记忆架构"之后，添加新章节

**内容**:
```markdown
## 🔄 标准化工作流程

### COLD 模式服务器启动

**重要**: Serena 和 Memory MCP 都是 COLD 模式服务器，首次使用前需要触发启动。

#### 正确的启动方法

```typescript
// ✅ 步骤 1: 触发服务器启动（使用 server 参数）
await airis-find({ server: "serena" });
await airis-find({ server: "memory" });

// ✅ 步骤 2: 验证服务器已启动（应该显示工具列表）
// serena (cold, enabled): 29 tools
// memory (cold, enabled): 9 tools
```

#### 常见错误

```typescript
// ❌ 错误方法 - 不会触发 COLD 服务器启动
await airis-find({ query: "serena" });
// 结果: serena (cold, enabled): 0 tools ⚠️

// ✅ 正确方法
await airis-find({ server: "serena" });
// 结果: serena (cold, enabled): 29 tools ✅
```

### Serena 项目激活要求

**关键规则**: 使用任何 Serena 工具之前，必须先激活项目。

```typescript
// Step 1: 激活项目（必需）
await airis-exec({
  tool: "serena:activate_project",
  arguments: {
    project: "."  // 当前目录，或使用已注册的项目名称
  }
});
// 返回: "The project with name 'xxx' at /path is activated."

// Step 2: 使用其他 Serena 工具
await airis-exec({
  tool: "serena:write_memory",
  arguments: { ... }
});
```

**错误处理**:
```typescript
// 如果未激活项目，会收到错误：
// "Error: No active project. Ask the user to provide the project path..."
```
```

### 2. 更新 Memory MCP 章节

**位置**: 替换当前的"Memory MCP - 短期记忆（可选）"章节

**变更**:
- 从"预期工具（需验证）"改为"已验证工具"
- 添加完整的 9 个工具清单
- 提供实际验证的代码示例

**新内容**:
```markdown
## 📋 Memory MCP - 短期记忆

### 核心功能

Memory MCP 提供会话级知识图谱，用于构建实体-关系网络。

**状态**: ✅ 所有工具已验证可用（2026-01-15）

### 完整工具清单（9 个）

| 工具 | 功能 | 状态 |
|------|------|------|
| `memory:create_entities` | 创建多个实体 | ✅ 已验证 |
| `memory:create_relations` | 创建实体间关系 | ✅ 已验证 |
| `memory:add_observations` | 添加实体观察 | ✅ 可用 |
| `memory:delete_entities` | 删除实体 | ✅ 可用 |
| `memory:delete_observations` | 删除观察 | ✅ 可用 |
| `memory:delete_relations` | 删除关系 | ✅ 可用 |
| `memory:read_graph` | 读取整个图谱 | ✅ 已验证 |
| `memory:search_nodes` | 搜索节点 | ✅ 已验证 |
| `memory:open_nodes` | 打开特定节点 | ✅ 可用 |

### 标准工作流

```typescript
// Step 1: 触发服务器启动
await airis-find({ server: "memory" });

// Step 2: 创建实体
await airis-exec({
  tool: "memory:create_entities",
  arguments: {
    entities: [
      {
        name: "UserService",
        entityType: "Component",
        observations: [
          "处理用户认证",
          "提供 REST API"
        ]
      },
      {
        name: "DatabaseLayer",
        entityType: "Component",
        observations: [
          "PostgreSQL 数据库",
          "处理数据持久化"
        ]
      }
    ]
  }
});

// Step 3: 创建关系
await airis-exec({
  tool: "memory:create_relations",
  arguments: {
    relations: [
      {
        from: "UserService",
        to: "DatabaseLayer",
        relationType: "depends_on"
      }
    ]
  }
});

// Step 4: 读取完整图谱
const graph = await airis-exec({
  tool: "memory:read_graph",
  arguments: {}
});
// 返回: { entities: [...], relations: [...] }

// Step 5: 语义搜索
const results = await airis-exec({
  tool: "memory:search_nodes",
  arguments: {
    query: "用户认证相关组件"
  }
});
```
```

### 3. 更新 Serena 章节

**位置**: 在"Serena - 项目记忆"章节

**添加内容**:
```markdown
### 重要前提条件

⚠️ **必须先激活项目**: 使用任何 Serena 工具前，必须调用 `activate_project`

```typescript
// 激活当前目录作为项目
await airis-exec({
  tool: "serena:activate_project",
  arguments: { project: "." }
});
```

### edit_memory 工具详细说明

**参数**:
```typescript
{
  memory_file_name: string;  // 必需：文件名
  needle: string;            // 必需：要替换的内容（正则或字面量）
  repl: string;              // 必需：替换后的内容
  mode: "literal" | "regex"; // 必需：匹配模式
}
```

**示例**:
```typescript
// 字面量替换
await airis-exec({
  tool: "serena:edit_memory",
  arguments: {
    memory_file_name: "project-status",
    needle: "状态: 进行中",
    repl: "状态: 已完成",
    mode: "literal"
  }
});

// 正则替换
await airis-exec({
  tool: "serena:edit_memory",
  arguments: {
    memory_file_name: "project-status",
    needle: "进度: \\d+%",
    repl: "进度: 100%",
    mode: "regex"
  }
});
```
```

### 4. 更新所有代码示例

**需要更新的位置**:
- 示例 1: 跨项目知识库管理（行 484+）
- 示例 2: 对话历史和会话管理（行 528+）
- 示例 3: 项目级文档管理（需要添加）

**更新原则**:
1. 所有示例都以触发 COLD 服务器启动开始
2. Serena 示例都包含 `activate_project` 步骤
3. 添加错误处理和验证步骤

### 5. 添加"故障排查"章节

**位置**: 在文档末尾添加

**内容**:
```markdown
## 🔧 故障排查

### 问题 1: Serena 报错 "No active project"

**症状**:
```
Error: No active project. Ask the user to provide the project path...
```

**解决方案**:
```typescript
// 先激活项目
await airis-exec({
  tool: "serena:activate_project",
  arguments: { project: "." }
});
```

### 问题 2: airis-find 返回 0 tools

**症状**:
```
serena (cold, enabled): 0 tools
```

**原因**: 使用了错误的参数名称

**解决方案**:
```typescript
// ❌ 错误
await airis-find({ query: "serena" });

// ✅ 正确
await airis-find({ server: "serena" });
```

### 问题 3: Memory MCP 工具不可用

**症状**:
```
MCP error -32602: Tool not found
```

**原因**: 服务器未启动

**解决方案**:
```typescript
// 先触发启动
await airis-find({ server: "memory" });

// 然后使用工具
await airis-exec({ tool: "memory:read_graph", arguments: {} });
```

### 问题 4: edit_memory 参数错误

**症状**:
```
3 validation errors for applyArguments
needle: Field required
repl: Field required
mode: Field required
```

**原因**: 使用了错误的参数名称

**解决方案**:
```typescript
// ❌ 错误
{ pattern: "...", replacement: "..." }

// ✅ 正确
{ needle: "...", repl: "...", mode: "literal" }
```
```

---

## 📝 实施检查清单

- [ ] 添加"标准化工作流程"章节
- [ ] 更新 Memory MCP 章节（从"预期"变为"已验证"）
- [ ] 更新 Serena 章节（添加激活要求）
- [ ] 更新所有代码示例
- [ ] 添加"故障排查"章节
- [ ] 更新 Frontmatter（version bump）
- [ ] 测试所有更新的代码示例
- [ ] 提交并标记为 v2.1

---

## 📊 影响评估

**影响范围**: 中等
- 核心功能不变
- 主要是工作流程和参数说明的完善
- 修复可能导致用户困惑的错误说明

**向后兼容性**: ✅ 完全兼容
- 只是添加和完善说明
- 不影响现有正确的用法

**测试需求**: 中等
- 需要验证所有更新的代码示例
- 需要测试故障排查章节的解决方案

---

**下一步**: 实施更新并创建 PR
