"""赛程模块测试"""

import pytest


@pytest.mark.asyncio
async def test_list_matches_empty(client):
    """无比赛数据时返回空列表"""
    resp = await client.get("/api/v1/matches/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_list_matches(client, test_match):
    """列出比赛"""
    resp = await client.get("/api/v1/matches/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    match = data["items"][0]
    assert match["stage"] == "group"
    assert match["group_name"] == "A"
    assert match["status"] == "upcoming"


@pytest.mark.asyncio
async def test_filter_matches_by_stage(client, test_match):
    """按赛事阶段筛选"""
    resp = await client.get("/api/v1/matches/", params={"stage": "group"})
    assert resp.status_code == 200
    assert resp.json()["total"] >= 1

    resp2 = await client.get("/api/v1/matches/", params={"stage": "final"})
    assert resp2.status_code == 200
    assert resp2.json()["total"] == 0


@pytest.mark.asyncio
async def test_filter_matches_by_group(client, test_match):
    """按小组筛选"""
    resp = await client.get("/api/v1/matches/", params={"group": "A"})
    assert resp.status_code == 200
    assert resp.json()["total"] >= 1

    resp2 = await client.get("/api/v1/matches/", params={"group": "Z"})
    assert resp2.status_code == 200
    assert resp2.json()["total"] == 0


@pytest.mark.asyncio
async def test_filter_matches_by_status(client, test_match, finished_match):
    """按状态筛选"""
    resp = await client.get("/api/v1/matches/", params={"status": "upcoming"})
    data = resp.json()
    assert data["total"] >= 1
    assert all(m["status"] == "upcoming" for m in data["items"])

    resp2 = await client.get("/api/v1/matches/", params={"status": "finished"})
    data2 = resp2.json()
    assert data2["total"] >= 1
    assert all(m["status"] == "finished" for m in data2["items"])


@pytest.mark.asyncio
async def test_get_match_detail(client, test_match):
    """获取比赛详情"""
    resp = await client.get(f"/api/v1/matches/{test_match.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == test_match.id
    assert data["venue"] == "MetLife Stadium"


@pytest.mark.asyncio
async def test_get_match_not_found(client):
    """比赛不存在"""
    resp = await client.get("/api/v1/matches/99999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_set_reminder(client, auth_headers, test_match):
    """设置比赛提醒"""
    resp = await client.post(
        f"/api/v1/matches/{test_match.id}/remind",
        headers=auth_headers,
        json={"match_id": test_match.id, "remind_before_minutes": 30},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["match_id"] == test_match.id
    assert data["remind_before_minutes"] == 30


@pytest.mark.asyncio
async def test_set_reminder_duplicate(client, auth_headers, test_match):
    """重复设置提醒应返回 409"""
    payload = {"match_id": test_match.id, "remind_before_minutes": 30}
    await client.post(
        f"/api/v1/matches/{test_match.id}/remind",
        headers=auth_headers,
        json=payload,
    )
    resp = await client.post(
        f"/api/v1/matches/{test_match.id}/remind",
        headers=auth_headers,
        json=payload,
    )
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_set_reminder_finished_match(client, auth_headers, finished_match):
    """已结束比赛不能设置提醒"""
    resp = await client.post(
        f"/api/v1/matches/{finished_match.id}/remind",
        headers=auth_headers,
        json={"match_id": finished_match.id, "remind_before_minutes": 30},
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_standings(client, test_teams):
    """积分榜接口"""
    resp = await client.get("/api/v1/matches/standings")
    assert resp.status_code == 200
    data = resp.json()
    assert "A" in data
    assert len(data["A"]) == 2  # 两支球队


@pytest.mark.asyncio
async def test_standings_filter_by_group(client, test_teams):
    """积分榜按小组筛选"""
    resp = await client.get("/api/v1/matches/standings", params={"group": "A"})
    assert resp.status_code == 200
    data = resp.json()
    assert "A" in data
