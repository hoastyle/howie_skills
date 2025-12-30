#!/bin/bash
set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SKILLS_DIR="$HOME/.claude/skills"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo -e "${GREEN}🚀 安装 Howie AIRIS Skills...${NC}"
echo ""

# 检查是否已安装
if [ -d "$SKILLS_DIR" ]; then
    echo -e "${YELLOW}⚠️  Skills 目录已存在: $SKILLS_DIR${NC}"
    read -p "是否覆盖已有 skills? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}✖ 安装已取消${NC}"
        exit 1
    fi
fi

# 创建 skills 目录
mkdir -p "$SKILLS_DIR"
echo -e "${GREEN}✓${NC} 创建 skills 目录: $SKILLS_DIR"

# 安装每个 skill
skill_count=0
for skill in "$REPO_DIR/skills/"*; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")

        # 检查是否有 SKILL.md
        if [ ! -f "$skill/SKILL.md" ]; then
            echo -e "${YELLOW}⚠️  跳过 $skill_name (缺少 SKILL.md)${NC}"
            continue
        fi

        echo -e "${GREEN}✓${NC} 安装 $skill_name..."

        # 复制 skill 目录
        cp -r "$skill" "$SKILLS_DIR/$skill_name"

        ((skill_count++))
    fi
done

echo ""
echo -e "${GREEN}✅ 安装完成！${NC}"
echo -e "已安装 ${GREEN}$skill_count${NC} 个 skills 到 $SKILLS_DIR"
echo ""

# 列出已安装的 skills
echo -e "${GREEN}📚 已安装的 Skills:${NC}"
for skill in "$SKILLS_DIR/"*/SKILL.md; do
    if [ -f "$skill" ]; then
        skill_dir=$(dirname "$skill")
        skill_name=$(basename "$skill_dir")

        # 提取 skill description (从 YAML frontmatter)
        desc=$(grep "^description:" "$skill" | sed 's/description: "//; s/"$//' | head -c 80)
        echo -e "  ${GREEN}✓${NC} ${YELLOW}$skill_name${NC}"
        echo -e "    $desc..."
    fi
done

echo ""
echo -e "${GREEN}🎉 安装成功！${NC}"
echo ""
echo -e "使用方式:"
echo -e "  - 自动触发: Claude 会根据你的请求自动使用相应的 skill"
echo -e "  - 手动调用: 在请求中明确指定 skill 名称"
echo ""
echo -e "示例:"
echo -e '  "帮我研究一下 React Server Components"'
echo -e "  ${GREEN}→${NC} 自动触发 airis-web-research skill"
echo ""
