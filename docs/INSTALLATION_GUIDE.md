# Howie AIRIS Skills 安装指南

**目标受众**: 希望在 Claude Code 中使用 Howie AIRIS Skills 的用户
**预估时间**: 5-10 分钟
**难度**: 初级

---

## 📋 前置条件

在安装 Howie AIRIS Skills 之前，请确保：

1. ✅ **Claude Code 已安装** (v1.0+)
   - 下载: https://claude.com/code
   - 验证: 运行 `claude --version`

2. ✅ **AIRIS MCP Gateway 已部署** (v2.0+)
   - 安装指南: https://github.com/airis-org/mcp-gateway
   - 验证: 访问 http://localhost:9400/health

3. ✅ **基础工具已安装**
   - Git (用于克隆仓库)
   - Bash (用于运行安装脚本)

---

## 🚀 安装方式

### 方式 1: Claude Code Marketplace 安装（推荐）

**适用场景**: 官方发布后的标准安装方式

**步骤**:

#### Step 1: 添加 Marketplace

在 Claude Code 中执行：

```bash
/plugin marketplace add your-org/howie_skills
```

**说明**: 将 `your-org` 替换为实际的 GitHub 组织名

#### Step 2: 浏览并安装

```bash
# 方法 1: 交互式安装
/plugin install

# 然后选择:
# 1. Browse and install plugins
# 2. howie-airis-skills
# 3. Install now

# 方法 2: 直接安装
/plugin install howie-airis-skills
```

#### Step 3: 验证安装

在 Claude Code 中执行：

```bash
# 列出已安装的 plugins
/plugin list

# 应该看到:
# howie-airis-skills (v1.0.0) - ACTIVE
```

---

### 方式 2: 手动安装（当前推荐）

**适用场景**: 在 marketplace 发布前，或需要自定义安装

**步骤**:

#### Step 1: 克隆仓库

```bash
# 克隆到本地
git clone https://github.com/your-org/howie_skills.git
cd howie_skills
```

**说明**: 将 `your-org` 替换为实际的 GitHub 组织名

#### Step 2: 运行增量式安装脚本

```bash
# 运行智能安装脚本（v2.0 增量式）
bash scripts/install.sh
```

**脚本新特性** (v2.0):

✨ **智能增量式安装**:
- ✅ 自动检测已安装的 Skills
- ✅ 识别新的 Skills 和可更新的 Skills
- ✅ 提供 5 种安装模式选择
- ✅ 支持逐个 Skill 选择安装
- ✅ 自动备份旧版本（更新时）

**脚本执行流程**:

1. **扫描分析**: 检测已安装 Skills 和仓库中的 Skills
2. **状态报告**: 显示新 Skills、可更新 Skills 数量
3. **模式选择**: 提供 5 种安装模式
4. **执行安装**: 根据选择安装/更新 Skills
5. **结果摘要**: 显示详细的安装统计

**预期输出**:

```
🚀 Howie AIRIS Skills 智能安装器
版本: v2.0 (增量式安装)

📊 安装状态分析:

  仓库中的 Skills: 7
  已安装的 Skills: 3
  待安装的新 Skills: 4
  可更新的 Skills: 0

📦 待安装的新 Skills (4 个):
  [新] airis-browser-automation
      浏览器自动化 (Playwright snapshot vs screenshot)...
  [新] airis-library-docs
      库文档查询 (Context7 两步流程)...
  [新] airis-ui-generation
      UI 组件生成 (Magic 绝对路径模式)...
  [新] airis-project-indexing
      项目索引分析 (AIRIS Agent 三功能)...

请选择操作模式:
  1. 安装/更新所有 (推荐)
  2. 仅安装新 Skills
  3. 仅更新已有 Skills
  4. 逐个选择
  5. 取消

请输入选项 (1-5): 1

开始安装...

📦 安装 airis-browser-automation...
   ✓ 完成
📦 安装 airis-library-docs...
   ✓ 完成
📦 安装 airis-ui-generation...
   ✓ 完成
📦 安装 airis-project-indexing...
   ✓ 完成

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 安装完成！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  新安装: 4 个
  已更新: 0 个

📚 当前已安装的 Skills:

  [新安装] airis-browser-automation
            浏览器自动化 (Playwright snapshot vs screenshot)...

  [新安装] airis-library-docs
            库文档查询 (Context7 两步流程)...

  [新安装] airis-ui-generation
            UI 组件生成 (Magic 绝对路径模式)...

  [新安装] airis-project-indexing
            项目索引分析 (AIRIS Agent 三功能)...

  [已有] airis-web-research
         完整的 Web 研究流程助手...

  [已有] airis-code-search
         代码搜索和编辑助手...

  [已有] airis-knowledge-mgmt
         知识图谱管理...

总计: 7 个 Skills

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 使用方式:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  自动触发: Claude 会根据你的请求自动使用相应的 skill
  手动调用: 在请求中明确指定 skill 名称

示例:
  "帮我研究一下 React Server Components"
  → 自动触发 airis-web-research skill

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 更多信息:
  - 快速入门: GETTING_STARTED.md
  - 安装指南: docs/INSTALLATION_GUIDE.md
  - 工作流示例: docs/WORKFLOW_EXAMPLES.md
```

