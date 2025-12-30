---
name: airis-ui-generation
description: UI 组件快速生成助手，使用 Magic MCP 生成 React/HTML 组件和搜索 Logo。支持绝对路径模式避免路径错误。适用于 UI 原型开发、组件库集成、Logo 查找等场景。注意必须使用 absolutePathToCurrentFile 而非相对路径。
---

# AIRIS UI Generation Helper

**MCP 服务器**: magic
**复杂度**: simple
**预估行数**: 220

---

## 🎯 触发条件

### 何时使用这个 Skill

**主要场景**:
- **UI 原型开发**: 快速生成组件原型
- **组件库集成**: 查找和使用现有 UI 组件
- **Logo 查找**: 搜索品牌 Logo 和图标
- **快速建模**: 根据描述生成初始 UI 代码
- **设计探索**: 快速测试不同的 UI 方案

**关键词触发**:
- "生成 UI"、"创建组件"、"生成 React 组件"
- "查找 Logo"、"搜索图标"、"品牌 Logo"
- "Modal"、"Card"、"Button"、"Form"
- "Magic"、"UI generation"

**典型用户请求**:
```
"生成一个 Modal 组件"
"创建一个用户卡片 UI"
"查找 GitHub 的 Logo"
"生成一个登录表单"
```

---

## 📋 双功能工作流

### 功能 1: 生成 UI 组件

**功能**: 根据描述生成 React 或 HTML 组件

**⚠️ 关键陷阱：必须使用绝对路径**

```typescript
// ❌ 错误：使用相对路径
await magic:generate_ui({
  description: "Create a modal component",
  path_to_current_file: "./components/Modal.tsx"  // 错误！
});

// ✅ 正确：使用绝对路径
await magic:generate_ui({
  description: "Create a modal component",
  absolutePathToCurrentFile: "/home/user/project/components/Modal.tsx"  // 正确！
});
```

**参数说明**:
- `description` (必需) - 组件描述（自然语言）
- `absolutePathToCurrentFile` (必需) - **绝对路径**到目标文件
- `framework` - 框架类型（react | html，默认 react）

**生成示例**:
```typescript
const uiComponent = await airis-exec({
  tool: "magic:generate_ui",
  arguments: {
    description: "Create a modal dialog with close button and title",
    absolutePathToCurrentFile: "/home/user/project/src/components/Modal.tsx",
    framework: "react"
  }
});
```

**返回结果**:
```json
{
  "code": "import React from 'react';\n\nexport function Modal({ title, onClose, children }) {\n  return (\n    <div className=\"modal-overlay\">\n      <div className=\"modal-content\">\n        <div className=\"modal-header\">\n          <h2>{title}</h2>\n          <button onClick={onClose}>×</button>\n        </div>\n        <div className=\"modal-body\">{children}</div>\n      </div>\n    </div>\n  );\n}",
  "file_path": "/home/user/project/src/components/Modal.tsx"
}
```

---

### 功能 2: 搜索 Logo

**功能**: 搜索品牌 Logo 和图标

**执行搜索**:
```typescript
const logo = await airis-exec({
  tool: "magic:search_logos",
  arguments: {
    query: "GitHub",
    limit: 5
  }
});
```

**参数说明**:
- `query` (必需) - Logo 搜索关键词（品牌名、公司名）
- `limit` - 返回结果数量（默认 5）

**返回结果**:
```json
{
  "logos": [
    {
      "name": "GitHub",
      "url": "https://logo.clearbit.com/github.com",
      "source": "Clearbit",
      "format": "SVG"
    },
    {
      "name": "GitHub",
      "url": "https://brandfetch.io/github.com/logo",
      "source": "Brandfetch",
      "format": "PNG"
    }
  ]
}
```

---

## 💻 完整示例

### 示例 1: 生成 Modal 组件

**用户需求**:
```
"生成一个可关闭的 Modal 组件，包含标题和内容区域"
```

**执行步骤**:

```typescript
// Step 1: 获取当前文件的绝对路径
const currentPath = process.cwd();
const targetFile = `${currentPath}/src/components/Modal.tsx`;

// Step 2: 生成 Modal 组件
const modalComponent = await airis-exec({
  tool: "magic:generate_ui",
  arguments: {
    description: "Create a Modal dialog component with title, close button, and content area. Use Tailwind CSS for styling.",
    absolutePathToCurrentFile: targetFile,
    framework: "react"
  }
});

// Step 3: 保存生成的代码
console.log(`✅ Modal 组件已生成: ${modalComponent.file_path}`);
console.log(modalComponent.code);

// 可选：保存到 Serena 记忆
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "ui-components-modal.md",
    content: `# Modal Component

## 生成路径
${modalComponent.file_path}

## 代码
\`\`\`tsx
${modalComponent.code}
\`\`\`

---
**生成日期**: ${new Date().toISOString().split('T')[0]}
`
  }
});
```

**预期输出**:
```
✅ Modal 组件已生成: /home/user/project/src/components/Modal.tsx

