"""任务系统服务 — 签到、每日任务、积分发放"""

from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.point_record import PointRecord
from app.models.user import User
from app.models.user_task import UserTask

# 每日任务定义
DAILY_TASKS = [
    {"task_type": "daily_sign_in", "points_reward": 10, "label": "每日签到"},
    {"task_type": "view_schedule", "points_reward": 5, "label": "查看赛程"},
    {"task_type": "share_content", "points_reward": 10, "label": "分享内容"},
    {"task_type": "join_circle", "points_reward": 5, "label": "加入圈子"},
    {"task_type": "predict_match", "points_reward": 10, "label": "参与竞猜"},
]

# 连续签到奖励
SIGN_IN_BONUS = {
    3: 5,   # 连续 3 天 +5
    7: 15,  # 连续 7 天 +15
    14: 30, # 连续 14 天 +30
    30: 100, # 连续 30 天 +100
}


async def get_or_create_daily_tasks(user_id: int, db: AsyncSession) -> list[UserTask]:
    """获取或创建今日任务列表"""
    today = date.today()

    result = await db.execute(
        select(UserTask).where(
            UserTask.user_id == user_id,
            UserTask.date == today,
        )
    )
    tasks = list(result.scalars().all())

    if not tasks:
        # 创建今日任务
        for task_def in DAILY_TASKS:
            task = UserTask(
                user_id=user_id,
                task_type=task_def["task_type"],
                points_reward=task_def["points_reward"],
                date=today,
            )
            db.add(task)
            tasks.append(task)
        await db.flush()

    return tasks


async def complete_task(user_id: int, task_type: str, db: AsyncSession) -> UserTask | None:
    """完成指定任务"""
    today = date.today()

    result = await db.execute(
        select(UserTask).where(
            UserTask.user_id == user_id,
            UserTask.task_type == task_type,
            UserTask.date == today,
            UserTask.completed == False,
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        return None

    task.completed = True
    task.completed_at = datetime.now(timezone.utc)

    # 发放积分
    await grant_points(user_id, task.points_reward, reason=task_type, detail=f"完成任务: {task_type}", db=db)

    return task


async def sign_in(user: User, db: AsyncSession) -> dict:
    """每日签到"""
    today = date.today()

    if user.daily_sign_in == today:
        return {"already_signed": True, "points_earned": 0, "consecutive_days": 0}

    # 计算连续签到天数
    if user.daily_sign_in and (today - user.daily_sign_in).days == 1:
        # 昨天签过到，连续签到天数 +1
        user.sign_in_streak += 1
    else:
        # 断签或首次签到，重置为 1
        user.sign_in_streak = 1

    consecutive = user.sign_in_streak
    user.daily_sign_in = today

    # 基础签到积分
    base_points = 10

    # 连续签到奖励
    bonus = SIGN_IN_BONUS.get(consecutive, 0)
    total_points = base_points + bonus

    await grant_points(user.id, total_points, reason="sign_in", detail=f"每日签到（+{base_points}）", db=db)

    # 完成签到任务
    await complete_task(user.id, "daily_sign_in", db)

    return {
        "already_signed": False,
        "points_earned": total_points,
        "consecutive_days": consecutive,
        "total_points": user.points,
    }


async def grant_points(
    user_id: int,
    amount: int,
    reason: str,
    detail: str | None = None,
    db: AsyncSession = None,
) -> None:
    """发放积分（正数=获取，负数=扣除）"""
    # 更新用户积分
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        user.points += amount

    # 记录积分流水
    record = PointRecord(
        user_id=user_id,
        amount=amount,
        reason=reason,
        detail=detail,
    )
    db.add(record)
