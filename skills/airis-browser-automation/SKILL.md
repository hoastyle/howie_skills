---
name: airis-browser-automation
description: 浏览器自动化助手，使用 Playwright MCP 进行页面导航、元素操作、表单填充和截图。支持 snapshot（获取 DOM 元素用于操作）和 screenshot（生成可视化图片）两种模式。适用于 Web 自动化测试、数据抓取、表单自动填充、UI 验证等场景。
---

# AIRIS Browser Automation Helper

**MCP 服务器**: playwright
**复杂度**: high
**预估行数**: 300

---

## 🎯 触发条件

### 何时使用这个 Skill

**主要场景**:
- **Web 自动化测试**: 自动化测试登录、表单提交、页面跳转等流程
- **数据抓取**: 从动态网页抓取数据（需要 JavaScript 渲染）
- **表单自动填充**: 批量填写表单、自动提交
- **UI 验证**: 验证页面元素、布局、样式
- **流程录制**: 记录用户操作流程并生成截图

**关键词触发**:
- "浏览器自动化"、"打开网页"、"点击按钮"
- "填写表单"、"自动登录"、"提交表单"
- "截图"、"抓取页面"、"测试网站"
- "Playwright"、"browser automation"

**典型用户请求**:
```
"打开 GitHub 登录页面并自动登录"
"访问这个网站，填写注册表单"
"对比两个网页的截图差异"
"测试购物车结账流程"
```

---

## 📋 决策树：snapshot vs screenshot

### 核心概念区别

**Snapshot** (DOM 快照):
- 用途: 获取页面 DOM 结构和元素引用
- 返回: DOM 元素列表 + ref（可用于后续操作）
- 何时用: 需要点击、填写、查找元素时

**Screenshot** (可视化截图):
- 用途: 生成页面的可视化图片
- 返回: 图片数据（PNG/JPEG）
- 何时用: 需要查看页面外观、对比 UI 时

### 决策流程

```
用户需求
    │
    ├─ 需要操作页面元素？（点击、填写、选择）
    │   YES → 使用 snapshot 获取元素 ref
    │
    ├─ 需要查看页面外观？（UI 验证、对比）
    │   YES → 使用 screenshot 生成图片
    │
    └─ 两者都需要？
        → 先 snapshot（操作） → 再 screenshot（验证）
```

---

## 📋 工作流程

### 四阶段浏览器自动化流程

#### Phase 1: 导航和等待

**功能**: 打开网页并等待加载完成

**执行导航**:
```typescript
// Step 1: 导航到目标 URL
const navigation = await airis-exec({
  tool: "playwright:browser_navigate",
  arguments: {
    url: "https://github.com/login",
    wait_until: "networkidle"     // load | domcontentloaded | networkidle
  }
});
```

**参数说明**:
- `url` (必需) - 目标网页 URL
- `wait_until` - 等待条件
  - `load`: 等待 load 事件（基本加载完成）
  - `domcontentloaded`: 等待 DOM 加载完成（较快）
  - `networkidle`: 等待网络空闲（推荐，确保 AJAX 完成）

**返回结果**:
```json
{
  "url": "https://github.com/login",
  "title": "Sign in to GitHub",
  "status": "success"
}
```

---

#### Phase 2: 获取页面状态（snapshot）

**功能**: 获取 DOM 元素用于后续操作

**执行 snapshot**:
```typescript
// Step 2: 获取页面 snapshot
const snapshot = await airis-exec({
  tool: "playwright:browser_snapshot",
  arguments: {
    selector: "body",              // 可选：限制范围
    include_text: true,            // 包含文本内容
    include_attributes: true       // 包含元素属性
  }
});
```

**参数说明**:
- `selector` - CSS 选择器（可选，默认整个页面）
- `include_text` - 是否包含文本内容
- `include_attributes` - 是否包含元素属性

**返回结果**:
```json
{
  "elements": [
    {
      "ref": "elem_123",
      "tag": "input",
      "type": "text",
      "name": "login",
      "placeholder": "Username or email",
      "text": ""
    },
    {
      "ref": "elem_124",
      "tag": "input",
      "type": "password",
      "name": "password",
      "placeholder": "Password"
    },
    {
      "ref": "elem_125",
      "tag": "button",
      "type": "submit",
      "text": "Sign in"
    }
  ]
}
```

