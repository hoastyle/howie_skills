---
name: commit
description: 智能 git commit 助手。自动分析 staged changes，检测项目历史提交语言风格，生成符合规范的 commit message 并直接执行提交。优先遵循项目 CLAUDE.md 中定义的提交格式；若无定义，使用 Conventional Commits 标准。body 始终必填。适用场景：用户说"帮我提交"、"commit 一下"、"git commit"、"提交代码"等。
---

# Commit

智能分析变更，生成信息充分、格式标准的 commit message，直接执行提交。

---

## 工作流程

### Step 1：检测格式规范

读取项目根目录 `CLAUDE.md`，搜索以下关键词：`commit`、`提交`、`git message`、`conventional`。

- **CLAUDE.md 不存在** → 直接使用本 skill 的默认规范
- **存在但无明确格式定义** → 使用本 skill 的默认规范
- **找到明确格式定义** → 使用项目规范（优先级最高）

```bash
cat CLAUDE.md 2>/dev/null | grep -A 20 -i "commit\|提交\|git message"
```

---

### Step 2：检测语言风格

读取最近 10 条提交，统计中文字符占比。

```bash
git log --oneline -10
```

**判断规则**：
- 历史提交中中文字符 > 30% → 使用**中文**
- 否则 → 使用**英文**

---

### Step 3：分析 staged changes

```bash
git diff --staged --stat        # 文件列表和变更量
git diff --staged               # 具体内容
```

若 staged 为空，**停止执行**，提示用户先 `git add` 后再重试。

分析要点：
- 变更了哪些文件/模块 → 推断 `scope`
- 变更的性质（新增/修复/重构）→ 推断 `type`
- 变更的核心逻辑 → 生成 `subject` 和 `body`

---

### Step 4：生成 commit message

按以下格式生成，**body 始终必填**：

```
<type>(<scope>): <subject>

<body>

[footer]
```

生成后**直接执行提交**：

```bash
git commit -m "<type>(<scope>): <subject>

<body>

[footer]"
```

---

## 默认格式规范

### 完整格式

```
<type>(<scope>): <subject>
<空行>
<body>
<空行>
[footer]
```

### type 枚举

| type | 用途 | 来源 |
|------|------|------|
| `feat` | 新功能 | 官方规范（对应 SemVer MINOR） |
| `fix` | Bug 修复 | 官方规范（对应 SemVer PATCH） |
| `revert` | 回滚提交 | 官方规范示例 |
| `docs` | 文档变更 | Angular 约定 |
| `refactor` | 重构（不影响功能） | Angular 约定 |
| `chore` | 构建/依赖/配置/工具 | Angular 约定 |
| `test` | 测试相关 | Angular 约定 |
| `perf` | 性能优化 | Angular 约定 |

### 各字段规则

**type**：必填，从上表选择
- `revert` 的 subject 格式：`revert: <被回滚提交的原始 subject>`

**scope**：可选，填模块/组件/目录名
- 示例：`feat(auth):` `fix(gantry):` `chore(deps):`
- 变更集中在单一模块时填写，跨多模块可省略

**subject**：必填
- 动词开头（英文用祈使句：`add`/`fix`/`update`，中文用动词：`新增`/`修复`/`更新`）
- 不超过 72 字符
- 不加句号
- 描述"做了什么"

**body**：**始终必填**，包含以下三部分：
1. **背景**：改动的前因后果，为什么需要这次改动（问题是什么、触发原因）
2. **原理**：改动的技术方案和实现逻辑（怎么解决的、核心思路）
3. **影响**：改动带来的效果、副作用、注意事项

若上下文信息不足以完整描述以上三点，**必须主动向用户提问**，获取补充信息后再生成。
- 中英文与 subject 保持一致

**footer**：可选
- Breaking change 完整写法：`BREAKING CHANGE: <描述>`
- Breaking change 简写：在 type/scope 后加 `!`，如 `feat!: remove API` 或 `feat(auth)!: drop v1`
- 关联 issue：`Closes #123` 或 `Fixes #456`
- `revert` 提交需在 footer 注明被回滚的 commit SHA：`Refs: <sha1>, <sha2>`

---

## 示例

### 英文示例

```
feat(auth): add JWT token refresh mechanism

Background: Tokens had a fixed 1-hour expiry with no renewal mechanism.
Users were being logged out mid-session when the token expired, causing
data loss on long-running forms and frustrating UX reports.

Principle: Added a background timer that fires 5 minutes before expiry,
silently calls /auth/refresh, and replaces the stored token. No user
interaction required; falls back to logout only if refresh itself fails.

Impact: Eliminates unexpected session termination. Slight increase in
/auth/refresh traffic (~1 req/user/hour), within acceptable load limits.

Closes #234
```

