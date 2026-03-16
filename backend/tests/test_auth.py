"""认证模块测试"""

import pytest


@pytest.mark.asyncio
async def test_register_success(client):
    """注册成功"""
    resp = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser",
            "password": "password123",
            "agreed_terms": True,
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "newuser"
    assert data["agreed_terms"] is True


@pytest.mark.asyncio
async def test_register_without_agreeing_terms(client):
    """注册未同意协议应被拒绝"""
    resp = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "noterms",
            "password": "password123",
            "agreed_terms": False,
        },
    )
    assert resp.status_code == 400
    assert "同意" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_register_duplicate_username(client):
    """重复用户名注册应返回 409"""
    payload = {
        "username": "dupuser",
        "password": "password123",
        "agreed_terms": True,
    }
    resp1 = await client.post("/api/v1/auth/register", json=payload)
    assert resp1.status_code == 201

    resp2 = await client.post("/api/v1/auth/register", json=payload)
    assert resp2.status_code == 409


@pytest.mark.asyncio
async def test_register_short_password(client):
    """密码过短应返回 422"""
    resp = await client.post(
        "/api/v1/auth/register",
        json={
            "username": "shortpw",
            "password": "123",
            "agreed_terms": True,
        },
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client, test_user):
    """登录成功返回 token"""
    resp = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "test123456",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client, test_user):
    """密码错误"""
    resp = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "testuser",
            "password": "wrongpassword",
        },
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client):
    """不存在的用户"""
    resp = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "ghostuser",
            "password": "password123",
        },
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client, auth_headers):
    """获取当前用户信息"""
    resp = await client.get("/api/v1/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "testuser"
    assert data["nickname"] == "测试用户"


@pytest.mark.asyncio
async def test_get_me_no_token(client):
    """无 token 访问应返回 401 或 403"""
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code in (401, 403)
