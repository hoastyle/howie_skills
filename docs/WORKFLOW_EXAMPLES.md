# AIRIS Skills 工作流组合示例

**目的**: 展示如何组合使用多个 Skills 完成复杂的开发任务
**受众**: 已掌握单个 Skill 使用，希望提升工作流效率的用户

---

## 📚 目录

1. [场景 1: 技术调研 + 知识沉淀](#场景-1-技术调研--知识沉淀)
2. [场景 2: 代码重构 + 文档更新](#场景-2-代码重构--文档更新)
3. [场景 3: 竞品分析 + UI 原型](#场景-3-竞品分析--ui-原型)
4. [场景 4: 项目初始化全流程](#场景-4-项目初始化全流程)
5. [场景 5: 调试 + 解决方案保存](#场景-5-调试--解决方案保存)
6. [最佳实践](#最佳实践)

---

## 场景 1: 技术调研 + 知识沉淀

### 业务需求

> "我们需要为新项目选择一个状态管理方案，请研究 Zustand、Jotai、Valtio 三个库，并将关键信息保存到项目知识库"

### 涉及 Skills

1. **airis-web-research** - Web 搜索和内容提取
2. **airis-library-docs** - 查询官方文档
3. **airis-knowledge-mgmt** - 知识图谱管理

### 完整工作流

#### Step 1: Web 搜索最新对比 (airis-web-research)

```typescript
// 用户提示
用户: "帮我研究 Zustand vs Jotai vs Valtio 的对比，重点关注性能和开发体验"

// airis-web-research 自动触发
// 执行流程:
// 1. Tavily 搜索: "Zustand Jotai Valtio comparison 2025 performance"
// 2. Fetch 提取前 3 篇文章内容
// 3. Serena 保存到: .serena/memories/state_management_comparison.md

// 输出示例
✅ 研究结果已保存到: .serena/memories/state_management_comparison.md

内容摘要:
- Zustand: 轻量级 (1KB)，Redux-like API，性能优秀
- Jotai: 原子化状态，React 18+ 优化，学习曲线低
- Valtio: Proxy-based，自动追踪依赖，API 最简洁

推荐: Zustand（团队熟悉 Redux）或 Jotai（新项目首选）
```

#### Step 2: 查询官方文档细节 (airis-library-docs)

```typescript
// 继续深入查询
用户: "查询 Zustand 官方文档，看看如何集成 TypeScript 和 DevTools"

// airis-library-docs 自动触发
// 执行流程:
// 1. Context7 搜索: "zustand" 库
// 2. 提取: TypeScript, DevTools 相关章节

// 输出示例
✅ 已查询 Zustand 官方文档

TypeScript 集成:
```typescript
import create from 'zustand'

interface BearState {
  bears: number
  increase: () => void
}

const useBearStore = create<BearState>((set) => ({
  bears: 0,
  increase: () => set((state) => ({ bears: state.bears + 1 })),
}))
```

DevTools:
```typescript
import { devtools } from 'zustand/middleware'
const useStore = create(devtools(store))
```
```

#### Step 3: 创建知识图谱 (airis-knowledge-mgmt)

```typescript
// 将关键决策保存到知识图谱
用户: "将状态管理方案的选择保存到知识库，标记为架构决策"

// airis-knowledge-mgmt 自动触发
// 执行流程:
// 1. Memory MCP 创建实体:
//    - 实体名: "State Management Decision"
//    - 类型: "architectural_decision"
//    - 关系: 关联 "Zustand", "Jotai", "Valtio" 实体
// 2. Serena 保存详细记录

// 输出示例
✅ 已创建知识图谱实体

实体:
- State Management Decision (architectural_decision)
  ├─ 关联: Zustand (library)
  ├─ 关联: Jotai (library)
  └─ 关联: Valtio (library)

决策记录:
- 选择: Zustand
- 理由: 团队熟悉 Redux，学习成本低，性能优秀
- 备选: Jotai (未来新项目可考虑)
```

### 时间估算

| 步骤 | 耗时 | 说明 |
|------|------|------|
| Web 搜索 + 内容提取 | 30-60s | Tavily + Fetch (COLD 启动) |
| 官方文档查询 | 10-20s | Context7 (COLD 启动) |
| 知识图谱创建 | 5-10s | Memory (HOT 模式) |
| **总计** | **~90s** | 首次调用（后续更快） |

### 产出物

1. `.serena/memories/state_management_comparison.md` - 完整研究报告
2. 知识图谱中的架构决策记录
3. 可搜索的技术知识（支持相似度搜索）

---

## 场景 2: 代码重构 + 文档更新

### 业务需求

> "重构用户认证模块，使用新的 JWT 库，并更新相关文档"

### 涉及 Skills

1. **airis-code-search** - 定位需要修改的代码
2. **airis-library-docs** - 查询新库文档
3. **airis-knowledge-mgmt** - 保存重构决策

### 完整工作流

#### Step 1: 定位认证相关代码 (airis-code-search)

```typescript
// 用户提示
用户: "找到所有处理 JWT token 生成和验证的代码"

// airis-code-search 自动触发
// 执行流程:
// 1. MorphLLM 语义搜索: "JWT token generation validation"
// 2. 定位相关文件和函数
// 3. Serena 保存搜索结果

// 输出示例
✅ 找到 JWT 相关代码（5 个位置）:

1. src/auth/jwt.service.ts:23-45
   - generateToken(userId, expiresIn)
   - 使用 jsonwebtoken 库

2. src/auth/jwt.service.ts:47-68
   - verifyToken(token)
   - 验证签名和过期时间

3. src/middleware/auth.middleware.ts:12-28
   - authenticateRequest(req, res, next)
   - 从 header 提取 token

4. src/utils/token.utils.ts:8-15
   - refreshToken(oldToken)
   - 刷新 token 逻辑

5. tests/auth/jwt.test.ts:10-50
   - JWT 测试用例
```

#### Step 2: 查询新库文档 (airis-library-docs)

```typescript
// 查询新库的迁移指南
用户: "查询 jose 库（新的 JWT 库）的使用方法"

// airis-library-docs 自动触发
// 输出示例
✅ jose 库文档摘要

安装:
```bash
npm install jose
```

生成 Token (对比 jsonwebtoken):
```typescript
// 旧方式 (jsonwebtoken)
import jwt from 'jsonwebtoken'
const token = jwt.sign({ userId }, secret, { expiresIn: '1h' })

// 新方式 (jose)
import { SignJWT } from 'jose'
const token = await new SignJWT({ userId })
  .setProtectedHeader({ alg: 'HS256' })
  .setExpirationTime('1h')
  .sign(new TextEncoder().encode(secret))
```

验证 Token:
```typescript
// 旧方式
const payload = jwt.verify(token, secret)

// 新方式
import { jwtVerify } from 'jose'
const { payload } = await jwtVerify(token, new TextEncoder().encode(secret))
```
```

#### Step 3: 保存重构决策 (airis-knowledge-mgmt)

```typescript
// 记录重构决策
用户: "记录 JWT 库迁移决策：从 jsonwebtoken 迁移到 jose"

// airis-knowledge-mgmt 自动触发
// 输出示例
✅ 已创建重构决策记录

实体:
- JWT Library Migration (refactoring_decision)
  ├─ 从: jsonwebtoken (deprecated)
  └─ 到: jose (recommended)

决策理由:
- jose 是 Web Crypto API 标准实现
- 更好的 TypeScript 支持
- 不依赖 Node.js crypto 模块（支持 Edge Runtime）
- 更小的包体积（tree-shakable）

影响文件:
- src/auth/jwt.service.ts
- src/middleware/auth.middleware.ts
- src/utils/token.utils.ts
```

### 后续步骤（手动）

```typescript
// 此时 Claude Code 已准备好所有信息，可以开始重构
// 1. 修改 src/auth/jwt.service.ts（使用 jose 库）
// 2. 更新 src/middleware/auth.middleware.ts（异步验证）
// 3. 更新测试用例（tests/auth/jwt.test.ts）
// 4. 提交代码并创建 PR
```

### 时间估算

| 步骤 | 耗时 | 说明 |
|------|------|------|
| 代码搜索 | 20-40s | MorphLLM (COLD 启动) |
| 文档查询 | 10-20s | Context7 (COLD 启动) |
| 决策记录 | 5-10s | Memory (HOT 模式) |
| **总计** | **~60s** | 信息收集阶段 |

---

## 场景 3: 竞品分析 + UI 原型

### 业务需求

> "分析竞品的定价页面设计，并生成一个类似的 UI 原型"

### 涉及 Skills

1. **airis-browser-automation** - 抓取竞品页面截图
2. **airis-web-research** - 搜索设计最佳实践
3. **airis-ui-generation** - 生成 UI 组件

### 完整工作流

#### Step 1: 抓取竞品页面 (airis-browser-automation)

```typescript
// 用户提示
用户: "打开 Stripe 的定价页面并截图保存"

// airis-browser-automation 自动触发
// 执行流程:
// 1. Playwright 打开 https://stripe.com/pricing
// 2. 等待页面加载完成
// 3. 截图保存到工作目录

// 输出示例
✅ 已截图保存: stripe_pricing_page.png

页面结构分析:
- 三栏定价方案（Starter, Growth, Scale）
- 每栏包含: 价格、功能列表、CTA 按钮
- 使用渐变背景和卡片设计
- 响应式布局
```

#### Step 2: 研究定价页面设计最佳实践 (airis-web-research)

```typescript
// 继续研究设计模式
用户: "研究 SaaS 定价页面的设计最佳实践"

// airis-web-research 自动触发
// 输出示例
✅ 研究完成

关键发现:
1. 推荐方案视觉突出（通常是中间栏）
2. 使用对比表格展示差异
3. 年付/月付切换器
4. 信任元素（客户评价、安全认证）
5. 清晰的 CTA 按钮（对比色）

已保存到: .serena/memories/saas_pricing_design_best_practices.md
```

#### Step 3: 生成 UI 原型 (airis-ui-generation)

```typescript
// 生成实际可用的 React 组件
用户: "基于 Stripe 的设计，生成一个三栏定价组件"

// airis-ui-generation 自动触发
// 执行流程:
// 1. Magic MCP 生成 React + Tailwind CSS 组件
// 2. 保存到项目目录

// 输出示例
✅ 已生成: src/components/PricingTable.tsx

组件特性:
- 响应式三栏布局
- 年付/月付切换
- 推荐方案高亮
- Tailwind CSS 样式
- TypeScript 类型定义

预览:
```tsx
import { PricingTable } from '@/components/PricingTable'

export default function PricingPage() {
  return (
    <div className="container mx-auto py-12">
      <h1 className="text-4xl font-bold text-center mb-8">
        选择适合你的方案
      </h1>
      <PricingTable />
    </div>
  )
}
```
```

### 时间估算

| 步骤 | 耗时 | 说明 |
|------|------|------|
| 页面截图 | 10-20s | Playwright (COLD 启动) |
| 设计研究 | 30-60s | Tavily + Fetch (COLD 启动) |
| UI 组件生成 | 15-30s | Magic (COLD 启动) |
| **总计** | **~90s** | 从分析到原型 |

### 产出物

1. `stripe_pricing_page.png` - 竞品截图
2. `.serena/memories/saas_pricing_design_best_practices.md` - 设计研究报告
3. `src/components/PricingTable.tsx` - 可用的 React 组件

---

## 场景 4: 项目初始化全流程

### 业务需求

> "开始一个新的 Next.js 项目，集成 Supabase，并建立完整的知识库"

### 涉及 Skills

1. **airis-project-indexing** - 分析项目结构
2. **airis-library-docs** - 查询框架文档
3. **airis-knowledge-mgmt** - 建立项目知识库
4. **airis-code-search** - 定位关键文件

### 完整工作流

#### Step 1: 索引项目结构 (airis-project-indexing)

```typescript
// 用户提示（在新项目目录下）
用户: "分析这个 Next.js 项目的结构"

// airis-project-indexing 自动触发
// 执行流程:
// 1. AIRIS Agent 扫描项目目录
// 2. 识别框架和依赖
// 3. 生成项目概览

// 输出示例
✅ 项目分析完成

框架: Next.js 14.0.4 (App Router)
依赖:
- React 18.2.0
- TypeScript 5.3.3
- Tailwind CSS 3.4.0

目录结构:
/app          # App Router 页面
/components   # React 组件
/lib          # 工具函数
/public       # 静态资源
/types        # TypeScript 类型

配置文件:
- next.config.js
- tailwind.config.ts
- tsconfig.json
```

#### Step 2: 查询 Supabase 集成文档 (airis-library-docs)

```typescript
// 查询集成指南
用户: "查询 Supabase 在 Next.js App Router 中的集成方法"

// airis-library-docs 自动触发
// 输出示例
✅ Supabase + Next.js 集成指南

安装:
```bash
npm install @supabase/supabase-js @supabase/ssr
```

配置 (app/utils/supabase/client.ts):
```typescript
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

Server Component 使用:
```typescript
import { createClient } from '@/utils/supabase/server'

export default async function Page() {
  const supabase = createClient()
  const { data } = await supabase.from('posts').select()
  return <div>{/* 使用 data */}</div>
}
```
```

#### Step 3: 建立项目知识库 (airis-knowledge-mgmt)

```typescript
// 保存项目信息到知识图谱
用户: "将项目技术栈和架构决策保存到知识库"

// airis-knowledge-mgmt 自动触发
// 输出示例
✅ 已创建项目知识库

实体网络:
- My Next.js Project (project)
  ├─ 使用: Next.js 14 (framework)
  ├─ 使用: Supabase (database)
  ├─ 使用: Tailwind CSS (styling)
  └─ 使用: TypeScript (language)

架构决策:
1. 选择 App Router（而非 Pages Router）
   - 理由: 支持 React Server Components
2. 选择 Supabase（而非 Firebase）
   - 理由: PostgreSQL, 开源, 更好的 SQL 支持
3. 选择 Tailwind CSS（而非 CSS Modules）
   - 理由: 快速开发, 一致性

已保存到: .serena/memories/project_architecture.md
```

#### Step 4: 定位关键配置文件 (airis-code-search)

```typescript
// 快速定位需要修改的文件
用户: "找到所有环境变量配置文件"

// airis-code-search 自动触发
// 输出示例
✅ 找到环境变量配置（3 个位置）:

1. .env.local.example
   - NEXT_PUBLIC_SUPABASE_URL=
   - NEXT_PUBLIC_SUPABASE_ANON_KEY=

2. .env.local（需要创建）
   - 填入实际的 Supabase 凭证

3. next.config.js
   - env: {} （可选的环境变量暴露）

建议: 复制 .env.local.example 为 .env.local 并填入凭证
```

### 时间估算

| 步骤 | 耗时 | 说明 |
|------|------|------|
| 项目索引 | 10-20s | AIRIS Agent (HOT 模式) |
| 文档查询 | 10-20s | Context7 (COLD 启动) |
| 知识库创建 | 5-10s | Memory (HOT 模式) |
| 代码搜索 | 20-40s | MorphLLM (COLD 启动) |
| **总计** | **~80s** | 完整项目初始化 |

---

## 场景 5: 调试 + 解决方案保存

### 业务需求

> "解决生产环境的性能问题，并将解决方案保存以便未来参考"

### 涉及 Skills

1. **airis-web-research** - 搜索类似问题的解决方案
2. **airis-code-search** - 定位性能瓶颈代码
3. **airis-knowledge-mgmt** - 保存故障排查记录

### 完整工作流

#### Step 1: 搜索解决方案 (airis-web-research)

```typescript
// 用户提示
用户: "研究 Next.js 中 hydration mismatch 错误的解决方法"

// airis-web-research 自动触发
// 输出示例
✅ 研究完成

常见原因:
1. 服务端和客户端渲染不一致
2. 使用了 localStorage（仅客户端可用）
3. 日期/时间格式化不一致
4. 第三方脚本注入（广告、分析）

解决方案:
1. 使用 useEffect 包裹客户端专属代码
2. 使用 suppressHydrationWarning 属性（临时）
3. 确保 SSR 和 CSR 数据一致

已保存到: .serena/memories/nextjs_hydration_mismatch_solutions.md
```

#### Step 2: 定位问题代码 (airis-code-search)

```typescript
// 定位可能的问题代码
用户: "找到所有使用 localStorage 的组件"

// airis-code-search 自动触发
// 输出示例
✅ 找到 localStorage 使用（4 个位置）:

1. components/ThemeToggle.tsx:15
   - const theme = localStorage.getItem('theme')
   - ⚠️ 可能导致 hydration mismatch

2. components/UserPreferences.tsx:22
   - const prefs = JSON.parse(localStorage.getItem('prefs'))
   - ⚠️ 同上

3. hooks/useLocalStorage.ts:8
   - 自定义 hook，封装 localStorage 访问
   - ✅ 已处理 SSR（检查 typeof window）

4. components/ShoppingCart.tsx:30
   - const cart = localStorage.getItem('cart')
   - ⚠️ 可能导致 hydration mismatch

建议: 1 和 2 需要使用 useEffect 包裹
```

#### Step 3: 保存故障排查记录 (airis-knowledge-mgmt)

```typescript
// 记录完整的调试过程
用户: "保存 hydration mismatch 的调试过程和解决方案"

// airis-knowledge-mgmt 自动触发
// 输出示例
✅ 已创建故障排查记录

实体:
- Next.js Hydration Mismatch Fix (troubleshooting_case)
  ├─ 问题: Hydration mismatch in ThemeToggle
  ├─ 原因: localStorage 在 SSR 中不可用
  └─ 解决: 使用 useEffect + useState 模式

解决方案代码:
```typescript
// 修改前
const ThemeToggle = () => {
  const theme = localStorage.getItem('theme') // ❌ SSR 中会失败
  return <div>{theme}</div>
}

// 修改后
const ThemeToggle = () => {
  const [theme, setTheme] = useState('light')  // 默认值

  useEffect(() => {
    // ✅ 仅在客户端执行
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) setTheme(savedTheme)
  }, [])

  return <div>{theme}</div>
}
```

时间线:
- 2025-12-31 14:30: 生产环境发现 hydration 错误
- 2025-12-31 14:35: 使用 airis-web-research 搜索解决方案
- 2025-12-31 14:40: 使用 airis-code-search 定位问题代码
- 2025-12-31 14:50: 修复并部署
- 2025-12-31 15:00: 验证修复成功

影响: 用户端无感知，性能改善 15%
```

### 时间估算

| 步骤 | 耗时 | 说明 |
|------|------|------|
| 解决方案研究 | 30-60s | Tavily + Fetch (COLD 启动) |
| 代码定位 | 20-40s | MorphLLM (COLD 启动) |
| 记录保存 | 5-10s | Memory (HOT 模式) |
| **总计** | **~90s** | 信息收集和记录 |

---

## 最佳实践

### 1. 工作流设计原则

#### 原则 1: 先搜索，后行动

```typescript
// ❌ 错误：直接动手
用户: "重构这个组件"
→ 立即开始修改代码

// ✅ 正确：先研究
用户: "重构这个组件"
→ 1. airis-web-research: 搜索最佳实践
→ 2. airis-code-search: 定位相关代码
→ 3. 开始重构
```

#### 原则 2: 信息沉淀优先

```typescript
// ✅ 每个关键决策都应保存到知识库
1. 架构决策 → airis-knowledge-mgmt
2. 技术调研 → airis-web-research（自动保存到 Serena）
3. 故障排查 → airis-knowledge-mgmt

// 好处:
// - 未来可搜索
// - 团队共享
// - 决策可追溯
```

#### 原则 3: 组合胜过单一

```typescript
// 单一 Skill（功能有限）
airis-web-research: "研究 React 19"
→ 只得到研究报告

// 组合 Skills（价值倍增）
airis-web-research: "研究 React 19"
  → 保存到 .serena/memories/
  ↓
airis-knowledge-mgmt: "创建 React 19 知识实体"
  → 建立知识图谱
  ↓
airis-code-search: "找到可升级到 React 19 的组件"
  → 执行计划
```

### 2. 时序优化技巧

#### 技巧 1: 利用 COLD 模式启动时间

```typescript
// 并行触发多个 COLD 服务器
用户: "同时研究 A 技术和 B 技术，并生成 UI 原型"

// Claude Code 会并行启动:
// - Tavily (COLD) - 研究 A 技术
// - Context7 (COLD) - 研究 B 技术
// - Magic (COLD) - 生成 UI

// 总耗时: max(A, B, UI) 而非 sum(A + B + UI)
```

#### 技巧 2: 预热常用服务器

```bash
# 如果频繁使用某个 COLD 服务器，改为 HOT
# 编辑 mcp-config.json:
{
  "mcpServers": {
    "tavily": {
      "mode": "hot"  // 从 cold 改为 hot
    }
  }
}
```

### 3. 错误处理策略

#### 策略 1: 优雅降级

```typescript
// ✅ 即使某个 Skill 失败，工作流也能继续
try {
  // 尝试使用 airis-web-research
  await webResearch("topic")
} catch (error) {
  console.log("Web 研究失败，跳过此步骤")
  // 继续执行后续步骤
}

await knowledgeMgmt("保存现有信息")  // 仍然执行
```

#### 策略 2: 参数验证优先

```typescript
// ✅ 始终先验证参数
const schema = await airis-schema({ tool: "serena:write_memory" })
// 确认参数正确后再执行
await airis-exec({ tool: "serena:write_memory", arguments: {...} })
```

### 4. 知识管理技巧

#### 技巧 1: 结构化命名

```markdown
# ✅ 良好的命名约定
.serena/memories/
├── architecture/
│   ├── state_management_decision.md
│   └── database_schema_design.md
├── research/
│   ├── react_19_features.md
│   └── nextjs_performance_optimization.md
└── troubleshooting/
    ├── hydration_mismatch_fix.md
    └── cors_error_resolution.md

# ❌ 混乱的命名
.serena/memories/
├── notes1.md
├── temp.md
└── untitled.md
```

#### 技巧 2: 关联相关实体

```typescript
// ✅ 建立实体之间的关系
创建实体:
- React 19 (framework_version)
  ├─ 引入: Server Actions (feature)
  ├─ 引入: Asset Loading (feature)
  └─ 影响: My Project (project)

// 好处: 未来可通过图查询找到所有受影响的项目
```

---

## 📊 工作流效率对比

### 传统方式 vs AIRIS Skills

| 任务 | 传统方式 | 使用 AIRIS Skills | 提升 |
|------|---------|------------------|------|
| **技术调研** | 30-60 分钟（手动搜索、整理） | 2-3 分钟（自动化） | **90% ↓** |
| **代码定位** | 10-20 分钟（手动 grep） | 30-60 秒（语义搜索） | **95% ↓** |
| **知识沉淀** | 15-30 分钟（手动编写文档） | 10-20 秒（自动保存） | **98% ↓** |
| **UI 原型** | 1-2 小时（手动编码） | 30-60 秒（生成组件） | **98% ↓** |

### 投资回报率

```
一次性投资:
- 安装 AIRIS MCP Gateway: 10-30 分钟
- 学习 7 个 Skills: 30-60 分钟
总计: 1-1.5 小时

每日收益:
- 节省 2-4 小时（假设 5 个任务/天）

回本周期: < 1 天
```

---

## 🎓 学习路径

### 初学者（第 1 天）

1. 熟悉单个 Skill 使用
2. 尝试场景 1（技术调研）
3. 完成 1-2 个简单工作流

### 中级用户（第 2-3 天）

1. 尝试所有 5 个场景
2. 设计自己的工作流
3. 优化 HOT/COLD 模式配置

### 高级用户（第 4+ 天）

1. 创建自定义工作流模板
2. 集成到 CI/CD 流程
3. 贡献新的场景示例

---

## 📞 获取帮助

- **文档**: [README.md](../README.md)
- **快速入门**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **验证指南**: [GATEWAY_VERIFICATION.md](GATEWAY_VERIFICATION.md)
- **GitHub Issues**: https://github.com/your-org/howie_skills/issues

---

**最后更新**: 2025-12-31
**适用版本**: howie_skills v1.0+
