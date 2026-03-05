"""积分流水 API"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User
from app.models.point_record import PointRecord
from app.schemas.point import PointRecordListResponse
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("/records", response_model=PointRecordListResponse)
async def get_point_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取积分流水记录"""
    stmt = (
        select(PointRecord)
        .where(PointRecord.user_id == current_user.id)
        .order_by(PointRecord.created_at.desc())
    )

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar_one()

    result = await db.execute(stmt.offset(skip).limit(limit))
    items = result.scalars().all()

    return PointRecordListResponse(items=items, total=total)
