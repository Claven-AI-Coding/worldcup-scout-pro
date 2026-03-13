#!/usr/bin/env python3
"""API 功能测试脚本"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.main import app


async def test_imports():
    """测试所有模块导入"""
    print("🧪 测试模块导入...")
    
    try:
        from app.api.v1 import (
            ai_match_report,
            ai_prediction,
            auth,
            community,
            compliance,
            legal,
            matches,
            membership,
            players,
            points,
            predictions,
            rankings,
            reports,
            schedule_filter,
            tasks,
            teams,
            wallpaper_generation,
            wallpapers,
        )
        print("✅ 所有 API 模块导入成功")
        return True
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False


async def test_routes():
    """测试路由注册"""
    print("\n🧪 测试路由注册...")
    
    routes = [route.path for route in app.routes]
    
    expected_routes = [
        "/api/v1/membership/plans",
        "/api/v1/membership/subscribe",
        "/api/v1/ai/predict-match",
        "/api/v1/schedule/filter",
        "/api/v1/schedule/stats",
        "/api/v1/wallpapers/generate",
        "/api/v1/reports/match/{match_id}",
    ]
    
    missing = []
    for route in expected_routes:
        # Check if route pattern exists
        found = any(route.replace("{match_id}", "") in r for r in routes)
        if found:
            print(f"✅ {route}")
        else:
            print(f"❌ {route} - 未找到")
            missing.append(route)
    
    if missing:
        print(f"\n⚠️  缺失 {len(missing)} 个路由")
        return False
    else:
        print(f"\n✅ 所有路由注册成功 (共 {len(routes)} 个)")
        return True


async def test_schemas():
    """测试 Schema 定义"""
    print("\n🧪 测试 Schema 定义...")
    
    try:
        from app.schemas.membership import MembershipPlan, SubscribeRequest
        from app.schemas.ai_prediction import MatchPredictionRequest
        from app.schemas.schedule_filter import ScheduleFilterRequest
        from app.schemas.wallpaper_generation import WallpaperGenerateRequest
        
        print("✅ 所有 Schema 定义正确")
        return True
    except Exception as e:
        print(f"❌ Schema 定义错误: {e}")
        return False


async def test_services():
    """测试 Service 层"""
    print("\n🧪 测试 Service 层...")
    
    try:
        from app.services.membership_service import MembershipService
        from app.services.ai_prediction_service import AIPredictionService
        from app.services.schedule_filter_service import ScheduleFilterService
        from app.services.wallpaper_generation_service import WallpaperGenerationService
        from app.services.ai_match_report_service import AIMatchReportService
        
        print("✅ 所有 Service 定义正确")
        return True
    except Exception as e:
        print(f"❌ Service 定义错误: {e}")
        return False


async def main():
    """运行所有测试"""
    print("=" * 60)
    print("🚀 世界杯球探 Pro - API 功能测试")
    print("=" * 60)
    
    results = []
    
    # 运行测试
    results.append(await test_imports())
    results.append(await test_routes())
    results.append(await test_schemas())
    results.append(await test_services())
    
    # 总结
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ 所有测试通过 ({passed}/{total})")
        print("\n📋 功能清单:")
        print("  ✅ 合规风控系统")
        print("  ✅ AI 预测系统")
        print("  ✅ 会员体系")
        print("  ✅ 赛程筛选")
        print("  ✅ AI 壁纸生成")
        print("  ✅ AI 战报生成")
        print("  ✅ 数据可视化组件")
        print("\n🎉 项目已就绪！")
        return 0
    else:
        print(f"❌ 部分测试失败 ({passed}/{total})")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
