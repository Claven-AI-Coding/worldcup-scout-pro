from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PredictionCreate(BaseModel):
    match_id: int
    predicted_result: str = Field(..., pattern=r"^(home|draw|away)$")
    predicted_home_score: int | None = Field(default=None, ge=0)
    predicted_away_score: int | None = Field(default=None, ge=0)
    points_wagered: int = Field(default=100, ge=10, le=10000)


class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    match_id: int
    predicted_result: str
    predicted_home_score: int | None = None
    predicted_away_score: int | None = None
    points_wagered: int
    points_earned: int | None = None
    settled: bool = False
    created_at: datetime


class LeaderboardEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    nickname: str
    avatar: str | None = None
    total_points: int
    win_streak: int = 0
