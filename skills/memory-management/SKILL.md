---
name: memory-management
description: Intelligent three-tier memory management system integrating Memory MCP (session memory), Serena MCP (project context), and Mindbase (long-term knowledge). Automatically selects appropriate storage layer and provides smart recall across all tiers. Use when users need to store information, recall past context, manage session/project memories, or search knowledge bases. Supports Chinese and English semantic search with optimized thresholds.
---

# Memory Management

Intelligent memory system with automatic layer selection and smart recall across three complementary storage tiers.

---

## 🏗️ Three-Tier Architecture

### Quick Reference

| Layer | MCP | Scope | Speed | Use For |
|-------|-----|-------|-------|---------|
| **L1** | Memory MCP | Session | <50ms | Current tasks, temporary states |
| **L2** | Serena MCP | Project | <200ms | Project decisions, code context |
| **L3** | Mindbase | Global | <1s | Conversations, cross-project knowledge |

### L1: Short-Term Memory (Memory MCP)

**Characteristics**:
- Session-scoped, cleared after conversation ends
- Fastest response time (<50ms)
- Graph-based: entities + relations
- Ideal for working memory and current context

**Available Tools**:
- `create_entities` - Store entities with observations
- `create_relations` - Link entities with relationships
- `search_nodes` - Search by entity/observation text
- `open_nodes` - Retrieve specific entities by name
- `delete_entities` - Remove entities and relations

**Use Cases**:
- Current task status
- Temporary variables
- Active conversation context
- Working memory graph

### L2: Project Context (Serena MCP)

**Characteristics**:
- Project-scoped, persistent across sessions
- Fast response (<200ms)
- File-based: Markdown with Frontmatter
- Symbol-level code understanding via LSP

**Available Tools**:
- `activate_project` - Load project context
- `write_memory` - Save project memories (Markdown)
- `read_memory` - Retrieve project memories
- `list_memories` - List all project memories
- `get_symbol_references` - Code symbol tracking
- `find_symbol` - Symbol-level code search

**Use Cases**:
- Architectural decisions
- Design patterns
- Project-specific conventions
- Code context and dependencies

### L3: Long-Term Memory (Mindbase)

**Characteristics**:
- Global scope, permanent storage
- Slower but comprehensive (<1s)
- PostgreSQL + pgvector semantic search
- Cross-project knowledge base

**Available Tools**:
- `conversation_save` - Archive conversations
- `conversation_search` - Semantic search conversations
- `conversation_get` - Retrieve by ID
- `memory_write` - Store structured knowledge
- `memory_search` - Semantic search memories
- `session_create/start` - Session management

**Use Cases**:
- Historical conversations
- Cross-project patterns
- Best practices library
- Reusable solutions

---

## 🤖 Automatic Layer Selection

### Decision Logic

When user asks to "remember", "save", or "store" something:

```
1. Analyze content type:
   - Task/status/current context → L1 (Memory MCP)
   - Design decision/architecture → L2 (Serena MCP)
   - Conversation/knowledge → L3 (Mindbase)

2. Consider persistence need:
   - Session only → L1
   - Project lifetime → L2
   - Permanent/cross-project → L3

3. Store automatically without asking user
```

### Examples

**User**: "Remember I'm working on the authentication feature"
→ **Action**: Store in L1 (Memory MCP)
```typescript
create_entities([{
  name: "current_task",
  entityType: "task",
  observations: ["Working on authentication feature"]
}])
```

**User**: "We decided to use JWT instead of sessions"
→ **Action**: Store in L2 (Serena MCP)
```typescript
write_memory({
  memory_file_name: "auth-architecture-decision",
  content: "# Authentication Decision\n\nDecided to use JWT..."
})
```

**User**: "Save this conversation for future reference"
→ **Action**: Store in L3 (Mindbase)
```typescript
conversation_save({
  source: "claude-code",
  title: "Authentication Implementation Discussion",
  content: { messages: [...] },
  metadata: { project: "current-project", tags: ["authentication", "architecture"] }
})
```

---

## 🔍 Smart Recall Strategy

### Search Cascade

When user asks to "recall", "find", or "search" for something:

