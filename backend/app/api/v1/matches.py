from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Match, MatchEvent, Reminder, Team, User
from app.schemas.match import (
    MatchEventResponse,
    MatchListResponse,
    MatchResponse,
    ReminderCreate,
    ReminderResponse,
)
from app.services.ai_analysis import generate_match_prediction
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=MatchListResponse)
async def list_matches(
    stage: str | None = Query(
        None,
        description="Filter by stage: group, round_32, round_16, quarter, semi, third_place, final",
    ),
    group: str | None = Query(None, description="Filter by group (A-L)"),
    team_id: int | None = Query(None, description="Filter by team ID"),
    date_filter: date | None = Query(None, alias="date", description="Filter by date (YYYY-MM-DD)"),
    match_status: str | None = Query(
        None, alias="status", description="Filter by status: upcoming, live, finished"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List matches with optional filters for stage, group, team, date, and status."""
    stmt = (
        select(Match)
        .options(
            selectinload(Match.home_team),
            selectinload(Match.away_team),
            selectinload(Match.events),
        )
        .order_by(Match.start_time)
    )

    if stage:
        stmt = stmt.where(Match.stage == stage)
    if group:
        stmt = stmt.where(Match.group_name == group.upper())
    if team_id:
        stmt = stmt.where((Match.home_team_id == team_id) | (Match.away_team_id == team_id))
    if date_filter:
        stmt = stmt.where(func.date(Match.start_time) == date_filter)
    if match_status:
        stmt = stmt.where(Match.status == match_status)

    # Count total before pagination
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    matches = result.scalars().all()

    return MatchListResponse(items=matches, total=total)


@router.get("/standings")
async def get_standings(
    group: str | None = Query(None, description="Filter by group (A-L)"),
    db: AsyncSession = Depends(get_db),
):
    """Get group standings calculated from match results.

    Returns a dict of group_name -> list of team standings.
    """
    # Fetch all group-stage finished matches
    stmt = (
        select(Match)
        .options(selectinload(Match.home_team), selectinload(Match.away_team))
        .where(Match.stage == "group", Match.status == "finished")
    )
    if group:
        stmt = stmt.where(Match.group_name == group.upper())

    result = await db.execute(stmt)
    matches = result.scalars().all()

    # Build standings from match results
    standings: dict[str, dict[int, dict]] = {}

    # Initialize teams from teams table
    team_stmt = select(Team)
    if group:
        team_stmt = team_stmt.where(Team.group_name == group.upper())
    else:
        team_stmt = team_stmt.where(Team.group_name.isnot(None))
    team_result = await db.execute(team_stmt)
    teams = team_result.scalars().all()

    for team in teams:
        grp = team.group_name or "?"
        if grp not in standings:
            standings[grp] = {}
        standings[grp][team.id] = {
            "team_id": team.id,
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

    for match in matches:
        grp = match.group_name or "?"
        if grp not in standings:
            continue

        home_id = match.home_team_id
        away_id = match.away_team_id
        home_score = match.home_score or 0
        away_score = match.away_score or 0

        for tid in (home_id, away_id):
            if tid not in standings.get(grp, {}):
                continue

        if home_id in standings[grp]:
            standings[grp][home_id]["played"] += 1
            standings[grp][home_id]["goals_for"] += home_score
            standings[grp][home_id]["goals_against"] += away_score

        if away_id in standings[grp]:
            standings[grp][away_id]["played"] += 1
            standings[grp][away_id]["goals_for"] += away_score
            standings[grp][away_id]["goals_against"] += home_score

        if home_score > away_score:
            if home_id in standings[grp]:
                standings[grp][home_id]["won"] += 1
                standings[grp][home_id]["points"] += 3
            if away_id in standings[grp]:
                standings[grp][away_id]["lost"] += 1
        elif home_score < away_score:
            if away_id in standings[grp]:
                standings[grp][away_id]["won"] += 1
                standings[grp][away_id]["points"] += 3
            if home_id in standings[grp]:
                standings[grp][home_id]["lost"] += 1
        else:
            if home_id in standings[grp]:
                standings[grp][home_id]["drawn"] += 1
                standings[grp][home_id]["points"] += 1
            if away_id in standings[grp]:
                standings[grp][away_id]["drawn"] += 1
                standings[grp][away_id]["points"] += 1

    # Compute goal difference and sort
    result_standings = {}
    for grp, team_map in sorted(standings.items()):
        for entry in team_map.values():
            entry["goal_difference"] = entry["goals_for"] - entry["goals_against"]
        sorted_teams = sorted(
            team_map.values(),
            key=lambda t: (t["points"], t["goal_difference"], t["goals_for"]),
            reverse=True,
        )
        result_standings[grp] = sorted_teams

    return result_standings


@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(match_id: int, db: AsyncSession = Depends(get_db)):
    """Get match detail with events and team info."""
    stmt = (
        select(Match)
        .options(
            selectinload(Match.home_team),
            selectinload(Match.away_team),
            selectinload(Match.events),
        )
        .where(Match.id == match_id)
    )
    result = await db.execute(stmt)
    match = result.scalar_one_or_none()

    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="比赛不存在",
        )

    return match


@router.get("/{match_id}/events", response_model=list[MatchEventResponse])
async def get_match_events(match_id: int, db: AsyncSession = Depends(get_db)):
    """Get events for a specific match, ordered by minute."""
    # Verify match exists
    match_result = await db.execute(select(Match).where(Match.id == match_id))
    if not match_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="比赛不存在",
        )

    stmt = select(MatchEvent).where(MatchEvent.match_id == match_id).order_by(MatchEvent.minute)
    result = await db.execute(stmt)
    events = result.scalars().all()
    return events


@router.post(
    "/{match_id}/remind", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED
)
async def set_reminder(
    match_id: int,
    payload: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Set a reminder for a match (authenticated)."""
    # Verify match exists
    match_result = await db.execute(select(Match).where(Match.id == match_id))
    match = match_result.scalar_one_or_none()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="比赛不存在",
        )

    if match.status == "finished":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="比赛已结束，无法设置提醒",
        )

    # Check if reminder already exists
    existing_stmt = select(Reminder).where(
        Reminder.user_id == current_user.id,
        Reminder.match_id == match_id,
    )
    existing_result = await db.execute(existing_stmt)
    existing = existing_result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="已设置过该比赛的提醒",
        )

    reminder = Reminder(
        user_id=current_user.id,
        match_id=match_id,
        remind_before_minutes=payload.remind_before_minutes,
    )
    db.add(reminder)
    await db.flush()
    await db.refresh(reminder)
    return reminder


