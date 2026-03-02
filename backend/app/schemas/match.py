from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MatchTeamInfo(BaseModel):
    """Nested team info embedded in match responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    flag_url: str | None = None


class MatchEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    match_id: int
    event_type: str
    minute: int
    player_id: int | None = None
    detail: str | None = None
    created_at: datetime


class MatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    stage: str
    group_name: str | None = None
    home_team_id: int
    away_team_id: int
    home_score: int | None = None
    away_score: int | None = None
    status: str = "upcoming"
    start_time: datetime
    venue: str | None = None
    matchday: int | None = None
    created_at: datetime

    home_team: MatchTeamInfo | None = None
    away_team: MatchTeamInfo | None = None
    events: list[MatchEventResponse] = []


class MatchListResponse(BaseModel):
    items: list[MatchResponse]
    total: int


class ReminderCreate(BaseModel):
    match_id: int
    remind_before_minutes: int = Field(default=30, ge=5, le=1440)


class ReminderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    match_id: int
    remind_before_minutes: int
    sent: bool = False
    created_at: datetime
