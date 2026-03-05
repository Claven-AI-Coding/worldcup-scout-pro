"""合规与风控测试 — 违禁词过滤、举报、法律文本"""

import pytest

from app.utils.content_filter import check_content, filter_content, reset_cache


@pytest.mark.asyncio
async def test_check_content_clean(db_session, banned_words):
    """正常内容通过检测"""
    result = await check_content("今天比赛太精彩了", db_session)
    assert result["is_clean"] is True
    assert result["matched_words"] == []


@pytest.mark.asyncio
async def test_check_content_dirty(db_session, banned_words):
    """包含违禁词被检出"""
    result = await check_content("这里有脏话测试内容", db_session)
    assert result["is_clean"] is False
    assert "脏话测试" in result["matched_words"]
    assert "profanity" in result["categories"]


@pytest.mark.asyncio
async def test_check_content_gambling(db_session, banned_words):
    """赌博违禁词检测"""
    result = await check_content("赌博推荐给大家", db_session)
    assert result["is_clean"] is False
    assert "gambling" in result["categories"]


@pytest.mark.asyncio
async def test_filter_content(db_session, banned_words):
    """违禁词替换"""
    filtered = await filter_content("这里有脏话测试内容", db_session)
    assert "脏话测试" not in filtered
    assert "**" in filtered


@pytest.mark.asyncio
async def test_check_content_with_spaces(db_session, banned_words):
    """空格干扰检测"""
    result = await check_content("脏 话 测 试", db_session)
    assert result["is_clean"] is False


@pytest.mark.asyncio
async def test_reset_cache(db_session, banned_words):
    """缓存重置后重新加载"""
    result1 = await check_content("脏话测试", db_session)
    assert result1["is_clean"] is False

    reset_cache()
    result2 = await check_content("脏话测试", db_session)
    assert result2["is_clean"] is False


# ---- 举报测试 ----

@pytest.mark.asyncio
async def test_create_report(client, auth_headers):
    """创建举报"""
    resp = await client.post(
        "/api/v1/reports/",
        headers=auth_headers,
        json={"target_type": "post", "target_id": 1, "reason": "违规内容"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["target_type"] == "post"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_create_report_invalid_type(client, auth_headers):
    """无效举报类型"""
    resp = await client.post(
        "/api/v1/reports/",
        headers=auth_headers,
        json={"target_type": "invalid", "target_id": 1, "reason": "test"},
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_create_report_duplicate(client, auth_headers):
    """重复举报应返回 409"""
    payload = {"target_type": "post", "target_id": 100, "reason": "测试"}
    resp1 = await client.post("/api/v1/reports/", headers=auth_headers, json=payload)
    assert resp1.status_code == 201

    resp2 = await client.post("/api/v1/reports/", headers=auth_headers, json=payload)
    assert resp2.status_code == 409


@pytest.mark.asyncio
async def test_my_reports(client, auth_headers):
    """查看我的举报"""
    # 先创建一条举报
    await client.post(
        "/api/v1/reports/",
        headers=auth_headers,
        json={"target_type": "user", "target_id": 999, "reason": "骚扰"},
    )

    resp = await client.get("/api/v1/reports/my", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_report_requires_auth(client):
    """举报需要认证"""
    resp = await client.post(
        "/api/v1/reports/",
        json={"target_type": "post", "target_id": 1, "reason": "test"},
    )
    assert resp.status_code in (401, 403)


# ---- 法律文本测试 ----

@pytest.mark.asyncio
async def test_privacy_policy(client):
    """隐私政策可访问"""
    resp = await client.get("/api/v1/legal/privacy-policy")
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "隐私政策"
    assert "信息收集" in data["content"]


@pytest.mark.asyncio
async def test_user_agreement(client):
    """用户协议可访问"""
    resp = await client.get("/api/v1/legal/user-agreement")
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "用户协议"
    assert "不可兑换现金" in data["content"]


@pytest.mark.asyncio
async def test_disclaimer(client):
    """免责声明可访问"""
    resp = await client.get("/api/v1/legal/disclaimer")
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "免责声明"
    assert "不构成任何投注建议" in data["content"]
