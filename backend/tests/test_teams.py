"""球队模块测试"""

import pytest

from app.models import Player


@pytest.fixture
async def test_player(db_session, test_teams):
    """创建测试球员"""
    team_a, _ = test_teams
    player = Player(
        team_id=team_a.id,
        name="内马尔",
        name_en="Neymar Jr",
        number=10,
        position="FW",
        age=34,
        club="桑托斯",
        stats={"goals": 5, "assists": 3, "appearances": 10, "yellow_cards": 2, "red_cards": 0},
    )
    db_session.add(player)
    await db_session.commit()
    await db_session.refresh(player)
    return player


@pytest.mark.asyncio
async def test_list_teams(client, test_teams):
    """列出球队"""
    resp = await client.get("/api/v1/teams/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2


@pytest.mark.asyncio
async def test_filter_teams_by_group(client, test_teams):
    """按小组筛选球队"""
    resp = await client.get("/api/v1/teams/", params={"group": "A"})
    assert resp.status_code == 200
    assert resp.json()["total"] == 2


@pytest.mark.asyncio
async def test_search_teams(client, test_teams):
    """搜索球队"""
    resp = await client.get("/api/v1/teams/", params={"search": "巴西"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "巴西"


@pytest.mark.asyncio
async def test_get_team_detail(client, test_teams):
    """球队详情"""
    team_a, _ = test_teams
    resp = await client.get(f"/api/v1/teams/{team_a.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "巴西"
    assert data["code"] == "BRA"


@pytest.mark.asyncio
async def test_get_team_not_found(client):
    """球队不存在"""
    resp = await client.get("/api/v1/teams/99999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_team_players(client, test_player, test_teams):
    """球队球员列表"""
    team_a, _ = test_teams
    resp = await client.get(f"/api/v1/teams/{team_a.id}/players")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    assert data["items"][0]["name"] == "内马尔"


@pytest.mark.asyncio
async def test_subscribe_team_matches(client, auth_headers, test_match, test_teams):
    """一键订阅球队全赛程提醒"""
    team_a, _ = test_teams
    resp = await client.post(
        f"/api/v1/matches/subscribe-team/{team_a.id}",
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["subscribed_count"] >= 1
    assert "巴西" in data["team_name"]


@pytest.mark.asyncio
async def test_subscribe_team_matches_idempotent(client, auth_headers, test_match, test_teams):
    """重复订阅不创建重复提醒"""
    team_a, _ = test_teams
    await client.post(f"/api/v1/matches/subscribe-team/{team_a.id}", headers=auth_headers)
    resp = await client.post(f"/api/v1/matches/subscribe-team/{team_a.id}", headers=auth_headers)
    data = resp.json()
    assert data["subscribed_count"] == 0
    assert data["already_subscribed"] >= 1
