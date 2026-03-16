"""举报模块测试"""

import pytest

from app.models import Post


@pytest.fixture
async def test_post_for_report(db_session, test_user, test_teams):
    """创建测试帖子用于举报"""
    team_a, _ = test_teams
    post = Post(user_id=test_user.id, team_id=team_a.id, content="可疑帖子")
    db_session.add(post)
    await db_session.commit()
    await db_session.refresh(post)
    return post


@pytest.mark.asyncio
async def test_create_report(client, auth_headers, test_post_for_report):
    """举报帖子"""
    resp = await client.post(
        "/api/v1/reports/",
        headers=auth_headers,
        json={
            "target_type": "post",
            "target_id": test_post_for_report.id,
            "reason": "包含不当内容",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["target_type"] == "post"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_duplicate_report(client, auth_headers, test_post_for_report):
    """重复举报同一目标"""
    payload = {
        "target_type": "post",
        "target_id": test_post_for_report.id,
        "reason": "垃圾内容",
    }
    resp1 = await client.post("/api/v1/reports/", headers=auth_headers, json=payload)
    assert resp1.status_code == 201

    resp2 = await client.post("/api/v1/reports/", headers=auth_headers, json=payload)
    assert resp2.status_code == 409


@pytest.mark.asyncio
async def test_list_my_reports(client, auth_headers, test_post_for_report):
    """我的举报记录"""
    await client.post(
        "/api/v1/reports/",
        headers=auth_headers,
        json={
            "target_type": "post",
            "target_id": test_post_for_report.id,
            "reason": "测试",
        },
    )
    resp = await client.get("/api/v1/reports/my", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