**关键**: `ref` 字段用于后续的点击和填充操作

---

#### Phase 3: 元素操作

**操作 A: 点击元素**

```typescript
// Step 3a: 点击按钮
const clickResult = await airis-exec({
  tool: "playwright:browser_click",
  arguments: {
    ref: "elem_125",              // 使用 snapshot 返回的 ref
    // 或使用选择器
    selector: "button[type='submit']",
    wait_after: 1000              // 点击后等待 1 秒
  }
});
```

**操作 B: 填充表单**

```typescript
// Step 3b: 填写输入框
const fillResult = await airis-exec({
  tool: "playwright:browser_fill",
  arguments: {
    ref: "elem_123",              // 使用 snapshot 返回的 ref
    // 或使用选择器
    selector: "input[name='login']",
    value: "my-username",
    clear_first: true             // 先清空现有内容
  }
});
```

**参数说明**:
- `ref` 或 `selector` - 元素引用（二选一）
- `value` - 要填充的值
- `clear_first` - 是否先清空（默认 true）
- `wait_after` - 操作后等待时间（毫秒）

---

#### Phase 4: 截图保存（screenshot）

**功能**: 生成页面可视化图片

**执行截图**:
```typescript
// Step 4: 截图
const screenshot = await airis-exec({
  tool: "playwright:browser_screenshot",
  arguments: {
    full_page: false,             // false: 视口，true: 整页
    format: "png",                // png | jpeg
    quality: 90,                  // JPEG 质量 (1-100)
    selector: null                // 可选：截取特定元素
  }
});
```

**参数说明**:
- `full_page` - 是否截取完整页面（包括滚动区域）
- `format` - 图片格式（PNG 无损，JPEG 有损但小）
- `quality` - JPEG 质量（仅 JPEG 格式）
- `selector` - 截取特定元素（可选）

**返回结果**:
```json
{
  "image": "base64-encoded-image-data...",
  "format": "png",
  "width": 1920,
  "height": 1080
}
```

---

## 💻 完整示例

### 示例 1: 自动登录流程

**用户需求**:
```
"自动登录 GitHub，填写用户名密码并提交"
```

**执行步骤**:

```typescript
// Step 1: 导航到登录页
await airis-exec({
  tool: "playwright:browser_navigate",
  arguments: {
    url: "https://github.com/login",
    wait_until: "networkidle"
  }
});

// Step 2: 获取页面元素
const page = await airis-exec({
  tool: "playwright:browser_snapshot",
  arguments: {
    include_text: true,
    include_attributes: true
  }
});

// 找到用户名、密码输入框和提交按钮的 ref
const usernameRef = page.elements.find(e =>
  e.name === "login" && e.type === "text"
).ref;

const passwordRef = page.elements.find(e =>
  e.name === "password" && e.type === "password"
).ref;

const submitRef = page.elements.find(e =>
  e.tag === "button" && e.type === "submit"
).ref;

// Step 3: 填写表单
await airis-exec({
  tool: "playwright:browser_fill",
  arguments: {
    ref: usernameRef,
    value: "my-username"
  }
});

await airis-exec({
  tool: "playwright:browser_fill",
  arguments: {
    ref: passwordRef,
    value: "my-password"
  }
});

// Step 4: 提交表单
await airis-exec({
  tool: "playwright:browser_click",
  arguments: {
    ref: submitRef,
    wait_after: 2000
  }
});

// Step 5: 截图验证
const screenshot = await airis-exec({
  tool: "playwright:browser_screenshot",
  arguments: {
    full_page: false,
    format: "png"
  }
});

console.log("✅ 登录完成，已截图保存");
```

---

### 示例 2: 数据抓取和对比

**用户需求**:
```
"访问产品页面，获取价格信息并截图"
```

**执行步骤**:

