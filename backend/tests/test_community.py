"""社区模块测试"""

import pytest

from app.models import Post, Team


@pytest.fixture
async def test_post(db_session, test_user, test_teams):
    """创建测试帖子"""
    team_a, _ = test_teams
    post = Post(
        user_id=test_user.id,
        team_id=team_a.id,
        content="测试帖子内容",
        likes=5,
        comments_count=2,
    )
    db_session.add(post)
    await db_session.commit()
    await db_session.refresh(post)
    return post


@pytest.mark.asyncio
async def test_list_team_posts(client, test_post, test_teams):
    """列出球队帖子"""
    team_a, _ = test_teams
    resp = await client.get(f"/api/v1/community/{team_a.id}/posts")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_list_team_posts_sort_hot(client, test_post, test_teams):
    """球队帖子热门排序"""
    team_a, _ = test_teams
    resp = await client.get(f"/api/v1/community/{team_a.id}/posts", params={"sort": "hot"})
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_hot_posts(client, test_post):
    """全站热门帖子"""
    resp = await client.get("/api/v1/community/hot")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_create_post(client, auth_headers, test_teams):
    """发帖"""
    team_a, _ = test_teams
    resp = await client.post("/api/v1/community/posts", headers=auth_headers, json={
        "team_id": team_a.id,
        "content": "这是一条新帖子",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["content"] == "这是一条新帖子"


@pytest.mark.asyncio
async def test_create_post_with_banned_words(client, auth_headers, test_teams, banned_words):
    """发帖包含违禁词被拦截"""
    team_a, _ = test_teams
    resp = await client.post("/api/v1/community/posts", headers=auth_headers, json={
        "team_id": team_a.id,
        "content": "这里有脏话测试内容",
    })
    assert resp.status_code == 400
    assert "违规" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_like_post(client, auth_headers, test_post):
    """点赞帖子"""
    resp = await client.post(f"/api/v1/community/posts/{test_post.id}/like", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["likes"] == test_post.likes + 1


@pytest.mark.asyncio
async def test_comment_on_post(client, auth_headers, test_post):
    """评论帖子"""
    resp = await client.post(
        f"/api/v1/community/posts/{test_post.id}/comment",
        headers=auth_headers,
        json={"content": "好帖！"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["content"] == "好帖！"


@pytest.mark.asyncio
async def test_list_comments(client, auth_headers, test_post):
    """帖子评论列表"""
    # 先评论
    await client.post(
        f"/api/v1/community/posts/{test_post.id}/comment",
        headers=auth_headers,
        json={"content": "评论1"},
    )
    resp = await client.get(f"/api/v1/community/posts/{test_post.id}/comments")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
