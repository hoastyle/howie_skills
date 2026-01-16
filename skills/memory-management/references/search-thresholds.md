# Semantic Search Threshold Guide

## Quick Reference

### Recommended Thresholds

| Scenario | Chinese | English | Mixed |
|----------|---------|---------|-------|
| **Exploratory** (find anything related) | 0.2 | 0.3 | 0.25 |
| **Daily Use** (balanced) | **0.3** ✅ | **0.5** ✅ | **0.35** ✅ |
| **Precise** (high relevance) | 0.5 | 0.7 | 0.6 |
| **Exact Match** (almost identical) | 0.7 | 0.9 | 0.8 |

## Understanding Similarity Scores

### Chinese (qwen3-embedding:8b)

Based on actual testing:

| Similarity | Meaning | Example |
|------------|---------|---------|
| **70-100%** | Nearly identical | Same text, minor variations |
| **40-60%** | Highly relevant ✅ | Same topic, related concepts |
| **30-40%** | Related | Tangentially connected |
| **<30%** | Weak connection | May be noise |

**Key Insight**: 40-60% similarity indicates **high relevance** for Chinese text. Don't expect >70% unless texts are nearly identical.

### English

| Similarity | Meaning |
|------------|---------|
| **80-100%** | Nearly identical |
| **60-80%** | Highly relevant ✅ |
| **50-60%** | Related |
| **<50%** | Weak connection |

## Real-World Examples

### Example 1: Chinese Search

**Query**: "测试"
**Results**:
- "qwen3-embedding 迁移成功记录" - 41.7% ✅ Contains "测试"
- "测试 qwen3-embedding 4000维" - 40.0% ✅ Title contains "测试"

**Analysis**: Both results are highly relevant despite being only 40% similar.

### Example 2: English Search

**Query**: "authentication implementation"
**Results**:
- "JWT Authentication Guide" - 67% ✅ Direct match
- "User Login System" - 54% ✅ Related concept
- "Session Management" - 48% ⚠️ Tangentially related

**Analysis**: 50%+ results are reliable for English.

## Troubleshooting

### Problem: Empty Results

**Symptoms**: Search returns no results despite data existing

**Solutions**:
1. **Lower threshold**:
   ```typescript
   // Too high
   threshold: 0.7 // ❌ May return nothing

   // Better
   threshold: 0.3 // ✅ For Chinese
   ```

2. **Check data**:
   ```sql
   SELECT COUNT(*) FROM conversations WHERE embedding IS NOT NULL;
   ```

3. **Verify model**:
   - Ensure qwen3-embedding:8b is active
   - Check embedding dimensions: 4000 (halfvec)

### Problem: Too Many Irrelevant Results

**Symptoms**: Search returns too much noise

**Solutions**:
1. **Increase threshold**: Try 0.4-0.5 for Chinese, 0.6-0.7 for English
2. **Add filters**:
   ```typescript
   conversation_search({
     query: "...",
     threshold: 0.3,
     source: "claude-code",     // Filter by source
     project: "my-project",     // Filter by project
     topic: "authentication"    // Filter by topic
   })
   ```
3. **Use more specific query**: "JWT authentication" vs "authentication"

## Advanced: Adaptive Thresholds

```typescript
function adaptiveThreshold(
  query: string,
  context: {
    hasFilters: boolean;
    queryLength: number;
    userIntent: "explore" | "find" | "exact";
  }
): number {
  const isChinese = /[\u4e00-\u9fff]/.test(query);
  let base = isChinese ? 0.3 : 0.5;

  // Adjust for filters
  if (context.hasFilters) {
    base += 0.05; // Can be more strict with filters
  }

  // Adjust for query length
  if (context.queryLength > 10) {
    base += 0.05; // Longer queries can be more specific
  }

  // Adjust for intent
  if (context.userIntent === "explore") {
    base -= 0.1; // Lower threshold for exploration
  } else if (context.userIntent === "exact") {
    base += 0.2; // Higher threshold for exact match
  }

  return Math.max(0.1, Math.min(0.9, base));
}
```

## Best Practices

### ✅ DO

1. **Start with recommended thresholds**: 0.3 (Chinese), 0.5 (English)
2. **Trust 40-60% similarity** for Chinese results
3. **Add filters** before increasing threshold
4. **Test with known content** to calibrate

### ❌ DON'T

1. **Don't use >0.7 as default** - Often returns nothing
2. **Don't expect >70% similarity** - Model is conservative
3. **Don't ignore 30-40% results** - May be relevant
4. **Don't forget language context** - Chinese ≠ English thresholds

## Performance Impact

| Threshold | Typical Results | Query Speed |
|-----------|----------------|-------------|
| **0.1** | 50-100 results | Slower (more processing) |
| **0.3** ✅ | 10-30 results | Fast |
| **0.5** | 5-15 results | Fast |
| **0.7** | 0-5 results | Fastest |

**Recommendation**: Use 0.3-0.5 range for balance of recall and precision.
