from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Match, Prediction, User
from app.schemas.prediction import LeaderboardEntry, PredictionCreate, PredictionResponse
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("/matches/{match_id}", response_model=dict)
async def get_match_prediction_info(
    match_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get prediction statistics for a match.

    Returns the total number of predictions and the distribution
    of predicted results (home/draw/away).
    """
    # Verify match exists
    match_result = await db.execute(select(Match).where(Match.id == match_id))
    match = match_result.scalar_one_or_none()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="比赛不存在",
        )

    # Count predictions per result type
    total_stmt = select(func.count()).where(Prediction.match_id == match_id)
    total_result = await db.execute(total_stmt)
    total = total_result.scalar_one()

    home_stmt = select(func.count()).where(
        Prediction.match_id == match_id,
        Prediction.predicted_result == "home",
    )
    draw_stmt = select(func.count()).where(
        Prediction.match_id == match_id,
        Prediction.predicted_result == "draw",
    )
    away_stmt = select(func.count()).where(
        Prediction.match_id == match_id,
        Prediction.predicted_result == "away",
    )

    home_count = (await db.execute(home_stmt)).scalar_one()
    draw_count = (await db.execute(draw_stmt)).scalar_one()
    away_count = (await db.execute(away_stmt)).scalar_one()

    return {
        "match_id": match_id,
        "total_predictions": total,
        "distribution": {
            "home": home_count,
            "draw": draw_count,
            "away": away_count,
        },
        "match_status": match.status,
    }


@router.post("/", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
async def submit_prediction(
    payload: PredictionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit a prediction for a match (authenticated).

    Validates that:
    - The match exists and hasn't started yet
    - The user hasn't already predicted this match
    - The user has enough points to wager
    """
    # Verify match exists
    match_result = await db.execute(select(Match).where(Match.id == payload.match_id))
    match = match_result.scalar_one_or_none()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="比赛不存在",
        )

    # Check match hasn't started
    if match.status != "upcoming":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="比赛已开始或已结束，无法提交预测",
        )

    now = datetime.now(timezone.utc)
    if match.start_time.tzinfo and match.start_time <= now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="比赛已开始，无法提交预测",
        )

    # Check user hasn't already predicted
    existing_stmt = select(Prediction).where(
        Prediction.user_id == current_user.id,
        Prediction.match_id == payload.match_id,
    )
    existing_result = await db.execute(existing_stmt)
    if existing_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="已提交过该比赛的预测",
        )

    # Check user has enough points
    if current_user.points < payload.points_wagered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"积分不足，当前积分: {current_user.points}",
        )

    # Deduct points and create prediction
    current_user.points -= payload.points_wagered

    prediction = Prediction(
        user_id=current_user.id,
        match_id=payload.match_id,
        predicted_result=payload.predicted_result,
        predicted_home_score=payload.predicted_home_score,
        predicted_away_score=payload.predicted_away_score,
        points_wagered=payload.points_wagered,
    )
    db.add(prediction)
    await db.flush()
    await db.refresh(prediction)

    return prediction


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
async def get_leaderboard(
    type: str = Query("all-time", description="Leaderboard type: daily or all-time"),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get prediction leaderboard (daily or all-time)."""
    if type == "daily":
        # Daily leaderboard: sum points earned today
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = (
            select(
                Prediction.user_id,
                User.nickname,
                User.avatar,
                func.coalesce(func.sum(Prediction.points_earned), 0).label("total_points"),
                User.win_streak,
            )
            .join(User, Prediction.user_id == User.id)
            .where(
                Prediction.settled.is_(True),
                Prediction.created_at >= today_start,
            )
            .group_by(Prediction.user_id, User.nickname, User.avatar, User.win_streak)
            .order_by(func.coalesce(func.sum(Prediction.points_earned), 0).desc())
            .limit(limit)
        )
    else:
        # All-time leaderboard: order by total user points
        stmt = (
            select(
                User.id.label("user_id"),
                User.nickname,
                User.avatar,
                User.points.label("total_points"),
                User.win_streak,
            )
            .order_by(User.points.desc())
            .limit(limit)
        )

    result = await db.execute(stmt)
    rows = result.all()

    return [
        LeaderboardEntry(
            user_id=row.user_id,
            nickname=row.nickname,
            avatar=row.avatar,
            total_points=row.total_points,
            win_streak=row.win_streak,
        )
        for row in rows
    ]


@router.get("/my", response_model=list[PredictionResponse])
async def get_my_predictions(
    settled: bool | None = Query(None, description="Filter by settled status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the current user's predictions (authenticated)."""
    stmt = (
        select(Prediction)
        .where(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
    )

    if settled is not None:
        stmt = stmt.where(Prediction.settled == settled)

    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    predictions = result.scalars().all()

    return predictions
