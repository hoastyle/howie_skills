#!/bin/bash
set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SKILLS_DIR="$HOME/.claude/skills"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo -e "${GREEN}🚀 Howie AIRIS Skills 智能安装器${NC}"
echo -e "${BLUE}版本: v2.0 (增量式安装)${NC}"
echo ""

# 创建 skills 目录
mkdir -p "$SKILLS_DIR"

# 扫描现有和新的 skills
declare -A existing_skills
declare -A new_skills
declare -A outdated_skills

# 检测已安装的 skills
if [ -d "$SKILLS_DIR" ]; then
    for skill_dir in "$SKILLS_DIR/"*/; do
        if [ -f "${skill_dir}SKILL.md" ]; then
            skill_name=$(basename "$skill_dir")
            existing_skills[$skill_name]=1
        fi
    done
fi

# 扫描仓库中的 skills
for skill in "$REPO_DIR/skills/"*; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")

        # 检查是否有 SKILL.md
        if [ ! -f "$skill/SKILL.md" ]; then
            continue
        fi

        if [ -z "${existing_skills[$skill_name]}" ]; then
            # 新 skill
            new_skills[$skill_name]=1
        else
            # 检查是否有更新（比较文件修改时间）
            repo_mtime=$(stat -c %Y "$skill/SKILL.md" 2>/dev/null || stat -f %m "$skill/SKILL.md" 2>/dev/null)
            installed_mtime=$(stat -c %Y "$SKILLS_DIR/$skill_name/SKILL.md" 2>/dev/null || stat -f %m "$SKILLS_DIR/$skill_name/SKILL.md" 2>/dev/null)

            if [ "$repo_mtime" -gt "$installed_mtime" ]; then
                outdated_skills[$skill_name]=1
            fi
        fi
    fi
done

# 显示安装状态摘要
echo -e "${BLUE}📊 安装状态分析:${NC}"
echo ""

total_in_repo=0
for skill in "$REPO_DIR/skills/"*/; do
    if [ -f "${skill}SKILL.md" ]; then
        total_in_repo=$((total_in_repo + 1))
    fi
done

echo -e "  仓库中的 Skills: ${GREEN}${total_in_repo}${NC}"
echo -e "  已安装的 Skills: ${GREEN}${#existing_skills[@]}${NC}"
echo -e "  待安装的新 Skills: ${YELLOW}${#new_skills[@]}${NC}"
echo -e "  可更新的 Skills: ${YELLOW}${#outdated_skills[@]}${NC}"
echo ""

