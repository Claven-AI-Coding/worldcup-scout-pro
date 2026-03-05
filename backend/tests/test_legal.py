"""法律文本与壁纸模块测试"""

import pytest


@pytest.mark.asyncio
async def test_privacy_policy(client):
    """隐私政策"""
    resp = await client.get("/api/v1/legal/privacy-policy")
    assert resp.status_code == 200
    data = resp.json()
    assert "title" in data
    assert "content" in data


@pytest.mark.asyncio
async def test_user_agreement(client):
    """用户协议"""
    resp = await client.get("/api/v1/legal/user-agreement")
    assert resp.status_code == 200
    data = resp.json()
    assert "title" in data


@pytest.mark.asyncio
async def test_disclaimer(client):
    """免责声明"""
    resp = await client.get("/api/v1/legal/disclaimer")
    assert resp.status_code == 200
    data = resp.json()
    assert "title" in data


@pytest.mark.asyncio
async def test_wallpaper_templates(client):
    """壁纸模板列表"""
    resp = await client.get("/api/v1/wallpapers/templates")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 4
    assert all("name" in t for t in data)


@pytest.mark.asyncio
async def test_wallpaper_gallery_empty(client):
    """壁纸画廊（空）"""
    resp = await client.get("/api/v1/wallpapers/gallery")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_health_check(client):
    """健康检查"""
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