**5 种安装模式**:

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| **1. 安装/更新所有** | 自动处理所有新 Skills 和更新 | 推荐：首次安装或全面更新 |
| **2. 仅安装新 Skills** | 只安装新增的 Skills，不更新已有 | 保留已有 Skills 的自定义修改 |
| **3. 仅更新已有 Skills** | 只更新已安装的 Skills | 跳过新 Skills，仅升级现有 |
| **4. 逐个选择** | 对每个 Skill 单独询问 | 精细控制，按需安装 |
| **5. 取消** | 不执行任何安装 | 仅查看状态，不做修改 |

#### Step 3: 验证安装

```bash
# 检查 skills 目录
ls ~/.claude/skills/

# 应该看到：
# airis-web-research/
# airis-code-search/
# airis-knowledge-mgmt/
# airis-browser-automation/
# airis-library-docs/
# airis-ui-generation/
# airis-project-indexing/

# 检查某个 Skill 的结构
ls ~/.claude/skills/airis-web-research/

# 应该看到：
# SKILL.md
# references/ (可选)
```

---

### 方式 3: 手动复制（高级用户）

**适用场景**: 需要自定义安装位置或仅安装部分 Skills

**步骤**:

#### Step 1: 创建 Skills 目录

```bash
mkdir -p ~/.claude/skills
```

#### Step 2: 复制所需的 Skills

```bash
# 复制所有 Skills
cp -r howie_skills/skills/* ~/.claude/skills/

# 或仅复制特定 Skills
cp -r howie_skills/skills/airis-web-research ~/.claude/skills/
cp -r howie_skills/skills/airis-code-search ~/.claude/skills/
```

#### Step 3: 验证结构

确保每个 Skill 目录包含：
- ✅ `SKILL.md` (必需) - 主要的 Skill 定义文件
- ✅ `references/` (可选) - 额外的参考文档

**SKILL.md 结构示例**:

```markdown
---
name: airis-web-research
description: 完整的 Web 研究流程助手，使用 Tavily 搜索...
---

# AIRIS Web Research Helper

[Skill 内容...]
```

---

## ✅ 验证安装

### 快速验证（2 分钟）

在 Claude Code 中测试以下场景：

#### 测试 1: 自动触发

```
用户: "帮我研究一下 React 19 的新特性"
```

**预期行为**:
1. Claude Code 自动识别需要 Web 研究
2. 触发 `airis-web-research` skill
3. 执行 Tavily 搜索 → Fetch 提取 → Serena 保存
4. 返回结构化的研究报告

**成功标志**:
```
✅ 研究结果已保存到: .serena/memories/react-19-features.md

内容摘要:
- React 19 新增 Actions API
- 改进的 Server Components 支持
- ...
```

#### 测试 2: 手动指定 Skill

```
用户: "使用 airis-code-search skill 找到所有处理用户认证的代码"
```

**预期行为**:
1. 使用 MorphLLM 语义搜索
2. 定位相关文件和函数
3. 保存搜索结果到 Serena

**成功标志**:
```
✅ 找到 JWT 相关代码（5 个位置）:

1. src/auth/jwt.service.ts:23-45
   - generateToken(userId, expiresIn)
   ...
```

#### 测试 3: 检查 Skill 元数据

```bash
# 在 Claude Code 中执行
/skills list

# 应该看到:
# airis-web-research - 完整的 Web 研究流程助手
# airis-code-search - 代码搜索和编辑助手
# airis-knowledge-mgmt - 知识图谱管理
# airis-browser-automation - 浏览器自动化
# airis-library-docs - 库文档查询
# airis-ui-generation - UI 组件生成
# airis-project-indexing - 项目索引分析
```