```typescript
// Step 1: 访问页面
await airis-exec({
  tool: "playwright:browser_navigate",
  arguments: {
    url: "https://example.com/product/123",
    wait_until: "networkidle"
  }
});

// Step 2: 获取页面内容
const snapshot = await airis-exec({
  tool: "playwright:browser_snapshot",
  arguments: {
    selector: ".product-info",   // 只获取产品信息区域
    include_text: true
  }
});

// 提取价格信息
const priceElement = snapshot.elements.find(e =>
  e.class?.includes("price")
);

const productPrice = priceElement.text;
console.log(`产品价格: ${productPrice}`);

// Step 3: 截图保存
const screenshot = await airis-exec({
  tool: "playwright:browser_screenshot",
  arguments: {
    selector: ".product-info",   // 只截取产品信息
    format: "png"
  }
});

// Step 4: 保存到 Serena 记忆
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "product-123-price-check.md",
    content: `# Product Price Check

**Product ID**: 123
**Price**: ${productPrice}
**Screenshot**: Saved
**Date**: ${new Date().toISOString().split('T')[0]}
`
  }
});
```

---

## ⚠️ 常见陷阱和解决方案

### 陷阱 1: 混淆 snapshot 和 screenshot

**错误现象**:
试图用 screenshot 获取元素进行操作，或用 snapshot 查看页面外观

**原因分析**:
两者用途不同，不能混用

**解决方案**:
```typescript
// ❌ 错误：使用 screenshot 获取元素（不返回 ref）
const img = await browser_screenshot();
// 无法获取元素 ref 进行操作

// ✅ 正确：使用 snapshot 获取元素
const page = await browser_snapshot();
const buttonRef = page.elements.find(e => e.tag === "button").ref;

// ✅ 正确：操作完成后使用 screenshot 验证
await browser_click({ ref: buttonRef });
const verification = await browser_screenshot();
```

---

### 陷阱 2: 未等待页面加载

**错误现象**:
```
Error: Element not found
Error: Page not loaded
```

**原因分析**:
页面还在加载时就尝试获取元素或操作

**解决方案**:
```typescript
// ❌ 错误：使用 load（可能 AJAX 未完成）
await browser_navigate({
  url: "https://example.com",
  wait_until: "load"
});

// ✅ 正确：使用 networkidle（等待 AJAX）
await browser_navigate({
  url: "https://example.com",
  wait_until: "networkidle"
});

// ✅ 正确：操作后添加等待
await browser_click({
  ref: "elem_123",
  wait_after: 1000              // 点击后等待 1 秒
});
```

---

### 陷阱 3: 浏览器未安装

**错误现象**:
```
Error: Chromium browser not found
```

**原因分析**:
Playwright 需要先安装浏览器

**解决方案**:
```bash
# 安装 Playwright 浏览器
npx playwright install chromium

# 或安装所有浏览器
npx playwright install

# 验证安装
npx playwright --version
```

**检查方法**:
```typescript
// 在执行自动化前，先检查浏览器是否可用
// Playwright MCP 会在首次使用时自动提示安装
```

---

## 🔌 AIRIS MCP Gateway 标准访问模式（完整版）

本章节展示完整的 AIRIS MCP Gateway 访问模式，确保工具使用的标准化和可靠性。

### 四步标准化工作流

#### Step 1: 工具发现 (airis-find)

使用 `airis-find` 发现本 skill 使用的 MCP 工具：

```typescript
// 发现 Playwright 浏览器自动化工具
const playwrightTools = await airis-find({
  query: "playwright"
});
console.log("Playwright 工具:", playwrightTools.map(t => t.name));
// 输出: ["playwright:browser_navigate", "playwright:browser_snapshot",
//        "playwright:browser_screenshot", "playwright:browser_click",
//        "playwright:browser_fill", ...]
```

**为什么需要这一步？**
- 发现新工具和功能
- 确认工具名称拼写
- 了解 Playwright MCP 提供的所有能力
- 验证 Playwright MCP 服务器已正确安装

---

#### Step 2: 参数验证 (airis-schema)

在执行前，使用 `airis-schema` 检查工具的参数要求：

```typescript
// 检查导航参数
const navigateSchema = await airis-schema({
  tool: "playwright:browser_navigate"
});
console.log("必需参数:", navigateSchema.inputSchema.required);
// 输出: ["url"]
console.log("可选参数:", Object.keys(navigateSchema.inputSchema.properties));
// 输出: ["url", "wait_until"]

// 检查截图参数
const screenshotSchema = await airis-schema({
  tool: "playwright:browser_screenshot"
});
console.log("Screenshot 参数:", screenshotSchema.inputSchema.properties);
// 输出: {full_page, format, quality, selector}
```

