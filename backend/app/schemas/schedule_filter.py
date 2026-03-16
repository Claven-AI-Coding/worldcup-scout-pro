"""Schedule Filter Schema"""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class MatchStage(str, Enum):
    """Match stage"""

    GROUP = "group"
    ROUND_16 = "round_16"
    QUARTER = "quarter"
    SEMI = "semi"
    FINAL = "final"


class MatchStatus(str, Enum):
    """Match status"""

    UPCOMING = "upcoming"
    LIVE = "live"
    FINISHED = "finished"


class ScheduleFilterRequest(BaseModel):
    """Schedule filter request"""

    stage: MatchStage | None = None
    status: MatchStatus | None = None
    team_id: int | None = None
    group_name: str | None = Field(None, pattern="^[A-L]$")
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)


class MatchResponse(BaseModel):
    """Match response"""

    id: int
    team1_id: int
    team1_name: str
    team2_id: int
    team2_name: str
    stage: str
    group_name: str | None
    start_time: str
    venue: str | None
    status: str
    team1_score: int | None
    team2_score: int | None
    is_live: bool

    model_config = ConfigDict(from_attributes=True)


class ScheduleStatsResponse(BaseModel):
    """Schedule statistics"""

    total_matches: int
    upcoming_count: int
    live_count: int
    finished_count: int
    by_stage: dict[str, int]
    by_group: dict[str, int]
