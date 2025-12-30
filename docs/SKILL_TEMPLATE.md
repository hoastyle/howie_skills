---
name: airis-example-skill
description: "简短描述这个 skill 的功能和触发条件（1-2 句话，100-200 词）。包含：(1) 做什么，(2) 何时使用，(3) 具体的触发条件。"
---

# AIRIS [操作]-[领域] Helper

**MCP 服务器**: [列出使用的 MCP 服务器，如 tavily, serena]
**复杂度**: [simple/medium/high]
**预估行数**: [200-500]

---

## 🎯 触发条件 (30 行)

### 何时使用这个 Skill

**主要场景**:
- 场景 1: [具体描述]
- 场景 2: [具体描述]
- 场景 3: [具体描述]

**关键词触发**:
- [关键词 1]
- [关键词 2]
- [关键词 3]

**典型用户请求**:
```
"帮我..."
"我需要..."
"请..."
```

---

## 📋 工作流程 (120-200 行)

### [选项 A: 线性流程]

#### Phase 1: [阶段名称]

**功能**: [简要说明]

**使用的工具**:
```typescript
// Step 1: [操作描述]
airis-exec({
  tool: "server:tool_name",
  arguments: {
    param1: "value1",
    param2: "value2"
  }
})
```

**参数说明**:
- `param1` - [说明]
- `param2` - [说明]

**返回结果**:
```json
{
  "field1": "...",
  "field2": "..."
}
```

---

#### Phase 2: [阶段名称]

[重复上述结构]

---

### [选项 B: 决策树流程]

#### 决策点: [选择标准]

**路径 1**: 如果 [条件]
→ [使用工具 A]
→ [后续步骤]

**路径 2**: 如果 [条件]
→ [使用工具 B]
→ [后续步骤]

---

## 💻 完整示例 (40-50 行)

### 示例 1: [场景名称]

**用户需求**:
```
[具体的用户请求]
```

**执行步骤**:

```typescript
// Step 1: [操作描述]
const result1 = await airis-exec({
  tool: "server:tool_name",
  arguments: { /* ... */ }
});

// Step 2: [操作描述]
const result2 = await airis-exec({
  tool: "server:tool_name2",
  arguments: { /* ... */ }
});

// Step 3: [最终输出]
console.log(result2);
```

**预期输出**:
```
[输出结果]
```

---

### 示例 2: [另一个场景]

[重复上述结构]

---

## ⚠️ 常见陷阱和解决方案 (30 行)

### 陷阱 1: [问题描述]

**错误现象**:
```
[错误信息或表现]
```

**原因分析**:
[为什么会发生这个问题]

**解决方案**:
```typescript
// ❌ 错误做法
{
  wrong_param: "value"
}

// ✅ 正确做法
{
  correct_param: "value"
}
```

---

### 陷阱 2: [问题描述]

[重复上述结构]

---

### 陷阱 3: [问题描述]

[重复上述结构]

---

## 📚 参考文档 (20 行)

### References 文件

本 skill 包含以下参考文档（在 `references/` 目录中）:

- **[文件名].md** ([行数] 行) - [简要说明]
  - 内容: [详细说明]
  - 何时阅读: [使用场景]

- **[文件名2].md** ([行数] 行) - [简要说明]
  - 内容: [详细说明]
  - 何时阅读: [使用场景]

### Scripts 文件（可选）

- **[脚本名].py** - [功能说明]
  - 用法: `python scripts/[脚本名].py [参数]`

---

## 🔗 相关资源

**MCP 服务器文档**:
- [Server Name] - [链接到 ai_workflow/docs/airis-mcp-gateway/servers/]

**AIRIS MCP Gateway**:
- [完整指南](../../ai_workflow/docs/airis-mcp-gateway/README.md)
- [工具索引](../../ai_workflow/docs/airis-mcp-gateway/TOOL_INDEX.md)

**相关 Skills**:
- [相关 skill 名称] - [简要说明关系]

---

## 📊 性能和限制

**性能考虑**:
- [性能相关注意事项]
- [推荐的使用规模]

**限制条件**:
- [限制 1]
- [限制 2]

**最佳实践**:
- [建议 1]
- [建议 2]

---

**版本**: 1.0.0
**最后更新**: 2025-12-30
**作者**: Hao
