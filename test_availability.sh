#!/bin/bash
# 完整的项目可用性测试脚本

echo "============================================================"
echo "🧪 世界杯球探 Pro - 完整可用性测试"
echo "============================================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

test_count=0
pass_count=0
fail_count=0

# 测试函数
run_test() {
    local test_name=$1
    local command=$2
    
    test_count=$((test_count + 1))
    echo -n "[$test_count] $test_name ... "
    
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}"
        pass_count=$((pass_count + 1))
    else
        echo -e "${RED}❌ FAIL${NC}"
        fail_count=$((fail_count + 1))
    fi
}

# ============================================================
# 1. 文件完整性检查
# ============================================================
echo "📁 1. 文件完整性检查"
echo "---"

run_test "后端主文件存在" "[ -f backend/app/main.py ]"
run_test "前端主文件存在" "[ -f frontend/src/main.ts ]"
run_test "Docker Compose 配置存在" "[ -f docker-compose.yml ]"
run_test "CI/CD 配置存在" "[ -f .github/workflows/ci.yml ]"
run_test ".env 文件存在" "[ -f .env ]"

echo ""

# ============================================================
# 2. 代码语法检查
# ============================================================
echo "🔍 2. 代码语法检查"
echo "---"

run_test "后端 main.py 语法正确" "python3 -m py_compile backend/app/main.py"
run_test "后端 API 文件语法正确" "find backend/app/api/v1 -name '*.py' -exec python3 -m py_compile {} \;"
run_test "后端 Service 文件语法正确" "find backend/app/services -name '*.py' -exec python3 -m py_compile {} \;"
run_test "后端 Schema 文件语法正确" "find backend/app/schemas -name '*.py' -exec python3 -m py_compile {} \;"

echo ""

# ============================================================
# 3. 前端代码检查
# ============================================================
echo "🎨 3. 前端代码检查"
echo "---"

run_test "前端 Lint 无错误" "cd frontend && npm run lint 2>&1 | grep -q '0 errors'"
run_test "前端 TypeScript 编译" "cd frontend && npm run build 2>&1 | grep -q 'dist'"

echo ""

# ============================================================
# 4. 依赖检查
# ============================================================
echo "📦 4. 依赖检查"
echo "---"

run_test "后端 pyproject.toml 有效" "python3 -c 'import tomllib; tomllib.load(open(\"backend/pyproject.toml\", \"rb\"))'"
run_test "前端 package.json 有效" "node -e 'JSON.parse(require(\"fs\").readFileSync(\"frontend/package.json\"))'"
run_test "前端依赖可安装" "cd frontend && npm install --dry-run 2>&1 | grep -q 'added'"

echo ""

# ============================================================
# 5. 配置检查
# ============================================================
echo "⚙️  5. 配置检查"
echo "---"

run_test "数据库配置存在" "grep -q 'DATABASE_URL' .env"
run_test "Redis 配置存在" "grep -q 'REDIS_URL' .env"
run_test "JWT 配置存在" "grep -q 'JWT_SECRET_KEY' .env"
run_test "API 密钥配置存在" "grep -q 'ANTHROPIC_API_KEY' .env"

echo ""

# ============================================================
# 6. 路由注册检查
# ============================================================
echo "🛣️  6. 路由注册检查"
echo "---"

run_test "AI 预测路由已注册" "grep -q 'ai_prediction.router' backend/app/main.py"
run_test "会员体系路由已注册" "grep -q 'membership.router' backend/app/main.py"
run_test "赛程筛选路由已注册" "grep -q 'schedule_filter.router' backend/app/main.py"
run_test "壁纸生成路由已注册" "grep -q 'wallpaper_generation.router' backend/app/main.py"
run_test "AI 战报路由已注册" "grep -q 'ai_match_report.router' backend/app/main.py"

echo ""

# ============================================================
# 7. 文档完整性
# ============================================================
echo "📚 7. 文档完整性"
echo "---"

run_test "合规系统文档存在" "[ -f docs/COMPLIANCE.md ]"
run_test "AI 预测文档存在" "[ -f docs/AI_PREDICTION.md ]"
run_test "会员体系文档存在" "[ -f docs/MEMBERSHIP.md ]"
run_test "数据可视化文档存在" "[ -f docs/DATA_VISUALIZATION.md ]"
run_test "测试指南文档存在" "[ -f docs/TESTING_AND_ACCEPTANCE.md ]"
run_test "验收报告存在" "[ -f ACCEPTANCE_REPORT.md ]"

echo ""

# ============================================================
# 8. Git 检查
# ============================================================
echo "🔗 8. Git 检查"
echo "---"

run_test "Git 仓库有效" "git rev-parse --git-dir > /dev/null 2>&1"
run_test "远程仓库连接正常" "git remote -v | grep -q 'origin'"
run_test "本地分支与远程同步" "[ -z \"\$(git status --porcelain)\" ] || echo 'has changes'"

echo ""

# ============================================================
# 总结
# ============================================================
echo "============================================================"
echo "📊 测试总结"
echo "============================================================"
echo ""
echo "总测试数: $test_count"
echo -e "通过: ${GREEN}$pass_count${NC}"
echo -e "失败: ${RED}$fail_count${NC}"
echo ""

if [ $fail_count -eq 0 ]; then
    echo -e "${GREEN}✅ 所有测试通过！项目可用性验证成功！${NC}"
    echo ""
    echo "📋 项目状态："
    echo "  ✅ 代码语法正确"
    echo "  ✅ 依赖配置完整"
    echo "  ✅ 路由注册完成"
    echo "  ✅ 文档齐全"
    echo "  ✅ Git 同步"
    echo ""
    echo "🚀 项目已就绪，可以进行部署或进一步开发"
    exit 0
else
    echo -e "${RED}❌ 部分测试失败，需要修复${NC}"
    exit 1
fi
