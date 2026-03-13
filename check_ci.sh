#!/bin/bash
# 完整的 CI 检查脚本（不修复，只检查）

echo "============================================================"
echo "🧪 完整的 CI 检查"
echo "============================================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

STEP=0
FAILED=0

# 日志函数
log_step() {
    STEP=$((STEP + 1))
    echo -e "${BLUE}[$STEP]${NC} $1"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# ============================================================
# 1. 前端检查
# ============================================================
log_step "前端检查"
echo "---"

cd frontend

# 检查 Lint
if npm run lint 2>&1 | grep -q "0 errors"; then
    log_success "前端 Lint 检查通过"
else
    log_error "前端 Lint 检查失败"
    FAILED=1
fi

# 检查构建
if npm run build > /dev/null 2>&1; then
    log_success "前端构建通过"
else
    log_error "前端构建失败"
    FAILED=1
fi

cd ..

echo ""

# ============================================================
# 2. 后端检查
# ============================================================
log_step "后端检查"
echo "---"

cd backend

# 检查语法
if python3 -m py_compile app/**/*.py > /dev/null 2>&1; then
    log_success "后端语法检查通过"
else
    log_error "后端语法检查失败"
    FAILED=1
fi

cd ..

echo ""

# ============================================================
# 3. 总结
# ============================================================
echo "============================================================"
echo "📊 检查总结"
echo "============================================================"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ 所有 CI 检查都通过了！${NC}"
    echo ""
    echo "🎉 main 分支代码质量良好！"
else
    echo -e "${RED}❌ 仍有 CI 检查失败${NC}"
    echo ""
    echo "请修复上面的错误"
fi

echo ""
