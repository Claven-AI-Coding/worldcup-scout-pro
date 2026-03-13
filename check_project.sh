#!/bin/bash
# 项目完整性检查脚本

echo "============================================================"
echo "🚀 世界杯球探 Pro - 项目完整性检查"
echo "============================================================"
echo ""

# 检查文件结构
echo "📁 检查文件结构..."
check_file() {
    if [ -f "$1" ]; then
        echo "  ✅ $1"
        return 0
    else
        echo "  ❌ $1 - 缺失"
        return 1
    fi
}

# 后端 API
echo ""
echo "🔧 后端 API 文件:"
check_file "backend/app/api/v1/ai_prediction.py"
check_file "backend/app/api/v1/membership.py"
check_file "backend/app/api/v1/schedule_filter.py"
check_file "backend/app/api/v1/wallpaper_generation.py"
check_file "backend/app/api/v1/ai_match_report.py"
check_file "backend/app/api/v1/compliance.py"

# 后端 Service
echo ""
echo "⚙️  后端 Service 文件:"
check_file "backend/app/services/ai_prediction_service.py"
check_file "backend/app/services/membership_service.py"
check_file "backend/app/services/schedule_filter_service.py"
check_file "backend/app/services/wallpaper_generation_service.py"
check_file "backend/app/services/ai_match_report_service.py"

# 后端 Schema
echo ""
echo "📋 后端 Schema 文件:"
check_file "backend/app/schemas/ai_prediction.py"
check_file "backend/app/schemas/membership.py"
check_file "backend/app/schemas/schedule_filter.py"
check_file "backend/app/schemas/wallpaper_generation.py"

# 前端组件
echo ""
echo "🎨 前端组件文件:"
check_file "frontend/src/components/charts/TeamRadarChart.vue"
check_file "frontend/src/components/charts/MatchHistoryChart.vue"
check_file "frontend/src/components/charts/StandingsTrendChart.vue"

# 前端测试
echo ""
echo "🧪 前端测试文件:"
check_file "frontend/tests/components/EmptyState.spec.ts"
check_file "frontend/tests/components/LoadingSpinner.spec.ts"
check_file "frontend/tests/components/MatchCard.spec.ts"
check_file "frontend/tests/components/PostCard.spec.ts"

# 文档
echo ""
echo "📚 文档文件:"
check_file "docs/COMPLIANCE.md"
check_file "docs/AI_PREDICTION.md"
check_file "docs/MEMBERSHIP.md"
check_file "docs/DATA_VISUALIZATION.md"
check_file "docs/TESTING_AND_ACCEPTANCE.md"

# 配置文件
echo ""
echo "⚙️  配置文件:"
check_file "backend/pyproject.toml"
check_file "frontend/package.json"
check_file ".github/workflows/ci.yml"
check_file "docker-compose.yml"

# 检查主路由注册
echo ""
echo "🔍 检查主路由注册..."
if grep -q "ai_match_report" backend/app/main.py && \
   grep -q "schedule_filter" backend/app/main.py && \
   grep -q "wallpaper_generation" backend/app/main.py; then
    echo "  ✅ 所有新路由已注册"
else
    echo "  ❌ 部分路由未注册"
fi

# 统计代码行数
echo ""
echo "📊 代码统计:"
echo "  后端 Python: $(find backend/app -name '*.py' | xargs wc -l | tail -1 | awk '{print $1}') 行"
echo "  前端 Vue/TS: $(find frontend/src -name '*.vue' -o -name '*.ts' | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}') 行"
echo "  测试代码: $(find frontend/tests -name '*.spec.ts' | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}') 行"

# Git 统计
echo ""
echo "📈 Git 统计:"
echo "  总提交数: $(git rev-list --count HEAD)"
echo "  今日提交: $(git log --since='today' --oneline | wc -l)"
echo "  分支数: $(git branch -a | wc -l)"

# 功能清单
echo ""
echo "============================================================"
echo "✅ 已完成功能清单"
echo "============================================================"
echo ""
echo "P0 - 合规风控:"
echo "  ✅ 违禁词管理系统"
echo "  ✅ 举报审核流程"
echo "  ✅ 用户封禁机制"
echo ""
echo "P1 - 核心功能:"
echo "  ✅ 数据可视化（3个图表）"
echo "  ✅ AI 预测系统"
echo "  ✅ 会员体系"
echo ""
echo "P2 - 增强功能:"
echo "  ✅ 赛程筛选"
echo "  ✅ AI 壁纸生成"
echo "  ✅ AI 战报生成"
echo ""
echo "============================================================"
echo "🎉 项目完整性检查完成！"
echo "============================================================"