---

## 🔧 Claude Code Skills 系统工作原理

### Skill 加载机制

**目录结构**:

```
~/.claude/
├── skills/                  # Skills 根目录
│   ├── airis-web-research/  # 单个 Skill 目录
│   │   ├── SKILL.md         # Skill 定义（必需）
│   │   └── references/      # 参考文档（可选）
│   ├── airis-code-search/
│   │   └── SKILL.md
│   └── ... (其他 Skills)
└── config.json              # Claude Code 配置（可选）
```

**加载流程**:

1. **启动时扫描**: Claude Code 启动时扫描 `~/.claude/skills/` 目录
2. **解析 YAML Frontmatter**: 读取每个 `SKILL.md` 的 frontmatter
   ```yaml
   ---
   name: airis-web-research
   description: 完整的 Web 研究流程助手...
   ---
   ```
3. **索引 Skills**: 根据 `name` 和 `description` 建立 Skill 索引
4. **准备激活**: 当用户请求匹配时，加载完整的 `SKILL.md` 内容

### Skill 触发机制

**自动触发**:

```
用户请求 → Claude 分析意图 → 匹配 Skill description → 激活 Skill
```

**匹配示例**:

| 用户请求 | 匹配的 Skill | 匹配原因 |
|---------|-------------|---------|
| "研究 XXX" | airis-web-research | description 包含 "研究"、"搜索" |
| "找到 XXX 的代码" | airis-code-search | description 包含 "代码搜索" |
| "保存到知识库" | airis-knowledge-mgmt | description 包含 "知识图谱" |

**手动触发**:

```
用户明确指定 → "使用 [skill-name] skill ..." → 直接激活
```

### Progressive Disclosure 机制

**设计理念**: 只在需要时加载详细内容

**实现方式**:

1. **Skill 扫描阶段**: 仅读取 frontmatter (name + description)
2. **Skill 匹配阶段**: 比较 description 与用户请求
3. **Skill 激活阶段**: 加载完整的 `SKILL.md` 内容
4. **Skill 执行阶段**: 根据指令执行 MCP 工具调用

**好处**:
- ✅ 快速启动（不加载所有 Skill 内容）
- ✅ 低内存占用（仅加载激活的 Skill）
- ✅ 高效匹配（基于简洁的 description）

---

## ⚙️ 配置选项

### Skill 优先级配置

**文件**: `~/.claude/config.json`

```json
{
  "skills": {
    "priority": [
      "airis-web-research",
      "airis-code-search",
      "airis-knowledge-mgmt"
    ],
    "disabled": []
  }
}
```

**说明**:
- `priority`: 优先匹配的 Skills（按顺序）
- `disabled`: 禁用的 Skills

### Skill 自定义配置

**文件**: `~/.claude/skills/airis-web-research/config.json` (可选)

```json
{
  "max_search_results": 5,
  "default_search_depth": "advanced",
  "auto_save_to_serena": true
}
```

**说明**: 每个 Skill 可以有自己的配置文件（仅当 Skill 支持时有效）

---

## 🔍 故障排查

### 问题 1: Skills 未被识别

**症状**:
```
用户: "帮我研究一下 React 19"
Claude: [未触发 airis-web-research]
```

**诊断**:

```bash
# 1. 检查 Skills 目录是否存在
ls ~/.claude/skills/

# 2. 检查 SKILL.md 文件
cat ~/.claude/skills/airis-web-research/SKILL.md | head -20

# 3. 验证 YAML frontmatter 格式
grep -A 5 "^---" ~/.claude/skills/airis-web-research/SKILL.md
```

**解决方案**:

```bash
# 方案 1: 重新安装
cd howie_skills
bash scripts/install.sh

# 方案 2: 手动修复 YAML frontmatter
# 确保格式正确:
# ---
# name: airis-web-research
# description: 完整的 Web 研究流程助手...
# ---
```

---

### 问题 2: Skill 触发但执行失败

**症状**:
```
✅ 触发 airis-web-research
❌ Error: AIRIS MCP Gateway not available
```

**诊断**:

```bash
# 1. 检查 Gateway 状态
curl http://localhost:9400/health

# 2. 检查 MCP 工具
# 在 Claude Code 中执行:
mcp__airis-mcp-gateway__airis-find({ query: "" })
```

**解决方案**:

参考 [GATEWAY_VERIFICATION.md](GATEWAY_VERIFICATION.md) 进行完整验证

---

