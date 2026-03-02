from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PlayerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    team_id: int
    name: str
    name_en: str | None = None
    number: int | None = None
    position: str | None = None
    age: int | None = None
    club: str | None = None
    photo_url: str | None = None
    stats: dict | None = None
    created_at: datetime


class PlayerListResponse(BaseModel):
    items: list[PlayerResponse]
    total: int
