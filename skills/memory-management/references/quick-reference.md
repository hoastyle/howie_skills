# Memory Management Quick Reference

## 30-Second Cheat Sheet

### When to Use Which Layer

```
Session-only? → L1 (Memory MCP)
Project-specific? → L2 (Serena MCP)
Globally useful? → L3 (Mindbase)
```

### Common Commands

```typescript
// L1: Store temporary task
create_entities([{ name: "task", entityType: "task", observations: ["..."] }])

// L2: Save project decision
write_memory({ memory_file_name: "decision", content: "..." })

// L3: Archive conversation
conversation_save({ title: "...", content: {...}, source: "claude-code" })

// Search all layers
search_nodes({ query: "..." })              // L1
read_memory({ memory_file_name: "..." })    // L2
conversation_search({ query: "...", threshold: 0.3 }) // L3
```

### Search Thresholds

- **Chinese**: 0.3 (default)
- **English**: 0.5 (default)
- **Exploratory**: -0.1 from default
- **Precise**: +0.2 from default

## Layer Comparison

| Feature | L1 (Memory) | L2 (Serena) | L3 (Mindbase) |
|---------|-------------|-------------|---------------|
| **Speed** | <50ms | <200ms | <1s |
| **Scope** | Session | Project | Global |
| **Storage** | RAM/Disk | Filesystem | PostgreSQL |
| **Format** | Graph | Markdown | JSON+Vector |
| **Persistence** | Temporary | Permanent | Permanent |
| **Search** | Text | Text/Symbol | Semantic |

## Decision Tree

```
User Request
    │
    ├─ "Remember I'm working on..."
    │   → L1 (current task)
    │
    ├─ "We decided to use..."
    │   → L2 (project decision)
    │
    ├─ "Save this conversation"
    │   → L3 (archive)
    │
    ├─ "Find similar problems"
    │   → L3 (semantic search)
    │
    └─ "What was the code structure?"
        → L2 (symbol search)
```

## Troubleshooting

### Search Returns Empty

1. Lower threshold: 0.3 → 0.2 (Chinese)
2. Check data exists: `conversation_get()` or `list_memories()`
3. Verify embeddings: See [search-thresholds.md](search-thresholds.md)

### Layer Not Responding

1. **COLD server**: First call triggers startup
2. **Check MCP settings**: Verify configuration
3. **Fallback to other layer**: L1 fails → try L2

### Performance Issues

1. **L1 slow**: Clear old entities with `delete_entities()`
2. **L2 slow**: Too many files? Archive to L3
3. **L3 slow**: Normal (embedding generation takes time)

## Code Snippets

### Initialize Project Session

```typescript
await activate_project({ path: "/path/to/project" });
const memories = await list_memories();
await create_entities([{
  name: "session_start",
  entityType: "meta",
  observations: [`Started at ${new Date().toISOString()}`]
}]);
```

### Smart Search

```typescript
async function smartSearch(query: string) {
  // Try L1 first
  let results = await search_nodes({ query });
  if (results.length > 0) return { layer: "L1", results };

  // Try L2 next
  const memories = await list_memories();
  const relevant = memories.filter(m => m.includes(query));
  if (relevant.length > 0) return { layer: "L2", results: relevant };

  // Fallback to L3
  const threshold = /[\u4e00-\u9fff]/.test(query) ? 0.3 : 0.5;
  results = await conversation_search({ query, threshold });
  return { layer: "L3", results };
}
```

### Promote Session to Project

```typescript
// At session end
const entities = await search_nodes({ query: "" }); // Get all
const important = entities.filter(e => e.entityType === "decision");

for (const entity of important) {
  await write_memory({
    memory_file_name: `session-${entity.name}`,
    content: `# ${entity.name}\n\n${entity.observations.join('\n\n')}`
  });
}
```

## Tips & Tricks

### Tip 1: Use Filters to Narrow Search

```typescript
// Instead of high threshold
conversation_search({ query: "auth", threshold: 0.7 }) // May return nothing

// Use filters with moderate threshold
conversation_search({
  query: "auth",
  threshold: 0.3,
  project: "my-app",
  source: "claude-code"
}) // Better results
```

### Tip 2: Batch Entity Creation

```typescript
// Instead of multiple calls
await create_entities([{ name: "task1", ... }]);
await create_entities([{ name: "task2", ... }]);

// Do this
await create_entities([
  { name: "task1", ... },
  { name: "task2", ... }
]);
```

### Tip 3: Use Relations for Context

```typescript
// Create related entities
await create_entities([
  { name: "auth_module", entityType: "module", observations: ["JWT-based"] },
  { name: "user_service", entityType: "service", observations: ["Handles users"] }
]);

// Link them
await create_relations([{
  from: "user_service",
  to: "auth_module",
  relationType: "depends_on"
}]);
```

## Performance Targets

| Operation | L1 | L2 | L3 |
|-----------|----|----|-----|
| **Store** | 15ms | 85ms | 850ms |
| **Retrieve** | 12ms | 45ms | 650ms |
| **Search** | 8ms | 120ms | 650ms |
| **List** | 8ms | 120ms | 150ms |

If actual performance is significantly worse, investigate system resources or network latency.
