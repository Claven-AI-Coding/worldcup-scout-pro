from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    name_en: str | None = None
    code: str
    group_name: str | None = None
    flag_url: str | None = None
    coach: str | None = None
    description: str | None = None
    stats: dict | None = None
    created_at: datetime


class TeamListResponse(BaseModel):
    items: list[TeamResponse]
    total: int
