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
