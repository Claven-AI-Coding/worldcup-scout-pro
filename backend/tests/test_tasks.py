"""积分任务系统测试"""

from datetime import date, timedelta

import pytest

from app.models.user import User
from app.services.task_service import (
    complete_task,
    get_or_create_daily_tasks,
    grant_points,
    sign_in,
    DAILY_TASKS,
)


@pytest.mark.asyncio
async def test_get_daily_tasks_creates(db_session, test_user):
    """首次调用创建今日任务"""
    tasks = await get_or_create_daily_tasks(test_user.id, db_session)
    await db_session.commit()
    assert len(tasks) == len(DAILY_TASKS)
    assert all(t.completed is False for t in tasks)


@pytest.mark.asyncio
async def test_get_daily_tasks_idempotent(db_session, test_user):
    """重复调用不会创建重复任务"""
    tasks1 = await get_or_create_daily_tasks(test_user.id, db_session)
    await db_session.commit()
    tasks2 = await get_or_create_daily_tasks(test_user.id, db_session)
    assert len(tasks1) == len(tasks2)


@pytest.mark.asyncio
async def test_complete_task(db_session, test_user):
    """完成任务"""
    await get_or_create_daily_tasks(test_user.id, db_session)
    await db_session.commit()

    task = await complete_task(test_user.id, "view_schedule", db_session)
    await db_session.commit()
    assert task is not None
    assert task.completed is True
    assert task.completed_at is not None


@pytest.mark.asyncio
async def test_complete_task_already_done(db_session, test_user):
    """重复完成任务返回 None"""
    await get_or_create_daily_tasks(test_user.id, db_session)
    await db_session.commit()

    await complete_task(test_user.id, "view_schedule", db_session)
    await db_session.commit()
    result = await complete_task(test_user.id, "view_schedule", db_session)
    assert result is None


@pytest.mark.asyncio
async def test_complete_nonexistent_task(db_session, test_user):
    """完成不存在的任务返回 None"""
    result = await complete_task(test_user.id, "nonexistent_task", db_session)
    assert result is None


@pytest.mark.asyncio
async def test_sign_in(db_session, test_user):
    """首次签到"""
    result = await sign_in(test_user, db_session)
    await db_session.commit()
    assert result["already_signed"] is False
    assert result["points_earned"] >= 10
    assert result["consecutive_days"] == 1


@pytest.mark.asyncio
async def test_sign_in_duplicate(db_session, test_user):
    """重复签到"""
    await sign_in(test_user, db_session)
    await db_session.commit()

    result = await sign_in(test_user, db_session)
    assert result["already_signed"] is True
    assert result["points_earned"] == 0


@pytest.mark.asyncio
async def test_sign_in_streak(db_session, test_user):
    """连续签到天数累计"""
    # 模拟昨天已签到
    yesterday = date.today() - timedelta(days=1)
    test_user.daily_sign_in = yesterday
    test_user.sign_in_streak = 1
    await db_session.commit()

    result = await sign_in(test_user, db_session)
    await db_session.commit()
    assert result["already_signed"] is False
    assert result["consecutive_days"] == 2


@pytest.mark.asyncio
async def test_sign_in_streak_broken(db_session, test_user):
    """签到断签重置"""
    # 模拟 3 天前签到
    three_days_ago = date.today() - timedelta(days=3)
    test_user.daily_sign_in = three_days_ago
    test_user.sign_in_streak = 5
    await db_session.commit()

    result = await sign_in(test_user, db_session)
    await db_session.commit()
    assert result["consecutive_days"] == 1  # 断签后重置为 1


@pytest.mark.asyncio
async def test_grant_points(db_session, test_user):
    """积分发放"""
    initial_points = test_user.points
    await grant_points(test_user.id, 50, reason="test", detail="测试积分", db=db_session)
    await db_session.commit()
    await db_session.refresh(test_user)
    assert test_user.points == initial_points + 50


# ---- API 测试 ----

@pytest.mark.asyncio
async def test_daily_tasks_api(client, auth_headers):
    """每日任务 API"""
    resp = await client.get("/api/v1/tasks/daily", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == len(DAILY_TASKS)


@pytest.mark.asyncio
async def test_sign_in_api(client, auth_headers):
    """签到 API"""
    resp = await client.post("/api/v1/tasks/sign-in", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["already_signed"] is False
    assert data["points_earned"] >= 10


@pytest.mark.asyncio
async def test_sign_in_api_duplicate(client, auth_headers):
    """重复签到 API"""
    await client.post("/api/v1/tasks/sign-in", headers=auth_headers)
    resp = await client.post("/api/v1/tasks/sign-in", headers=auth_headers)
    assert resp.status_code == 400
    assert "已签到" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_complete_task_api(client, auth_headers):
    """完成任务 API"""
    # 先获取任务列表（会创建任务）
    await client.get("/api/v1/tasks/daily", headers=auth_headers)
    resp = await client.post("/api/v1/tasks/view_schedule/complete", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["completed"] is True


@pytest.mark.asyncio
async def test_point_records_api(client, auth_headers):
    """积分流水 API"""
    # 先签到获取积分
    await client.post("/api/v1/tasks/sign-in", headers=auth_headers)

    resp = await client.get("/api/v1/points/records", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
