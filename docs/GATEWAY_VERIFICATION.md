# AIRIS MCP Gateway 验证指南

**目的**: 快速验证 AIRIS MCP Gateway 是否正确部署和配置
**预估时间**: 3-5 分钟
**前置条件**: 已按照 [AIRIS MCP Gateway 文档](https://github.com/airis-org/mcp-gateway) 完成安装

---

## 🚀 快速健康检查（3 分钟）

### Step 1: 验证 Gateway API 可用

```bash
# 检查 Gateway API 健康状态
curl http://localhost:9400/health

# 预期输出:
# {"status":"healthy","version":"2.0.0"}
```

**如果失败**:
```bash
# 检查 Docker 容器状态
docker ps | grep airis-mcp-gateway

# 如果容器未运行，启动服务
cd /path/to/airis-mcp-gateway
docker compose up -d
```

---

### Step 2: 验证 MCP 工具可用

在 Claude Code 中执行：

```typescript
// 方法 1: 使用空查询获取所有工具（推荐）
mcp__airis-mcp-gateway__airis-find({
  query: ""
})

// 预期输出: 找到 112 个工具
// [
//   "serena:write_memory",
//   "serena:read_memory",
//   "memory:create_entities",
//   "tavily:search",
//   ...
// ]
```

**如果返回 0 工具**:
```bash
# 检查 mcp-config.json
cat /path/to/airis-mcp-gateway/mcp-config.json | grep '"enabled": true'

# 确保至少有几个服务器已启用
```

---

### Step 3: 测试基础 MCP 调用

```typescript
// 测试 HOT 模式服务器 (应立即响应)
mcp__airis-mcp-gateway__airis-exec({
  tool: "memory:create_entities",
  arguments: {
    entities: [
      {
        name: "test_entity",
        entityType: "concept",
        observations: ["This is a test"]
      }
    ]
  }
})

// 预期: ✅ 成功创建实体
```

```typescript
// 测试 COLD 模式服务器 (首次调用 5-10 秒)
mcp__airis-mcp-gateway__airis-exec({
  tool: "serena:list_memories",
  arguments: {
    path: "/workspace"
  }
})

// 预期: ✅ 返回记忆文件列表（可能为空）
```

---

## 🔍 分层验证方法

### Level 1: 基础设施层

**检查项**: Docker 容器、网络、端口

```bash
# 1. 检查所有容器状态
docker compose ps

# 预期输出:
# NAME                    STATUS
# airis-mcp-gateway-api   Up
# airis-mcp-gateway       Up
# mindbase-postgres       Up (如果已配置并启用 MindBase)
# mindbase-ollama         Up (如果已配置并启用 MindBase)

# 注意: MindBase 服务器默认可能处于禁用状态
# 如需启用，使用: airis-mcp-gateway-control:gateway_enable_server
# 参数: {"server_name": "mindbase"}

# 2. 检查端口监听
netstat -tuln | grep 9400

# 预期输出: tcp 0.0.0.0:9400 LISTEN

# 3. 检查 Docker 网络
docker network ls | grep airis
```

**常见问题**:
| 问题 | 原因 | 解决方法 |
|------|------|---------|
| 端口 9400 被占用 | 其他服务使用 | `lsof -i :9400` 查找并停止 |
| 容器无法启动 | 配置错误 | `docker logs [container]` 查看日志 |
| 网络不通 | Docker 网络问题 | `docker network create airis-network` |

---

### Level 2: MCP 服务器层

**检查项**: HOT/COLD 模式服务器状态

```bash
# 检查 MCP 服务器状态
curl -s http://localhost:9400/api/tools/status | jq '.servers[] | {name, status, mode}'

# 预期输出:
# {
#   "name": "memory",
#   "status": "ready",
#   "mode": "hot"
# }
# {
#   "name": "serena",
#   "status": "cold",
#   "mode": "cold"
# }
# {
#   "name": "mindbase",
#   "status": "stopped",  # docker 模式，需要显式启用
#   "mode": "docker"
# }
```

**状态说明**:
- `ready` (HOT 模式) - 服务器已启动并就绪
- `cold` (COLD 模式) - 服务器未启动，将按需启动
- `stopped` (Docker 模式) - Docker 服务器，需要显式启用
- `error` - 服务器配置错误或启动失败

**启用 Docker 模式服务器（如 mindbase）**:
```typescript
// 使用 Gateway Control 启用服务器
await airis-exec({
  tool: "airis-mcp-gateway-control:gateway_enable_server",
  arguments: {
    server_name: "mindbase"
  }
});
// 预期: Server "mindbase" enabled. State: stopped
```

**如果状态为 error**:
```bash
# 查看具体错误信息
curl -s http://localhost:9400/api/tools/status | jq '.servers[] | select(.status == "error")'

# 检查服务器配置
cat mcp-config.json | jq '.mcpServers["服务器名称"]'

# 查看 Gateway 日志
docker logs airis-mcp-gateway --tail 50
```

---

### Level 3: 工具调用层

**检查项**: 三步工作流完整性

**测试用例 1: Memory MCP (HOT 模式)**

```typescript
// Step 1: 发现工具
const tools = await mcp__airis-mcp-gateway__airis-find({
  query: "memory entities"
})
// 预期: 找到 memory:create_entities, memory:search_nodes 等

// Step 2: 查看 schema
const schema = await mcp__airis-mcp-gateway__airis-schema({
  tool: "memory:create_entities"
})
// 预期: 返回完整的参数定义

// Step 3: 执行工具
const result = await mcp__airis-mcp-gateway__airis-exec({
  tool: "memory:create_entities",
  arguments: {
    entities: [
      {
        name: "verification_test",
        entityType: "test",
        observations: ["Gateway verification successful"]
      }
    ]
  }
})
// 预期: ✅ 成功
```

**测试用例 2: Serena MCP (COLD 模式)**

```typescript
// Step 1: 发现工具
const tools = await mcp__airis-mcp-gateway__airis-find({
  query: ""  // 使用空查询避免 bug
})
// 手动筛选: serena:write_memory, serena:read_memory

// Step 2: 查看 schema
const schema = await mcp__airis-mcp-gateway__airis-schema({
  tool: "serena:write_memory"
})
// 预期: memory_file_name, content

// Step 3: 执行工具 (首次调用等待 5-10 秒)
const result = await mcp__airis-mcp-gateway__airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "verification_test.md",
    content: "# Gateway Verification\n\nTest successful!"
  }
})
// 预期: ✅ 成功（首次调用较慢）
```

---

### Level 4: 集成验证

**检查项**: Skills 与 Gateway 集成

```typescript
// 在 Claude Code 中测试 Skill 自动触发
用户: "帮我搜索一下 React 19 新特性"

// 预期行为:
// 1. airis-web-research skill 自动触发
// 2. 依次调用: tavily:search → fetch:fetch → serena:write_memory
// 3. 保存研究结果到 .serena/memories/
```

**验证 Skill 安装**:
```bash
# 检查 Skills 目录
ls ~/.claude/skills/ | grep airis

# 预期输出:
# airis-web-research/
# airis-code-search/
# airis-knowledge-mgmt/
# airis-browser-automation/
# airis-library-docs/
# airis-ui-generation/
# airis-project-indexing/
```

---

## ⚠️ 常见配置错误诊断

### 错误 1: "Connection refused" 或 "Timeout"

**症状**:
```
Error: connect ECONNREFUSED 127.0.0.1:9400
```

**诊断步骤**:
```bash
# 1. 检查 Gateway 容器状态
docker ps | grep airis-mcp-gateway

# 2. 检查端口映射
docker port airis-mcp-gateway-api

# 3. 检查防火墙
sudo ufw status | grep 9400
```

**解决方案**:
```bash
# 重启 Gateway
docker compose restart

# 如果仍然失败，重建容器
docker compose down
docker compose up -d
```

---

### 错误 2: "0 tools found"

**症状**:
```typescript
airis-find({ query: "memory" })
// 返回: Found 0 tools
```

**诊断步骤**:
```bash
# 1. 检查 mcp-config.json
cat mcp-config.json | jq '.mcpServers | to_entries[] | select(.value.enabled == true) | .key'

# 2. 检查 Gateway 日志
docker logs airis-mcp-gateway --tail 100 | grep "error"
```

**解决方案**:
```bash
# 方案 1: 使用空查询
airis-find({ query: "" })  // 返回所有 112 个工具

# 方案 2: 启用更多服务器
# 编辑 mcp-config.json，设置 "enabled": true
docker compose restart
```

---

### 错误 3: "Field required" 参数验证错误

**症状**:
```
Error: 1 validation error for applyArguments
memory_file_name
  Field required [type=missing, input_value={'path': 'test.md'}]
```

**原因**: 参数名称错误（使用了 `path` 而非 `memory_file_name`）

**解决方案**:
```typescript
// ✅ 总是先用 airis-schema 验证参数
const schema = await airis-schema({ tool: "serena:write_memory" })
console.log(schema.inputSchema.required)  // ["memory_file_name", "content"]

// 然后使用正确的参数名
await airis-exec({
  tool: "serena:write_memory",
  arguments: {
    memory_file_name: "test.md",  // 正确！
    content: "..."
  }
})
```

**参考**: 查阅 [`docs/MCP_PARAMETER_REFERENCE.md`](MCP_PARAMETER_REFERENCE.md) 获取所有工具的正确参数名

---

### 错误 4: COLD 模式服务器首次调用超时

**症状**:
```
Error: Operation timed out after 5000ms
```

**原因**: COLD 模式服务器首次启动需要 5-10 秒

**解决方案**:
```typescript
// 方案 1: 增加超时时间（如果可配置）
// 方案 2: 等待并重试
try {
  await airis-exec({ tool: "serena:write_memory", ... })
} catch (error) {
  if (error.message.includes("timeout")) {
    console.log("COLD 模式服务器启动中，5 秒后重试...")
    await sleep(5000)
    await airis-exec({ tool: "serena:write_memory", ... })  // 第二次调用应成功
  }
}

// 方案 3: 改为 HOT 模式（频繁使用时）
// 编辑 mcp-config.json:
// "serena": { "mode": "hot" }
```

---

## 📋 完整验证清单

### 部署前检查

- [ ] 已克隆 AIRIS MCP Gateway 仓库
- [ ] 已创建 `.env` 文件并配置必要变量
- [ ] 已配置 Docker 镜像加速（国内）
- [ ] 已拉取必要的 Docker 镜像

### 部署后检查

- [ ] Gateway API 健康检查通过 (`/health`)
- [ ] 至少 4 个容器运行中
- [ ] `airis-find({ query: "" })` 返回 112 个工具
- [ ] HOT 模式工具调用成功（memory）
- [ ] COLD 模式工具调用成功（serena）
- [ ] Skills 已安装到 `~/.claude/skills/`

### 集成测试检查

- [ ] airis-web-research skill 可触发
- [ ] Tavily 搜索成功
- [ ] Serena 保存记忆成功
- [ ] 跨 Skill 工作流正常

---

## 🎯 性能基准

### 预期响应时间

| 操作 | HOT 模式 | COLD 模式（首次） | COLD 模式（后续） |
|------|---------|-----------------|-----------------|
| airis-find | < 100ms | N/A | N/A |
| airis-schema | < 100ms | N/A | N/A |
| airis-exec (memory) | < 200ms | N/A | N/A |
| airis-exec (serena) | N/A | 5-10s | < 500ms |
| airis-exec (tavily) | N/A | 3-8s | < 1s |

**如果响应时间显著超出预期**:
1. 检查网络延迟
2. 检查 Docker 资源限制
3. 考虑将常用服务器改为 HOT 模式

---

## 🔧 高级诊断

### 启用调试模式

```bash
# 1. 设置 Gateway 日志级别
export LOG_LEVEL=debug
docker compose up -d

# 2. 实时查看日志
docker logs -f airis-mcp-gateway

# 3. 查看特定服务器日志
docker logs -f airis-mcp-gateway | grep "serena"
```

### 测试 MCP 协议直连

```bash
# 绕过 Gateway，直接测试 MCP 服务器
# 例如：测试 Memory MCP
npx @modelcontextprotocol/server-memory
```

### 网络抓包

```bash
# 使用 tcpdump 抓取 9400 端口流量
sudo tcpdump -i lo -A 'tcp port 9400'
```

---

## 📞 获取帮助

如果验证失败且无法自行解决：

1. **查阅文档**:
   - [GETTING_STARTED.md](GETTING_STARTED.md) - 快速入门
   - [TROUBLESHOOTING.md](../ai_workflow/docs/airis-mcp-gateway/TROUBLESHOOTING.md) - 详细故障排查

2. **检查日志**:
   ```bash
   # Gateway 日志
   docker logs airis-mcp-gateway --tail 100

   # 所有容器日志
   docker compose logs --tail 50
   ```

3. **提交 Issue**:
   - GitHub Issues: https://github.com/your-org/howie_skills/issues
   - 包含完整的错误日志和配置信息

---

## 🔧 MindBase MCP 服务器特殊说明

**服务器**: `mindbase`
**模式**: Docker (需要显式启用)
**主要功能**: 会话记录持久化、对话语义搜索

### 启用 MindBase 服务器

```typescript
// Step 1: 启用服务器
await airis-exec({
  tool: "airis-mcp-gateway-control:gateway_enable_server",
  arguments: {
    server_name: "mindbase"
  }
});
// 预期: Server "mindbase" enabled. State: stopped
```

### 可用工具

**conversation_save** - 保存会话记录
```typescript
await airis-exec({
  tool: "mindbase:conversation_save",
  arguments: {
    source: "claude-code",  // 来源平台
    title: "会话标题",
    content: {
      summary: "会话摘要",
      stage: "阶段信息",
      // ... 其他会话上下文
    },
    category: "progress",    // task|decision|progress|note|warning|error
    priority: "high",        // critical|high|normal|low
    channel: "project-name",
    metadata: {
      project: "project-id",
      tags: ["tag1", "tag2"]
    }
  }
});
```

**常见错误**:
- ❌ 使用不存在的 `mindbase:memory_write`
- ✅ 正确使用 `mindbase:conversation_save`

### 验证 MindBase 功能

```typescript
// 测试保存会话
const result = await airis-exec({
  tool: "mindbase:conversation_save",
  arguments: {
    source: "claude-code",
    title: "MindBase 验证测试",
    content: { test: "验证内容" },
    category: "note",
    priority: "normal"
  }
});
// 预期: {} (成功) 或 { error: "..." } (失败)
```

---

**最后更新**: 2026-01-15
**适用版本**: AIRIS MCP Gateway v2.0+, howie_skills v1.0+
