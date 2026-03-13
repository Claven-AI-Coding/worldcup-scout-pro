"""AI 预测 API 路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.ai_prediction import (
    MatchPredictionRequest,
    MatchPredictionResponse,
    TeamStrengthResponse,
)
from app.services.ai_prediction_service import AIPredictionService

router = APIRouter(prefix="/ai", tags=["ai-prediction"])


@router.post("/predict-match", response_model=MatchPredictionResponse)
async def predict_match(
    data: MatchPredictionRequest, db: AsyncSession = Depends(get_db)
):
    """预测比赛结果（使用 AI 分析）"""
    service = AIPredictionService(db)
    try:
        prediction = await service.predict_match(data.match_id)
        return prediction
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.get("/team-strength/{team_id}", response_model=TeamStrengthResponse)
async def get_team_strength(team_id: int, db: AsyncSession = Depends(get_db)):
    """获取球队实力评估"""
    service = AIPredictionService(db)
    try:
        strength = await service.get_team_strength(team_id)
        return strength
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