@router.post("/subscribe-team/{team_id}", status_code=status.HTTP_201_CREATED)
async def subscribe_team_matches(
    team_id: int,
    remind_before_minutes: int = Query(30, ge=5, le=1440, description="提醒提前分钟数"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """一键订阅球队所有未开始比赛的提醒"""
    # 验证球队存在
    team_result = await db.execute(select(Team).where(Team.id == team_id))
    team = team_result.scalar_one_or_none()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="球队不存在")

    # 查询该球队所有未结束的比赛
    match_stmt = select(Match).where(
        ((Match.home_team_id == team_id) | (Match.away_team_id == team_id)),
        Match.status != "finished",
    )
    match_result = await db.execute(match_stmt)
    matches = match_result.scalars().all()

    if not matches:
        return {"message": "该球队暂无未来赛事", "subscribed_count": 0}

    # 查询已有的提醒
    existing_stmt = select(Reminder.match_id).where(
        Reminder.user_id == current_user.id,
        Reminder.match_id.in_([m.id for m in matches]),
    )
    existing_result = await db.execute(existing_stmt)
    existing_match_ids = set(existing_result.scalars().all())

    # 批量创建提醒
    new_count = 0
    for match in matches:
        if match.id not in existing_match_ids:
            db.add(
                Reminder(
                    user_id=current_user.id,
                    match_id=match.id,
                    remind_before_minutes=remind_before_minutes,
                )
            )
            new_count += 1

    await db.flush()
    return {
        "message": f"已订阅 {team.name} 全部赛事提醒",
        "team_name": team.name,
        "subscribed_count": new_count,
        "already_subscribed": len(existing_match_ids),
        "total_matches": len(matches),
    }


@router.get("/{match_id}/prediction")
async def get_match_prediction(
    match_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取比赛 AI 赛果预测（胜率 + 比分区间）"""

    stmt = (
        select(Match)
        .options(selectinload(Match.home_team), selectinload(Match.away_team))
        .where(Match.id == match_id)
    )
    result = await db.execute(stmt)
    match = result.scalar_one_or_none()

    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="比赛不存在")

    prediction = await generate_match_prediction(
        home_team=match.home_team.name,
        away_team=match.away_team.name,
        home_stats=match.home_team.stats,
        away_stats=match.away_team.stats,
        match_id=match_id,
    )

    return prediction
