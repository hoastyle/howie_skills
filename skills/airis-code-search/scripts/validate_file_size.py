#!/usr/bin/env python3
"""
文件大小验证工具

检查文件是否适合 MorphLLM 编辑（< 2000 行）

用法:
    python validate_file_size.py <file_path>
    python validate_file_size.py src/services/UserService.ts
"""

import sys
import os


def count_lines(file_path):
    """统计文件行数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    except UnicodeDecodeError:
        # 尝试其他编码
        with open(file_path, 'r', encoding='latin-1') as f:
            return sum(1 for _ in f)


def validate_file(file_path, max_lines=2000):
    """验证文件大小"""
    if not os.path.exists(file_path):
        print(f"❌ 错误: 文件不存在: {file_path}")
        return False

    if not os.path.isfile(file_path):
        print(f"❌ 错误: 不是文件: {file_path}")
        return False

    try:
        line_count = count_lines(file_path)
        file_size = os.path.getsize(file_path)
        file_size_kb = file_size / 1024

        print(f"\n📊 文件信息:")
        print(f"  路径: {file_path}")
        print(f"  行数: {line_count:,} 行")
        print(f"  大小: {file_size_kb:.2f} KB")
        print()

        if line_count <= max_lines:
            percentage = (line_count / max_lines) * 100
            print(f"✅ 文件大小合适 ({percentage:.1f}% of limit)")
            print(f"   可以使用 MorphLLM 进行编辑")
            return True
        else:
            overflow = line_count - max_lines
            print(f"❌ 文件过大 (超出 {overflow:,} 行)")
            print(f"   MorphLLM 限制: {max_lines:,} 行")
            print()
            print("💡 建议:")
            print("   1. 拆分文件为多个模块")
            print("   2. 使用传统编辑工具（Edit tool）")
            print("   3. 仅编辑文件的一部分")
            return False

    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("用法: python validate_file_size.py <file_path>")
        print()
        print("示例:")
        print("  python validate_file_size.py src/services/UserService.ts")
        print("  python validate_file_size.py components/Header.tsx")
        sys.exit(1)

    file_path = sys.argv[1]
    max_lines = 2000

    # 支持自定义限制（可选参数）
    if len(sys.argv) >= 3:
        try:
            max_lines = int(sys.argv[2])
        except ValueError:
            print(f"❌ 错误: 无效的行数限制: {sys.argv[2]}")
            sys.exit(1)

    result = validate_file(file_path, max_lines)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
