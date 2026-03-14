#!/bin/bash

# skill_security_check.sh
# Skill 安全检测脚本

set -e

SKILL_PATH="${1:-.}"
SKILL_NAME=$(basename "$SKILL_PATH")

if [ ! -d "$SKILL_PATH" ]; then
  echo "❌ 错误: 目录不存在: $SKILL_PATH"
  exit 1
fi

echo "=========================================="
echo "Skill 安全检测"
echo "=========================================="
echo "Skill: $SKILL_NAME"
echo "路径: $SKILL_PATH"
echo ""

# 初始化计数器
ISSUES=0
WARNINGS=0

# 1. 检查 SKILL.md
echo "[1/6] 检查 SKILL.md..."
if [ -f "$SKILL_PATH/SKILL.md" ]; then
  echo "✅ SKILL.md 存在"
else
  echo "❌ SKILL.md 不存在"
  ((ISSUES++))
fi
echo ""

# 2. 检查危险的系统调用
echo "[2/6] 检查危险的系统调用..."
DANGEROUS_CALLS=$(grep -r "exec\|eval\|system\|subprocess\|os.system\|shell=True" "$SKILL_PATH" 2>/dev/null | grep -v "node_modules" | wc -l)
if [ "$DANGEROUS_CALLS" -gt 0 ]; then
  echo "⚠️ 发现 $DANGEROUS_CALLS 个危险的系统调用"
  grep -r "exec\|eval\|system\|subprocess\|os.system\|shell=True" "$SKILL_PATH" 2>/dev/null | grep -v "node_modules" | head -5
  ((WARNINGS++))
else
  echo "✅ 无危险的系统调用"
fi
echo ""

# 3. 检查文件操作
echo "[3/6] 检查文件操作..."
FILE_OPS=$(grep -r "open\|write\|delete\|remove\|unlink" "$SKILL_PATH" 2>/dev/null | grep -v "node_modules" | wc -l)
if [ "$FILE_OPS" -gt 0 ]; then
  echo "⚠️ 发现 $FILE_OPS 个文件操作"
  ((WARNINGS++))
else
  echo "✅ 无危险的文件操作"
fi
echo ""

# 4. 检查网络操作
echo "[4/6] 检查网络操作..."
NETWORK_OPS=$(grep -r "http\|socket\|request\|fetch\|curl" "$SKILL_PATH" 2>/dev/null | grep -v "node_modules" | wc -l)
if [ "$NETWORK_OPS" -gt 0 ]; then
  echo "⚠️ 发现 $NETWORK_OPS 个网络操作"
  ((WARNINGS++))
else
  echo "✅ 无网络操作"
fi
echo ""

# 5. 检查依赖
echo "[5/6] 检查依赖..."
if [ -f "$SKILL_PATH/package.json" ]; then
  echo "Node.js 依赖检测..."
  cd "$SKILL_PATH"
  npm audit 2>&1 | grep -E "vulnerabilities|found" || echo "✅ 无已知漏洞"
  cd - > /dev/null
fi

if [ -f "$SKILL_PATH/requirements.txt" ]; then
  echo "Python 依赖检测..."
  echo "⚠️ 需要手动检查 (pip-audit 或 safety)"
fi
echo ""

# 6. 检查代码质量
echo "[6/6] 检查代码质量..."
if [ -f "$SKILL_PATH/package.json" ]; then
  echo "JavaScript 代码质量..."
  cd "$SKILL_PATH"
  npm run lint 2>&1 | head -10 || echo "✅ 无 lint 错误"
  cd - > /dev/null
fi
echo ""

# 总结
echo "=========================================="
echo "检测结果"
echo "=========================================="
echo "严重问题: $ISSUES"
echo "警告: $WARNINGS"
echo ""

if [ "$ISSUES" -gt 0 ]; then
  echo "❌ 检测失败: 发现 $ISSUES 个严重问题"
  exit 1
elif [ "$WARNINGS" -gt 0 ]; then
  echo "⚠️ 检测通过（有 $WARNINGS 个警告）"
  exit 0
else
  echo "✅ 检测通过"
  exit 0
fi
