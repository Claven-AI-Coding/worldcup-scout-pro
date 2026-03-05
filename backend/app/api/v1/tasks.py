"""任务签到 API"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User
from app.schemas.task import SignInResponse, TaskListResponse, TaskResponse
from app.services.task_service import complete_task, get_or_create_daily_tasks, sign_in
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("/daily", response_model=TaskListResponse)
async def get_daily_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取今日任务列表"""
    tasks = await get_or_create_daily_tasks(current_user.id, db)
    return TaskListResponse(items=tasks, total=len(tasks))


@router.post("/{task_type}/complete", response_model=TaskResponse)
async def complete_daily_task(
    task_type: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """完成指定任务"""
    task = await complete_task(current_user.id, task_type, db)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="任务不存在或已完成",
        )
    return task


@router.post("/sign-in")
async def daily_sign_in(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """每日签到"""
    result = await sign_in(current_user, db)
    if result.get("already_signed"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="今日已签到",
        )
    return result
