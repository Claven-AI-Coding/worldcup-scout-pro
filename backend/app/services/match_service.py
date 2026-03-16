"""Match service -- live matches, score updates, group standings."""

from typing import Any

import redis.asyncio as aioredis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models.match import Match
from app.models.team import Team


async def get_live_matches(db: AsyncSession) -> list[Match]:
    """Return all matches whose status is ``live``, eagerly loading team relations."""
    result = await db.execute(
        select(Match)
        .options(selectinload(Match.home_team), selectinload(Match.away_team))
        .where(Match.status == "live")
        .order_by(Match.start_time)
    )
    return list(result.scalars().all())


async def update_match_score(
    db: AsyncSession,
    match_id: int,
    home_score: int,
    away_score: int,
) -> Match | None:
    """Update the score for a match and publish the change via Redis Pub/Sub.

    Returns:
        The updated ``Match`` instance, or ``None`` if the match was not found.
    """
    result = await db.execute(
        select(Match)
        .options(selectinload(Match.home_team), selectinload(Match.away_team))
        .where(Match.id == match_id)
    )
    match = result.scalar_one_or_none()
    if match is None:
        return None

    match.home_score = home_score
    match.away_score = away_score
    await db.flush()

    # Publish score update to Redis so that WebSocket subscribers receive it.
    redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        payload = (
            f'{{"match_id": {match_id}, '
            f'"home_team": "{match.home_team.name}", '
            f'"away_team": "{match.away_team.name}", '
            f'"home_score": {home_score}, '
            f'"away_score": {away_score}, '
            f'"status": "{match.status}"}}'
        )
        await redis.publish("match_scores", payload)
    finally:
        await redis.close()

    return match


async def get_standings(db: AsyncSession, group_name: str) -> list[dict[str, Any]]:
    """Calculate group standings from match results.

    For every team in the given group, compute:
    - played, won, drawn, lost
    - goals_for, goals_against, goal_difference
    - points (3 for win, 1 for draw)

    The result is sorted by points DESC, then goal difference DESC, then goals for DESC.
    """
    # Gather finished group-stage matches for this group.
    matches_result = await db.execute(
        select(Match).where(
            Match.group_name == group_name,
            Match.stage == "group",
            Match.status == "finished",
        )
    )
    matches = list(matches_result.scalars().all())

    # Fetch teams in this group.
    teams_result = await db.execute(
        select(Team).where(Team.group_name == group_name).order_by(Team.name)
    )
    teams = {t.id: t for t in teams_result.scalars().all()}

    # Build per-team stats.
    stats: dict[int, dict[str, Any]] = {}
    for team_id, team in teams.items():
        stats[team_id] = {
            "team_id": team_id,
            "team_name": team.name,
            "team_code": team.code,
            "flag_url": team.flag_url,
            "played": 0,
            "won": 0,
            "drawn": 0,
            "lost": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0,
        }

    for m in matches:
        if m.home_score is None or m.away_score is None:
            continue

        for side, opp_side in [
            (m.home_team_id, m.away_team_id),
            (m.away_team_id, m.home_team_id),
        ]:
            if side not in stats:
                continue

            is_home = side == m.home_team_id
            gf = m.home_score if is_home else m.away_score
            ga = m.away_score if is_home else m.home_score

            stats[side]["played"] += 1
            stats[side]["goals_for"] += gf
            stats[side]["goals_against"] += ga

            if gf > ga:
                stats[side]["won"] += 1
                stats[side]["points"] += 3
            elif gf == ga:
                stats[side]["drawn"] += 1
                stats[side]["points"] += 1
            else:
                stats[side]["lost"] += 1

    # Derive goal difference and sort.
    for s in stats.values():
        s["goal_difference"] = s["goals_for"] - s["goals_against"]

    standings = sorted(
        stats.values(),
        key=lambda s: (s["points"], s["goal_difference"], s["goals_for"]),
        reverse=True,
    )
    return standings