### 问题 3: Skills 目录权限错误

**症状**:
```
Error: Permission denied: /home/user/.claude/skills
```

**解决方案**:

```bash
# 修复权限
chmod -R 755 ~/.claude/skills

# 重新安装
cd howie_skills
bash scripts/install.sh
```

---

### 问题 4: 旧版本 Skill 冲突

**症状**:
```
Warning: Skill 'airis-web-research' already exists
```

**解决方案**:

```bash
# 方案 1: 删除旧版本
rm -rf ~/.claude/skills/airis-*

# 方案 2: 备份后覆盖
mv ~/.claude/skills ~/.claude/skills.backup
bash scripts/install.sh
```

---

## 🎯 高级配置

### 仅安装部分 Skills

如果只需要特定的 Skills：

```bash
# 创建目录
mkdir -p ~/.claude/skills

# 仅安装 Web 研究和代码搜索
cp -r howie_skills/skills/airis-web-research ~/.claude/skills/
cp -r howie_skills/skills/airis-code-search ~/.claude/skills/
```

### 自定义 Skill 安装位置

如果需要安装到非默认位置：

```bash
# 设置自定义路径
export CLAUDE_SKILLS_DIR="/custom/path/to/skills"

# 创建目录
mkdir -p "$CLAUDE_SKILLS_DIR"

# 复制 Skills
cp -r howie_skills/skills/* "$CLAUDE_SKILLS_DIR/"

# 配置 Claude Code
# 编辑 ~/.claude/config.json:
# {
#   "skillsDirectory": "/custom/path/to/skills"
# }
```

### 开发模式安装（符号链接）

适用于 Skill 开发者：

```bash
# 使用符号链接（修改源码立即生效）
ln -s /path/to/howie_skills/skills/airis-web-research ~/.claude/skills/airis-web-research

# 验证链接
ls -la ~/.claude/skills/airis-web-research
# 应显示: airis-web-research -> /path/to/howie_skills/skills/airis-web-research
```

---

## 📚 后续步骤

安装完成后，建议按以下顺序学习：

### 第 1 天：快速上手

1. ✅ 阅读 [GETTING_STARTED.md](../GETTING_STARTED.md)（5 分钟）
2. ✅ 验证 Gateway 部署 [GATEWAY_VERIFICATION.md](GATEWAY_VERIFICATION.md)（3 分钟）
3. ✅ 尝试第一个 Skill（10 分钟）

### 第 2-3 天：掌握工作流

1. ✅ 学习工作流组合 [WORKFLOW_EXAMPLES.md](WORKFLOW_EXAMPLES.md)（30 分钟）
2. ✅ 实践 5 个实战场景（1-2 小时）
3. ✅ 自定义简单工作流（1 小时）

### 第 4+ 天：深度定制

1. ✅ 深入学习 MCP 参数 [MCP_PARAMETER_REFERENCE.md](MCP_PARAMETER_REFERENCE.md)（按需）
2. ✅ 创建自定义 Skills（参考 [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md)）
3. ✅ 优化 HOT/COLD 模式配置

---

## 🔗 相关资源

### 文档

- [快速入门指南](../GETTING_STARTED.md) - 5 分钟上手
- [Gateway 验证指南](GATEWAY_VERIFICATION.md) - 验证部署
- [工作流组合示例](WORKFLOW_EXAMPLES.md) - 实战场景
- [MCP 参数参考](MCP_PARAMETER_REFERENCE.md) - 完整参数文档

### 外部资源

- [Claude Code 官方文档](https://claude.com/code)
- [Agent Skills 标准](https://agentskills.io)
- [AIRIS MCP Gateway](https://github.com/airis-org/mcp-gateway)
- [Model Context Protocol](https://modelcontextprotocol.io)

### 社区

- [GitHub Issues](https://github.com/your-org/howie_skills/issues) - 问题报告
- [GitHub Discussions](https://github.com/your-org/howie_skills/discussions) - 讨论交流

---

## 📞 获取帮助

如果遇到安装问题：

1. **检查故障排查章节** - 本文档包含常见问题解决方案
2. **查看 Gateway 验证指南** - [GATEWAY_VERIFICATION.md](GATEWAY_VERIFICATION.md)
3. **提交 GitHub Issue** - https://github.com/your-org/howie_skills/issues
4. **联系维护者** - hao@example.com

---

**最后更新**: 2025-12-31
**适用版本**: howie_skills v1.0+, Claude Code v1.0+
**维护者**: Hao