**常见参数命名陷阱**（本 skill 涉及）:
- ⚠️ `wait_until` 值必须是 `load` | `domcontentloaded` | `networkidle`（严格匹配）
- ⚠️ `ref` vs `selector` - 只能二选一，不能同时使用
- ⚠️ `format` 必须是 `png` | `jpeg`（小写）

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

// 验证 Playwright 服务器已启动
const playwrightServer = servers.find(s => s.name === "playwright");

if (!playwrightServer) {
  throw new Error("Playwright 服务器未安装");
}

if (playwrightServer.mode === "COLD" && !playwrightServer.ready) {
  console.log("⏳ 等待 Playwright 启动（COLD 模式，浏览器初始化需要 3-8 秒）...");
  await sleep(5000);
}

console.log("✅ Playwright MCP 服务器已就绪");
```

**什么时候需要健康检查？**
- ✅ 长时间运行的自动化测试套件
- ✅ 生产环境部署
- ✅ 首次使用 Playwright（浏览器可能未安装）
- ⚠️ 快速原型开发时可以跳过（但要处理错误）

---

### 完整示例：端到端标准化工作流

```typescript
async function standardizedBrowserAutomation(url: string, taskDescription: string) {
  // Step 1: 健康检查
  const health = await airis-exec({
    tool: "gateway-control:health"
  });

  if (!health.ok) {
    throw new Error("Gateway 不可用");
  }

  // Step 2: 发现工具
  const tools = await airis-find({ query: "playwright navigate" });
  const navigateTool = tools.find(t => t.name === "playwright:browser_navigate");

  if (!navigateTool) {
    throw new Error("Playwright 导航工具未找到");
  }

  // Step 3: 验证参数
  const schema = await airis-schema({ tool: navigateTool.name });
  console.log("工具参数:", schema.inputSchema);

  // Step 4: 执行导航
  await airis-exec({
    tool: "playwright:browser_navigate",
    arguments: {
      url: url,
      wait_until: "networkidle"
    }
  });

  // Step 5: 获取页面状态
  const snapshot = await airis-exec({
    tool: "playwright:browser_snapshot",
    arguments: {
      include_text: true,
      include_attributes: true
    }
  });

  // Step 6: 截图保存
  const screenshot = await airis-exec({
    tool: "playwright:browser_screenshot",
    arguments: {
      full_page: true,
      format: "png"
    }
  });

  return { snapshot, screenshot };
}
```

---

## ⚙️ 服务运行模式

### MCP 服务器特性

本 skill 使用 **Playwright MCP 服务器**（COLD 模式）：

| 服务器 | 工具数 | 运行模式 | 启动延迟 | 首次调用建议 |
|--------|--------|---------|---------|-------------|
| **playwright** | 8+ | COLD ❄️ | 3-8 秒 | 浏览器安装检查 + 健康检查 |

### COLD 模式说明

**COLD 模式服务器特点**:
- ❄️ 按需启动，首次调用需要 3-8 秒启动时间
  - Playwright 启动包括：进程启动 + 浏览器初始化 + 上下文创建
- 💤 长时间不用会自动休眠
- 🔄 重新启动需要等待
- 🌐 浏览器类型影响启动时间（Chromium < Firefox < WebKit）
- 📊 适合批量操作（复用已启动的浏览器实例）

**vs HOT 模式**（不适用于 Playwright）:
- 🔥 常驻内存，即时响应
- ⚡ 无启动延迟
- 🎯 适合高频率调用

### 性能优化建议

#### 对于 COLD 模式服务器（Playwright）:

1. **首次调用前执行健康检查**
   ```typescript
   const health = await airis-exec({ tool: "gateway-control:health" });
   ```

2. **预期并处理浏览器启动延迟**
   ```typescript
   // 首次调用可能需要等待浏览器启动
   try {
     const result = await airis-exec({
       tool: "playwright:browser_navigate",
       arguments: { url: "..." }
     });
   } catch (error) {
     if (error.message.includes("browser not ready") || error.message.includes("server not ready")) {
       console.log("浏览器正在启动，等待 5 秒后重试...");
       await sleep(5000);
       // 重试
       const result = await airis-exec({
         tool: "playwright:browser_navigate",
         arguments: { url: "..." }
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

4. **批量操作时复用已启动的浏览器**
   ```typescript
   // ✅ 高效：复用已启动的 Playwright 浏览器
   const urls = [
     "https://example.com/page1",
     "https://example.com/page2",
     "https://example.com/page3"
   ];

   for (const url of urls) {
     await airis-exec({
       tool: "playwright:browser_navigate",
       arguments: { url, wait_until: "networkidle" }
     });

     const screenshot = await airis-exec({
       tool: "playwright:browser_screenshot",
       arguments: { full_page: true, format: "png" }
     });
     // 后续调用无需浏览器启动延迟
   }

   // ❌ 低效：每次都可能触发浏览器启动
   // （如果在调用之间等待时间过长，浏览器可能关闭）
   ```

5. **检查浏览器是否已安装**
   ```typescript
   // Playwright 首次使用时，浏览器可能未安装
   // MCP 会自动提示安装命令，但最好提前检查
   try {
     await airis-exec({
       tool: "playwright:browser_navigate",
       arguments: { url: "https://example.com" }
     });
   } catch (error) {
     if (error.message.includes("browser not found") || error.message.includes("chromium")) {
       console.error(`
         ❌ Playwright 浏览器未安装。请运行以下命令：

         npx playwright install chromium

         或安装所有浏览器：
         npx playwright install
       `);
       throw new Error("Playwright 浏览器未安装");
     }
   }
   ```

### 服务可用性检查

```typescript
async function ensurePlaywrightAvailable() {
  const servers = await airis-exec({
    tool: "gateway-control:list-servers"
  });

  const playwright = servers.find(s => s.name === "playwright");

  if (!playwright) {
    throw new Error("Playwright 服务器不存在或未安装");
  }

  if (playwright.mode === "COLD" && !playwright.ready) {
    console.log("⏳ 等待 Playwright 启动（COLD 模式，浏览器初始化中）...");
    await sleep(5000);

    // 验证服务器是否已就绪
    const updatedServers = await airis-exec({
      tool: "gateway-control:list-servers"
    });
    const updatedPlaywright = updatedServers.find(s => s.name === "playwright");

    if (!updatedPlaywright.ready) {
      throw new Error("Playwright 启动失败，请检查浏览器是否已安装");
    }
  }

  return playwright;
}

// 使用示例
await ensurePlaywrightAvailable();
```

---

## 🔄 统一错误处理

### 错误分类体系

本 skill 的错误可分为 4 大类：

#### 1. 参数错误 → 使用 airis-schema 预验证

**典型错误**:
```
Error: Invalid parameter 'wait_for' (should be 'wait_until')
Error: Unknown value 'idle' for wait_until (should be 'networkidle')
Error: Both 'ref' and 'selector' provided (choose one)
```

**处理策略**:
```typescript
// ✅ 推荐：执行前验证
const schema = await airis-schema({ tool: "playwright:browser_navigate" });
const requiredParams = schema.inputSchema.required;

// 检查必需参数
if (!arguments.url) {
  throw new Error("缺少必需参数: url");
}

// 检查 wait_until 值是否合法
const validWaitUntil = ["load", "domcontentloaded", "networkidle"];
if (arguments.wait_until && !validWaitUntil.includes(arguments.wait_until)) {
  throw new Error(`wait_until 必须是 ${validWaitUntil.join(" | ")} 之一`);
}

// 执行工具
await airis-exec({
  tool: "playwright:browser_navigate",
  arguments: {
    url: "https://example.com",
    wait_until: "load"
  }
});
```

**预防措施**:
- 总是使用 `airis-schema` 查询正确的参数名
- 参考本文档的"常见陷阱"章节
- 使用 TypeScript 类型定义（如果可用）

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

#### 3. 浏览器错误 → 具体错误具体处理

**典型错误**:
```
Error: Playwright browser not found
Error: Element not found
Error: Element is stale
Error: Navigation timeout
```

**处理策略**:

**浏览器未安装**:
```typescript
try {
  await airis-exec({
    tool: "playwright:browser_navigate",
    arguments: { url: "https://example.com" }
  });
} catch (error) {
  if (error.message.includes("browser not found") || error.message.includes("chromium")) {
    console.error(`
      ❌ Playwright 浏览器未安装。请运行：

      npx playwright install chromium

      或安装所有浏览器：
      npx playwright install
    `);
    throw new Error("Playwright 浏览器未安装");
  }
  throw error;
}
```

**元素未找到**:
```typescript
try {
  const page = await airis-exec({
    tool: "playwright:browser_snapshot",
    arguments: { include_text: true }
  });

  const targetElement = page.elements.find(e => e.name === "login");

  if (!targetElement) {
    throw new Error("登录表单元素未找到");
  }
} catch (error) {
  if (error.message.includes("not found")) {
    console.log("元素未找到，可能页面未完全加载，重新获取 snapshot...");
    await sleep(2000);
    // 重试
    const page = await airis-exec({
      tool: "playwright:browser_snapshot",
      arguments: { include_text: true }
    });
  }
  throw error;
}
```

**元素陈旧（Element is stale）**:
```typescript
// 问题：snapshot 获取的 ref 在页面变化后失效
try {
  await airis-exec({
    tool: "playwright:browser_click",
    arguments: { ref: "elem_123" }
  });
} catch (error) {
  if (error.message.includes("stale") || error.message.includes("detached")) {
    console.log("元素已失效，重新获取 snapshot...");
    // 重新获取 snapshot
    const newPage = await airis-exec({
      tool: "playwright:browser_snapshot",
      arguments: { include_text: true }
    });

    const newRef = newPage.elements.find(e => /* 重新定位元素 */).ref;

    // 使用新的 ref 重试
    await airis-exec({
      tool: "playwright:browser_click",
      arguments: { ref: newRef }
    });
  }
  throw error;
}
```

**导航超时**:
```typescript
try {
  await airis-exec({
    tool: "playwright:browser_navigate",
    arguments: {
      url: "https://slow-site.com",
      wait_until: "networkidle"
    }
  });
} catch (error) {
  if (error.message.includes("timeout") || error.message.includes("navigation")) {
    console.log("导航超时，使用 load 等待条件重试...");
    // 使用更宽松的等待条件
    await airis-exec({
      tool: "playwright:browser_navigate",
      arguments: {
        url: "https://slow-site.com",
        wait_until: "load"  // 更快但可能未完全加载
      }
    });
  }
  throw error;
}
```

---

#### 4. 服务不可用 → 重试或回退

**典型错误**:
```
Error: Playwright server not ready
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
          throw new Error(`Playwright 服务器启动失败（已重试 ${maxRetries} 次）`);
        }

        const waitTime = (i + 1) * 3000;  // 递增等待时间
        console.log(`Playwright 正在启动，等待 ${waitTime/1000} 秒后重试...`);
        await sleep(waitTime);
        continue;
      }

      throw error;
    }
  }
}

// 使用示例
const result = await executeWithServerRetry(
  "playwright:browser_navigate",
  { url: "https://example.com", wait_until: "networkidle" }
);
```

**回退方案**:
```typescript
try {
  // 尝试使用 Playwright
  const screenshot = await airis-exec({
    tool: "playwright:browser_screenshot",
    arguments: { full_page: true }
  });
} catch (error) {
  if (error.message.includes("not available") || error.message.includes("not installed")) {
    console.warn("⚠️ Playwright 不可用，回退到 Fetch 方案...");

    // 回退：使用 Fetch 获取 HTML（无法截图，但可以获取内容）
    const htmlContent = await airis-exec({
      tool: "fetch:fetch",
      arguments: { url: "https://example.com" }
    });

    console.log("✅ 已获取 HTML 内容（无截图）");
    return { html: htmlContent, screenshot: null };
  }

  throw error;
}
```

---

### 完整错误处理示例（端到端）

```typescript
async function robustBrowserAutomation(url: string) {
  // Step 1: Gateway 健康检查（错误类型 2）
  try {
    const health = await airis-exec({ tool: "gateway-control:health" });
    if (!health.ok) {
      throw new Error("Gateway 不健康");
    }
  } catch (error) {
    throw new Error(`Gateway 不可用: ${error.message}`);
  }

  // Step 2: 确保 Playwright 可用（错误类型 4）
  await ensurePlaywrightAvailable();

  // Step 3: 参数验证（错误类型 1）
  const schema = await airis-schema({ tool: "playwright:browser_navigate" });
  if (!url || typeof url !== "string") {
    throw new Error("url 参数必须是非空字符串");
  }

  // Step 4: 导航（错误类型 3 - 超时）
  try {
    await airis-exec({
      tool: "playwright:browser_navigate",
      arguments: { url, wait_until: "networkidle" }
    });
  } catch (error) {
    if (error.message.includes("timeout")) {
      console.warn("导航超时，使用 load 等待条件重试...");
      await airis-exec({
        tool: "playwright:browser_navigate",
        arguments: { url, wait_until: "load" }
      });
    } else {
      throw error;
    }
  }

  // Step 5: 获取 snapshot（错误类型 3 - 元素未找到）
  let snapshot;
  try {
    snapshot = await airis-exec({
      tool: "playwright:browser_snapshot",
      arguments: { include_text: true, include_attributes: true }
    });
  } catch (error) {
    console.warn("Snapshot 失败，等待 2 秒后重试...");
    await sleep(2000);
    snapshot = await airis-exec({
      tool: "playwright:browser_snapshot",
      arguments: { include_text: true, include_attributes: true }
    });
  }

  // Step 6: 截图（错误类型 3 - 浏览器未安装）
  let screenshot;
  try {
    screenshot = await airis-exec({
      tool: "playwright:browser_screenshot",
      arguments: { full_page: true, format: "png" }
    });
  } catch (error) {
    if (error.message.includes("browser not found")) {
      throw new Error("Playwright 浏览器未安装，请运行: npx playwright install chromium");
    }
    throw error;
  }

  return { snapshot, screenshot };
}
```

---

## 📚 参考文档

### References 文件

本 skill 包含以下参考文档（在 `references/` 目录中）:

- **playwright-selectors.md** (~80 行) - 选择器类型和最佳实践
  - 内容: text=、role=、CSS、XPath 选择器类型，选择器优先级，常见模式
  - 何时阅读: 需要精确定位元素时

- **automation-patterns.md** (~70 行) - 常见自动化模式
  - 内容: 登录流程、表单填充、分页导航、文件上传、弹窗处理
  - 何时阅读: 需要实现复杂自动化流程时

---

## 🔗 相关资源

**MCP 服务器文档**:
- [Playwright MCP](../../ai_workflow/docs/airis-mcp-gateway/servers/PLAYWRIGHT.md) - 浏览器自动化详细文档

**AIRIS MCP Gateway**:
- [完整指南](../../ai_workflow/docs/airis-mcp-gateway/README.md)
- [工具索引](../../ai_workflow/docs/airis-mcp-gateway/TOOL_INDEX.md)

**相关 Skills**:
- airis-web-research - Web 研究和内容抓取
- airis-code-search - 代码搜索（可用于测试脚本）

---

## 📊 性能和限制

**性能考虑**:
- 导航: ~2-5 秒/页面（取决于网络和页面复杂度）
- Snapshot: ~0.5-1 秒
- Click/Fill: ~0.2-0.5 秒/操作
- Screenshot: ~1-2 秒
- **总耗时**: 约 5-15 秒/完整流程

**限制条件**:
- 浏览器内存: 建议 < 1GB/页面
- 并发页面: 建议 < 5 个同时打开
- Screenshot 大小: 建议 < 5MB/图片
- 页面复杂度: 建议 < 1000 DOM 元素用于 snapshot

**最佳实践**:
- 优先使用 `networkidle` 等待完全加载
- 使用 `ref` 而非 `selector` 提高稳定性（snapshot 后获取 ref）
- 操作后添加 `wait_after` 等待动画完成
- 截图前滚动到目标位置
- 使用 `selector` 限制 snapshot 范围（提高性能）
- 定期清理浏览器缓存和 cookies
- 对于长时间自动化，考虑分批执行避免内存泄漏

---

**版本**: 1.0.0
**最后更新**: 2025-12-30
**作者**: Hao
