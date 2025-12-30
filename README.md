# Howie AIRIS Skills

> 7 个 Helper Skills 简化 AIRIS MCP Gateway 常见操作

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.9.0-blue.svg)](https://github.com/your-org/howie_skills)

---

## 📖 简介

**Howie AIRIS Skills** 是一套专为 AIRIS MCP Gateway 设计的 Helper Skills，封装了 7 个最常用的操作模式。基于 **Progressive Disclosure** 设计理念，每个 skill 都包含详细的工作流程、代码示例和常见陷阱解决方案。

### 核心价值

- **简化复杂流程**: 将多步 MCP 工具调用封装为统一的 skill 接口
- **最佳实践文档化**: 记录常见陷阱和解决方案，避免重复踩坑
- **渐进式信息披露**: SKILL.md < 500 行，详细内容在 references/ 目录

---

## 🚀 快速开始

### Claude Code Marketplace 安装（推荐）

```bash
# 在 Claude Code 中执行
/plugin marketplace add your-org/howie_skills
/plugin install howie-airis-skills
```

### 手动安装

```bash
# 克隆仓库
git clone https://github.com/your-org/howie_skills.git
cd howie_skills

# 运行安装脚本
bash scripts/install.sh
```

### 验证安装

```bash
# 检查 skills 目录
ls ~/.claude/skills/

# 应该看到：
# airis-web-research/
# airis-code-search/
# airis-knowledge-mgmt/
# ... (其他 skills)
```

---

## 📚 Skills 索引

### MVP Release (v0.9.0) - 3 个核心 Skills

| Skill | 功能 | MCP 服务器 | 复杂度 | 行数 | 状态 |
|-------|------|-----------|--------|------|------|
| **airis-web-research** | Web 研究流程 (Tavily → Fetch → Serena) | tavily, fetch, serena | 中等 | 250 | ✅ 完成 |
| **airis-code-search** | 代码搜索编辑 (MorphLLM 占位符模式) | morphllm, serena | 中高 | 280 | 🚧 开发中 |
| **airis-knowledge-mgmt** | 知识图谱管理 (Memory + Serena) | memory, serena | 中等 | 260 | 📋 计划中 |

### Full Release (v1.0.0) - 7 个完整 Skills

| Skill | 功能 | MCP 服务器 | 复杂度 | 行数 | 状态 |
|-------|------|-----------|--------|------|------|
| **airis-browser-automation** | 浏览器自动化 (Playwright) | playwright | 中高 | 300 | 📋 计划中 |
| **airis-library-docs** | 库文档查询 (Context7) | context7 | 简单 | 200 | 📋 计划中 |
| **airis-ui-generation** | UI 组件生成 (Magic) | magic | 简单 | 220 | 📋 计划中 |
| **airis-project-indexing** | 项目索引分析 (AIRIS Agent) | airis-agent | 中等 | 240 | 📋 计划中 |

---

## 🎯 使用方式

### 自动触发（推荐）

Skills 会根据用户请求自动触发：

```
用户: "帮我研究一下 React Server Components"
Claude: [自动触发 airis-web-research skill]
       → Tavily 搜索 → Fetch 提取 → Serena 保存
       ✅ 已保存研究结果到 .serena/memories/react-rsc-research.md
```

### 手动调用

也可以明确指定使用某个 skill：

```
用户: "使用 airis-web-research skill 查询 Tailwind CSS v4 新特性"
```

---

## 📦 依赖

### 必需

- **AIRIS MCP Gateway** (v1.0+)
  - 提供统一的 MCP 工具访问接口
  - 安装: [AIRIS MCP Gateway 指南](https://github.com/airis-org/mcp-gateway)

- **Claude Code** (v1.0+)
  - 支持 Skills 功能

### 可选

推荐同时安装以下 MCP 服务器以获得完整功能：

- tavily - Web 搜索和内容提取
- fetch - 网页抓取
- serena - 项目记忆管理
- morphllm - 代码搜索和编辑
- memory - 知识图谱
- playwright - 浏览器自动化
- context7 - 库文档查询
- magic - UI 组件生成
- airis-agent - 项目索引分析

---

## 📖 文档

- [命名规范](docs/naming-convention.md) - Skill 命名规则和约定
- [集成指南](docs/integration-guide.md) - 安装和集成到项目
- [开发指南](docs/development-guide.md) - 创建新 Skill 的指南
- [变更日志](docs/changelog.md) - 版本历史和更新

---

## 🤝 贡献

欢迎贡献！请遵循以下流程：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-skill`)
3. 提交更改 (`git commit -m 'Add amazing skill'`)
4. 推送到分支 (`git push origin feature/amazing-skill`)
5. 创建 Pull Request

### 开发新 Skill

参考 [docs/SKILL_TEMPLATE.md](docs/SKILL_TEMPLATE.md) 模板和 [docs/development-guide.md](docs/development-guide.md) 指南。

---

## 📜 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🔗 相关项目

- [AIRIS MCP Gateway](https://github.com/airis-org/mcp-gateway) - 统一 MCP 工具访问
- [AI Workflow 知识库](https://github.com/your-org/ai_workflow) - AI 工具和最佳实践

---

## 📞 获取帮助

- **Issues**: [GitHub Issues](https://github.com/your-org/howie_skills/issues)
- **文档**: [完整文档](docs/)
- **邮箱**: hao@example.com

---

**最后更新**: 2025-12-30
**版本**: 0.9.0 (MVP)
**维护者**: Hao