```
1. L1 (Fastest): Check current session
   └─ search_nodes(query)

2. L2 (Project context): Check project memories
   └─ list_memories() + read_memory()

3. L3 (Comprehensive): Semantic search globally
   └─ conversation_search() or memory_search()
      - Threshold: 0.3 (Chinese), 0.5 (English)
```

### Search Examples

**User**: "What did we decide about authentication?"
→ **Strategy**: L2 → L3
```typescript
// First check L2 (project context)
const l2Results = await read_memory({ memory_file_name: "auth-architecture-decision" });

// If not found, search L3 (global knowledge)
if (!l2Results) {
  const l3Results = await conversation_search({
    query: "authentication decision",
    threshold: 0.3,
    project: "current-project"
  });
}
```

**User**: "Have we solved similar problems before?"
→ **Strategy**: L3 only (cross-project)
```typescript
const results = await conversation_search({
  query: "similar problems",
  threshold: 0.3,
  limit: 10
});
```

**User**: "What was I working on?"
→ **Strategy**: L1 only (current session)
```typescript
const task = await search_nodes({ query: "working" });
```

---

## 🔄 Automatic Promotion

### Session End Promotion

When session ends (user says goodbye or `/sc:save`):

1. **Review L1 memories** - Identify important findings
2. **Promote to L2** - Save project-relevant items to Serena
3. **Archive to L3** - Optionally save full conversation