代码包含:
- React 函数组件
- Tailwind CSS 样式
- 标题和关闭按钮
- 内容区域
```

---

### 示例 2: 查找和使用 Logo

**用户需求**:
```
"查找 React 和 TypeScript 的 Logo，生成一个技术栈展示卡片"
```

**执行步骤**:

```typescript
// Step 1: 搜索 React Logo
const reactLogos = await airis-exec({
  tool: "magic:search_logos",
  arguments: {
    query: "React",
    limit: 3
  }
});

// Step 2: 搜索 TypeScript Logo
const tsLogos = await airis-exec({
  tool: "magic:search_logos",
  arguments: {
    query: "TypeScript",
    limit: 3
  }
});

// Step 3: 提取最佳 Logo URL
const reactLogo = reactLogos.logos[0].url;
const tsLogo = tsLogos.logos[0].url;

// Step 4: 生成技术栈展示组件
const techStackCard = await airis-exec({
  tool: "magic:generate_ui",
  arguments: {
    description: `Create a TechStack card component displaying React and TypeScript logos.
    React logo: ${reactLogo}
    TypeScript logo: ${tsLogo}
    Include tech name and description.`,
    absolutePathToCurrentFile: "/home/user/project/src/components/TechStack.tsx",
    framework: "react"
  }
});

console.log(`
✅ 技术栈卡片已生成

包含 Logos:
- React: ${reactLogo}
- TypeScript: ${tsLogo}

组件路径: ${techStackCard.file_path}
`);
```

---

## ⚠️ 常见陷阱和解决方案

### 陷阱 1: 使用相对路径

**错误现象**:
```
Error: Invalid path format
Error: File path must be absolute
```

**原因分析**:
Magic MCP 要求使用绝对路径，不接受相对路径

**解决方案**:
```typescript
// ❌ 错误：相对路径
{
  absolutePathToCurrentFile: "./components/Modal.tsx"
}

{
  absolutePathToCurrentFile: "../src/Modal.tsx"
}

// ✅ 正确：绝对路径
{
  absolutePathToCurrentFile: "/home/user/project/src/components/Modal.tsx"
}

// ✅ 正确：使用 process.cwd() 构建
{
  absolutePathToCurrentFile: `${process.cwd()}/src/components/Modal.tsx`
}
```

**路径转换技巧**:
```typescript
// 从相对路径转换为绝对路径
const relativePath = "./src/components/Modal.tsx";
const absolutePath = `${process.cwd()}/${relativePath.replace('./', '')}`;

// 或使用 Node.js path 模块
const path = require('path');
const absolutePath = path.resolve(process.cwd(), "src/components/Modal.tsx");
```

---

### 陷阱 2: Logo 查询过于宽泛

**错误现象**:
返回的 Logo 不是想要的品牌

**原因分析**:
搜索关键词不够具体，匹配到同名但不同的品牌

**解决方案**:
```typescript
// ❌ 不推荐：查询过于宽泛
{
  query: "vue"                    // 可能匹配到 "Vue Cinema" 等
}

// ✅ 推荐：使用全名
{
  query: "Vue.js"                 // 明确指定
}

// ✅ 推荐：添加上下文
{
  query: "React JavaScript library"
}
```

---

## 📚 参考文档

### References 文件

本 skill 包含以下参考文档（在 `references/` 目录中）:

- **component-patterns.md** (~50 行) - 常见组件模式
  - 内容: Modal、Card、Button、Form、Table 等常见组件的描述模式
  - 何时阅读: 需要生成特定类型组件时

- **logo-sources.md** (~50 行) - Logo 来源和版权
  - 内容: Clearbit、Brandfetch 等 Logo 来源、版权说明、使用限制
  - 何时阅读: 使用 Logo 前需要了解版权时

---

## 🔗 相关资源

**MCP 服务器文档**:
- [Magic MCP](../../ai_workflow/docs/airis-mcp-gateway/servers/MAGIC.md) - UI 生成详细文档

**AIRIS MCP Gateway**:
- [完整指南](../../ai_workflow/docs/airis-mcp-gateway/README.md)
- [工具索引](../../ai_workflow/docs/airis-mcp-gateway/TOOL_INDEX.md)

**相关 Skills**:
- airis-browser-automation - UI 验证和测试
- airis-web-research - 设计灵感搜索

---

## 📊 性能和限制

**性能考虑**:
- UI 生成: ~3-5 秒/组件
- Logo 搜索: ~1-2 秒/查询
- **总耗时**: 约 5-8 秒/完整流程

**限制条件**:
- 组件复杂度: 建议 < 200 行/组件
- Logo 搜索: 返回 1-10 个结果
- 框架支持: React、HTML（主要）
- 文件路径: 必须使用绝对路径

**最佳实践**:
- 提供清晰具体的组件描述
- 指定样式框架（如 "Use Tailwind CSS"）
- 使用 `process.cwd()` 构建绝对路径
- Logo 查询使用品牌全名
- 生成的代码需要人工审查和调整
- 对于复杂组件，分步生成（先基础结构，再添加功能）

---

**版本**: 1.0.0
**最后更新**: 2025-12-30
**作者**: Hao
