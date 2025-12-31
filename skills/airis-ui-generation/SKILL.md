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
// ❌ 错误：使用相对路径且缺少必需参数
await magic:generate_ui({
  description: "Create a modal component",
  path_to_current_file: "./components/Modal.tsx"  // 错误！
});

// ✅ 正确：使用绝对路径和所有必需参数
await magic:generate_ui({
  absolutePathToCurrentFile: "/home/user/project/components/Modal.tsx",
  content: "import React from 'react';\n\nexport const Modal = () => {\n  return <div></div>;\n};",
  prompt: "Create a modal component"
});
```

**参数说明**:
- `absolutePathToCurrentFile` (必需) - **绝对路径**到目标文件
- `content` (必需) - 当前文件内容
- `prompt` (必需) - UI 生成提示（自然语言描述）
- `framework` (可选) - 框架类型（react | html，默认 react）

**生成示例**:
```typescript
const uiComponent = await airis-exec({
  tool: "magic:generate_ui",
  arguments: {
    absolutePathToCurrentFile: "/home/user/project/src/components/Modal.tsx",
    content: "import React from 'react';\n\nexport const Modal = () => {\n  return <div></div>;\n};",
    prompt: "Create a modal dialog with close button and title",
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
    absolutePathToCurrentFile: targetFile,
    content: "import React from 'react';\n\nexport const Modal = () => {\n  return <div></div>;\n};",
    prompt: "Create a Modal dialog component with title, close button, and content area. Use Tailwind CSS for styling.",
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
    absolutePathToCurrentFile: "/home/user/project/src/components/TechStack.tsx",
    content: "import React from 'react';\n\nexport const TechStack = () => {\n  return <div></div>;\n};",
    prompt: `Create a TechStack card component displaying React and TypeScript logos.
    React logo: ${reactLogo}
    TypeScript logo: ${tsLogo}
    Include tech name and description.`,
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

## 🔌 AIRIS MCP Gateway 标准访问模式（完整版）

本章节展示完整的 AIRIS MCP Gateway 访问模式，确保工具使用的标准化和可靠性。

### 四步标准化工作流

#### Step 1: 工具发现 (airis-find)

使用 `airis-find` 发现 Magic 提供的工具：

```typescript
// 发现 Magic 工具
const magicTools = await airis-find({
  query: "magic"
});
console.log("Magic 工具:", magicTools.map(t => t.name));
// 输出: ["magic:generate_ui", "magic:search_logos"]
```

**为什么需要这一步？**
- 发现 Magic 的可用工具
- 确认工具名称拼写正确
- 验证 Magic MCP 服务器已正确安装

---

#### Step 2: 参数验证 (airis-schema)

在执行前，使用 `airis-schema` 检查工具的参数要求：

```typescript
// 检查 generate_ui 参数
const generateSchema = await airis-schema({
  tool: "magic:generate_ui"
});
console.log("必需参数:", generateSchema.inputSchema.required);
// 输出: ["absolutePathToCurrentFile", "content", "prompt"]
console.log("可选参数:", Object.keys(generateSchema.inputSchema.properties));
// 输出: ["absolutePathToCurrentFile", "content", "prompt", "framework"]

// 检查 search_logos 参数
const searchSchema = await airis-schema({
  tool: "magic:search_logos"
});
console.log("Logo 搜索参数:", searchSchema.inputSchema.required);
// 输出: ["query"]
```

**常见参数命名陷阱**（本 skill 涉及）:
- ⚠️ 参数名是 `absolutePathToCurrentFile`（不是 `path` 或 `file_path`）
- ⚠️ 必须使用绝对路径（不能使用相对路径如 `./` 或 `../`）
- ⚠️ `framework` 默认是 `react`（可选值：react | html）

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

// 验证 Magic 已安装
const magic = servers.find(s => s.name === "magic");

if (!magic) {
  throw new Error("Magic 服务器未安装");
}

if (magic.mode === "COLD" && !magic.ready) {
  console.log("⏳ 等待 Magic 启动（COLD 模式，需要 2-5 秒）...");
  await sleep(3000);
}

console.log("✅ Magic 已就绪");
```

**什么时候需要健康检查？**
- ✅ 首次使用 Magic（COLD 模式需要启动时间）
- ✅ 生产环境部署
- ✅ 批量生成多个组件
- ⚠️ 单次快速生成时可以跳过（但要处理错误）

---

### 完整示例：端到端标准化工作流

```typescript
async function standardizedUIGeneration(description: string, targetPath: string) {
  // Step 1: 健康检查
  const health = await airis-exec({
    tool: "gateway-control:health"
  });

  if (!health.ok) {
    throw new Error("Gateway 不可用");
  }

  // Step 2: 发现工具
  const tools = await airis-find({ query: "magic" });
  console.log(`发现 ${tools.length} 个 Magic 工具`);

  // Step 3: 验证参数
  const generateSchema = await airis-schema({
    tool: "magic:generate_ui"
  });
  console.log("生成工具参数:", generateSchema.inputSchema);

  // Step 4: 验证路径是绝对路径
  const path = require('path');
  if (!path.isAbsolute(targetPath)) {
    // 转换为绝对路径
    targetPath = path.resolve(process.cwd(), targetPath);
    console.log(`路径已转换为绝对路径: ${targetPath}`);
  }

  // Step 5: 生成 UI
  const component = await airis-exec({
    tool: "magic:generate_ui",
    arguments: {
      absolutePathToCurrentFile: targetPath,
      content: "import React from 'react';\n\nexport const Component = () => {\n  return <div></div>;\n};",
      prompt: description,
      framework: "react"
    }
  });

  console.log(`✅ UI 组件已生成: ${component.file_path}`);
  return component;
}
```

---

## ⚙️ 服务运行模式

### MCP 服务器特性

本 skill 使用的 Magic 为 **COLD 模式**：

| 服务器 | 工具数 | 运行模式 | 启动延迟 | 首次调用建议 |
|--------|--------|---------|---------|-------------|
| **magic** | 3 | COLD ❄️ | 2-5 秒 | 使用前检查健康状态 |

### COLD 模式说明

**COLD 模式服务器特点**:
- ❄️ 按需启动，首次调用需要 2-5 秒启动时间
- 💤 长时间不用会自动休眠
- 🔄 重新启动需要等待
- 📊 适合批量操作（复用已启动的服务）

**vs HOT 模式**（不适用于本 skill）:
- 🔥 常驻内存，即时响应
- ⚡ 无启动延迟
- 🎯 适合高频率调用

### 性能优化建议

#### 对于 COLD 模式服务器（Magic）:

1. **首次调用前执行健康检查**
   ```typescript
   const health = await airis-exec({ tool: "gateway-control:health" });
   ```

2. **预期并处理启动延迟**
   ```typescript
   // 首次调用可能需要等待
   try {
     const result = await airis-exec({
       tool: "magic:generate_ui",
       arguments: {
         absolutePathToCurrentFile: "/home/user/project/Component.tsx",
         content: "import React from 'react';\n\nexport const Component = () => <div />;",
         prompt: "Create a component"
       }
     });
   } catch (error) {
     if (error.message.includes("server not ready")) {
       console.log("Magic 正在启动，等待 3 秒后重试...");
       await sleep(3000);
       // 重试
       const result = await airis-exec({
         tool: "magic:generate_ui",
         arguments: {
           absolutePathToCurrentFile: "/home/user/project/Component.tsx",
           content: "import React from 'react';\n\nexport const Component = () => <div />;",
           prompt: "Create a component"
         }
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
         await sleep(2000);
       }
     }
   }
   ```

4. **批量生成时复用已启动的服务**
   ```typescript
   // ✅ 高效：批量生成复用 Magic 服务
   const components = [
     { name: "Modal", desc: "Create a modal dialog" },
     { name: "Card", desc: "Create a card component" },
     { name: "Button", desc: "Create a button component" }
   ];

   for (const comp of components) {
     // 首次调用后，Magic 已启动，后续调用无延迟
     const result = await airis-exec({
       tool: "magic:generate_ui",
       arguments: {
         absolutePathToCurrentFile: `/project/src/${comp.name}.tsx`,
         content: `import React from 'react';\n\nexport const ${comp.name} = () => <div />;`,
         prompt: comp.desc
       }
     });
     console.log(`${comp.name} 生成完成`);
   }
   ```

### 服务可用性检查

```typescript
async function ensureMagicAvailable() {
  const servers = await airis-exec({
    tool: "gateway-control:list-servers"
  });

  const magic = servers.find(s => s.name === "magic");

  if (!magic) {
    throw new Error(`
      Magic 服务器未安装

      请安装 Magic：
      1. 检查 AIRIS MCP Gateway 配置
      2. 安装 Magic MCP 服务器
      3. 重启 Gateway
    `);
  }

  if (magic.mode === "COLD" && !magic.ready) {
    console.log(`⏳ 等待 Magic 启动（COLD 模式）...`);
    await sleep(3000);

    // 验证服务器是否已就绪
    const updatedServers = await airis-exec({
      tool: "gateway-control:list-servers"
    });
    const updatedMagic = updatedServers.find(s => s.name === "magic");

    if (!updatedMagic.ready) {
      throw new Error(`Magic 启动失败`);
    }
  }

  console.log(`✅ Magic 已就绪（3 个工具可用）`);
  return magic;
}

// 使用示例
await ensureMagicAvailable();
```

---

## 🔄 统一错误处理

### 错误分类体系

本 skill 的错误可分为 4 大类：

#### 1. 参数错误 → 使用 airis-schema 预验证

**典型错误**:
```
Error: Invalid path format - must be absolute
Error: Required parameter 'absolutePathToCurrentFile' is missing
Error: Parameter name should be 'absolutePathToCurrentFile' not 'path'
```

**处理策略**:
```typescript
// ✅ 推荐：执行前验证
const generateSchema = await airis-schema({
  tool: "magic:generate_ui"
});
const requiredParams = generateSchema.inputSchema.required;

// 检查必需参数
if (!arguments.absolutePathToCurrentFile) {
  throw new Error("缺少必需参数: absolutePathToCurrentFile");
}

if (!arguments.content) {
  throw new Error("缺少必需参数: content");
}

if (!arguments.prompt) {
  throw new Error("缺少必需参数: prompt");
}

// 检查路径是否为绝对路径
const path = require('path');
if (!path.isAbsolute(arguments.absolutePathToCurrentFile)) {
  throw new Error(`路径必须是绝对路径，当前: ${arguments.absolutePathToCurrentFile}`);
}

// 执行工具
await airis-exec({
  tool: "magic:generate_ui",
  arguments: arguments  // 验证后的参数
});
```

**预防措施**:
- 总是使用 `airis-schema` 查询正确的参数名
- 使用 `path.isAbsolute()` 验证路径格式
- 使用 `path.resolve()` 转换相对路径为绝对路径
- 参数名是 `absolutePathToCurrentFile`（不是 `path`）

---

#### 2. Gateway 错误 → 检查健康状态

**典型错误**:
```
Error: Failed to connect to AIRIS MCP Gateway
Error: Magic not found
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

  // 验证 Magic 可用
  const servers = await airis-exec({
    tool: "gateway-control:list-servers"
  });

  if (!servers.some(s => s.name === "magic")) {
    throw new Error("Magic 未安装");
  }

} catch (error) {
  console.error("Gateway 错误:", error.message);

  // 提供用户友好的错误信息
  throw new Error(`
    AIRIS MCP Gateway 不可用。请检查：
    1. Gateway 是否正在运行（http://localhost:9400/health）
    2. Magic 是否已安装
    3. 网络连接是否正常
  `);
}
```

**预防措施**:
- 工作流开始前执行健康检查
- 验证 Magic 在服务器列表中
- 提供清晰的错误提示和修复建议

---

#### 3. 工具执行错误 → 具体错误具体处理

**典型错误**:
```
Error: Component generation failed
Error: Invalid framework specified
Error: Logo not found
```

**处理策略**:

**组件生成失败（Generation failed）**:
```typescript
try {
  const component = await airis-exec({
    tool: "magic:generate_ui",
    arguments: {
      absolutePathToCurrentFile: "/project/Component.tsx",
      content: "import React from 'react';\n\nexport const Component = () => <div />;",
      prompt: "vague description"
    }
  });
} catch (error) {
  if (error.message.includes("generation failed")) {
    console.log("组件生成失败，可能是描述不够具体");

    throw new Error(`
      UI 生成失败。请提供更具体的描述：
      - 明确组件类型（Modal、Card、Button 等）
      - 指定样式框架（"Use Tailwind CSS"）
      - 说明交互行为（"with close button", "on hover effect"）
      - 描述数据结构（props, state）

      示例描述：
      "Create a Modal dialog component with title, close button, and content area.
       Use Tailwind CSS for styling. Include fade-in animation."
    `);
  }
  throw error;
}
```

**框架不支持（Invalid framework）**:
```typescript
try {
  const component = await airis-exec({
    tool: "magic:generate_ui",
    arguments: {
      absolutePathToCurrentFile: "/project/Component.tsx",
      content: "import React from 'react';\n\nexport const Component = () => <div />;",
      prompt: "Create a component",
      framework: "vue" // 不支持
    }
  });
} catch (error) {
  if (error.message.includes("invalid framework")) {
    throw new Error(`
      框架 "vue" 不支持。

      Magic 支持的框架：
      - react (默认)
      - html

      请使用支持的框架，或省略 framework 参数使用默认值（react）
    `);
  }
  throw error;
}
```

**Logo 未找到（Logo not found）**:
```typescript
const logos = await airis-exec({
  tool: "magic:search_logos",
  arguments: {
    query: "unknown-brand"
  }
});

if (!logos.logos || logos.logos.length === 0) {
  console.log("未找到 Logo，尝试更具体的查询...");

  throw new Error(`
    未找到 "${query}" 的 Logo。请尝试：
    1. 使用品牌全名（"Vue.js" 而非 "vue"）
    2. 检查拼写是否正确
    3. 确认品牌确实存在于 Logo 数据库中

    提示：Magic 使用 Clearbit 和 Brandfetch 作为 Logo 来源
  `);
}
```

---

#### 4. 服务不可用 → 重试或回退

**典型错误**:
```
Error: Server 'magic' not found
Error: Server 'magic' not ready
```

**处理策略**:

**服务器未安装**:
```typescript
const servers = await airis-exec({
  tool: "gateway-control:list-servers"
});

const magic = servers.find(s => s.name === "magic");

if (!magic) {
  throw new Error(`
    Magic 服务器未安装

    请按以下步骤安装：
    1. 检查 AIRIS MCP Gateway 配置文件
    2. 添加 Magic 服务器配置
    3. 重启 AIRIS MCP Gateway
    4. 验证安装：airis-gateway list-servers

    配置示例：
    {
      "mcpServers": {
        "magic": {
          "command": "magic-mcp",
          "mode": "COLD"
        }
      }
    }
  `);
}
```

**服务器未就绪（COLD 模式）**:
```typescript
async function waitForMagicReady(maxWaitTime = 10000) {
  const startTime = Date.now();

  while (Date.now() - startTime < maxWaitTime) {
    const servers = await airis-exec({
      tool: "gateway-control:list-servers"
    });

    const magic = servers.find(s => s.name === "magic");

    if (magic && magic.ready) {
      return true;
    }

    console.log(`⏳ 等待 Magic 就绪...`);
    await sleep(2000);
  }

  return false;
}

// 使用示例
const ready = await waitForMagicReady();
if (!ready) {
  throw new Error("Magic 服务器启动超时");
}
```

**回退方案**:
```typescript
// 主方案：使用 Magic 生成 UI
try {
  const component = await airis-exec({
    tool: "magic:generate_ui",
    arguments: {
      absolutePathToCurrentFile: "/project/Modal.tsx",
      content: "import React from 'react';\n\nexport const Modal = () => <div />;",
      prompt: "Create a modal"
    }
  });
} catch (error) {
  console.log("Magic 不可用，提供手动创建指导...");

  // 回退方案：提供手动创建模板
  const manualTemplate = `
import React from 'react';

export function Modal({ title, onClose, children }) {
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>{title}</h2>
          <button onClick={onClose}>×</button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
}
  `;

  console.log("建议使用以下模板手动创建 Modal 组件：");
  console.log(manualTemplate);

  return { code: manualTemplate, manual: true };
}
```

---

### 完整错误处理示例

```typescript
async function robustUIGeneration(description: string, targetPath: string) {
  try {
    // 1. 健康检查
    const health = await airis-exec({
      tool: "gateway-control:health"
    });

    if (!health.ok) {
      throw new Error("GATEWAY_UNHEALTHY");
    }

    // 2. 验证 Magic 可用性
    await ensureMagicAvailable();

    // 3. 路径验证和转换
    const path = require('path');
    let absolutePath = targetPath;

    if (!path.isAbsolute(targetPath)) {
      // 转换为绝对路径
      absolutePath = path.resolve(process.cwd(), targetPath);
      console.log(`路径已转换为绝对路径: ${absolutePath}`);
    }

    // 4. 生成 UI（带错误处理）
    let component;
    try {
      component = await execWithRetry(
        "magic:generate_ui",
        {
          absolutePathToCurrentFile: absolutePath,
          content: "import React from 'react';\n\nexport const Component = () => <div />;",
          prompt: description,
          framework: "react"
        },
        3
      );
    } catch (error) {
      if (error.message.includes("generation failed")) {
        throw new Error(`UI 生成失败，请提供更具体的描述`);
      }
      throw error;
    }

    console.log(`✅ UI 组件已生成: ${component.file_path}`);
    return component;

  } catch (error) {
    // 统一错误处理
    console.error("UI 生成失败:", error);

    if (error.message === "GATEWAY_UNHEALTHY") {
      throw new Error("AIRIS MCP Gateway 不可用，请检查服务状态");
    } else if (error.message.includes("not found")) {
      throw new Error("Magic 未安装，请先安装该服务器");
    } else if (error.message.includes("absolute")) {
      throw new Error(`路径必须是绝对路径，当前: ${targetPath}`);
    } else {
      throw new Error(`生成失败: ${error.message}`);
    }
  }
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
