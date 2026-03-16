"""Data synchronization service -- sync matches, teams, and live scores from Football-Data.org."""

import logging
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.match import Match
from app.models.team import Team
from app.utils.football_api import FootballDataClient

logger = logging.getLogger(__name__)

# FIFA World Cup 2026 competition id on Football-Data.org
WC_COMPETITION_ID = 2000


async def _upsert_team(db: AsyncSession, team_data: dict[str, Any]) -> Team:
    """Insert or update a team based on its ``code``."""
    code = team_data.get("tla", team_data.get("shortName", ""))
    result = await db.execute(select(Team).where(Team.code == code))
    team = result.scalar_one_or_none()

    if team is None:
        team = Team(
            name=team_data.get("shortName", team_data.get("name", "")),
            name_en=team_data.get("name"),
            code=code,
            flag_url=team_data.get("crest"),
            coach=team_data.get("coach", {}).get("name") if team_data.get("coach") else None,
        )
        db.add(team)
        await db.flush()
    else:
        team.name_en = team_data.get("name", team.name_en)
        team.flag_url = team_data.get("crest", team.flag_url)
        if team_data.get("coach"):
            team.coach = team_data["coach"].get("name", team.coach)
        await db.flush()

    return team


async def sync_teams(db: AsyncSession) -> int:
    """Sync all teams for the World Cup competition.

    Returns:
        Number of teams synced.
    """
    client = FootballDataClient()
    data = await client.get_teams(WC_COMPETITION_ID)
    teams = data.get("teams", [])

    count = 0
    for team_data in teams:
        await _upsert_team(db, team_data)
        count += 1

    logger.info("Synced %d teams", count)
    return count


def _parse_iso_datetime(dt_str: str | None) -> datetime | None:
    """Parse an ISO 8601 datetime string to a timezone-aware datetime."""
    if not dt_str:
        return None
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))


def _map_api_status(api_status: str) -> str:
    """Map Football-Data.org match status to the internal status enum."""
    mapping: dict[str, str] = {
        "SCHEDULED": "upcoming",
        "TIMED": "upcoming",
        "IN_PLAY": "live",
        "PAUSED": "live",
        "FINISHED": "finished",
        "POSTPONED": "upcoming",
        "CANCELLED": "finished",
        "SUSPENDED": "live",
        "AWARDED": "finished",
    }
    return mapping.get(api_status, "upcoming")


async def sync_matches(db: AsyncSession) -> int:
    """Sync match data from the external Football-Data.org API.

    Uses an upsert approach keyed on ``matchday``, ``home_team_id`` and ``away_team_id``.

    Returns:
        Number of matches synced.
    """
    client = FootballDataClient()
    data = await client.get_matches(WC_COMPETITION_ID)
    api_matches = data.get("matches", [])

    count = 0
    for m in api_matches:
        # Resolve home/away teams by code.
        home_code = m.get("homeTeam", {}).get("tla", "")
        away_code = m.get("awayTeam", {}).get("tla", "")

        home_team_result = await db.execute(select(Team).where(Team.code == home_code))
        home_team = home_team_result.scalar_one_or_none()

        away_team_result = await db.execute(select(Team).where(Team.code == away_code))
        away_team = away_team_result.scalar_one_or_none()

        if home_team is None or away_team is None:
            logger.warning(
                "Skipping match: team not found (home=%s, away=%s)", home_code, away_code
            )
            continue

        # Determine start time.
        start_time = _parse_iso_datetime(m.get("utcDate"))
        if start_time is None:
            continue

        # Upsert logic -- match uniqueness by matchday + teams.
        matchday = m.get("matchday")
        stage_raw = m.get("stage", "GROUP_STAGE")
        stage = _map_stage(stage_raw)
        group_raw = m.get("group")
        group_name = group_raw[-1] if group_raw else None  # "GROUP_A" -> "A"

        existing_result = await db.execute(
            select(Match).where(
                Match.home_team_id == home_team.id,
                Match.away_team_id == away_team.id,
                Match.matchday == matchday,
            )
        )
        match = existing_result.scalar_one_or_none()

        score = m.get("score", {})
        full_time = score.get("fullTime", {})
        home_score = full_time.get("home")
        away_score = full_time.get("away")
        status = _map_api_status(m.get("status", "SCHEDULED"))
        venue = m.get("venue")

        if match is None:
            match = Match(
                stage=stage,
                group_name=group_name,
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                home_score=home_score,
                away_score=away_score,
                status=status,
                start_time=start_time,
                venue=venue,
                matchday=matchday,
            )
            db.add(match)
        else:
            match.home_score = home_score
            match.away_score = away_score
            match.status = status
            match.start_time = start_time
            match.venue = venue
            match.stage = stage
            match.group_name = group_name

        await db.flush()
        count += 1

    logger.info("Synced %d matches", count)
    return count


def _map_stage(api_stage: str) -> str:
    """Map Football-Data.org stage names to internal stage values."""
    mapping: dict[str, str] = {
        "GROUP_STAGE": "group",
        "LAST_16": "round_16",
        "QUARTER_FINALS": "quarter",
        "SEMI_FINALS": "semi",
        "THIRD_PLACE": "third_place",
        "FINAL": "final",
    }
    return mapping.get(api_stage, "group")


async def sync_live_scores(db: AsyncSession) -> int:
    """Sync live scores for matches currently in progress.

    Returns:
        Number of matches updated.
    """
    client = FootballDataClient()
    data = await client.get_matches(WC_COMPETITION_ID, status="LIVE")
    api_matches = data.get("matches", [])

    count = 0
    for m in api_matches:
        home_code = m.get("homeTeam", {}).get("tla", "")
        away_code = m.get("awayTeam", {}).get("tla", "")

        home_team_result = await db.execute(select(Team).where(Team.code == home_code))
        home_team = home_team_result.scalar_one_or_none()

        away_team_result = await db.execute(select(Team).where(Team.code == away_code))
        away_team = away_team_result.scalar_one_or_none()

        if home_team is None or away_team is None:
            continue

        # Find the match in our database.
        match_result = await db.execute(
            select(Match).where(
                Match.home_team_id == home_team.id,
                Match.away_team_id == away_team.id,
                Match.status.in_(["upcoming", "live"]),
            )
        )
        match = match_result.scalar_one_or_none()
        if match is None:
            continue

        score = m.get("score", {})
        full_time = score.get("fullTime", {})
        match.home_score = full_time.get("home", match.home_score)
        match.away_score = full_time.get("away", match.away_score)
        match.status = "live"
        await db.flush()
        count += 1

    logger.info("Synced live scores for %d matches", count)
    return count
