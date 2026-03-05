"""排行榜 API — 射手榜 / 助攻榜"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Player

router = APIRouter()


@router.get("/scorers")
async def get_scorers(
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """射手榜 — 按进球数排序"""
    stmt = (
        select(Player)
        .options(selectinload(Player.team))
        .order_by(Player.stats["goals"].as_integer().desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    players = result.scalars().all()

    return [
        {
            "rank": idx + 1,
            "player_id": p.id,
            "player_name": p.name,
            "player_name_en": p.name_en,
            "team_id": p.team_id,
            "team_name": p.team.name if p.team else None,
            "team_code": p.team.code if p.team else None,
            "goals": (p.stats or {}).get("goals", 0),
            "appearances": (p.stats or {}).get("appearances", 0),
            "position": p.position,
        }
        for idx, p in enumerate(players)
    ]


@router.get("/assists")
async def get_assists(
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """助攻榜 — 按助攻数排序"""
    stmt = (
        select(Player)
        .options(selectinload(Player.team))
        .order_by(Player.stats["assists"].as_integer().desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    players = result.scalars().all()

    return [
        {
            "rank": idx + 1,
            "player_id": p.id,
            "player_name": p.name,
            "player_name_en": p.name_en,
            "team_id": p.team_id,
            "team_name": p.team.name if p.team else None,
            "team_code": p.team.code if p.team else None,
            "assists": (p.stats or {}).get("assists", 0),
            "appearances": (p.stats or {}).get("appearances", 0),
            "position": p.position,
        }
        for idx, p in enumerate(players)
    ]