# 如果没有任何操作需要执行
if [ ${#new_skills[@]} -eq 0 ] && [ ${#outdated_skills[@]} -eq 0 ]; then
    echo -e "${GREEN}✅ 所有 Skills 已是最新版本！${NC}"
    echo ""
    echo -e "已安装的 Skills:"
    for skill_name in "${!existing_skills[@]}"; do
        desc=$(grep "^description:" "$SKILLS_DIR/$skill_name/SKILL.md" | sed 's/description: "//; s/"$//' | head -c 60)
        echo -e "  ${GREEN}✓${NC} ${YELLOW}$skill_name${NC}"
        echo -e "    $desc..."
    done
    exit 0
fi

# 显示待安装和待更新的 skills
if [ ${#new_skills[@]} -gt 0 ]; then
    echo -e "${YELLOW}📦 待安装的新 Skills (${#new_skills[@]} 个):${NC}"
    for skill_name in "${!new_skills[@]}"; do
        desc=$(grep "^description:" "$REPO_DIR/skills/$skill_name/SKILL.md" | sed 's/description: "//; s/"$//' | head -c 60)
        echo -e "  ${GREEN}[新]${NC} ${YELLOW}$skill_name${NC}"
        echo -e "      $desc..."
    done
    echo ""
fi

if [ ${#outdated_skills[@]} -gt 0 ]; then
    echo -e "${YELLOW}🔄 可更新的 Skills (${#outdated_skills[@]} 个):${NC}"
    for skill_name in "${!outdated_skills[@]}"; do
        desc=$(grep "^description:" "$REPO_DIR/skills/$skill_name/SKILL.md" | sed 's/description: "//; s/"$//' | head -c 60)
        echo -e "  ${BLUE}[更新]${NC} ${YELLOW}$skill_name${NC}"
        echo -e "        $desc..."
    done
    echo ""
fi

# 交互式选择
echo -e "${BLUE}请选择操作模式:${NC}"
echo -e "  ${GREEN}1${NC}. 安装/更新所有 (推荐)"
echo -e "  ${GREEN}2${NC}. 仅安装新 Skills"
echo -e "  ${GREEN}3${NC}. 仅更新已有 Skills"
echo -e "  ${GREEN}4${NC}. 逐个选择"
echo -e "  ${GREEN}5${NC}. 取消"
echo ""
read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        # 安装/更新所有
        mode="all"
        ;;
    2)
        # 仅安装新的
        mode="new"
        ;;
    3)
        # 仅更新
        mode="update"
        ;;
    4)
        # 逐个选择
        mode="interactive"
        ;;
    5|*)
        echo -e "${RED}✖ 安装已取消${NC}"
        exit 0
        ;;
esac

echo ""
echo -e "${GREEN}开始安装...${NC}"
echo ""

installed_count=0
updated_count=0
skipped_count=0

# 安装函数
install_skill() {
    local skill_name=$1
    local skill_path="$REPO_DIR/skills/$skill_name"
    local is_update=$2

    if [ "$is_update" = "update" ]; then
        echo -e "${BLUE}🔄 更新${NC} $skill_name..."
        # 备份旧版本
        if [ -d "$SKILLS_DIR/$skill_name.backup" ]; then
            rm -rf "$SKILLS_DIR/$skill_name.backup"
        fi
        mv "$SKILLS_DIR/$skill_name" "$SKILLS_DIR/$skill_name.backup"
        updated_count=$((updated_count + 1))
    else
        echo -e "${GREEN}📦 安装${NC} $skill_name..."
        installed_count=$((installed_count + 1))
    fi

    # 复制 skill 目录
    cp -r "$skill_path" "$SKILLS_DIR/$skill_name"
    echo -e "   ${GREEN}✓${NC} 完成"
}

# 根据模式执行安装
if [ "$mode" = "all" ]; then
    # 安装所有新 skills
    for skill_name in "${!new_skills[@]}"; do
        install_skill "$skill_name" "new"
    done

    # 更新所有旧 skills
    for skill_name in "${!outdated_skills[@]}"; do
        install_skill "$skill_name" "update"
    done

elif [ "$mode" = "new" ]; then
    # 仅安装新的
    for skill_name in "${!new_skills[@]}"; do
        install_skill "$skill_name" "new"
    done

elif [ "$mode" = "update" ]; then
    # 仅更新
    for skill_name in "${!outdated_skills[@]}"; do
        install_skill "$skill_name" "update"
    done

elif [ "$mode" = "interactive" ]; then
    # 逐个询问
    echo -e "${BLUE}逐个选择模式:${NC}"
    echo ""

    # 处理新 skills
    for skill_name in "${!new_skills[@]}"; do
        desc=$(grep "^description:" "$REPO_DIR/skills/$skill_name/SKILL.md" | sed 's/description: "//; s/"$//' | head -c 60)
        echo -e "${GREEN}[新]${NC} ${YELLOW}$skill_name${NC}"
        echo -e "     $desc..."
        read -p "     安装此 skill? (Y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            install_skill "$skill_name" "new"
        else
            skipped_count=$((skipped_count + 1))
            echo -e "   ${YELLOW}⊘${NC} 已跳过"
        fi
        echo ""
    done

    # 处理需要更新的 skills
    for skill_name in "${!outdated_skills[@]}"; do
        desc=$(grep "^description:" "$REPO_DIR/skills/$skill_name/SKILL.md" | sed 's/description: "//; s/"$//' | head -c 60)
        echo -e "${BLUE}[更新]${NC} ${YELLOW}$skill_name${NC}"
        echo -e "       $desc..."
        read -p "       更新此 skill? (Y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            install_skill "$skill_name" "update"
        else
            skipped_count=$((skipped_count + 1))
            echo -e "   ${YELLOW}⊘${NC} 已跳过"
        fi
        echo ""
    done
fi

# 安装摘要
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ 安装完成！${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  ${GREEN}新安装:${NC} $installed_count 个"
echo -e "  ${BLUE}已更新:${NC} $updated_count 个"
if [ $skipped_count -gt 0 ]; then
    echo -e "  ${YELLOW}已跳过:${NC} $skipped_count 个"
fi
echo ""

# 列出所有已安装的 skills
total_installed=0
echo -e "${GREEN}📚 当前已安装的 Skills:${NC}"
echo ""
for skill_dir in "$SKILLS_DIR/"*/; do
    if [ -f "${skill_dir}SKILL.md" ]; then
        skill_name=$(basename "$skill_dir")
        desc=$(grep "^description:" "${skill_dir}SKILL.md" | sed 's/description: "//; s/"$//' | head -c 60)

        # 检查是否是新安装或更新的
        if [ ! -z "${new_skills[$skill_name]}" ]; then
            status_label="${GREEN}[新安装]${NC}"
        elif [ ! -z "${outdated_skills[$skill_name]}" ]; then
            status_label="${BLUE}[已更新]${NC}"
        else
            status_label="${YELLOW}[已有]${NC}"
        fi

        echo -e "  ${status_label} ${YELLOW}$skill_name${NC}"
        echo -e "            $desc..."
        echo ""
        total_installed=$((total_installed + 1))
    fi
done

echo -e "${GREEN}总计: $total_installed 个 Skills${NC}"
echo ""

# 清理备份提示
backup_count=$(find "$SKILLS_DIR" -name "*.backup" -type d 2>/dev/null | wc -l)
if [ $backup_count -gt 0 ]; then
    echo -e "${YELLOW}💡 提示: 发现 $backup_count 个备份目录${NC}"
    echo -e "   如果新版本工作正常，可以删除备份:"
    echo -e "   ${BLUE}rm -rf ~/.claude/skills/*.backup${NC}"
    echo ""
fi

# 使用说明
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎯 使用方式:${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  ${GREEN}自动触发:${NC} Claude 会根据你的请求自动使用相应的 skill"
echo -e "  ${GREEN}手动调用:${NC} 在请求中明确指定 skill 名称"
echo ""
echo -e "${YELLOW}示例:${NC}"
echo -e '  "帮我研究一下 React Server Components"'
echo -e "  ${GREEN}→${NC} 自动触发 airis-web-research skill"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}📖 更多信息:${NC}"
echo -e "  - 快速入门: ${BLUE}GETTING_STARTED.md${NC}"
echo -e "  - 安装指南: ${BLUE}docs/INSTALLATION_GUIDE.md${NC}"
echo -e "  - 工作流示例: ${BLUE}docs/WORKFLOW_EXAMPLES.md${NC}"
echo ""
