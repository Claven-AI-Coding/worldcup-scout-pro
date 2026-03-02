from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Player
from app.schemas.player import PlayerListResponse, PlayerResponse

router = APIRouter()


@router.get("/", response_model=PlayerListResponse)
async def search_players(
    name: str | None = Query(None, description="Search by player name (Chinese or English)"),
    position: str | None = Query(None, description="Filter by position"),
    team_id: int | None = Query(None, description="Filter by team ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Search players with optional name, position, and team filters."""
    stmt = select(Player).order_by(Player.team_id, Player.number, Player.name)

    if name:
        stmt = stmt.where(
            or_(
                Player.name.ilike(f"%{name}%"),
                Player.name_en.ilike(f"%{name}%"),
            )
        )
    if position:
        stmt = stmt.where(Player.position == position)
    if team_id:
        stmt = stmt.where(Player.team_id == team_id)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    players = result.scalars().all()

    return PlayerListResponse(items=players, total=total)


@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(player_id: int, db: AsyncSession = Depends(get_db)):
    """Get player detail by ID."""
    result = await db.execute(select(Player).where(Player.id == player_id))
    player = result.scalar_one_or_none()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="球员不存在",
        )

    return player
