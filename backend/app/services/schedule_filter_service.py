"""Schedule Filter Service"""

from datetime import datetime, timezone

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.match import Match
from app.models.team import Team
from app.schemas.schedule_filter import (
    MatchResponse,
    MatchStage,
    MatchStatus,
    ScheduleFilterRequest,
    ScheduleStatsResponse,
)


class ScheduleFilterService:
    """Schedule filtering service"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def filter_matches(
        self, request: ScheduleFilterRequest
    ) -> tuple[list[MatchResponse], int]:
        """Filter matches with various criteria"""
        query = select(Match)

        # Filter by stage
        if request.stage:
            query = query.where(Match.stage == request.stage.value)

        # Filter by status
        if request.status:
            now = datetime.now(timezone.utc)
            if request.status == MatchStatus.UPCOMING:
                query = query.where(Match.start_time > now)
            elif request.status == MatchStatus.LIVE:
                query = query.where(
                    and_(
                        Match.start_time <= now,
                        Match.end_time >= now,
                    )
                )
            elif request.status == MatchStatus.FINISHED:
                query = query.where(Match.end_time < now)

        # Filter by team
        if request.team_id:
            query = query.where(
                or_(
                    Match.team1_id == request.team_id,
                    Match.team2_id == request.team_id,
                )
            )

        # Filter by group
        if request.group_name:
            query = query.where(Match.group_name == request.group_name)

        # Get total count
        count_result = await self.db.execute(
            select(Match).where(
                *[c for c in query.whereclause.clauses]
                if query.whereclause is not None
                else []
            )
        )
        total = len(count_result.scalars().all())

        # Apply pagination
        query = query.order_by(Match.start_time).offset(request.skip).limit(request.limit)

        result = await self.db.execute(query)
        matches = result.scalars().all()

        # Convert to response
        responses = []
        for match in matches:
            # Get team names
            team1_result = await self.db.execute(
                select(Team).where(Team.id == match.team1_id)
            )
            team1 = team1_result.scalar_one_or_none()

            team2_result = await self.db.execute(
                select(Team).where(Team.id == match.team2_id)
            )
            team2 = team2_result.scalar_one_or_none()

            now = datetime.now(timezone.utc)
            is_live = match.start_time <= now <= match.end_time

            responses.append(
                MatchResponse(
                    id=match.id,
                    team1_id=match.team1_id,
                    team1_name=team1.name if team1 else "Unknown",
                    team2_id=match.team2_id,
                    team2_name=team2.name if team2 else "Unknown",
                    stage=match.stage,
                    group_name=match.group_name,
                    start_time=match.start_time.isoformat(),
                    venue=match.venue,
                    status=self._get_status(match),
                    team1_score=match.team1_score,
                    team2_score=match.team2_score,
                    is_live=is_live,
                )
            )

        return responses, total

    async def get_stats(self) -> ScheduleStatsResponse:
        """Get schedule statistics"""
        now = datetime.now(timezone.utc)

        # Get all matches
        result = await self.db.execute(select(Match))
        all_matches = result.scalars().all()

        # Count by status
        upcoming = sum(1 for m in all_matches if m.start_time > now)
        live = sum(1 for m in all_matches if m.start_time <= now <= m.end_time)
        finished = sum(1 for m in all_matches if m.end_time < now)

        # Count by stage
        by_stage = {}
        for match in all_matches:
            stage = match.stage
            by_stage[stage] = by_stage.get(stage, 0) + 1

        # Count by group
        by_group = {}
        for match in all_matches:
            if match.group_name:
                group = match.group_name
                by_group[group] = by_group.get(group, 0) + 1

        return ScheduleStatsResponse(
            total_matches=len(all_matches),
            upcoming_count=upcoming,
            live_count=live,
            finished_count=finished,
            by_stage=by_stage,
            by_group=by_group,
        )

    def _get_status(self, match: Match) -> str:
        """Get match status"""
        now = datetime.now(timezone.utc)
        if match.start_time > now:
            return "upcoming"
        elif match.start_time <= now <= match.end_time:
            return "live"
        else:
            return "finished"
