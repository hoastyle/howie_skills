# MCP Parameter Validation Report

## Overall Statistics

- **Total airis-exec calls**: 114
- **Total errors found**: 37
- **Accuracy**: 67.5%

## Per-Skill Results

| Skill | Calls | Errors | Accuracy | Status |
|-------|-------|--------|----------|--------|
| airis-browser-automation | 18 | 3 | 83.3% | ❌ |
| airis-code-search | 22 | 6 | 72.7% | ❌ |
| airis-knowledge-mgmt | 19 | 3 | 84.2% | ❌ |
| airis-library-docs | 13 | 0 | 100.0% | ✅ |
| airis-project-indexing | 12 | 0 | 100.0% | ✅ |
| airis-ui-generation | 12 | 19 | -58.3% | ❌ |
| airis-web-research | 18 | 6 | 66.7% | ❌ |

### airis-browser-automation

**File**: `skills/airis-browser-automation/SKILL.md`

**Line 719**: `playwright:browser_navigate`
- ⚠️ Missing required: `url`

**Line 822**: `playwright:browser_navigate`
- ⚠️ Missing required: `url`

**Line 1077**: `playwright:browser_navigate`
- ⚠️ Missing required: `url`

### airis-code-search

**File**: `skills/airis-code-search/SKILL.md`

**Line 812**: `serena:find_symbol`
- ❌ Wrong parameter: `name`
- ✅ Correct parameter: `name_path_pattern`

**Line 812**: `serena:find_symbol`
- ⚠️ Missing required: `name_path_pattern`

**Line 990**: `serena:find_symbol`
- ❌ Wrong parameter: `name`
- ✅ Correct parameter: `name_path_pattern`

**Line 990**: `serena:find_symbol`
- ⚠️ Missing required: `name_path_pattern`

**Line 1042**: `serena:find_symbol`
- ❌ Wrong parameter: `name`
- ✅ Correct parameter: `name_path_pattern`

**Line 1042**: `serena:find_symbol`
- ⚠️ Missing required: `name_path_pattern`

### airis-knowledge-mgmt

**File**: `skills/airis-knowledge-mgmt/SKILL.md`

**Line 228**: `serena:write_memory`
- ❌ Wrong parameter: `filename`
- ✅ Correct parameter: `memory_file_name, content`

**Line 228**: `serena:write_memory`
- ⚠️ Missing required: `memory_file_name`

**Line 1146**: `serena:write_memory`
- ⚠️ Missing required: `content`

### airis-ui-generation

**File**: `skills/airis-ui-generation/SKILL.md`

**Line 70**: `magic:generate_ui`
- ⚠️ Missing required: `prompt`

**Line 70**: `magic:generate_ui`
- ⚠️ Missing required: `content`

**Line 143**: `magic:generate_ui`
- ⚠️ Missing required: `prompt`

**Line 143**: `magic:generate_ui`
- ⚠️ Missing required: `content`

**Line 440**: `magic:generate_ui`
- ⚠️ Missing required: `prompt`

**Line 440**: `magic:generate_ui`
- ⚠️ Missing required: `content`

**Line 519**: `magic:generate_ui`
- ⚠️ Missing required: `prompt`

**Line 519**: `magic:generate_ui`
- ⚠️ Missing required: `content`

**Line 561**: `magic:generate_ui`
- ⚠️ Missing required: `prompt`

**Line 561**: `magic:generate_ui`
- ⚠️ Missing required: `content`

**Line 644**: `magic:generate_ui`
- ⚠️ Missing required: `prompt`

**Line 644**: `magic:generate_ui`
- ⚠️ Missing required: `absolutePathToCurrentFile`

**Line 644**: `magic:generate_ui`
- ⚠️ Missing required: `content`

**Line 741**: `magic:generate_ui`
- ⚠️ Missing required: `prompt`

**Line 741**: `magic:generate_ui`
- ⚠️ Missing required: `content`

**Line 771**: `magic:generate_ui`
- ⚠️ Missing required: `prompt`

**Line 771**: `magic:generate_ui`
- ⚠️ Missing required: `content`

**Line 894**: `magic:generate_ui`
- ⚠️ Missing required: `prompt`

**Line 894**: `magic:generate_ui`
- ⚠️ Missing required: `content`

### airis-web-research

**File**: `skills/airis-web-research/SKILL.md`

**Line 142**: `serena:write_memory`
- ❌ Wrong parameter: `filename`
- ✅ Correct parameter: `memory_file_name, content`

**Line 142**: `serena:write_memory`
- ⚠️ Missing required: `memory_file_name`

**Line 389**: `serena:write_memory`
- ⚠️ Missing required: `content`

**Line 741**: `serena:write_memory`
- ⚠️ Missing required: `memory_file_name`

**Line 741**: `serena:write_memory`
- ⚠️ Missing required: `content`

**Line 985**: `serena:write_memory`
- ⚠️ Missing required: `content`

