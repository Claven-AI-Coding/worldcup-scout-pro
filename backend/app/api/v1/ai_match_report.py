"""AI Match Report API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.ai_match_report_service import AIMatchReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/match/{match_id}")
async def get_match_report(match_id: int, db: AsyncSession = Depends(get_db)):
    """Generate AI match report"""
    service = AIMatchReportService(db)
    try:
        return await service.generate_report(match_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")
