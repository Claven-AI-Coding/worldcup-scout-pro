"""Schedule Filter API"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.schedule_filter import (
    MatchResponse,
    ScheduleFilterRequest,
    ScheduleStatsResponse,
)
from app.services.schedule_filter_service import ScheduleFilterService

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.post("/filter", response_model=dict)
async def filter_matches(
    request: ScheduleFilterRequest, db: AsyncSession = Depends(get_db)
):
    """Filter matches with various criteria"""
    service = ScheduleFilterService(db)
    matches, total = await service.filter_matches(request)
    return {
        "data": matches,
        "total": total,
        "skip": request.skip,
        "limit": request.limit,
    }


@router.get("/stats", response_model=ScheduleStatsResponse)
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Get schedule statistics"""
    service = ScheduleFilterService(db)
    return await service.get_stats()
