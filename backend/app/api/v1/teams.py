from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Player, Team
from app.schemas.player import PlayerListResponse
from app.schemas.team import TeamListResponse, TeamResponse

router = APIRouter()


@router.get("/", response_model=TeamListResponse)
async def list_teams(
    group: str | None = Query(None, description="Filter by group (A-L)"),
    confederation: str | None = Query(
        None, description="Filter by confederation (UEFA/CONMEBOL/CONCACAF/CAF/AFC/OFC)"
    ),
    search: str | None = Query(None, description="Search by team name"),
    db: AsyncSession = Depends(get_db),
):
    """List all teams with optional group filter."""
    stmt = select(Team).order_by(Team.group_name, Team.name)

    if group:
        stmt = stmt.where(Team.group_name == group.upper())
    if confederation:
        # 按大洲联盟筛选（存储在 stats JSONB 中）
        stmt = stmt.where(Team.stats["confederation"].astext == confederation.upper())
    if search:
        stmt = stmt.where(Team.name.ilike(f"%{search}%") | Team.name_en.ilike(f"%{search}%"))

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    result = await db.execute(stmt)
    teams = result.scalars().all()

    return TeamListResponse(items=teams, total=total)


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int, db: AsyncSession = Depends(get_db)):
    """Get team detail by ID."""
    result = await db.execute(select(Team).where(Team.id == team_id))
    team = result.scalar_one_or_none()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="球队不存在",
        )

    return team


@router.get("/{team_id}/players", response_model=PlayerListResponse)
async def get_team_players(team_id: int, db: AsyncSession = Depends(get_db)):
    """Get all players for a specific team."""
    # Verify team exists
    team_result = await db.execute(select(Team).where(Team.id == team_id))
    if not team_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="球队不存在",
        )

    stmt = select(Player).where(Player.team_id == team_id).order_by(Player.number, Player.name)
    result = await db.execute(stmt)
    players = result.scalars().all()

    return PlayerListResponse(items=players, total=len(players))
