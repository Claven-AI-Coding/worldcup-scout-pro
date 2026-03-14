#!/bin/bash

# manage_skills.sh
# Skill 管理工作流

set -e

SKILL_NAME="${1:-}"
SKILL_URL="${2:-}"

if [ -z "$SKILL_NAME" ] || [ -z "$SKILL_URL" ]; then
  echo "用法: $0 <skill_name> <skill_url>"
  echo ""
  echo "示例:"
  echo "  $0 weather https://github.com/openclaw/skill-weather.git"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="/tmp/skill_check_$SKILL_NAME"
SKILLS_DIR="/usr/lib/node_modules/openclaw/skills"

echo "=========================================="
echo "Skill 管理工作流"
echo "=========================================="
echo ""

# 步骤 1: 下载
echo "📥 步骤 1: 下载 Skill..."
echo "名称: $SKILL_NAME"
echo "URL: $SKILL_URL"
echo ""

rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

if ! git clone "$SKILL_URL" . 2>&1 | tail -5; then
  echo "❌ 下载失败"
  exit 1
fi

echo "✅ 下载完成"
echo ""

# 步骤 2: 安全检测
echo "🔒 步骤 2: 安全检测..."
echo ""

if ! bash "$SCRIPT_DIR/skill_security_check.sh" "$TEMP_DIR"; then
  echo ""
  echo "❌ 安全检测失败"
  echo "请查看上面的错误信息"
  exit 1
fi

echo ""
echo "✅ 安全检测通过"
echo ""

# 步骤 3: 用户确认
echo "❓ 步骤 3: 确认安装?"
echo ""
echo "Skill 信息:"
if [ -f "$TEMP_DIR/SKILL.md" ]; then
  head -10 "$TEMP_DIR/SKILL.md"
fi
echo ""
read -p "是否继续安装? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "❌ 已取消"
  exit 1
fi
echo ""

# 步骤 4: 安装
echo "📦 步骤 4: 安装 Skill..."

if [ ! -f "$TEMP_DIR/SKILL.md" ]; then
  echo "❌ 错误: SKILL.md 不存在"
  exit 1
fi

mkdir -p "$SKILLS_DIR/$SKILL_NAME"
cp -r "$TEMP_DIR"/* "$SKILLS_DIR/$SKILL_NAME/"

echo "✅ Skill 已安装到: $SKILLS_DIR/$SKILL_NAME"
echo ""

# 步骤 5: 验证
echo "✔️ 步骤 5: 验证安装..."

if [ -f "$SKILLS_DIR/$SKILL_NAME/SKILL.md" ]; then
  echo "✅ 验证成功"
else
  echo "❌ 验证失败"
  exit 1
fi
echo ""

# 步骤 6: 清理
echo "🧹 步骤 6: 清理临时文件..."
rm -rf "$TEMP_DIR"
echo "✅ 清理完成"
echo ""

echo "=========================================="
echo "✅ Skill 安装完成"
echo "=========================================="
echo ""
echo "Skill 已安装: $SKILL_NAME"
echo "位置: $SKILLS_DIR/$SKILL_NAME"
echo ""
echo "使用方法:"
echo "  openclaw skills list"
echo "  openclaw skills enable $SKILL_NAME"