```typescript
// Example promotion workflow
async function promoteMemories() {
  // 1. Get important L1 entities
  const entities = await search_nodes({ query: "" }); // All entities

  // 2. Filter important ones
  const important = entities.filter(e =>
    e.entityType === "decision" ||
    e.entityType === "finding"
  );

  // 3. Promote to L2
  for (const entity of important) {
    await write_memory({
      memory_file_name: `session-${Date.now()}-${entity.name}`,
      content: `# ${entity.name}\n\n${entity.observations.join('\n')}`
    });
  }

  // 4. Archive conversation to L3
  await conversation_save({
    source: "claude-code",
    title: "Session Summary",
    content: { entities, relations },
    category: "progress"
  });
}
```

---

## 📊 Search Thresholds

### Language-Specific Thresholds

Based on actual testing with qwen3-embedding:8b model:

| Language | Exploratory | Daily Use | Precise | Exact Match |
|----------|-------------|-----------|---------|-------------|
| **Chinese** | 0.2 | 0.3 ✅ | 0.5 | 0.7 |
| **English** | 0.3 | 0.5 ✅ | 0.7 | 0.9 |
| **Mixed** | 0.25 | 0.35 ✅ | 0.6 | 0.8 |

**Default**: Use 0.3 for Chinese, 0.5 for English

### Why These Values?

- **Chinese semantic search** typically returns 40-60% similarity for relevant results
- **English search** returns 50-70% for relevant results
- Higher thresholds (>0.7) often return empty results
- Lower thresholds (<0.2) return too much noise

### Adaptive Threshold Example

```typescript
function getThreshold(query: string, mode: "exploratory" | "daily" | "precise" = "daily"): number {
  const isChinese = /[\u4e00-\u9fff]/.test(query);
  const isEnglish = /[a-zA-Z]/.test(query);

  if (isChinese && !isEnglish) {
    return { exploratory: 0.2, daily: 0.3, precise: 0.5 }[mode];
  } else if (isEnglish && !isChinese) {
    return { exploratory: 0.3, daily: 0.5, precise: 0.7 }[mode];
  } else {
    return { exploratory: 0.25, daily: 0.35, precise: 0.6 }[mode];
  }
}
```

---

## 📝 Common Patterns

### Pattern 1: Project Initialization

```typescript
// When starting work on a project
async function initializeProject(projectPath: string) {
  // 1. Activate project in Serena
  await activate_project({ path: projectPath });

  // 2. Load project memories
  const memories = await list_memories();

  // 3. Create session in Mindbase
  const session = await session_start({
    name: "Project Work Session",
    description: "Working on project features"
  });

  // 4. Set current task in L1
  await create_entities([{
    name: "project_context",
    entityType: "context",
    observations: [`Working on ${projectPath}`, `Session: ${session.id}`]
  }]);
}
```

### Pattern 2: Decision Recording

```typescript
// When important decision is made
async function recordDecision(decision: string, rationale: string) {
  // 1. Store in L1 for current session
  await create_entities([{
    name: `decision_${Date.now()}`,
    entityType: "decision",
    observations: [decision, rationale]
  }]);

  // 2. Persist to L2 for project reference
  await write_memory({
    memory_file_name: `decision-${Date.now()}`,
    content: `# Decision\n\n${decision}\n\n## Rationale\n\n${rationale}`
  });
}
```

### Pattern 3: Knowledge Search

```typescript
// When user asks for past solutions
async function searchKnowledge(query: string) {
  const results = [];

  // 1. Check current session (L1)
  const l1 = await search_nodes({ query });
  if (l1.length > 0) {
    results.push({ layer: "L1", data: l1 });
  }

  // 2. Check project context (L2)
  const memories = await list_memories();
  const relevant = memories.filter(m => m.toLowerCase().includes(query.toLowerCase()));
  for (const mem of relevant) {
    const content = await read_memory({ memory_file_name: mem });
    results.push({ layer: "L2", data: content });
  }

  // 3. Semantic search globally (L3)
  const threshold = query.match(/[\u4e00-\u9fff]/) ? 0.3 : 0.5;
  const l3 = await conversation_search({ query, threshold, limit: 5 });
  if (l3.length > 0) {
    results.push({ layer: "L3", data: l3 });
  }

  return results;
}
```

---

## ⚠️ Important Notes

### COLD Mode Servers

Memory MCP and Serena MCP are **COLD mode** servers - they start on first use.

**First time usage**:
```typescript
// These calls trigger server startup
await create_entities([...]); // Memory MCP
await list_memories();         // Serena MCP
```

If server fails to start, check MCP configuration in Claude settings.

### Performance Expectations

- **L1** operations should complete in <50ms
- **L2** operations should complete in <200ms
- **L3** operations may take up to 1s (embedding generation)

If performance degrades:
1. Check system resources
2. Reduce batch sizes
3. Clear old L1 entities: `delete_entities([...])`

### Chinese Search Troubleshooting

If Chinese semantic search returns empty:
1. **Lower threshold** to 0.2-0.3
2. **Verify embeddings exist**: Check if `has_embedding` is true in database
3. **Test with known content**: Search for text you know exists
4. **Review model**: Ensure qwen3-embedding:8b is active

---

## 🎯 Usage Guidelines

### When to Use Each Layer

**Use L1 (Memory MCP) when**:
- Information is session-specific
- Need fastest access (<50ms)
- Building temporary knowledge graphs
- Tracking current task state

**Use L2 (Serena MCP) when**:
- Information is project-specific
- Need symbol-level code understanding
- Recording architectural decisions
- Cross-session project continuity

**Use L3 (Mindbase) when**:
- Information is globally useful
- Need semantic search
- Archiving conversations
- Cross-project knowledge sharing

### Response Format

Always indicate which layer was used:

```
✅ Stored in L1 (session memory)
✅ Found in L2 (project context): [memory-name]
✅ Retrieved from L3 (knowledge base): 3 results
```

### Error Handling

If a layer fails:
1. **Try next layer**: L1 fails → try L2 → try L3
2. **Inform user**: Explain which layer failed and why
3. **Suggest alternatives**: Recommend manual storage or different layer

---

## 📚 Reference

### Related Documentation

- [mindbase-architecture-configuration](serena://mindbase-architecture-configuration) - Mindbase setup
- [mindbase-chinese-semantic-search-guide](serena://mindbase-chinese-semantic-search-guide) - Chinese search best practices
- Memory MCP: See MCP settings for configuration
- Serena MCP: See MCP settings for configuration

### Performance Benchmarks

Based on actual testing:
- Memory MCP: avg 15ms (store), 12ms (retrieve)
- Serena MCP: avg 85ms (write), 45ms (read)
- Mindbase: avg 850ms (embedding), 650ms (search)

### Version

- **Version**: 1.0.0
- **Last Updated**: 2026-01-16
- **Author**: AI Assistant
- **License**: MIT