```
fix(gantry): correct one-frame correction failure on direction change

Background: Field reports showed the lane keeper applying a wrong
correction on the first frame after a vehicle direction reversal,
causing a visible jerk in the output trajectory.

Principle: The correction state was reset immediately on direction change,
but the new direction's first frame was still processed against the stale
state before the reset took effect. Fixed by deferring the state reset to
execute before processing the second frame after direction change.

Impact: Eliminates the one-frame artifact. No change to steady-state
correction behavior or performance.
```

### 中文示例

```
feat(tos): 新增协议抽象层支持策略模式

背景：原有代码将具体协议实现硬编码在核心处理流程中，每次新增协议类型
都需要修改主逻辑，导致多次上线风险和回归测试成本持续增加。

原理：引入策略模式，将各协议实现封装为独立策略类，核心流程只依赖抽象
接口。新增协议只需实现接口并注册，无需改动主流程代码。

影响：后续扩展成本从"修改核心+全量回归"降为"新增策略类+单元测试"。
现有协议行为不变，已通过全量回归验证。
```

```
chore: 升级 pre-commit 依赖至 3.6.0

背景：CI 在 Python 3.12 环境下偶发 pre-commit hook 执行失败，
错误为 `AttributeError: module 'distutils'`，影响约 20% 的流水线运行。

原理：该问题为 pre-commit 3.4.x 的已知 bug，在 Python 3.12 移除
`distutils` 后触发。3.6.0 已修复，改用 `importlib.metadata` 替代。

影响：CI 稳定性恢复正常，同时 hook 执行速度提升约 15%。
```

### revert 示例

```
revert: add JWT token refresh mechanism

Background: The refresh mechanism introduced in commit a3f9c2e caused
token storms under high concurrency—multiple tabs triggered simultaneous
refresh calls, generating hundreds of redundant requests per user.

Principle: Rolling back to the previous stateless token behavior while
a proper mutex-based solution is designed. The revert restores the
original expiry-on-logout behavior.

Impact: Eliminates the token storm. Users will again experience session
expiry after 1 hour of inactivity until the fix is re-implemented.

Refs: a3f9c2e
```

---

## 常见陷阱

### 陷阱 1：subject 描述"做了什么"而非"是什么"

```
# ❌ 名词堆砌
feat: JWT token refresh mechanism

# ✅ 动词开头
feat: add JWT token refresh mechanism
```

### 陷阱 2：body 只重复 subject

```
# ❌ 无效 body
fix(auth): resolve login timeout issue

Fixed the login timeout issue in auth module.

# ✅ 包含背景、原理、影响
fix(auth): resolve login timeout issue

Background: Users in non-UTC timezones reported being logged out after
30 minutes despite the configured 1-hour session timeout.

Principle: Session expiry was calculated using server UTC time but
compared against client local time. Fixed by normalizing both timestamps
to UTC before comparison.

Impact: Resolves premature logout for all non-UTC timezones. No change
to session duration behavior for UTC users.
```

### 陷阱 3：staged 为空时直接提交

执行前先确认有 staged changes：
```bash
git diff --staged --stat
```
若为空，提示用户先 `git add`。

---

## 执行检查清单

执行提交前确认：
- [ ] 有 staged changes（`git diff --staged --stat` 非空）
- [ ] type 准确反映变更性质
- [ ] subject ≤ 72 字符，动词开头，无句号
- [ ] body 包含背景、原理、影响三部分
- [ ] 语言与项目历史一致

---

## 规范来源

本 skill 的格式标准基于以下规范：

- **Conventional Commits v1.0.0**（官方规范）：https://www.conventionalcommits.org/en/v1.0.0/
  - 定义了格式结构、`feat`/`fix` 两个核心 type、BREAKING CHANGE 语法、`!` 简写、`revert` 示例
- **Angular Commit Convention**（社区约定）：https://github.com/angular/angular/blob/main/CONTRIBUTING.md
  - 扩展了 `docs`、`refactor`、`chore`、`test`、`perf` 等 type

**本 skill 的扩展**（超出规范的有意加严）：
- body 由可选改为**始终必填**，且要求包含背景、原理、影响三部分
- 语言自动跟随项目历史提交风格

---

**版本**: 1.0.0
**最后更新**: 2026-02-23
